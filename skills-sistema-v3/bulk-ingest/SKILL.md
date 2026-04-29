---
name: bulk-ingest
description: "Procesa lotes de 15-25 documentos desde Inbox/ con checkpoints agrupados. Preserva el control editorial pero elimina interrupciones repetitivas. Usar para la carga masiva de fuentes existentes."
---

# BULK-INGEST — Carga Masiva de Fuentes

**Principio:** El control editorial de Daniel no desaparece — se agrupa por lote.

---

## Cuándo usar

- Carga masiva de fuentes existentes (Fase 1 del vault)
- 5+ documentos pendientes en `Inbox/`
- Nunca para contenido nuevo del día (ese sigue el pipeline individual)

---

## Diferencias con el pipeline individual

| Paso | Pipeline individual | Bulk-ingest |
|---|---|---|
| inbox-triage F1 | OK por documento | Resumen de lote → OK de lote |
| inbox-triage F2 + mode skills | OK por documento | Auto-ejecuta sin pausa |
| zettelkasten-forge | OK por documento | Acumula buffer → revisión al final |
| pattern-harvester | OK por documento | Una vez al final del lote |

---

## Tamaño de lote recomendado

| Tipo de contenido | Modo | Lote máximo |
|---|---|---|
| Libros completos | 1–2 | 5 docs (generan 15-30 ZK cada uno) |
| Clases / predicaciones | 6 | 10-12 docs |
| Ideas sueltas / notas | 3, 5 | 20-25 docs |
| Notas de maestría | Académico | 8-10 docs |

**Regla de dominio:** Si el lote mezcla pastoral y académico, procesarlos en sublotes separados.

---

## Reglas de sesión (activas siempre)

1. **Caveman mode — full:** Activar `/caveman` al inicio de cada sesión antes de cualquier PASO. Si la sesión se reinicia o compacta, reactivar con `/caveman` inmediatamente.
2. **Compactar entre pasos:** Antes de avanzar al siguiente PASO, ejecutar `/compact` para limpiar el contexto. El prompt de compactación debe incluir: estado del lote, IDs ZK generados, patrones pendientes.
3. Si caveman no está activo al inicio → activarlo antes de responder.
4. Si el contexto supera 70% antes de un `/compact` programado → compactar de inmediato, sin esperar el checkpoint.

---

## PROTOCOLO

### PASO 0 — Inventario

Listar todos los archivos en `Inbox/` (excluir `scrivener-sync/`).

Presentar resumen al Daniel:

```
📦 LOTE PROPUESTO — [N] documentos
──────────────────────────────────
1. nombre-archivo.pdf → tipo detectado: libro / clase / paper...
2. otro-archivo.docx → tipo detectado: ...
...

¿Proceder con este lote completo, o ajustar el tamaño?
```

Esperar OK antes de continuar.

> **→ Al recibir OK:** ejecutar `/compact` antes de avanzar a PASO 1. Verificar caveman activo.

---

### PASO 1 — Triage rápido del lote

Para cada documento del lote, ejecutar `inbox-triage Fase 1` (auto, sin pausa).

Acumular resultados y presentar TODO el triage junto:

```
📋 TRIAGE DEL LOTE — [N] documentos
──────────────────────────────────────────────────────────────
Doc 1: "Nombre del archivo"
  → MODO 1 (Libro Terminado) | tema: 05_DoctrinasFundamentales
  → YAML clave: serie: "Orígenes", libro: Génesis

Doc 2: "Otro archivo"
  → MODO 6 (Clase Larga) | tema: 03_Escatologia—Destino
  → YAML clave: libro: Lucas, personajes: [Noé]

...
──────────────────────────────────────────────────────────────
¿Correcto? Señala cualquier discrepancia antes de continuar.
```

Esperar OK. Si hay correcciones, aplicarlas antes de avanzar.

> **→ Al recibir OK:** ejecutar `/compact` antes de avanzar a PASO 2. Verificar caveman activo.

---

### PASO 2 — Procesamiento automático

Una vez aprobado el triage del lote, procesar cada documento **sin pausas intermedias**:

Para cada documento (en orden):
1. `inbox-triage Fase 2` → crea contenedor en `Temas/`
2. Skills del modo detectado → procesa el contenido
3. `zettelkasten-forge` → genera propuestas ZK → **guardar en buffer interno** (NO crear archivos todavía)

Reportar progreso en tiempo real:
```
✓ [1/12] "Nombre" → procesado | 18 ZK propuestas acumuladas
✓ [2/12] "Otro"   → procesado | 26 ZK propuestas acumuladas
...
```

> **→ Al terminar PASO 2:** ejecutar `/compact` antes de presentar propuestas ZK. Verificar caveman activo.

---

### PASO 3 — Revisión de ZK del lote

Una vez procesados todos los documentos, presentar las propuestas ZK agrupadas por documento fuente:

```
📝 NOTAS ZK PROPUESTAS — [N] total
══════════════════════════════════════
FUENTE: "Nombre del libro" — 18 propuestas
──────────────────────────────────────
ZK-[ID]-001: "Título atómico"
  Idea: [una oración]
  Wikilinks: [[nota1]] [[nota2]]

ZK-[ID]-002: "Otro título"
  ...

══════════════════════════════════════
FUENTE: "Otra fuente" — 8 propuestas
...
```

Daniel puede:
- `OK todo` → aprobar todo el lote
- `OK fuente 1, rechazar fuente 3` → aprobar por grupos
- Señalar notas específicas para ajuste

Solo crear archivos tras OK explícito.

> **→ Al recibir OK:** crear archivos ZK, luego ejecutar `/compact` antes de avanzar a PASO 4. Verificar caveman activo.

---

### PASO 4 — pattern-harvester del lote

Correr `pattern-harvester` **una sola vez** con todas las notas ZK del lote como contexto.

Presentar propuestas de patrones según el formato estándar del harvester.

Daniel aprueba con OK granular (patrón por patrón).

> **→ Al recibir OK:** actualizar `activePatterns.json`, luego ejecutar `/compact` antes de avanzar a PASO 5. Verificar caveman activo.

---

### PASO 5 — PROCESS_LOG

Actualizar `_Skills/PROCESS_LOG.md` con entrada de batch:

```markdown
### YYYY-MM-DD — BULK-INGEST — Lote [N] — [N] documentos

**Documentos procesados:**
- Doc 1 (MODO 1) → ZK: 18
- Doc 2 (MODO 6) → ZK: 8
...

**Total ZK generadas:** N
**Patrones propuestos:** N | Aprobados: N
**Dominio:** pastoral | académico | mixto
```

> **→ Al terminar PASO 5:** lote cerrado. Si hay Lote 2, ejecutar `/compact` antes de iniciar PASO 0 del siguiente lote. Verificar caveman activo.

---

## Gestión de errores

- Si un documento falla el triage (tipo no detectado): pausar, avisar a Daniel, continuar con el siguiente.
- Si un documento no tiene contenido suficiente para ZK: registrar en el log con nota `sin_zk_suficiente`, continuar.
- Si el lote supera el 70% del contexto antes de terminar: cerrar el lote, guardar el estado en PROCESS_LOG, comenzar nuevo lote en la próxima sesión.

---

## Archivos que modifica

- `Temas/[tema]/[subcarpeta]/[archivo].md` (crea contenedores)
- `09_Zettelkasten/pastoral/` o `academico/` (crea notas ZK aprobadas)
- `_Skills/PROCESS_LOG.md` (entrada de batch)
- `_Skills/activePatterns.json` (solo si hay patrones aprobados)

## Archivos que solo lee

- `Inbox/` (documentos fuente)
- `ContextoMaestro/00_ESENCIAL.md`
- `_Skills/activePatterns.json`
