---
name: scrivener-export
description: "Exporta archivos del vault de Obsidian hacia Scrivener. Genera copia limpia sin YAML, sin wiki links, sin tags inline. Actívalo cuando Claude Code haya terminado edits en un archivo que Daniel necesita continuar en Scrivener."
---

---
# SCRIVENER-EXPORT

**Dirección:** Obsidian → Scrivener. Solo exportación.
**Regla crítica:** Nunca exportar sin mostrar el diff preview a Daniel y recibir OK explícito.

## PASO 1 — IDENTIFICAR CANDIDATOS

1. Cargar `_Skills/scrivener-manifest.json`.
2. Listar archivos con `estado: pendiente_export` o `editado_en_vault_post_sync: true`.
3. Si Daniel especificó un archivo concreto, verificar que existe en el vault y que tiene `fuente: scrivener` en su YAML.

## PASO 2 — PREVIEW DEL DIFF LIMPIO

Ejecutar en modo preview para mostrar qué recibirá Scrivener **sin escribir el archivo**:

```
python3 _Scripts/scrivener_export.py "<ruta_vault>" --preview
```

El script reporta:
- Líneas del resultado
- Cantidad de wiki links convertidos a texto plano
- Cantidad de tags inline eliminados
- Ruta de destino en `Inbox/scrivener-sync/export/`

Presentar este reporte a Daniel antes de continuar.

## PASO 3 — ESPERAR OK EXPLÍCITO

Preguntar: *"¿Exporto esta versión limpia a `Inbox/scrivener-sync/export/[nombre.md]`?"*

No avanzar sin confirmación de Daniel.

## PASO 4 — EJECUTAR EXPORTACIÓN

```
python3 _Scripts/scrivener_export.py "<ruta_vault>" [nombre_salida.md]
```

El script:
1. Strip completo del YAML v2
2. `[[wiki links]]` → texto plano
3. `#tags` inline → eliminados
4. Escribe archivo limpio en `Inbox/scrivener-sync/export/`
5. Actualiza manifest: `ultima_export`, `estado → sincronizado`, `editado_en_vault_post_sync → false`

## PASO 5 — CONFIRMAR Y REGISTRAR

1. Confirmar que el archivo existe en `Inbox/scrivener-sync/export/`.
2. Registrar en `_Skills/PROCESS_LOG.md`:
   `[FECHA] SCRIVENER-EXPORT: [archivo_vault] → Inbox/scrivener-sync/export/[nombre.md] | estado: sincronizado`
