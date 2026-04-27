#!/usr/bin/env python3
"""
spaced_review.py — Cola de revisión espaciada para notas Zettelkasten (SM-2).

Modos:
  --mode queue   Encuentra notas vencidas o no revisadas. Output: JSON.
  --mode calc    Calcula nuevos valores SM-2 dado intervalo/repeticiones/facilidad/rating.

Uso — queue:
  python spaced_review.py --vault /ruta/vault --mode queue [--limit 5] [--dominio pastoral]

Uso — calc:
  python spaced_review.py --mode calc --intervalo 6 --repeticiones 2 --facilidad 2.5 --rating 3
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

# Carpetas dentro de 09_Zettelkasten a excluir
EXCLUDED_ZK_DIRS = {"_indice"}

VAULT_ZK_PATH = "09_Zettelkasten"


# ─── YAML helpers ─────────────────────────────────────────────────────────────

def extract_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    yaml_block = text[3:end].strip()
    result = {}
    current_list = None

    for line in yaml_block.splitlines():
        if line.startswith("  - ") or line.startswith("- "):
            item = line.strip().lstrip("- ").strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(item)
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                result[key] = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()] if inner else []
                current_list = None
            elif val in ("", "[]"):
                result[key] = []
                current_list = result[key]
            else:
                result[key] = val.strip('"').strip("'")
                current_list = None
    return result


def parse_date(s: str):
    """Parsea YYYY-MM-DD → date. Devuelve None si inválido."""
    try:
        return date.fromisoformat(s)
    except Exception:
        return None


# ─── SM-2 ─────────────────────────────────────────────────────────────────────

def sm2_calc(intervalo: int, repeticiones: int, facilidad: float, rating: int) -> dict:
    """
    Calcula nuevos valores SM-2.
    rating: 1 = olvidé, 3 = bien, 5 = fácil
    """
    MIN_FACILIDAD = 1.3
    MIN_INTERVALO = 1

    if rating == 1:
        nuevo_intervalo = 1
        nuevas_repeticiones = 0
        nueva_facilidad = facilidad
    else:
        if repeticiones == 0:
            nuevo_intervalo = 1
        elif repeticiones == 1:
            nuevo_intervalo = 6
        else:
            nuevo_intervalo = max(MIN_INTERVALO, round(intervalo * facilidad))

        nuevas_repeticiones = repeticiones + 1
        # Fórmula SM-2 estándar: penaliza facilidad cuando rating < 5
        nueva_facilidad = facilidad + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
        nueva_facilidad = max(MIN_FACILIDAD, round(nueva_facilidad, 2))

    fecha_proxima = (date.today() + timedelta(days=nuevo_intervalo)).isoformat()

    return {
        "nuevo_intervalo": nuevo_intervalo,
        "nuevas_repeticiones": nuevas_repeticiones,
        "nueva_facilidad": nueva_facilidad,
        "fecha_proxima": fecha_proxima,
    }


# ─── Queue mode ───────────────────────────────────────────────────────────────

def get_body_excerpt(text: str, words: int = 80) -> str:
    """Extrae las primeras N palabras del cuerpo (después del frontmatter)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    # Saltar título H1
    lines = text.strip().splitlines()
    body_lines = [l for l in lines if not l.startswith("# ") and l.strip()]
    body = " ".join(body_lines)
    tokens = body.split()
    excerpt = " ".join(tokens[:words])
    if len(tokens) > words:
        excerpt += "…"
    return excerpt


def build_queue(vault_path: str, limit: int = 5, dominio: str = None) -> list:
    vault = Path(vault_path)
    zk_root = vault / VAULT_ZK_PATH
    if not zk_root.exists():
        print(f"Error: {zk_root} no existe.", file=sys.stderr)
        sys.exit(1)

    today = date.today()
    never_reviewed = []
    due = []

    for md_file in zk_root.rglob("*.md"):
        # Excluir _indice y MOC
        parts = md_file.relative_to(zk_root).parts
        if any(p in EXCLUDED_ZK_DIRS for p in parts):
            continue
        if "MOC" in md_file.name or "Dashboard" in md_file.name:
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        fm = extract_frontmatter(text)
        if fm.get("tipo") != "zettelkasten":
            continue

        # Filtro dominio
        if dominio and fm.get("dominio", "") != dominio:
            continue

        try:
            repeticiones = int(fm.get("repeticiones", 0) or 0)
        except (ValueError, TypeError):
            repeticiones = 0
        try:
            intervalo = int(fm.get("intervalo_dias", 1) or 1)
        except (ValueError, TypeError):
            intervalo = 1
        try:
            facilidad = float(fm.get("facilidad", 2.5) or 2.5)
        except (ValueError, TypeError):
            facilidad = 2.5

        fecha_proxima_str = fm.get("fecha_proxima_revision", "")
        fecha_proxima = parse_date(fecha_proxima_str)

        entry = {
            "filepath": str(md_file.relative_to(vault)),
            "id": fm.get("id", md_file.stem),
            "titulo": fm.get("titulo", md_file.stem),
            "dominio": fm.get("dominio", ""),
            "subtipo": fm.get("subtipo", ""),
            "tags": fm.get("tags", []),
            "versiculos_biblicos": fm.get("versiculos_biblicos", []),
            "notas_relacionadas": fm.get("notas_relacionadas", []),
            "source_file": fm.get("source_file", ""),
            "fecha_creacion": fm.get("fecha_creacion", ""),
            "fecha_proxima_revision": fecha_proxima_str,
            "intervalo_dias": intervalo,
            "repeticiones": repeticiones,
            "facilidad": facilidad,
            "pregunta_reflexion": fm.get("pregunta_reflexion", ""),
            "excerpt": get_body_excerpt(text),
        }

        if repeticiones == 0:
            never_reviewed.append(entry)
        elif fecha_proxima and fecha_proxima <= today:
            due.append(entry)

    # Orden: nunca revisadas primero (por fecha_creacion ASC), luego vencidas (por fecha_proxima ASC)
    never_reviewed.sort(key=lambda x: x.get("fecha_creacion", ""))
    due.sort(key=lambda x: x.get("fecha_proxima_revision", ""))

    queue = (never_reviewed + due)[:limit]
    return queue


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Spaced Review — cola SM-2 para notas ZK")
    parser.add_argument("--mode", required=True, choices=["queue", "calc"], help="Modo de operación")

    # Queue args
    parser.add_argument("--vault", help="Ruta al vault de Obsidian")
    parser.add_argument("--limit", type=int, default=5, help="Máximo de notas en cola (default: 5)")
    parser.add_argument("--dominio", default=None, help="Filtrar por dominio: pastoral | academico")

    # Calc args
    parser.add_argument("--intervalo", type=int, help="intervalo_dias actual")
    parser.add_argument("--repeticiones", type=int, help="repeticiones actuales")
    parser.add_argument("--facilidad", type=float, help="facilidad actual")
    parser.add_argument("--rating", type=int, choices=[1, 3, 5], help="Calificación: 1=olvidé 3=bien 5=fácil")

    args = parser.parse_args()

    if args.mode == "queue":
        if not args.vault:
            print("Error: --vault requerido en modo queue.", file=sys.stderr)
            sys.exit(1)
        queue = build_queue(args.vault, limit=args.limit, dominio=args.dominio)
        print(json.dumps(queue, ensure_ascii=False, indent=2))

    elif args.mode == "calc":
        required = [args.intervalo, args.repeticiones, args.facilidad, args.rating]
        if any(v is None for v in required):
            print("Error: --intervalo, --repeticiones, --facilidad y --rating requeridos en modo calc.", file=sys.stderr)
            sys.exit(1)
        result = sm2_calc(args.intervalo, args.repeticiones, args.facilidad, args.rating)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
