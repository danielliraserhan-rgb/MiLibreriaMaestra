#!/usr/bin/env python3
"""
scan_vault.py — Escanea el vault de Obsidian y encuentra notas relevantes para un query,
o genera un reporte de huecos de conocimiento.

Uso — modo scan (default):
    python scan_vault.py --vault /ruta/al/vault --query "Génesis"
    python scan_vault.py --vault /ruta/al/vault --query "fe y obediencia"
    python scan_vault.py --vault /ruta/al/vault --query "gracia" --tipo zettelkasten

Uso — modo gaps:
    python scan_vault.py --vault /ruta/al/vault --mode gaps

Salida: JSON.
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
YAML_FIELDS = [
    ("libro_biblico_principal", 3),
    ("serie", 3),
    ("personajes", 2),
    ("temas_principales", 2),
    ("tags", 2),
    ("versiculos_citados", 2),
    ("versiculos_biblicos", 2),
    ("author_quotes", 2),
    ("Versiculos_Citados", 1),
    ("titulo", 1),
    ("title", 1),
    ("modo", 1),
    ("dominio", 1),
    ("subtipo", 1),
    ("tema", 1),
]

# Carpetas a excluir del escaneo
EXCLUDED_DIRS = {
    "_Skills",
    "Templates",
    "Assets",
    "ContextoMaestro",
    "ClasesPorSemestre",
    "_indice",
    ".obsidian",
    ".git",
    "_Archive",
}

# Caracteres del cuerpo a buscar (primeros N chars después del frontmatter)
BODY_SEARCH_CHARS = 800


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
                items = [v.strip().strip('"').strip("'") for v in inner.split(",")] if inner else []
                result[key] = items
                current_list = None
                current_key = None
            elif val == "" or val == "[]":
                result[key] = []
                current_key = key
                current_list = result[key]
            else:
                result[key] = val.strip('"').strip("'")
                current_key = key
                current_list = None

    return result


def extract_body(text: str) -> str:
    """Extrae el cuerpo de texto después del frontmatter YAML."""
    if not text.startswith("---"):
        return text[:BODY_SEARCH_CHARS]
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    body = text[end + 4:].strip()
    return body[:BODY_SEARCH_CHARS]


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


def score_note(frontmatter: dict, filename: str, body: str, query_terms: list) -> int:
    """Calcula puntaje de relevancia combinando YAML, nombre de archivo y cuerpo."""
    score = 0
    norm_filename = normalize(filename)

    # Score por campos YAML
    for field, weight in YAML_FIELDS:
        value = frontmatter.get(field, "")
        if not value:
            continue
        norm_value = normalize(value)
        for term in query_terms:
            if term in norm_value:
                score += weight

    # Score por nombre de archivo
    for term in query_terms:
        if term in norm_filename:
            score += 1

    # Score por cuerpo (máximo 2 puntos — evita sobre-ponderar documentos largos)
    if body:
        norm_body = normalize(body)
        body_hits = sum(1 for term in query_terms if term in norm_body)
        score += min(body_hits, 2)

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
    try:
        rel = path.relative_to(vault)
    except ValueError:
        return True

    parts = rel.parts
    for part in parts[:-1]:
        if part in EXCLUDED_DIRS:
            return True

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
        body = extract_body(text)

        if tipo_filter:
            note_tipo = frontmatter.get("tipo", "")
            if normalize(note_tipo) != normalize(tipo_filter):
                continue

        score = score_note(frontmatter, md_file.stem, body, query_terms)

        if score == 0:
            continue

        is_zettelkasten = frontmatter.get("tipo", "") == "zettelkasten"

        results.append({
            "filepath": str(md_file.relative_to(vault)),
            "title": frontmatter.get("titulo", frontmatter.get("title", md_file.stem)),
            "tipo": frontmatter.get("tipo", "desconocido"),
            "subtipo": frontmatter.get("subtipo", ""),
            "dominio": frontmatter.get("dominio", ""),
            "modo": frontmatter.get("modo", ""),
            "date": frontmatter.get("fecha", frontmatter.get("date", "")),
            "serie": frontmatter.get("serie", ""),
            "libro_biblico_principal": frontmatter.get("libro_biblico_principal", ""),
            "personajes": frontmatter.get("personajes", []),
            "temas_principales": frontmatter.get("temas_principales", []),
            "author_quotes": frontmatter.get("author_quotes", []),
            "tags": frontmatter.get("tags", []),
            "zettelkasten_notes": frontmatter.get("zettelkasten_notes", []),
            "notas_relacionadas": frontmatter.get("notas_relacionadas", []),
            "source_file": frontmatter.get("source_file", "") if is_zettelkasten else "",
            "score": score,
            "relevancia": relevance_label(score),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ─────────────────────────────────────────────
# MODO GAPS — detección de huecos de conocimiento
# ─────────────────────────────────────────────

ZK_COVERAGE_THRESHOLD = 2   # temas con menos de N notas ZK = hueco


def analyze_gaps(vault_path: str) -> dict:
    """
    Analiza el vault para detectar huecos de conocimiento.

    Detecta:
    1. Temas presentes en documentos fuente que tienen pocas notas ZK (< threshold)
    2. Documentos fuente que no tienen notas ZK generadas (zettelkasten_notes: [])
    3. Notas ZK sin conexiones (notas_relacionadas: []) — huérfanas
    """
    vault = Path(vault_path)
    if not vault.exists():
        print(f"Error: vault path '{vault_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Acumuladores
    source_topic_map = {}   # normalized_topic -> {"topic": str, "sources": [{"filepath", "title"}]}
    zk_tag_counts = {}      # normalized_tag -> int
    source_docs_without_zk = []
    orphan_zk_notes = []
    total_zk = 0
    total_sources = 0

    for md_file in vault.rglob("*.md"):
        if should_exclude(md_file, vault):
            continue

        # Saltar archivos del sistema sin tipo
        if md_file.stem in ("Bienvenido", "CLAUDE"):
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        frontmatter = extract_frontmatter(text)
        tipo = frontmatter.get("tipo", "")

        if not tipo:
            continue

        if tipo == "zettelkasten":
            total_zk += 1
            for tag in frontmatter.get("tags", []):
                norm = normalize(tag)
                zk_tag_counts[norm] = zk_tag_counts.get(norm, 0) + 1
            related = frontmatter.get("notas_relacionadas", [])
            if not related:
                orphan_zk_notes.append({
                    "filepath": str(md_file.relative_to(vault)),
                    "title": frontmatter.get("titulo", md_file.stem),
                    "dominio": frontmatter.get("dominio", ""),
                    "fecha_creacion": frontmatter.get("fecha_creacion", ""),
                })

        elif tipo not in ("indice-zettelkasten",):
            # Documento fuente — excluir MOCs
            if "MOC" in md_file.stem:
                continue

            total_sources += 1
            topics = frontmatter.get("temas_principales", [])
            for topic in topics:
                norm = normalize(topic)
                if norm not in source_topic_map:
                    source_topic_map[norm] = {"topic": topic, "sources": []}
                source_topic_map[norm]["sources"].append({
                    "filepath": str(md_file.relative_to(vault)),
                    "title": frontmatter.get("title", frontmatter.get("titulo", md_file.stem)),
                })

            # Documentos sin notas ZK generadas
            zk_notes = frontmatter.get("zettelkasten_notes", [])
            if isinstance(zk_notes, list) and len(zk_notes) == 0:
                source_docs_without_zk.append({
                    "filepath": str(md_file.relative_to(vault)),
                    "title": frontmatter.get("title", frontmatter.get("titulo", md_file.stem)),
                    "tipo": tipo,
                    "dominio": frontmatter.get("dominio", ""),
                    "temas_principales": topics[:3],
                })

    # Detectar temas con baja cobertura ZK
    coverage_gaps = []
    for norm_topic, data in source_topic_map.items():
        zk_count = zk_tag_counts.get(norm_topic, 0)
        if zk_count < ZK_COVERAGE_THRESHOLD:
            coverage_gaps.append({
                "topic": data["topic"],
                "zk_notes_count": zk_count,
                "aparece_en_n_fuentes": len(data["sources"]),
                "fuentes_ejemplo": data["sources"][:2],
            })

    # Ordenar por número de fuentes que lo mencionan (más urgente primero)
    coverage_gaps.sort(key=lambda x: x["aparece_en_n_fuentes"], reverse=True)

    topics_covered = len([
        t for t in source_topic_map
        if zk_tag_counts.get(t, 0) >= ZK_COVERAGE_THRESHOLD
    ])

    return {
        "resumen": {
            "total_documentos_fuente": total_sources,
            "total_notas_zk": total_zk,
            "temas_unicos_en_fuentes": len(source_topic_map),
            "temas_con_cobertura_zk": topics_covered,
            "temas_con_hueco": len(coverage_gaps),
            "fuentes_sin_zk": len(source_docs_without_zk),
            "notas_zk_huerfanas": len(orphan_zk_notes),
        },
        "huecos_de_cobertura": coverage_gaps[:25],
        "fuentes_sin_notas_zk": source_docs_without_zk,
        "notas_zk_huerfanas": orphan_zk_notes,
    }


# ─────────────────────────────────────────────
# MODO INDEX — índice comprimido del vault
# ─────────────────────────────────────────────

def generate_index(vault_path: str) -> str:
    """
    Genera un índice comprimido del vault en Markdown.

    Salida pensada para ser cargada por Claude Code al inicio de sesiones
    de investigación, navegación o coach — en lugar de leer 2000 archivos.

    Uso:
        python scan_vault.py --vault . --mode index > _Skills/VAULT_INDEX.md
    """
    from datetime import date

    vault = Path(vault_path)
    if not vault.exists():
        print(f"Error: vault path '{vault_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    source_docs = {"pastoral": [], "academico": []}
    zk_by_domain = {"pastoral": [], "academico": []}
    zk_by_source = {}   # source_title -> list of ZK titles

    for md_file in vault.rglob("*.md"):
        if should_exclude(md_file, vault):
            continue
        if md_file.stem in ("Bienvenido", "CLAUDE", "VAULT_INDEX"):
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        fm = extract_frontmatter(text)
        tipo = fm.get("tipo", "")
        if not tipo:
            continue

        dominio = fm.get("dominio", "")
        domain = dominio if dominio in ("pastoral", "academico") else "pastoral"

        if tipo == "zettelkasten":
            titulo = fm.get("titulo", md_file.stem)
            zk_id = fm.get("id", md_file.stem)
            fecha = fm.get("fecha_creacion", "")
            n_conexiones = len(fm.get("notas_relacionadas", []))
            source_raw = fm.get("source_file", "")
            source = source_raw.replace("[[", "").replace("]]", "").strip()

            zk_by_domain[domain].append({
                "id": zk_id,
                "titulo": titulo,
                "tags": fm.get("tags", []),
                "source": source,
                "fecha": fecha,
                "n_conexiones": n_conexiones,
            })

            if source:
                if source not in zk_by_source:
                    zk_by_source[source] = {"domain": domain, "titles": []}
                zk_by_source[source]["titles"].append(titulo)

        elif tipo not in ("indice-zettelkasten",) and "MOC" not in md_file.stem:
            titulo = fm.get("title", fm.get("titulo", md_file.stem))
            zk_count = len(fm.get("zettelkasten_notes", []))
            modo = fm.get("modo", "")
            tema = fm.get("tema", "")
            fecha = fm.get("fecha", fm.get("fecha_actualizacion", ""))
            source_docs[domain].append({
                "titulo": titulo,
                "modo": modo,
                "tema": tema,
                "zk_count": zk_count,
                "fecha": fecha,
                "tipo": tipo,
            })

    # Ordenar por fecha descendente
    for d in ("pastoral", "academico"):
        zk_by_domain[d].sort(key=lambda x: x["fecha"], reverse=True)
        source_docs[d].sort(key=lambda x: x["fecha"], reverse=True)

    today = date.today().isoformat()
    pastoral_zk = len(zk_by_domain["pastoral"])
    academico_zk = len(zk_by_domain["academico"])
    pastoral_src = len(source_docs["pastoral"])
    academico_src = len(source_docs["academico"])

    lines = [
        "# VAULT INDEX — MiLibreriaMaestra",
        f"> Regenerar: `python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --mode index > _Skills/VAULT_INDEX.md`",
        f"> Última actualización: {today}",
        "",
        "---",
        "",
        "## Estado del vault",
        "",
        "| | Fuentes procesadas | Notas ZK |",
        "|---|---|---|",
        f"| **Pastoral** | {pastoral_src} | {pastoral_zk} |",
        f"| **Académico** | {academico_src} | {academico_zk} |",
        f"| **Total** | {pastoral_src + academico_src} | {pastoral_zk + academico_zk} |",
        "",
        "---",
        "",
        "## Dominio Pastoral",
        "",
    ]

    if source_docs["pastoral"]:
        lines += ["### Fuentes procesadas", ""]
        for doc in source_docs["pastoral"]:
            lines.append(
                f"- **{doc['titulo']}** — modo: `{doc['modo']}` · tema: `{doc['tema']}` · ZK generadas: {doc['zk_count']}"
            )
        lines.append("")

    if zk_by_source:
        lines += ["### Clusters por fuente", ""]
        for source, data in sorted(zk_by_source.items()):
            if data["domain"] != "pastoral":
                continue
            titles = data["titles"]
            lines.append(f"**{source}** — {len(titles)} notas")
            for t in titles[:6]:
                lines.append(f"  - {t}")
            if len(titles) > 6:
                lines.append(f"  - _...y {len(titles) - 6} más_")
            lines.append("")

    if zk_by_domain["pastoral"]:
        most_connected = sorted(
            zk_by_domain["pastoral"], key=lambda x: x["n_conexiones"], reverse=True
        )[:5]
        lines += ["### Notas más conectadas", ""]
        for zk in most_connected:
            lines.append(
                f"- `{zk['id']}` — {zk['titulo']} _(conexiones: {zk['n_conexiones']})_"
            )
        lines.append("")

    lines += ["---", "", "## Dominio Académico", ""]

    if source_docs["academico"]:
        lines += ["### Fuentes procesadas", ""]
        for doc in source_docs["academico"]:
            lines.append(
                f"- **{doc['titulo']}** — tipo: `{doc['tipo']}` · ZK generadas: {doc['zk_count']}"
            )
        lines.append("")

    if zk_by_source:
        acad_sources = {s: d for s, d in zk_by_source.items() if d["domain"] == "academico"}
        if acad_sources:
            lines += ["### Clusters por fuente", ""]
            for source, data in sorted(acad_sources.items()):
                titles = data["titles"]
                lines.append(f"**{source}** — {len(titles)} notas")
                for t in titles[:6]:
                    lines.append(f"  - {t}")
                lines.append("")

    if not zk_by_domain["academico"]:
        lines.append("_Sin notas ZK generadas todavía._")
        lines.append("")

    lines += [
        "---",
        "",
        "## Comandos rápidos",
        "",
        "```bash",
        "# Buscar notas sobre un tema",
        "python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --query \"término\"",
        "",
        "# Detectar huecos de conocimiento",
        "python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --mode gaps",
        "",
        "# Regenerar este índice",
        "python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --mode index > _Skills/VAULT_INDEX.md",
        "```",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scan Obsidian vault: búsqueda, huecos o índice comprimido"
    )
    parser.add_argument("--vault", required=True, help="Ruta al vault de Obsidian")
    parser.add_argument("--query", default=None, help="Query de búsqueda (modo scan)")
    parser.add_argument("--tipo", default=None, help="Filtrar por tipo (ej: zettelkasten, libro)")
    parser.add_argument(
        "--mode",
        default="scan",
        choices=["scan", "gaps", "index"],
        help="scan: buscar notas | gaps: detectar huecos | index: índice comprimido del vault",
    )
    args = parser.parse_args()

    if args.mode == "gaps":
        result = analyze_gaps(args.vault)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.mode == "index":
        print(generate_index(args.vault))
    else:
        if not args.query:
            parser.error("--query es requerido en modo scan")
        notes = scan_vault(args.vault, args.query, tipo_filter=args.tipo)
        print(json.dumps(notes, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
