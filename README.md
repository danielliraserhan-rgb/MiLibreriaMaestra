Imagina que tienes una gran biblioteca personal donde guardas todo tu trabajo, tus estudios y tus escritos, pero en lugar de ser solo un archivero estático, es una biblioteca viva que interactúa contigo. Está dividida en dos roles principales:
Tu Archivo Central (El Segundo Cerebro): Es donde guardas toda tu investigación, tus libros como "Orígenes", tus clases, tus sermones para la iglesia y tus trabajos de la maestría. Aquí cada idea está conectada con otras, como un gran mapa de tus pensamientos.
Tu Asistente Editorial (El Coach de Escritura): Es un asistente inteligente que se ha leído absolutamente todo lo que tú has escrito. Su regla de oro es que nunca escribe por ti, sino que funciona como un editor o mentor muy exigente. Él conoce tu estilo, sabe cómo te gusta explicar las cosas y conoce los límites de tu teología.

￼
¿Cómo es el proceso cuando quieres guardar algo nuevo?
Todo lo que escribes (ya sea un capítulo de un libro, un ensayo para la escuela o los apuntes de una clase) pasa por un proceso de revisión muy ordenado. Piénsalo como una fábrica donde tú eres el director y debes aprobar (dar el "OK") en cada paso del ensamble:
Recepción y Diagnóstico: El asistente recibe tu nuevo texto, lo lee y te dice: "Ah, veo que este es un ensayo para la universidad", o "Esto es el borrador de tu nuevo libro". Te pregunta: "¿Es correcto?". Si le dices que sí, avanza.
Edición y Estructura: Dependiendo de lo que estés escribiendo, el asistente saca diferentes herramientas.
Si es material para la iglesia, verifica que mantengas un tono cercano, pastoral y esperanzador (tiene una lista de 10 puntos que debe cumplir).
Si es para tu maestría, "apaga" su lado pastoral y se vuelve estricto, revisando que el formato sea académico y neutral.
Si nota que te falta explicar mejor una idea, te lo señala para que tú lo corrijas.
Destilación de Ideas (Extracción de las pepitas de oro): Una vez que el texto está pulido, el asistente no solo lo guarda en la carpeta correspondiente, sino que saca las ideas más importantes y las convierte en "tarjetas de ideas" independientes. Así, si en tres años necesitas hablar sobre "El Bautismo", tendrás a la mano todas las ideas clave que escribiste hoy sobre ese tema.
Aprendizaje Final: Al terminar todo el proceso, el asistente analiza cómo escribiste hoy y te dice: "Noté que últimamente te gusta usar esta nueva estructura para explicar tus puntos. ¿Quieres que me aprenda ese estilo para evaluar tus futuros escritos?". Tú le das el OK y el asistente se vuelve un poco más inteligente y más parecido a ti para la próxima vez.

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
