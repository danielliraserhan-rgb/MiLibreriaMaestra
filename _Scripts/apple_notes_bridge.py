#!/usr/bin/env python3
"""
apple_notes_bridge.py — Módulo 3: sincronización Apple Notes → Inbox/
Carpeta Apple Notes: "MiLibreria — Inbox"
Tags en primera línea: #inbox | #listo | #procesado

Requiere MCP: mcp__Read_and_Write_Apple_Notes__ activo en la sesión de Claude Code.
Este script define la lógica; el transporte MCP se invoca vía el protocolo del server.

Uso:
  python _Scripts/apple_notes_bridge.py --mode sync
  python _Scripts/apple_notes_bridge.py --mode status
  python _Scripts/apple_notes_bridge.py --mode clean
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
INBOX_DIR = VAULT_ROOT / "Inbox"
NOTES_FOLDER = "MiLibreria — Inbox"

TAG_INBOX = "#inbox"
TAG_LISTO = "#listo"
TAG_PROCESADO = "#procesado"
ALL_TAGS = (TAG_INBOX, TAG_LISTO, TAG_PROCESADO)


# ── MCP transport stub ───────────────────────────────────────────────────────
# En producción, Claude Code invoca el MCP server directamente.
# Este módulo puede ser importado por un agente que inyecte un transport real.

_mcp_transport = None  # set externamente si se usa como librería


def set_mcp_transport(transport_fn):
    """Inyectar función de transporte real: fn(method, params) -> dict."""
    global _mcp_transport
    _mcp_transport = transport_fn


def _call_mcp(method: str, params: dict) -> dict:
    if _mcp_transport is not None:
        return _mcp_transport(method, params)
    # Stub: log la llamada y devuelve estructura vacía
    print(f"[MCP STUB] {method}({json.dumps(params, ensure_ascii=False)[:100]})")
    return {"result": None, "error": "MCP transport no configurado"}


# ── Apple Notes helpers ──────────────────────────────────────────────────────

def list_notes() -> list:
    result = _call_mcp("list_notes", {"folder": NOTES_FOLDER})
    notes = result.get("result") or []
    return notes if isinstance(notes, list) else []


def get_note_content(note_id: str) -> str:
    result = _call_mcp("get_note", {"id": note_id})
    content = (result.get("result") or {}).get("content", "")
    return content if isinstance(content, str) else ""


def update_note(note_id: str, new_content: str) -> bool:
    result = _call_mcp("update_note", {"id": note_id, "content": new_content})
    return result.get("error") is None


def parse_tag(content: str) -> str | None:
    """Return the first tag found in the first non-empty line."""
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        for tag in ALL_TAGS:
            if tag in line:
                return tag
        break  # only check first non-empty line
    return None


def replace_tag(content: str, old_tag: str, new_tag: str) -> str:
    """Replace old_tag with new_tag in the first non-empty line only."""
    lines = content.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip():
            lines[i] = line.replace(old_tag, new_tag, 1)
            break
    return "".join(lines)


def safe_filename(title: str) -> str:
    """Convert title to a safe filename (no special chars)."""
    clean = re.sub(r'[<>:"/\\|?*#\n\r\t]', "", title).strip()
    return clean or "nota_sin_titulo"


def get_note_title(note: dict, content: str) -> str:
    """Best-effort title: note metadata title first, then second non-empty line."""
    title = (note.get("title") or "").strip()
    if title:
        return title
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    # Skip the tag line, use next line as title
    for line in lines[1:]:
        if line:
            return line[:80]
    return "nota_sin_titulo"


def get_note_body(content: str) -> str:
    """Return content without the first (tag) line."""
    lines = content.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip():
            return "".join(lines[i + 1:]).lstrip("\n")
    return content


# ── CLI commands ─────────────────────────────────────────────────────────────

def cmd_sync():
    """Transfer #listo notes to Inbox/. Mark them #procesado."""
    notes = list_notes()
    synced = 0

    for note in notes:
        note_id = note.get("id", "")
        if not note_id:
            continue

        content = get_note_content(note_id)
        if not content:
            continue

        tag = parse_tag(content)
        if tag != TAG_LISTO:
            continue

        title = get_note_title(note, content)
        filename = safe_filename(title) + ".md"
        target = INBOX_DIR / filename

        if target.exists():
            print(f"SKIP [ya existe]: Inbox/{filename}")
            continue

        body = get_note_body(content)
        target.write_text(body, encoding="utf-8")
        print(f"✓ Creado: Inbox/{filename}")

        new_content = replace_tag(content, TAG_LISTO, TAG_PROCESADO)
        if update_note(note_id, new_content):
            print(f"  → Nota actualizada a {TAG_PROCESADO}")
        else:
            print(f"  ✗ No se pudo actualizar la nota en Apple Notes")

        synced += 1

    print(f"\nSincronizadas: {synced} nota(s)")


def cmd_status():
    """Print note count by tag."""
    notes = list_notes()
    counts = {TAG_INBOX: 0, TAG_LISTO: 0, TAG_PROCESADO: 0, "sin_tag": 0}

    for note in notes:
        note_id = note.get("id", "")
        content = get_note_content(note_id) if note_id else ""
        tag = parse_tag(content)
        key = tag if tag in counts else "sin_tag"
        counts[key] += 1

    print(f"\nEstado — carpeta Apple Notes: \"{NOTES_FOLDER}\"")
    print(f"  {TAG_INBOX:<14} {counts[TAG_INBOX]}")
    print(f"  {TAG_LISTO:<14} {counts[TAG_LISTO]}")
    print(f"  {TAG_PROCESADO:<14} {counts[TAG_PROCESADO]}")
    print(f"  {'sin_tag':<14} {counts['sin_tag']}")
    print(f"  {'TOTAL':<14} {sum(counts.values())}")


def cmd_clean():
    """List #procesado notes older than 30 days. Does NOT delete anything."""
    notes = list_notes()
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    old_notes = []

    for note in notes:
        note_id = note.get("id", "")
        content = get_note_content(note_id) if note_id else ""
        tag = parse_tag(content)

        if tag != TAG_PROCESADO:
            continue

        modified_str = note.get("modified") or note.get("created") or ""
        try:
            modified = datetime.fromisoformat(modified_str.replace("Z", "+00:00"))
        except Exception:
            continue

        if modified < cutoff:
            old_notes.append({
                "id": note_id,
                "title": note.get("title", "sin título"),
                "modified": modified_str,
            })

    if not old_notes:
        print(f"No hay notas {TAG_PROCESADO} con más de 30 días.")
        return

    print(f"\nNotas {TAG_PROCESADO} con >30 días (solo listadas — no se elimina nada):\n")
    print(f"{'Modificada':<28} Título")
    print("-" * 70)
    for n in old_notes:
        print(f"{n['modified']:<28} {n['title']}")
    print(f"\nTotal: {len(old_notes)}")


def main():
    parser = argparse.ArgumentParser(description="Apple Notes bridge — MiLibreriaMaestra")
    parser.add_argument("--mode", choices=["sync", "status", "clean"], required=True)
    args = parser.parse_args()

    if args.mode == "sync":
        cmd_sync()
    elif args.mode == "status":
        cmd_status()
    elif args.mode == "clean":
        cmd_clean()


if __name__ == "__main__":
    main()
