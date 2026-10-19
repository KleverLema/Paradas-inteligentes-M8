# Evidencia técnica del prototipo usado como referencia

**Objetivo:** permitir que el lector comprenda de dónde surgieron las necesidades del dosier, sin incorporar archivos de equipos o asignaturas anteriores. La versión que se analizó fue un prototipo académico de una API REST en Python/FastAPI, facilitado durante la preparación de este trabajo. **El código fuente completo no forma parte de esta entrega SEM01 y el dosier no pretende acreditar una implementación nueva.**

## Contrato comprobado en el archivo `main.py` de referencia

| Método y ruta | Responsabilidad | Referencia del análisis |
|---|---|---|
| `GET /paradas` | Devuelve un catálogo fijo de cinco paradas. | `listar_paradas()` / `CATALOGO_PARADAS` |
| `POST /solicitudes` | Registra solicitud si el pasajero y la parada no tienen solicitud activa equivalente. | `crear_solicitud()` |
| `GET /solicitudes/{id_solicitud}` | Devuelve solicitud por ID; 404 si no existe. | `obtener_solicitud()` |
| `PATCH /solicitudes/{id_solicitud}/estado` | Cambia el estado según reglas de transición. | `cambiar_estado()` / `TRANSICIONES_VALIDAS` |

## Hallazgos relevantes para la arquitectura

**Persistencia (ADR-001):** el prototipo mantiene los registros en un diccionario del proceso:

```python
solicitudes: Dict[int, SolicitudOut] = {}
_siguiente_id = 1
```

Tras reiniciar la API, el proceso crea de nuevo estas estructuras. Esto origina el escenario E2. **No se afirma que SQLite esté implementado.**

**Unicidad (ADR-002):** `crear_solicitud()` aplica una búsqueda con `any(...)` sobre `solicitudes.values()` y después inserta en el diccionario. La lógica tiene respuesta HTTP 409 para duplicados encontrados en una ejecución secuencial, pero **no hay una restricción transaccional que cubra peticiones simultáneas**. La propuesta usa índice único parcial y transacciones; en implementación deberán manejarse los errores de integridad y de contención de SQLite para probar la meta E1.

**Seguridad (D3 / E4):** el código facilitado no configura autenticación o autorización. El dosier la trata como un requisito futuro y no debe usarse para datos de pasajeros reales sin implementar las salvaguardas aplicables.

**Estilo (ADR-003):** el prototipo concentra API, esquemas, lógica y memoria en un único `main.py`. El monolito **modular** es la arquitectura objetivo comparada en la matriz, no el estado de la implementación de partida.

## Límites de evidencia

Estas observaciones fueron contrastadas a nivel de lectura del código de referencia y documentación académica del caso. Las **metas numéricas** de E1–E6 son propuestas para futuras pruebas, no resultados ya medidos. La revisión cruzada con otro equipo se documentará por separado cuando ocurra realmente.
