# SkillsMap.md — Mapa de Skills y Scripts

> Referencia completa de todos los skills y scripts del sistema. Carga este archivo al ejecutar cualquier skill o script.

---

## Regla de Oro

**Claude tiene estrictamente prohibido usar `cat`, `echo >>`, `sed`, `awk` o cualquier terminal para modificar archivos Markdown.** Toda modificación estructural pasa por `_Scripts/`. Toda creación o edición de `.md` pasa por el skill `obsidian-markdown`.

---

## Scripts Python — Comandos Completos

Todos los scripts se ejecutan desde la raíz del vault. Usan `Path(__file__).parent.parent` para resolver rutas — no requieren `cd`.

| Script | Comando completo |
|---|---|
| **modo_selector** | `python3 _Scripts/modo_selector.py "Inbox/archivo.md"` → devuelve JSON `{status, action}` |
| **inbox_triage** | `python3 _Scripts/inbox_triage.py "Inbox/archivo.md" '{"tipo":"X","tema":"01_Origenes","dominio":"pastoral","modo":"1","destino":"Temas/01_Origenes/01_Libros/"}'` |
| **write_moc** | `python3 _Scripts/write_moc.py "Tema" '{"Grupo1":["[[Nota A]]","[[Nota B]]"]}'` |
| **scan_vault (gaps)** | `python3 _Scripts/scan_vault.py --mode gaps` |
| **scan_vault (index)** | `python3 _Scripts/scan_vault.py --mode index` |
| **markdown_cleaner** | `python3 _Scripts/markdown_cleaner.py "Temas/01_Origenes/archivo.md"` |
| **mass_convert** | `python3 _Scripts/mass_convert.py "Inbox"` — convierte PDF/DOCX en el directorio dado; mueve originales a `_Originales_Procesados/` |
| **scrivener_bridge** | `python3 _Scripts/scrivener_bridge.py "Inbox/scrivener-sync/archivo.md" "Temas/.../destino.md"` |
| **scrivener_export** | `python3 _Scripts/scrivener_export.py "Temas/.../archivo.md" [nombre_salida.md] [--preview]` |
| **semantic_indexer** | `python3 _Scripts/semantic_indexer.py --mode index` · `--mode update` · `--mode query --q "texto"` |
| **bridge_linker** | `python3 _Scripts/bridge_linker.py --mode scan` · `--mode propose` · `--mode inject --confirm` |
| **apple_notes_bridge** | `python3 _Scripts/apple_notes_bridge.py --mode sync` · `--mode status` · `--mode clean` *(requiere MCP `mcp__Read_and_Write_Apple_Notes__`)* |
| **zk_rename** | `python3 _Scripts/zk_rename.py` — renombra todas las notas ZK en `09_Zettelkasten/pastoral/` y actualiza wikilinks en el vault |
| **zk_fix_title_field** | `python3 _Scripts/zk_fix_title_field.py` — corrige campo `title` → `titulo` en notas ZK |

### Pipeline Semántico (Módulos 1–3)

| Script | Función | Dependencias externas |
|---|---|---|
| `semantic_indexer.py` | Índice ChromaDB para notas ZK. `--mode index\|update\|query --q "..."` | `frontmatter`, `chromadb`, `sentence_transformers` |
| `bridge_linker.py` | Vincula archivos Inbox con notas ZK existentes (3 tiers: keywords, versículos, semántico). `--mode scan\|propose\|inject --confirm` | — |
| `apple_notes_bridge.py` | Sincroniza Apple Notes (carpeta "MiLibreria — Inbox") → `Inbox/`. `--mode sync\|status\|clean` | MCP `mcp__Read_and_Write_Apple_Notes__` activo |

**Instalar dependencias** (Python 3.11+; si no están disponibles, los módulos 1–3 y `mass_convert.py` fallarán con `ModuleNotFoundError`):
```bash
pip install -r requirements.txt
```

---

## Skills — Tabla de Enrutamiento por Situación

| Situación | Skill |
|---|---|
| Nuevo archivo en inbox | `modo-selector` |
| **5+ archivos en inbox (carga masiva)** | `bulk-ingest` |
| **Convertir PDF/DOCX/PPTX/XLSX a .md antes del triage** | `conversion-documentos` |
| Diagnóstico de tipo y generación de JSON payload para inyección YAML vía Python | `inbox-triage` |
| Texto pastoral: oral + escrito, o borrador | `modo-ab-seccion-mixta` |
| Diagnóstico / mapa estructural | `modo-c-esquema-editorial` |
| Hueco estructural, material de referencia | `modo-r-material-referencia` |
| Esquema para clase / enseñanza | `modo-e-unificado` |
| Lectura académica / nota de maestría | `notas-maestria` |
| Generar notas atómicas Zettelkasten | `zettelkasten-forge` |
| Detectar y proponer patrones | `pattern-harvester` |
| Mapa de contenido (índice de notas) | `moc-builder` |
| **Huecos estructurales** (preguntas abiertas, patrones débiles, huérfanas) | `desarrollador-de-temas` |
| **Cobertura cuantitativa de temas** (temas mencionados con pocas notas ZK) | script: `scan_vault.py --mode gaps` |
| **Análisis de voz + teología (S2)** | `writing-coach` |
| **Espejo de voz vs patrones aprobados** | `voice-trainer` |
| **Guía de formato por tipo de contenido** | `format-adapter` |
| **Sincronizar Apple Notes → Inbox/** | script: `apple_notes_bridge.py --mode sync` |
| **Vincular archivos Inbox con notas ZK existentes** | script: `bridge_linker.py --mode propose` |
| **Detectar archivo nuevo desde Scrivener** | `scrivener-bridge` |
| **Exportar archivo del vault hacia Scrivener** | `scrivener-export` |
| **Limpiar formato visual RegEx** | `markdown-cleaner` |
| **Crear/editar Obsidian Flavored Markdown** (wikilinks, callouts, embeds) | `obsidian-markdown` |
| **Crear/editar Obsidian Bases** (.base — vistas, filtros, fórmulas) | `obsidian-bases` |
| **Crear/editar JSON Canvas** (.canvas — diagramas de nodos) | `json-canvas` |
| **Revisión espaciada de notas ZK vencidas** | `spaced-review` |

---

## Reglas Especiales por Skill

### scrivener-bridge
Cuando detectes cambios en `Inbox/scrivener-sync/`, lista los archivos pero **NO fusiones los textos manualmente**. Ejecuta siempre:
```bash
python3 _Scripts/scrivener_bridge.py "<origen>" "<destino>"
```
Preserva el YAML v2 del vault.

### scrivener-export
Cuando Claude Code termine edits en un archivo con `fuente: scrivener` y Daniel necesite continuar en Scrivener. Ejecuta siempre:
```bash
python3 _Scripts/scrivener_export.py "<ruta_vault>" [nombre_salida.md] [--preview]
```
El archivo limpio queda en `Inbox/scrivener-sync/export/`.

### moc-builder
Escanea con `scan_vault.py`, agrupa con criterio editorial, y **TIENES PROHIBIDO escribir el archivo final en el vault**. Para guardar, compila un JSON y ejecuta:
```bash
python3 _Scripts/write_moc.py "<Tema>" '<json_payload>'
```

### markdown-cleaner
**NUNCA** intentes corregir espacios o tabulaciones reescribiendo el archivo. Si Daniel pide "limpiar el formato visual", ejecuta:
```bash
python3 _Scripts/markdown_cleaner.py "<ruta_del_archivo>"
```
