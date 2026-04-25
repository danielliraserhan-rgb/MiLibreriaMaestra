---
name: modo-c-esquema-editorial
description: "Skill de Diagnostico, antes llamado MODO C para el editor profesional de Daniel Lira. Usar cuando Daniel pida \"el esquema\", \"el mapa\", \"el panorama\" o \"análisis editorial\" de una sección o capítulo de Orígenes Ed.2 u otro libro. También activar cuando pida \"diagnóstico\", \"dónde está el argumento\" o \"qué falta\" en un bloque de texto. Este skill produce el desglose estructural completo por sección más una VISTA GENERAL al final. Siempre usar este skill antes de proponer correcciones de fondo o restructuraciones en Scrivener. No usar si el propósito es didáctico o para dar clase — ese es MODO E."
---

---
name: modo-C-esquema-editorial
description: "Esquema editorial completo + detección automática de huecos tanmbien llamado MODO DIAGNOSTICO"
---

# MODO DIAGNÓSTICO — Mapa Editorial

## Paso 0 — Cargar activePatterns

Leer `_Skills/activePatterns.json` al inicio.
Los patrones de scope `estructura` informan qué patrones de organización ya están documentados — úsalos para afinar el diagnóstico de huecos (no proponer como hueco algo que ya es patrón deliberado de Daniel).

---

## Paso 1 — Lectura completa
Lee todo antes de analizar.

## Paso 2 — Desglose por sección
Para cada bloque entrega las 7 fichas:  
- Idea central  
- Puerta de entrada  
- Arco (tres tiempos)  
- Remate corto  
- Hilo conductor  
- Patrones repetidos  
- Diagnóstico (máximo 3 líneas)

## Paso 3 — Vista general
Hilo conductor global, piezas sin lugar, huecos, candidatos a mover/cortar, fortalezas.

En esta sección agregar también:
**Candidatos a nota atómica Zettelkasten:**
Lista las 3–5 ideas más densas o autónomas detectadas durante el diagnóstico. No genera las notas aquí — sólo las señala para que `zettelkasten-forge` las use de referencia.

**Al finalizar:** actualizar YAML v2 completo (incluyendo `author_quotes`, `fecha_actualizacion`) y mover archivo a carpeta correcta.

---

## Paso 4 — Derivar a zettelkasten-forge (siempre al cerrar modo-c)

Al completar el diagnóstico, indicar a Daniel:
```
Diagnóstico completo. Activando zettelkasten-forge para generar propuestas de notas atómicas a partir de los candidatos detectados.
```

Invocar `zettelkasten-forge`. Luego `pattern-harvester`.