"""Punto de entrada de la aplicación FastAPI para Paradas Inteligentes."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.database import init_database
from src.models import (
    ErrorResponse,
    EstadoUpdate,
    Parada,
    SolicitudCreate,
    SolicitudResponse,
)
from src.repository import ParadasRepository, RepositoryError

repository = ParadasRepository()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa la base de datos y catálogo al arrancar el servicio."""
    init_database()
    yield


app = FastAPI(
    title="API de Gestión de Solicitudes de Paradas Inteligentes",
    version="0.2.0",
    description="Servicio modular de registro y gestión del ciclo de vida de solicitudes de parada urbana (Tulcán).",
    lifespan=lifespan,
    responses={
        400: {"model": ErrorResponse, "description": "Solicitud incorrecta o regla de negocio no cumplida"},
        404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
        409: {"model": ErrorResponse, "description": "Conflicto por duplicidad activa"}
    }
)


@app.exception_handler(RepositoryError)
async def repository_error_handler(request, exc: RepositoryError):
    """Capturador global para excepciones controladas del repositorio."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get(
    "/paradas",
    response_model=list[Parada],
    tags=["Paradas"],
    summary="Consultar catálogo de paradas habilitadas",
    description="Devuelve la lista completa de paradas autorizadas en la red urbana de Tulcán."
)
async def listar_paradas():
    return repository.listar_paradas()


@app.post(
    "/solicitudes",
    response_model=SolicitudResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Solicitudes"],
    summary="Registrar una nueva solicitud de parada",
    description="Registra una nueva petición de abordaje verificando horario comercial y unicidad activa."
)
async def crear_solicitud(solicitud: SolicitudCreate):
    return repository.crear_solicitud(
        id_parada=solicitud.id_parada,
        id_pasajero=solicitud.id_pasajero
    )


@app.get(
    "/solicitudes/{id_solicitud}",
    response_model=SolicitudResponse,
    tags=["Solicitudes"],
    summary="Consultar solicitud de parada por ID",
    description="Recupera los datos y estado actual de una solicitud registrada."
)
async def obtener_solicitud(id_solicitud: int):
    return repository.obtener_solicitud(id_solicitud)


@app.patch(
    "/solicitudes/{id_solicitud}/estado",
    response_model=SolicitudResponse,
    tags=["Solicitudes"],
    summary="Actualizar estado de una solicitud de parada",
    description="Avanza el estado de la solicitud verificando las transiciones legales permitidas."
)
async def actualizar_estado(id_solicitud: int, body: EstadoUpdate):
    return repository.actualizar_estado(
        id_solicitud=id_solicitud,
        nuevo_estado=body.nuevo_estado
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
