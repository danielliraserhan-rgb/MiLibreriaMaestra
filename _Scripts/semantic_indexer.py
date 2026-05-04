#!/usr/bin/env python3
"""
semantic_indexer.py — Módulo 1: índice semántico ChromaDB para notas ZK
Uso:
  python _Scripts/semantic_indexer.py --mode index
  python _Scripts/semantic_indexer.py --mode update
  python _Scripts/semantic_indexer.py --mode query --q "regeneración en Juan 3"
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import frontmatter
import chromadb
from sentence_transformers import SentenceTransformer

VAULT_ROOT = Path(__file__).parent.parent
CHROMA_PATH = VAULT_ROOT / "_Skills" / "semantic_index"
ZK_PASTORAL = VAULT_ROOT / "09_Zettelkasten" / "pastoral"
INDEX_META_PATH = CHROMA_PATH / "index_meta.json"

MODEL_NAME = "intfloat/multilingual-e5-small"
ALLOWED_COLLECTIONS = ("zk_pastoral", "zk_academico")


def get_client() -> chromadb.PersistentClient:
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PATH))


def get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def _assert_collection(name: str):
    if name not in ALLOWED_COLLECTIONS:
        raise ValueError(
            f"Guard: colección '{name}' no permitida. Solo: {ALLOWED_COLLECTIONS}"
        )


def get_or_create_collection(client: chromadb.PersistentClient, name: str):
    _assert_collection(name)
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def parse_zk_note(path: Path) -> dict | None:
    try:
        post = frontmatter.load(str(path))
    except Exception:
        return None

    meta = post.metadata
    body = post.content.strip()

    # B4+B5: fallback a path.stem si title ausente, vacío o None
    _title_raw = meta.get("title")
    titulo = str(_title_raw) if _title_raw else path.stem
    tema = str(meta.get("tema", ""))
    libro = str(meta.get("libro_biblico_principal", ""))
    dominio = str(meta.get("dominio", "pastoral"))
    fecha = str(meta.get("fecha", ""))

    versiculos = meta.get("versiculos_citados", [])
    if not isinstance(versiculos, list):
        versiculos = []

    temas_principales = meta.get("temas_principales", [])
    if not isinstance(temas_principales, list):
        temas_principales = []

    temas_joined = ", ".join(str(t) for t in temas_principales)
    embed_text = f"passage: {titulo}. {temas_joined}. {body[:500]}"

    return {
        "id": path.stem,
        "titulo": titulo,
        "dominio": dominio,
        "tema": tema,
        "libro_biblico_principal": libro,
        "versiculos_citados": json.dumps(versiculos, ensure_ascii=False),
        "temas_principales": json.dumps(temas_principales, ensure_ascii=False),
        "fecha_creacion": fecha,
        "embed_text": embed_text,
        "mtime": path.stat().st_mtime,
    }


def load_index_meta() -> dict:
    if INDEX_META_PATH.exists():
        with open(INDEX_META_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_index_meta(note_count: int, collection_names: list) -> dict:
    meta = {
        "indexed_at": datetime.now(timezone.utc).isoformat(),
        "note_count": note_count,
        "model": MODEL_NAME,
        "collection_names": collection_names,
    }
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    with open(INDEX_META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return meta


def _build_metadata_record(d: dict) -> dict:
    return {
        "id": d["id"],
        "titulo": d["titulo"],
        "dominio": d["dominio"],
        "tema": d["tema"],
        "libro_biblico_principal": d["libro_biblico_principal"],
        "versiculos_citados": d["versiculos_citados"],
        "temas_principales": d["temas_principales"],
        "fecha_creacion": d["fecha_creacion"],
        "indexed_at": datetime.now(timezone.utc).isoformat(),
    }


def cmd_index(client: chromadb.PersistentClient, model: SentenceTransformer):
    """Rebuild full index from scratch."""
    try:
        client.delete_collection("zk_pastoral")
    except Exception:
        pass

    col = get_or_create_collection(client, "zk_pastoral")
    get_or_create_collection(client, "zk_academico")  # vacía

    notes = sorted(ZK_PASTORAL.glob("*.md"))
    if not notes:
        print(f"No se encontraron notas en {ZK_PASTORAL}")
        return

    parsed = [parse_zk_note(p) for p in notes]
    parsed = [d for d in parsed if d is not None]

    print(f"Indexando {len(parsed)} notas...")

    ids = [d["id"] for d in parsed]
    texts = [d["embed_text"] for d in parsed]
    metadatas = [_build_metadata_record(d) for d in parsed]

    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    # B3: proteger batch — guardar meta solo si col.add() tiene éxito
    try:
        col.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts)
    except Exception as e:
        print(f"Error durante col.add(): {e}")
        print("El índice puede estar incompleto. Ejecuta --mode index para reconstruir.")
        sys.exit(1)

    meta = save_index_meta(len(parsed), ["zk_pastoral", "zk_academico"])
    print(f"✓ Indexadas {len(parsed)} notas | {meta['indexed_at']}")


def cmd_update(client: chromadb.PersistentClient, model: SentenceTransformer):
    """Incremental update: only re-index notes newer than indexed_at."""
    index_meta = load_index_meta()
    last_indexed = index_meta.get("indexed_at")

    if not last_indexed:
        print("No hay índice previo. Ejecutando index completo...")
        cmd_index(client, model)
        return

    last_ts = datetime.fromisoformat(last_indexed).timestamp()
    col = get_or_create_collection(client, "zk_pastoral")
    get_or_create_collection(client, "zk_academico")

    notes = sorted(ZK_PASTORAL.glob("*.md"))
    updated = [p for p in notes if p.stat().st_mtime > last_ts]

    if not updated:
        print("No hay notas nuevas desde el último índice.")
        return

    print(f"Actualizando {len(updated)} notas...")
    raw_parsed = [(p, parse_zk_note(p)) for p in updated]
    # Bug 1: advertir sobre notas que fallan parse — sin aviso quedarían excluidas
    for path, result in raw_parsed:
        if result is None:
            print(f"WARN [parse fallido, requiere --mode index]: {path.name}")
    parsed = [d for _, d in raw_parsed if d is not None]

    for d in parsed:
        meta_record = _build_metadata_record(d)
        embedding = model.encode([d["embed_text"]])[0].tolist()
        try:
            col.update(
                ids=[d["id"]],
                embeddings=[embedding],
                metadatas=[meta_record],
                documents=[d["embed_text"]],
            )
        except Exception:
            col.add(
                ids=[d["id"]],
                embeddings=[embedding],
                metadatas=[meta_record],
                documents=[d["embed_text"]],
            )

    total = col.count()
    save_index_meta(total, ["zk_pastoral", "zk_academico"])
    print(f"✓ Actualizadas {len(parsed)} notas | Total en índice: {total}")


def cmd_query(
    client: chromadb.PersistentClient,
    model: SentenceTransformer,
    query_text: str,
    n_results: int = 5,
    collection: str = "zk_pastoral",  # B7: colección seleccionable
):
    """Query a collection and print ranked results."""
    col = get_or_create_collection(client, collection)

    if col.count() == 0:
        print(f"La colección '{collection}' está vacía. Ejecuta --mode index primero.")
        return

    query_embedding = model.encode([f"query: {query_text}"])[0].tolist()

    # Bug 2: almacenar count una vez para evitar doble llamada y posible TOCTOU
    count = col.count()
    try:
        results = col.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count),
            include=["metadatas", "distances"],
        )
    except Exception as e:
        print(f"Error al consultar ChromaDB: {e}")
        print("Conexiones semánticas no disponibles. Las demás funciones siguen activas.")
        return

    print(f'\nResultados para: "{query_text}" [{collection}]\n')
    print(f"{'ID':<30} {'Titulo':<45} {'Tema':<28} {'Score':>6}")
    print("-" * 115)

    for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
        score = 1 - dist  # cosine distance → similarity
        doc_id = meta.get("id", "")[:28]
        titulo = meta.get("titulo", "")[:43]
        tema = meta.get("tema", "")[:26]
        print(f"{doc_id:<30} {titulo:<45} {tema:<28} {score:>6.3f}")


def main():
    parser = argparse.ArgumentParser(description="Semantic indexer — MiLibreriaMaestra")
    parser.add_argument("--mode", choices=["index", "update", "query"], required=True)
    parser.add_argument("--q", type=str, help="Texto de búsqueda (requerido para --mode query)")
    parser.add_argument("--n", type=int, default=5, help="Número de resultados (query mode)")
    # B7: colección seleccionable — por defecto pastoral, permite academico en el futuro
    parser.add_argument(
        "--collection",
        choices=list(ALLOWED_COLLECTIONS),
        default="zk_pastoral",
        help="Colección ChromaDB a consultar (default: zk_pastoral)",
    )
    args = parser.parse_args()

    # B2: inicialización de ChromaDB con mensaje amigable si falla
    try:
        client = get_client()
    except Exception as e:
        print(f"Error: no se pudo inicializar ChromaDB — {e}")
        print("Verifica que _Skills/semantic_index/ no esté corrompido o que haya espacio en disco.")
        sys.exit(1)

    model = get_model()

    if args.mode == "index":
        cmd_index(client, model)
    elif args.mode == "update":
        cmd_update(client, model)
    elif args.mode == "query":
        if not args.q:
            print("Error: --q requerido para --mode query")
            sys.exit(1)
        cmd_query(client, model, args.q, args.n, args.collection)


if __name__ == "__main__":
    main()
