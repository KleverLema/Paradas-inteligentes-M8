# Paradas Inteligentes

**Maestría en Ingeniería de Software — UPEC | Módulo 8**  
**Integrantes:** Klever Lema Tamay, Edwin Toapanta y Ariel Aguirre

## Descripción

Paradas Inteligentes es un prototipo de API REST para administrar solicitudes de parada del transporte público urbano de Tulcán. Permite consultar paradas habilitadas, registrar solicitudes, consultar su estado y actualizarlo según las transiciones permitidas.

El sistema está implementado con **Python, FastAPI, Pydantic y SQLite**. Se organiza en módulos para separar la interfaz HTTP, los modelos de datos, la lógica de negocio y la persistencia.

## Funcionalidades

| Método | Ruta | Función |
|---|---|---|
| `GET` | `/paradas` | Consultar el catálogo de paradas |
| `POST` | `/solicitudes` | Registrar una solicitud de parada |
| `GET` | `/solicitudes/{id_solicitud}` | Consultar una solicitud |
| `PATCH` | `/solicitudes/{id_solicitud}/estado` | Actualizar su estado |

Los estados permitidos son `PENDIENTE`, `CONFIRMADA`, `ATENDIDA` y `CANCELADA`. SQLite almacena las solicitudes y aplica una restricción de unicidad para solicitudes activas del mismo pasajero y parada.

## Estructura del proyecto

| Ruta | Descripción |
|---|---|
| `src/main.py` | Inicio de FastAPI y definición de endpoints |
| `src/models.py` | Modelos de entrada y salida, y estados |
| `src/repository.py` | Reglas de negocio y operaciones de solicitudes |
| `src/database.py` | Conexión, creación de tablas e inicialización de SQLite |
| `api/openapi.yaml` | Contrato de la API en OpenAPI 3.0.3 |
| `tests/test_api.py` | Pruebas automatizadas con pytest |
| `docs/01-contexto-y-drivers.md` | Contexto, restricciones y escenarios de calidad |
| `docs/02-vistas-c4/` | Diagramas y coherencia de vistas C4 |
| `docs/03-adr/` | Decisiones de arquitectura |
| `docs/04-registro-ia.md` | Registro y verificación crítica del uso de IA |
| `docs/05-evidencia-tecnica.md` | Evidencia del sistema de referencia |
| `docs/06-mapa-toolchain.md` | Herramientas CASE y priorización de tareas |
| `docs/07-historias-y-criterios.md` | Historias y criterios de aceptación en Gherkin |
| `docs/08-matriz-evaluacion-case.md` | Evaluación de herramientas CASE |

## Ejecución local en Windows

Requiere Python 3.11 o superior, porque el código usa `datetime.UTC` (pruebas y auditoría verificadas con Python 3.14). Desde la carpeta principal del repositorio, abrir PowerShell o la terminal de Visual Studio Code y ejecutar:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

El servicio se inicia en `http://127.0.0.1:8000`.

- Documentación interactiva: `http://127.0.0.1:8000/docs`
- Catálogo de paradas: `http://127.0.0.1:8000/paradas`
- Especificación generada: `http://127.0.0.1:8000/openapi.json`

## Pruebas automatizadas

Desde otra terminal, situada en la raíz del proyecto y con las dependencias instaladas:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Para revisar el estilo y los errores estáticos del código:

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
```

La documentación de diseño, los criterios de aceptación y las decisiones arquitectónicas se encuentran en `docs/`.
