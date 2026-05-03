import sys
import json
import os
from datetime import datetime
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent

def write_moc(tema, json_data_str):
    try:
        grupos = json.loads(json_data_str)
    except json.JSONDecodeError:
        print("❌ Error: JSON inválido proporcionado por Claude.")
        return

    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    
    contenido = f"""---
title: "MOC — {tema}"
date: {fecha_hoy}
dominio: mixto
tipo: MOC
tema: "{tema}"
tags: [moc]
---

# MOC — {tema}

> Mapa de contenido. Última actualización: {fecha_hoy}.

"""

    for grupo, notas in grupos.items():
        contenido += f"## {grupo}\n\n"
        for nota in notas:
            titulo_limpio = nota.replace("[[", "").replace("]]", "")
            contenido += f"- [[{titulo_limpio}]]\n"
        contenido += "\n"

    moc_dir = VAULT_ROOT / "MapasDeContenido—MOCs"
    moc_dir.mkdir(exist_ok=True)

    filepath = moc_dir / f"MOC — {tema}.md"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(contenido)

    print(f"✅ MOC escrito exitosamente en: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 _Scripts/write_moc.py <Tema> '<json_con_grupos>'")
    else:
        write_moc(sys.argv[1], sys.argv[2])
