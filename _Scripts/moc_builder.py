import os
import sys
from datetime import datetime

def build_moc(target_folder, moc_name):
    base_path = os.getcwd()
    folder_path = os.path.join(base_path, target_folder)
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: La carpeta {target_folder} no existe.")
        return

    moc_filepath = os.path.join(base_path, "MapasDeContenido-MOCs", f"{moc_name}.md")
    
    links = []
    # Escanear archivos recursivamente o en la carpeta base
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md') and file != f"{moc_name}.md":
                name_without_ext = os.path.splitext(file)[0]
                links.append(f"- [[{name_without_ext}]]")
    
    links.sort()
    
    moc_content = f"""---
title: "{moc_name}"
tipo: "moc"
fecha_actualizacion: "{datetime.now().strftime('%Y-%m-%d')}"
version_yaml: "2.0"
---
# 🗺️ MOC: {moc_name}
Generado automáticamente a partir de: `{target_folder}`

## Índice de Contenidos
""" + "\n".join(links)

    # Asegurar que la carpeta de MOCs exista
    os.makedirs(os.path.join(base_path, "MapasDeContenido-MOCs"), exist_ok=True)

    with open(moc_filepath, 'w', encoding='utf-8') as f:
        f.write(moc_content)
    
    print(f"🗺️ MOC generado exitosamente: {moc_filepath} con {len(links)} enlaces.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 _Scripts/moc_builder.py <carpeta_objetivo> <nombre_del_moc>")
        print("Ejemplo: python3 _Scripts/moc_builder.py Temas/05_DoctrinasFundamentales MOC_Doctrinas")
    else:
        build_moc(sys.argv[1], sys.argv[2])
