---
title: "Índice Zettelkasten — Notas Huérfanas"
tipo: indice-zettelkasten
fecha_actualizacion: ""
---

# Notas Zettelkasten Huérfanas

> Notas atómicas sin ningún enlace entrante ni saliente.
> Una nota huérfana es señal de que le falta conexión — revisitar y conectar.
> Este índice se actualiza automáticamente por `zettelkasten-forge` al detectar notas pendientes de conectar.

## Pendientes de conectar

- (vacío — se pobla cuando zettelkasten-forge no encuentra conexión para una nota propuesta)

---

## Cómo resolver una huérfana

1. Leer la nota y buscar manualmente en `09_Zettelkasten/` una nota relacionada
2. Agregar `[[ZK-...]]` en la sección "Conexiones" de ambas notas
3. Actualizar `notas_relacionadas:` en el YAML de ambas
4. Quitar la nota de este índice cuando tenga al menos 1 enlace bidireccional
