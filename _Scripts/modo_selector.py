import json
import os
import sys

def check_file(filepath):
    if not os.path.exists(filepath):
        print(json.dumps({"status": "error", "action": "ignorar"}))
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            primera_linea = f.readline().strip()

        # Si la primera línea es ---, asumimos que ya tiene YAML/fue procesado
        if primera_linea == '---':
            print(json.dumps({"status": "procesado", "action": "saltar"}))
        else:
            print(json.dumps({"status": "virgen", "action": "inbox-triage"}))

    except Exception as e:
        print(json.dumps({"status": "error", "action": "ignorar", "msg": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "action": "ignorar", "msg": "Falta ruta del archivo"}))
    else:
        check_file(sys.argv[1])
