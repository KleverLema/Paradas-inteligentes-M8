# Paradas Inteligentes — SEM01: dosier de arquitectura (Módulo 8)

**Equipo:** Klever Lema Tamay · Edwin Toapanta · Ariel Aguirre.  
**Repositorio:** https://github.com/KleverLema/Paradas-inteligentes-M8  
**Estado:** documentación académica de arquitectura, con decisiones propuestas; la implementación futura no se declara terminada.

## Alcance del proyecto

Se documenta **únicamente** el módulo de solicitudes de parada de una API REST FastAPI. El prototipo de referencia permite consultar paradas, crear solicitudes, consultar una solicitud y cambiar estados. No implementa ETA, GPS, aplicación móvil, notificaciones ni base de datos persistente. La separación modular, la persistencia SQLite y la garantía transaccional se evalúan como **decisiones de diseño**, no como trabajo programado esta semana.

## Índice del dosier

| Práctica | Archivo | Contenido |
|---|---|---|
| 01 | [01-contexto-y-drivers.md](docs/01-contexto-y-drivers.md) | Problema, stakeholders, concerns, restricciones, 5 drivers y 6 escenarios con seis partes y medidas |
| 02 | [c4-nivel1.md](docs/02-vistas-c4/c4-nivel1.md) | C4 contexto como código Mermaid |
| 02 | [c4-nivel2.md](docs/02-vistas-c4/c4-nivel2.md) | C4 contenedores de la arquitectura objetivo; enlazado a ADR |
| Complementaria | [c4-nivel2-actual.md](docs/02-vistas-c4/c4-nivel2-actual.md) | Vista del prototipo en memoria; evita confundir realidad y propuesta |
| 03 | [ADR-001](docs/03-adr/ADR-001-persistencia-solicitudes.md), [ADR-002](docs/03-adr/ADR-002-unicidad-concurrencia.md) y [ADR-003](docs/03-adr/ADR-003-estilo-monolito-modular.md) | Contexto, alternativas, decisión, consecuencias y trade-offs |
| 03 | [matriz-decision.md](docs/03-adr/matriz-decision.md) | Comparación de alternativas, pesos 100 %, valoración y sensibilidad |
| Verificación | [04-registro-ia.md](docs/04-registro-ia.md) | Consulta y contraste crítico con IA |
| Evidencia | [05-evidencia-tecnica.md](docs/05-evidencia-tecnica.md) | Extractos y observaciones del prototipo de referencia; no incorpora código ajeno |
| Colaboración | [revision-cruzada.md](docs/02-vistas-c4/revision-cruzada.md) | Ficha para la revisión **real** con otro equipo: pendiente hasta efectuarla |

## Qué se ha verificado y qué falta

- Los diagramas se escribieron en Mermaid y deben comprobarse en la pestaña **Preview** de GitHub tras cada cambio.
- La matriz contiene puntajes **hipotéticos**, no mediciones de desempeño. La segunda distribución de pesos contrasta la sensibilidad de la elección.
- Los escenarios E1–E6 son metas para una eventual implementación, no pruebas superadas.
- **Pendiente de efectuar con personas reales:** aprobación de las decisiones por Edwin, Ariel y Klever y revisión cruzada con otro equipo; completar los registros correspondientes sin inventar firmas, resultados ni fechas.
- Repositorio privado: el docente debe ser invitado como colaborador y aceptar el acceso.
- Antes de enviar EVA, crear la etiqueta `v0.1.0` para el commit final que el grupo apruebe.

## Entrega SEM01 en EVA

Enviar **únicamente la URL de un commit específico**, que fijará la versión evaluada; no adjuntar ZIP ni elaborar otro Word obligatorio. Si después del commit original se realizan correcciones, se debe compartir el **nuevo commit final**. Esta versión de documentación no publica material de compañeros de otro grupo ni su código fuente.
