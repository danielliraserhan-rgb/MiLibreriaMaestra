Este es el documento formateado y optimizado para ser el rostro de tu repositorio en GitHub. He aplicado **Mermaid** para los diagramas, bloques de alerta para las reglas críticas y tablas de alta legibilidad para que cualquier persona (o tú mismo en el futuro) entienda la genialidad detrás de **MiLibreriaMaestra**.

---

# MiLibreriaMaestra — Documento Ejecutivo del Sistema

**Autor:** Daniel Lira Serhan  
**Versión:** `v3.0`  
**Fecha:** 28 de abril de 2026  
**Repositorio:** `danielliraserhan-rgb/MiLibreriaMaestra`

---

## 1. Introducción
**MiLibreriaMaestra** es un sistema de gestión de conocimiento teológico construido sobre **Obsidian** y potenciado por **Claude Code**. Su propósito es procesar, catalogar y conectar el material pastoral y académico de Daniel Lira: libros, predicaciones, clases, papers y notas.

### La Dualidad del Sistema
El sistema opera bajo una filosofía **Zettelkasten** (notas atómicas interconectadas) y está gobernado por dos identidades:

* **S1 - Segundo Cerebro (Obsidian):** El almacén. Donde viven los archivos, MOCs (Mapas de Contenido) y la base de datos de conocimiento.
* **S2 - Coach de Escritura (Claude Code):** La inteligencia. Analiza, diagnostica y entrena. Claude observa; Daniel decide.

---

## 2. Arquitectura del Vault
La estructura se divide por dominios con reglas hermenéuticas y editoriales distintas:

| Dominio | Temas | Enfoque | Voz |
| :--- | :--- | :--- | :--- |
| **Pastoral** | 01-07 | Orígenes, Historia, Escatología, Exégesis, Doctrinas, Discipulado, Predicaciones. | Cristocéntrica, pastoral, narrativa. |
| **Académico** | 08 | Maestría en Biola University. | Neutral, formal, citación técnica. |

### Carpetas de Sistema Críticas
* `Inbox/`: Punto de entrada (incluye sincronización con Scrivener).
* `_Skills/`: Scripts de Python, lógica de patrones (`activePatterns.json`) y bitácoras de proceso.
* `09_Zettelkasten/`: El núcleo atómico del sistema.
* `ContextoMaestro/`: El "ADN" del sistema (reglas de voz y líneas rojas teológicas).

---

## 3. Flujo de Entrada (El Trayecto)
El flujo es estrictamente lineal y secuencial. **Regla de Oro:** Nunca se avanza sin el `OK` explícito del autor.

```mermaid
graph TD
    A[Archivo en Inbox] --> B{Paso 1: modo-selector}
    B --> C[Paso 2.5: Conversión MarkItDown]
    C --> D[Paso 3: inbox-triage FASE 1]
    D -- "Reporte + YAML Propuesto" --> E{¿Aprobado?}
    E -- Sí --> F[Paso 4: inbox-triage FASE 2]
    F --> G[Paso 5: Skills del Modo Detectado]
    G --> H[Paso 6: zettelkasten-forge]
    H -- "Propuesta Notas Atómicas" --> I{¿Aprobado?}
    I -- Sí --> J[Paso 7: pattern-harvester]
    J --> K[Fin: Archivo en Destino + Log Actualizado]
```

---

## 4. Los 8 Modos de Procesamiento
Cada archivo entrante activa un pipeline específico según su naturaleza:

| Modo | Tipo | Pipeline de Skills | Objetivo ZK |
| :--- | :--- | :--- | :--- |
| **1** | Libro Terminado | `triage` → `modo-c` → `forge` → `harvester` | 15-30 notas |
| **2** | Libro Pre-Diseño | `triage` → `modo-c` → `modo-ab` → `modo-r` → `forge` | 10-25 notas |
| **3** | Ideas Sueltas | `triage` → `forge` → `harvester` | 5-10 notas |
| **4** | Guía de Estudio | `triage` → `modo-e` (bíblica) → `forge` | 10-20 notas |
| **8** | Académico | `triage` → `notas-maestria` → `forge` → `harvester` | 5-15 notas |

---

## 5. Catálogo de Skills (Capacidades del Sistema)

### 5.1 Flujo Principal
* **`inbox-triage`**: Clasifica el archivo, asigna el modo y genera metadatos YAML v2.
* **`modo-ab` (Coach Anotador)**: Separa transcripciones orales de borradores escritos para identificar redundancias.
* **`zettelkasten-forge`**: Genera notas atómicas con campos **SM-2** para repetición espaciada.
* **`pattern-harvester`**: Extrae patrones de voz y teología para alimentar la IA.

### 5.2 Skills de Soporte y Autónomos
* **`spaced-review` (SM-2)**: Algoritmo de aprendizaje para revisar notas vencidas diariamente.
* **`desarrollador-de-temas`**: Escáner de "huecos" que detecta preguntas abiertas o temas sin contenido.
* **`conversion-documentos`**: Integración con `markitdown` para transformar PDFs y DOCX a Markdown.

---

## 6. Infraestructura Técnica

### Stack Tecnológico
* **Motor:** Claude Code (terminal) & Obsidian (UI).
* **Lógica:** Python 3.x (scripts de automatización y SM-2).
* **Control de Versiones:** Git con flujo de Pull Requests para cada sesión de edición.
* **Algoritmo de Memoria:** SM-2 (SuperMemo 2).

> [!CAUTION]
> **Gestión de Worktrees (Git):** > Claude Code opera en ramas aisladas. Para evitar desincronización, ejecutar siempre tras cerrar sesión:
> `git fetch --all && git reset --hard origin/main && git clean -fd`

---

## 7. Estado del Sistema (al 28 de abril de 2026)

* **Notas Zettelkasten Totales:** 330
* **Patrones de Voz Activos:** 5 (v1.1)
* **Última Mejora:** Implementación del "Gap Detector" (PR #9) para identificar temas huerfanos.

### Reglas Editoriales No Negociables
1.  **Cristocentrismo:** En el dominio pastoral, todo apunta a Cristo.
2.  **Identidad antes que conducta:** La teología precede a la ética.
3.  **Preservación Oral:** En transcripciones, no se elimina nada; solo se da estructura.
4.  **Régimen Académico:** Neutralidad total en el Tema 08 (Biola).

---
**Daniel Lira Serhan** | *MiLibreriaMaestra v3.0*
