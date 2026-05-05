# CLAUDE.md v4.0 — MiLibreriaMaestra

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Archivo de enrutamiento principal. Lee los 3 mapas según el tipo de sesión.

---

## Your Maps — Carga según sesión

| Archivo | Carga cuando... |
|---|---|
| `Daniel.md` | **Siempre.** Identidad, misión, voz y marcos teológicos de Daniel. Reemplaza `ContextoMaestro/00_ESENCIAL.md` en uso directo. |
| `VaultMap.md` | Al navegar, mover archivos o iniciar sesión de investigación. |
| `SkillsMap.md` | Al ejecutar cualquier skill o script. |

---

## §0 Principios Operativos (Karpathy Rules)

1. **Think Before Acting:** No asumas contexto, intención ni postura teológica. Si un documento en `Inbox/` es ambiguo respecto a su dominio (Pastoral o Académico), detente y pregunta a Daniel. Muestra tus supuestos teológicos antes de procesar.
2. **Simplicity First:** Prioriza siempre el enfoque mínimo viable. Cuando generes notas atómicas (ZK) o MOCs, usa síntesis extrema y cero texto de relleno ("verborrea de IA"). Respeta la voz original del documento.
3. **Surgical Changes:** Jamás reescribas un archivo `.md` completo para aplicar un cambio menor. Toda modificación de texto debe ser quirúrgica (solo las líneas afectadas). Confía enteramente en los scripts de `_Scripts/` para cambios estructurales o inyección masiva de YAML.
4. **Goal-Driven Execution:** Asegura el resultado de tu Modo Activo. Tienes estrictamente prohibido avanzar de la Fase 1 a la Fase 2 sin la aprobación explícita de Daniel, y antes de terminar, debes verificar empíricamente que se lograron los entregables exactos (ej. creación de las N notas ZK correspondientes al lote).
5. **Pre-edición Scrivener:** Antes de editar cualquier `.md` con `fuente: scrivener` en su YAML, consultar `_Skills/scrivener-manifest.json`. Si `editado_en_vault_post_sync: true`, avisar a Daniel antes de proceder. Después de editar, actualizar la entrada del manifest: `estado → modificado_vault`, `editado_en_vault_post_sync → true`.

---

## §0.5 Rutas Críticas del Sistema

**Vault:** raíz del repositorio (todos los scripts usan rutas relativas a `__file__`)

| Componente | Ruta relativa al vault |
|---|---|
| Scripts Python | `_Scripts/` |
| SKILL.md de skills | `skills-sistema-v3/<nombre-skill>/SKILL.md` |
| Patrones y estado | `_Skills/` |
| MOCs generados | `MapasDeContenido—MOCs/` |
| ZK Pastoral | `09_Zettelkasten/pastoral/` |
| ZK Académico | `09_Zettelkasten/academico/` |
| ContextoMaestro | `ContextoMaestro/` |

> Para comandos completos de scripts y tabla completa de skills → `SkillsMap.md`
> Para arquitectura del vault, archivos del sistema y protocolo de carga → `VaultMap.md`

---

## §3 Protocolo de Entrada

**Punto de entrada siempre:** `modo-selector` → lee `activePatterns.json` → llama a `inbox-triage`

```
Daniel trae archivo → Inbox/ (o llega vía Inbox/scrivener-sync/ con source: scrivener)
↓
modo-selector → inbox-triage Fase 1 → detecta MODO + dominio + tema
↓
[INTERVENCIÓN HÍBRIDA - AHORRO DE TOKENS]
Claude NO genera el YAML ni mueve el archivo. Claude ejecuta en terminal:
`python3 _Scripts/inbox_triage.py "Inbox/archivo.md" '{"tipo": "X", "tema": "01_Origenes", "dominio": "pastoral", "modo": "1", "destino": "Temas/01_Origenes/01_Libros/"}'`
↓
Python inyecta YAML v2 y mueve el archivo al contenedor.
↓
[cargar categorías load_for según dominio — ver protocolo en VaultMap.md]
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

**Motor de escritura:** skill `/obsidian-markdown` (instalado en `skills-sistema-v3/obsidian-markdown/`). Aplica siempre al crear o editar `.md` en el vault. Prohibido en cualquier caso: `cat`, `echo >>`, `sed`, `awk`, terminal para markdown.

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
scrivener_sync:
  estado: ""        # sincronizado | modificado_vault | pendiente_export | conflicto
  ultima_sync: ""
  ultima_export: ""
  scrivener_nombre: ""
---
```

**Regla:** YAML v1 sigue siendo válido. Al pasar por el sistema: upgrade automático. Campos v1 NUNCA se renombran.

---

## §8 Protocolo Coach de Escritura (S2)

**Principio:** El coach analiza. Daniel escribe. Siempre.

**Activación:** Cuando Daniel trae un texto propio para revisión (no para catalogar).

**Flujo del coach:**
1. Leer `Daniel.md` (voz, marcos, líneas rojas) + `ContextoMaestro/04_voz.md`
2. Leer `_Skills/activePatterns.json` para patrones activos
3. Analizar el texto en 5 categorías:
   - **Voz** — ¿Cuáles de las 5 marcas están presentes / ausentes? Citar líneas exactas.
   - **Teología** — ¿Algún marco está ausente o comprometido?
   - **Estructura** — ¿El arco condición humana → respuesta de Dios → aplicación está completo?
   - **Ritmo** — ¿Párrafos largos sin remate corto? ¿Dónde falta respiración?
   - **Líneas rojas** — ¿Alguna de las 9 prohibiciones activada? Citar sección exacta.
4. Proponer 2–3 preguntas que Daniel pueda hacerse para mejorar el texto (no reescribir)
4b. **Conexiones semánticas:** Si ChromaDB indexado, consultar con primeros 200 palabras. Mostrar 2-3 notas ZK. Formato: `[[ZK-ID Título]] — tema — relevancia`. Solo mismo dominio. Degradación elegante si ChromaDB no disponible.
5. Si el análisis genera insights permanentes → proponer a `pattern-harvester`

**Regla:** Toda observación debe citar la sección de `Daniel.md` o `ContextoMaestro/` que la sustenta.

---

## §9 Reglas de Control

- **70% del contexto:** Avisar: *"Estamos al 70%. Considera abrir una nueva sesión."*
- **ContextoMaestro/:** Nunca modificar. Solo leer.
- **activePatterns.json:** Solo actualizar con OK explícito de Daniel.
- **Notas ZK:** Solo crear con OK explícito de Daniel después de revisión.
- **Dominio académico ↔ pastoral:** No mezclar. Las notas ZK de cada dominio no se enlazan entre sí salvo aprobación explícita.
- **Scrivener sync:** La dirección `Obsidian → Scrivener` se maneja via `scrivener-export`. El sistema nunca sobreescribe drafts de Scrivener sin OK explícito de Daniel.
