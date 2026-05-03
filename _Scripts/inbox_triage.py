import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent

def triage_file(filepath, meta_json_str):
    if not os.path.exists(filepath):
        print(f"❌ Error: Archivo no encontrado ({filepath})")
        return

    try:
        meta = json.loads(meta_json_str)
    except json.JSONDecodeError:
        print("❌ Error: JSON de metadatos inválido.")
        return

    # Generar YAML v2 estandarizado
    yaml_content = f"""---
title: "{os.path.splitext(os.path.basename(filepath))[0]}"
tipo: "{meta.get('tipo', '')}"
tema: "{meta.get('tema', '')}"
libro_biblico_principal: ""
personajes: []
versiculos_citados: []
temas_principales: []
seo_keywords: []
fecha: "{datetime.now().strftime('%Y-%m-%d')}"
estado: "en_proceso"
dominio: "{meta.get('dominio', '')}"
modo: "{meta.get('modo', '')}"
fase: ""
serie: ""
fuente: ""
author_quotes: []
zettelkasten_notes: []
coaching_notes: []
version_yaml: "2.0"
fecha_actualizacion: "{datetime.now().strftime('%Y-%m-%d')}"
scrivener_sync:
  estado: ""
  ultima_sync: ""
  ultima_export: ""
  scrivener_nombre: ""
---
"""

    # Leer contenido original
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Evitar duplicar YAML si el archivo ya tenía uno
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].lstrip()

    final_content = yaml_content + content

    # Asegurar directorio destino — validar que quede dentro del vault
    destino_dir = meta.get('destino', '')
    if not destino_dir:
        print("❌ Error: No se especificó carpeta destino.")
        return

    destino_path = (VAULT_ROOT / destino_dir).resolve()
    if not destino_path.is_relative_to(VAULT_ROOT.resolve()):
        print(f"❌ Error: destino fuera del vault ({destino_dir})")
        return

    destino_path.mkdir(parents=True, exist_ok=True)
    dest_filepath = destino_path / os.path.basename(filepath)

    # Escribir y mover
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)

    shutil.move(filepath, str(dest_filepath))
    print(f"✅ Triage completado: {dest_filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 _Scripts/inbox_triage.py <ruta_archivo> '<json_metadatos>'")
    else:
        triage_file(sys.argv[1], sys.argv[2])
