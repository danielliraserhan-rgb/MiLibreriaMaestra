---
name: zettelkasten-forge
description: "Genera notas atómicas Zettelkasten a partir de contenido procesado. Actívalo después de modo-ab, modo-e, modo-c, inbox-triage, o notas-maestria — cuando el pipeline del modo lo requiera. Produce notas ZK con IDs canónicos (ZK-YYYYMMDD-HHMM), nombres de archivo formato 'ZK-YYYYMMDD-HHMM Titulo Corto.md', wikilinks, YAML v2 completo, y campo coaching_notes para loops con S2. Nunca guarda notas sin OK explícito de Daniel."
---

# ZETTELKASTEN-FORGE — Generador de Notas Atómicas

**Principio:** Una idea = una nota. Granular, enlazada, permanente.

**Principio de Autoría:** El contenido de cada nota es 70–80% texto de Daniel, extraído directamente del archivo fuente. La IA puede aportar hasta un 20–30% únicamente como *puente de coherencia*: una bisagra mínima que hace que la idea se sostenga sola sin el contexto del documento completo. La IA no sintetiza, no concluye, no elabora por cuenta propia.

## FASE 1 — LECTURA DEL MATERIAL

Leer el archivo fuente (ya procesado por el pipeline anterior).

Identificar internamente:
- Dominio: pastoral | academico
- Modo de origen (1–7 o Académico)
- Rango de notas esperado (ver tabla)

| Modo | Rango ZK |
|---|---|
| 1 — Libro Terminado | 15–30 |
| 2 — Libro Pre-Diseño | 10–25 |
| 3 — Ideas Sueltas | 5–10 |
| 4 — Guía de Estudio | 10–20 |
| 5 — Nota Temática | 5–10 |
| 6 — Clase Larga | 8–15 |
| 7 — Grupos Conexión | 3–5 |
| Académico | 5–15 |

## FASE 2 — PROPONER NOTAS

Para cada nota candidata, presentar:

```
Nombre de archivo: ZK-YYYYMMDD-HHMM Titulo Corto.md
ID: ZK-YYYYMMDD-HHMM
Título: [título atómico completo — una sola idea]
Idea central: [una oración]
Wikilinks sugeridos: [[ZK-YYYYMMDD-HHMM Titulo Corto]] [[ZK-YYYYMMDD-HHMM Titulo Corto]]
Dominio: pastoral | academico
```

**Regla para Titulo Corto (en el nombre de archivo):**
- Si el título tiene ` — ` (raya em), tomar solo la parte anterior al primer ` — `
- Sin ` — `: usar el título completo
- Máximo 60 caracteres (cortar en la última palabra que quepa)
- Sin caracteres problemáticos: `: " / \ ? * | < >`

**Regla de autoría en propuestas:**
- `Idea central`: extraer una oración directamente del texto fuente — no generar una nueva. Si no hay oración que capture la idea, usar el fragmento más cercano y marcarlo: `[extraído aproximado]`.
- `Título`: derivar del fuente (encabezado, frase clave del texto de Daniel). Solo generarlo si el fuente no ofrece ningún ancla clara — en ese caso marcarlo con `[TÍTULO GENERADO]` para que Daniel lo revise y reemplace.

Presentar TODAS las propuestas antes de crear cualquiera.
Esperar OK de Daniel (puede aprobar todas, algunas, o pedir cambios).

## FASE 3 — CREAR NOTAS APROBADAS

Solo tras OK explícito de Daniel.

**Nombre de archivo:** `ZK-YYYYMMDD-HHMM Titulo Corto.md` (mismo formato propuesto en Fase 2).

### REGLA DE CONTENIDO — Autoría Exclusiva (70/30)

El cuerpo de la nota (todo lo que va después del YAML) se construye con texto de Daniel como base:

- **Permitido (70–80%):** citas textuales, fragmentos del fuente, párrafos del material procesado, bullets transcritos.
- **Permitido como puente (20–30%):** una bisagra mínima de coherencia cuando la imagen, metáfora o referencia del fuente no se sostiene sin el contexto del documento completo. Ejemplos válidos: explicar que "la barca" es figura del regreso de Cristo, conectar una cita de Abraham con su cumplimiento cristológico, hilvanar bullets yuxtapuestos que sin conector pierden su dirección.
- **Prohibido:** síntesis propias, conclusiones elaboradas, párrafos explicativos que van más allá de lo que Daniel escribió, frases que "mejoran" o "completan" la idea de Daniel.
- Si el fragmento fuente es insuficiente para completar el cuerpo: presentar lo extraído y **esperar** a que Daniel lo complete. No rellenar.

Usar `obsidian-markdown` para crear cada nota con este formato:

```yaml
---
id: ZK-YYYYMMDD-HHMM
titulo: ""          # Afirmación completa
tipo: zettelkasten
subtipo: ""         # conceptual | argumental | exegetica | narrativa | conexion
dominio: ""         # pastoral | academico
tags: []
versiculos_biblicos: []
personajes: []
source_file: ""
source_section: ""
source_type: ""
notas_relacionadas: []
pattern_id:
coaching_notes: []  # IDs de sesiones de writing-coach o voice-trainer que usaron esta nota como fuente
fecha_creacion: YYYY-MM-DD
# === Spaced Review (SM-2) ===
fecha_proxima_revision: YYYY-MM-DD   # = fecha_creacion + 1 día
intervalo_dias: 1
repeticiones: 0
facilidad: 2.5
pregunta_reflexion: ""  # Ver instrucción abajo
---
```

**Instrucción `pregunta_reflexion`:** Generar una pregunta que interrogue la afirmación central de la nota desde el ministerio concreto de Daniel. La pregunta debe:
- Ser específica a la idea de la nota (no genérica)
- Conectar con predicación, congregación o vida espiritual si dominio=pastoral
- Conectar con el argumento académico y su vigencia si dominio=academico
- Formato: una sola oración interrogativa directa

Ejemplos pastorales:
- "¿En qué momento de tu última predicación esta distinción hubiera cambiado la aplicación?"
- "¿Dónde has visto a tu congregación confundir precisamente esto?"

Ejemplos académicos:
- "¿Qué evidencia del texto cambiaría esta interpretación?"
- "¿Cómo responde este argumento a la objeción más fuerte del autor contrario?"

Carpeta destino:
- Pastoral: `09_Zettelkasten/pastoral/`
- Académico: `09_Zettelkasten/academico/`

## FASE 4 — ACTUALIZAR FUENTE

Agregar los IDs de las notas ZK creadas al campo `zettelkasten_notes:` del archivo fuente.

**Nota para writing-coach y voice-trainer:** cuando una sesión de S2 use una nota ZK como fuente de análisis, agregar el ID de la sesión al campo `coaching_notes:` de esa nota usando `obsidian-markdown`.

---

**Regla de dominio:** Notas pastorales y académicas no se enlazan entre sí salvo aprobación explícita de Daniel.
