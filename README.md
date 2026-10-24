# Paradas Inteligentes

## Dosier de arquitectura de software y Cadena CASE

**Maestría en Ingeniería de Software — UPEC · Módulo 8: Automatización de procesos de software**  
**Integrantes:** Klever Lema Tamay, Edwin Toapanta y Ariel Aguirre  
**Fecha:** 24 de octubre de 2026 (Actualizado Semana 2)

---

### Descripción del sistema

Se analiza e implementa una API REST para gestionar solicitudes de parada en el transporte público urbano de Tulcán. El alcance funcional comprende la consulta de un catálogo de paradas, el registro y la consulta de solicitudes, y la actualización de su estado. La arquitectura objetivo define persistencia con SQLite, integridad transaccional (ADR-001, ADR-002) y separación modular (ADR-003), respaldada por una cadena CASE completa y ejecutable.

El estudio delimita las responsabilidades del sistema, los atributos de calidad y las decisiones que más condicionan su evolución. El cálculo de tiempo estimado de llegada (ETA), el seguimiento GPS, la mensajería y las aplicaciones móviles no forman parte de esta API.

---

### Estructura del repositorio y artefactos

| Área / Fase | Documento | Contenido |
|---|---|---|
| **Contexto y drivers** | [01-contexto-y-drivers.md](docs/01-contexto-y-drivers.md) | Interesados, preocupaciones, restricciones, cinco drivers y seis escenarios medibles |
| **C4 nivel 1** | [c4-nivel1.md](docs/02-vistas-c4/c4-nivel1.md) | Contexto, límite del sistema y relaciones externas |
| **C4 nivel 2** | [c4-nivel2.md](docs/02-vistas-c4/c4-nivel2.md) | Contenedores de la arquitectura objetivo y tecnologías propuestas |
| **C4 actual** | [c4-nivel2-actual.md](docs/02-vistas-c4/c4-nivel2-actual.md) | Vista del prototipo en memoria vs propuesta |
| **Coherencia** | [coherencia-de-vistas.md](docs/02-vistas-c4/coherencia-de-vistas.md) | Correspondencia entre actores, contenedores, drivers y decisiones |
| **ADR-001** | [Persistencia de solicitudes](docs/03-adr/ADR-001-persistencia-solicitudes.md) | Selección de almacenamiento SQLite transaccional |
| **ADR-002** | [Unicidad transaccional](docs/03-adr/ADR-002-unicidad-concurrencia.md) | Protección frente a registros activos duplicados |
| **ADR-003** | [Estilo arquitectónico](docs/03-adr/ADR-003-estilo-monolito-modular.md) | Selección de monolito modular FastAPI |
| **Selección de estilo** | [matriz-decision.md](docs/03-adr/matriz-decision.md) | Comparación ponderada, sensibilidad y trade-offs |
| **Análisis crítico de IA** | [04-registro-ia.md](docs/04-registro-ia.md) | Uso, verificación y tratamiento de propuestas de IA (Semana 1 y Semana 2) |
| **Base técnica** | [05-evidencia-tecnica.md](docs/05-evidencia-tecnica.md) | Evidencias del comportamiento de la API analizada |
| **Colaboración** | [revision-cruzada.md](docs/02-vistas-c4/revision-cruzada.md) | Ficha para la revisión con otro equipo |
| **06 — Toolchain (SEM02)** | [06-mapa-toolchain.md](docs/06-mapa-toolchain.md) | Mapa de toolchain, 10 tareas priorizadas (F×E×R) y pruebas de herramientas Top (Spectral, IA, Pytest) |
| **07 — Historias (SEM02)** | [07-historias-y-criterios.md](docs/07-historias-y-criterios.md) | Historias de usuario (HU01–HU04) y criterios de aceptación en Gherkin vinculados a E1–E6 |
| **08 — Matriz CASE (SEM02)** | [08-matriz-evaluacion-case.md](docs/08-matriz-evaluacion-case.md) | Matriz de evaluación CASE (ISO/IEC 14102), ponderación al 100 %, selección y análisis de riesgos |
| **Contrato OpenAPI** | [api/openapi.yaml](api/openapi.yaml) | Especificación formal OpenAPI 3.0.3 validada con Spectral (0 errores) |
| **Código ejecutable y tests** | [src/](src/) y [tests/](tests/) | Esqueleto modular FastAPI con persistencia SQLite y suite de pruebas pytest |

---

### Hitos y Entregas

* **Hito H1 (Semana 1):** Dossier de arquitectura etiquetado como `v0.1.0`.
* **Hito H2 (Semana 2):** Cadena CASE, contrato OpenAPI, esqueleto ejecutable y pruebas etiquetado como `v0.2.0`.

### Entrega SEM02 en Moodle / EVA

Enviar la **URL del commit específico** y la URL de la etiqueta **`v0.2.0`** que fija la versión evaluada. Asegurarse de que el docente del módulo tenga acceso como colaborador al repositorio privado.
