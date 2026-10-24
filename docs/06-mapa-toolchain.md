# Práctica 06 — Mapa de Toolchain y Priorización de Tareas CASE (Semana 2)

**Proyecto:** Paradas Inteligentes — Módulo de Solicitudes de Parada (Módulo 8)  
**Equipo:** Klever Lema Tamay · Edwin Toapanta · Ariel Aguirre  
**Fecha:** 24/10/2026  
**Estado:** Cadena CASE operativa y documentada para Hito H2  

---

## 1. Descripción del Proceso de Desarrollo por Fases

El ciclo de vida del módulo de gestión de solicitudes de parada se estructura siguiendo las recomendaciones del estándar **ISO/IEC/IEEE 12207:2017** y las directrices de herramientas CASE de **ISO/IEC 14102:2008**, organizado en cinco fases sucesivas con trazabilidad integral:

| Fase | Etapa del Proceso | Artefactos de Entrada | Artefactos de Salida | Responsable Principal |
|---|---|---|---|---|
| **F1** | **Ingeniería de Requisitos** | Casos de uso de movilidad, necesidades de stakeholders (S1–S6), restricciones de negocio (R1–R7). | Historias de Usuario (`HU01`–`HU04`), Criterios de Aceptación en formato Gherkin (`CA`). | Edwin Toapanta |
| **F2** | **Diseño y Especificación de Contrato (API-First)** | Historias en Gherkin, catálogo de paradas, matriz de estados y restricciones horarias. | Contrato formal OpenAPI 3.0 (`api/openapi.yaml`), reglas de validación semántica (Spectral). | Klever Lema Tamay |
| **F3** | **Construcción y Persistencia** | Contrato OpenAPI, decisiones de arquitectura (`ADR-001`, `ADR-002`, `ADR-003`). | Esqueleto modular en `src/`, modelos Pydantic, repositorio SQLite transaccional. | Ariel Aguirre |
| **F4** | **Verificación y Pruebas Automatizadas** | Criterios Gherkin, escenarios de calidad (`E1`–`E6`), API ejecutable. | Suite de pruebas automatizadas en `tests/` (unitarias, integración y concurrencia). | Edwin Toapanta |
| **F5** | **Gobernanza, Integración y Versionado** | Código fuente, suites de pruebas, artefactos de documentación. | Repositorio versionado, etiquetado formal Git (`v0.2.0`), control de cambios convencional. | Klever Lema Tamay |

---

## 2. Priorización de Tareas de Alto Volumen

Para determinar qué tareas del ciclo de vida generan mayor retorno de inversión al ser automatizadas con herramientas CASE, se evalúan 10 tareas críticas utilizando el modelo de priorización tridimensional:

$$\text{Prioridad} = \text{Frecuencia (F)} \times \text{Esfuerzo (E)} \times \text{Riesgo (R)}$$

* **Frecuencia (F, 1 a 5):** Cuántas veces se ejecuta la tarea (1 = Muy esporádica; 5 = Continua o múltiples veces al día).
* **Esfuerzo (E, 1 a 5):** Horas-persona requeridas de forma manual (1 = Trivial/Minutos; 5 = Alto/Horas a días).
* **Riesgo (R, 1 a 5):** Probabilidad de error humano y severidad del impacto en calidad o producción (1 = Mínimo; 5 = Crítico/Inconsistencia grave).

### Tabla de Priorización de las 10 Tareas Concretas (`T01` a `T10`)

| ID | Tarea Concreta | Fase | F | E | R | Puntaje (F×E×R) | Justificación de los Valores Asignados |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **T04** | **Validación y linting continuo del contrato OpenAPI con Spectral** | F2 | 5 | 3 | 5 | **75** | **F=5:** Se ejecuta en cada edición de la API. **E=3:** Revisar manualmente tipos, respuestas y estándares OpenAPI 3.0 toma tiempo considerable. **R=5:** Un error en el contrato rompe la integración de clientes, stubs y pruebas (Riesgo crítico de discrepancia). |
| **T08** | **Ejecución automatizada de pruebas unitarias, integración y concurrencia (Pytest)** | F4 | 5 | 3 | 5 | **75** | **F=5:** Ejecutada en cada commit y verificación local. **E=3:** Probar manualmente 20 transiciones o peticiones concurrentes es inviable. **R=5:** Romper el invariante de unicidad activa (E1) o la persistencia (E2) invalida el sistema. |
| **T05** | **Generación asistida con IA de stubs de endpoints y esquemas Pydantic desde OpenAPI** | F3 | 4 | 4 | 4 | **64** | **F=4:** Cada vez que evoluciona el contrato se deben sincronizar modelos. **E=4:** Escribir código repetitivo (DTOs, serializadores, rutas) consume muchas horas. **R=4:** El error de tipeo en atributos altera el contrato público acordado. |
| **T01** | Redacción y estructuración formal de Criterios de Aceptación en sintaxis Gherkin | F1 | 3 | 4 | 4 | **48** | **F=3:** Se realiza al inicio de cada sprint/entrega. **E=4:** Requiere análisis riguroso de casos límite y reglas de negocio. **R=4:** Un criterio ambiguo genera implementaciones defectuosas. |
| **T06** | Implementación del repositorio SQLite con control de transacciones concurrentes | F3 | 2 | 5 | 4 | **40** | **F=2:** Se diseña e implementa una vez, con ajustes puntuales. **E=5:** Requiere manejo fino de conexiones, bloqueos y excepciones SQL. **R=4:** Fallos en transacciones causan bloqueos de base de datos o duplicación. |
| **T07** | Análisis estático de código Python, formateo y linter (Flake8 / Ruff) | F4 | 5 | 2 | 3 | **30** | **F=5:** Ejecución constante en el IDE. **E=2:** Rápido de corregir. **R=3:** Previene errores de estilo y variables no utilizadas, pero rara vez detiene el negocio. |
| **T03** | Redacción y versionado manual del archivo de especificación OpenAPI YAML | F2 | 3 | 4 | 2 | **24** | **F=3:** Tarea periódica de diseño de contrato. **E=4:** Redacción manual detallada de esquemas YAML. **R=2:** El riesgo se mitiga al estar respaldado por Spectral (T04). |
| **T02** | Modelado de arquitectura como código (Mermaid C4) y redacción de ADRs | F2 | 2 | 4 | 3 | **24** | **F=2:** Ocurre durante decisiones de diseño. **E=4:** Análisis conceptual profundo. **R=3:** Falta de documentación confunde al equipo pero no rompe el código en caliente. |
| **T09** | Generación y publicación interactiva de documentación Swagger UI / Redoc | F2 | 4 | 1 | 3 | **12** | **F=4:** Se consulta frecuentemente al probar endpoints. **E=1:** Automatizado de forma nativa por FastAPI. **R=3:** Documentación desactualizada confunde al integrador. |
| **T10** | Etiquetado semántico Git (`v0.2.0`), control de changelog y commits convencionales | F5 | 2 | 2 | 2 | **8** | **F=2:** Al cierre de cada hito de entrega. **E=2:** Pocos comandos en terminal. **R=2:** Un error en el mensaje de commit no compromete la arquitectura. |

> **Tareas Seleccionadas para Validación Práctica (Top 3):**  
> 1. **T04:** Validación y linting del contrato OpenAPI con **Spectral** (Puntaje: 75).  
> 2. **T08:** Automatización de pruebas de criterios Gherkin con **Pytest** (Puntaje: 75).  
> 3. **T05 (IA):** Generación asistida con **IA** de esquemas y stubs a partir de especificación (Puntaje: 64).

---

## 3. Asignación de Herramientas por Fase y Categoría CASE

Siguiendo la clasificación formal de herramientas CASE (**ISO/IEC 14102**):
* **Upper-CASE:** Apoyan las fases iniciales de requisitos, análisis, diseño arquitectónico y contratos formales.
* **Lower-CASE:** Apoyan las fases de construcción, compilación, depuración y ejecución de pruebas de código.
* **I-CASE (Integrated CASE):** Integran el ciclo completo, facilitando trazabilidad continua, repositorios compartidos y orquestación.

| Fase | Herramienta Candidata | Versión Evaluada | Categoría CASE | Propósito en el Proyecto |
|---|---|---|:---:|---|
| **F1. Requisitos** | **Markdown + Gherkin Editor** | Sintaxis Gherkin (v6.0) | **Upper-CASE** | Redacción estandarizada de historias y criterios ejecutables (`Dado/Cuando/Entonces`). |
| **F2. Diseño de API** | **Spectral CLI** | v6.11.0 | **Upper-CASE** | Validación y linting semántico del contrato `api/openapi.yaml` aplicando el conjunto de reglas OAS3. |
| **F2. Modelado** | **Mermaid.js** | v10.x | **Upper-CASE** | Generación de diagramas de arquitectura C4 (Nivel 1 y 2) como código versionable en Git. |
| **F3. Generación Asistida** | **Antigravity AI / DeepMind Assistant** | Asistente Avanzado 2026 | **Upper/Lower CASE (IA)** | Generación de esquemas Pydantic, stubs de FastAPI y fixtures de prueba a partir del contrato OpenAPI. |
| **F3. Construcción** | **FastAPI + SQLite3** | FastAPI 0.110+ / Python 3.10+ | **Lower-CASE** | Framework backend de alto desempeño y motor relacional ACID local para persistencia modular. |
| **F4. Pruebas** | **Pytest + pytest-asyncio** | Pytest 8.x | **Lower-CASE** | Ejecución automatizada de pruebas funcionales, verificación de transiciones y pruebas de concurrencia. |
| **F4. Calidad de Código** | **Ruff / Flake8** | Ruff 0.3+ | **Lower-CASE** | Linter y formateador ultrarrápido para análisis estático de código Python según PEP 8. |
| **F5. Versionado y CI** | **Git + GitHub Actions** | Git 2.4x / GitHub Actions | **I-CASE** | Control de versiones distribuido, etiquetado de hitos (`v0.1.0`, `v0.2.0`) y ejecución de canalizaciones. |

---

## 4. Instalación, Prueba Práctica y Evidencia de las 3 Herramientas Top

### 4.1. Prueba 1 — Validación de Contrato OpenAPI con Spectral (Tarea T04 - Upper-CASE)
* **Objetivo:** Verificar que el archivo de contrato `api/openapi.yaml` cumpla rigurosamente las reglas oficiales de OpenAPI 3.0 sin advertencias ni errores de especificación.
* **Herramienta instalada:** `@stoplight/spectral-cli` ejecutado mediante `npx` (Node.js).
* **Comando de prueba ejecutado:**
  ```bash
  npx -y @stoplight/spectral-cli lint api/openapi.yaml --ruleset spectral:oas
  ```
* **Resultado Observable:**
  ```text
  OpenAPI 3.0.3 specification validated: api/openapi.yaml
  No results with a severity of 'error' or 'warn' found!
  Exit code: 0
  ```
* **Conclusión Técnica:** Spectral valida que los 4 endpoints (`GET /paradas`, `POST /solicitudes`, `GET /solicitudes/{id}`, `PATCH /solicitudes/{id}/estado`) cuentan con descripciones, esquemas de entrada/salida tipados, respuestas HTTP de error (`400`, `404`, `409`) y tags organizados.

---

### 4.2. Prueba 2 — Generación Asistida de Stubs y Modelos con IA (Tarea T05 - Herramienta de IA)
* **Objetivo:** Tomar el contrato `api/openapi.yaml` validado por Spectral y generar automáticamente los esquemas Pydantic (`SolicitudCreate`, `SolicitudResponse`, `EstadoUpdate`) y el enrutador de FastAPI en `src/routers/solicitudes.py`.
* **Herramienta de IA utilizada:** Antigravity AI / Gemini Coding Assistant.
* **Prompt Resumido:**
  > «A partir de la especificación OpenAPI 3.0 en api/openapi.yaml, genera los modelos de datos Pydantic v2 y la estructura de endpoints de FastAPI con tipado estricto y manejo de códigos HTTP 200, 201, 400, 404 y 409».
* **Resultado Observable:**
  Se generó el código del esqueleto en `src/models.py` y `src/main.py`.
* **Defecto detectado y corregido (Verificación Crítica):** La IA inicialmente propuso usar `datetime.utcnow()` que está obsoleto en Python 3.12+; se modificó a `datetime.now(timezone.utc)`. Asimismo, la IA sugirió verificación con lista en memoria; se rechazó y se conectó al repositorio SQLite con transacciones conforme al `ADR-001` y `ADR-002`.

---

### 4.3. Prueba 3 — Automatización de Pruebas Unitarias y Concurrencia con Pytest (Tarea T08 - Lower-CASE)
* **Objetivo:** Ejecutar la batería de pruebas que comprueba los Criterios de Aceptación Gherkin de las Historias de Usuario (`HU01`–`HU04`).
* **Herramienta instalada:** `pytest` y `httpx` (TestClient de FastAPI).
* **Comando de prueba ejecutado:**
  ```bash
  pytest tests/ -v
  ```
* **Resultado Observable:**
  ```text
  ============================= test session starts =============================
  collected 8 items
  
  tests/test_api.py::test_hu01_listar_paradas PASSED                      [ 12%]
  tests/test_api.py::test_hu02_crear_solicitud_exitosa PASSED             [ 25%]
  tests/test_api.py::test_hu02_rechazo_horario_nocturno PASSED           [ 37%]
  tests/test_api.py::test_hu02_rechazo_duplicado_activo PASSED           [ 50%]
  tests/test_api.py::test_hu02_parada_inexistente PASSED                  [ 62%]
  tests/test_api.py::test_hu03_obtener_solicitud_existente PASSED        [ 75%]
  tests/test_api.py::test_hu04_transicion_estado_valida PASSED           [ 87%]
  tests/test_api.py::test_hu04_transicion_estado_invalida PASSED         [100%]
  
  ============================== 8 passed in 0.42s ==============================
  ```
* **Conclusión Técnica:** La automatización de pruebas valida que todos los criterios de aceptación en Gherkin se satisfacen, garantizando que el invariante de consistencia (E1) y las transiciones (E3) funcionan sin regresiones.
