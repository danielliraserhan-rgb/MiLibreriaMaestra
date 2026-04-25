---
name: modo-e-unificado
description: "Generador de esquemas para enseñanza"
---

---
name: modo-e-unificado
description: "Produce esquemas de enseñanza jerárquicos (MODO E) para Daniel Lira. Úsalo SIEMPRE que Daniel pida: 'esquema estilo Efesios', 'esquema estilo Panorama', 'manual de estudio', 'andamiaje didáctico', 'MODO E', 'estructura esto para enseñarlo', 'destila este libro a clase', o cuando entregue un pasaje/libro/tema y quiera organizarlo para enseñar o como referencia personal. También úsalo cuando diga 'prepárame el esquema de [libro o tema]' aunque no mencione MODO E explícitamente, si el contexto es docente o de preparación de clase. DISTINGUIR de MODO C (diagnóstico editorial): si el material ya está escrito y Daniel quiere saber qué falta o qué mover, es MODO C. Si quiere enseñarlo o tenerlo como referencia, es MODO E. Cuando no esté claro, preguntar."
---

# MODO E — Esquema de enseñanza

Materiales de referencia canónicos: *Efesios, Manual de Estudio* · *Panorama escatológico 2024*

---

## 0. Cargar activePatterns

Leer `_Skills/activePatterns.json` al inicio.
Los patrones de scope `estructura` pueden informar cómo Daniel organiza sus clases (ej. "siempre abre con personaje bíblico antes de doctrina"). Aplicar al construir la intro discursiva del esquema.

---

## 1. Tres ejes de decisión antes de construir

Antes de escribir una sola línea, resolver estos tres ejes en orden:

### Eje 1 — ¿MODO C o MODO E?

Si Daniel entrega un manuscrito ya escrito, preguntar explícitamente.
- MODO C = diagnóstico editorial ("¿qué me falta?")
- MODO E = esquema para enseñar ("¿cómo lo enseño?")

### Eje 2 — ¿Material completo o incompleto?

**Material incompleto** *(notas, transcripciones, ideas dispersas)*
→ Operación: **construir** el esquema desde esos fragmentos.
→ Si no hay fuente: detenerse y pedir. Nunca generar teología propia.
> *"Antes de construir el MODO E sobre [tema], necesito tu material fuente — notas, predicaciones previas, esquema de clase. Sin eso construiría teología propia, no la tuya. ¿Qué tienes?"*
→ Si el material es disperso: diagnóstico MODO R primero.

**Material completo** *(manuscrito o libro terminado)*
→ Operación: **extraer** — destilar a esquema navegable para dar clase sin abrir el libro.
→ Confirmar que la operación es extracción, no reescritura.

### Eje 3 — ¿Jerarquía bíblica o jerarquía temática?

| | **Variante bíblica** | **Variante temática** |
|---|---|---|
| Bullet L1 | `Gén. 3:15 — la simiente aplastará la serpiente` | `El Protoevangelio: primera promesa del Mesías (Gén. 3:15)` |
| Versículo | Es el encabezado del bullet | Va entre paréntesis al final del L1 |
| Cuándo | Libros narrativo-bíblicos secuenciales | Libros temáticos, clases conceptuales |
| Referencia canónica | Efesios, Manual de Estudio | Panorama escatológico 2024 |

**Señales para elegir:**

→ Variante bíblica: "esquema estilo Efesios", material que sigue el orden del texto, el versículo es el evento principal.
→ Variante temática: "organiza por ideas", "versículos como apoyo", "libro temático", el patrón importa más que el evento.
→ Si no está claro: preguntar.

---

## 2. Arquitectura obligatoria — 7 elementos en orden

Los 7 elementos aplican a **ambas variantes**. Lo que cambia es la lógica del cuerpo en bullets (§3 y §4).

### 2.1 Encuadre macro

Bloque inicial que ubica al lector en el mapa completo. Incluye:
- Contexto / ¿qué es y qué no es?
- Qué se lleva el lector
- División estructural en secciones mayores (tabla)

### 2.2 Intro discursiva por capítulo/sección

**En prosa, no en bullets.** Máximo 3 líneas. Voz pastoral-didáctica (ver §6).
- Material incompleto → Claude redacta en voz de Daniel.
- Material terminado → **extraer del libro por defecto.**

### 2.3 Subsecciones con título

- **Variante bíblica:** `**· Título ·**` con puntos medios + subtítulo en cursiva
- **Variante temática:** título en negrita sin puntos medios, mismo nivel tipográfico

### 2.4 Cuerpo en bullets jerárquicos

Ver §3 (bíblica) y §4 (temática).

### 2.5 Remates intercalados

Frase en negrita que marca el latido del capítulo. No es cierre final — **va intercalada, mínimo 2 veces por capítulo mayor.**
- Material terminado: extraer del libro, literal.
- Si el libro no tiene la frase: marcar hueco y preguntar.

### 2.6 Bloques de recapitulación

Al cierre de capítulos mayores:
- Lista numerada de puntos clave
- Tabla de síntesis cuando hay patrón repetido (ej. cuatro caídas, expectativa mesiánica)

### 2.7 Apéndice técnico (condicional)

Incluir **solo si el material lo requiere**: términos griegos/hebreos, paralelos bíblicos densos, contexto histórico-calendárico. Si el libro es devocional/aplicado: no incluir.

---

## 3. Cuerpo en bullets — Variante bíblica

### Estructura

```
● [Versículo o referencia] — Afirmación
  ○ Exégesis breve
  ○ Implicación teológica
    ■ Subnota técnica si aplica
```

**Regla clave:** todo bullet L1 va anclado a versículo o referencia. Sin ancla, no va como bullet de cuerpo — va en bloque de síntesis o remate.

### Longitud
- L1: versículo + afirmación breve. La afirmación ≤ 8 palabras.
- L2: una cláusula. Máximo 10 palabras.
- L3: detalle técnico o cita. Máximo 8 palabras.

### Reglas de extracción (material terminado)
1. Todo sale del libro. No agregar teología propia.
2. Prosa larga → bullet padre + 2-3 sub-bullets. Preservar palabras clave del libro.
3. Voz preservada: si el libro usa "nosotros", el esquema usa "nosotros".
4. Remates extraídos literales.
5. Sin apéndice técnico si el libro no lo tiene.

**Material que sobra:** señalar al final en "Material del libro no incluido."
**Material que falta:** no inventar. Señalar el hueco y preguntar.

### Trazabilidad `[Cap. X]`
Agregar solo en: zonas densas (1 cap. del esquema destila 2+ del libro), referencias cruzadas, paralelos temáticos no obvios.

---

## 4. Cuerpo en bullets — Variante temática

### Estructura

```
● Etiqueta o máxima — idea o patrón (Ref.)
  ○ Desarrollo de la idea
  ○ Cita directa en cursiva
    ■ Detalle técnico o conexión intertextual
```

### Regla C — dos tipos de bullet L1

**Tipo B — Etiqueta nominal** (para conceptos específicos anclados a un pasaje):
- Corta, nominal, ≤ 7 palabras + referencia entre paréntesis al final
- Ejemplos: `El Sabbat (Gén. 2:1-3)`, `El jardín del Edén: primer templo (Gén. 2:7-8)`

**Tipo A — Máxima / principio** (para patrones transversales sin ancla única):
- Frase que expresa el patrón completo, sin referencia o con referencia múltiple
- Ejemplos: `La semilla no muere — Dios la resucita`, `Gracia: no ausencia de proceso, sino presencia en él`

**Cuándo usar cada tipo:**
- Tipo B → el concepto se origina en un pasaje específico
- Tipo A → el patrón atraviesa múltiples textos o es implicación teológica

La mezcla deliberada de ambos tipos (Regla C) es lo que hace el esquema navegable y denso a la vez. No forzar todo a un solo tipo.

### Longitud
- L1: ≤ 8 palabras (sin contar la referencia)
- L2: una cláusula, máximo 12 palabras
- L3: detalle técnico, máximo 10 palabras

### Referencias bíblicas
- **Solo en L1** — nunca en L2 ni L3
- Formato: `(Gén. 3:15)` — paréntesis, tamaño menor, sin negrita
- Patrón que atraviesa varios textos: `(Gén. 4:26 → Apoc. 22:20)`

---

## 5. Formato de documento .docx — fiel al Panorama

Aplica a **ambas variantes**. El Panorama escatológico 2024 es la referencia tipográfica.

### Tipografía
- Fuente única: **Georgia** en todo el documento — cuerpo, títulos, bullets, tabla
- Color único: **negro puro `#000000`** — sin azules, dorados ni grises en texto
- Sin bordes decorativos en títulos de sección
- Sin encabezado de página (solo pie)

### Títulos
| Elemento | Tamaño | Estilo | Espaciado |
|---|---|---|---|
| Título de sección mayor | 15pt | Negrita | before 360 / after 120 |
| Subsección | 12pt | Negrita | before 240 / after 80 |
| Sub-subsección | 11pt | Negrita itálica | before 180 / after 60 |
| Cuerpo / intro | 11pt | Normal | after 120 |
| Remate | 11.5pt | Negrita | before 120 / after 120 |

### Bullets — sangría exacta del Panorama
| Nivel | Símbolo | Fuente símbolo | Sangría izq. | Hanging |
|---|---|---|---|---|
| L1 ● | `\u2022` | Symbol | 480 | 280 |
| L2 ○ | `\u006F` | Courier New | 1440 | 280 |
| L3 ■ | `\u25A0` | Arial | 2160 | 280 |

### Pie de página
Itálica izquierda: `Título · Daniel Lira · Año`

### Separadores
Línea gris `#CCCCCC`, grosor 1pt — solo entre subsecciones grandes, máximo 1 por sección mayor.

### Scaffold JS (numbering)
```javascript
{ reference: 'b1', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022',
    style: { paragraph: { indent: { left: 480, hanging: 280 } },
             run: { font: 'Symbol', size: 22, color: '000000' } } }] },
{ reference: 'b2', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u006F',
    style: { paragraph: { indent: { left: 1440, hanging: 280 } },
             run: { font: 'Courier New', size: 21, color: '000000' } } }] },
{ reference: 'b3', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u25A0',
    style: { paragraph: { indent: { left: 2160, hanging: 280 } },
             run: { font: 'Arial', size: 20, color: '000000' } } }] },
```

Helper para referencia inline (variante temática):
```javascript
function ref(text) {
  return new TextRun({ text: ` (${text})`, font: 'Georgia',
                       size: 19, bold: false, color: '000000' });
}
```

### Audit antes de entregar
```python
colors = set(re.findall(r'<w:color w:val="([^"]+)"', xml))
# Debe ser: {'000000'} — si hay otro color, corregir antes de entregar
```

---

## 6. Voz pastoral-didáctica — intros discursivas

**Sí aplican:**
- *Nosotros* — la intro convoca, no dicta. Nunca tono acusatorio.
- Entrada por pregunta universal, personaje o escena.

**No aplican en intro:**
- Arco en tres tiempos — lo hace el capítulo entero.
- Remate corto — lo hacen los bloques intercalados.

**Arranques válidos:**
- Por pregunta: *"¿Para qué? ¿Cuál es el punto de todo esto?"*
- Por recapitulación: *"Vimos en Efesios 2 cómo, por su gracia, nos dio una nueva identidad."*
- Por escena: *"Éfeso era la ciudad más importante de Asia menor."*

**Arranques inválidos:**
- ❌ Definición doctrinal en frío: *"La escatología es el estudio de los eventos finales…"*
- ❌ Meta-comentario: *"En este capítulo vamos a estudiar…"*
- ❌ Tono acusatorio: *"El lector debe entender que…"*

---

## 7. Checklist antes de entregar

Si 2+ fallan en cualquier sección, corregir antes de entregar el .docx.

**Base (ambas variantes):**
1. ¿El encuadre macro está al inicio con tabla de estructura?
2. ¿Cada capítulo abre con intro en prosa (≤ 3 líneas), no en bullets?
3. ¿Las intros entran por pregunta/personaje/escena y usan *nosotros*?
4. ¿Hay al menos 2 remates intercalados por capítulo mayor?
5. ¿Las tablas de síntesis están donde hay patrón repetido?
6. ¿El apéndice técnico aparece solo donde el material lo requiere?
7. ¿El audit de color devuelve solo `000000`?

**Variante bíblica — adicionales:**
8. ¿Todo bullet L1 está anclado a versículo o referencia?
9. ¿Todo el contenido sale del libro, sin teología propia?
10. ¿La trazabilidad `[Cap. X]` aparece solo en zonas densas o cruzadas?

**Variante temática — adicionales:**
8. ¿Todos los L1 son ≤ 8 palabras (sin la referencia)?
9. ¿Las referencias bíblicas están solo en L1, nunca en L2/L3?
10. ¿Se aplicó la Regla C (mezcla Tipo A y Tipo B)?
11. ¿Ningún bullet supera 15 palabras?
12. ¿No hay frases repetidas entre secciones?

---

## 8. Flujo de entrega — tres pasos obligatorios

**Paso 1 — Chat primero.** Entregar el esquema en chat. Daniel edita, corta, reordena, marca huecos. Nunca ir directo a .docx.

**Paso 2 — .docx al cerrar.** Cuando Daniel dé visto bueno ("cerrar", "pásalo a docx", "listo"), generar .docx respetando el formato del §5.

**Paso 3 — zettelkasten-forge + pattern-harvester.** Al entregar el .docx, invocar `zettelkasten-forge` sobre el esquema aprobado. Los remates intercalados (§2.5) y las máximas/afirmaciones del esquema son candidatos naturales a notas de tipo `argumental` y `conceptual`. Luego cerrar con `pattern-harvester`.

---

## 9. Distinción rápida con otros modos

| Modo | Input | Salida | Cuándo |
|---|---|---|---|
| **A** | Transcripción oral | Transcripción con estructura literaria | Material dictado/grabado |
| **B** | Borrador escrito | Análisis + alternativas de redacción | Mejorar prosa de libro |
| **C** | Manuscrito existente | Mapa editorial con diagnóstico | "¿Qué me falta?" |
| **R** | Material externo | Diagnóstico de utilidad | Referencia de otro proyecto |
| **E bíblico** | Pasaje/libro + fuente | Esquema didáctico anclado a versículos | Libros narrativo-bíblicos |
| **E temático** | Libro/tema + fuente | Esquema didáctico anclado a ideas | Libros temáticos/conceptuales |

---

## 10. Firma

Pie de todo esquema MODO E:

```
Daniel Lira — [Año]
```

Si es parte de serie/proyecto:

```
[Nombre del proyecto] · Módulo [N]