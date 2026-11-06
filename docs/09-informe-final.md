# Informe final integrador — Semana 4 (Hito H4)

**Maestría en Ingeniería de Software · Módulo 8: Automatización de procesos de software**  
**Proyecto:** Paradas Inteligentes — API de solicitudes de parada  
**Entrega:** viernes 06/11/2026, 23:59, según rúbrica de Semana 4  
**Estado:** Borrador integrador con evidencias verificadas y tareas de cierre explícitas.  
**Versión de preparación:** 05/11/2026.

> Este informe enlaza los artefactos que ya existen en el repositorio. No sustituye la ejecución ni el cierre de PR pendientes. Una aprobación de CI prueba que se ejecutaron los controles definidos; no demuestra ausencia de defectos ni cumplimiento de objetivos de carga no medidos.

## 1. Resumen del caso y alcance

Paradas Inteligentes es un prototipo académico de API REST de gestión de solicitudes para transporte urbano. Permite consultar un catálogo inicial de cinco paradas, registrar solicitudes, consultarlas por identificador y cambiar sus estados dentro de una máquina de estados controlada. El propósito de la automatización no es añadir más funcionalidades sino verificar de forma repetible el software y gobernar su evolución mediante Git, revisiones y controles de calidad.

La implementación usa Python 3.14 como entorno verificado de la práctica actual, FastAPI, Pydantic, SQLite y pytest. Los cuatro endpoints documentados son:

| Operación | Propósito | Archivo principal |
|---|---|---|
| `GET /paradas` | Consultar el catálogo. | [`src/main.py`](../src/main.py) |
| `POST /solicitudes` | Registrar una petición válida y sin duplicado activo. | [`src/main.py`](../src/main.py), [`src/repository.py`](../src/repository.py) |
| `GET /solicitudes/{id_solicitud}` | Consultar el estado vigente. | [`src/main.py`](../src/main.py) |
| `PATCH /solicitudes/{id_solicitud}/estado` | Aplicar transiciones permitidas. | [`src/main.py`](../src/main.py), [`src/repository.py`](../src/repository.py) |

No se afirma disponer de GPS en tiempo real, ETA predictivo, aplicación móvil, autenticación productiva ni despliegue continuo al servidor: no hay evidencia de esas funciones dentro del alcance verificado.

## 2. Arquitectura: drivers, escenarios, vistas y decisiones

El dossier de arquitectura se encuentra en [`docs/01-contexto-y-drivers.md`](01-contexto-y-drivers.md), las vistas están en [`docs/02-vistas-c4/`](02-vistas-c4/) y las decisiones en [`docs/03-adr/`](03-adr/).

Los drivers priorizados son: **D1** unicidad e integridad ante concurrencia; **D2** persistencia tras reinicio; **D3** seguridad de acceso; **D4** desempeño; y **D5** mantenibilidad. Se formularon los escenarios **E1–E6** con condiciones y metas de calidad, que no deben confundirse con resultados ejecutados.

- **ADR-001 — SQLite transaccional.** Se adoptó persistencia local frente al diccionario en memoria para recuperar solicitudes y acotar la infraestructura. Su límite es el alcance académico de instancia única y los problemas de contención si crece la carga.
- **ADR-002 — Unicidad activa.** Se priorizó el control transaccional para impedir dos solicitudes activas de la misma pareja pasajero–parada. Hay prueba de duplicado secuencial; el objetivo E1 de 100 solicitudes simultáneas todavía necesita prueba específica.
- **ADR-003 — Monolito modular.** Se escogió por sencillez de operación y mantenimiento para cuatro endpoints, separando API, repositorio, persistencia y modelos. El costo es que algunos acoplamientos requerirán vigilancia al crecer.
- **ADR-004 — Git como control de versiones.** Repositorio distribuido y colaboración mediante ramas, PR y revisión cruzada; la decisión está respaldada por [`docs/08-matriz-git-vs-svn.md`](08-matriz-git-vs-svn.md).

### Valoración crítica

La arquitectura resuelve adecuadamente el alcance pequeño sin añadir infraestructura innecesaria. Su riesgo más visible en las evidencias actuales es que no todas las metas no funcionales han sido demostradas: no hay resultados verificables de prueba de carga E5 ni de autenticación E4. Además, las pruebas de horario usan valores UTC; es prudente verificar expresamente la zona operativa (`America/Guayaquil`) antes de afirmar cobertura del horario local.

## 3. Cadena CASE y selección de herramientas

La cadena CASE se describe en [`docs/06-mapa-toolchain.md`](06-mapa-toolchain.md) y se justifica en [`docs/08-matriz-evaluacion-case.md`](08-matriz-evaluacion-case.md).

| Fase | Herramienta | Aporte | Comprobación real |
|---|---|---|---|
| Analizar/diseñar | C4 y ADR en Markdown | Decisiones examinables y versionables | Artefactos enlazados en `docs/`. |
| Especificar | OpenAPI 3.0.3 | Contrato explícito de cuatro endpoints | Validación con Spectral (sin warnings, salida `0`). |
| Implementar | FastAPI, Pydantic, SQLite | API y reglas de negocio | Suite pytest. |
| Probar | Ruff, pytest | Detección de errores simples y regresiones | Ruff aprobado y 9/9 tests locales aprobados. |
| Documentar | Redocly | HTML generado desde OpenAPI | `docs-generada/index.html` compiló localmente y se visualizó. |
| Integrar | GitHub Actions | Ejecutar controles en runner limpio por PR | PR #19 (Ruff/pytest); PR #20 (Spectral/Redocly). |
| Gobernar | Git, PR, branch protection | Revisión y trazabilidad | PR #19 aprobado por Ariel y fusionado; PR #20 revisión solicitada. |

**Limitación:** las herramientas elegidas no sustituyen revisión humana de diseño, seguridad o requisitos. Un resultado verde es válido solo para las reglas configuradas.

## 4. Versionamiento y repositorio gobernado

El flujo elegido fue **rama → commits atómicos → push → PR → validaciones automáticas → revisión cruzada → merge a `main`**. Se documentó un conflicto deliberado de Git en [`docs/09-reporte-conflicto.md`](09-reporte-conflicto.md), y el análisis de Git frente a SVN se respalda en [`ADR-004`](03-adr/ADR-004-seleccion-git.md).

| Hito de historial | Evidencia | Interpretación |
|---|---|---|
| H3 / v0.3.0 | [Release](https://github.com/KleverLema/Paradas-inteligentes-M8/releases/tag/v0.3.0) | Referencia etiquetada de la Semana 3. |
| PR #19 | [Enlace](https://github.com/KleverLema/Paradas-inteligentes-M8/pull/19) | Agrega `.github/workflows/ci.yml` y corrige uso de variable en tests; aprobado y fusionado. |
| Merge #19 | `72d4996` | Evidencia de integración en `main`. |
| PR #20 | [Enlace](https://github.com/KleverLema/Paradas-inteligentes-M8/pull/20) | Agrega Spectral, Redocly, lockfile y job `contrato`; **en revisión** al redactar. |
| CI en PR #20 | [Actions](https://github.com/KleverLema/Paradas-inteligentes-M8/actions) | Dos jobs aprobados en una ejecución de 20 segundos. |

**Actualización obligatoria antes de entregar:** comprobar si PR #20 fue aprobado/fusionado, anotar su commit de merge y obtener la evidencia de CI sobre la rama `main`.

## 5. Automatización, pipeline y quality gates

El archivo central es [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). En PR a `main`, GitHub Actions ejecuta jobs de un runner Linux con permisos mínimos `contents: read`.

**Pipeline integrado (PR #19):** job `calidad` instala dependencias de Python, ejecuta `ruff check src tests` y después `pytest tests/ -v`. La prueba local reportó **9 passed**, y los pasos Ruff/pytest del workflow se observaron en verde.

**Ampliación (PR #20):** job `contrato` instala dependencias npm desde `package-lock.json` con `npm ci`, ejecuta Spectral sobre `api/openapi.yaml` con `--fail-severity=warn` y genera documentación con Redocly. Este job se observó en verde junto al de `calidad` dentro del PR #20.

```text
Pull Request a main
      |
      +-- Job calidad: Python --> Ruff --> pytest
      |
      +-- Job contrato: Node.js --> npm ci --> Spectral --> Redocly
      |
     Checks en GitHub --> revisión humana --> merge si se cumplen todas las reglas
```

### Controles pendientes exigidos por la rúbrica

- [ ] Incorporar cobertura de código y registrar porcentaje/umbral medido.
- [ ] Añadir análisis estático de seguridad apropiado para Python (p. ej., CodeQL).
- [ ] Escanear secretos y dependencias de Python y Node.js en cada PR (no solo instalación local).
- [ ] Verificar fijación segura de acciones y permisos mínimos.
- [ ] Configurar **checks obligatorios** en la protección de `main` y confirmar que no existe bypass.
- [ ] Provocar una **falla controlada y reversible** (por ejemplo, fallo de lint en rama separada), capturar check rojo y bloqueo de merge, corregir, obtener verde y cerrar el experimento.
- [ ] Agregar badges de CI al README y revisar su enlace.

No afirmar que todos esos controles ya existen. La captura de dos jobs verdes demuestra la ejecución de esos dos jobs, no el cumplimiento total de la rúbrica.

## 6. Esqueleto ejecutable y pruebas ligadas a criterios

El módulo se inicia localmente con una aplicación FastAPI; la documentación interactiva se encuentra en `/docs` cuando el servidor está en ejecución. Las pruebas se ubican en [`tests/test_api.py`](../tests/test_api.py) y están relacionadas con HU01–HU04 y sus criterios. La suite actual contiene nueve pruebas:

- HU01: consultar cinco paradas y validar campos.
- HU02: crear solicitud; rechazar horario fuera de servicio, duplicado activo y parada inexistente.
- HU03: consultar solicitud existente e inexistente.
- HU04: transiciones válidas e inválidas.

**Resultado evidenciado:** nueve pruebas aprobadas localmente; Ruff sin errores; PR #19 y PR #20 con jobs de prueba aprobados. Hay advertencias de Pydantic y pytest-asyncio que no invalidan el éxito de las pruebas, pero conviene documentarlas y atenderlas planificadamente.

**Brechas reales:** falta prueba dedicada CA03.3 (recuperación tras reinicio), CA04.4 (actualización de inexistente), concurrencia efectiva E1 de 100 solicitudes y objetivos de rendimiento/seguridad no implementados. La matriz detallada y la clasificación de cobertura están en [`docs/05-trazabilidad.md`](05-trazabilidad.md).

## 7. Métricas aproximadas tipo DORA — fuentes y límites

Se explicita el origen y método para evitar atribuir métricas de producción a simples merges o ejecuciones de CI. **La captura de Actions evidencia una corrida de 20 segundos, que es duración de CI, NO tiempo de entrega de cambios ni frecuencia de despliegue.**

| Métrica | Fórmula o aproximación | Datos requeridos | Situación comprobable |
|---|---|---|---|
| Tiempo de entrega de cambios | Fecha de despliegue − fecha del commit (o PR abierto → merge como **proxy de integración**, claramente rotulado) | Timestamps de commit, PR, merge y despliegue | Sin evento de despliegue documentado: DORA real **no calculable**. Se puede calcular proxy de integración al recuperar datos. |
| Frecuencia de despliegue | Número de despliegues exitosos / periodo | Registro de despliegues de servicio | **No calculable** con solo PR y CI. |
| Tiempo de recuperación | Hora de recuperación − hora de incidente | Incidentes y correcciones en producción | **No calculable** sin incidentes fechados. |
| Tasa de fallos de cambios | Despliegues que requieren rollback/hotfix / total de despliegues | Eventos de despliegue y fallos | **No calculable** sin despliegues. |
| Retrabajo por despliegue | Cambios no planificados de corrección / total, según definición docente | Etiquetas de incidencias/hotfixes y despliegues | Necesita clasificación y timestamps; no inventar porcentaje. |

**Indicadores observados, no DORA:** 9 de 9 pruebas existentes aprobadas; job CI en PR #20 con dos trabajos verdes, duración total reportada de 20 s; PR #19 revisado e integrado; PR #20 en revisión al redactar. Si el equipo calcula un indicador proxy mediante GitHub, anotar el intervalo, fórmula, fuente exacta y limitaciones.

**Procedimiento reproducible para documentar métricas:** exportar lista de PR y commits (`git log --date=iso --pretty=...` y vista de PR GitHub); anotar fechas de apertura, merge y, solo cuando existan, despliegue; calcular mediana de tiempos y conteos con el período declarado; no equiparar merge con producción a menos que haya despliegue automático verificado.

## 8. Uso responsable de inteligencia artificial

El registro histórico está en [`docs/04-registro-ia.md`](04-registro-ia.md). Durante Semana 4 se utilizó asistencia de ChatGPT (OpenAI, modelo GPT-6) para interpretar la rúbrica, revisar decisiones, proponer comandos Git y elaborar borradores del workflow y de documentación. El equipo debe confirmar y registrar qué sugerencias aceptó, modificó o rechazó mediante evidencia real, y evitar introducir datos personales o credenciales.

**Verificaciones reales aplicadas a las propuestas:** ejecución local de `ruff`, `pytest`, `spectral` y `redocly`; inspección de `git diff --cached`; revisión del PR por un segundo integrante; logs de GitHub Actions con dos trabajos aprobados. **Aspectos a completar:** registrar la revisión explícita de permisos mínimos, fijación de acciones, detección de secretos y resultado de prueba de fallo controlado. Esas revisiones deben hacerse, no declararse retrospectivamente.

| Elemento sugerido con IA | Decisión y evidencia |
|---|---|
| Corregir `client` no utilizado | **Modificado** de `client, repo` a `_, repo` en test; Ruff y nueve tests posteriores aprobados. |
| CI con Ruff y pytest | **Aceptado tras verificación** local y GitHub Actions; merge PR #19. |
| Validación Spectral | **Aceptado tras verificación** `--fail-severity=warn`, código de salida 0 y CI PR #20 verde. |
| Generar HTML con Redocly | **Aceptado tras verificación** de `docs-generada/index.html`; CI PR #20 verde. |
| Cobertura / análisis de seguridad / métricas DORA | **No declarados como implementados** mientras falten datos y verificaciones. |

## 9. Análisis crítico y lecciones aprendidas

**Qué funcionó.** Las verificaciones locales previas evitaron publicar YAML y pruebas no revisadas; la revisión cruzada en PR #19 añadió control humano; el pipeline convirtió controles repetitivos en trabajo automático; OpenAPI permitió generar una página de documentación sin duplicar la especificación.

**Qué no funcionó inicialmente.** Se detectó `RUF059` por variable no usada, luego corregida; el workflow inicial aún no contenía puertas de contrato ni controles de seguridad; y el formato UTF-8 se mostró con caracteres incorrectos al leerlo sin `-Encoding utf8` en PowerShell, aunque el archivo era válido. Parte de la evaluación de requisitos de calidad permanece incompleta porque una suite corta no prueba automáticamente los escenarios de escala.

**Qué cambiaríamos.** Establecer desde el comienzo una matriz HU/CA → prueba → gate; fijar versiones de herramientas y de acciones; tratar la seguridad como requisito verificable recurrente; añadir pruebas de persistencia, concurrencia y límites de estado; configurar el ruleset con los nombres exactos de cada check; y recoger tiempos y eventos desde el inicio para obtener métricas DORA reales.

**Límites.** El sistema es un prototipo académico y una ejecución verde no equivale a certificación de seguridad, cobertura suficiente o despliegue productivo. La colaboración y la automatización tienen valor únicamente si las evidencias pueden comprobarse en archivos, PR, commits y logs existentes.

## 10. Evidencias a enseñar en la defensa

1. Abrir el [repositorio](https://github.com/KleverLema/Paradas-inteligentes-M8) y señalar arquitectura, ADR, contratos, pruebas y documentos.
2. Mostrar `api/openapi.yaml` y la documentación generada; explicar por qué Spectral valida el contrato.
3. Ejecutar API o mostrar `/docs` y una transacción válida junto a rechazo de duplicado y transición ilegal.
4. Mostrar `tests/test_api.py`, `pytest` y diferencia entre objetivos E1–E6 y pruebas realmente ejecutadas.
5. Mostrar [PR #19](https://github.com/KleverLema/Paradas-inteligentes-M8/pull/19) con aprobación, merge y ejecución de CI.
6. Mostrar [PR #20](https://github.com/KleverLema/Paradas-inteligentes-M8/pull/20) y ejecución de ambos jobs; actualizar su estado final.
7. Explicar las puertas pendientes o mostrar su incorporación, incluyendo el check rojo y bloqueo si se completó la práctica.
8. Mostrar la [matriz de trazabilidad](05-trazabilidad.md), el [registro de IA](04-registro-ia.md) y la tabla de métricas con limitaciones honestas.

## 11. Comprobaciones antes de enviar el commit final

- [ ] Confirmar PR #20 fusionado y checks de `main` verdes.
- [ ] Completar puertas de seguridad, análisis estático, cobertura y requisito de checks obligatorios.
- [ ] Registrar fallo controlado y corrección con enlaces a Actions.
- [ ] Actualizar registro IA (herramienta/versión, prompts resumidos, verificación, decisión).
- [ ] Sustituir los estados «pendiente» por evidencia **solo** cuando exista.
- [ ] Revisar de forma cruzada las rutas de este informe y la matriz.
- [ ] Publicar commit final y facilitar a Moodle/EVA el **mismo commit de grupo**, conforme instrucciones del docente.

---

### Referencias internas

- [Dossier de arquitectura](01-contexto-y-drivers.md) y [ADR](03-adr/)
- [Historias y criterios](07-historias-y-criterios.md)
- [Mapa CASE](06-mapa-toolchain.md) y [matriz de evaluación](08-matriz-evaluacion-case.md)
- [Git frente a SVN](08-matriz-git-vs-svn.md) y [reporte de conflicto](09-reporte-conflicto.md)
- [Contrato OpenAPI](../api/openapi.yaml), [código](../src/), [pruebas](../tests/), [pipeline](../.github/workflows/ci.yml)
