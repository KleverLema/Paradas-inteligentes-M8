# ADR-001 — Persistir solicitudes en una base de datos relacional ligera

- **Estado:** Propuesto — pendiente de aceptación por el equipo.
- **Fecha:** 15/10/2026.
- **Drivers:** D2, D5. **Escenarios:** E2, E6. **Restricciones:** R4, R5, R6.

## Contexto

`main.py` almacena las solicitudes en `solicitudes: Dict[int, SolicitudOut] = {}` y asigna IDs mediante `_siguiente_id`. Es una solución válida para demostrar reglas y pruebas, pero **no conserva los registros tras reiniciar el proceso**. E2 propone recuperar 100 de 100 registros. Se supone un piloto académico de una sola instancia y presupuesto limitado; el equipo debe validar ese supuesto.

## Decisión propuesta

Adoptar **SQLite** como repositorio persistente para la primera etapa, introduciendo una capa de acceso a datos separada del endpoint y usando transacciones. No se sustituirá el `dict` hasta una implementación futura. El esquema y los índices deben documentarse y probarse antes de declarar la decisión implementada.

## Alternativas consideradas

1. **Continuar con `dict`:** muy simple y fácil de probar, pero no cumple E2.
2. **SQLite (preferida):** persistencia transaccional en archivo, sin servicio de BD adicional; adecuada como hipótesis para una sola instancia académica.
3. **PostgreSQL:** ofrece administración y despliegues de mayor escala, con mayor trabajo operativo para el piloto. Reconsiderarla si crecen los requisitos.

## Consecuencias positivas

- Posibilita cumplir E2 con pruebas de reinicio.
- Proporciona transacciones y soporte SQL para el invariante de E1.
- Reduce dependencia directa de memoria del proceso.

## Consecuencias negativas / trade-offs

- Añade persistencia, migraciones/estructura y gestión de archivos/respaldo.
- SQLite de archivo local no resuelve, por sí solo, alta disponibilidad ni escalamiento horizontal distribuido.
- La API actual deberá modificarse y verificarse; **no basta con cambiar el diagrama**.

## Evidencia y verificación

- Evidencia actual: `main.py`, bloque «Base de datos en memoria» y `README_API_ORIGINAL.md`.
- Prueba futura E2: registrar 100 solicitudes, reiniciar proceso y comprobar recuperación exacta.
- Condición de reconsideración: se requieren múltiples réplicas, acceso remoto intensivo o requisitos de operación mayores.
- **Vínculo:** [`c4-nivel2.md`](../02-vistas-c4/c4-nivel2.md), matriz ponderada, E2.
