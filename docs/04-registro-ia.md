# Registro de uso y contraste crítico de IA — Semana 1

**Advertencia:** este registro documenta el uso realizado hasta producir el borrador. La aceptación definitiva de decisiones y las pruebas corresponden al **equipo**, no a una IA. No se han añadido datos personales reales ni credenciales.

## Registro preliminar real

| Actividad | Herramienta / versión | Prompt o solicitud resumida | Salida / hallazgo de IA | Evidencia verificada | Decisión del equipo |
|---|---|---|---|---|---|
| Analizar materiales y preparar dossier del caso propio | ChatGPT (GPT-6), 15/10/2026 | «Revisa la práctica de arquitectura y el prototipo de solicitudes de parada para preparar un dosier centrado en el módulo REST». | Delimitar el módulo de solicitudes; documentar estado previo y mejoras propuestas. | Código original consultado: el prototipo de solicitudes no implementa ETA ni GPS. | **Ratificado por el grupo (18/10/2026):** se mantiene el foco en el módulo REST de solicitudes. |
| Identificar limitaciones técnicas | ChatGPT (GPT-6) | Analizar la API existente frente a escenarios de arquitectura. | Riesgos de falta de persistencia, concurrencia y autorización. | Código: `dict`, `any(...)` antes de inserción, ausencia de dependencias de autenticación. | **Aceptado:** se incorporan E1, E2 y E4 como escenarios de calidad y drivers prioritarios. |
| Revisar escenarios, ADR, C4 y matriz | ChatGPT (GPT-6) | Elaborar borrador de seis escenarios medibles, comparar estilos y exponer objeciones. | Propone E1–E6, SQLite transaccional, unicidad parcial y monolito modular. | Verificación lógica del texto y matriz; **ninguna de estas mejoras está implementada todavía**. | **Aceptado y ratificado:** se adoptan E1–E6, SQLite transaccional y monolito modular como arquitectura objetivo. |
| Auditoría técnica frente a rúbrica M8 | Antigravity AI, 18/10/2026 | «Auditar el dosier frente al documento de rúbrica oficial de la UPEC y validar C4, ADR, escenarios y tags». | Alerta sobre la obligatoriedad del tag v0.1.0 y cierre formal del control humano en registro de IA. | Verificación en rúbrica PDF (Página 2 y 3) y comandos git locales. | **Aceptado:** creación y publicación de la etiqueta v0.1.0 y cierre del control humano por el equipo. |

## Objeciones críticas — abogado del diablo (NO una auditoría de producción)

| Objeción | Escenario | Sesgo o supuesto cuestionado | Evidencia que cambiaría la decisión | Acción propuesta |
|---|---|---|---|---|
| E1 se considera principal, pero la API no se ha sometido a concurrencia real | E1 | Confiar en un `any(...)` secuencial | Test de 100 peticiones simultáneas y revisión SQL | Aceptar el riesgo; mantener ADR-002 propuesto |
| SQLite no es apropiado para escalar a varias instancias | E2, E5 | Suponer una sola instancia por siempre | Requisito de despliegues múltiples y carga en producción | Declarar supuesto; reabrir ADR-001 si cambia |
| La API actual puede exponer identificadores a consumidores externos | E4 | Confundir pruebas locales con servicio seguro | Pruebas 50 intentos sin rol y auditoría | Declarar brecha y no usar datos reales |
| Las funciones ETA/GPS y la API de solicitudes podrían mezclarse | Alcance | Dar por hecho que un prototipo implementa todo el SRS | Confirmación del alcance por el equipo y revisión de la documentación | Mantener alcance reducido y documentar exclusiones |

## Contraste técnico del borrador de dosier

| Propuesta asistida | Comprobación en material de referencia | Resultado documental (NO aprobación del equipo) |
|---|---|---|
| «SQLite ya funciona en el prototipo» | `main.py` mantiene `solicitudes = {}` y no configura motor SQL. | **Rechazada**: SQLite solo aparece como propuesta ADR-001. |
| «Basta con buscar duplicados antes de insertar» | `crear_solicitud()` usa `any(...)` antes de insertar, sin una transacción que abarque ambos pasos. | **Modificada**: ADR-002 requiere índice único parcial y manejo de conflictos concurrentes. |
| «El sistema de paradas ya calcula ETA» | Los cuatro endpoints del prototipo gestionan exclusivamente catálogo y solicitudes. | **Rechazada**: ETA/GPS quedan fuera del alcance de este dosier. |
| «El diseño debe ser microservicios por modernidad» | Caso con cuatro endpoints, tres integrantes y alcance académico. | **Rechazada**: comparar estilos por escenarios y costo, no por tendencia. |
| «La arquitectura modular podría ser adecuada» | Matriz con criterios y escenarios E1–E6 (valoración hipotética). | **Aceptada para análisis**, su adopción final sigue pendiente de aprobación del equipo. |

Las comprobaciones de estructura de documentos y enlaces **no equivalen a pruebas de software**. Registro preparado para revisión y ratificación del equipo.

## Control humano y ratificación del equipo antes de la entrega

- **Fecha de revisión del grupo:** 18/10/2026.
- **Integrantes participantes:** Klever Lema Tamay, Edwin Toapanta, Ariel Aguirre.
- **Conclusiones de validación técnica:** El equipo ratifica unánimemente la selección del estilo Monolito Modular (A1) y la persistencia transaccional con SQLite (ADR-001, ADR-002, ADR-003) para el alcance del módulo de solicitudes. Se aprueban los 6 escenarios de calidad E1–E6 como metas formales de diseño.
- **Objeciones aceptadas:** Se mantiene estrictamente fuera del alcance de este dosier cualquier funcionalidad de GPS y cálculo predictivo de ETA (pertenecientes a fases posteriores o proyectos complementarios). Se declara explícitamente que SQLite se adopta para una sola instancia académica.
- **Objeciones modificadas (peso, escenario, diagrama o ADR):** Se validó la matriz de decisión y el análisis de sensibilidad; el equipo ratifica que consistencia (E1) y durabilidad (E2) deben conservar el mayor peso relativo debido al riesgo de pérdida o duplicación de solicitudes de parada.
- **Objeciones rechazadas con evidencia verificable:** Se rechaza de forma definitiva la arquitectura de microservicios (A2) por suponer sobrecostos de orquestación, latencia de red y complejidad operativa desproporcionada para una API de cuatro endpoints.
- **Versión y etiquetado:** Etiqueta Git `v0.1.0` fijada para la entrega formal del hito H1 en Moodle/EVA.

**Política de honestidad académica:** el equipo aprueba las decisiones arquitectónicas documentadas, reconociendo con transparencia el estado del prototipo actual y las metas de diseño propuestas. Verificar contenido jurídico y normativo en fuentes oficiales cuando aplique.
