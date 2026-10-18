# ADR-003 — Adoptar monolito modular para la API académica

- **Estado:** Propuesto — pendiente de aprobación por equipo.
- **Fecha:** 15/10/2026.
- **Drivers:** D1–D5. **Escenarios:** E1–E6. **Restricciones:** R3–R6.

## Contexto

La API suministrada está contenida en `main.py`, sin separación física entre rutas, esquemas, reglas y almacenamiento. Su alcance actual es una sola entidad, cuatro operaciones REST principales, catálogo fijo y máquina de estados. La primera semana requiere documentar arquitectura; el docente no exige reprogramar la API para completar el dosier. Una eventual implementación debe priorizar fiabilidad (E1–E3), protección de datos (E4), rendimiento (E5) y facilidad de mantenimiento (E6).

## Alternativas de estilo

- **A1 — Monolito modular (preferida):** una aplicación FastAPI desplegable, con paquetes internos para API, dominio, casos de uso y repositorio de datos; una SQLite transaccional en etapa académica.
- **A2 — Microservicios:** servicio de solicitudes, servicio de catálogo/identidad y almacenamiento/integración administrados de forma independiente, mayor complejidad de red y despliegue.
- **Estado actual, no competidor como solución objetivo:** un solo `main.py` con `dict` (referencia de partida, no alcanza E1/E2/E4).

## Matriz de decisión

La evaluación detallada y sus justificaciones están en [`matriz-decision.md`](matriz-decision.md). Con pesos ilustrativos **A1 = 4,25 / 5** y **A2 = 3,70 / 5**. Las calificaciones son razonadas, **no resultados de pruebas de rendimiento**.

## Decisión propuesta

Seleccionar **A1, monolito modular**: conservar un proceso FastAPI, separar lógica de negocio y acceso a datos, incorporar SQLite (ADR-001) y unicidad transaccional (ADR-002). Evitar microservicios y broker hasta demostrar un requisito real que los justifique.

## Alternativa descartada

A2 microservicios: aportaría escalabilidad independiente para un futuro mayor, pero requiere varios despliegues, identidades entre servicios y manejo distribuido innecesarios para cuatro endpoints académicos y el equipo disponible.

## Consecuencias positivas

- Menos infraestructura que operar, menor carga de aprendizaje y despliegue más sencillo.
- Mantiene el contrato HTTP existente y permite modularizar de manera incremental.
- Las transacciones de solicitudes quedan dentro de un almacenamiento consistente.

## Consecuencias negativas / trade-offs

- No escala por componentes independientemente como microservicios.
- Persistencia SQLite local no es adecuado asumirla para múltiples instancias distribuidas sin rediseño.
- Modularizar exige pruebas de regresión y disciplina de límites entre paquetes.
- E4 requerirá una solución de autenticación y autorización que **no existe** en el prototipo suministrado.

## Sensibilidad y riesgos

Si en otro alcance el sistema pasa a múltiples instancias, varias ciudades, concurrencia elevada o integración en tiempo real con GPS/ETA, deben cambiar los pesos de desempeño/operación y estudiar PostgreSQL, colas u otros estilos. No se asume que el piloto académico tenga hoy esas necesidades. El punto de sensibilidad es **una instancia + carga moderada**. Una prueba de carga y concurrencia podría invalidar la elección.

## Evidencia y vínculos

- `main.py` y `README_API_ORIGINAL.md`: versión actual.
- [`matriz-decision.md`](matriz-decision.md): peso y justificación de las notas.
- [`c4-nivel2.md`](../02-vistas-c4/c4-nivel2.md): **vista objetivo**, todavía no implementada.
- E1–E6: [`01-contexto-y-drivers.md`](../01-contexto-y-drivers.md).
