---
name: conversion-documentos
description: "Convierte archivos no-markdown (PDF, DOCX, PPTX, etc.) a .md usando MarkItDown antes de entrar al flujo editorial. Llamar desde modo-selector cuando el archivo no sea .md."
---

# CONVERSION-DOCUMENTOS — Conversión con MarkItDown

**Único trabajo:** convertir el archivo a `.md` → entregar el `.md` a `inbox-triage`.

## PASO 1 — VERIFICAR EXTENSIÓN

Recibir el path del archivo original. Extraer la extensión.

- Si ya es `.md`: **no hacer nada** — retornar el path original para que `modo-selector` continúe el flujo normal con `inbox-triage`.
- Si es `.pdf`, `.docx`, `.pptx`, `.txt`, `.rtf`, `.html` u otro formato soportado por MarkItDown: continuar al PASO 2.
- Si la extensión no es reconocida: avisar a Daniel y detener.

## PASO 2 — CONSTRUIR NOMBRE DE SALIDA

El archivo de salida `.md` tendrá el mismo nombre base que el original, con extensión `.md`, en el mismo directorio.

Ejemplo: `Inbox/Carta-de-Pablo.docx` → `Inbox/Carta-de-Pablo.md`

## PASO 3 — EJECUTAR MARKITDOWN

Ejecutar via Bash:

```bash
markitdown "RUTA_ARCHIVO_ORIGINAL" > "RUTA_ARCHIVO_MD"
```

- Usar paths absolutos o relativos desde la raíz del vault.
- Si `markitdown` no está instalado: avisar a Daniel con instrucción de instalación:
  ```
  pip install markitdown
  ```
  Detener hasta que Daniel confirme instalación.

## PASO 4 — VERIFICAR RESULTADO

Leer las primeras líneas del `.md` generado para confirmar que tiene contenido real (no vacío, no error de parseo).

- Si el archivo está vacío o contiene solo error: avisar a Daniel y detener.
- Si tiene contenido: continuar al PASO 5.

## PASO 5 — INFORMAR Y PASAR A INBOX-TRIAGE

Reportar a Daniel:

```
Conversión completada:
  Original : [nombre-archivo.ext]
  Generado : [nombre-archivo.md]
  Tamaño   : ~X palabras / Y líneas

Pasando a inbox-triage para diagnóstico...
```

Invocar `inbox-triage` con el path del `.md` generado.

---

**Regla:** Este skill solo convierte. No edita el contenido del archivo. No agrega YAML. No toma decisiones editoriales. Todo eso es trabajo de `inbox-triage` y los skills posteriores.
