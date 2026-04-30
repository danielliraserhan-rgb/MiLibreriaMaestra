import os
import sys

def sync_scrivener_to_vault(scrivener_file, vault_file):
    if not os.path.exists(scrivener_file):
        print(f"❌ Error: Archivo de Scrivener no encontrado ({scrivener_file})")
        return
    
    # Leer el texto actualizado de Scrivener
    with open(scrivener_file, 'r', encoding='utf-8') as f:
        scrivener_content = f.read()

    # Si el archivo en el Vault no existe, lo creamos directamente
    if not os.path.exists(vault_file):
        with open(vault_file, 'w', encoding='utf-8') as f:
            f.write(scrivener_content)
        print(f"✅ Archivo copiado al Vault (Nuevo): {vault_file}")
        return

    # Si ya existe en el Vault, extraemos su YAML y lo inyectamos al texto de Scrivener
    with open(vault_file, 'r', encoding='utf-8') as f:
        vault_content = f.read()

    parts = vault_content.split("---", 2)
    
    if len(parts) >= 3 and vault_content.startswith("---"):
        yaml_block = f"---{parts[1]}---\n"
        # Limpiar cualquier YAML que Scrivener haya intentado exportar
        scriv_parts = scrivener_content.split("---", 2)
        if len(scriv_parts) >= 3 and scrivener_content.startswith("---"):
            pure_text = scriv_parts[2].lstrip()
        else:
            pure_text = scrivener_content.lstrip()
            
        final_content = yaml_block + pure_text
    else:
        # Si no había YAML en el Vault, solo sobrescribimos
        final_content = scrivener_content

    with open(vault_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"🔄 Sincronización Scrivener -> Vault exitosa: {vault_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 _Scripts/scrivener_bridge.py <archivo_scrivener> <archivo_vault>")
    else:
        sync_scrivener_to_vault(sys.argv[1], sys.argv[2])
