---
title: Dashboard — Revisión Espaciada ZK
tipo: dashboard
---

# Dashboard — Revisión Espaciada

## Notas vencidas hoy

```dataview
TABLE titulo, fecha_proxima_revision, repeticiones, facilidad, dominio
FROM "09_Zettelkasten"
WHERE tipo = "zettelkasten" AND fecha_proxima_revision <= date(today)
SORT fecha_proxima_revision ASC
LIMIT 20
```

## Nunca revisadas

```dataview
TABLE titulo, fecha_creacion, dominio, subtipo
FROM "09_Zettelkasten"
WHERE tipo = "zettelkasten" AND repeticiones = 0
SORT fecha_creacion ASC
LIMIT 20
```

## Próximas (7 días)

```dataview
TABLE titulo, fecha_proxima_revision, intervalo_dias, repeticiones
FROM "09_Zettelkasten"
WHERE tipo = "zettelkasten" AND fecha_proxima_revision > date(today) AND fecha_proxima_revision <= date(today) + dur(7 days)
SORT fecha_proxima_revision ASC
```

## Estadísticas del vault ZK

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total notas",
  length(filter(rows, (r) => r.repeticiones = 0)) AS "Sin revisar",
  length(filter(rows, (r) => r.fecha_proxima_revision <= date(today))) AS "Vencidas hoy"
FROM "09_Zettelkasten"
WHERE tipo = "zettelkasten"
GROUP BY true
```
