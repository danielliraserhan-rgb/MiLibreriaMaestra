# Mapeo Modos → Skills

> Referencia rápida para `modo-selector`. Tabla canónica.
> El modo se detecta en `inbox-triage` Fase 1 y determina qué skills se activan.

## Señales de detección por modo

| Modo | Señales clave |
|---|---|
| **1 — Libro Terminado** | Estructura completa con capítulos, arco cerrado, prosa pulida. Estado editorial: terminado. |
| **2 — Libro Pre-Diseño** | Estructura completa pero requiere edición. Puede tener transcripción oral + borrador mezclado. |
| **3 — Ideas Sueltas** | Sin estructura. Fragmentos, listas, apuntes dispersos. Sin arco claro. |
| **4 — Guía de Estudio** | Sigue el orden de un texto bíblico versículo a versículo. Exegético. Preguntas de estudio. |
| **5 — Nota Temática** | Desarrolla un solo tema teológico. Argumento central claro. Referencia permanente. |
| **6 — Estudio / Clase Larga** | Material de clase, 1–3 horas. Puede incluir notas del maestro + apuntes de estudiantes. |
| **7 — Grupos Conexión** | Material corto (~15 min). Diseñado para que OTRA persona facilite. Preguntas de discusión. |
| **Académico** | Vocabulario técnico, aparato de citas, estructura formal. No es voz de Daniel. |

## Flujo por modo

### MODO 1 — Libro Terminado
```
inbox-triage (diagnóstico + contenedor)
→ modo-c (diagnóstico opcional — solo si se detecta hueco)
→ zettelkasten-forge (15–30 notas)
→ pattern-harvester
Destino: Temas/NN/01_Libros/
```

### MODO 2 — Libro Pre-Diseño
```
inbox-triage (diagnóstico + contenedor)
→ modo-c (diagnóstico estructural obligatorio)
→ modo-ab (edición bloque a bloque — 5 fases)
→ modo-r (si se detecta hueco)
→ zettelkasten-forge (10–25 notas)
→ pattern-harvester
Destino: Temas/NN/01_Libros/ con fase: pre-diseno
```

### MODO 3 — Ideas Sueltas
```
inbox-triage (diagnóstico + contenedor)
→ zettelkasten-forge (5–10 notas — una por idea principal)
→ pattern-harvester
Destino: Temas/NN/04_NotasSinProcesar/
```

### MODO 4 — Guía de Estudio
```
inbox-triage (diagnóstico + contenedor)
→ modo-e (variante bíblica — esquema versículo a versículo)
→ zettelkasten-forge (10–20 notas — una por sección exegética clave)
→ pattern-harvester
Destino: Temas/NN/02_EsquemasDeClase/
```

### MODO 5 — Nota Temática
```
inbox-triage (diagnóstico + contenedor)
→ modo-c (opcional — si el argumento no está claro)
→ zettelkasten-forge (5–10 notas)
→ pattern-harvester
Destino: Temas/NN/ (raíz del tema)
```

### MODO 6 — Estudio / Clase Larga
```
inbox-triage (diagnóstico + contenedor)
→ modo-e (esquema didáctico — bíblica o temática según el material)
→ modo-ab (si hay transcripción oral — fases 1–5)
→ zettelkasten-forge (8–15 notas)
→ pattern-harvester
Destino: Temas/NN/02_EsquemasDeClase/ + Temas/NN/03_ClasesEnVivo/ (si transcripción)
```

### MODO 7 — Grupos Conexión
```
inbox-triage (diagnóstico + contenedor)
→ modo-e (variante temática reducida — ~15 min)
→ zettelkasten-forge (3–5 notas)
→ pattern-harvester
Destino: Temas/NN/02_EsquemasDeClase/ (subcarpeta grupos-conexion/)
```

### ACADÉMICO (fuera de los 7)
```
inbox-triage (diagnóstico + contenedor — plantilla académica)
→ notas-maestria (6 secciones fijas, régimen neutral)
→ zettelkasten-forge (5–15 notas, régimen neutral)
→ pattern-harvester (scope: académico)
Destino: Temas/08_Academico/Maestria/
ZK destino: 09_Zettelkasten/academico/
```

---

## Motor de escritura — obsidian-markdown

**`obsidian-markdown` es el motor oficial de escritura.** Se activa siempre que hay que crear o editar un `.md` tras aprobación de Daniel.

| Momento | Acción de `obsidian-markdown` |
|---|---|
| Post-aprobación ZK (paso 2.e) | Crea los archivos en `09_Zettelkasten/pastoral/` o `/academico/` con YAML v2 y wikilinks `[[…]]` |
| Actualización YAML fuente (paso 2.f) | Edita el frontmatter del archivo fuente añadiendo los IDs a `zettelkasten_notes` |
| Creación de contenedor (inbox-triage Fase 2) | Crea el archivo de destino con el frontmatter YAML v2 completo |

**Prohibido usar terminal** (`cat`, `echo`, `sed`, `awk`) para escribir archivos `.md` en cualquier momento del flujo.

---

## Reglas de oro

1. `inbox-triage` **siempre primero**
2. `pattern-harvester` **siempre último**
3. `zettelkasten-forge` **siempre antes del harvester**
4. `obsidian-markdown` **siempre para crear/editar `.md`** — nunca terminal
5. Nunca avanzar de paso sin OK explícito de Daniel
6. Si el modo no está claro después de leer el archivo, preguntar antes de proceder
