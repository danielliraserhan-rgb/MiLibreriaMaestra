import os
import sys
import re
import json
from datetime import datetime

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(VAULT_ROOT, "_Skills", "scrivener-manifest.json")
EXPORT_DIR = os.path.join(VAULT_ROOT, "Inbox", "scrivener-sync", "export")


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"archivos": []}


def save_manifest(manifest):
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def clean_for_scrivener(body):
    # [[link|alias]] → alias
    body = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', body)
    # [[link]] → link
    body = re.sub(r'\[\[([^\]]+)\]\]', r'\1', body)
    # #tags inline → eliminados (solo tags standalone, no encabezados #)
    body = re.sub(r'(?<!\S)#[a-zA-ZáéíóúÁÉÍÓÚñÑ][a-zA-ZáéíóúÁÉÍÓÚñÑ0-9_/-]*', '', body)
    # Limpiar espacios dobles dejados por eliminación de tags
    body = re.sub(r'  +', ' ', body)
    body = re.sub(r' \n', '\n', body)
    return body


def export_to_scrivener(vault_path, output_filename=None, preview=False):
    if not os.path.exists(vault_path):
        print(f"❌ Error: Archivo no encontrado: {vault_path}")
        return

    with open(vault_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar YAML del body
    if content.startswith("---"):
        parts = content.split("---", 2)
        body = parts[2].lstrip() if len(parts) >= 3 else content
    else:
        body = content

    clean_body = clean_for_scrivener(body)

    # Determinar ruta de salida
    if output_filename is None:
        base = os.path.splitext(os.path.basename(vault_path))[0]
        output_filename = f"{base}.md"
    output_path = os.path.join(EXPORT_DIR, output_filename)

    # Calcular diff para reporte
    old_lines = body.splitlines()
    new_lines = clean_body.splitlines()
    wiki_links = len(re.findall(r'\[\[([^\]]+)\]\]', body))
    tags = len(re.findall(r'(?<!\S)#[a-zA-ZáéíóúÁÉÍÓÚñÑ][a-zA-ZáéíóúÁÉÍÓÚñÑ0-9_/-]*', body))

    print(f"📋 DIFF LIMPIO — exportación para Scrivener:")
    print(f"   Origen:           {vault_path}")
    print(f"   Destino:          {output_path}")
    print(f"   YAML:             eliminado")
    print(f"   Wiki links:       {wiki_links} convertidos a texto plano")
    print(f"   Tags inline:      {tags} eliminados")
    print(f"   Líneas resultado: {len(new_lines)}")

    if preview:
        print(f"\n⏸  Modo preview — archivo NO escrito. Ejecuta sin --preview para confirmar.")
        return

    # Escribir export
    os.makedirs(EXPORT_DIR, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_body)

    print(f"\n✅ Exportación exitosa: {output_path}")

    # Actualizar manifest
    manifest = load_manifest()
    now = datetime.now().isoformat(timespec='seconds')
    entry = next((a for a in manifest["archivos"] if a["vault_path"] == vault_path), None)
    if entry:
        entry["ultima_export"] = now
        entry["estado"] = "sincronizado"
        entry["editado_en_vault_post_sync"] = False
    else:
        manifest["archivos"].append({
            "vault_path": vault_path,
            "scrivener_nombre": os.path.splitext(output_filename)[0],
            "estado": "sincronizado",
            "ultima_sync": None,
            "ultima_export": now,
            "editado_en_vault_post_sync": False
        })
    save_manifest(manifest)
    print(f"   Manifest: estado=sincronizado, ultima_export={now}")


if __name__ == "__main__":
    args = sys.argv[1:]
    preview = "--preview" in args
    args = [a for a in args if a != "--preview"]

    if len(args) < 1:
        print("Uso: python3 _Scripts/scrivener_export.py <ruta_vault> [nombre_salida.md] [--preview]")
    elif len(args) == 1:
        export_to_scrivener(args[0], preview=preview)
    else:
        export_to_scrivener(args[0], args[1], preview=preview)
