#!/usr/bin/env python3
"""
bridge_linker.py — Módulo 2: vincula archivos Inbox con notas puente en Temas/
Matching 3 tiers: (1) Jaccard keywords, (2) versículos compartidos, (3) semántico ChromaDB
NUNCA modifica archivos en Inbox/ (salvo inject --confirm que agrega nota_puente al YAML)

Uso:
  python _Scripts/bridge_linker.py --mode scan
  python _Scripts/bridge_linker.py --mode propose
  python _Scripts/bridge_linker.py --mode inject --confirm
"""

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import frontmatter

VAULT_ROOT = Path(__file__).parent.parent
INBOX_DIR = VAULT_ROOT / "Inbox"
TEMAS_DIR = VAULT_ROOT / "Temas"
PROPOSALS_PATH = VAULT_ROOT / "_Skills" / "bridge_proposals.json"
CHROMA_PATH = VAULT_ROOT / "_Skills" / "semantic_index"

TRIAGE_DESTINO = "Temas/07_PredicacionesDevocionales/04_NotasSinProcesar/"
TRIAGE_PARAMS = {
    "tipo": "clase_en_vivo",
    "tema": "07_PredicacionesDevocionales",
    "dominio": "pastoral",
    "modo": "7-grupos-conexion",
    "destino": TRIAGE_DESTINO,
}

INBOX_PREFIXES = ["Predicación_", "Predicaciónes_", "Predicaciones_"]


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def strip_inbox_prefix(stem: str) -> str:
    """Remove sermon prefixes from inbox filename stem for name matching.
    Normalizes to NFC before comparison — macOS filenames use NFD."""
    stem_nfc = _nfc(stem)
    for prefix in INBOX_PREFIXES:
        if stem_nfc.startswith(_nfc(prefix)):
            return stem_nfc[len(_nfc(prefix)):]
    return stem_nfc


STOPWORDS_ES = {
    "de", "la", "el", "en", "y", "a", "los", "del", "las", "un", "una",
    "con", "por", "para", "que", "es", "se", "no", "lo", "como", "más",
    "pero", "sus", "le", "ya", "o", "este", "si", "porque", "cuando",
    "muy", "sin", "sobre", "también", "me", "hasta", "desde", "nos",
    "durante", "ni", "contra", "al", "su", "son", "fue", "ser", "hay",
    "era", "han", "has", "he", "mi", "tu", "su",
}


# ── Parsing helpers ─────────────────────────────────────────────────────────

def get_inbox_md_files() -> list:
    """Get .md files from Inbox/ root only (exclude scrivener-sync/)."""
    return [p for p in INBOX_DIR.glob("*.md")]


def get_temas_files() -> list:
    """Get all .md files from Temas/ (all subdirs). No version_yaml filter —
    notas puente procesadas con versión anterior pueden no tener YAML v2."""
    result = []
    for p in TEMAS_DIR.rglob("*.md"):
        try:
            result.append(p)
        except Exception:
            continue
    return result


def load_note(path: Path) -> tuple:
    """Returns (metadata dict, body str). Body is empty string on parse error."""
    try:
        post = frontmatter.load(str(path))
        return post.metadata, post.content
    except Exception:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        return {}, raw


def extract_keywords(text: str) -> set:
    text = text.lower()
    words = re.findall(r"\b[a-záéíóúñü]{3,}\b", text)
    return {w for w in words if w not in STOPWORDS_ES}


def get_versiculos(meta: dict) -> set:
    raw = meta.get("versiculos_citados", [])
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = []
    return {str(v).strip().lower() for v in raw if v}


# ── Tier matching ────────────────────────────────────────────────────────────

def jaccard(set_a: set, set_b: set) -> float:
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _get_chroma_col(collection: str):
    """Lazy singleton: instancia ChromaDB y el modelo una sola vez por proceso.
    Bug 3: evita reinstanciar SentenceTransformer en cada llamada a semantic_score.
    """
    import chromadb
    from sentence_transformers import SentenceTransformer

    if not hasattr(_get_chroma_col, "_cache"):
        _get_chroma_col._cache = {}

    if collection not in _get_chroma_col._cache:
        client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        col = client.get_collection(collection)
        model = SentenceTransformer("intfloat/multilingual-e5-small")
        _get_chroma_col._cache[collection] = (col, model)

    return _get_chroma_col._cache[collection]


def semantic_score(inbox_body: str, temas_stem: str, collection: str = "zk_pastoral") -> float:
    """Query ChromaDB for a specific doc. Returns 0.0 if index unavailable.
    B7: collection param permite separar consultas pastoral/academico en el futuro.
    """
    if not CHROMA_PATH.exists():
        return 0.0
    try:
        col, model = _get_chroma_col(collection)
        if col.count() == 0:
            return 0.0

        emb = model.encode([f"query: {inbox_body[:300]}"])[0].tolist()

        results = col.query(
            query_embeddings=[emb],
            n_results=1,
            where={"id": temas_stem},
            include=["distances"],
        )
        if results["distances"] and results["distances"][0]:
            return round(1 - results["distances"][0][0], 4)
        return 0.0
    except Exception:
        return 0.0


def match_files(inbox_files: list, temas_files: list) -> list:
    """Run 3-tier matching. Returns proposals sorted by tier asc, score desc."""
    proposals = []

    for inbox_path in inbox_files:
        inbox_meta, inbox_body = load_note(inbox_path)
        inbox_title = str(inbox_meta.get("title", inbox_path.stem))
        inbox_kw = extract_keywords(inbox_title + " " + inbox_body[:500])
        inbox_vs = get_versiculos(inbox_meta)

        for temas_path in temas_files:
            temas_meta, temas_body = load_note(temas_path)
            temas_title = str(temas_meta.get("title", temas_path.stem))
            temas_kw = extract_keywords(temas_title + " " + temas_body[:500])
            temas_vs = get_versiculos(temas_meta)

            # Tier 0: exact name match (inbox stem sin prefijo == temas stem)
            inbox_stripped = strip_inbox_prefix(inbox_path.stem).lower()
            if inbox_stripped == _nfc(temas_path.stem).lower():
                proposals.append({
                    "inbox_file": str(inbox_path.relative_to(VAULT_ROOT)),
                    "temas_file": str(temas_path.relative_to(VAULT_ROOT)),
                    "nota_puente": f"[[{temas_path.stem}]]",
                    "tier": 0,
                    "score": 1.0,
                    "match_reason": "Nombre exacto (sin prefijo)",
                    "proposed_zk_ids": [],
                })
                continue

            # Tier 1: Jaccard on keywords (umbral 0.25 — notas puente pueden usar
            # vocabulario distinto al inbox original)
            j = jaccard(inbox_kw, temas_kw)
            if j >= 0.25:
                proposals.append({
                    "inbox_file": str(inbox_path.relative_to(VAULT_ROOT)),
                    "temas_file": str(temas_path.relative_to(VAULT_ROOT)),
                    "nota_puente": f"[[{temas_path.stem}]]",
                    "tier": 1,
                    "score": round(j, 4),
                    "match_reason": f"Jaccard keywords={j:.3f}",
                    "proposed_zk_ids": [],
                })
                continue

            # Tier 2: shared versiculos
            shared = inbox_vs & temas_vs
            if shared:
                union_size = max(len(inbox_vs | temas_vs), 1)
                score = round(len(shared) / union_size, 4)
                proposals.append({
                    "inbox_file": str(inbox_path.relative_to(VAULT_ROOT)),
                    "temas_file": str(temas_path.relative_to(VAULT_ROOT)),
                    "nota_puente": f"[[{temas_path.stem}]]",
                    "tier": 2,
                    "score": score,
                    "match_reason": f"Versículos compartidos: {', '.join(list(shared)[:3])}",
                    "proposed_zk_ids": [],
                })
                continue

            # Tier 3: semantic via ChromaDB
            sem = semantic_score(inbox_body, temas_path.stem)
            if sem > 0.5:
                proposals.append({
                    "inbox_file": str(inbox_path.relative_to(VAULT_ROOT)),
                    "temas_file": str(temas_path.relative_to(VAULT_ROOT)),
                    "nota_puente": f"[[{temas_path.stem}]]",
                    "tier": 3,
                    "score": sem,
                    "match_reason": f"Semántico ChromaDB score={sem:.3f}",
                    "proposed_zk_ids": [],
                })

    return sorted(proposals, key=lambda x: (x["tier"], -x["score"]))


# ── CLI commands ─────────────────────────────────────────────────────────────

def cmd_scan(inbox_files: list, temas_files: list):
    proposals = match_files(inbox_files, temas_files)

    if not proposals:
        print("No se encontraron coincidencias.")
        return

    print(f"\n{'Inbox':<35} {'Nota Puente (Temas/)':<45} {'Tier':>4} {'Score':>6}  Razón")
    print("-" * 115)
    for p in proposals:
        inbox = Path(p["inbox_file"]).name[:33]
        temas = Path(p["temas_file"]).name[:43]
        print(f"{inbox:<35} {temas:<45} {p['tier']:>4} {p['score']:>6.3f}  {p['match_reason']}")
    print(f"\nTotal: {len(proposals)} propuesta(s)")


def cmd_propose(inbox_files: list, temas_files: list):
    proposals = match_files(inbox_files, temas_files)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(proposals),
        "proposals": proposals,
    }

    with open(PROPOSALS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ {len(proposals)} propuesta(s) escritas en {PROPOSALS_PATH.relative_to(VAULT_ROOT)}")


def cmd_inject(confirm: bool):
    if not PROPOSALS_PATH.exists():
        print("No se encontró bridge_proposals.json. Ejecuta --mode propose primero.")
        sys.exit(1)

    with open(PROPOSALS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    # Only Tier 0 (exact name match) — high-confidence, safe to auto-inject
    tier0 = [p for p in data.get("proposals", []) if p.get("tier") == 0]

    if not tier0:
        print("No hay propuestas Tier 0 para inyectar.")
        return

    processed = 0

    for prop in tier0:
        inbox_path = VAULT_ROOT / prop["inbox_file"]
        nota_puente = prop["nota_puente"]
        # Destino = misma carpeta donde vive la nota puente
        destino_dir = (VAULT_ROOT / prop["temas_file"]).parent
        destino_rel = str(destino_dir.relative_to(VAULT_ROOT)) + "/"
        moved_path = destino_dir / inbox_path.name

        if not inbox_path.exists():
            print(f"SKIP [no existe en Inbox]: {prop['inbox_file']}")
            continue

        if moved_path.exists():
            print(f"SKIP [ya existe en destino]: {moved_path.relative_to(VAULT_ROOT)}")
            continue

        if not confirm:
            print(f"[DRY RUN] {inbox_path.name}")
            print(f"  → {destino_rel}")
            print(f"  → nota_puente: {nota_puente}")
            continue

        # 1. Run inbox_triage.py — inyecta YAML v2 y mueve el archivo
        params = {**TRIAGE_PARAMS, "destino": destino_rel}
        result = subprocess.run(
            ["python3", str(VAULT_ROOT / "_Scripts" / "inbox_triage.py"),
             str(inbox_path), json.dumps(params)],
            capture_output=True, text=True, cwd=str(VAULT_ROOT),
        )
        if result.returncode != 0:
            print(f"ERROR triage {inbox_path.name}: {result.stderr.strip()}")
            continue

        # 2. Inyectar nota_puente en el archivo movido
        if not moved_path.exists():
            print(f"ERROR: archivo no encontrado en destino tras triage: {moved_path}")
            continue

        try:
            post = frontmatter.load(str(moved_path))
        except Exception as e:
            print(f"ERROR YAML {moved_path.name}: {e}")
            continue

        post.metadata["nota_puente"] = nota_puente
        post.metadata["fecha_actualizacion"] = datetime.now(timezone.utc).date().isoformat()

        with open(moved_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        print(f"✓ {inbox_path.name}")
        print(f"  → {TRIAGE_DESTINO} | nota_puente: {nota_puente}")
        processed += 1

    action = "procesados" if confirm else "DRY RUN"
    print(f"\n{action}: {processed}/{len(tier0)} Tier 0")


def main():
    parser = argparse.ArgumentParser(description="Bridge linker: Inbox → Temas/07")
    parser.add_argument("--mode", choices=["scan", "propose", "inject"], required=True)
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirmar escritura en inject mode (sin este flag = dry run)",
    )
    args = parser.parse_args()

    if args.mode in ("scan", "propose"):
        inbox_files = get_inbox_md_files()
        temas_files = get_temas_files()
        print(f"Inbox/.md: {len(inbox_files)} | Temas/ notas: {len(temas_files)}")

    if args.mode == "scan":
        cmd_scan(inbox_files, temas_files)
    elif args.mode == "propose":
        cmd_propose(inbox_files, temas_files)
    elif args.mode == "inject":
        cmd_inject(args.confirm)


if __name__ == "__main__":
    main()
