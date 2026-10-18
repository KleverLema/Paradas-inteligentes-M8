# Registro de uso y contraste crítico de IA — Semana 1

**Advertencia:** este registro documenta el uso realizado hasta producir el borrador. La aceptación definitiva de decisiones y las pruebas corresponden al **equipo**, no a una IA. No se han añadido datos personales reales ni credenciales.

## Registro preliminar real

| Actividad | Herramienta / versión | Prompt o solicitud resumida | Salida / hallazgo de IA | Evidencia verificada | Decisión del equipo |
|---|---|---|---|---|---|
| Analizar materiales y preparar dossier del caso propio | ChatGPT (GPT-6), 15/10/2026 | «Revisa la práctica de arquitectura y el prototipo de solicitudes de parada para preparar un dosier centrado en el módulo REST». | Delimitar el módulo de solicitudes; documentar estado previo y mejoras propuestas. | Código original consultado: el prototipo de solicitudes no implementa ETA ni GPS. | **Pendiente de ratificación** por el grupo. |
| Identificar limitaciones técnicas | ChatGPT (GPT-6) | Analizar la API existente frente a escenarios de arquitectura. | Riesgos de falta de persistencia, concurrencia y autorización. | Código: `dict`, `any(...)` antes de inserción, ausencia de dependencias de autenticación. | **Pendiente:** decidir si incorporar E1/E2/E4. |
| Revisar escenarios, ADR, C4 y matriz | ChatGPT (GPT-6) | Elaborar borrador de seis escenarios medibles, comparar estilos y exponer objeciones. | Propone E1–E6, SQLite transaccional, unicidad parcial y monolito modular. | Verificación lógica del texto y matriz; **ninguna de estas mejoras está implementada todavía**. | **Pendiente:** validación grupal y ajustes. |

## Objeciones críticas — abogado del diablo (NO una auditoría de producción)

| Objeción | Escenario | Sesgo o supuesto cuestionado | Evidencia que cambiaría la decisión | Acción propuesta |
|---|---|---|---|---|
| E1 se considera principal, pero la API no se ha sometido a concurrencia real | E1 | Confiar en un `any(...)` secuencial | Test de 100 peticiones simultáneas y revisión SQL | Aceptar el riesgo; mantener ADR-002 propuesto |
| SQLite no es apropiado para escalar a varias instancias | E2, E5 | Suponer una sola instancia por siempre | Requisito de despliegues múltiples y carga en producción | Declarar supuesto; reabrir ADR-001 si cambia |
| La API actual puede exponer identificadores a consumidores externos | E4 | Confundir pruebas locales con servicio seguro | Pruebas 50 intentos sin rol y auditoría | Declarar brecha y no usar datos reales |
| Las funciones ETA/GPS y la API de solicitudes podrían mezclarse | Alcance | Dar por hecho que un prototipo implementa todo el SRS | Confirmación del alcance por el equipo y revisión de la documentación | Mantener alcance reducido y documentar exclusiones |

## Control humano por completar antes de la entrega

- Fecha de revisión del grupo: **[PENDIENTE]**.
- Conclusiones de validación técnica: **[PENDIENTE]**.
- Objeciones aceptadas: **[PENDIENTE]**.
- Objeciones modificadas (peso, escenario, diagrama o ADR): **[PENDIENTE]**.
- Objeciones rechazadas **con evidencia verificable**: **[PENDIENTE]**.
- URL del commit después de revisión: **[PENDIENTE]**.

**Política de honestidad académica:** no declarar que el equipo aprobó una decisión, realizó una revisión cruzada ni implementó controles de concurrencia/persistencia/autorización sin haberlo hecho. Verificar contenido jurídico y normativo en fuentes oficiales cuando aplique.
