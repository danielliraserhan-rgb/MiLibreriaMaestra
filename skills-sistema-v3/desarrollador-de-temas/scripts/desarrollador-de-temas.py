#!/usr/bin/env python3
"""
desarrollador-de-temas.py — Detecta huecos estructurales en el vault de Obsidian.

Combina analyze_gaps() de scan_vault.py con dos detectores nuevos:
  - Tipo 1: preguntas abiertas en notas ZK y académicas
  - Tipo 5: patrones aprobados con poca evidencia ZK

Uso:
    python desarrollador-de-temas.py --vault /ruta/al/vault

Salida: JSON con 5 tipos de huecos + resumen.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def _load_scan_vault(vault: Path):
    """Importa scan_vault desde el vault activo (versión con analyze_gaps)."""
    scan_path = vault / "skills-sistema-v3" / "moc-builder" / "scripts"
    if str(scan_path) not in sys.path:
        sys.path.insert(0, str(scan_path))
    import scan_vault
    return scan_vault


# Directorios donde buscar preguntas abiertas
_QUESTION_DIRS = ["09_Zettelkasten", "Temas/08_Academico"]

# Patrones que indican pregunta abierta
_QUESTION_PATTERNS = [
    re.compile(r"\[PREGUNTA:", re.IGNORECASE),
    re.compile(r"\[PUNTO OSCURO:", re.IGNORECASE),
    re.compile(r"¿[^?]{5,}\?"),  # mínimo 5 chars entre ¿ y ?
]


def detect_open_questions(vault: Path, sv) -> list:
    """Tipo 1: líneas con [PREGUNTA:, [PUNTO OSCURO: o ¿...? en notas ZK y maestría."""
    results = []
    for search_dir in _QUESTION_DIRS:
        target = vault / search_dir
        if not target.exists():
            continue
        for md_file in target.rglob("*.md"):
            if sv.should_exclude(md_file, vault):
                continue
            try:
                text = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                for pattern in _QUESTION_PATTERNS:
                    if pattern.search(line):
                        results.append({
                            "filepath": str(md_file.relative_to(vault)),
                            "linea": i,
                            "texto": line.strip()[:200],
                        })
                        break  # una sola entrada por línea
    return results


def detect_weak_patterns(vault: Path, sv) -> list:
    """Tipo 5: patrones en activePatterns.json con 0-1 apariciones en notas ZK."""
    patterns_path = vault / "_Skills" / "activePatterns.json"
    if not patterns_path.exists():
        return []

    try:
        data = json.loads(patterns_path.read_text(encoding="utf-8"))
    except Exception:
        return []

    all_patterns = []
    for scope_list in data.get("patterns", {}).values():
        if isinstance(scope_list, list):
            all_patterns.extend(scope_list)

    if not all_patterns:
        return []

    # Contar apariciones del pattern_id en notas ZK
    zk_root = vault / "09_Zettelkasten"
    pattern_counts: dict[str, int] = {p["id"]: 0 for p in all_patterns if "id" in p}

    if zk_root.exists():
        for md_file in zk_root.rglob("*.md"):
            if sv.should_exclude(md_file, vault):
                continue
            try:
                text = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            fm = sv.extract_frontmatter(text)
            coaching = fm.get("coaching_notes", [])
            tags = fm.get("tags", [])
            referenced = set(coaching) | set(tags)
            for pid in pattern_counts:
                if pid in referenced or pid in text:
                    pattern_counts[pid] += 1

    results = []
    for p in all_patterns:
        pid = p.get("id", "")
        count = pattern_counts.get(pid, 0)
        if count <= 1:
            results.append({
                "pattern_id": pid,
                "nombre": p.get("name", ""),
                "scope": p.get("scope", ""),
                "evidencia_count": count,
            })

    results.sort(key=lambda x: x["evidencia_count"])
    return results


def run(vault_path: str) -> dict:
    vault = Path(vault_path).resolve()
    sv = _load_scan_vault(vault)
    base = sv.analyze_gaps(str(vault))

    return {
        "fecha_escaneo": date.today().isoformat(),
        "tipo_1_preguntas": detect_open_questions(vault, sv),
        "tipo_2_huerfanas": base.get("notas_zk_huerfanas", []),
        "tipo_3_sin_zk": base.get("fuentes_sin_notas_zk", []),
        "tipo_4_temas_sin_desarrollo": base.get("huecos_de_cobertura", []),
        "tipo_5_patrones_debiles": detect_weak_patterns(vault, sv),
        "resumen": base.get("resumen", {}),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Detecta huecos estructurales en el vault de Obsidian"
    )
    parser.add_argument("--vault", required=True, help="Ruta al vault de Obsidian")
    args = parser.parse_args()

    result = run(args.vault)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
