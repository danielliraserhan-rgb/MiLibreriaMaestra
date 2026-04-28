# PROCESS LOG — MiLibreriaMaestra

> Bitácora append-only. Nunca borrar entradas existentes.
> Una entrada por archivo procesado. Formato fijo.
> Actualizado automáticamente por `pattern-harvester` al cerrar cada sesión.

---

## Formato de entrada

```markdown
### YYYY-MM-DD — MODO N (Tipo) — "Título del archivo"

**Archivo:** Temas/.../nombre-del-archivo.md
**Skills ejecutados:** inbox-triage → [skills del modo] → zettelkasten-forge → pattern-harvester
**Metadatos extraídos:**
- Temas principales: [lista]
- Libros bíblicos: [lista]
- Autores citados: [lista]
- Versículos clave: [lista]

**Notas Zettelkasten generadas:** N (ZK-YYYYMMDD-HHMM-001 a ZK-YYYYMMDD-HHMM-NNN)

**Patrones detectados (pattern-harvester):**
1. [Patrón detectado] ([scope: estructura | voz | teología])
2. [Patrón detectado]

**Propuestas:**
- [ ] Patrón 1 — PENDIENTE
- [ ] Patrón 2 — PENDIENTE

**Resolución:** [se rellena al aprobar/rechazar]
```

---

<!-- Las entradas reales van debajo, en orden cronológico -->

### 2026-04-23 — MODO 1 (Libro Terminado) — "Nacer de Nuevo"

**Archivo:** `Temas/05_DoctrinasFundamentales/01_Libros/Nacer de Nuevo.md`
**Archivos fuente:** `Inbox/Nacer de nuevo Libro Digital.pdf` · `Inbox/Nacer de Nuevo_ Versión Final tamaño carta.docx`
**Skills ejecutados:** inbox-triage → zettelkasten-forge → pattern-harvester (pendiente)
**Metadatos extraídos:**
- Temas principales: Nuevo nacimiento, Doctrina de los Bautismos, Mikveh hebreo, Cuatro bautismos, Naturaleza corrupta y pecado, Expiación y propiciación, Identidad en Cristo, Bautismo en agua, Bautismo en el Espíritu Santo, Fe activa y obediencia
- Libros bíblicos: Juan, Génesis, Éxodo, Levítico, Jeremías, Salmos, Mateo, Hechos, Romanos, 1-2 Corintios, Gálatas, Efesios, Colosenses
- Autores citados: Luis Ortiz, Rodrigo Weigend
- Versículos clave: Juan 3:16-21, Génesis 1:26, Efesios 2:10, Efesios 1:3-14, Romanos 5:12-21, Gálatas 2:20, 2 Corintios 5:17-20, Hechos 8:30-38

**Notas Zettelkasten generadas:** 22 (ZK-20260423-1200-001 a ZK-20260423-1200-022)

**Patrones detectados (pattern-harvester):** 8 propuestos · 3 aprobados

**Propuestas:**
- [x] P-006 — La tríada como estructura de completitud — APROBADO (sugerencia al detectar pares)
- [ ] P-001 — El remate de golpe — RECHAZADO (ya cubierto en ContextoMaestro §4.5)
- [ ] P-002 — "Pero Dios" como bisagra — RECHAZADO
- [ ] P-003 — La objeción anticipada — RECHAZADO
- [ ] P-004 — El personaje como espejo del lector — RECHAZADO
- [ ] P-005 — Definición en negativo antes del positivo — RECHAZADO
- [x] P-007 — Diseño → corrupción → restauración — APROBADO (alternativa al arco de 3 tiempos)
- [x] P-008 — Identidad antes de conducta — APROBADO (corrección ante tono acusatorio o sin base teológica)

**Resolución:** Completado 2026-04-23. 3 patrones activos en activePatterns.json v1.1

---

### 2026-04-24 — MODO 6 (Clase Larga) — "En los días de Noé"

**Archivo:** `Temas/03_Escatologia—Destino/02_EsquemasDeClase/2026-04-24-en-los-dias-de-noe.md`
**Archivos fuente:** notas de predicación (borrador escrito)
**Skills ejecutados:** inbox-triage → modo-e → zettelkasten-forge → pattern-harvester
**Metadatos extraídos:**
- Temas principales: Reino de Dios, Regreso de Cristo / escatología, Urgencia misionera, Santidad y separación del mundo, Identidad en Cristo
- Libros bíblicos: Lucas, Marcos, Génesis, 1 Pedro
- Personajes: Noé, Lot, Jesús, apóstoles
- Versículos clave: Marcos 1:14, Marcos 1:17-18, Génesis 6:11-13, Lucas 17:20-21, Lucas 17:26-30, 1 Pedro 1

**Notas Zettelkasten generadas:** 8 (ZK-20260424-1628-001 a ZK-20260424-1628-008)

**Patrones detectados (pattern-harvester):** 2 aprobados

**Propuestas:**
- [x] P-009 — El tipo del AT como espejo del momento presente — APROBADO (hermenéutica)
- [x] P-010 — La frustración personal como umbral de revelación teológica — APROBADO (estructura/voz)

**Resolución:** Completado 2026-04-24. 5 patrones activos en activePatterns.json v1.1

---

### 2026-04-27 — SESIÓN DE AUDITORÍA Y MANTENIMIENTO DEL SISTEMA

**Tipo:** Mantenimiento · No procesamiento de archivo nuevo
**Ejecutado por:** Claude Code (6 sub-agentes de auditoría + correcciones directas)

---

#### BUGS CORREGIDOS (aplicados automáticamente)

**1. CLAUDE.md §8 — Error de conteo**
- Corregido: "8 prohibiciones" → "9 prohibiciones" (línea 177)
- Impacto: el coach ahora revisa las 9 líneas rojas del ContextoMaestro

**2. spaced_review.py — Fórmula SM-2 incorrecta (línea 94)**
- Corregido: `facilidad + (0.1 if rating == 5 else 0.0)` → fórmula SM-2 estándar con decremento por rating < 5
- Impacto: las notas difíciles ahora se programan con más frecuencia correctamente

**3. spaced_review.py — Crash potencial con YAML inválido (línea 159)**
- Corregido: `int()` envuelto en `try/except (ValueError, TypeError)`
- Impacto: frontmatter corrupto ya no crashea el script

**4. scan_vault.py — generate_index() producía índice vacío (línea 491)**
- Corregido: fallback de `fm.get("tema")` a `fm.get("temas_principales")[0]`
- Impacto: `--mode index` ahora agrupa documentos correctamente

---

#### DECISIONES DE DANIEL — APLICADAS

**A1 — Obsidian Sync deshabilitado**
- `.obsidian/core-plugins.json`: `"sync": true` → `"sync": false`
- Razón: conflicto con `obsidian-git` (ambos activos simultáneamente)
- obsidian-git queda como único sistema de versionado

**B1 — Upgrade masivo YAML v2 en 30 notas ZK**
- 22 notas ZK-20260423-1200-* ya tenían upgrade completo (procesadas en sesión anterior)
- 8 notas ZK-20260424-1628-* upgradeadas con 16 campos nuevos cada una:
  - Campos YAML v1 agregados: `title`, `tema`, `libro_biblico_principal`, `versiculos_citados`, `temas_principales`, `seo_keywords`, `fecha`, `estado`
  - Campos YAML v2 agregados: `modo`, `version_yaml: "2.0"`, `fecha_actualizacion`
  - Campos SM-2 agregados: `fecha_proxima_revision`, `intervalo_dias`, `repeticiones`, `facilidad`, `pregunta_reflexion`
- Todas las 30 notas ahora cumplen el contrato YAML v2 de CLAUDE.md §6

**C1 — MOC files generados (8 archivos)**
- `Temas/05_DoctrinasFundamentales/MOC_Doctrinas.md` — 22 ZK enlazados, 1 fuente
- `Temas/03_Escatologia—Destino/MOC_Escatologia.md` — 8 ZK enlazados, 1 fuente
- `Temas/08_Academico/Maestria/MOC_Maestria.md` — 2 fuentes académicas enlazadas
- Temas 01, 02, 04, 06, 07 — MOC mínimos creados (sin contenido procesado aún)

**D2 — Normalización zettelkasten_notes**
- `Temas/05_DoctrinasFundamentales/01_Libros/Nacer de Nuevo.md`
- Formato: `"ZK-..."` → `"[[ZK-...]]"` (wiki-links para navegación en Obsidian)
- Los 22 IDs normalizados

**E1 — Bifurcación académica en writing-coach**
- `skills-sistema-v3/writing-coach/SKILL.md`
- FASE 2 dividida en: FASE 2-P (pastoral, 5 categorías originales) y FASE 2-A (académica, 5 categorías neutrales)
- Ahora el coach no aplica criterios pastorales a textos académicos

**F1 — Sección .docx eliminada de modo-e-unificado**
- `skills-sistema-v3/modo-e-unificado/SKILL.md`
- Eliminados: frontmatter duplicado + sección "## 5. Formato de documento .docx" (61 líneas)
- Razón: herramienta de creación .docx no definida; la sección era referencia no ejecutable

**G2 — DOCX original eliminado de Inbox**
- `Inbox/Naked but not ahsamedExegetical Paper OT DBU.docx` eliminado
- El archivo ya estaba procesado en `Temas/08_Academico/Maestria/01_ArtículosAcadémicos/`

---

### 2026-04-28 — MODO 5 (Nota Temática) — "How and when did you come to faith in Jesus"

**Archivos creados:**
- `Temas/06_DiscipuladoVidaCristiana/04_NotasSinProcesar/2026-04-28-how-and-when-did-you-come-to-faith-in-jesus.md`
- `Temas/06_DiscipuladoVidaCristiana/04_NotasSinProcesar/2026-04-28-como-y-cuando-llego-a-la-fe-en-jesus.md`

**Skills ejecutados:** modo-selector → inbox-triage → zettelkasten-forge → pattern-harvester
**Metadatos extraídos:**
- Temas principales: conversión, búsqueda de verdad, islam y new age como caminos vacíos, identidad en Cristo
- Libros bíblicos: Juan
- Autores citados: John MacArthur (Study Bible), "El desconocido en el camino a Emaús"
- Versículos clave: Juan 4:26

**Notas Zettelkasten generadas:** 8 (ZK-20260428-1000-001 a ZK-20260428-1000-008)

**Patrones detectados (pattern-harvester):**
1. P-011 — Todo se cae, solo Cristo se sostiene (estructura)
2. P-012 — La pregunta que nombra el problema exacto (voz)
3. P-013 — Durante todo este tiempo era Él quien me hablaba (teologia)
4. P-014 — Imagen física para una crisis (voz)

**Resolución:** 4 aprobados, 0 rechazados

**Notas:**
- Documento original bilingüe (EN + ES) dividido en dos notas enlazadas entre sí
- Conversión desde .docx via markitdown[docx]; fuente eliminada tras verificación
- Skill conversion-documentos confirmado presente en main

---

#### PROBLEMAS DOCUMENTADOS (sin acción requerida ahora)

- `inbox-triage/SKILL.md`: ruta académica no especifica subcarpeta en `Maestria/` → pendiente revisión
- `writing-coach/SKILL.md`: actualizado en esta sesión (E1)
- `zettelkasten-forge/SKILL.md`: campo `coaching_notes` declarado pero no implementado en plantilla
- `pattern_id` vacío en 29/30 notas ZK → ejecutar pattern-harvester retrospectivo cuando haya tiempo
- Checkpoints explícitos faltantes en `modo-ab` (FASE 5) y `modo-c` (PASO 3→4) → pendiente revisión

**Resolución:** Completado 2026-04-27. Sistema auditado, 4 bugs corregidos, 7 decisiones aplicadas. activePatterns.json sin cambios (5 patrones activos P-006 a P-010).
