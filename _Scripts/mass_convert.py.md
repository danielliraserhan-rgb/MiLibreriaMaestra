import os
import shutil
from markitdown import MarkItDown
from datetime import datetime

def batch_convert(directory):
    # Inicializar MarkItDown
    md = MarkItDown()
    
    # Carpeta de respaldo para evitar desorden
    originals_dir = os.path.join(directory, "_Originales_Procesados")
    
    if not os.path.exists(originals_dir):
        os.makedirs(originals_dir)

    print(f"\n🚀 [BATCH-CONVERTER] Iniciando: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📂 Directorio: {directory}\n" + "-"*40)
    
    count_success = 0
    count_error = 0
    
    # Listar archivos omitiendo ocultos y carpetas de sistema
    files = [f for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f)) 
             and not f.startswith('.')]

    if not files:
        print("📭 El Inbox está vacío. Nada que convertir.")
        return

    for filename in files:
        filepath = os.path.join(directory, filename)
        name_part, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # Extensiones soportadas por MarkItDown
        if ext in ['.pdf', '.docx', '.pptx', '.xlsx', '.html', '.txt']:
            try:
                print(f"📦 Procesando: {filename}...", end="\r")
                result = md.convert(filepath)
                
                # Crear el nuevo archivo .md
                new_filename = f"{name_part}.md"
                new_filepath = os.path.join(directory, new_filename)
                
                # Guardar contenido
                with open(new_filepath, "w", encoding="utf-8") as f:
                    f.write(result.text_content)
                
                # Mover el original a la carpeta de respaldo
                shutil.move(filepath, os.path.join(originals_dir, filename))
                
                print(f"✅ Convertido: {filename} -> {new_filename}")
                count_success += 1
                
            except Exception as e:
                print(f"❌ Error en {filename}: {str(e)}")
                count_error += 1
        else:
            if ext != '.md':
                print(f"⚠️ Saltando (Extensión no soportada): {filename}")

    print("-"*40)
    print(f"✨ Finalizado. Éxitos: {count_success} | Errores: {count_error}")
    print(f"📂 Los originales están en: {originals_dir}\n")

if __name__ == "__main__":
    # Ajusta 'Inbox' si tu carpeta tiene una ruta distinta
    batch_convert("Inbox")