"""Modelos de datos Pydantic para la API de Paradas Inteligentes."""

from enum import Enum

from pydantic import BaseModel, Field


class EstadoSolicitud(str, Enum):
    """Estados del ciclo de vida de una solicitud de parada."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    ATENDIDA = "ATENDIDA"
    CANCELADA = "CANCELADA"


class Parada(BaseModel):
    """Modelo representativo de una parada de transporte público."""
    id_parada: int = Field(..., description="Identificador único de la parada", example=1)
    nombre: str = Field(..., description="Nombre del punto de embarque", example="Parada Parque Central Tulcán")
    latitud: float = Field(..., description="Coordenada de latitud en grados decimales", example=0.8116)
    longitud: float = Field(..., description="Coordenada de longitud en grados decimales", example=-77.7173)


class SolicitudCreate(BaseModel):
    """Datos de entrada requeridos para crear una solicitud de parada."""
    id_parada: int = Field(..., description="Identificador de la parada donde abordará el pasajero", example=1)
    id_pasajero: str = Field(..., min_length=3, max_length=50, description="Identificador del pasajero", example="pasajero-101")


class SolicitudResponse(BaseModel):
    """Representación de salida de una solicitud registrada o consultada."""
    id_solicitud: int = Field(..., description="Identificador autoincremental de la solicitud", example=1)
    id_parada: int = Field(..., description="Identificador de la parada", example=1)
    id_pasajero: str = Field(..., description="Identificador del pasajero", example="pasajero-101")
    hora_solicitud: str = Field(..., description="Marca de tiempo en formato ISO 8601 UTC", example="2026-10-24T14:30:00Z")
    estado: EstadoSolicitud = Field(..., description="Estado actual de la solicitud", example=EstadoSolicitud.PENDIENTE)


class EstadoUpdate(BaseModel):
    """Cuerpo de solicitud para actualizar el estado operativo."""
    nuevo_estado: EstadoSolicitud = Field(..., description="Nuevo estado que se aplicará", example=EstadoSolicitud.CONFIRMADA)


class ErrorResponse(BaseModel):
    """Estructura estandarizada de respuestas de error."""
    detail: str = Field(..., description="Mensaje detallado con la causa del error")
