#!/usr/bin/env python3
"""
scan_vault.py — MiLibreriaMaestra
Modos:
  --mode gaps   : temas con baja cobertura ZK
  --mode index  : regenera _Skills/VAULT_INDEX.md
"""
import re
import sys
from pathlib import Path
from datetime import datetime

VAULT = Path(__file__).parent.parent
ZK_PASTORAL = VAULT / "09_Zettelkasten" / "pastoral"
ZK_ACADEMICO = VAULT / "09_Zettelkasten" / "academico"
TEMAS = VAULT / "Temas"
VAULT_INDEX = VAULT / "_Skills" / "VAULT_INDEX.md"


def _zk_refs_in_file(path: Path) -> int:
    try:
        return len(re.findall(r'ZK-\d{8}-\d{4}-\d{3}', path.read_text(encoding='utf-8')))
    except Exception:
        return 0


def scan_gaps():
    tema_dirs = sorted([d for d in TEMAS.iterdir() if d.is_dir() and not d.name.startswith('.')])
    print("## GAPS DE COBERTURA ZK\n")
    for tema in tema_dirs:
        md_files = list(tema.rglob("*.md"))
        zk_refs = sum(_zk_refs_in_file(f) for f in md_files)
        if len(md_files) == 0:
            continue
        status = "⚠️ GAP" if zk_refs == 0 else ("🟡 BAJO" if zk_refs < 3 else "✅ OK")
        print(f"{status} | {tema.name} | archivos: {len(md_files)} | ZK refs: {zk_refs}")


def regenerate_index():
    tema_dirs = sorted([d for d in TEMAS.iterdir() if d.is_dir() and not d.name.startswith('.')])
    fecha = datetime.now().strftime('%Y-%m-%d')

    zk_p = len(list(ZK_PASTORAL.glob("*.md"))) if ZK_PASTORAL.exists() else 0
    zk_a = len(list(ZK_ACADEMICO.glob("*.md"))) if ZK_ACADEMICO.exists() else 0

    lines = [
        f"# VAULT INDEX — {fecha}",
        "",
        f"**ZK Pastoral:** {zk_p} notas | **ZK Académico:** {zk_a} notas",
        "",
        "## Cobertura por Tema",
        "",
    ]

    for tema in tema_dirs:
        md_files = list(tema.rglob("*.md"))
        v2 = sum(1 for f in md_files if 'version_yaml: "2.0"' in f.read_text(encoding='utf-8', errors='ignore'))
        lines.append(f"- **{tema.name}**: {len(md_files)} archivos ({v2} con YAML v2)")

    VAULT_INDEX.write_text("\n".join(lines) + "\n", encoding='utf-8')
    print(f"✅ VAULT_INDEX regenerado: {VAULT_INDEX}")


if __name__ == "__main__":
    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        mode = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        if mode == "gaps":
            scan_gaps()
        elif mode == "index":
            regenerate_index()
        else:
            print(f"❌ Modo desconocido: {mode}. Usa --mode gaps o --mode index")
    else:
        print("Uso: python3 _Scripts/scan_vault.py --mode [gaps|index]")
