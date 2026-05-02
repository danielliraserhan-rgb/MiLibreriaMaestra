
---

# MiLibreriaMaestra — Documento Ejecutivo del Sistema

**Autor:** Daniel Lira Serhan

**Versión:** `v3.2 (Arquitectura Híbrida — Auditada)`

**Fecha:** 2 de mayo de 2026

**Repositorio:** `danielliraserhan-rgb/MiLibreriaMaestra`

---

## 1. Introducción: El Salto a la Automatización Híbrida

**MiLibreriaMaestra** ha migrado a un sistema de **Nivel 2**, donde la inteligencia de **Claude Code** se separa de la ejecución mecánica. En esta versión, Claude actúa exclusivamente como el cerebro estratégico (Arquitecto), mientras que una suite de scripts en **Python** se encarga de la escritura de archivos, inyección de metadatos y movimientos en el sistema.

### La Tríada del Sistema

1. **S1 - Segundo Cerebro (Obsidian):** El almacén y base de datos de conocimiento.
    
2. **S2 - Arquitecto Editorial (Claude Code):** La inteligencia que diagnostica, organiza y decide. Ya no escribe código YAML manualmente para ahorrar ~80% de tokens.
    
3. **Los Obreros (Python Scripts):** Ejecutores deterministas que garantizan que el formato y la estructura sean perfectos sin error humano o alucinación de la IA.
    

---

## 2. Arquitectura del Vault y Scripts

Se ha añadido una capa de infraestructura crítica para la automatización:

### Scripts Python (`_Scripts/`)

| Script | Función |
|---|---|
| `inbox_triage.py` | Inyecta YAML v2 y mueve archivos al destino según JSON de Claude |
| `modo_selector.py` | Cadenero: responde `saltar` si ya tiene YAML, `inbox-triage` si virgen |
| `write_moc.py` | Escribe MOC físico en `MapasDeContenido—MOCs/` según JSON de Claude |
| `scrivener_bridge.py` | Sincroniza Scrivener → Obsidian protegiendo el YAML existente |
| `markdown_cleaner.py` | Limpieza RegEx: headers, saltos de línea, espacios finales |
| `mass_convert.py` | Conversión masiva PDF/DOCX → Markdown via MarkItDown |
| `scan_vault.py` | `--mode gaps`: cobertura ZK por tema. `--mode index`: regenera VAULT_INDEX.md |
| `zk_fix_title_field.py` | Utilidad: corrige campo `title` → `titulo` en notas ZK |
| `zk_rename.py` | Utilidad: renombra notas ZK al formato `{id} {titulo_corto}.md` |

### Skills del Sistema (`skills-sistema-v3/`)

Cada skill tiene su propio directorio con `SKILL.md`. Skills activos:
`inbox-triage` · `modo-selector` · `moc-builder` · `scrivener-bridge` · `markdown-cleaner` · `format-adapter` · `modo-ab-seccion-mixta` · `modo-c-esquema-editorial` · `modo-e-unificado` · `modo-r-material-referencia` · `notas-maestria` · `zettelkasten-forge` · `pattern-harvester` · `bulk-ingest` · `writing-coach` · `voice-trainer` · `desarrollador-de-temas` · `spaced-review` · `conversion-documentos`


---

## 3. Flujo de Entrada (El Trayecto Híbrido)

El flujo lineal ahora incluye una **intervención determinista** para proteger la integridad de los datos.

Fragmento de código

```
graph TD
    A[Archivo en Inbox] --> B{modo-selector: Cadenero Python}
    B -- "Virgen" --> C[Conversión Masiva: MarkItDown]
    C --> D[inbox-triage: Diagnóstico Claude]
    D -- "Genera JSON Payload" --> E[Obrero Python: Inyección YAML + Movimiento]
    E --> F[Skills del Modo Detectado]
    F --> G[zettelkasten-forge]
    G -- "Propuesta Notas Atómicas" --> H{¿Aprobado?}
    H -- Sí --> I[pattern-harvester]
    I --> J[Fin: Registro en PROCESS_LOG]
```

---

## 4. Evolución de los Skills (Capacidades Híbridas)

|**Skill**|**Rol de Claude (S2)**|**Rol de Python (Obrero)**|
|---|---|---|
|**`inbox-triage`**|Diagnostica dominio, tema y modo.|Escribe el YAML v2 y mueve el archivo.|
|**`moc-builder`**|Agrupa notas temáticamente con criterio pastoral.|Redacta el archivo .md y crea los [[wikilinks]].|
|**`markdown-cleaner`**|Detecta que el archivo está "sucio".|Ejecuta RegEx para normalizar el texto.|
|**`format-adapter`**|**(Intelectual)** Adapta el género (libro a blog, etc).|N/A (Es puramente editorial).|
|**`scrivener-bridge`**|Identifica cambios en la carpeta de sincronización.|Fusiona el texto nuevo protegiendo el YAML del vault.|

---

## 5. Infraestructura Técnica Actualizada

- **Motor de Ingesta:** Python 3.13 (necesario para las últimas dependencias de MarkItDown).
    
- **Protocolo de Comunicación:** JSON Estructurado. Claude Code envía "instrucciones de construcción" a los scripts locales.
    
- **Ahorro de Contexto:** Al delegar la escritura de MOCs y YAMLs, la ventana de contexto de Claude se mantiene limpia para tareas de análisis teológico profundo.
    

> [!IMPORTANT]
> 
> **Regla de Oro Nivel 2:** Claude tiene **estrictamente prohibido** usar comandos de terminal como `cat`, `echo >>` o `sed` para modificar archivos Markdown. Toda modificación estructural debe pasar por los scripts autorizados en `_Scripts/`.

---

## 6. Estado del Sistema (al 2 de mayo de 2026)

- **Pipeline:** 100% Híbrido, operativo y auditado (v3.2).
- **Scripts:** 9 scripts activos, todos con `chmod +x` y paths portables (`Path(__file__).parent.parent`).
- **YAML v2:** 54+ archivos migrados. Migración en curso.
- **Pruebas funcionales:** modo-selector ✅ · inbox-triage ✅ · write_moc ✅ · scan_vault ✅
    

---

**Daniel Lira Serhan** | _MiLibreriaMaestra v3.1_
