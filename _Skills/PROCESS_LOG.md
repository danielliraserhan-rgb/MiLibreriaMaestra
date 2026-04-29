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

### 2026-04-28 — MODO 6 (Clase Larga) — "Introducción a los Profetas Menores"

**Archivo:** `Temas/02_HistoriaDeIsrael/02_EsquemasDeClase/2026-04-28-introduccion-profetas-menores.md`
**Archivos fuente:** `Inbox/Intro Profetas Menores (1).docx` (~10,500 palabras)
**Skills ejecutados:** conversion-documentos → inbox-triage → modo-e-unificado → zettelkasten-forge → pattern-harvester
**Metadatos extraídos:**
- Temas principales: Profetismo bíblico y fuentes de revelación, Canon bíblico, Gobierno teocrático de Israel, Reino dividido (norte/sur), Etnocentrismo y universalidad de la salvación
- Libros bíblicos: Los Doce (Profetas Menores), Abdías, Joel
- Autores citados: Alfonso Ropero (Editorial Clie), Laureano Benitez Grande-Caballero, John Calvin
- Versículos clave: Mal. 2:7, Ez. 44:23, Jer. 5:23, Abd. 1-14, Abd. 15-21, Joel 2, 2 Ti. 3:16, 2 Pe. 1:19-21

**Notas Zettelkasten generadas:** 12 (ZK-20260428-1600-001 a ZK-20260428-1611-012)

**Outputs adicionales:**
- `Temas/02_HistoriaDeIsrael/02_EsquemasDeClase/MODO-E-Introduccion-Profetas-Menores.docx` — esquema MODO E generado (docx-js)
- `Temas/02_HistoriaDeIsrael/02_EsquemasDeClase/Intro Profetas Menores (1).md` — conversión markitdown del original

**Patrones detectados (pattern-harvester):**
1. P-015 — Juicio → restauración → soberanía final de Dios (estructura)
2. P-016 — El profeta como fiscal del pacto, no como adivino (teología)
3. P-017 — Cristo como filtro de selección del canon (teología)

**Propuestas:**
- [x] P-015 — Juicio → restauración → soberanía final de Dios — APROBADO
- [x] P-016 — El profeta como fiscal del pacto, no como adivino — APROBADO
- [x] P-017 — Cristo como filtro de selección del canon — APROBADO

**Resolución:** 3 aprobados, 0 rechazados. activePatterns.json actualizado a 17 patrones. ZK con pattern_id actualizados: ZK-1607-008, ZK-1608-009 (P-015); ZK-1600-001 (P-016); ZK-1602-003, ZK-1610-011 (P-017)

---

### 2026-04-28 — BULK-INGEST Lote 1 — 21 predicaciones pastorales

**Archivos fuente (Inbox/):**
1. `Predicación_Afirmar el Rostro.docx`
2. `Predicación_Discipulos.docx`
3. `Predicación_El Hombre Liberado y su Deseo de Estar con Jesús.docx`
4. `Predicación_El Rey David — Hombre conforme al corazón de Dios.docx`
5. `Predicación_El ministerio de la reconciliación.docx`
6. `Predicación_El pan de vid.docx`
7. `Predicación_El plan de Dios.docx`
8. `Predicación_Fin — Conoce el comienzo y el Fin.docx`
9. `Predicación_Fruto del pecado vs fruto de la gracia.docx`
10. `Predicación_ICF Ensenada.docx`
11. `Predicación_La Brecha.docx`
12. `Predicación_La conquista — Parte 2 Los procesos de la promesa.docx`
13. `Predicación_La esperanza Segura 5.docx`
14. `Predicación_La esperanza Segura.docx`
15. `Predicación_La imagen de la verdad.docx`
16. `Predicación_La mujer.docx`
17. `Predicación_La resurrección.docx`
18. `Predicación_La verdadera Conquista simple.docx`
19. `Predicación_La verdadera conquista.docx`
20. `Predicación_Las 4 copas.docx`
21. `Predicación_MARANATHA — EL YA VIENE.docx`

**Nota:** Doc 11 original (`Predicaciónes_Juan 4:26`) descartado — archivo vacío. Total procesado: 21/22.

**Skills ejecutados:** bulk-ingest → inbox-triage (F1+F2, todos sin pausas) → zettelkasten-forge (directo, sin modo-c per memoria activa) → pattern-harvester

**Contenedores creados:**
- `Temas/02_HistoriaDeIsrael/02_EsquemasDeClase/El Rey David — Hombre conforme al corazón de Dios.md`
- `Temas/03_Escatologia—Destino/02_EsquemasDeClase/Fin — Conoce el comienzo y el Fin.md`
- `Temas/03_Escatologia—Destino/02_EsquemasDeClase/La esperanza Segura.md`
- `Temas/03_Escatologia—Destino/02_EsquemasDeClase/La esperanza Segura 5.md`
- `Temas/03_Escatologia—Destino/02_EsquemasDeClase/MARANATHA — EL YA VIENE.md`
- `Temas/04_ExegesisNT/02_EsquemasDeClase/Las 4 copas.md`
- `Temas/04_ExegesisNT/02_EsquemasDeClase/La imagen de la verdad.md`
- `Temas/05_DoctrinasFundamentales/02_EsquemasDeClase/La resurrección.md`
- `Temas/05_DoctrinasFundamentales/02_EsquemasDeClase/La verdadera conquista.md`
- `Temas/05_DoctrinasFundamentales/02_EsquemasDeClase/La verdadera Conquista simple.md`
- `Temas/06_DiscipuladoVidaCristiana/02_EsquemasDeClase/Afirmar el Rostro.md`
- `Temas/06_DiscipuladoVidaCristiana/02_EsquemasDeClase/Discipulos.md`
- `Temas/06_DiscipuladoVidaCristiana/02_EsquemasDeClase/El Hombre Liberado y su Deseo de Estar con Jesús.md`
- `Temas/06_DiscipuladoVidaCristiana/02_EsquemasDeClase/El ministerio de la reconciliación.md`
- `Temas/06_DiscipuladoVidaCristiana/02_EsquemasDeClase/El pan de vid.md`
- `Temas/06_DiscipuladoVidaCristiana/02_EsquemasDeClase/La Brecha.md`
- `Temas/06_DiscipuladoVidaCristiana/02_EsquemasDeClase/La mujer.md`
- `Temas/07_PredicacionesDevocionales/02_EsquemasDeClase/El plan de Dios.md`
- `Temas/07_PredicacionesDevocionales/02_EsquemasDeClase/Fruto del pecado vs fruto de la gracia.md`
- `Temas/07_PredicacionesDevocionales/02_EsquemasDeClase/ICF Ensenada.md`
- `Temas/07_PredicacionesDevocionales/02_EsquemasDeClase/La conquista — Parte 2 Los procesos de la promesa.md`

**Notas Zettelkasten generadas:** 63 (ZK-20260428-1700-001 a ZK-20260428-1700-063)
- 3 notas por predicación · dominio: pastoral · todos los contenedores actualizados con IDs

**Patrones detectados (pattern-harvester):** 7 propuestos · 7 aprobados

**Propuestas:**
- [x] P-018 — La espera tiene función teológica — APROBADO (teologia)
- [x] P-019 — El clamor humano fundamental es el mismo desde Génesis hasta Apocalipsis — APROBADO (hermeneutica)
- [x] P-020 — La identidad precede siempre a la función en el discipulado — APROBADO (estructura)
- [x] P-021 — El evangelio es proclamación de conquista, no invitación de consumidor — APROBADO (hermeneutica)
- [x] P-022 — La escatología produce misión y radicalidad, no escapismo — APROBADO (teologia)
- [x] P-023 — La hermenéutica tipológica: David como tipo de Cristo — APROBADO (hermeneutica)
- [x] P-024 — La Biblia como meta-narrativa: Creación–Caída–Redención–Restauración — APROBADO (estructura)

**Resolución:** 7 aprobados, 0 rechazados. activePatterns.json actualizado a 24 patrones.

---

#### PROBLEMAS DOCUMENTADOS (sin acción requerida ahora)

- `inbox-triage/SKILL.md`: ruta académica no especifica subcarpeta en `Maestria/` → pendiente revisión
- `writing-coach/SKILL.md`: actualizado en esta sesión (E1)
- `zettelkasten-forge/SKILL.md`: campo `coaching_notes` declarado pero no implementado en plantilla
- `pattern_id` vacío en 29/30 notas ZK → ejecutar pattern-harvester retrospectivo cuando haya tiempo
- Checkpoints explícitos faltantes en `modo-ab` (FASE 5) y `modo-c` (PASO 3→4) → pendiente revisión

**Resolución:** Completado 2026-04-27. Sistema auditado, 4 bugs corregidos, 7 decisiones aplicadas. activePatterns.json sin cambios (5 patrones activos P-006 a P-010).

---

### 2026-04-29 — BULK-INGEST — Lote 2 — 21 documentos

**Dominio:** pastoral
**Modo de ejecución:** aprobación total anticipada (no se esperaron OKs intermedios)
**Caveman mode:** activo

**Documentos procesados:**

| # | Archivo | MODO | Destino | ZK |
|---|---|---|---|---|
| 1 | Momentos con Jesus | 6 | 07_PredicacionesDevocionales/03_ClasesEnVivo | 3 |
| 2 | Navidad — Maranatha 2019 | 5 | 07_PredicacionesDevocionales/04_NotasSinProcesar | 2 |
| 3 | Notas breves Soldado Atleta Agricultor | 3 | 06_DiscipuladoVidaCristiana/04_NotasSinProcesar | 1 |
| 4 | Nicodemo — Parque el Capitán 2023 | 6 | 04_ExegesisNT/03_ClasesEnVivo | 2 |
| 5 | El buen pastor — Parque el Capitán 2023 | 6 | 04_ExegesisNT/03_ClasesEnVivo | 3 |
| 6 | Jesús te vuelve a llamar en la barca | 6 | 06_DiscipuladoVidaCristiana/03_ClasesEnVivo | 2 |
| 7 | La vid verdadera — Parque el Capitán 2023 | 6 | 06_DiscipuladoVidaCristiana/03_ClasesEnVivo | 3 |
| 8 | La carrera de la fe | 5 | 03_Escatologia—Destino/04_NotasSinProcesar | 2 |
| 9 | Sensatez — Miguel Pla (material externo) | 5 | 07_PredicacionesDevocionales/05_MaterialExterno | 2 |
| 10 | Hechos 4 — ¿A quién obedeceremos? | 6 | 04_ExegesisNT/03_ClasesEnVivo | 2 |
| 11 | Sígueme — La perla de gran precio | 5 | 06_DiscipuladoVidaCristiana/04_NotasSinProcesar | 2 |
| 12 | Soldado Atleta y Agricultor | 6 | 06_DiscipuladoVidaCristiana/03_ClasesEnVivo | 2 |
| 13 | Versículos y frases — Permanece | 3 | 03_Escatologia—Destino/04_NotasSinProcesar | 2 |
| 14 | Zaqueo — Lucas 19 | 5 | 04_ExegesisNT/04_NotasSinProcesar | 3 |
| 15 | ¿No ardía nuestro corazón? — Agosto 2022 | 6 | 07_PredicacionesDevocionales/03_ClasesEnVivo | 2 |
| 16 | ¿No ardía nuestro corazón? — versión base | 5 | 07_PredicacionesDevocionales/04_NotasSinProcesar | 1 |
| 17 | Boda Paco Moreno y Brenda Hernandez | 7 | 07_PredicacionesDevocionales/03_ClasesEnVivo | 2 |
| 18 | XV Años — Naomi | 7 | 07_PredicacionesDevocionales/03_ClasesEnVivo | 2 |
| 19 | HOSANNA — El Rey que completa la conquista | 5 | 05_DoctrinasFundamentales/04_NotasSinProcesar | 2 |
| 20 | Permanece hasta el día de su regreso | 6 | 03_Escatologia—Destino/03_ClasesEnVivo | 2 |
| 21 | Proveerá un cordero — El llamado en la gran historia | 5 | 05_DoctrinasFundamentales/04_NotasSinProcesar | 3 |

**Total ZK generadas:** 45 (ZK-20260429-1000-001 a ZK-20260429-1000-045)
**Patrones propuestos:** pendiente (pattern-harvester no ejecutado — fuera del alcance acordado)
**Directorios creados:** 7 nuevos subdirectorios en Temas/

**Resolución:** Lote cerrado. 21 contenedores creados, 45 notas ZK creadas. Pattern-harvester queda pendiente para próxima sesión.
