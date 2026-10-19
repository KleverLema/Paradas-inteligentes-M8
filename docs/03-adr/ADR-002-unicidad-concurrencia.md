# ADR-002 — Garantizar unicidad de solicitudes activas con restricción de base de datos

- **Estado:** Propuesto — pendiente de aceptación por el equipo.
- **Fecha:** 15/10/2026.
- **Drivers:** D1. **Escenarios:** E1, E3. **Restricciones:** R1, R2.
- **Dependencia:** ADR-001 (almacenamiento relacional).

## Contexto

En `main.py`, la ruta `POST /solicitudes` primero busca duplicados recorriendo `solicitudes.values()` con `any(...)` y después inserta en el diccionario. Ese esquema sirve para comprobaciones secuenciales, pero **no proporciona garantía transaccional de unicidad ante solicitudes concurrentes**. La meta E1 requiere una única solicitud activa por pareja pasajero-parada para 100 peticiones simultáneas.

## Decisión propuesta

Tras implementar ADR-001, crear una **restricción de unicidad activa a nivel de base de datos** (SQLite: índice único parcial) para la pareja (`id_pasajero`, `id_parada`) cuando `estado` sea `PENDIENTE` o `CONFIRMADA`. Crear y actualizar solicitudes dentro de transacciones y traducir el conflicto de unicidad a HTTP 409 sin duplicar estados.

**Ejemplo de diseño, no migración ejecutada:**

```sql
CREATE UNIQUE INDEX uq_solicitud_activa
ON solicitudes (id_pasajero, id_parada)
WHERE estado IN ('PENDIENTE', 'CONFIRMADA');
```

Al cancelar o atender una solicitud, dejará de estar comprendida en el índice, permitiendo una futura solicitud según las reglas del negocio. El diseño debe confirmar con el equipo si múltiples horarios o fechas son parte del identificador lógico de duplicado; **el código actual solo usa pasajero + parada**.

## Alternativas consideradas

1. Validación `any(...)` en `dict` como ahora: simple, sin protección transaccional de concurrencia.
2. Candado (`Lock`) solo en memoria: serializa dentro de un proceso, pero no protege varias instancias ni la persistencia.
3. Índice único parcial y transacciones en BD (preferida): el motor preserva el invariante incluso ante solicitudes simultáneas compatibles con la misma base.

## Consecuencias positivas

- La regla crítica R1 se verifica en el nivel donde se confirman los datos.
- La API puede devolver HTTP 409 de forma consistente.
- Apoya E1 sin depender solo de comprobaciones previas.

## Consecuencias negativas / trade-offs

- Requiere adaptar la lógica de guardado y tratar errores de integridad.
- Introduce bloqueo/contención durante escritura; rendimiento debe evaluarse con E5.
- Cambiar posteriormente la definición del duplicado (p. ej. agregar fecha, ruta o franja) implica migraciones.

## Evidencia y verificación

- Evidencia actual: [extracto de `crear_solicitud()` y estados](../05-evidencia-tecnica.md).
- Prueba pendiente: 100 peticiones simultáneas, esperar 1 creación y 99 rechazos; verificar cero activos duplicados en BD.
- **Vínculo:** [`c4-nivel2.md`](../02-vistas-c4/c4-nivel2.md), E1, ADR-001.
