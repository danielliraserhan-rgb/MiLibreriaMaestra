# VAULT INDEX — MiLibreriaMaestra
> Regenerar: `python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --mode index > _Skills/VAULT_INDEX.md`
> Última actualización: 2026-04-26

---

## Estado del vault

| | Fuentes procesadas | Notas ZK |
|---|---|---|
| **Pastoral** | 2 | 30 |
| **Académico** | 1 | 0 |
| **Total** | 3 | 30 |

---

## Dominio Pastoral

### Fuentes procesadas

- **En los días de Noé** — modo: `6-estudio-clase` · tema: `03_Escatologia—Destino` · ZK generadas: 8
- **Nacer de Nuevo** — modo: `1-libro-terminado` · tema: `05_DoctrinasFundamentales` · ZK generadas: 22

### Clusters por fuente

**2026-04-24-en-los-dias-de-noe** — 8 notas
  - El Reino de Dios es el eje de toda la existencia — vivir fuera de esa realidad es vivir sin sentido
  - Dos eras, una decisión: ¿para cuál vivimos?
  - El arca abierta — el evangelio es una invitación urgente, no una oferta permanente
  - Dejar las redes al instante — el llamado misionero exige abandono inmediato, no negociación gradual
  - El pecado de los días de Noé no fue la inmoralidad — fue vivir sin sentido ante el diluvio que se acercaba
  - Diluir el evangelio a un ritual dominical es repetir el error de la generación de Noé
  - _...y 2 más_

**Nacer de Nuevo** — 22 notas
  - La caída produce tres reinos del pecado: Satanás, la carne y el mundo
  - El vacío espiritual es la invitación de Dios, no un defecto del diseño
  - Presentar el cuerpo como sacrificio vivo es el culto racional — la respuesta lógica a la gracia
  - La expiación tiene dos caras: corregir lo que estaba mal y cubrir al que pecó
  - Los seis cuerpos del Mikveh apuntan al agua viva como origen divino de la purificación
  - Somos embajadores de reconciliación: ya fuiste reconciliado, ahora lleva la reconciliación
  - _...y 16 más_

### Notas más conectadas

- `ZK-20260423-1200-005` — La serpiente de bronce prefigura a Cristo levantado: el mismo veneno, el mismo remedio _(conexiones: 4)_
- `ZK-20260423-1200-003` — Nacer de nuevo es reconocer — no un proceso sino un momento de fe _(conexiones: 4)_
- `ZK-20260424-1628-003` — El Reino de Dios es el eje de toda la existencia — vivir fuera de esa realidad es vivir sin sentido _(conexiones: 3)_
- `ZK-20260424-1628-004` — Dos eras, una decisión: ¿para cuál vivimos? _(conexiones: 3)_
- `ZK-20260424-1628-007` — El arca abierta — el evangelio es una invitación urgente, no una oferta permanente _(conexiones: 3)_

---

## Dominio Académico

### Fuentes procesadas

- **Naked But Not Ashamed: The Fruit of Sin Covered by God's Grace** — tipo: `articulo_academico` · ZK generadas: 0

_Sin notas ZK generadas todavía._

---

## Comandos rápidos

```bash
# Buscar notas sobre un tema
python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --query "término"

# Detectar huecos de conocimiento
python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --mode gaps

# Regenerar este índice
python skills-sistema-v3/moc-builder/scripts/scan_vault.py --vault . --mode index > _Skills/VAULT_INDEX.md
```

