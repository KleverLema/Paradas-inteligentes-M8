# Matriz de trazabilidad de extremo a extremo — H4

**Proyecto:** Paradas Inteligentes — módulo de solicitudes de parada  
**Módulo:** Automatización de procesos de software, Semana 4  
**Estado:** Documento de consolidación con evidencias verificadas y brechas declaradas.  
**Fecha de preparación:** 05/11/2026.

> **Nota de verificación.** Esta matriz se elaboró con los archivos de proyecto compartidos previamente y las capturas de ejecución de Git y GitHub Actions. Antes de la entrega, comprobar los vínculos y actualizar el estado del PR #20. «Prueba aprobada» significa que pasa la suite existente, no que se haya demostrado cada criterio de calidad a escala.

## 1. Finalidad y criterio de lectura

La cadena exigida para el hito H4 es **requisito (HU/CA) → escenario (E) → decisión (ADR) → artefacto y prueba → commit o PR → pipeline**. La trazabilidad permite localizar qué parte del software implementa cada decisión, qué control la verifica y qué evidencias faltan.

El alcance funcional comprende cuatro operaciones REST para cinco paradas: `GET /paradas`, `POST /solicitudes`, `GET /solicitudes/{id_solicitud}` y `PATCH /solicitudes/{id_solicitud}/estado`. El repositorio utiliza Python, FastAPI, Pydantic y SQLite. GPS, predicción ETA, aplicación móvil y autenticación productiva están fuera del alcance del prototipo entregado; no deben describirse como implementados.

Fuentes internas: [contexto y drivers](01-contexto-y-drivers.md), [historias de usuario](07-historias-y-criterios.md), [decisiones ADR](03-adr/), [contrato OpenAPI](../api/openapi.yaml), [pruebas](../tests/test_api.py) y [pipeline](../.github/workflows/ci.yml).

## 2. Matriz funcional y técnica

| Requisito / criterio | Escenario / driver | ADR o restricción | Código / contrato | Verificación existente | Historial y pipeline | Estado y brecha |
|---|---|---|---|---|---|---|
| **HU01 · CA01.1–CA01.2** Consultar cinco paradas y sus campos | E5 / D4 | ADR-003; R3 | `src/main.py` (`GET /paradas`), `src/repository.py`, `api/openapi.yaml` | `test_hu01_listar_paradas` en `tests/test_api.py` | Suite `pytest` en PR [#19](https://github.com/KleverLema/Paradas-inteligentes-M8/pull/19); CI [Actions](https://github.com/KleverLema/Paradas-inteligentes-M8/actions) | **Verificado** para catálogo y estructura de campos; E5 aún sin medición de rendimiento. |
| **HU02 · CA02.1** Crear solicitud válida | E1/E2; D1/D2 | ADR-001 y ADR-002 | `src/main.py` (`POST /solicitudes`), `src/repository.py`, `src/database.py` | `test_hu02_crear_solicitud_exitosa` | PR #19; job de pruebas del CI | **Parcial:** crea solicitud en prueba de repositorio; no cubre por sí solo un HTTP POST completo. |
| **HU02 · CA02.2** Rechazar horario no permitido | R2; D1 | Regla de negocio; ADR-003 | `src/repository.py`; OpenAPI | `test_hu02_rechazo_horario_nocturno` | PR #19; job `calidad` | **Parcial:** la prueba usa horas UTC forzadas; revisar correspondencia del horario 05:00–22:00 con `America/Guayaquil` antes de afirmar validación local. |
| **HU02 · CA02.3** Rechazar duplicado activo | E1 / D1 | ADR-002: restricción transaccional | `src/database.py`, `src/repository.py` y OpenAPI | `test_hu02_rechazo_duplicado_activo` | PR #19; job `calidad` | **Parcial:** prueba duplicidad secuencial. Escenario E1 de 100 solicitudes simultáneas no demostrado. |
| **HU02 · CA02.4** Rechazar parada inexistente | R3 / D1 | Validación de catálogo | `src/repository.py` y OpenAPI | `test_hu02_rechazo_parada_inexistente` | PR #19; job `calidad` | **Verificado** en prueba de repositorio. |
| **HU03 · CA03.1** Consultar solicitud existente | E2/E5; D2/D4 | ADR-001 | `src/main.py`, `src/repository.py`, OpenAPI | `test_hu03_obtener_solicitud_existente` | PR #19; job `calidad` | **Verificado** por GET con `TestClient`; sin medición E5. |
| **HU03 · CA03.2** Consultar inexistente | E2 / D2 | ADR-001 | `src/main.py`, `src/repository.py` | `test_hu03_obtener_solicitud_inexistente` | PR #19; job `calidad` | **Verificado** para respuesta 404. |
| **HU03 · CA03.3** Recuperar después de reiniciar | E2 / D2 | ADR-001 | `src/database.py`, `src/repository.py` | **No hay prueba específica** en la suite de 9 tests | Se requiere nuevo test y ejecución en CI | **Pendiente**: verificar recuperación tras nueva instancia/conexión. |
| **HU04 · CA04.1–CA04.2** Transiciones válidas | E3 / D1 | ADR-003; máquina de estados | `src/main.py` (`PATCH`), `src/repository.py` | `test_hu04_transicion_estado_valida` | PR #19; job `calidad` | **Verificado** para flujo PENDIENTE → CONFIRMADA → ATENDIDA. |
| **HU04 · CA04.3** Rechazar transición ilegal | E3 / D1 | ADR-003; R2 | `src/repository.py`, `src/main.py` | `test_hu04_rechazo_transicion_invalida` | PR #19; job `calidad` | **Verificado** para un caso de ATENDIDA → PENDIENTE; E3 de 20 intentos no medido. |
| **HU04 · CA04.4** Actualizar una solicitud inexistente | E3 / D1 | Máquina de estados | `src/main.py`, `src/repository.py` | **No hay prueba específica** en la suite compartida | Agregar test HTTP 404 y comprobar en CI | **Pendiente**. |

## 3. Escenarios de calidad no demostrados por la suite actual

| Escenario | Objetivo diseñado en Semana 1 | Evidencia real disponible | Qué falta |
|---|---|---|---|
| E1 (concurrencia) | 100 solicitudes idénticas simultáneas: 1 éxito y 99 conflictos | Un test de duplicado **secuencial** | Test de concurrencia real y conteo de respuestas. |
| E2 (persistencia) | Recuperar 100/100 solicitudes tras reinicio | SQLite presente, consultas funcionales | Reinicio o reapertura de conexión + prueba CA03.3. |
| E3 (estados) | Rechazar 20/20 transiciones prohibidas | Un test con transición inválida | Escenarios adicionales hasta el tamaño objetivo. |
| E4 (seguridad) | Denegar 50/50 accesos sin autorización | No existe autenticación/autorización completa | Mantener como **meta fuera del prototipo**; no afirmar cumplimiento. |
| E5 (desempeño) | Objetivos de latencia/carga definidos en `docs/01-contexto-y-drivers.md` | No hay resultado de prueba de carga documentado | Ejecutar y registrar medición específica o declarar pendiente. |
| E6 (mantenibilidad) | Independencia y evolución controlada del diseño modular | ADR-003 y separación de módulos | Función de aptitud automatizada si la rúbrica lo requiere. |

**Nota técnica:** 9/9 pruebas aprobadas significa que las **nueve pruebas existentes** pasan; no representa 100 % de cobertura de código ni de todos los criterios de aceptación.

## 4. Relación de artefactos arquitectónicos, CASE y Git

| Decisión / artefacto | Archivo fuente | Evidencia para la sustentación |
|---|---|---|
| Drivers D1–D5 y escenarios E1–E6 | [`docs/01-contexto-y-drivers.md`](01-contexto-y-drivers.md) | Explicar qué se quiere medir y distinguir meta de resultado. |
| Vistas C4 y coherencia | [`docs/02-vistas-c4/`](02-vistas-c4/) | Contexto, contenedores, correspondencia con el código. |
| Persistencia | [`ADR-001`](03-adr/ADR-001-persistencia-solicitudes.md) | SQLite transaccional, durabilidad y trade-offs. |
| Unicidad activa | [`ADR-002`](03-adr/ADR-002-unicidad-concurrencia.md) | Índice/restricción y conflicto HTTP 409. |
| Monolito modular | [`ADR-003`](03-adr/ADR-003-estilo-monolito-modular.md) | Simplicidad del prototipo y separación por módulos. |
| Elección de Git | [`ADR-004`](03-adr/ADR-004-seleccion-git.md), [`matriz Git/SVN`](08-matriz-git-vs-svn.md) | Justificar Git distribuido y flujo de revisión. |
| Selección CASE | [`mapa`](06-mapa-toolchain.md), [`evaluación`](08-matriz-evaluacion-case.md) | Relacionar necesidades, puntuaciones y herramientas. |
| Evidencia de colaboración | [`reporte de conflicto`](09-reporte-conflicto.md), [`revisión de seguridad`](10-revision-seguridad-dependencias.md), [`CONTRIBUTING`](../CONTRIBUTING.md) | Explicar PR y decisiones sin adjudicar aportes no demostrados. |
| Contrato REST | [`api/openapi.yaml`](../api/openapi.yaml) | Validación con Spectral y documentación generada con Redocly. |

## 5. Evidencias de commits, PR y pipeline

| Evidencia | Identificador / enlace | Estado comprobado |
|---|---|---|
| Entrega H3 | [Etiqueta v0.3.0](https://github.com/KleverLema/Paradas-inteligentes-M8/releases/tag/v0.3.0) | Referencia histórica de Semana 3. |
| Pipeline Python | [PR #19](https://github.com/KleverLema/Paradas-inteligentes-M8/pull/19), commits `fcc22f2` y `469d6d2` | **Merged**; merge `72d4996`. Ruff y pytest aprobados. |
| Pipeline contrato/documentación | [PR #20](https://github.com/KleverLema/Paradas-inteligentes-M8/pull/20), commit `b48031b` | **Abierto en la última captura**; dos jobs en verde en Actions, revisión solicitada a Ariel. Actualizar tras merge. |
| Estado de `main` mostrado | Commit `aacd55e` (merge PR #18) | Corresponde al último `git log -1` mostrado en `main`; no significa que PR #20 esté fusionado. |
| Pipeline GitHub Actions | [Pestaña Actions](https://github.com/KleverLema/Paradas-inteligentes-M8/actions) | Una corrida CI del PR #20 en 20 s con trabajos `Analisis y pruebas` y `Contrato OpenAPI y documentacion` aprobados. |

> **Atención antes de entregar:** actualizar enlaces y nuevos commits obtenidos desde PR #20; verificar que los controles sean obligatorios en el ruleset de `main`. Dos checks verdes por sí solos no prueban que el merge sea bloqueado ante un fallo.

## 6. Quality gates: mapa de evidencia

| Puerta | Herramienta | Evidencia | Estado al redactar |
|---|---|---|---|
| Lint de Python | Ruff | `python -m ruff check src tests` | **Automatizada y aprobada** en PR #19 y #20. |
| Pruebas de API | pytest | `python -m pytest tests/ -v` | **Automatizada y aprobada**; nueve pruebas. |
| Validación contractual | Spectral | `npx spectral lint api/openapi.yaml --ruleset .spectral.yaml --fail-severity=warn` | **Automatizada y aprobada** en PR #20. |
| Documentación de API | Redocly | `npx redocly build-docs ...` | **Automatizada y aprobada** en PR #20; HTML generado localmente. |
| Cobertura | pytest-cov | Sin medición en la evidencia disponible | **Pendiente**. |
| Seguridad de dependencias y secretos | pip-audit, npm audit, escáner de secretos | `docs/10-revision-seguridad-dependencias.md` incluye revisión manual previa; npm instaló paquetes sin vulnerabilidades detectadas en revisión local | **Pendiente como gate recurrente**; una instalación limpia no equivale a análisis exhaustivo. |
| Análisis estático de seguridad | CodeQL / herramienta apropiada para Python | Sin workflow verificado | **Pendiente**. |
| Bloqueo de merge por checks | Ruleset de `main` | Aprobación humana exigida en PR #19 y #20 | **Pendiente de comprobar** checks requeridos y fallo controlado. |

## 7. Lista de verificación para el cierre

- [ ] Integrar PR #20 solo con aprobación y ambos checks verdes; actualizar tabla de historial.
- [ ] Configurar y verificar cobertura, análisis estático y seguridad en CI.
- [ ] Exigir checks correctos en protección de `main`.
- [ ] Provocar un fallo **inocuo y reversible** en rama de prueba y demostrar check rojo y bloqueo; corregir y mostrar verde.
- [ ] Registrar pruebas que faltan para CA03.3, CA04.4 y escenarios de calidad (o declararlos como límites explícitos).
- [ ] Completar `docs/09-informe-final.md`, `docs/04-registro-ia.md` y métricas sustentadas.
- [ ] Guardar enlaces permanentes de Actions/PR y enviar el commit final según la rúbrica.
