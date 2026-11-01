# Checklist de validación funcional — Paradas Inteligentes M8

## 1. Objetivo

Establecer un procedimiento de revisión funcional para la API REST del proyecto Paradas Inteligentes M8, con el propósito de comprobar el comportamiento de sus endpoints y documentar los criterios que deben evaluarse antes de aprobar un Pull Request.

Este documento complementa los criterios de aceptación de las historias de usuario HU01 a HU04.

## 2. Componentes involucrados

El proyecto utiliza Python, FastAPI, Pydantic y SQLite.

Los archivos principales relacionados con la validación son:

- `src/main.py`: definición de los endpoints REST.
- `src/models.py`: modelos de datos y estados de las solicitudes.
- `src/repository.py`: reglas de negocio y persistencia.
- `src/database.py`: inicialización de SQLite.
- `api/openapi.yaml`: contrato de la API.
- `tests/test_api.py`: pruebas funcionales automatizadas.

## 3. Endpoints que deben verificarse

| Método | Endpoint | Resultado esperado |
|---|---|---|
| GET | `/paradas` | Devuelve el catálogo de paradas habilitadas. |
| POST | `/solicitudes` | Registra una nueva solicitud válida. |
| GET | `/solicitudes/{id_solicitud}` | Devuelve los datos de la solicitud consultada. |
| PATCH | `/solicitudes/{id_solicitud}/estado` | Actualiza el estado cuando la transición está permitida. |

## 4. Checklist de validación funcional

### HU01 — Consulta de paradas

- [ ] Verificar que GET `/paradas` responda con HTTP 200.
- [ ] Comprobar que devuelva el catálogo de cinco paradas definido en las pruebas.
- [ ] Verificar la presencia de identificador, nombre, latitud y longitud.

### HU02 — Registro de solicitudes

- [ ] Registrar una solicitud válida y comprobar su estado inicial PENDIENTE.
- [ ] Verificar el rechazo de solicitudes fuera del horario permitido.
- [ ] Comprobar el rechazo de solicitudes activas duplicadas del mismo pasajero y parada.
- [ ] Comprobar el rechazo cuando la parada solicitada no existe.

### HU03 — Consulta de solicitudes

- [ ] Consultar una solicitud existente y verificar su información.
- [ ] Consultar un identificador inexistente y comprobar la respuesta HTTP 404.

### HU04 — Actualización de estados

- [ ] Verificar la transición PENDIENTE a CONFIRMADA.
- [ ] Verificar la transición CONFIRMADA a ATENDIDA.
- [ ] Comprobar el rechazo de una transición inválida de ATENDIDA a PENDIENTE.

## 5. Validaciones técnicas

Desde la raíz del proyecto, con Python 3.11 o superior y las dependencias instaladas, ejecutar:

```bash
python -m pytest tests/ -v
python -m ruff check src tests
```

Para iniciar la API en un entorno de desarrollo:

```bash
python -m uvicorn src.main:app --reload
```

Consultar la documentación interactiva en:

`http://127.0.0.1:8000/docs`

## 6. Registro de resultados

Para cada comprobación ejecutada, registrar:

- Caso de prueba.
- Resultado esperado.
- Resultado obtenido.
- Estado: aprobado, fallido o pendiente.
- Evidencia correspondiente, cuando exista.

**Nota:** Este documento define las verificaciones que deben realizarse. No constituye evidencia de ejecución de pruebas ni certifica que todos los casos estén aprobados.

## 7. Criterio de aceptación

El checklist se considera completo como documento cuando:

- Incluye los cuatro endpoints del proyecto.
- Identifica los casos funcionales principales.
- Describe las comprobaciones y sus resultados esperados.
- Establece cómo registrar evidencias y resultados.
- Es revisado y aprobado mediante un Pull Request.

## 8. Referencias internas

- `README.md`
- `api/openapi.yaml`
- `src/main.py`
- `src/models.py`
- `tests/test_api.py`
- Issue #15 — Documentar checklist de validación funcional de la API.

## 9. Declaración de uso de IA

Se utilizó ChatGPT (OpenAI, GPT-6) como apoyo para estructurar la documentación y contrastar los casos propuestos con el código fuente publicado en el repositorio. El contenido debe ser revisado por el autor y validado por otro integrante mediante Pull Request antes de su incorporación a la rama principal.
