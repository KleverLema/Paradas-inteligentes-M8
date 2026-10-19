# Paradas Inteligentes

## Dosier de arquitectura de software

**Maestría en Ingeniería de Software — UPEC · Módulo 8: Automatización de procesos de software**  
**Integrantes:** Klever Lema Tamay, Edwin Toapanta y Ariel Aguirre  
**Fecha:** 18 de octubre de 2026

### Descripción del sistema

Se analiza una API REST para gestionar solicitudes de parada en el transporte público. El alcance funcional comprende la consulta de un catálogo fijo de paradas, el registro y la consulta de solicitudes, y la actualización de su estado. La referencia técnica es una aplicación Python/FastAPI cuyo almacenamiento reside en memoria. El dosier define una arquitectura objetivo con persistencia, integridad transaccional y separación modular.

El estudio delimita las responsabilidades del sistema, los atributos de calidad y las decisiones que más condicionan su evolución. El cálculo de tiempo estimado de llegada (ETA), el seguimiento GPS, la mensajería y las aplicaciones de usuario no forman parte de esta API.

### Estructura del dosier

| Área | Documento | Contenido |
|---|---|---|
| Contexto y drivers | [01-contexto-y-drivers.md](docs/01-contexto-y-drivers.md) | Interesados, preocupaciones, restricciones, cinco drivers y seis escenarios medibles |
| C4 nivel 1 | [c4-nivel1.md](docs/02-vistas-c4/c4-nivel1.md) | Contexto, límite del sistema y relaciones externas |
| C4 nivel 2 | [c4-nivel2.md](docs/02-vistas-c4/c4-nivel2.md) | Contenedores de la arquitectura objetivo y tecnologías propuestas |
| Coherencia | [coherencia-de-vistas.md](docs/02-vistas-c4/coherencia-de-vistas.md) | Correspondencia entre actores, contenedores, drivers y decisiones |
| ADR-001 | [Persistencia de solicitudes](docs/03-adr/ADR-001-persistencia-solicitudes.md) | Selección de almacenamiento SQLite |
| ADR-002 | [Unicidad transaccional](docs/03-adr/ADR-002-unicidad-concurrencia.md) | Protección frente a registros activos duplicados |
| ADR-003 | [Estilo arquitectónico](docs/03-adr/ADR-003-estilo-monolito-modular.md) | Selección de monolito modular |
| Selección de estilo | [matriz-decision.md](docs/03-adr/matriz-decision.md) | Comparación ponderada, sensibilidad y trade-offs |
| Análisis crítico de IA | [04-registro-ia.md](docs/04-registro-ia.md) | Uso, verificación y tratamiento de propuestas de IA |
| Base técnica | [05-evidencia-tecnica.md](docs/05-evidencia-tecnica.md) | Evidencias del comportamiento de la API analizada |

### Decisiones arquitectónicas

1. **Persistencia:** SQLite con una capa de acceso a datos separada de los endpoints, adecuado para una primera instancia de despliegue.
2. **Consistencia:** transacciones y un índice único parcial para evitar más de una solicitud activa por pareja pasajero–parada.
3. **Organización:** monolito modular FastAPI frente a microservicios, seleccionado mediante criterios de fiabilidad, seguridad, rendimiento, mantenibilidad y operación.

Estas decisiones describen la **arquitectura objetivo**. La API de referencia conserva actualmente las solicitudes en memoria; no se atribuyen al prototipo capacidades de persistencia, autorización o consistencia transaccional que no implementa.

### Referencias de arquitectura

- Bass, L., Clements, P., & Kazman, R. (2021). *Software architecture in practice* (4.ª ed.). Addison-Wesley.
- Brown, S. (s. f.). *The C4 model for visualising software architecture*. https://c4model.com/
- ISO/IEC/IEEE. (2022). *ISO/IEC/IEEE 42010:2022: Software, systems and enterprise — Architecture description*.
- Nygard, M. (2011). *Documenting architecture decisions*. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
