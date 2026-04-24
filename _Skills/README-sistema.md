# README — Sistema de Catalogación Inteligente con Zettelkasten

**Proyecto:** MiLibreriaMaestra — Daniel Lira
**Versión:** 2.0
**Fecha de implementación:** 2026-04-23

---

## ¿Qué es este sistema?

Un sistema de dos fases para gestionar el conocimiento pastoral y teológico de Daniel Lira:

**FASE 1 (Catalogación):** Procesar todos los archivos existentes con:
- YAML frontmatter v2 unificado
- Notas atómicas Zettelkasten derivadas
- Retroalimentación continua que mejora el sistema

**FASE 2 (Generación):** Una vez catalogado todo, procesar contenido nuevo con el sistema refinado.

---

## Cómo usar el sistema

### Para procesar un archivo nuevo:

1. Coloca el archivo en `Inbox/`
2. Activa el skill `modo-selector`:
   ```
   TIPO: [descríbelo brevemente, ej: "clase sobre Génesis", "capítulo de libro"]
   [pega el contenido o di la ruta]
   ```
3. `modo-selector` orquesta todo. Sólo responde con SÍ/NO en cada checkpoint.

### Para explorar el segundo cerebro:

- `moc-builder` — construye índices navegables de temas
- `09_Zettelkasten/_indice/` — índices por tipo y tema
- Obsidian Graph View — visualiza las conexiones entre notas ZK

---

## Archivos del sistema

| Archivo | Función |
|---|---|
| `_Skills/activePatterns.json` | Patrones aprobados — crece con cada archivo |
| `_Skills/PROCESS_LOG.md` | Bitácora de archivos procesados |
| `_Skills/mapeo-modos-skills.md` | Referencia rápida modo→skills |
| `ContextoMaestro/ContextoMaestro.md` | Voz, teología, líneas rojas |
| `Templates/YAML-pastoral.md` | Template para notas pastorales |
| `Templates/YAML-academico.md` | Template para notas académicas |
| `Templates/YAML-zettelkasten.md` | Template para notas atómicas |

---

## Skills disponibles

| Skill | Activa cuando... |
|---|---|
| `modo-selector` | Siempre — punto de entrada obligatorio |
| `inbox-triage` | Automático (invocado por modo-selector) |
| `zettelkasten-forge` | Automático — propone notas atómicas al cerrar cada modo |
| `pattern-harvester` | Automático — detecta patrones al cerrar cada archivo |
| `modo-ab-seccion-mixta` | Material oral + escrito o borrador (MODOs 2, 6) |
| `modo-c-esquema-editorial` | Diagnóstico estructural (MODOs 1, 2, 5) |
| `modo-e-unificado` | Esquemas de enseñanza (MODOs 4, 6, 7) |
| `modo-r-material-referencia` | Cuando hay hueco en el argumento (MODO 2) |
| `notas-maestria` | Material académico de maestría |
| `moc-builder` | Manualmente — cuando quieres un mapa de un tema |

---

## Motor oficial de escritura — obsidian-markdown

A partir de 2026-04-24, **toda creación o edición de archivos `.md` en el vault usa `obsidian-markdown`** (kepano/obsidian-skills), que se activa en los pasos 2.e y 2.f del ciclo por archivo (escritura de ZK aprobadas y actualización del YAML fuente).

### Reglas de escritura (obligatorias)

| Regla | Detalle |
|---|---|
| **Usar `obsidian-markdown` siempre** | Para crear o editar cualquier `.md` en Modos 1–7 y Académico tras aprobación de Daniel |
| **Prohibido: terminal** | `cat`, `echo`, `sed`, `awk` y similares NO pueden usarse para escribir archivos Markdown |
| **YAML v2 vía `obsidian-markdown`** | La inyección del frontmatter usa el motor para garantizar formato perfecto sin escapes manuales |
| **Wikilinks obligatorios** | Los campos `source_file`, `notas_relacionadas` y la sección "Conexiones" usan `[[Nombre]]` — `obsidian-markdown` los genera nativamente |
| **Callouts nativos** | Las ideas centrales se resaltan con callouts de Obsidian (`> [!note]`, `> [!important]`, etc.) mediante `obsidian-markdown` |

### Cuándo se activa en el flujo

```
Ciclo por archivo (§6 del plan):
  2.e — zettelkasten-forge propone notas → Daniel aprueba
        → obsidian-markdown CREA los archivos ZK en 09_Zettelkasten/
  2.f — actualizar zettelkasten_notes en YAML del archivo fuente
        → obsidian-markdown EDITA el frontmatter del archivo fuente
```

`obsidian-markdown` también se usa al crear contenedores en `inbox-triage` Fase 2 si el archivo de destino es nuevo.

---

## Reglas no negociables

1. Nunca aplicar voz pastoral a material académico (`08_Academico/Maestria/`)
2. Nunca generar notas Zettelkasten que no sean autocontenidas
3. Nunca escribir en `activePatterns.json` sin aprobación explícita de Daniel
4. Nunca cortar, resumir ni tomar decisiones de contenido en transcripciones orales (§11 Contexto Maestro)
5. Nunca inventar teología — si hay hueco, señalar y preguntar
6. **Nunca usar comandos de terminal para escribir archivos `.md` — usar `obsidian-markdown` siempre**

---

## Sincronización del Contexto Maestro

El Contexto Maestro canónico vive en dos lugares:
- **Vault:** `ContextoMaestro/ContextoMaestro.md` (usado por los skills)
- **Desktop:** `~/Desktop/Claude/Contexto Maestro — Daniel Lira.md` (source of truth editable)

Cuando Daniel actualice el Contexto Maestro, copiar manualmente:
```bash
cp ~/Desktop/Claude/"Contexto Maestro — Daniel Lira.md" \
   ~/Desktop/MiLibreriaMaestra—DanielLira/ContextoMaestro/ContextoMaestro.md
```
