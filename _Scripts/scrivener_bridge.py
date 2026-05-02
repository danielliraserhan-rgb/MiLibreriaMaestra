import os
import sys
import re

def sync_scrivener(src_path, dest_path):
    if not os.path.exists(src_path):
        print(f"❌ Error: Origen no encontrado: {src_path}")
        return

    # 1. Leer contenido de Scrivener
    with open(src_path, 'r', encoding='utf-8') as f:
        new_content = f.read()

    # Limpiar cualquier YAML parcial que Scrivener haya exportado
    if new_content.startswith("---"):
        parts = new_content.split("---", 2)
        new_body = parts[2].lstrip() if len(parts) >= 3 else new_content
    else:
        new_body = new_content

    # 2. Manejar el destino
    if os.path.exists(dest_path):
        # Preservar YAML existente en el Vault
        with open(dest_path, 'r', encoding='utf-8') as f:
            vault_content = f.read()
        
        if vault_content.startswith("---"):
            parts = vault_content.split("---", 2)
            yaml_block = f"---{parts[1]}---\n"
        else:
            yaml_block = "---\nfuente: scrivener\n---\n"
    else:
        # Es un archivo nuevo
        yaml_block = "---\nfuente: scrivener\n---\n"

    # 3. Fusionar y Guardar
    final_output = yaml_block + new_body
    
    # Asegurar que la carpeta destino exista
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_output)
    
    print(f"✅ Sincronización exitosa: {dest_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 _Scripts/scrivener_bridge.py <origen_scrivener> <destino_vault>")
    else:
        sync_scrivener(sys.argv[1], sys.argv[2])
