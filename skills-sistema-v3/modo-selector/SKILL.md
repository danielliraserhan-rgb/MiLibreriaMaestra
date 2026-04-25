---
name: modo-selector
description: "Punto de entrada del sistema. Confirma activePatterns.json cargado y pasa a inbox-triage. Actívalo SIEMPRE que llegue un archivo nuevo para procesar. No enruta — la lógica de enrutamiento está en CLAUDE.md §4. Solo verifica que el contexto esté listo y llama a inbox-triage."
---

# MODO-SELECTOR — Punto de Entrada

**Único trabajo:** cargar contexto → llamar inbox-triage.

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

## PASO 3 — LLAMAR INBOX-TRIAGE

Invocar `inbox-triage` con el archivo recibido.

La lógica de enrutamiento de modos (1–7 + Académico) está en CLAUDE.md §4.
inbox-triage detecta el modo y propone el pipeline completo.

---

**Regla:** Nunca enrutar directamente a un skill secundario sin pasar por inbox-triage primero.
