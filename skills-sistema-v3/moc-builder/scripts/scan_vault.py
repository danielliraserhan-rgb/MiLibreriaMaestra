#!/usr/bin/env python3
"""
scan_vault.py — Escanea el vault de Obsidian y encuentra notas relevantes para un query.

Uso:
    python scan_vault.py --vault /ruta/al/vault --query "Génesis"
    python scan_vault.py --vault /ruta/al/vault --query "fe y obediencia"
    python scan_vault.py --vault /ruta/al/vault --query "gracia" --tipo zettelkasten

Salida: JSON con lista de notas relevantes, puntaje de relevancia, y metadatos YAML.
Incluye: Temas/01–08, 09_Zettelkasten/pastoral/, 09_Zettelkasten/academico/
Excluye: _indice/, MOC en nombre de archivo, _Skills/, Templates/, Assets/
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Campos YAML donde buscar coincidencias (en orden de peso)
# v2: agrega author_quotes, modo, dominio, subtipo para notas ZK
YAML_FIELDS = [
    ("libro_biblico_principal", 3),
    ("serie", 3),
    ("personajes", 2),
    ("temas_principales", 2),
    ("tags", 2),
    ("versiculos_citados", 2),
    ("versiculos_biblicos", 2),   # campo en notas ZK
    ("author_quotes", 2),          # NUEVO v2
    ("Versiculos_Citados", 1),     # legacy capitalización
    ("titulo", 1),                 # notas ZK usan "titulo"
    ("title", 1),
    ("modo", 1),                   # NUEVO v2
    ("dominio", 1),                # NUEVO v2
    ("subtipo", 1),                # notas ZK
    ("tema", 1),                   # v1 legacy
]

# Carpetas a excluir del escaneo
EXCLUDED_DIRS = {
    "_Skills",
    "Templates",
    "Assets",
    "ContextoMaestro",
    "ClasesPorSemestre",
    "_indice",       # dentro de 09_Zettelkasten
    ".obsidian",
    ".git",
}


def extract_frontmatter(text: str) -> dict:
    """Extrae el frontmatter YAML de un archivo Markdown."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    yaml_block = text[3:end].strip()
    result = {}
    current_key = None
    current_list = None

    for line in yaml_block.splitlines():
        # Lista YAML multilinea (items con "  - valor")
        if line.startswith("  - ") or line.startswith("- "):
            item = line.strip().lstrip("- ").strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(item)
            continue

        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()

            # Lista inline: [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                if inner:
                    items = [v.strip().strip('"').strip("'") for v in inner.split(",")]
                else:
                    items = []
                result[key] = items
                current_list = None
                current_key = None
            elif val == "" or val == "[]":
                # inicio de lista multilinea
                result[key] = []
                current_key = key
                current_list = result[key]
            else:
                result[key] = val.strip('"').strip("'")
                current_key = key
                current_list = None

    return result


def normalize(text) -> str:
    """Normaliza texto para comparación: minúsculas, sin tildes."""
    if isinstance(text, list):
        return " ".join(normalize(t) for t in text)
    text = str(text).lower()
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ü": "u", "ñ": "n",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text


def score_note(frontmatter: dict, filename: str, query_terms: list) -> int:
    """Calcula un puntaje de relevancia para una nota dado el query."""
    score = 0
    norm_filename = normalize(filename)

    for field, weight in YAML_FIELDS:
        value = frontmatter.get(field, "")
        if not value:
            continue
        norm_value = normalize(value)
        for term in query_terms:
            if term in norm_value:
                score += weight

    # También busca en el nombre del archivo
    for term in query_terms:
        if term in norm_filename:
            score += 1

    return score


def relevance_label(score: int) -> str:
    if score >= 4:
        return "alta"
    elif score >= 2:
        return "media"
    elif score >= 1:
        return "baja"
    return "none"


def should_exclude(path: Path, vault: Path) -> bool:
    """Devuelve True si el archivo debe excluirse del escaneo."""
    # Excluir si algún componente del path relativo está en EXCLUDED_DIRS
    try:
        rel = path.relative_to(vault)
    except ValueError:
        return True

    parts = rel.parts
    for part in parts[:-1]:  # no incluir el propio nombre del archivo
        if part in EXCLUDED_DIRS:
            return True

    # Excluir archivos MOC
    if "MOC" in path.name:
        return False  # NO excluir — ahora los MOC son válidos para referenciar

    return False


def scan_vault(vault_path: str, query: str, tipo_filter: str = None) -> list:
    """Escanea el vault y retorna notas ordenadas por relevancia."""
    vault = Path(vault_path)
    if not vault.exists():
        print(f"Error: vault path '{vault_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    query_terms = [normalize(t) for t in query.split() if len(t) > 2]

    results = []
    for md_file in vault.rglob("*.md"):
        if should_exclude(md_file, vault):
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        frontmatter = extract_frontmatter(text)

        # Filtrar por tipo si se especifica (ej: --tipo zettelkasten)
        if tipo_filter:
            note_tipo = frontmatter.get("tipo", "")
            if normalize(note_tipo) != normalize(tipo_filter):
                continue

        score = score_note(frontmatter, md_file.stem, query_terms)

        if score == 0:
            continue

        # Detectar si es nota ZK
        is_zettelkasten = frontmatter.get("tipo", "") == "zettelkasten"

        results.append({
            "filepath": str(md_file.relative_to(vault)),
            "title": frontmatter.get("titulo", frontmatter.get("title", md_file.stem)),
            "tipo": frontmatter.get("tipo", "desconocido"),
            "subtipo": frontmatter.get("subtipo", ""),           # NUEVO — notas ZK
            "dominio": frontmatter.get("dominio", ""),           # NUEVO v2
            "modo": frontmatter.get("modo", ""),                 # NUEVO v2
            "date": frontmatter.get("fecha", frontmatter.get("date", "")),
            "serie": frontmatter.get("serie", ""),
            "libro_biblico_principal": frontmatter.get("libro_biblico_principal", ""),
            "personajes": frontmatter.get("personajes", []),
            "temas_principales": frontmatter.get("temas_principales", []),
            "author_quotes": frontmatter.get("author_quotes", []),  # NUEVO v2
            "tags": frontmatter.get("tags", []),
            "zettelkasten_notes": frontmatter.get("zettelkasten_notes", []),  # NUEVO v2
            "notas_relacionadas": frontmatter.get("notas_relacionadas", []),  # ZK
            "source_file": frontmatter.get("source_file", "") if is_zettelkasten else "",
            "score": score,
            "relevancia": relevance_label(score),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="Scan Obsidian vault for relevant notes")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault")
    parser.add_argument("--query", required=True, help="Search query (topic, biblical book, series, etc.)")
    parser.add_argument("--tipo", default=None, help="Filtrar por tipo de nota (ej: zettelkasten, libro, clase)")
    args = parser.parse_args()

    notes = scan_vault(args.vault, args.query, tipo_filter=args.tipo)

    print(json.dumps(notes, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
