# Registro de uso y verificación crítica de inteligencia artificial

La inteligencia artificial se utilizó como apoyo para estructurar documentación, formular alternativas y contrastar argumentos arquitectónicos. Las decisiones se fundamentan en las reglas de la API y en los escenarios de calidad descritos en el dosier.

| Actividad | Herramienta y versión | Solicitud resumida | Aporte generado | Verificación / tratamiento |
|---|---|---|---|---|
| Identificación de drivers | ChatGPT (GPT-6), octubre de 2026 | Relacionar reglas de la API con atributos de calidad | Priorizar integridad, persistencia y seguridad | **Modificado:** se restringió el alcance a cuatro operaciones REST verificadas en la API. |
| Selección de persistencia | ChatGPT (GPT-6) | Comparar memoria, SQLite y PostgreSQL | Propuesta de SQLite para una instancia | **Aceptado como decisión de diseño:** `solicitudes = {}` confirma ausencia de persistencia. |
| Concurrencia | ChatGPT (GPT-6) | Analizar el riesgo de solicitudes activas duplicadas | Índice único parcial y transacción | **Aceptado como diseño:** se contrastó con la búsqueda `any(...)` de `crear_solicitud()`; no se atribuyó implementación al prototipo. |
| Estilo arquitectónico | ChatGPT (GPT-6) | Comparar monolito modular y microservicios | Matriz ponderada y análisis de trade-offs | **Modificado:** se añadieron pesos explícitos y una prueba de sensibilidad, sin presentar las notas como mediciones. |
| Vistas C4 | ChatGPT (GPT-6) | Separar contexto y contenedores | Dos diagramas Mermaid | **Modificado:** se mantuvieron consumidores externos fuera del límite y SQLite como contenedor objetivo. |

## Contraste crítico de resultados

| Planteamiento contrastado | Evidencia | Resolución |
|---|---|---|
| La API ya conserva solicitudes tras reiniciarse | El almacenamiento consultado es un diccionario local al proceso | **Rechazado.** La persistencia se define en ADR-001 como arquitectura objetivo. |
| La búsqueda previa de duplicados es suficiente bajo concurrencia | El código consulta con `any(...)` y después escribe, sin transacción | **Rechazado.** Se requiere restricción transaccional en ADR-002. |
| Los microservicios son necesarios por tratarse de transporte público | El módulo tiene cuatro operaciones y no integra ETA ni GPS | **Rechazado.** La matriz favorece el monolito modular para el alcance establecido. |
| SQLite resuelve todos los escenarios de calidad | E4 exige autorización y E5 exige medir latencia | **Modificado.** SQLite contribuye a E1–E2, pero no sustituye seguridad ni pruebas. |
| Los diagramas C4 pueden representar la arquitectura propuesta | Las vistas distinguen actores externos de contenedores propios | **Aceptado.** Se documenta el límite entre implementación actual y diseño objetivo. |

Los resultados numéricos de escenarios y las valoraciones de alternativas son criterios de diseño, no pruebas ejecutadas. Esta distinción preserva la trazabilidad entre evidencia técnica, decisiones y objetivos de calidad.

## Control humano y ratificación del equipo (Semana 1)

- **Fecha de revisión del grupo:** 18/10/2026.
- **Integrantes participantes:** Klever Lema Tamay, Edwin Toapanta, Ariel Aguirre.
- **Conclusiones de validación técnica:** El equipo ratifica unánimemente la selección del estilo Monolito Modular (A1) y la persistencia transaccional con SQLite (ADR-001, ADR-002, ADR-003) para el alcance del módulo de solicitudes. Se aprueban los 6 escenarios de calidad E1–E6 como metas formales de diseño.
- **Objeciones aceptadas:** Se mantiene estrictamente fuera del alcance de este dosier cualquier funcionalidad de GPS y cálculo predictivo de ETA (pertenecientes a fases posteriores o proyectos complementarios). Se declara explícitamente que SQLite se adopta para una sola instancia académica.
- **Objeciones modificadas (peso, escenario, diagrama o ADR):** Se validó la matriz de decisión y el análisis de sensibilidad; el equipo ratifica que consistencia (E1) y durabilidad (E2) deben conservar el mayor peso relativo debido al riesgo de pérdida o duplicación de solicitudes de parada.
- **Objeciones rechazadas con evidencia verificable:** Se rechaza de forma definitiva la arquitectura de microservicios (A2) por suponer sobrecostos de orquestación, latencia de red y complejidad operativa desproporcionada para una API de cuatro endpoints.
- **Versión y etiquetado:** Etiqueta Git `v0.1.0` fijada para la entrega formal del hito H1 en Moodle/EVA.

---

# Registro de uso y verificación crítica de IA — Semana 2: Cadena CASE (Hito H2)

**Fecha:** 24/10/2026  
**Equipo:** Klever Lema Tamay · Edwin Toapanta · Ariel Aguirre  
**Objetivo:** Documentar la asistencia de IA en la generación de la cadena CASE (contrato OpenAPI, stubs FastAPI, pruebas Pytest y matrices), explicitando los defectos detectados, correcciones y ejecución real.

## 1. Bitácora de Asistencia y Verificación de Artefactos de la Semana 2

| Actividad | Herramienta y versión | Prompt resumido | Salida generada | Defectos / Riesgos detectados | Decisión y verificación real (Linter / Tests) |
|---|---|---|---|---|---|
| **Diseño de Contrato OpenAPI 3.0** (`api/openapi.yaml`) | Antigravity AI / Gemini 3.8 Flash | «Generar contrato OpenAPI 3.0.3 para los 4 endpoints del módulo de solicitudes con esquemas y respuestas de error 400, 404 y 409». | Archivo YAML completo con esquemas `Parada`, `SolicitudCreate`, `SolicitudResponse` y `EstadoUpdate`. | La salida inicial omitió la descripción del requestBody y no tipaba el header `application/json` en respuestas 409. | **Modificado:** Se completaron descripciones y códigos de estado. Verificado con Spectral CLI (`spectral:oas`): **0 errores**. |
| **Generación de Esqueleto y Modelos Pydantic** (`src/models.py`) | Antigravity AI / Gemini 3.8 Flash | «Generar modelos Pydantic v2 y Enum de estados a partir de api/openapi.yaml con tipado estricto». | Código Python con `BaseModel` y `EstadoSolicitud(str, Enum)`. | Uso sugerido de `datetime.utcnow()` (deprecado en Python 3.12) y ausencia de validación de longitud en `id_pasajero`. | **Modificado:** Se reemplazó por `datetime.now(timezone.utc)` y se agregaron restricciones `min_length=3`, `max_length=50`. |
| **Persistencia SQLite Transaccional** (`src/database.py`, `src/repository.py`) | Antigravity AI / Gemini 3.8 Flash | «Implementar repositorio en SQLite con índice único condicional para solicitudes activas según ADR-001 y ADR-002». | DDL con tabla `solicitudes`, índice parcial y métodos CRUD con manejo de `IntegrityError`. | La IA propuso inicialmente capturar excepciones de manera genérica (`except Exception:`), ocultando posibles bloqueos de SQLite. | **Modificado:** Se acotó la captura específica a `sqlite3.IntegrityError` retornando HTTP 409 explícito. Verificado con pruebas unitarias. |
| **Generación de Suite de Pruebas Pytest** (`tests/test_api.py`) | Antigravity AI / Gemini 3.8 Flash | «Generar pruebas automatizadas con pytest y TestClient basadas en los criterios de aceptación Gherkin CA01.1 a CA04.4». | 9 funciones de prueba cubriendo paradas, horario comercial, duplicados concurrentes y transiciones de estado. | Las pruebas dependían de la base de datos fija `paradas.db`, pudiendo generar efectos secundarios o fallos por orden de ejecución. | **Modificado:** Se implementó la fixture `client_and_repo` con base de datos temporal aislada (`tempfile.NamedTemporaryFile`). Verificado: **9 pruebas pasando al 100%**. |
| **Matriz de Evaluación de Herramientas CASE** (`docs/08-matriz-evaluacion-case.md`) | Antigravity AI / Gemini 3.8 Flash | «Estructurar matriz comparativa de 3 herramientas CASE (Spectral, Pytest y Antigravity AI) bajo ISO/IEC 14102 con pesos 100%». | Tabla de 5 criterios ponderados y puntuaciones observables basadas en pruebas reales. | La IA asignó puntaje perfecto (5/5) a sí misma en detección de defectos. | **Rechazado y corregido:** Se ajustó la calificación de la IA a 3/5 por tendencia a alucinar APIs deprecadas o patrones en memoria, obligando a verificación humana. |

## 2. Verificación con Ejecución Real de Herramientas

Cada artefacto generado en la Semana 2 fue sometido a validación práctica:
1. **Spectral CLI:** Comprobación formal del contrato OpenAPI (`api/openapi.yaml`). Resultado: Especificación limpia, libre de violaciones semánticas (`spectral:oas`).
2. **Pytest (Suite de Pruebas):** Ejecución de la suite completa en `tests/test_api.py`. Resultado: **9 pruebas ejecutadas y aprobadas**.
3. **Aislamiento de Entorno:** Base de datos relacional SQLite inicializada con catálogo verificado y restricciones de integridad comprobadas.

## 3. Control Humano y Aprobación del Hito H2

- **Fecha de revisión del equipo:** 24/10/2026.
- **Participantes:** Klever Lema Tamay, Edwin Toapanta, Ariel Aguirre.
- **Decisión final:** Se aprueba formalmente la cadena CASE compuesta por Spectral, Antigravity AI y Pytest, consolidando los artefactos `docs/06-mapa-toolchain.md`, `docs/07-historias-y-criterios.md`, `docs/08-matriz-evaluacion-case.md`, `api/openapi.yaml`, `src/` y `tests/`.
- **Etiquetado:** Versión fijada con la etiqueta Git **`v0.2.0`** para la entrega del Hito H2.
