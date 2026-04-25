---
name: notas-maestria
description: "Protocolo para notas académicas de maestría de Daniel Lira. Actívalo SIEMPRE que Daniel diga 'notas de maestría', 'procesa esta lectura', 'ficha académica', 'nota de clase', 'protocolo académico', 'régimen neutral', o cuando entregue material académico (artículo, capítulo, paper, lectura de curso) para convertir en nota de estudio. También actívalo cuando Daniel diga 'esto es para la maestría' o 'aplica el protocolo académico'. DISTINGUIR de MODO A+B (que es para texto pastoral de Daniel) y de inbox-triage (que solo clasifica). Este skill PRODUCE la nota completa con estructura fija. No aplica voz pastoral, no aplica las 5 marcas de Daniel, no aplica el checklist de 10 puntos — régimen neutral de escritura académica."
---

# NOTAS-MAESTRÍA — Protocolo de Nota Académica

**Principio rector:** Este protocolo opera en régimen neutral. No hay marcas de voz pastoral, no hay checklist de prosa literaria, no hay arco en tres tiempos. El criterio es claridad analítica, fidelidad al autor y utilidad para el trabajo académico de Daniel.

---

## FASE -1 — CARGAR ACTIVEPATTERNS

Leer `_Skills/activePatterns.json`.
Los patrones de scope `academico` (si existen) informan preferencias previas en notas académicas de Daniel.
Si no hay patrones académicos, continuar normalmente.

---

## FASE 0 — LECTURA COMPLETA

Lee el material completo antes de escribir una sola línea.

Responde internamente:
- ¿Cuál es la tesis central del autor?
- ¿Qué estructura argumental sigue?
- ¿Hay citas textuales que vale la pena preservar literalmente?
- ¿Hay tensiones o puntos débiles en el argumento?

No escribas la nota hasta haber leído todo.

---

## ESTRUCTURA FIJA — Las 6 secciones en orden

### 1. FICHA BIBLIOGRÁFICA

```
Autor(es): 
Título: 
Publicación / Editorial: 
Año: 
Páginas leídas: 
Tipo de fuente: [artículo / capítulo / libro / tesis / ponencia]
```

### 2. TESIS DEL AUTOR

Una sola oración, lo más precisa posible. Debe responder: ¿qué afirma el autor que es verdad y no trivialmente obvio?

Si el texto tiene múltiples argumentos, identificar la tesis principal y las sub-tesis en lista breve.

### 3. DESARROLLO DEL ARGUMENTO

Sigue la estructura del texto, no la temática. El objetivo es mostrar cómo el autor construye su argumento paso a paso.

Formato: prosa con subtítulos solo si hay secciones claramente delimitadas en el original. Sin bullets salvo que el autor mismo use listas.

Extensión: proporcional al material. No resumir en exceso — el objetivo es que Daniel pueda reconstruir el argumento sin releer el texto.

### 4. CITAS TEXTUALES CLAVE

Selecciona las 3 a 6 citas más importantes. Criterios para seleccionar:
- Define un concepto de manera que ninguna paráfrasis lo capture igual
- Es el momento donde el autor hace su afirmación más fuerte
- Es una frase que Daniel podría citar directamente en un paper

Formato:
```
> "Cita textual exacta entre comillas." (p. XX)

[Una línea explicando por qué esta cita es irreemplazable]
```

### 5. PARÁFRASIS Y SÍNTESIS

Reformula el argumento completo en palabras de Daniel — no del autor. Esta sección debe poder leerse de forma independiente de las anteriores.

No es un resumen del resumen. Es una reescritura activa que muestra comprensión profunda.

Dos reglas:
- No usar jerga que el autor no use (no proyectar vocabulario externo)
- Si hay algo que no quedó claro en la lectura, señalarlo con [PUNTO OSCURO: …]

### 6. REFLEXIÓN CRÍTICA Y PREGUNTAS ABIERTAS

Dos partes:

**Reflexión crítica** — 2 a 4 observaciones propias de Daniel:
- ¿Qué convence y por qué?
- ¿Qué no convence, o dónde el argumento parece débil?
- ¿Qué supone el autor sin demostrar?
- ¿Cómo dialoga esto con otras lecturas del curso o con el proyecto de tesis?

Estas observaciones van en primera persona de Daniel. Son genuinamente de él, no frases genéricas.

**Preguntas abiertas** — 2 a 5 preguntas que el texto deja sin resolver:
- Preguntas de investigación que el material suscita
- Tensiones con otros autores o marcos
- Vacíos metodológicos o empíricos

Formato:
```
1. ¿[Pregunta concreta que apunta a un problema real]?
```

---

## YAML — Plantilla académica

```yaml
---
título: ""
fecha: YYYY-MM-DD
dominio: academico
tipo_contenido: nota-maestria
autor_fuente: ""
título_fuente: ""
año_fuente: 
curso: ""
temas_principales:
  - ""
tesis_del_autor: ""
estado: en-proceso     # en-proceso | revisado | entregado | archivado
---
```

---

## REGLAS DE RÉGIMEN NEUTRAL

El régimen neutral significa que en este protocolo NO aplican:

- Las 5 marcas de voz pastoral de Daniel
- El checklist de 10 puntos de prosa literaria
- El arco en tres tiempos
- La regla de "no quitar nada" (aquí sí se parafrasea y sintetiza)
- Los campos bíblicos del YAML (libro_biblico_principal, versiculos_citados, personajes)

Lo que SÍ aplica:
- Precisión terminológica — usar los términos del autor tal como los usa el autor
- Fidelidad — no distorsionar el argumento aunque se esté en desacuerdo
- Distinción clara entre "lo que dice el autor" y "lo que piensa Daniel"
- YAML completo antes de cerrar la nota

---

## ENTREGA

La nota se entrega en tres pasos:

**Paso 1 — Chat primero.** Presentar la nota completa en chat. Daniel revisa, corrige, agrega. No crear archivo todavía.

**Paso 2 — Archivo al cerrar.** Cuando Daniel dé visto bueno, crear el archivo Markdown con YAML v2 y guardarlo en `08_Academico/Maestria/`.

Nombre del archivo: `YYYY-MM-DD-[apellido-autor]-[slug-tema].md`

El YAML debe incluir los campos v2 comunes: `dominio: academico`, `modo: academico`, `zettelkasten_notes: []`, `version_yaml: "2.0"`.

**Paso 3 — zettelkasten-forge (régimen neutral).** Al guardar el archivo, invocar `zettelkasten-forge` con instrucción:
```
"Material académico — aplicar régimen neutral. Las notas ZK generadas van a 09_Zettelkasten/academico/"
```
Las citas textuales clave (§4) son candidatas a notas de tipo `exegetica` o `conceptual`.
La sección de reflexión crítica (§6) genera notas de tipo `argumental` en primera persona de Daniel.
Luego `pattern-harvester` con scope académico.
