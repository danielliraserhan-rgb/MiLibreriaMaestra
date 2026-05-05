---
name: modo-selector
description: Punto de entrada del sistema y cadenero híbrido. Utiliza Python para verificar si un archivo ya fue procesado antes de gastar tokens leyendo su contenido o cargando el contexto maestro. Si el archivo es nuevo, verifica el formato, carga el contexto y deriva a inbox-triage."
---
---
# MODO-SELECTOR — Punto de Entrada Híbrido

**Único trabajo:** Consultar al script de Python → saltar si ya está procesado → si es virgen, verificar formato, cargar contexto y llamar a inbox-triage.

## PASO 1 — EL CADENERO (PYTHON)

Antes de leer el archivo o cargar contextos pesados, TIENES OBLIGATORIAMENTE que consultar el estado del archivo usando la terminal.

Ejecuta este comando exacto:
`python3 _Scripts/modo_selector.py "<ruta_del_archivo>"`

Analiza la respuesta JSON de la terminal:
- Si la respuesta es `"action": "saltar"`: El archivo ya tiene YAML o ya fue procesado. **DETENTE AQUÍ**. Ignora el archivo por completo y pasa al siguiente (si es carga masiva) o avisa a Daniel. No gastes tokens cargando contexto.
- Si la respuesta es `"action": "inbox-triage"`: El archivo es virgen y requiere atención. **CONTINÚA AL PASO 2**.

## PASO 2 — VERIFICAR FORMATO DEL ARCHIVO

Inspeccionar la extensión del archivo recibido:
- **Si ya es `.md`:** continuar directamente al PASO 3.
- **Si NO es `.md`** (PDF, DOCX, PPTX, TXT, etc.): **Detente**. Indica a Daniel que los archivos no-markdown deben pre-procesarse primero ejecutando `python3 _Scripts/mass_convert.py` para limpiar el Inbox antes del triaje. (Si estás en medio de un `bulk-ingest` autorizado, puedes ejecutar el conversor masivo tú mismo antes de continuar).

## PASO 3 — CARGAR CONTEXTO MAESTRO (Solo para archivos vírgenes)

Ahora que confirmaste que el archivo es `.md` y no ha sido procesado, prepara tu memoria para el análisis:
1. Lee `_Skills/activePatterns.json` (confirma internamente patrones y scopes).
2. Confirma que tienes acceso a `ContextoMaestro/00_ESENCIAL.md` (siempre) y `ContextoMaestro/04_voz.md` (solo si la tarea es pastoral).

No generes reportes de este paso a menos que falte un archivo crítico.

## PASO 4 — LLAMAR INBOX-TRIAGE

Transfiere el control invocando el skill `inbox-triage` pasándole el archivo validado.

---

## §Límite de Rol — Catalogación Únicamente

**Este skill enruta hacia skills de catalogación exclusivamente.**

PROHIBIDO:
- Derivar a `writing-coach`, `voice-trainer` o cualquier skill de coaching
- Mencionar análisis de escritura, S2, o voz de Daniel
- Sugerir coaching como paso siguiente al triage

Después de `inbox-triage`: el flujo continúa con los skills del MODO (modo-ab, modo-c, modo-e, etc.) → `zettelkasten-forge` → `pattern-harvester`. El coaching es una fase independiente que Daniel activa por separado.