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
    "skills-sistema-v3",
    ".claude",
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
MIN_MATCH_WORD_LEN = 4       # palabras más cortas que esto no se usan en matching parcial


def _count_zk_for_topic(norm_topic: str, zk_notes_tags: list) -> int:
    """
    Cuenta cuántas notas ZK distintas cubren un tema.
    Usa matching de subcadena por palabra: una nota cubre el tema si alguno
    de sus tags es subcadena del topic o viceversa (palabras >= MIN_MATCH_WORD_LEN).
    Evita doble conteo — cada nota se cuenta una sola vez.
    """
    topic_words = {w for w in norm_topic.split() if len(w) >= MIN_MATCH_WORD_LEN}
    if not topic_words:
        return 0
    count = 0
    for note_tags in zk_notes_tags:
        matched = False
        for tag in note_tags:
            if matched:
                break
            # El tag completo aparece dentro del topic (ej: "mikveh" en "mikveh hebreo")
            if len(tag) >= MIN_MATCH_WORD_LEN and tag in norm_topic:
                matched = True
            else:
                # Alguna palabra del topic aparece dentro del tag
                # (ej: "expiacion" del topic en el tag "expiacion")
                for w in topic_words:
                    if w in tag:
                        matched = True
                        break
        if matched:
            count += 1
    return count


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
    zk_notes_tags = []      # lista de frozensets — tags normalizados de cada nota ZK
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
            note_tags = frozenset(
                normalize(tag).replace("-", " ")
                for tag in frontmatter.get("tags", [])
            )
            zk_notes_tags.append(note_tags)
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
        zk_count = _count_zk_for_topic(norm_topic, zk_notes_tags)
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
        if _count_zk_for_topic(t, zk_notes_tags) >= ZK_COVERAGE_THRESHOLD
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

def _norm_tema(tema: str) -> str:
    """Normaliza el campo tema a clave canónica (minúsculas, sin tildes, sin espacios)."""
    return normalize(tema).replace(" ", "_").replace("/", "_")


def _folder_to_label(folder_name: str) -> str:
    """
    Convierte nombre de carpeta Temas/ a etiqueta de display legible.
    '03_Escatologia—Destino' → '03 · Escatologia — Destino'
    '05_DoctrinasFundamentales' → '05 · Doctrinas Fundamentales'
    """
    if "_" not in folder_name:
        return folder_name
    num, rest = folder_name.split("_", 1)
    # Em-dash → espaciado legible
    rest = rest.replace("—", " — ").replace("--", " — ")
    # Insertar espacio en transiciones CamelCase (minúscula → Mayúscula)
    rest = re.sub(r"([a-záéíóúüñ])([A-ZÁÉÍÓÚÜÑ])", r"\1 \2", rest)
    return f"{num} · {rest}"


def _discover_temas(vault: Path) -> list:
    """
    Descubre la taxonomía de temas leyendo la estructura de Temas/.
    Retorna lista ordenada de (tema_norm, label_display).

    Si Daniel añade o renombra un folder en Temas/, el índice lo refleja
    automáticamente sin tocar el código.
    """
    temas_dir = vault / "Temas"
    if not temas_dir.exists():
        return []

    temas = []
    for folder in sorted(temas_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        name = folder.name
        norm = _norm_tema(name)
        label = _folder_to_label(name)
        temas.append((norm, label))

    return temas


def generate_index(vault_path: str) -> str:
    """
    Genera un índice comprimido del vault agrupado por tema teológico (01-08).

    Escalable: a 254 fuentes da 8 grupos temáticos, no 254 clusters por fuente.
    Cargable en segundos al inicio de sesiones de investigación o coach.

    Uso:
        python scan_vault.py --vault . --mode index > _Skills/VAULT_INDEX.md
    """
    from datetime import date

    vault = Path(vault_path)
    if not vault.exists():
        print(f"Error: vault path '{vault_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Paso 1 — construir mapa source_title → tema (del documento fuente)
    source_to_tema = {}   # titulo_fuente -> tema normalizado
    source_docs_by_tema = {}  # tema_norm -> lista de {titulo, modo, zk_count, fecha}

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
        if not tipo or tipo == "zettelkasten" or tipo == "indice-zettelkasten":
            continue
        if "MOC" in md_file.stem:
            continue

        titulo = fm.get("title", fm.get("titulo", md_file.stem))
        # Busca campo 'tema' (singular, YAML v1) y fallback a 'temas_principales' (lista, YAML v2)
        tema_raw = fm.get("tema", "")
        if not tema_raw:
            temas_list = fm.get("temas_principales", [])
            tema_raw = temas_list[0] if temas_list else ""
        tema_norm = _norm_tema(tema_raw) if tema_raw else ""
        zk_count = len(fm.get("zettelkasten_notes", []))
        modo = fm.get("modo", "")
        fecha = fm.get("fecha", fm.get("fecha_actualizacion", ""))

        # Registrar mapeo por título Y por nombre de archivo (stem)
        # Las notas ZK pueden referenciar la fuente de cualquiera de las dos formas
        source_to_tema[titulo] = tema_norm
        source_to_tema[md_file.stem] = tema_norm

        if tema_norm:
            if tema_norm not in source_docs_by_tema:
                source_docs_by_tema[tema_norm] = []
            source_docs_by_tema[tema_norm].append({
                "titulo": titulo,
                "modo": modo,
                "zk_count": zk_count,
                "fecha": fecha,
            })

    # Paso 2 — agrupar notas ZK por tema (via source_file → tema)
    zk_by_tema = {}      # tema_norm -> lista de {id, titulo, n_conexiones, fecha}
    zk_all = []          # lista completa para stats globales

    for md_file in vault.rglob("*.md"):
        if should_exclude(md_file, vault):
            continue
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        fm = extract_frontmatter(text)
        if fm.get("tipo", "") != "zettelkasten":
            continue

        titulo = fm.get("titulo", md_file.stem)
        zk_id = fm.get("id", md_file.stem)
        fecha = fm.get("fecha_creacion", "")
        n_conexiones = len(fm.get("notas_relacionadas", []))
        source_raw = fm.get("source_file", "")
        source = source_raw.replace("[[", "").replace("]]", "").strip()

        # Resolver tema via source_file
        tema_norm = source_to_tema.get(source, "")

        zk_entry = {
            "id": zk_id,
            "titulo": titulo,
            "fecha": fecha,
            "n_conexiones": n_conexiones,
            "source": source,
        }
        zk_all.append(zk_entry)

        if tema_norm:
            if tema_norm not in zk_by_tema:
                zk_by_tema[tema_norm] = []
            zk_by_tema[tema_norm].append(zk_entry)

    # Totales
    today = date.today().isoformat()
    total_src = sum(len(v) for v in source_docs_by_tema.values())
    total_zk = len(zk_all)
    pastoral_zk = sum(
        len(v) for k, v in zk_by_tema.items() if k != "08_academico"
    )
    academico_zk = len(zk_by_tema.get("08_academico", []))

    # ── Construir output ──────────────────────────────────────────────
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
        f"| **Pastoral** | {total_src - len(source_docs_by_tema.get('08_academico', []))} | {pastoral_zk} |",
        f"| **Académico** | {len(source_docs_by_tema.get('08_academico', []))} | {academico_zk} |",
        f"| **Total** | {total_src} | {total_zk} |",
        "",
        "---",
        "",
    ]

    # ── Secciones por tema (orden descubierto de Temas/) ────────────────
    discovered_temas = _discover_temas(vault)
    seen_temas = set()
    for tema_key, label in discovered_temas:
        if tema_key in seen_temas:
            continue
        seen_temas.add(tema_key)

        src_list = source_docs_by_tema.get(tema_key, [])
        zk_list = sorted(
            zk_by_tema.get(tema_key, []),
            key=lambda x: x["n_conexiones"],
            reverse=True,
        )

        if not src_list and not zk_list:
            continue

        lines += [f"## {label}  ({len(zk_list)} notas ZK)", ""]

        # Fuentes del tema (condensadas en una línea cada una)
        if src_list:
            for doc in sorted(src_list, key=lambda x: x["fecha"], reverse=True):
                lines.append(
                    f"- _fuente:_ **{doc['titulo']}** · modo `{doc['modo']}` · {doc['zk_count']} ZK"
                )
            lines.append("")

        # Notas ZK del tema — primeras 8, ordenadas por conexiones
        for zk in zk_list[:8]:
            conn = f" _{zk['n_conexiones']} cx_" if zk["n_conexiones"] > 0 else ""
            lines.append(f"- `{zk['id']}` {zk['titulo']}{conn}")
        if len(zk_list) > 8:
            lines.append(f"- _...y {len(zk_list) - 8} notas más_")
        lines.append("")

    # Temas de otros dominios no cubiertos por TEMA_ORDER
    extra_temas = set(zk_by_tema.keys()) - seen_temas
    if extra_temas:
        lines += ["## Otras notas (tema no clasificado)", ""]
        for tema_key in sorted(extra_temas):
            for zk in zk_by_tema[tema_key]:
                lines.append(f"- `{zk['id']}` {zk['titulo']}")
        lines.append("")

    # ── Notas sin tema (huérfanas de tema) ───────────────────────────
    sin_tema = [z for z in zk_all if not source_to_tema.get(z["source"], "")]
    if sin_tema:
        lines += [f"## Sin tema detectado  ({len(sin_tema)} notas)", ""]
        for zk in sin_tema[:5]:
            lines.append(f"- `{zk['id']}` {zk['titulo']}")
        if len(sin_tema) > 5:
            lines.append(f"- _...y {len(sin_tema) - 5} más_")
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
