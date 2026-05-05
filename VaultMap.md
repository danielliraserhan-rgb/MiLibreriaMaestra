# VaultMap.md — Mapa de la Bóveda

> Arquitectura completa del vault. Carga al navegar, mover archivos o iniciar sesión de investigación.
> Distingue dónde viven los archivos de operación de Claude vs. dónde vive la base de conocimiento de Daniel.
> Claude puede tocar archivos del Segundo Cerebro con OK explícito de Daniel — la distinción es geográfica, no de permisos.

---

## Para Claude — Infraestructura Operativa

Estos directorios y archivos son el sistema nervioso. Claude los lee, escribe via scripts, o ejecuta contra ellos.

| Ruta | Función | Regla |
|---|---|---|
| `Inbox/` | Punto de entrada de todo material nuevo | Nunca procesar sin `modo-selector` primero |
| `Inbox/scrivener-sync/` | Archivos que llegan desde Scrivener | Solo modificar via `scrivener_bridge.py` |
| `Inbox/scrivener-sync/export/` | Archivos exportados hacia Scrivener | Limpiados por script (sin YAML, sin wikilinks) |
| `ContextoMaestro/` | Fuente de verdad: voz, teología, líneas rojas | **Nunca modificar. Solo leer.** |
| `ContextoMaestro/00_ESENCIAL.md` | Resumen ejecutivo del ContextoMaestro | Reemplazado por `Daniel.md` para uso directo |
| `ContextoMaestro/04_voz.md` | Ejemplos de corpus y marcas de voz | Cargar solo en sesiones de coach (S2) |
| `_Skills/activePatterns.json` | Patrones aprobados v2.0 (estructura, teologia, hermeneutica, voz) | Actualizar solo con OK explícito de Daniel |
| `_Skills/VAULT_INDEX.md` | Índice comprimido: fuentes procesadas, clusters ZK | Regenerar: `python3 _Scripts/scan_vault.py --mode index` |
| `_Skills/PROCESS_LOG.md` | Bitácora append-only de procesamiento | Solo append — nunca editar entradas anteriores |
| `_Skills/scrivener-manifest.json` | Registro de co-edición: estado, timestamps, flag de conflicto | Consultar antes de editar cualquier archivo con `fuente: scrivener` |
| `_Scripts/` | Scripts Python — ejecutores del sistema | Comandos completos en `SkillsMap.md` |
| `skills-sistema-v3/<skill>/SKILL.md` | Definiciones de skills activos | Ruta raíz de todos los skills del vault |
| `Templates/` | Plantillas del vault | Solo usar como base — nunca editar directamente |
| `MapasDeContenido—MOCs/` | MOCs generados por `write_moc.py` | **No editar manualmente. Solo via script.** |
| `Daniel.md` | Identidad, voz, teología, instrucciones para la IA | Cargar siempre al inicio de sesión |
| `SkillsMap.md` | Skills y scripts con comandos completos | Cargar al ejecutar cualquier skill o script |

---

## Segundo Cerebro — Base de Conocimiento de Daniel

Estos directorios son la biblioteca viva de Daniel. Claude los procesa, popula y edita **con OK explícito de Daniel**. La separación no indica restricción — indica dónde vive el conocimiento vs. dónde vive la infraestructura del sistema.

### Temas Pastorales — `Temas/01–07`

| Tema | Directorio |
|---|---|
| Orígenes | `01_Origenes` |
| Historia de Israel | `02_HistoriaDeIsrael` |
| Escatología / Destino | `03_Escatologia—Destino` |
| Exégesis NT | `04_ExegesisNT` |
| Doctrinas Fundamentales | `05_DoctrinasFundamentales` |
| Discipulado / Vida Cristiana | `06_DiscipuladoVidaCristiana` |
| Predicaciones Devocionales | `07_PredicacionesDevocionales` |

Cada tema tiene 5 contenedores estándar:
`01_Libros` / `02_EsquemasDeClase` / `03_ClasesEnVivo` / `04_NotasSinProcesar` / `05_MaterialExterno`

### Temas Académicos — `Temas/08_Academico/Maestria`

`01_ArtículosAcadémicos` / `02_CasosDeEstudio` / `03_ForosDePreguntas` / `04_Exámenes` / `05_NotasDeClasePorMi` / `06_NotasDeClasePorElProfesor`

### Zettelkasten — `09_Zettelkasten/`

| Subdirectorio | Contenido |
|---|---|
| `pastoral/` | Notas ZK del dominio pastoral |
| `academico/` | Notas ZK del dominio académico |
| `_indice/` | Índice de notas ZK |

**Regla:** Dominios pastoral y académico no se enlazan entre sí salvo aprobación explícita de Daniel.

---

## Fuera del Alcance de Claude

| Directorio / Archivo | Razón |
|---|---|
| `ClasesPorSemestre/` | Fuera del sistema. No procesar. |
| `Bienvenido.md` | Nota inicial de Obsidian — ignorar. |
| `_Archive/` | Solo almacenamiento. No procesar sin instrucción explícita. |

---

## Protocolo de Carga por Tipo de Sesión

| Tipo de sesión | Clave `load_for` | Archivos a cargar | Categorías de patrones |
|---|---|---|---|
| Procesamiento pastoral (Modos 1–7) | `pastoral_general` | `Daniel.md` + `activePatterns.json` | estructura, teologia, hermeneutica |
| Coach de escritura (S2) | `coach_s2` | `Daniel.md` + `04_voz.md` + `activePatterns.json` | voz, estructura |
| Exégesis / estudio bíblico | `exegesis` | `Daniel.md` + `activePatterns.json` | hermeneutica, teologia |
| Académico (Modo Acad.) | `academico` | `Daniel.md` + `activePatterns.json` | teologia, hermeneutica |
| Bulk-ingest | `bulk_ingest` | `Daniel.md` + `activePatterns.json` | teologia, hermeneutica, estructura |
| Investigación / MOC | `pastoral_general` + VAULT_INDEX | `Daniel.md` + `VAULT_INDEX.md` + `activePatterns.json` | estructura, teologia, hermeneutica |

> `Daniel.md` reemplaza la carga directa de `ContextoMaestro/00_ESENCIAL.md` en todos los tipos de sesión.

---

## Nota de Sincronización

> Sincronizar `ContextoMaestro/ContextoMaestro.md` con `~/Desktop/Claude/Contexto Maestro — Daniel Lira.md` cuando se actualice.
