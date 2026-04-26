# Skill: spaced-review

## Propósito
Revisar notas ZK vencidas usando SM-2. Combina rigor cognitivo (intervalos adaptativos) con reflexión teológica activa (pregunta contextual por nota).

## Activación
- Cron job diario (5:00 AM) vía `scheduled-tasks`
- Manual: Daniel escribe `/spaced-review`

---

## Flujo

### Paso 1 — Encontrar notas vencidas

```bash
python skills-sistema-v3/spaced-review/scripts/spaced_review.py \
  --vault /Users/danielliraserhan/Desktop/MiLibreriaMaestra—DanielLira \
  --mode queue
```

Output: JSON con máximo 5 notas. Prioridad:
1. `repeticiones: 0` — nunca revisadas
2. `fecha_proxima_revision <= hoy` — vencidas, más antiguas primero

Si no hay notas vencidas → informar a Daniel y terminar.

### Paso 2 — Presentar cada nota

Para cada nota en la cola:

1. Leer el archivo `.md` completo con `obsidian-markdown`
2. Mostrar a Daniel:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 NOTA [N/5] — [ID]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**[Título de la nota]**

[Primeros 150 palabras del cuerpo]

**Conexiones:** [[ZK-...]] · [[ZK-...]]
**Fuente:** [source_file]

❓ **Pregunta de hoy:**
[Ver §Generación de pregunta abajo]

¿Cómo te resultó? → 1 (olvidé) · 3 (bien) · 5 (fácil)
```

3. Esperar calificación de Daniel.

### Paso 3 — Calcular SM-2 y actualizar YAML

Con la calificación recibida:

```bash
python skills-sistema-v3/spaced-review/scripts/spaced_review.py \
  --mode calc \
  --intervalo [intervalo_dias actual] \
  --repeticiones [repeticiones actual] \
  --facilidad [facilidad actual] \
  --rating [1|3|5]
```

Output JSON: `{ "nuevo_intervalo": N, "nuevas_repeticiones": N, "nueva_facilidad": N, "fecha_proxima": "YYYY-MM-DD" }`

Actualizar el YAML de la nota con `obsidian-markdown`:
- `fecha_proxima_revision`: fecha calculada
- `intervalo_dias`: nuevo valor
- `repeticiones`: nuevo valor
- `facilidad`: nuevo valor

### Paso 4 — Generar archivo de sesión (opcional)

Si Daniel quiere registro, crear en `Inbox/`:

```
Review_Queue_[YYYY-MM-DD].md
```

Con la lista de notas revisadas, calificaciones y próximas fechas.

---

## Generación de pregunta de reflexión

La `pregunta_reflexion` guardada en el YAML es la pregunta base (generada por `zettelkasten-forge` al crear la nota).

Al revisar, Claude genera una **pregunta contextual fresca** combinando:
1. El campo `pregunta_reflexion` del YAML (ancla temática)
2. Los últimos patrones activos de `_Skills/activePatterns.json`
3. La fecha y contexto reciente (si hay entradas recientes en `_Skills/PROCESS_LOG.md`)

**Formato de pregunta contextual:**

> "Esta nota dice: *[afirmación central en una línea]*.
> [pregunta_reflexion base].
> Después de [referencia a trabajo reciente si existe], ¿esta idea se confirma, se matiza, o necesita revisión?"

**Dominio pastoral:** la pregunta conecta con predicación, ministerio o vida cristiana concreta.
**Dominio académico:** la pregunta conecta con el argumento del paper/clase y su vigencia.

---

## Algoritmo SM-2

| Rating | Intervalo nuevo | Repeticiones | Facilidad |
|--------|----------------|--------------|-----------|
| 1 (olvidé) | 1 día | reset → 0 | sin cambio |
| 3 (bien) | `round(intervalo × facilidad)` | +1 | sin cambio |
| 5 (fácil) | `round(intervalo × facilidad)` | +1 | +0.1 |

Reglas:
- `facilidad` mínima: 1.3
- `intervalo` mínimo: 1 día
- Primera revisión (repeticiones=0): intervalo → 1 independientemente
- Segunda revisión (repeticiones=1, rating≥3): intervalo → 6

---

## Responsabilidades de zettelkasten-forge

Al crear una nota ZK, `zettelkasten-forge` debe:
1. Llenar `fecha_proxima_revision` = `fecha_creacion` + 1 día
2. Generar `pregunta_reflexion`: una pregunta que interrogue la afirmación central de la nota desde el ministerio de Daniel. Ejemplos:
   - "¿Cómo cambia esta idea tu forma de predicar la gracia en contextos de fracaso?"
   - "¿Dónde has visto esta tensión actuar en tu congregación?"
   - "¿Qué versículo refutaría esta afirmación, y cómo responderías?"

---

## Archivos que modifica
- YAML de notas ZK revisadas (campos SM-2 únicamente)
- `Inbox/Review_Queue_[fecha].md` (opcional)

## Archivos que solo lee
- `_Skills/activePatterns.json`
- `_Skills/PROCESS_LOG.md`
- Notas ZK en `09_Zettelkasten/`
