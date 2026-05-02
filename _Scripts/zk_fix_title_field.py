#!/usr/bin/env python3
"""
Fix the 8 ZK files that use 'title' instead of 'titulo' — rename them
to the correct {id} {titulo_corto}.md format and update wikilinks + aliases.
"""

import os
import re
import yaml
from pathlib import Path

VAULT = Path(__file__).parent.parent
ZK_PASTORAL = VAULT / "09_Zettelkasten" / "pastoral"
PROBLEMATIC_CHARS = r'[:"\/\\?*|<>]'


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


def parse_frontmatter(content: str):
    if not content.startswith("---"):
        return {}, "", -1
    end = content.find("\n---", 3)
    if end == -1:
        return {}, "", -1
    raw_yaml = content[3:end + 1]
    yaml_end_pos = end + 4
    try:
        data = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError:
        data = {}
    return data, raw_yaml, yaml_end_pos


def build_aliases_yaml(aliases_list):
    lines = ["aliases:"]
    for a in aliases_list:
        lines.append(f'  - "{a}"')
    return "\n".join(lines)


def get_all_md_files(root: Path):
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        yield path


# ── Find the 8 files that still have ID as their titulo_corto ────────────────

problem_files = [
    f for f in ZK_PASTORAL.iterdir()
    if f.is_file() and f.suffix == ".md" and
    # Their stem ends with the pattern " ZK-YYYYMMDD-HHMM-NNN" (ID repeated)
    re.search(r' ZK-\d{8}-\d{4}-\d{3}$', f.stem)
]

print(f"Found {len(problem_files)} files to fix:")
for f in problem_files:
    print(f"  {f.name}")

renamed_ok = []
wikilink_updated_files = {}

for zk_file in problem_files:
    content = zk_file.read_text(encoding="utf-8")
    old_stem = zk_file.stem
    data, raw_yaml, yaml_end_pos = parse_frontmatter(content)

    # Extract id
    zk_id = str(data.get("id", "")).strip()
    if not zk_id:
        print(f"  SKIP (no id): {zk_file.name}")
        continue

    # Get title (the 'title' field, not 'titulo')
    title = str(data.get("title") or data.get("titulo") or "").strip()
    if not title:
        print(f"  SKIP (no title): {zk_file.name}")
        continue

    titulo_corto = make_titulo_corto(title)
    new_stem = f"{zk_id} {titulo_corto}"

    new_path = ZK_PASTORAL / f"{new_stem}.md"

    if new_path.exists():
        print(f"  SKIP (dest exists): {new_stem}.md")
        continue

    # Rename file
    os.rename(zk_file, new_path)
    renamed_ok.append((old_stem, new_stem))
    print(f"  ✓ {old_stem}.md\n    → {new_stem}.md")

    # Update aliases in the renamed file
    current_aliases = data.get("aliases") or []
    if isinstance(current_aliases, str):
        current_aliases = [current_aliases]
    current_aliases = list(current_aliases)

    # The old alias stored was the old_stem (which was the ID-only name before the
    # first rename pass). Keep it. Now also make sure both old stems are present.
    # The very first rename stored "{id} {id}" as stem — that's what old_stem is now.
    # The ORIGINAL file name before any processing was just "{id}.md" stem.
    original_id_only_stem = zk_id  # e.g. ZK-20260428-1000-001

    for alias_candidate in [old_stem, original_id_only_stem]:
        if alias_candidate not in current_aliases:
            current_aliases.append(alias_candidate)

    aliases_yaml_str = build_aliases_yaml(current_aliases)
    yaml_inner = raw_yaml

    if re.search(r'^aliases:', yaml_inner, re.MULTILINE):
        yaml_inner = re.sub(
            r'^aliases:(?:[ \t]*\n(?:[ \t]+[^\n]*\n)*|[^\n]*\n)',
            aliases_yaml_str + "\n",
            yaml_inner,
            count=1,
            flags=re.MULTILINE
        )
    else:
        yaml_inner, count = re.subn(
            r'(^id:[^\n]*\n)',
            r'\1' + aliases_yaml_str + "\n",
            yaml_inner,
            count=1,
            flags=re.MULTILINE
        )
        if count == 0:
            yaml_inner = aliases_yaml_str + "\n" + yaml_inner

    rest_of_file = content[yaml_end_pos:]
    new_content = "---" + yaml_inner + "---" + rest_of_file
    new_path.write_text(new_content, encoding="utf-8")

# ── Update wikilinks across the vault for both renames ───────────────────────

if renamed_ok:
    all_md = list(get_all_md_files(VAULT))
    print(f"\nScanning {len(all_md)} files for wikilinks...")

    for md_path in all_md:
        try:
            original = md_path.read_text(encoding="utf-8")
        except Exception:
            continue

        modified = original
        file_replacements = 0

        for old_stem, new_stem in renamed_ok:
            old_escaped = re.escape(old_stem)
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

print("\n=== FIX REPORT ===")
print(f"Files corrected: {len(renamed_ok)}")
print(f"Wikilinks updated in: {len(wikilink_updated_files)} files")
for fpath, count in sorted(wikilink_updated_files.items()):
    rel = os.path.relpath(fpath, str(VAULT))
    print(f"  - {rel} ({count} replacements)")
