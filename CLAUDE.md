# CLAUDE.md — MiLibreriaMaestra

> Las 5 marcas de voz, marcos teológicos, líneas rojas, checklist de 11 puntos
> y descripción de modos (A, B, C, R, E) están en el Contexto Maestro.
> Ruta canónica: `ContextoMaestro/ContextoMaestro.md`
> Este archivo cubre solo arquitectura operativa.

---

## Estructura del Vault

**Dominio pastoral** — `Temas/01–07`:
`01_Origenes` · `02_HistoriaDeIsrael` · `03_Escatologia—Destino` · `04_ExegesisNT`
`05_DoctrinasFundamentales` · `06_DiscipuladoVidaCristiana` · `07_PredicacionesDevocionales`

Cada tema contiene: `01_Libros` / `02_EsquemasDeClase` / `03_ClasesEnVivo` / `04_NotasSinProcesar` / `05_MaterialExterno`

**Dominio académico** — `Temas/08_Academico/Maestria`:
`01_ArtículosAcadémicos` / `02_CasosDeEstudio` / `03_ForosDePreguntas` / `04_Exámenes` / `05_NotasDeClasePorMi` / `06_NotasDeClasePorElProfesor`

**Sistema**:
`Inbox/` · `Templates/` · `ContextoMaestro/` · `MapasDeContenido—MOCs/` · `_Skills/` · `Assets/`

**Segundo cerebro (Zettelkasten)**:
`09_Zettelkasten/pastoral/` · `09_Zettelkasten/academico/` · `09_Zettelkasten/_indice/`

> `ClasesPorSemestre/` — fuera del alcance del sistema. No procesar.

---

## Flujo de Entrada — Sistema completo

**Punto de entrada siempre:** `modo-selector` (lee `_Skills/activePatterns.json`, orquesta todo)

```
Daniel trae archivo → Inbox/
↓
modo-selector:
  1. Lee _Skills/activePatterns.json
  2. inbox-triage Fase 1 → detecta MODO (1-7) + YAML → reporte → espera OK
  3. inbox-triage Fase 2 → crea contenedor
  4. Ejecuta skills del MODO (ver tabla §Modos)
  5. zettelkasten-forge → propone N notas atómicas → espera OK
  6. Guarda ZK aprobadas → actualiza zettelkasten_notes en YAML
  7. pattern-harvester → propone patrones → espera OK granular
  8. Si aprueba: actualiza _Skills/activePatterns.json + _Skills/PROCESS_LOG.md
```

**Regla de oro:** `inbox-triage` siempre primero. `pattern-harvester` siempre último. `zettelkasten-forge` siempre antes del harvester. Nunca avanzar sin OK explícito de Daniel.

---

## Los 7 Modos — Tipología de archivos

| Modo | Tipo | Descripción | Skills en orden |
|---|---|---|---|
| **1** | Libro Terminado | Completo, va directo a catalogar | `inbox-triage` → `modo-c`(opcional) → `zettelkasten-forge` → `pattern-harvester` |
| **2** | Libro Pre-Diseño | Necesita edición bloque a bloque | `inbox-triage` → `modo-c` → `modo-ab` → `modo-r`(si hueco) → `zettelkasten-forge` → `pattern-harvester` |
| **3** | Ideas Sueltas | Sin estructura, solo mapear | `inbox-triage` → `zettelkasten-forge` → `pattern-harvester` |
| **4** | Guía de Estudio | Exegética versículo a versículo | `inbox-triage` → `modo-e`(bíblica) → `zettelkasten-forge` → `pattern-harvester` |
| **5** | Nota Temática | Resuelve un tema, referencia permanente | `inbox-triage` → `modo-c`(opcional) → `zettelkasten-forge` → `pattern-harvester` |
| **6** | Estudio / Clase Larga | Clase 1–3 h, notas para Daniel + estudiantes | `inbox-triage` → `modo-e` → `modo-ab`(si transcripción) → `zettelkasten-forge` → `pattern-harvester` |
| **7** | Grupos Conexión | ~15 min, para OTRA PERSONA facilite | `inbox-triage` → `modo-e`(temática) → `zettelkasten-forge` → `pattern-harvester` |
| — | Académico | Material maestría, régimen neutral | `inbox-triage` → `notas-maestria` → `zettelkasten-forge`(neutral) → `pattern-harvester` |

**Output Zettelkasten por modo:**
`Modo 1:` 15–30 notas · `Modo 2:` 10–25 · `Modo 3:` 5–10 · `Modo 4:` 10–20 · `Modo 5:` 5–10 · `Modo 6:` 8–15 · `Modo 7:` 3–5

---

## Plantilla YAML v2

```yaml
---
# === Bloque canónico v1 (no renombrar nunca) ===
title: ""
tipo: ""            # libro | esquema | clase_en_vivo | notas_sin_procesar | material_externo | articulo_academico
tema: ""            # 01_Origenes | 02_HistoriaDeIsrael | 03_Escatologia—Destino | 04_ExegesisNT |
                    # 05_DoctrinasFundamentales | 06_DiscipuladoVidaCristiana | 07_PredicacionesDevocionales | 08_Academico
libro_biblico_principal: ""
personajes: []
versiculos_citados: []
temas_principales: []
seo_keywords: []
fecha: ""
estado: ""          # sin_procesar | en_proceso | completado

# === Extensión v2 (campos nuevos — no reemplaza los de arriba) ===
dominio: ""         # pastoral | academico
modo: ""            # 1-libro-terminado | 2-libro-pre-diseno | 3-ideas-sueltas |
                    # 4-guia-estudio | 5-nota-tematica | 6-estudio-clase |
                    # 7-grupos-conexion | academico
fase: ""            # (solo MODO 2) pre-diseno | en-diseno | disenado
serie: ""
fuente: ""          # dictado | grabacion | borrador | clase | conferencia | paper
author_quotes: []   # autores/teólogos citados (Wright, Keller, Walton…)
zettelkasten_notes: []  # IDs de notas atómicas generadas desde este archivo (ZK-YYYYMMDD-HHMM-NNN)
version_yaml: "2.0"
fecha_actualizacion: ""
---
```

**Regla de coexistencia:** Notas con YAML v1 siguen siendo válidas. Al pasar por el sistema se hace upgrade automático (campos nuevos con `""` o `[]`). Los campos v1 NUNCA se renombran.

---

## Mapa de Skills

| Situación | Skill |
|---|---|
| Nuevo archivo en inbox (punto de entrada siempre) | `modo-selector` |
| Diagnóstico de tipo + YAML | `inbox-triage` |
| Texto pastoral: oral + escrito, o borrador limpio | `modo-ab-seccion-mixta` |
| Diagnóstico / mapa estructural | `modo-c-esquema-editorial` |
| Hueco estructural, buscar material de referencia | `modo-r-material-referencia` |
| Esquema para clase / enseñanza | `modo-e-unificado` |
| Lectura académica / nota de maestría | `notas-maestria` |
| Generar notas atómicas Zettelkasten | `zettelkasten-forge` |
| Detectar y proponer patrones de voz/estructura | `pattern-harvester` |
| Mapa de contenido (índice de notas existentes) | `moc-builder` |

---

## Archivos del Sistema

| Archivo | Propósito |
|---|---|
| `_Skills/activePatterns.json` | Patrones de voz/estructura aprobados por Daniel — se lee en cada sesión |
| `_Skills/PROCESS_LOG.md` | Bitácora append-only de archivos procesados + propuestas de cambio |
| `_Skills/mapeo-modos-skills.md` | Tabla canónica modo → skills (referencia rápida) |
| `_Skills/README-sistema.md` | Documentación operativa del sistema completo |
| `ContextoMaestro/ContextoMaestro.md` | Fuente de verdad de voz, teología y líneas rojas |

> **IMPORTANTE:** Sincronizar `ContextoMaestro/ContextoMaestro.md` con `~/Desktop/Claude/Contexto Maestro — Daniel Lira.md` cada vez que el Contexto Maestro se actualice.

---

## Control de Tokens

Al llegar al **50% del contexto** de la sesión, avisar: *"Estamos al 70% del contexto. Considera abrir una nueva sesión para no perder continuidad."*

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
