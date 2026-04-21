# CLAUDE.md — MiLibreriaMaestra

> Las 5 marcas de voz, marcos teológicos, líneas rojas, checklist de 10 puntos
> y descripción de modos (A, B, C, R, E) están en el Contexto Maestro.
> Este archivo cubre solo arquitectura operativa.

## Estructura del Vault

**Dominio pastoral** — `Temas/01–07`:
`01_Origenes` · `02_HistoriaDeIsrael` · `03_Escatologia—Destino` · `04_ExegesisNT`
`05_DoctrinasFundamentales` · `06_DiscipuladoVidaCristiana` · `07_PredicacionesDevocionales`

Cada tema contiene: `01_Libros` / `02_EsquemasDeClase` / `03_ClasesEnVivo` / `04_NotasSinProcesar` / `05_MaterialExterno`

**Dominio académico** — `Temas/08_Academico/Maestria`:
`01_ArtículosAcadémicos` / `02_CasosDeEstudio` / `03_ForosDePreguntas` / `04_Exámenes` / `05_NotasDeClasePorMi` / `06_NotasDeClasePorElProfesor`

**Sistema**: `Inbox/` · `Templates/` · `ContextoMaestro/` · `MapasDeContenido—MOCs/` · `_Skills/` · `Assets/`

---

## Flujo de Inbox

**Fase 1 — Diagnóstico** (automático, sin crear nada):
Leer el archivo → identificar tipo, dominio, tema probable, estado del texto → presentar diagnóstico a Daniel. Esperar aprobación.

**Fase 2 — Procesamiento** (solo con OK explícito de Daniel):
Crear nota en carpeta correcta → completar YAML → aplicar estructura → mover original.

---

## Plantilla YAML

```yaml
---
title: ""
tipo: ""            # libro | esquema | clase_en_vivo | notas_sin_procesar | material_externo | articulo_academico
tema: ""            # 01_Origenes | 02_HistoriaDeIsrael | ... | 08_Academico
libro_biblico_principal: ""
personajes: []
versiculos_citados: []
temas_principales: []
seo_keywords: []
fecha: ""
estado: ""          # sin_procesar | en_proceso | completado
---
```

---

## Mapa de Skills

| Situación | Skill |
|---|---|
| Nuevo archivo en inbox | `inbox-triage` |
| Texto pastoral: oral + escrito, o borrador limpio | `modo-ab-seccion-mixta` |
| Diagnóstico / mapa estructural | `modo-c-esquema-editorial` |
| Hueco estructural, buscar material de referencia | `modo-r-material-referencia` |
| Esquema para clase / enseñanza | `modo-e-unificado` |
| Lectura académica / nota de maestría | `notas-maestria` |

---

## Control de Tokens

Al llegar al **70% del contexto** de la sesión, avisar: *"Estamos al 70% del contexto. Considera abrir una nueva sesión para no perder continuidad."*
