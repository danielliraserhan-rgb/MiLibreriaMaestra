---
name: scrivener-bridge
description: '"Sincroniza archivos desde Inbox/scrivener-sync/ hacia el vault protegiendo el YAML v2. Actívalo cuando haya ediciones nuevas en Scrivener."'
---

---
# SCRIVENER-BRIDGE (Híbrido)

**Regla crítica:** Dirección única Scrivener → Obsidian. Prohibido reescribir archivos manualmente; usa el script de Python para proteger los metadatos.

## PASO 1 — INSPECCIÓN
Lista los archivos en `Inbox/scrivener-sync/` y compáralos con los existentes en el vault para identificar cuáles han sido modificados.

## PASO 2 — REPORTE
Presenta a Daniel la lista de archivos detectados y pregunta: 
*"¿Sincronizo estos cambios al Vault protegiendo el YAML existente?"*

## PASO 3 — EJECUCIÓN (PYTHON)
Por cada archivo aprobado, TIENES PROHIBIDO copiar y pegar el texto tú mismo. Debes ejecutar el comando de terminal:

`python3 _Scripts/scrivener_bridge.py "Inbox/scrivener-sync/[archivo.md]" "[Ruta/en/el/Vault/archivo.md]"`

## PASO 4 — FINALIZACIÓN
1. Si el archivo es nuevo en el Vault, invoca a `modo-selector`.
2. Registra la acción en `_Skills/PROCESS_LOG.md`.