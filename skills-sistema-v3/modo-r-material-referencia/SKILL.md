---
name: modo-r-material-referencia
description: "Activa este skill cuando detectes un hueco estructural en un manuscrito, de una sección incompleta, un bloque de cierre débil, un argumento que no termina de desarrollarse, o material insuficiente para sostener el arco teológico. Úsalo también cuando Daniel mencione conferencias previas, predicaciones, notas de otros proyectos, o cualquier fuente externa que podría alimentar una sección. No esperes que Daniel lo pida explícitamente — si hay un hueco y material externo podría cubrirlo, dispara este skill y pregunta."
---

---
name: modo-r-material-referencia
description: "Activa cuando detectes hueco estructural o cuando Daniel mencione notas, conferencias o predicaciones externas."
---

# MODO R — Material de Referencia Externo

## Antes de activar — Cargar activePatterns

Leer `_Skills/activePatterns.json`.
Si hay patrones de scope `estructura` con huecos ya registrados en archivos anteriores, anotar — puede haber material de referencia relevante ya procesado en el vault.

---

## Cuándo se activa
Este skill se dispara ante cualquiera de estas señales:  
- Arco incompleto  
- Cierre débil  
- Material insuficiente  
- Daniel menciona fuente externa

## Paso 1 — Detectar y nombrar el hueco
Identifica con precisión el hueco en una sola frase.

## Paso 2 — Preguntar a Daniel
Pregunta 1: “Hay un hueco en [sección]. ¿Implementamos MODO R?”  
Pregunta 2 (si dice sí): “¿Tienes material de referencia?”

## Paso 3 — Recibir y leer
Lee el material completo antes de diagnosticar. Confirma: “Leí el material.”

## Paso 4 — Diagnóstico en tres categorías
- ✅ Directamente utilizable  
- 🔄 Pertenece a otro contexto  
- ❓ Implícito pero sin desarrollar

## Paso 5 — Esperar confirmación
“¿Qué entra y qué no? Dime qué quieres integrar.”

## Paso 6 — Integración
Integra solo lo autorizado. Aplica CORE-CHECKLIST. Actualiza YAML v2 (incluir `author_quotes` si el material externo tiene autores citables) y mueve archivo a carpeta correcta.

## Paso 7 — Notas de conexión (Zettelkasten)
El material integrado desde una fuente externa es candidato natural a **nota de tipo `conexion`** en Zettelkasten — conecta el argumento de Daniel con una fuente o idea externa.

Al cerrar modo-r, señalar a `zettelkasten-forge`:
```
"Hay [N] bloques integrados desde material externo — candidatos a notas de tipo 'conexion'."
```
`zettelkasten-forge` los incluye en sus propuestas.