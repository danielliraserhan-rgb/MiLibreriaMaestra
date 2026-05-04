import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(VAULT_ROOT, "_Skills", "scrivener-manifest.json")
_VAULT_ROOT_PATH = Path(VAULT_ROOT).resolve()


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"archivos": []}


def save_manifest(manifest):
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def update_manifest(vault_path, scrivener_nombre):
    manifest = load_manifest()
    now = datetime.now().isoformat(timespec='seconds')
    entry = next((a for a in manifest["archivos"] if a["vault_path"] == vault_path), None)
    if entry:
        entry["ultima_sync"] = now
        entry["estado"] = "sincronizado"
        entry["editado_en_vault_post_sync"] = False
    else:
        manifest["archivos"].append({
            "vault_path": vault_path,
            "scrivener_nombre": scrivener_nombre,
            "estado": "sincronizado",
            "ultima_sync": now,
            "ultima_export": None,
            "editado_en_vault_post_sync": False
        })
    save_manifest(manifest)


def sync_scrivener(src_path, dest_path):
    if not Path(src_path).resolve().is_relative_to(_VAULT_ROOT_PATH):
        print(f"❌ Error: origen fuera del vault ({src_path})")
        return
    if not Path(dest_path).resolve().is_relative_to(_VAULT_ROOT_PATH):
        print(f"❌ Error: destino fuera del vault ({dest_path})")
        return
    if not os.path.exists(src_path):
        print(f"❌ Error: Origen no encontrado: {src_path}")
        return

    # 1. Leer contenido de Scrivener
    with open(src_path, 'r', encoding='utf-8') as f:
        new_content = f.read()

    # Strip YAML parcial que Scrivener haya exportado
    if new_content.startswith("---"):
        parts = new_content.split("---", 2)
        new_body = parts[2].lstrip() if len(parts) >= 3 else new_content
    else:
        new_body = new_content

    # 2. Manejar destino — preservar YAML del vault
    old_body = ""
    if os.path.exists(dest_path):
        with open(dest_path, 'r', encoding='utf-8') as f:
            vault_content = f.read()
        if vault_content.startswith("---"):
            parts = vault_content.split("---", 2)
            yaml_block = f"---{parts[1]}---\n"
            old_body = parts[2].lstrip() if len(parts) >= 3 else ""
        else:
            yaml_block = "---\nfuente: scrivener\n---\n"
            old_body = vault_content
    else:
        yaml_block = "---\nfuente: scrivener\n---\n"

    # 3. Actualizar fecha_actualizacion en YAML
    now_date = datetime.now().strftime("%Y-%m-%d")
    if yaml_block.endswith("---\n"):
        base = yaml_block[:-4]
        if "fecha_actualizacion:" in base:
            base = re.sub(r'fecha_actualizacion:.*\n', f'fecha_actualizacion: "{now_date}"\n', base)
        else:
            base += f'fecha_actualizacion: "{now_date}"\n'
        yaml_block = base + "---\n"

    # 4. Fusionar y guardar
    final_output = yaml_block + new_body
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_output)

    # 5. Reporte de diff
    old_lines = len(old_body.splitlines())
    new_lines = len(new_body.splitlines())
    diff = new_lines - old_lines
    sign = "+" if diff >= 0 else ""
    print(f"✅ Sincronización exitosa: {dest_path}")
    print(f"   Contenido: {old_lines} → {new_lines} líneas ({sign}{diff})")

    # 6. Actualizar manifest
    scrivener_nombre = os.path.splitext(os.path.basename(src_path))[0]
    update_manifest(dest_path, scrivener_nombre)
    print(f"   Manifest: estado=sincronizado, ultima_sync={datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 _Scripts/scrivener_bridge.py <origen_scrivener> <destino_vault>")
    else:
        sync_scrivener(sys.argv[1], sys.argv[2])
