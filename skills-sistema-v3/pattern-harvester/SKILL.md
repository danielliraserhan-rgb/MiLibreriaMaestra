---
name: pattern-harvester
description: "Detecta y propone patrones recurrentes de voz, estructura y teología en el corpus de Daniel. Actívalo SIEMPRE como último paso del pipeline, después de zettelkasten-forge. Nunca mezcla patrones pastorales y académicos. Solo actualiza activePatterns.json con OK explícito de Daniel."
---

# PATTERN-HARVESTER — Detector de Patrones

**Posición en el pipeline:** siempre último. Después de zettelkasten-forge.

## FASE 1 — CARGAR ESTADO ACTUAL

Leer `_Skills/activePatterns.json`.

Registrar internamente:
- Cuántos patrones activos hay
- Sus scopes (pastoral / academico / ambos)
- Sus IDs (para evitar duplicados)

## FASE 2 — ANALIZAR MATERIAL

Leer el archivo fuente del pipeline actual.

Buscar candidatos a patrón en 3 categorías:

**Voz** — Giros sintácticos, estructuras de frase, ritmo característico que se repite.
Ejemplo: "pregunta retórica + respuesta teológica directa"

**Estructura** — Patrones de arco narrativo, secuencias argumentativas, transiciones recurrentes.
Ejemplo: "condición humana → silencio → irrupción de Dios"

**Teología** — Marcos doctrinales, énfasis hermenéuticos, referencias cruzadas recurrentes.
Ejemplo: "uso de NT para iluminar AT antes de interpretar el pasaje directo"

## FASE 3 — PROPONER CANDIDATOS

Para cada candidato, presentar:

```
PATRÓN CANDIDATO #N
Categoría: voz | estructura | teología
Scope: pastoral | academico
Nombre propuesto: [nombre corto]
Descripción: [una oración]
Evidencia: [citar 2-3 líneas del texto que lo muestran]
Notas ZK relacionadas: [IDs ZK-YYYYMMDD-HHMM-NNN donde aparece esta evidencia — dejar vacío si la evidencia viene del archivo fuente, no de notas ZK]
Frecuencia observada: [primera vez | segunda vez | recurrente]
```

**Regla de scope:** Un patrón pastoral NUNCA se propone para scope académico y viceversa, a menos que Daniel lo pida explícitamente.

Esperar respuesta granular de Daniel por cada candidato (puede aprobar, rechazar o pedir ajuste).

## FASE 4 — ACTUALIZAR ACTIVEPATTERNS.JSON

Solo tras OK explícito de Daniel por cada patrón aprobado.

Agregar al array `patterns` de `_Skills/activePatterns.json`:

```json
{
  "id": "P-YYYYMMDD-NNN",
  "nombre": "",
  "categoria": "voz | estructura | teologia",
  "scope": "pastoral | academico",
  "descripcion": "",
  "evidencia": [],
  "fecha_aprobacion": "YYYY-MM-DD",
  "sesion_origen": ""
}
```

## FASE 4.5 — ACTUALIZAR pattern_id EN NOTAS ZK

Para cada patrón aprobado: si el candidato tenía "Notas ZK relacionadas" con IDs, actualizar el campo `pattern_id:` de esas notas usando `obsidian-markdown`:

```yaml
pattern_id: P-YYYYMMDD-NNN
```

Si múltiples patrones aplican a la misma nota: agregar el ID como lista `[P-001, P-002]`.

## FASE 5 — ACTUALIZAR PROCESS_LOG

Agregar entrada en `_Skills/PROCESS_LOG.md`:

```
[YYYY-MM-DD] pattern-harvester — [N] patrones aprobados | [N] rechazados | archivo fuente: [nombre]
```
