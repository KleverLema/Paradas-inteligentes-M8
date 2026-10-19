# ADR-002 — Unicidad de solicitudes activas

**Fecha:** 18/10/2026  
**Estado:** Seleccionada para la arquitectura objetivo; no implementada en la API de referencia.  
**Drivers:** D1 · **Escenarios:** E1, E3 · **Restricción:** R1 · **Depende de:** ADR-001.

## Contexto

La ruta `POST /solicitudes` utiliza una búsqueda `any(...)` sobre el diccionario para detectar otra solicitud activa con el mismo `id_pasajero` y `id_parada`. Esa comprobación funciona para peticiones secuenciales, pero la lectura y posterior escritura no están protegidas por una transacción. Dos solicitudes concurrentes podrían observar la misma disponibilidad.

## Alternativas

| Alternativa | Ventaja | Limitación |
|---|---|---|
| Comprobación previa en Python | Simple, ya existe en la API | No ofrece garantía transaccional |
| Bloqueo en memoria del proceso | Sin base de datos adicional | No garantiza unicidad entre múltiples procesos y no resuelve persistencia |
| Restricción única parcial en SQLite | Invariante protegido por el motor de datos | Puede generar contención en escrituras concurrentes |

## Decisión

Utilizar una **restricción de unicidad a nivel de base de datos** sobre la pareja (`id_pasajero`, `id_parada`) solamente mientras la solicitud esté en estado `PENDIENTE` o `CONFIRMADA`. Ejecutar el registro dentro de una transacción y traducir la violación de unicidad a **HTTP 409**.

```sql
CREATE UNIQUE INDEX ux_solicitud_activa
ON solicitudes (id_pasajero, id_parada)
WHERE estado IN ('PENDIENTE', 'CONFIRMADA');
```

El diseño de esquema deberá asegurar que los identificadores, los estados y las transacciones correspondan al contrato de la API.

## Consecuencias y trade-offs

- Se protege la regla de negocio independientemente del orden de llegada de las peticiones.
- Se admite una nueva solicitud una vez finalizada o cancelada la anterior, según las reglas vigentes.
- La escritura concurrente puede experimentar bloqueos o reintentos, cuyo impacto se evaluará en E1 y E5.

## Comprobación

La prueba E1 establece 100 solicitudes concurrentes equivalentes: una aceptada, 99 rechazadas y cero registros activos duplicados. La base transaccional se representa en [C4 nivel 2](../02-vistas-c4/c4-nivel2.md).
