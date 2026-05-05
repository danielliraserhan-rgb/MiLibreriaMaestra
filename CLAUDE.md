# CLAUDE.md v4.0 — MiLibreriaMaestra

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Archivo de enrutamiento principal. Lee los 3 mapas según el tipo de sesión.

---

## Your Maps — Carga según sesión

| Archivo | Carga cuando... |
|---|---|
| `Daniel.md` | **Siempre.** Identidad, misión, voz y marcos teológicos de Daniel. Reemplaza `ContextoMaestro/00_ESENCIAL.md` en uso directo. |
| `VaultMap.md` | Al navegar o mover archivos · al iniciar sesión de investigación · **solo en Fase de Catalogación** (no cargar en sesiones de coaching). |
| `SkillsMap.md` | Al ejecutar cualquier skill o script · **solo en Fase de Catalogación**. |

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

## §3A Protocolo de Catalogación

**Trigger:** Daniel dice `inbox [archivo]` (un archivo) o `bulk` (5+ archivos)
**Contexto que carga:** VaultMap + activePatterns.json + SkillsMap
**Contexto que NO carga:** Daniel.md voz completo · ContextoMaestro/04_voz.md · nada relacionado con coaching

**LÍMITE DE ROL — PROHIBIDO en sesión de catalogación:**
- Mencionar coaching, análisis de escritura, S2 o voz de Daniel
- Recomendar `writing-coach` o `voice-trainer` dentro del flujo
- Opinar sobre calidad, estilo o tono del texto

```
Daniel trae archivo → Inbox/ (o llega vía Inbox/scrivener-sync/ con source: scrivener)
↓
modo-selector → inbox-triage Fase 1 → detecta MODO + dominio + tema
↓
[INTERVENCIÓN HÍBRIDA - AHORRO DE TOKENS]
Claude NO genera el YAML ni mueve el archivo. Claude ejecuta en terminal:
`python3 _Scripts/inbox_triage.py "Inbox/archivo.md" '{"tipo": "X", "tema": "01_Origenes", "dominio": "pastoral", "modo": "1", "destino": "Temas/01_Origenes/01_Libros/"}'`
↓
Python inyecta YAML v2 (incluye fase_sistema: catalogado) y mueve el archivo al contenedor.
Si Python retorna error → reportar el error exacto. El archivo permanece en Inbox/ sin YAML.
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

**Para carga masiva (5+ documentos):** usar `bulk-ingest` en lugar de `modo-selector`. Los checkpoints se agrupan por lote: triage del lote → OK → procesamiento auto → revisión ZK del lote → OK → pattern-harvester una vez → OK. Al terminar: todos los archivos del lote tienen `fase_sistema: catalogado`.

**Regla de fecha en carga inicial (batch):** Durante `bulk-ingest` o cualquier ingesta de contenido pre-existente, el campo `fecha` DEBE reflejar cuándo se creó o impartió el contenido original, **no** la fecha en que se ingresó al vault. El sistema escanea el documento para detectar esa fecha antes de asignar `fecha: ""`. `fecha_ingesta` registra automáticamente la fecha de hoy. Las notas nuevas (escritas hoy) no necesitan detección: `fecha` = hoy. Ver §6 para el algoritmo de detección y jerarquía de fuentes.

**Regla de oro:** `inbox-triage` siempre primero · `zettelkasten-forge` antes del harvester · nunca avanzar sin OK explícito de Daniel · `pattern-harvester` solo si ZK ≥ 8 o contenido teológicamente nuevo (Modo 7: siempre diferir).

**Motor de escritura:** skill `/obsidian-markdown` (instalado en `skills-sistema-v3/obsidian-markdown/`). Aplica siempre al crear o editar `.md` en el vault. Prohibido en cualquier caso: `cat`, `echo >>`, `sed`, `awk`, terminal para markdown.

---

## §3B Protocolo de Coaching

**Trigger:** Daniel dice `inicia coaching [archivo]` o `inicia coaching [archivo] modo:[X]`
**Contexto que carga:** Daniel.md + ContextoMaestro/04_voz.md + activePatterns.json (solo categoría voz)
**Contexto que NO carga:** VaultMap · SkillsMap · reglas de enrutamiento · rutas del vault

**Modos disponibles:**

| Modo | Qué analiza |
|---|---|
| `voz` | Las 5 marcas de voz de Daniel, ritmo, remates cortos — ideal para predicaciones y dictados |
| `teologia` | Marcos teológicos, líneas rojas, estructura arco — ideal para libros y estudios doctrinales |
| `estructura` | Arco condición humana → respuesta de Dios → aplicación — ideal para manuscritos en desarrollo |
| `ritmo` | Densidad de párrafos, respiración, variación de longitud |
| `auto` | Claude lee los primeros 300 palabras y propone el modo más útil antes de empezar |

```
PASO 0 — Verificación de estado:
python3 _Scripts/coaching_selector.py "ruta/archivo.md"
→ Si fase_sistema ≠ catalogado: avisar a Daniel y ofrecer ejecutar inbox primero
→ Si fase_sistema = catalogado: continuar

PASO 1 — Modo de análisis:
- Si Daniel especificó modo → usar ese modo directamente
- Si Daniel no especificó modo (o modo=auto):
  → Claude lee primeros 300 palabras del texto
  → Propone: "Veo que este texto es [tipo]. Te sugiero modo [X]. ¿Seguimos?"
  → Espera confirmación antes de analizar

PASO 2 — Cargar contexto de coaching:
Daniel.md + ContextoMaestro/04_voz.md + activePatterns.json (categoría voz únicamente)

PASO 3 — Análisis según modo activo (ver skill writing-coach)

PASO 4 — Proponer 2–3 preguntas que Daniel pueda hacerse (nunca reescribir)

PASO 5 — Si análisis genera insights permanentes → proponer pattern-harvester → OK de Daniel

PASO 6 — YAML actualiza: coaching_notes agrega ID de sesión · fase_sistema: coaching_completado
```

**Regla:** Toda observación debe citar la sección de `Daniel.md` o `ContextoMaestro/` que la sustenta. El coach analiza. Daniel escribe. Siempre.

---

## §4 Tabla de Enrutamiento de Modos

| Modo      | Tipo             | Skills en orden                                                                         | Output ZK |
| --------- | ---------------- | --------------------------------------------------------------------------------------- | --------- |
| **1**     | Libro Terminado  | `inbox-triage`  → `zettelkasten-forge` → `pattern-harvester`                            | 15–30     |
| **2**     | Libro Pre-Diseño | `inbox-triage`  → `zettelkasten-forge` → `pattern-harvester`                            | 10–25     |
| **3**     | Ideas Sueltas    | `inbox-triage` → `zettelkasten-forge` → `pattern-harvester`*(si ZK ≥ 8)*                | 5–10      |
| **4**     | Guía de Estudio  | `inbox-triage` → `zettelkasten-forge` → `pattern-harvester`                             | 10–20     |
| **5**     | Nota Temática    | `inbox-triage` → `zettelkasten-forge` → `pattern-harvester`*(si ZK ≥ 8)*                | 5–10      |
| **6**     | Clase Larga      | `inbox-triage` → `zettelkasten-forge` → `pattern-harvester`                             | 8–15      |
| **7**     | Grupos Conexión  | `inbox-triage` → `zettelkasten-forge` *(harvester siempre diferido)*                    | 3–5       |
| **Acad.** | Maestría         | `inbox-triage` → `notas-maestria` → `zettelkasten-forge`(neutral) → `pattern-harvester` | 5–15      |

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
fecha: ""           # fecha de creación/impartición original del contenido (NO fecha de ingesta al vault)
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
fase_sistema: ""        # sin_procesar | catalogado | coaching_activo | coaching_completado
version_yaml: "2.0"
fecha_ingesta: ""   # auto: fecha en que se procesó el archivo en el vault (hoy)
fecha_actualizacion: ""
scrivener_sync:
  estado: ""        # sincronizado | modificado_vault | pendiente_export | conflicto
  ultima_sync: ""
  ultima_export: ""
  scrivener_nombre: ""
---
```

**Regla:** YAML v1 sigue siendo válido. Al pasar por el sistema: upgrade automático. Campos v1 NUNCA se renombran.

### §6.1 Algoritmo de detección de fecha (carga inicial / batch)

**Solo aplica cuando el contenido es pre-existente** (bulk-ingest o ingesta de material histórico). Para notas nuevas: `fecha` = hoy, skip.

**Jerarquía de fuentes (en orden de prioridad):**

1. **YAML frontmatter existente** — si `fecha:` ya tiene valor, respetar y no sobreescribir.
2. **Nombre del archivo** — buscar patrón `YYYY-MM-DD`, `YYYY_MM_DD`, o `YYYY-MM` en el nombre.
3. **Primeros 500 caracteres del cuerpo** — buscar fechas explícitas:
   - Formato ISO: `2023-05-14`
   - Formato textual ES: "14 de mayo de 2023", "Domingo 14 mayo", "mayo 2023"
   - Encabezados de clase/predicación: "Clase del...", "Predicación:", "Serie:", "Sesión"
4. **Cualquier mención de año (1990–2030) en los primeros 200 palabras** con contexto de mes.
5. **Sin fecha detectada** → asignar `fecha: "sin_fecha"` y marcar en el triage como `⚠ fecha no detectada` para que Daniel la asigne manualmente.

**Formato de salida:** siempre `YYYY-MM-DD`. Si solo se detecta año → `YYYY`. Si año+mes → `YYYY-MM`.

**Cuando hay múltiples fechas:** usar la más antigua (fecha de origen, no de edición).

---

## §8 Protocolo Coach de Escritura (S2)

> **Ver §3B para el protocolo completo de activación, modos y flujo.**

**Trigger:** `inicia coaching [archivo]` o `inicia coaching [archivo] modo:[voz|teologia|estructura|ritmo|auto]`

**Principio:** El coach analiza. Daniel escribe. Siempre.

**Skill:** `writing-coach` — acepta parámetro `modo`. Si no se especifica, usa `auto`.

**Conexiones semánticas (opcional):** Si ChromaDB indexado, consultar con primeros 200 palabras. Mostrar 2–3 notas ZK. Formato: `[[ZK-ID Título]] — tema — relevancia`. Solo mismo dominio. Degradación elegante si ChromaDB no disponible.

**Regla:** Toda observación debe citar la sección de `Daniel.md` o `ContextoMaestro/` que la sustenta. No cargar VaultMap ni SkillsMap en sesiones de coaching.

---

## §9 Reglas de Control

- **50% del contexto:** Avisar: *"Estamos al 50%. Considera abrir una nueva sesión."*
- **Daniel es el único autor del Segundo Cerebro:** Claude no tiene autoría sobre el contenido. Solo puede intervenir de dos formas: (1) agregar contexto que hace comprensible una idea incompleta, (2) agregar conjunciones o mínimas modificaciones para que citas textuales de Daniel fluyan en prosa legible. Ninguna intervención puede introducir ideas, argumentos o voz nuevos. Ver detalle en `Daniel.md §Instrucciones Operativas`.
- **Segundo Cerebro:** Claude puede crear, editar o mover archivos en `Temas/`, `09_Zettelkasten/` y `MapasDeContenido—MOCs/` solo con OK explícito de Daniel. La distinción "Para Claude / Segundo Cerebro" en `VaultMap.md` es geográfica, no de permisos.
- **ContextoMaestro/:** Nunca modificar. Solo leer.
- **activePatterns.json:** Solo actualizar con OK explícito de Daniel.
- **Notas ZK:** Solo crear con OK explícito de Daniel después de revisión.
- **Dominio académico ↔ pastoral:** No mezclar. Las notas ZK de cada dominio no se enlazan entre sí salvo aprobación explícita.
- **Scrivener sync:** La dirección `Obsidian → Scrivener` se maneja via `scrivener-export`. El sistema nunca sobreescribe drafts de Scrivener sin OK explícito de Daniel.
