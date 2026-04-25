---
name: zettelkasten-forge
description: "Genera notas atómicas Zettelkasten a partir de contenido procesado. Actívalo después de modo-ab, modo-e, modo-c, inbox-triage, o notas-maestria — cuando el pipeline del modo lo requiera. Produce notas ZK con IDs canónicos (ZK-YYYYMMDD-HHMM-NNN), wikilinks, YAML v2 completo, y campo coaching_notes para loops con S2. Nunca guarda notas sin OK explícito de Daniel."
---

# ZETTELKASTEN-FORGE — Generador de Notas Atómicas

**Principio:** Una idea = una nota. Granular, enlazada, permanente.

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
ZK-YYYYMMDD-HHMM-NNN
Título: [título atómico — una sola idea]
Idea central: [una oración]
Wikilinks sugeridos: [[nota1]] [[nota2]]
Dominio: pastoral | academico
```

Presentar TODAS las propuestas antes de crear cualquiera.
Esperar OK de Daniel (puede aprobar todas, algunas, o pedir cambios).

## FASE 3 — CREAR NOTAS APROBADAS

Solo tras OK explícito de Daniel.

Usar `obsidian-markdown` para crear cada nota con este formato:

```yaml
---
id: ZK-YYYYMMDD-HHMM-NNN
title: ""
tipo: zettelkasten
dominio: pastoral | academico
tema: ""
libro_biblico_principal: ""
temas_principales: []
versiculos_citados: []
fuente: ""            # ID del archivo fuente (título o ruta)
coaching_notes: []    # IDs de sesiones de writing-coach que usaron esta nota
zettelkasten_notes: []
fecha: ""
version_yaml: "2.0"
fecha_actualizacion: ""
---
```

Carpeta destino:
- Pastoral: `09_Zettelkasten/pastoral/`
- Académico: `09_Zettelkasten/academico/`

## FASE 4 — ACTUALIZAR FUENTE

Agregar los IDs de las notas ZK creadas al campo `zettelkasten_notes:` del archivo fuente.

---

**Regla de dominio:** Notas pastorales y académicas no se enlazan entre sí salvo aprobación explícita de Daniel.
