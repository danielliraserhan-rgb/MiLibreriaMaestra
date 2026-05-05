#!/usr/bin/env python3
"""
coaching_selector.py — Guardia de fase y selector de modo para coaching S2.

Uso: python3 _Scripts/coaching_selector.py "Temas/ruta/archivo.md"

Retorna JSON:
  {
    "puede_coaching": true | false,
    "modo_sugerido": "voz" | "teologia" | "estructura" | "ritmo" | "auto",
    "mensaje": "Texto para mostrar a Daniel"
  }

Errores retornan:
  {"puede_coaching": false, "modo_sugerido": null, "mensaje": "Descripción del error"}
"""

import sys
import json
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent


def leer_yaml_frontmatter(filepath: Path) -> dict:
    """Lee el bloque YAML del frontmatter sin dependencias externas."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {"_error": f"Archivo no encontrado: {filepath}"}
    except Exception as e:
        return {"_error": str(e)}

    if not text.startswith("---"):
        return {}

    lines = text.split("\n")
    yaml_lines = []
    in_block = False
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_block = True
            continue
        if in_block:
            if line.strip() == "---":
                break
            yaml_lines.append(line)

    data = {}
    for line in yaml_lines:
        if ":" in line and not line.startswith(" ") and not line.startswith("#"):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip().strip('"').strip("'")

    return data


def sugerir_modo(yaml: dict) -> str:
    """
    Sugiere el modo de coaching más útil según los metadatos del archivo.

    Jerarquía:
    1. dominio academico → modo "teologia" (análisis argumental/doctrinal)
    2. tipo oral (dictado/grabacion) → modo "voz" (marcas de oralidad presentes)
    3. tipo libro o borrador largo → modo "estructura"
    4. modo 4 (guia-estudio) → modo "estructura"
    5. default → "auto" (Claude evalúa al leer)
    """
    dominio = yaml.get("dominio", "").lower()
    fuente = yaml.get("fuente", "").lower()
    tipo = yaml.get("tipo", "").lower()
    modo = yaml.get("modo", "").lower()

    if dominio == "academico":
        return "teologia"

    if fuente in ("dictado", "grabacion") or "oral" in tipo:
        return "voz"

    if fuente in ("borrador", "clase", "conferencia") and "libro" in tipo:
        return "estructura"

    if "4" in modo or "guia" in modo:
        return "estructura"

    if "7" in modo or "grupos" in modo:
        return "ritmo"

    return "auto"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "puede_coaching": False,
            "modo_sugerido": None,
            "mensaje": "Uso: python3 _Scripts/coaching_selector.py \"ruta/archivo.md\""
        }))
        sys.exit(1)

    ruta_relativa = sys.argv[1]
    filepath = VAULT_ROOT / ruta_relativa

    if not filepath.exists():
        print(json.dumps({
            "puede_coaching": False,
            "modo_sugerido": None,
            "mensaje": f"Archivo no encontrado: {ruta_relativa}"
        }))
        sys.exit(1)

    yaml = leer_yaml_frontmatter(filepath)

    if "_error" in yaml:
        print(json.dumps({
            "puede_coaching": False,
            "modo_sugerido": None,
            "mensaje": f"Error leyendo archivo: {yaml['_error']}"
        }))
        sys.exit(1)

    fase_sistema = yaml.get("fase_sistema", "").strip()

    if not fase_sistema or fase_sistema == "sin_procesar":
        estado_actual = fase_sistema or "sin_procesar"
        print(json.dumps({
            "puede_coaching": False,
            "modo_sugerido": None,
            "mensaje": (
                f"⚠ El archivo '{filepath.name}' no ha sido catalogado todavía "
                f"(fase_sistema: '{estado_actual}'). "
                "Ejecuta primero: inbox <archivo> o bulk."
            )
        }))
        sys.exit(0)

    if fase_sistema not in ("catalogado", "coaching_completado"):
        print(json.dumps({
            "puede_coaching": False,
            "modo_sugerido": None,
            "mensaje": (
                f"Estado inesperado: fase_sistema='{fase_sistema}'. "
                "Solo se puede iniciar coaching desde estado 'catalogado'."
            )
        }))
        sys.exit(0)

    modo_sugerido = sugerir_modo(yaml)

    dominio = yaml.get("dominio", "desconocido")
    tipo = yaml.get("tipo", "")
    fuente = yaml.get("fuente", "")
    detalles = f"dominio={dominio}"
    if tipo:
        detalles += f", tipo={tipo}"
    if fuente:
        detalles += f", fuente={fuente}"

    print(json.dumps({
        "puede_coaching": True,
        "modo_sugerido": modo_sugerido,
        "mensaje": (
            f"✓ Archivo catalogado. Modo sugerido: {modo_sugerido} "
            f"({detalles}). "
            f"Usa 'inicia coaching modo:{modo_sugerido}' o 'inicia coaching' para auto."
        )
    }))


if __name__ == "__main__":
    main()
