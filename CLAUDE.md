# CLAUDE.md v3 — MiLibreriaMaestra

> Voz, teología, marcos y líneas rojas: `ContextoMaestro/ContextoMaestro.md`
> Este archivo cubre arquitectura operativa únicamente.

---

## §1 Identidad del Sistema

**S1 — Segundo cerebro** (Obsidian): catalogar, conectar, generar notas atómicas.
**S2 — Coach de escritura** (Claude Code): analizar, retroalimentar, entrenar. Nunca escribe por Daniel.
Ambos comparten: `Inbox/` · `ContextoMaestro/` · `_Skills/activePatterns.json`

---

## §2 Estructura del Vault

**Pastoral** — `Temas/01–07`:
`01_Origenes` · `02_HistoriaDeIsrael` · `03_Escatologia—Destino` · `04_ExegesisNT`
`05_DoctrinasFundamentales` · `06_DiscipuladoVidaCristiana` · `07_PredicacionesDevocionales`

Cada tema: `01_Libros` / `02_EsquemasDeClase` / `03_ClasesEnVivo` / `04_NotasSinProcesar` / `05_MaterialExterno`

**Académico** — `Temas/08_Academico/Maestria`:
`01_ArtículosAcadémicos` / `02_CasosDeEstudio` / `03_ForosDePreguntas` / `04_Exámenes` / `05_NotasDeClasePorMi` / `06_NotasDeClasePorElProfesor`

**Sistema**: `Inbox/` · `Inbox/scrivener-sync/` · `Templates/` · `ContextoMaestro/` · `MapasDeContenido—MOCs/` · `_Skills/` · `Assets/`

**Zettelkasten**: `09_Zettelkasten/pastoral/` · `09_Zettelkasten/academico/` · `09_Zettelkasten/_indice/`

> `ClasesPorSemestre/` — fuera del alcance. No procesar.

---

## §3 Protocolo de Entrada

**Punto de entrada siempre:** `modo-selector` → lee `activePatterns.json` → llama a `inbox-triage`

```
**Punto de entrada siempre:** `modo-selector` → lee `activePatterns.json` → llama a `inbox-triage`

Daniel trae archivo → Inbox/ (o llega vía Inbox/scrivener-sync/ con source: scrivener)
↓
modo-selector → inbox-triage Fase 1 → detecta MODO + dominio + tema
↓
**[INTERVENCIÓN HÍBRIDA - AHORRO DE TOKENS]**
Claude NO genera el YAML ni mueve el archivo. Claude ejecuta en terminal:
`python3 _Scripts/inbox_triage.py "Inbox/archivo.md" '{"tipo": "X", "tema": "01_Origenes", "dominio": "pastoral", "modo": "1", "destino": "Temas/01_Origenes/01_Libros/"}'`
↓
Python inyecta YAML v2 y mueve el archivo al contenedor.
↓
[cargar categorías load_for según dominio — ver tabla §7]
↓
Skills del MODO (ver §4) → espera OK en cada checkpoint
↓
zettelkasten-forge → propone notas atómicas → espera OK
↓
¿ZK ≥ 8 O contenido teológicamente nuevo?
  SÍ → pattern-harvester → OK granular → actualiza activePatterns.json
  NO → registrar en PROCESS_LOG como "harvester diferido" (procesar en sesión batch)
↓
PROCESS_LOG.md updated

```

**Para carga masiva (5+ documentos):** usar `bulk-ingest` en lugar de `modo-selector`. Los checkpoints se agrupan por lote: triage del lote → OK → procesamiento auto → revisión ZK del lote → OK → pattern-harvester una vez → OK.

**Regla de oro:** `inbox-triage` siempre primero · `zettelkasten-forge` antes del harvester · nunca avanzar sin OK explícito de Daniel · `pattern-harvester` solo si ZK ≥ 8 o contenido teológicamente nuevo (Modo 7: siempre diferir).

**Motor de escritura:** `obsidian-markdown` es la ÚNICA herramienta para crear/editar .md en el vault. Prohibido: `cat`, `echo >>`, `sed`, `awk`, terminal para markdown.

---

## §4 Tabla de Enrutamiento de Modos

| Modo | Tipo | Skills en orden | Output ZK |
|---|---|---|---|
| **1** | Libro Terminado | `inbox-triage` → `modo-c`(opt) → `zettelkasten-forge` → `pattern-harvester` | 15–30 |
| **2** | Libro Pre-Diseño | `inbox-triage` → `modo-c` → `modo-ab` → `modo-r`(si hueco) → `zettelkasten-forge` → `pattern-harvester` | 10–25 |
| **3** | Ideas Sueltas | `inbox-triage` → `zettelkasten-forge` → `pattern-harvester`*(si ZK ≥ 8)* | 5–10 |
| **4** | Guía de Estudio | `inbox-triage` → `modo-e`(bíblica) → `zettelkasten-forge` → `pattern-harvester` | 10–20 |
| **5** | Nota Temática | `inbox-triage` → `modo-c`(opt) → `zettelkasten-forge` → `pattern-harvester`*(si ZK ≥ 8)* | 5–10 |
| **6** | Clase Larga | `inbox-triage` → `modo-e` → `modo-ab`(si transcripción) → `zettelkasten-forge` → `pattern-harvester` | 8–15 |
| **7** | Grupos Conexión | `inbox-triage` → `modo-e`(temática) → `zettelkasten-forge` *(harvester siempre diferido)* | 3–5 |
| **Acad.** | Maestría | `inbox-triage` → `notas-maestria` → `zettelkasten-forge`(neutral) → `pattern-harvester` | 5–15 |

---

## §5 Mapa de Skills

| Situación                                                                        | Skill                               |
| -------------------------------------------------------------------------------- | ----------------------------------- |
| Nuevo archivo en inbox                                                           | `modo-selector`                     |
| **5+ archivos en inbox (carga masiva)**                                          | `bulk-ingest`                       |
| Diagnóstico de tipo y generación de JSON payload para inyección YAML vía Python. | `inbox-triage`                      |
| Texto pastoral: oral + escrito, o borrador                                       | `modo-ab-seccion-mixta`             |
| Diagnóstico / mapa estructural                                                   | `modo-c-esquema-editorial`          |
| Hueco estructural, material de referencia                                        | `modo-r-material-referencia`        |
| Esquema para clase / enseñanza                                                   | `modo-e-unificado`                  |
| Lectura académica / nota de maestría                                             | `notas-maestria`                    |
| Generar notas atómicas Zettelkasten                                              | `zettelkasten-forge`                |
| Detectar y proponer patrones                                                     | `pattern-harvester`                 |
| Mapa de contenido (índice de notas)                                              | `moc-builder`                       |
| **Huecos estructurales** (preguntas abiertas, patrones débiles, huérfanas)       | `desarrollador-de-temas`            |
| **Cobertura cuantitativa de temas** (temas mencionados con pocas notas ZK)       | script: `scan_vault.py --mode gaps` |
| **Análisis de voz + teología (S2)**                                              | `writing-coach`                     |
| **Espejo de voz vs patrones aprobados**                                          | `voice-trainer`                     |
| **Guía de formato por tipo de contenido**                                        | `format-adapter`                    |
| **Detectar archivo nuevo desde Scrivener**                                       | `scrivener-bridge`                  |
|                                                                                  |                                     |
|                                                                                  |                                     |
### Reglas para Skills de Soporte (100% Python)
* **scrivener-bridge:** Cuando Daniel indique que un borrador de Scrivener está listo para el vault, NO leas ni fusiones los textos. Ejecuta en la terminal: `python3 _Scripts/scrivener_bridge.py "<ruta_scrivener>" "<ruta_vault>"`
* **moc-builder:** Escanea con `scan_vault.py`, agrupa las notas con tu criterio editorial, y TIENES PROHIBIDO escribir el archivo final en el vault. Para guardar, debes compilar un JSON y ejecutar el comando: `python3 _Scripts/write_moc.py "<Tema>" '<json_payload>'`.
* **markdown-cleaner:** NUNCA intentes corregir espacios o tabulaciones reescribiendo el archivo. Si Daniel pide "limpiar el formato visual" o arreglar espacios, ejecuta en la terminal: python3 _Scripts/format_adapter.py "<ruta_del_archivo>"
---

## §6 Contrato YAML v2

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
fuente: ""          # dictado | grabacion | borrador | clase | conferencia | paper | scrivener
author_quotes: []
zettelkasten_notes: []  # IDs: ZK-YYYYMMDD-HHMM-NNN
coaching_notes: []      # IDs de sesiones de coach que usaron este archivo como fuente
version_yaml: "2.0"
fecha_actualizacion: ""
---
```

**Regla:** YAML v1 sigue siendo válido. Al pasar por el sistema: upgrade automático. Campos v1 NUNCA se renombran.

---

## §7 Archivos del Sistema

| Archivo | Propósito |
|---|---|
| `_Skills/activePatterns.json` | Patrones aprobados v2.0 — organizados por categoría (estructura, teologia, hermeneutica, voz). Usar `load_for` para cargar solo las categorías relevantes a la tarea. |
| `_Skills/VAULT_INDEX.md` | Índice comprimido del vault: fuentes procesadas, clusters ZK, notas más conectadas. Cargar al inicio de sesiones de investigación o coach. Regenerar con `scan_vault.py --mode index`. |
| `_Skills/PROCESS_LOG.md` | Bitácora append-only |
| `ContextoMaestro/ContextoMaestro.md` | Fuente de verdad: voz, teología, líneas rojas |
| `ContextoMaestro/00_ESENCIAL.md` | Cargar siempre. Resumen ejecutivo del ContextoMaestro |
| `ContextoMaestro/04_voz.md` | Cargar solo para tareas pastorales o sesiones de coach |
| `Inbox/scrivener-sync/` | Carpeta monitoreada: archivos que llegan desde Scrivener |

**Protocolo de carga por tipo de sesión:**

| Tipo de sesión | Clave `load_for` | Categorías que carga |
|---|---|---|
| Procesamiento pastoral (Modos 1–7) | `pastoral_general` | estructura, teologia, hermeneutica |
| Coach de escritura (S2) | `coach_s2` | voz, estructura |
| Exégesis / estudio bíblico | `exegesis` | hermeneutica, teologia |
| Académico (Modo Acad.) | `academico` | teologia, hermeneutica |
| Bulk-ingest | `bulk_ingest` | teologia, hermeneutica, estructura |
| Investigación / MOC | `pastoral_general` + VAULT_INDEX | estructura, teologia, hermeneutica |

Todos los tipos cargan `00_ESENCIAL.md`. Coach S2 también carga `04_voz.md`.

> Sincronizar `ContextoMaestro/ContextoMaestro.md` con `~/Desktop/Claude/Contexto Maestro — Daniel Lira.md` cuando se actualice.

---

## §8 Protocolo Coach de Escritura (S2)

**Principio:** El coach analiza. Daniel escribe. Siempre.

**Activación:** Cuando Daniel trae un texto propio para revisión (no para catalogar).

**Flujo del coach:**
1. Leer `ContextoMaestro/00_ESENCIAL.md` + `ContextoMaestro/04_voz.md` antes de analizar
2. Leer `_Skills/activePatterns.json` para patrones activos
3. Analizar el texto en 5 categorías y devolver reporte:
   - **Voz** — ¿Cuáles de las 5 marcas están presentes / ausentes? Citar líneas exactas.
   - **Teología** — ¿Algún marco del §2 está ausente o comprometido?
   - **Estructura** — ¿El arco humana condición → respuesta de Dios → aplicación está completo?
   - **Ritmo** — ¿Hay párrafos largos sin remate corto? ¿Dónde falta respiración?
   - **Líneas rojas** — ¿Alguna de las 9 prohibiciones activada? Citar sección exacta del ContextoMaestro.
4. Proponer 2–3 preguntas que Daniel pueda hacerse para mejorar el texto (no reescribir)
5. Si el análisis genera insights permanentes → proponer a `pattern-harvester`

**Regla:** Toda observación debe citar la sección de ContextoMaestro que la sustenta.

---

## §9 Reglas de Control

- **70% del contexto:** Avisar: *"Estamos al 70%. Considera abrir una nueva sesión."*
- **ContextoMaestro/:** Nunca modificar. Solo leer.
- **activePatterns.json:** Solo actualizar con OK explícito de Daniel.
- **Notas ZK:** Solo crear con OK explícito de Daniel después de revisión.
- **Dominio académico ↔ pastoral:** No mezclar. Las notas ZK de cada dominio no se enlazan entre sí salvo aprobación explícita.
- **Scrivener sync:** La dirección `Obsidian → Scrivener` es siempre manual. El sistema nunca sobreescribe drafts de Scrivener.
