# Evidencia técnica del sistema analizado

## 1. Componentes funcionales

La referencia técnica examinada es una API REST Python/FastAPI con modelos Pydantic. Permite listar cinco paradas, crear solicitudes, consultar una solicitud individual y actualizar su estado. El estado de una solicitud se representa mediante `PENDIENTE`, `CONFIRMADA`, `ATENDIDA` o `CANCELADA`.

| Regla o función | Evidencia del código fuente | Implicación arquitectónica |
|---|---|---|
| Catálogo fijo | `CATALOGO_PARADAS` y `IDS_PARADAS_VALIDAS` | Catálogo interno sin servicio independiente |
| Horario | `HORA_MINIMA = 5 * 60`, `HORA_MAXIMA = 22 * 60` | Regla de negocio validada al registrar |
| Registro | `POST /solicitudes`, estado HTTP 201 | Contrato de creación para consumidor REST |
| Duplicados | `duplicada = any(...)` sobre `solicitudes.values()` | Validación secuencial sin garantía transaccional |
| Consultas | `GET /solicitudes/{id_solicitud}` | Lectura de solicitud por identificador |
| Cambios de estado | `TRANSICIONES_VALIDAS`, `PATCH /solicitudes/{id_solicitud}/estado` | Máquina de estados con HTTP 400 para transiciones no permitidas |
| Persistencia | `solicitudes: Dict[int, SolicitudOut] = {}` | Los registros no sobreviven al reinicio del proceso |

## 2. Limitaciones relevantes

La API de referencia almacena el estado en memoria del proceso y no integra un mecanismo de autenticación y autorización. El código comprueba la existencia de duplicados antes de insertar, pero no aplica restricciones de unicidad en una base transaccional. En consecuencia, el análisis plantea ADR-001, ADR-002 y el escenario E4 como evolución arquitectónica.

## 3. Relación con el modelo C4

El diseño de partida corresponde a un único contenedor de aplicación FastAPI con estado en memoria; el [C4 nivel 2](02-vistas-c4/c4-nivel2.md) especifica dos contenedores en la arquitectura objetivo: API FastAPI modular y almacenamiento SQLite. El [C4 nivel 1](02-vistas-c4/c4-nivel1.md) mantiene el límite funcional de gestión de solicitudes.
