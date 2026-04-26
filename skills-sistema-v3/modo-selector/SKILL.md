---
name: modo-selector
description: "Punto de entrada del sistema. Confirma activePatterns.json cargado, convierte el archivo a .md si no lo es, y pasa a inbox-triage. Actívalo SIEMPRE que llegue un archivo nuevo para procesar. No enruta — la lógica de enrutamiento está en CLAUDE.md §4. Solo verifica que el contexto esté listo y llama a inbox-triage."
---

# MODO-SELECTOR — Punto de Entrada

**Único trabajo:** cargar contexto → convertir si no es .md → llamar inbox-triage.

## PASO 1 — CARGAR ACTIVEPATTERNS

Leer `_Skills/activePatterns.json`.

- Si existe: confirmar internamente cuántos patrones activos hay y sus scopes (pastoral / academico).
- Si no existe o está vacío: continuar normalmente.
- No reportar este paso a Daniel a menos que haya un error de lectura.

## PASO 2 — VERIFICAR CONTEXTO

Confirmar que estos archivos son accesibles (leer solo si no están ya en contexto):
- `ContextoMaestro/00_ESENCIAL.md` — siempre
- `ContextoMaestro/04_voz.md` — solo si la tarea es pastoral o de coaching

Si alguno falta, avisar a Daniel antes de continuar.

## PASO 2.5 — VERIFICAR FORMATO DEL ARCHIVO

Inspeccionar la extensión del archivo recibido:

- **Si ya es `.md`:** continuar directamente al PASO 3. No hacer nada extra.
- **Si NO es `.md`** (PDF, DOCX, PPTX, TXT, RTF, HTML, etc.): invocar `conversion-documentos` con el path del archivo antes de continuar. `conversion-documentos` se encarga de convertir a `.md` y luego llama a `inbox-triage` directamente. **Detener aquí** — el flujo continúa desde dentro de `conversion-documentos`.

## PASO 3 — LLAMAR INBOX-TRIAGE

(Solo si el archivo ya era `.md` desde el inicio.)

Invocar `inbox-triage` con el archivo recibido.

La lógica de enrutamiento de modos (1–7 + Académico) está en CLAUDE.md §4.
inbox-triage detecta el modo y propone el pipeline completo.

---

**Regla:** Nunca enrutar directamente a un skill secundario sin pasar por inbox-triage primero.
**Regla:** Si el archivo no era `.md`, la conversión ocurre ANTES del triage. `conversion-documentos` es el puente obligatorio.
