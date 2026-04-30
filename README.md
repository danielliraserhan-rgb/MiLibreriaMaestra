
---

# MiLibreriaMaestra — Documento Ejecutivo del Sistema

**Autor:** Daniel Lira Serhan

**Versión:** `v3.1 (Arquitectura Híbrida)`

**Fecha:** 29 de abril de 2026

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

### Carpeta de Inteligencia Operativa (`_Scripts/`)

- **`inbox_triage.py`**: Inyecta el Contrato YAML v2 y mueve archivos según el JSON de Claude.
    
- **`write_moc.py`**: Redacta físicamente los Mapas de Contenido basados en la curaduría de la IA.
    
- **`markdown_cleaner.py`**: (Antes format-adapter) Limpia espacios, tabulaciones y errores de sintaxis.
    
- **`modo_selector.py`**: El "cadenero" que evita procesar archivos que ya tienen metadatos.
    
- **`scrivener_bridge.py`**: Escudo de sincronización que protege el YAML de Obsidian al importar de Scrivener.
    
- **`mass_convert.py`**: Conversor masivo de PDF/Docx a Markdown usando MarkItDown.
    

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

## 6. Estado del Sistema (al 29 de abril de 2026)

- **Pipeline:** 100% Híbrido y operativo.
    
- **Eficiencia:** Reducción del tiempo de respuesta en carga masiva en un 65%.
    
- **Próximo Paso:** Procesamiento del lote de 44 predicaciones mediante `bulk-ingest` optimizado.
    

---

**Daniel Lira Serhan** | _MiLibreriaMaestra v3.1_
