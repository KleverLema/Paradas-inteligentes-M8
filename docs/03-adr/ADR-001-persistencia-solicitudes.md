# ADR-001 — Persistencia de solicitudes

**Fecha:** 18/10/2026  
**Estado:** Seleccionada para la arquitectura objetivo; no implementada en la API de referencia.  
**Drivers:** D2 y D5 · **Escenarios:** E2, E6 · **Restricción:** R4.

## Contexto

La API FastAPI almacena registros en `solicitudes: Dict[int, SolicitudOut] = {}`. Ese mecanismo permite desarrollar reglas de negocio con pocas dependencias, pero los registros se pierden cuando termina el proceso. El escenario E2 establece que 100 solicitudes deben recuperarse tras un reinicio.

## Alternativas

| Alternativa | Ventaja | Limitación |
|---|---|---|
| Diccionario en memoria | Sencillo para demostración | No cumple la persistencia E2 |
| SQLite | Transacciones, archivo local, operación de una instancia | Escalamiento horizontal y alta disponibilidad limitados |
| PostgreSQL | Mayor flexibilidad de operación multiinstancia | Administración y recursos adicionales |

## Decisión

Seleccionar **SQLite** para la primera etapa y aislar la persistencia mediante un módulo repositorio separado de los endpoints FastAPI. Registrar solicitudes y transiciones como operaciones transaccionales.

## Consecuencias y trade-offs

- Mejora la durabilidad y habilita el diseño de unicidad transaccional de ADR-002.
- Añade esquema, migraciones y respaldos a una API que antes funcionaba sin base de datos.
- Reduce complejidad operativa frente a PostgreSQL para una sola instancia, pero limita una futura distribución en múltiples réplicas.

## Evidencia y criterio de comprobación

La limitación proviene del almacenamiento en memoria descrito en [evidencia técnica](../05-evidencia-tecnica.md). El cumplimiento de E2 se determinará con 100 registros antes y después de un reinicio. Esta decisión aparece en [C4 nivel 2](../02-vistas-c4/c4-nivel2.md).
