---
name: inbox-triage
description: "Punto de entrada de todo el flujo editorial de Daniel Lira. Actívalo SIEMPRE que Daniel diga 'nuevo archivo en inbox', 'aplica triage a este archivo', 'procesa esto del inbox', 'clasifica este archivo', 'triagea esto', o cuando entregue un archivo sin indicar qué hacer con él y el contexto sea editorial. El skill ejecuta dos fases en estricto orden: Fase 1 (automática) lee y diagnostica el archivo sin crear nada; Fase 2 (solo tras OK explícito de Daniel) crea la nota, llena el YAML v2, aplica estructura y mueve el archivo. NUNCA saltar de Fase 1 a Fase 2 sin confirmación. También actívalo si Daniel dice 'qué tipo de archivo es este' o 'dónde va esto' en contexto de vault o sistema editorial."
---

# INBOX-TRIAGE — Punto de Entrada del Flujo Editorial

**Regla de oro:** Fase 1 siempre antes de Fase 2. **TIENES ESTRICTAMENTE PROHIBIDO generar bloques YAML, crear archivos .md o mover archivos tú mismo.** Tu única función de escritura es invocar el script de Python con las variables que diagnosticaste.

---

## FASE 1 — DIAGNÓSTICO (automática)

Lee el archivo completo de principio a fin, sin editar, sin crear nada.

### 1.1 Identificar tipo de fuente

Clasifica en uno de estos cuatro tipos:

| Tipo | Señales clave |
|---|---|
| **Transcripción oral** | Oralidad marcada, repeticiones, muletillas, frases cortadas, "o sea", "¿verdad?", estructura no lineal |
| **Borrador escrito** | Párrafos estructurados, sin marcas de dictado, prosa deliberada aunque imperfecta |
| **Material académico** | Vocabulario técnico, aparato de citas, notas bibliográficas, estructura formal |
| **Referencia externa** | Artículo, capítulo de libro, fragmento de tercero — no es voz de Daniel |

Si el archivo **mezcla dos fuentes** (ej. transcripción oral + borrador escrito), clasificarlo como "Mixto".

### 1.2 Identificar dominio

- **Pastoral** — predicación, enseñanza bíblica, devocional, reflexión teológica aplicada
- **Académico** — ensayo de maestría, análisis exegético-académico, investigación formal

Si no es claro, anotar ambas posibilidades y preguntar a Daniel antes de avanzar.

### 1.3 Detectar MODO (1–7 o Académico)

Este es el paso nuevo del sistema. Lee el archivo completo y asigna uno de los 8 modos:

| Modo | Tipo | Señales de detección |
|---|---|---|
| **1 — Libro Terminado** | Libro completo | Estructura cerrada con capítulos, arco editorial completo, prosa pulida, revisado. |
| **2 — Libro Pre-Diseño** | Libro que necesita edición | Estructura presente pero borrador: transcripción oral mezclada, capítulos incompletos, anotaciones de trabajo. |
| **3 — Ideas Sueltas** | Sin estructura | Fragmentos, listas dispersas, apuntes sin arco. Sin argumento central claro. |
| **4 — Guía de Estudio** | Exegética versículo a versículo | Sigue orden de un texto bíblico, incluye preguntas de estudio, comentario exegético sección por sección. |
| **5 — Nota Temática** | Un tema, argumento cerrado | Desarrolla un solo concepto teológico. Referencia permanente. Argument central definido. |
| **6 — Estudio / Clase Larga** | Material de clase 1–3 h | Notas de maestro, apuntes de sesión, material largo para clase presencial. Puede incluir transcripción. |
| **7 — Grupos Conexión** | ~15 min, facilitado por otros | Corto, diseñado para que otra persona lo facilite. Incluye preguntas de discusión. Guía de facilitador. |
| **Académico** | Maestría / formal | Vocabulario técnico, citas bibliográficas, argumento formal. No es voz pastoral de Daniel. |

Si el modo no está claro después de leer, anotar las dos opciones más probables y preguntar.

### 1.4 Extraer metadatos clave

Del archivo, extraer sin inferir más de lo que el texto dice:

- **Título** — proponer uno si el archivo no tiene
- **Tema principal** — en una frase corta
- **Serie** — si el texto menciona o sugiere una serie o ciclo
- **Libro bíblico principal** — el libro con más protagonismo
- **Personajes bíblicos** — lista de personajes mencionados o desarrollados
- **Versículos citados** — lista exhaustiva de todas las referencias (formato: Gén. 3:15)
- **Temas principales** — 3 a 5 temas teológicos o conceptuales centrales
- **Author quotes** — autores o teólogos citados explícitamente (N.T. Wright, Tim Keller, etc.)
- **SEO keywords** — 4 a 6 términos de búsqueda
- **Fuente** — origen del archivo (dictado, grabación, borrador propio, clase, conferencia, paper)

### 1.5 Proponer ruta de destino

Basado en dominio, tipo y MODO:

| Modo | Carpeta de destino |
|---|---|
| 1 — Libro Terminado | `Temas/NN/01_Libros/` |
| 2 — Libro Pre-Diseño | `Temas/NN/01_Libros/` (con `fase: pre-diseno`) |
| 3 — Ideas Sueltas | `Temas/NN/04_NotasSinProcesar/` |
| 4 — Guía de Estudio | `Temas/NN/02_EsquemasDeClase/` |
| 5 — Nota Temática | `Temas/NN/` (raíz del tema) |
| 6 — Estudio / Clase (escrito) | `Temas/NN/02_EsquemasDeClase/` |
| 6 — Estudio / Clase (oral) | `Temas/NN/03_ClasesEnVivo/` |
| 7 — Grupos Conexión | `Temas/NN/02_EsquemasDeClase/grupos-conexion/` |
| Académico | `Temas/08_Academico/Maestria/` |
| Transcripción pendiente | `Inbox/pendiente-modo-ab/` (hasta procesar con modo-ab) |
| Referencia externa | `Temas/NN/05_MaterialExterno/` |

`NN` = número de tema (01–08). Si no es claro, proponer los dos más probables.

### 1.6 Derivación de skills

Indicar en el reporte qué skills deben activarse después, en orden:

- Ver CLAUDE.md §4 para tabla de enrutamiento por modo
- Señalar si `modo-ab` es necesario (material mixto o transcripción oral)
- Señalar si `modo-c` es recomendado (manuscrito con posibles huecos)
- Recordar que `zettelkasten-forge` y `pattern-harvester` siempre cierran el flujo

### 1.7 Presentar reporte de triage

Genera un objeto JSON compacto de una sola línea con los metadatos extraídos. Este JSON será el "payload" para la Fase 2.

**Formato del JSON requerido:**
`{"title": "...", "tipo": "...", "tema": "...", "libro_biblico_principal": "...", "personajes": [...], "versiculos_citados": [...], "temas_principales": [...], "seo_keywords": [...], "dominio": "...", "modo": "...", "serie": "...", "fuente": "...", "author_quotes": [...], "destino": "Ruta/Propuesta/Completa/"}`

Presenta el reporte a Daniel con este formato exacto:
```
── REPORTE DE TRIAGE HÍBRIDO ───────────────────────
Archivo: [nombre]
MODO DETECTADO: [N — Nombre del modo]
Ruta destino: [ruta/propuesta/]

Payload preparado:
`[Inserta aquí el JSON compacto en una sola línea]`
──────────────────────────────────────────────────────
¿Procedo con Fase 2 (Inyección Python)? (sí / no)
```

---

## FASE 2 — EJECUCIÓN HÍBRIDA (solo tras OK explícito)

Si Daniel responde "sí", "adelante" o da luz verde, **tu única acción** en esta fase es ejecutar el script de Python en la terminal utilizando el payload JSON que generaste en la Fase 1.

**Comando exacto a ejecutar:**
`python3 _Scripts/inbox_triage.py "Inbox/[nombre_del_archivo]" '[Copia_exacta_del_payload_JSON_de_la_Fase_1]'`

*Nota crítica: Asegúrate de que el JSON esté envuelto en comillas simples `' '` dentro del comando de terminal para evitar errores de sintaxis.*

Una vez que la terminal devuelva el mensaje de éxito de Python, confirma a Daniel que el archivo ha sido procesado y movido.```

---

## §Estructuras — Cuerpo de la nota

### Estructura pastoral (transcripción oral o borrador)

```markdown
## Resumen

[2–3 oraciones: tema central, tono, estado del texto — suficiente para decidir si vale leer el original]

## Archivo fuente

[[nombre-del-archivo-original]]

## Notas de triage

- Tipo detectado: [tipo]
- Dominio: pastoral
- Modo asignado: [N — Nombre]
- Próximo paso sugerido: [skills en orden]
```

### Estructura académica

```markdown
## Resumen

[2–3 oraciones: tesis del autor, argumento central, relevancia para la maestría]

## Archivo fuente

[[nombre-del-archivo-original]]

## Notas de triage

- Tipo detectado: [tipo]
- Dominio: académico
- Próximo paso sugerido: [notas-maestria / revisión directa]
```

### Estructura referencia externa

```markdown
## Ficha bibliográfica

- Autor:
- Título completo:
- Fuente / editorial:
- Año:
- Páginas relevantes:

## Archivo fuente

[[nombre-del-archivo-original]]

## Notas de lectura

[espacio vacío para que Daniel agregue sus observaciones]
```

---

## §Advertencias críticas

**Si es transcripción oral pastoral:**
⚠️ TRANSCRIPCIÓN ORAL: En Fase 2 no se modifica ninguna palabra del texto original. El triage solo crea el contenedor (YAML + estructura). Para editar el contenido, usar MODO A+B posteriormente.

**Si es material académico:**
ℹ️ DOMINIO ACADÉMICO: Se suspenden las 5 marcas de voz pastoral y el checklist de 11 puntos. Se aplica régimen neutral de escritura académica.

**Si es archivo mixto (dos fuentes):**
⚠️ ARCHIVO MIXTO: Se detectaron dos fuentes mezcladas. En Fase 2 se crea el contenedor pero no se toca el texto. Después de triage, usar MODO A+B para separar y procesar.

**Si el dominio no está claro:**
❓ DOMINIO AMBIGUO: El archivo podría ser pastoral o académico. ¿Confirmas el dominio antes de proceder?

**Si el modo no está claro:**
❓ MODO AMBIGUO: El archivo podría ser [Modo X] o [Modo Y]. Las principales diferencias son [explicar]. ¿Cuál aplica?

---

## §Reglas que nunca se rompen

1. **Nunca saltar de Fase 1 a Fase 2** sin respuesta afirmativa explícita de Daniel.
2. **Nunca modificar** el texto de una transcripción oral en ninguna fase — solo crear el contenedor.
3. **Nunca dejar el YAML incompleto** al cerrar — si un campo no tiene datos, dejar `""` o `[]`, nunca omitir.
4. **Nunca inventar versículos** — si el texto no cita un versículo, no agregarlo al YAML.
5. **Si el archivo es mixto**, señalarlo con claridad y programar MODO A+B después del triage.
6. **Si el dominio es académico**, no aplicar criterios de voz pastoral.
7. **Siempre indicar** los skills que vienen después (derivación por modo) en el reporte de Fase 2.
