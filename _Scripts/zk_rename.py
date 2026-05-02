#!/usr/bin/env python3
"""
ZK Rename Script — MiLibreriaMaestra
Renames all ZK notes in 09_Zettelkasten/pastoral/ to {id} {titulo_corto}.md format.
Also updates wikilinks across the entire vault and adds aliases to renamed notes.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

VAULT = Path(__file__).parent.parent
ZK_PASTORAL = VAULT / "09_Zettelkasten" / "pastoral"
PROBLEMATIC_CHARS = r'[:"\/\\?*|<>]'


# ── helpers ──────────────────────────────────────────────────────────────────

def clean_filename(text: str) -> str:
    text = re.sub(PROBLEMATIC_CHARS, "", text)
    text = re.sub(r"  +", " ", text).strip()
    return text


def truncate_to_words(text: str, max_len: int = 60) -> str:
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_space = truncated.rfind(" ")
    if last_space > 0:
        return truncated[:last_space]
    return truncated


def make_titulo_corto(titulo: str) -> str:
    if " — " in titulo:
        titulo = titulo.split(" — ")[0].strip()
    cleaned = clean_filename(titulo)
    return truncate_to_words(cleaned, 60)


def extract_yaml_field_regex(content: str, field: str):
    pattern = rf'^{field}:\s*["\']?([^"\'\n]+)["\']?\s*$'
    m = re.search(pattern, content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def parse_frontmatter(content: str):
    """Returns (data_dict, raw_yaml_text, yaml_block_end_pos)."""
    if not content.startswith("---"):
        return {}, "", -1
    end = content.find("\n---", 3)
    if end == -1:
        return {}, "", -1
    raw_yaml = content[3:end + 1]  # includes leading \n
    yaml_end_pos = end + 4         # position right after closing ---
    try:
        data = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError:
        data = {}
    return data, raw_yaml, yaml_end_pos


def build_aliases_yaml(aliases_list):
    """Return YAML aliases block string (no trailing newline)."""
    lines = ["aliases:"]
    for a in aliases_list:
        lines.append(f'  - "{a}"')
    return "\n".join(lines)


def get_all_md_files(root: Path):
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        yield path


# ── Step 1: Scan ZK pastoral notes ──────────────────────────────────────────

print("Scanning ZK pastoral notes...")

zk_files = sorted(
    [f for f in ZK_PASTORAL.iterdir() if f.is_file() and f.suffix == ".md"],
    key=lambda f: f.name
)

print(f"  Found {len(zk_files)} .md files")

rename_map = {}                  # old_stem -> new_stem
no_id_files = []
collision_candidates = defaultdict(list)  # new_stem -> [old_stems]

for zk_file in zk_files:
    content = zk_file.read_text(encoding="utf-8")
    old_stem = zk_file.stem

    data, _, _ = parse_frontmatter(content)

    # Extract id
    zk_id = data.get("id") or extract_yaml_field_regex(content, "id")
    if not zk_id:
        no_id_files.append(old_stem)
        continue
    zk_id = str(zk_id).strip()

    # Extract titulo
    titulo = data.get("titulo") or extract_yaml_field_regex(content, "titulo")
    if not titulo:
        titulo = old_stem

    titulo_corto = make_titulo_corto(str(titulo).strip())
    new_stem = f"{zk_id} {titulo_corto}"

    collision_candidates[new_stem].append(old_stem)
    rename_map[old_stem] = new_stem

print(f"  Mapped {len(rename_map)} files for rename consideration")

# ── Step 2: Detect collisions ────────────────────────────────────────────────

collisions = {k: v for k, v in collision_candidates.items() if len(v) > 1}
collision_stems = set(s for lst in collisions.values() for s in lst)

# ── Step 3: Execute renames ───────────────────────────────────────────────────

renamed_ok = []      # (old_stem, new_stem)
skipped_same = []
skipped_collision = []
skipped_dest_exists = []

for old_stem, new_stem in rename_map.items():
    if old_stem in collision_stems:
        skipped_collision.append((old_stem, new_stem))
        continue

    if old_stem == new_stem:
        skipped_same.append(old_stem)
        continue

    old_path = ZK_PASTORAL / f"{old_stem}.md"
    new_path = ZK_PASTORAL / f"{new_stem}.md"

    if new_path.exists():
        skipped_dest_exists.append((old_stem, new_stem))
        continue

    os.rename(old_path, new_path)
    renamed_ok.append((old_stem, new_stem))

print(f"  Renamed {len(renamed_ok)} files")
print(f"  Skipped (already correct name): {len(skipped_same)}")
print(f"  Skipped (collision): {len(skipped_collision)}")
print(f"  Skipped (dest exists): {len(skipped_dest_exists)}")

# ── Step 4: Update wikilinks across the vault ─────────────────────────────────

effective_renames = {old: new for old, new in renamed_ok}
wikilink_updated_files = {}  # str(filepath) -> int(count)

all_md = list(get_all_md_files(VAULT))
print(f"  Scanning {len(all_md)} .md files for wikilinks...")

for md_path in all_md:
    try:
        original = md_path.read_text(encoding="utf-8")
    except Exception:
        continue

    modified = original
    file_replacements = 0

    for old_stem, new_stem in effective_renames.items():
        old_escaped = re.escape(old_stem)
        # Match [[old_stem]] or [[old_stem|pipe text]]
        pattern = r'\[\[' + old_escaped + r'(\|[^\]\n]*)?\]\]'

        def replace_link(m, ns=new_stem):
            suffix = m.group(1) or ""
            return f"[[{ns}{suffix}]]"

        new_text, count = re.subn(pattern, replace_link, modified)
        if count > 0:
            modified = new_text
            file_replacements += count

    if modified != original:
        md_path.write_text(modified, encoding="utf-8")
        wikilink_updated_files[str(md_path)] = file_replacements

print(f"  Updated wikilinks in {len(wikilink_updated_files)} files")

# ── Step 5: Add aliases to renamed notes ─────────────────────────────────────

alias_added = []

for old_stem, new_stem in renamed_ok:
    new_path = ZK_PASTORAL / f"{new_stem}.md"
    if not new_path.exists():
        continue

    content = new_path.read_text(encoding="utf-8")
    data, raw_yaml, yaml_end_pos = parse_frontmatter(content)

    if yaml_end_pos == -1:
        continue  # No frontmatter

    # Get current aliases
    aliases = data.get("aliases") or []
    if isinstance(aliases, str):
        aliases = [aliases]
    aliases = list(aliases)

    if old_stem in aliases:
        continue  # Already there

    aliases.append(old_stem)
    aliases_yaml_str = build_aliases_yaml(aliases)

    # Work on the raw yaml text (between the --- markers, includes leading/trailing \n)
    yaml_inner = raw_yaml  # e.g. "\nid: ZK-...\ntitulo: ...\n"

    if re.search(r'^aliases:', yaml_inner, re.MULTILINE):
        # Replace existing aliases block (handles list format or inline)
        # Match from "aliases:" to the next top-level key or end of yaml
        yaml_inner = re.sub(
            r'^aliases:(?:[ \t]*\n(?:[ \t]+[^\n]*\n)*|[^\n]*\n)',
            aliases_yaml_str + "\n",
            yaml_inner,
            count=1,
            flags=re.MULTILINE
        )
    else:
        # Insert after id: line
        yaml_inner, count = re.subn(
            r'(^id:[^\n]*\n)',
            r'\1' + aliases_yaml_str + "\n",
            yaml_inner,
            count=1,
            flags=re.MULTILINE
        )
        if count == 0:
            # id line not found — prepend
            yaml_inner = aliases_yaml_str + "\n" + yaml_inner

    # Reconstruct the full file
    rest_of_file = content[yaml_end_pos:]
    new_content = "---" + yaml_inner + "---" + rest_of_file

    new_path.write_text(new_content, encoding="utf-8")
    alias_added.append(new_stem)

print(f"  Added aliases to {len(alias_added)} files")

# ── Step 6: Print audit report ────────────────────────────────────────────────

print()
print("=" * 65)
print("=== AUDITORÍA DE RENOMBRE ZK ===")
print("=" * 65)

print(f"\nRENOMBRES EJECUTADOS ({len(renamed_ok)} total):")
for old, new in renamed_ok:
    print(f"  ✓ {old}.md")
    print(f"    → {new}.md")

if skipped_same:
    print(f"\nARCHIVOS YA CON NOMBRE CORRECTO (sin cambio) ({len(skipped_same)}):")
    for s in skipped_same:
        print(f"  = {s}.md")

if skipped_dest_exists:
    print(f"\nSALTADOS — DESTINO YA EXISTE ({len(skipped_dest_exists)}):")
    for old, new in skipped_dest_exists:
        print(f"  ⚠ {old}.md → {new}.md")

print(f"\nWIKILINKS ACTUALIZADOS ({len(wikilink_updated_files)} archivos modificados):")
if wikilink_updated_files:
    for fpath, count in sorted(wikilink_updated_files.items()):
        rel = os.path.relpath(fpath, str(VAULT))
        print(f"  - {rel} ({count} reemplazos)")
else:
    print("  (ninguno)")

print(f"\nARCHIVOS CON ALIAS AGREGADO: {len(alias_added)}")
if alias_added:
    for a in alias_added:
        print(f"  + {a}.md")

if collisions:
    print(f"\nCOLISIONES DETECTADAS ({len(collisions)}):")
    for new_stem, old_list in collisions.items():
        print(f"  ⚠ Nuevo nombre: '{new_stem}'")
        print(f"    Conflicto entre:")
        for o in old_list:
            print(f"      - {o}.md")
    print("  (Estos archivos NO fueron renombrados)")
else:
    print("\nCOLISIONES DETECTADAS: ninguna")

if no_id_files:
    print(f"\nNOTAS SIN id EN YAML ({len(no_id_files)}):")
    for f in no_id_files:
        print(f"  ⚠ {f}.md")
else:
    print("\nNOTAS SIN id EN YAML: ninguna")

print()
print("=" * 65)
print("FIN DE AUDITORÍA")
print("=" * 65)
