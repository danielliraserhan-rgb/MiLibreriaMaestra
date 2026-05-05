#!/usr/bin/env python3
"""
audio_to_zettelkasten_pipeline.py — Pipeline de Ingesta Acústica Estructurada

Fase 1: Transcripción cruda → Premisas atómicas (Claude Haiku — extractor de ruido)
Fase 2: Premisas atómicas → Especificaciones ZK en JSON (Claude Sonnet — orquestador)
Fase 3: JSON → Archivos .md en 09_Zettelkasten/

Uso:
  python3 _Scripts/audio_to_zettelkasten_pipeline.py "Inbox/transcripcion.txt"
  python3 _Scripts/audio_to_zettelkasten_pipeline.py "Inbox/transcripcion.txt" --dominio academico
  python3 _Scripts/audio_to_zettelkasten_pipeline.py "Inbox/transcripcion.txt" --write

Variable de entorno requerida:
  ANTHROPIC_API_KEY — clave para la API de Anthropic (usada en ambas fases)
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import anthropic

VAULT_ROOT = Path(__file__).parent.parent
ZK_PATHS = {
    "pastoral":  VAULT_ROOT / "09_Zettelkasten" / "pastoral",
    "academico": VAULT_ROOT / "09_Zettelkasten" / "academico",
}

MODEL_EXTRACTOR    = "claude-haiku-4-5-20251001"
MODEL_ORCHESTRATOR = "claude-sonnet-4-6"

# ─── SYSTEM PROMPTS ────────────────────────────────────────────────────────────

SYSTEM_PROMPT_EXTRACTOR = """\
Eres un filtro de ruido verbal. Tu única tarea es procesar una transcripción cruda de voz \
y extraer las premisas conceptuales limpias que contiene.

REGLAS ABSOLUTAS:
1. Devuelve ÚNICAMENTE un objeto JSON válido — sin texto antes ni después, sin bloques de código markdown.
2. No asignes etiquetas, dominios, versículos ni metadatos. Eso es trabajo de otro sistema.
3. No reescribas ni mejores el texto del autor. Extrae sus palabras reales, eliminando solo el ruido verbal.
4. Si el texto contiene menos de 2 premisas claras, devuelve las que haya (mínimo 1).
5. Cada premisa tiene exactamente dos campos: "titulo" (afirmación única y completa en ≤ 12 palabras) \
y "desarrollo" (1–2 párrafos del texto original del autor, limpiado de muletillas y repeticiones, \
sin añadir ideas propias).

Esquema de salida:
{
  "premisas": [
    {"titulo": "...", "desarrollo": "..."},
    {"titulo": "...", "desarrollo": "..."}
  ]
}

Ruido a eliminar: muletillas ("o sea", "¿verdad?", "este..."), repeticiones directas, \
correcciones en voz alta ("no espera, quise decir"), pausas verbalizadas.\
"""

SYSTEM_PROMPT_ORCHESTRATOR = """\
Eres el Orquestador del Zettelkasten de Daniel Lira. Recibirás un array JSON de premisas \
atómicas ya limpias (extraídas de una transcripción de voz). Tu tarea es convertir cada \
premisa en la especificación completa de una nota ZK, siguiendo exactamente el esquema del \
sistema MiLibreriaMaestra.

REGLAS ABSOLUTAS:
1. Devuelve ÚNICAMENTE un array JSON válido — cero texto antes ni después, sin bloques markdown.
2. No reescribas el campo "desarrollo" de la premisa. Cópialo exactamente tal como llegó.
3. Para "subtipo", usa SOLO: conceptual | argumental | exegetica | narrativa | conexion
4. Para "tema", usa SOLO los códigos de la taxonomía:
   01_Origenes | 02_HistoriaDeIsrael | 03_Escatologia—Destino | 04_ExegesisNT |
   05_DoctrinasFundamentales | 06_DiscipuladoVidaCristiana | 07_PredicacionesDevocionales | 08_Academico
5. Para "tags", usa solo los que correspondan al contenido. Tags válidos:
   pastoral, academico, cristologia, hermeneutica, tipologia, discipulado, ecclesiologia,
   escatologia, doctrina, identidad, mision, iglesia, pacto, torah, restauracion,
   santidad, gracia, fe, obediencia
6. "versiculos_citados": extrae solo versículos explícitamente mencionados en el desarrollo.
   Formato: ["Gálatas 2:20", "Juan 3:16"]. Array vacío si ninguno.
7. "titulo_corto": máximo 60 caracteres, sin caracteres especiales (: " / \\ ? * | < >),
   sin raya em ( — ).
8. "notas_relacionadas": solo si hay certeza de conexión lógica con notas conocidas.
   Usa formato wikilink: ["[[ZK-ID Titulo Corto]]"]. Array vacío si no hay certeza.

Esquema de salida (array de N objetos, uno por premisa):
[
  {
    "titulo": "...",
    "titulo_corto": "...",
    "subtipo": "...",
    "tema": "...",
    "tags": ["...", "..."],
    "versiculos_citados": [],
    "desarrollo": "...",
    "notas_relacionadas": []
  }
]\
"""

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> str:
    """Extrae JSON de un string que puede contener texto extra o bloques de código."""
    for pattern in (
        r"```(?:json)?\s*(\{[\s\S]*\}|\[[\s\S]*\])\s*```",
        r"```(?:json)?\s*(\{[\s\S]*\}|\[[\s\S]*\])\s*$",
    ):
        m = re.search(pattern, text, re.DOTALL)
        if m:
            return m.group(1).strip()
    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        end   = text.rfind(closer)
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]
    return text.strip()


def _yaml_str(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", "")


def _safe_tags(tags: object) -> str:
    if not isinstance(tags, list):
        return "[]"
    return "[" + ", ".join(f'"{t}"' for t in tags) + "]"


def _safe_list(items: object) -> str:
    if not isinstance(items, list):
        return "[]"
    return "[" + ", ".join(f'"{_yaml_str(str(i))}"' for i in items) + "]"


def _next_sequence(base_path: Path, datestamp: str, timestamp: str) -> int:
    """Calcula el próximo número de secuencia libre para este instante."""
    prefix = f"ZK-{datestamp}-{timestamp}-"
    taken = {
        int(f.stem.split("-")[-1])
        for f in base_path.glob(f"{prefix}*.md")
        if f.stem.split("-")[-1].isdigit()
    }
    n = 1
    while n in taken:
        n += 1
    return n


def _normalize_premise(raw: dict) -> dict | None:
    """Intenta normalizar una premisa con campos distintos al schema esperado."""
    title_keys = ("titulo", "title", "idea", "premisa", "concepto")
    body_keys  = ("desarrollo", "development", "texto", "body", "contenido", "cuerpo")
    titulo     = next((raw[k] for k in title_keys if k in raw and raw[k]), None)
    desarrollo = next((raw[k] for k in body_keys  if k in raw and raw[k]), None)
    if titulo and desarrollo:
        return {"titulo": str(titulo), "desarrollo": str(desarrollo)}
    return None


def _get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY no configurada en el entorno.")
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def _call_claude(
    client: anthropic.Anthropic,
    model: str,
    system: str,
    user_message: str,
    label: str,
) -> str:
    """Llama a la API de Claude con un retry en caso de fallo."""
    last_error: Exception | None = None
    raw_response = ""
    for attempt in range(2):
        try:
            message = client.messages.create(
                model=model,
                max_tokens=4096,
                system=system,
                messages=[{"role": "user", "content": user_message}],
            )
            return message.content[0].text
        except Exception as e:
            last_error = e
            if attempt == 0:
                print(f"  ⚠ {label}: error de API — reintentando en 2s... ({e})")
                time.sleep(2)
    print(f"❌ {label}: falló después de 2 intentos — {last_error}")
    sys.exit(1)


# ─── FASE 1: EXTRACTOR (Claude Haiku) ──────────────────────────────────────────

def call_extractor(client: anthropic.Anthropic, raw_text: str) -> list[dict]:
    """Extrae premisas atómicas del texto crudo usando Claude Haiku."""
    raw_response = _call_claude(
        client, MODEL_EXTRACTOR, SYSTEM_PROMPT_EXTRACTOR, raw_text, "Extractor"
    )
    try:
        parsed = json.loads(_extract_json(raw_response))
    except json.JSONDecodeError as e:
        print(f"❌ Extractor: respuesta no es JSON válido — {e}")
        print(f"  Respuesta cruda (primeros 500 chars):\n  {raw_response[:500]}")
        sys.exit(1)

    # Aceptar {"premisas": [...]} o directamente [...]
    candidates = parsed.get("premisas", parsed) if isinstance(parsed, dict) else parsed
    if not isinstance(candidates, list):
        print(f"❌ Extractor: se esperaba una lista, se recibió {type(candidates).__name__}")
        sys.exit(1)

    premises: list[dict] = []
    for item in candidates:
        if isinstance(item, dict):
            normalized = _normalize_premise(item)
            if normalized:
                premises.append(normalized)
            else:
                print(f"  ⚠ Premisa ignorada (campos no reconocidos): {list(item.keys())}")

    if not premises:
        print("❌ Extractor: ninguna premisa válida extraída.")
        sys.exit(1)
    return premises


# ─── FASE 2: ORQUESTADOR (Claude Sonnet) ───────────────────────────────────────

def call_orchestrator(
    client: anthropic.Anthropic, premises: list[dict], dominio: str
) -> list[dict]:
    """Convierte premisas en especificaciones ZK usando Claude Sonnet."""
    user_message = (
        f"Dominio del contenido: {dominio}\n\n"
        f"Premisas a estructurar:\n{json.dumps(premises, ensure_ascii=False, indent=2)}"
    )
    raw_response = _call_claude(
        client, MODEL_ORCHESTRATOR, SYSTEM_PROMPT_ORCHESTRATOR, user_message, "Orquestador"
    )
    try:
        specs = json.loads(_extract_json(raw_response))
    except json.JSONDecodeError as e:
        print(f"❌ Orquestador: respuesta no es JSON válido — {e}")
        print(f"  Respuesta cruda (primeros 500 chars):\n  {raw_response[:500]}")
        sys.exit(1)

    if not isinstance(specs, list):
        print(f"❌ Orquestador: se esperaba un array JSON, se recibió {type(specs).__name__}")
        sys.exit(1)
    return specs


# ─── VALIDACIÓN ────────────────────────────────────────────────────────────────

REQUIRED_FIELDS = {
    "titulo", "titulo_corto", "subtipo", "tema",
    "tags", "versiculos_citados", "desarrollo", "notas_relacionadas",
}
VALID_SUBTIPOS = {"conceptual", "argumental", "exegetica", "narrativa", "conexion"}
VALID_TEMAS    = {
    "01_Origenes", "02_HistoriaDeIsrael", "03_Escatologia—Destino", "04_ExegesisNT",
    "05_DoctrinasFundamentales", "06_DiscipuladoVidaCristiana",
    "07_PredicacionesDevocionales", "08_Academico",
}
BAD_CHARS = set(':"/\\?*|<>')


def validate_spec(spec: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS - set(spec.keys())
    if missing:
        errors.append(f"Campos faltantes: {missing}")
    if spec.get("subtipo") not in VALID_SUBTIPOS:
        errors.append(f"subtipo inválido: {spec.get('subtipo')!r}")
    if spec.get("tema") not in VALID_TEMAS:
        errors.append(f"tema inválido: {spec.get('tema')!r}")
    titulo_corto = str(spec.get("titulo_corto", ""))
    if len(titulo_corto) > 60:
        errors.append(f"titulo_corto excede 60 chars ({len(titulo_corto)})")
    bad = BAD_CHARS & set(titulo_corto)
    if bad:
        errors.append(f"titulo_corto contiene caracteres inválidos: {bad}")
    if not str(spec.get("desarrollo", "")).strip():
        errors.append("desarrollo vacío")
    return errors


# ─── FASE 3: CREACIÓN DE ARCHIVOS ──────────────────────────────────────────────

def create_zk_file(spec: dict, base_path: Path, zk_id: str, dominio: str) -> Path:
    titulo_corto = spec["titulo_corto"]
    filepath     = base_path / f"{zk_id} {titulo_corto}.md"
    today        = datetime.now().strftime("%Y-%m-%d")

    notas_rel = spec.get("notas_relacionadas", [])
    conexiones_section = ""
    if notas_rel:
        links = "\n".join(f"- {link}" for link in notas_rel)
        conexiones_section = f"\n## Conexiones\n{links}\n"

    versiculos = spec.get("versiculos_citados", [])
    versiculo_header = f"\n> {versiculos[0]}\n" if versiculos else ""

    content = f"""\
---
id: {zk_id}
aliases:
  - "{_yaml_str(spec['titulo'])}"
titulo: "{_yaml_str(spec['titulo'])}"
tags: {_safe_tags(spec.get('tags', []))}
tipo: zettelkasten
subtipo: {spec['subtipo']}
tema: {spec['tema']}
fuente: "dictado"
versiculos_citados: {_safe_list(versiculos)}
dominio: {dominio}
fecha: {today}
version_yaml: "2.0"
fecha_ingesta: {today}
---

# {spec['titulo']}
{versiculo_header}
{spec['desarrollo']}
{conexiones_section}
## Fuente
`Ingesta acústica — {today}`
"""
    filepath.write_text(content, encoding="utf-8")
    return filepath


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline de Ingesta Acústica Estructurada: voz → notas ZK"
    )
    parser.add_argument(
        "transcript",
        help="Ruta al archivo de transcripción cruda (.txt o .md), relativa al vault o absoluta",
    )
    parser.add_argument(
        "--dominio",
        choices=["pastoral", "academico"],
        default="pastoral",
        help="Dominio de las notas (default: pastoral)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Crea los archivos físicos en 09_Zettelkasten/. Sin este flag solo muestra preview.",
    )
    args = parser.parse_args()

    transcript_path = Path(args.transcript)
    if not transcript_path.is_absolute():
        transcript_path = VAULT_ROOT / transcript_path
    if not transcript_path.exists():
        print(f"❌ Archivo no encontrado: {transcript_path}")
        sys.exit(1)

    raw_text = transcript_path.read_text(encoding="utf-8").strip()
    if len(raw_text) < 50:
        print("❌ La transcripción es demasiado corta (mínimo 50 caracteres).")
        sys.exit(1)

    zk_base = ZK_PATHS[args.dominio]
    zk_base.mkdir(parents=True, exist_ok=True)

    client = _get_client()

    # Fase 1 — Extracción
    print(f"📡 Fase 1 — Extrayendo premisas atómicas ({MODEL_EXTRACTOR})...")
    premises = call_extractor(client, raw_text)
    print(f"   → {len(premises)} premisa(s) extraída(s).")

    # Fase 2 — Orquestación
    print(f"🧠 Fase 2 — Estructurando metadatos ZK ({MODEL_ORCHESTRATOR})...")
    specs = call_orchestrator(client, premises, args.dominio)
    print(f"   → {len(specs)} especificación(es) generada(s).")

    # Validación
    print("\n🔍 Validando especificaciones...")
    valid_specs: list[dict] = []
    for i, spec in enumerate(specs):
        errors = validate_spec(spec)
        if errors:
            print(f"   ⚠ Spec #{i + 1} tiene errores — se omitirá:")
            for e in errors:
                print(f"     • {e}")
        else:
            valid_specs.append(spec)
    print(f"   → {len(valid_specs)}/{len(specs)} spec(s) válida(s).")

    if not valid_specs:
        print("❌ Ninguna especificación pasó la validación.")
        sys.exit(1)

    # Calcular IDs antes del preview para que sean fieles a lo que se crearía
    now       = datetime.now()
    datestamp = now.strftime("%Y%m%d")
    timestamp = now.strftime("%H%M")
    base_seq  = _next_sequence(zk_base, datestamp, timestamp)

    previews: list[tuple[dict, str]] = [
        (spec, f"ZK-{datestamp}-{timestamp}-{(base_seq + i):03d}")
        for i, spec in enumerate(valid_specs)
    ]

    # Preview siempre, independiente de --write
    print("\n📋 PREVIEW — Notas que se crearían:")
    for i, (spec, zk_id) in enumerate(previews):
        print(f"\n  [{i + 1}] {zk_id}")
        print(f"       Archivo:  {zk_id} {spec['titulo_corto']}.md")
        print(f"       Título:   {spec['titulo']}")
        print(f"       Subtipo:  {spec['subtipo']}  |  Tema: {spec['tema']}")
        print(f"       Tags:     {spec.get('tags', [])}")
        if spec.get("versiculos_citados"):
            print(f"       Versículos: {spec['versiculos_citados']}")
        if spec.get("notas_relacionadas"):
            print(f"       Conexiones: {spec['notas_relacionadas']}")
        preview_text = spec["desarrollo"][:120].replace("\n", " ")
        ellipsis = "..." if len(spec["desarrollo"]) > 120 else ""
        print(f"       Desarrollo: {preview_text}{ellipsis}")

    if not args.write:
        print(
            "\n⚠  Modo preview. Para crear los archivos físicos, agrega --write al comando."
        )
        return

    # Fase 3 — Creación
    print("\n📝 Fase 3 — Creando archivos .md...")
    created: list[Path] = []
    for spec, zk_id in previews:
        path = create_zk_file(spec, zk_base, zk_id, args.dominio)
        created.append(path)
        print(f"   ✅ {path.name}")

    print(f"\n✓ Pipeline completado. {len(created)} nota(s) ZK creada(s) en:")
    print(f"  {zk_base.relative_to(VAULT_ROOT)}/")
    print("\n→ Siguiente paso recomendado:")
    print("  python3 _Scripts/semantic_indexer.py --mode update")


if __name__ == "__main__":
    main()
