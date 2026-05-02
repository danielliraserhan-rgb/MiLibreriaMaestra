---
name: markdown-cleaner
description: "Limpieza RegEx de formato Markdown: normaliza headers, elimina saltos de línea excesivos, limpia espacios al final de línea. Delega 100% a Python — nunca reescribe el archivo manualmente. Actívalo cuando Daniel pida 'limpiar el formato visual' o arreglar espacios/títulos en un .md."
---

# MARKDOWN-CLEANER (Híbrido Python)

**Regla crítica:** NUNCA corrijas espacios o tabulaciones reescribiendo el archivo. Toda limpieza va por el script Python para garantizar precisión RegEx y preservar el YAML frontmatter intacto.

## LO QUE HACE EL SCRIPT

- Normaliza headers (asegura espacio tras `#`, ej. `##Título` → `## Título`)
- Elimina saltos de línea excesivos (3+ consecutivos → 2)
- Limpia espacios al final de cada línea
- Preserva el bloque YAML frontmatter sin modificarlo

## PASO 1 — CONFIRMAR RUTA

Verifica que el archivo `.md` existe en el vault y anota su ruta relativa desde la raíz del vault.

## PASO 2 — EJECUCIÓN (PYTHON)

TIENES PROHIBIDO editar el archivo directamente. Ejecuta:

```
python3 _Scripts/markdown_cleaner.py "<ruta/al/archivo.md>"
```

El script imprime `🧹 Formato adaptado con éxito: <ruta>` al terminar.

## PASO 3 — VERIFICACIÓN

Confirma a Daniel que la limpieza fue exitosa. Si el script reporta error (`❌`), informa la ruta o mensaje de error exacto y detente.
