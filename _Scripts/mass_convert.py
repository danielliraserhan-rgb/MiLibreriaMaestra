import os
import shutil
from pathlib import Path
from markitdown import MarkItDown
from datetime import datetime

VAULT_ROOT = Path(__file__).parent.parent


def batch_convert(directory):
    md = MarkItDown()
    base_path = os.getcwd()
    target_dir = Path(os.path.join(base_path, directory)).resolve()
    if not target_dir.is_relative_to(VAULT_ROOT.resolve()):
        print(f"❌ Error: directorio fuera del vault ({directory})")
        return
    target_dir = str(target_dir)
    originals_dir = os.path.join(target_dir, "_Originales_Procesados")

    if not os.path.exists(target_dir):
        print(f"❌ Error: No se encuentra la carpeta '{directory}' en {base_path}")
        return

    if not os.path.exists(originals_dir):
        os.makedirs(originals_dir)

    print(f"\n🚀 [BATCH-CONVERTER] Iniciando: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📂 Directorio: {target_dir}\n" + "-"*40)
    
    count_success = 0
    count_error = 0
    
    files = [f for f in os.listdir(target_dir) 
             if os.path.isfile(os.path.join(target_dir, f)) 
             and not f.startswith('.')]

    for filename in files:
        filepath = os.path.join(target_dir, filename)
        name_part, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        if ext in ['.pdf', '.docx', '.pptx', '.xlsx', '.html', '.txt']:
            try:
                new_filename = f"{name_part}.md"
                new_filepath = os.path.join(target_dir, new_filename)

                if os.path.exists(new_filepath):
                    print(f"⚠️  Saltado (ya existe): {new_filename}")
                    count_error += 1
                    continue

                print(f"📦 Procesando: {filename}...")
                result = md.convert(filepath)

                with open(new_filepath, "w", encoding="utf-8") as f:
                    f.write(result.text_content)

                shutil.move(filepath, os.path.join(originals_dir, filename))
                count_success += 1
                print(f"✅ Convertido: {new_filename}")
            except Exception as e:
                print(f"❌ Error en {filename}: {str(e)}")
                count_error += 1
    
    print("-"*40)
    print(f"✨ Finalizado. Éxitos: {count_success} | Errores: {count_error}\n")

if __name__ == "__main__":
    batch_convert("Inbox")
