---
name: scrivener-bridge
description: "Detecta archivos nuevos o modificados en Inbox/scrivener-sync/ y los prepara para el pipeline de S1. Actívalo cuando Daniel diga 'revisa scrivener', 'hay algo nuevo de scrivener', o cuando detectes que hay archivos en Inbox/scrivener-sync/ que no han sido procesados."
---

# SCRIVENER-BRIDGE — Puente Scrivener → Obsidian

**Dirección única:** Scrivener → Obsidian. Nunca al revés sin acción manual de Daniel.

## PASO 1 — INSPECCIONAR CARPETA

Revisar `Inbox/scrivener-sync/` para archivos nuevos o modificados.

Para cada archivo encontrado, verificar:
- ¿Ya fue procesado? (buscar en `_Skills/PROCESS_LOG.md` si hay registro)
- ¿Cuándo fue modificado?
- ¿Qué tipo de archivo es? (.md, .txt, .docx)

Si la carpeta está vacía o todos los archivos ya fueron procesados: reportar a Daniel y detener.

## PASO 2 — REPORTE DE ARCHIVOS NUEVOS

```
── SCRIVENER SYNC ──────────────────────────────────────

Archivos nuevos detectados en Inbox/scrivener-sync/:

[N] archivos sin procesar:
  1. [nombre del archivo] — modificado: [fecha] — tipo: [extensión]
  2. ...

¿Proceso todos o seleccionas cuáles?
────────────────────────────────────────────────────────
```

Esperar confirmación de Daniel.

## PASO 3 — PREPARAR PARA PIPELINE

Para cada archivo aprobado por Daniel:

1. Copiar el archivo a `Inbox/` (no mover — mantener copia en scrivener-sync/)
2. Agregar al YAML del archivo copiado: `fuente: scrivener`
3. Agregar tag `source: scrivener` en el nombre o en el contenido si el formato lo permite

## PASO 4 — LLAMAR MODO-SELECTOR

Invocar `modo-selector` con cada archivo preparado.
El pipeline normal toma el control desde ahí.

## PASO 5 — REGISTRAR EN PROCESS_LOG

```
[YYYY-MM-DD] scrivener-bridge — [N] archivos transferidos desde scrivener-sync/ | [lista de nombres]
```

---

**Regla crítica:** La dirección Obsidian → Scrivener es SIEMPRE manual e intencional de Daniel.
Nunca sobreescribir o modificar archivos en `Inbox/scrivener-sync/`.
