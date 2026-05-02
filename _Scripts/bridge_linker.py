#!/usr/bin/env python3
"""
bridge_linker.py — Módulo 2: vincula archivos Inbox con notas en Temas/07
Matching 3 tiers: (1) Jaccard keywords, (2) versículos compartidos, (3) semántico ChromaDB
NUNCA modifica archivos en Inbox/

Uso:
  python _Scripts/bridge_linker.py --mode scan
  python _Scripts/bridge_linker.py --mode propose
  python _Scripts/bridge_linker.py --mode inject --confirm
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import frontmatter

VAULT_ROOT = Path(__file__).parent.parent
INBOX_DIR = VAULT_ROOT / "Inbox"
PREDICACIONES_DIR = VAULT_ROOT / "Temas" / "07_PredicacionesDevocionales"
PROPOSALS_PATH = VAULT_ROOT / "_Skills" / "bridge_proposals.json"
CHROMA_PATH = VAULT_ROOT / "_Skills" / "semantic_index"

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


def get_temas_v2_files() -> list:
    """Get .md files from Temas/07 that have version_yaml: '2.0'."""
    result = []
    for p in PREDICACIONES_DIR.rglob("*.md"):
        try:
            post = frontmatter.load(str(p))
            if post.metadata.get("version_yaml") == "2.0":
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


def semantic_score(inbox_body: str, temas_stem: str, collection: str = "zk_pastoral") -> float:
    """Query ChromaDB for a specific doc. Returns 0.0 if index unavailable.
    B7: collection param permite separar consultas pastoral/academico en el futuro.
    """
    if not CHROMA_PATH.exists():
        return 0.0
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer

        client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        col = client.get_collection(collection)
        if col.count() == 0:
            return 0.0

        model = SentenceTransformer("intfloat/multilingual-e5-small")
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

            # Tier 1: Jaccard on keywords
            j = jaccard(inbox_kw, temas_kw)
            if j >= 0.3:
                proposals.append({
                    "inbox_file": str(inbox_path.relative_to(VAULT_ROOT)),
                    "temas_file": str(temas_path.relative_to(VAULT_ROOT)),
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

    print(f"\n{'Inbox':<35} {'Temas':<40} {'Tier':>4} {'Score':>6}  Razón")
    print("-" * 110)
    for p in proposals:
        inbox = Path(p["inbox_file"]).name[:33]
        temas = Path(p["temas_file"]).name[:38]
        print(f"{inbox:<35} {temas:<40} {p['tier']:>4} {p['score']:>6.3f}  {p['match_reason']}")
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

    proposals = [p for p in data.get("proposals", []) if p.get("proposed_zk_ids")]

    if not proposals:
        print(
            "No hay propuestas con proposed_zk_ids. "
            "Edita _Skills/bridge_proposals.json para agregar IDs ZK antes de inyectar."
        )
        return

    injected = 0
    for prop in proposals:
        temas_path = VAULT_ROOT / prop["temas_file"]

        # Safety guard: NEVER touch anything inside Inbox/
        try:
            temas_path.relative_to(INBOX_DIR)
            print(f"SKIP [Inbox protegido]: {prop['temas_file']}")
            continue
        except ValueError:
            pass

        if not temas_path.exists():
            print(f"SKIP [no existe]: {prop['temas_file']}")
            continue

        try:
            post = frontmatter.load(str(temas_path))
        except Exception as e:
            print(f"SKIP [error YAML]: {prop['temas_file']} — {e}")
            continue

        if post.metadata.get("version_yaml") != "2.0":
            print(f"SKIP [no es YAML v2]: {prop['temas_file']}")
            continue

        current_zk = post.metadata.get("zettelkasten_notes", [])
        if not isinstance(current_zk, list):
            current_zk = []

        new_ids = [zk for zk in prop["proposed_zk_ids"] if zk not in current_zk]
        if not new_ids:
            print(f"SKIP [ya tiene los IDs]: {prop['temas_file']}")
            continue

        if not confirm:
            print(f"[DRY RUN] Agregaría a {prop['temas_file']}: {new_ids}")
            continue

        post.metadata["zettelkasten_notes"] = current_zk + new_ids
        post.metadata["fecha_actualizacion"] = datetime.now(timezone.utc).date().isoformat()

        with open(temas_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        print(f"✓ Inyectados {new_ids} en {prop['temas_file']}")
        injected += 1

    action = "inyectadas" if confirm else "DRY RUN — propuestas"
    print(f"\n{action}: {injected} modificación(es)")


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
        temas_files = get_temas_v2_files()
        print(f"Inbox/.md: {len(inbox_files)} | Temas/07 YAML v2: {len(temas_files)}")

    if args.mode == "scan":
        cmd_scan(inbox_files, temas_files)
    elif args.mode == "propose":
        cmd_propose(inbox_files, temas_files)
    elif args.mode == "inject":
        cmd_inject(args.confirm)


if __name__ == "__main__":
    main()
