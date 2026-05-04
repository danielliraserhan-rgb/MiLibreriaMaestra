import re
import sys
import os
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
_VAULT_ROOT_RESOLVED = VAULT_ROOT.resolve()


def clean_markdown(filepath):
    resolved = Path(filepath).resolve()
    if not resolved.is_relative_to(_VAULT_ROOT_RESOLVED):
        print(f"❌ Error: ruta fuera del vault ({filepath})")
        return
    if not os.path.exists(filepath):
        print(f"❌ Error: No se encontró el archivo {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Separar el YAML frontmatter del resto del contenido para no alterarlo
    parts = content.split("---", 2)
    if len(parts) >= 3 and content.startswith("---"):
        yaml_block = f"---{parts[1]}---"
        text_body = parts[2]
    else:
        yaml_block = ""
        text_body = content

    # 2. Reglas de limpieza RegEx
    # Eliminar más de dos saltos de línea consecutivos
    text_body = re.sub(r'\n{3,}', '\n\n', text_body)
    # Asegurar que haya un espacio después de los # en los títulos (ej. ##Título -> ## Título)
    text_body = re.sub(r'^(#+)([^ #\n])', r'\1 \2', text_body, flags=re.MULTILINE)
    # Limpiar espacios en blanco al final de las líneas
    text_body = re.sub(r' +$', '', text_body, flags=re.MULTILINE)
    # Estandarizar viñetas (cambiar asteriscos por guiones para homogeneidad, opcional)
    # text_body = re.sub(r'^(\s*)\* ', r'\1- ', text_body, flags=re.MULTILINE)

    final_content = yaml_block + text_body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"🧹 Formato adaptado con éxito: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 _Scripts/markdown_cleaner.py <ruta_al_archivo>")
    else:
        clean_markdown(sys.argv[1])
