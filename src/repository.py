"""Repositorio desacoplado para operaciones de acceso a datos y reglas de negocio."""

import sqlite3
from datetime import UTC, datetime, time

from src.database import get_db_connection
from src.models import EstadoSolicitud, Parada, SolicitudResponse

HORA_MINIMA = time(5, 0)   # 05:00 AM
HORA_MAXIMA = time(22, 0)  # 22:00 PM

# Matriz de transiciones autorizadas (R2, E3)
TRANSICIONES_VALIDAS = {
    EstadoSolicitud.PENDIENTE: [EstadoSolicitud.CONFIRMADA, EstadoSolicitud.CANCELADA],
    EstadoSolicitud.CONFIRMADA: [EstadoSolicitud.ATENDIDA, EstadoSolicitud.CANCELADA],
    EstadoSolicitud.ATENDIDA: [],
    EstadoSolicitud.CANCELADA: [],
}


class RepositoryError(Exception):
    """Excepción base del repositorio."""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ParadasRepository:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path

    def listar_paradas(self) -> list[Parada]:
        """Recupera la lista de paradas habilitadas en el sistema."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id_parada, nombre, latitud, longitud FROM paradas ORDER BY id_parada ASC;")
        rows = cursor.fetchall()
        conn.close()
        return [Parada(**dict(r)) for r in rows]

    def parada_existe(self, id_parada: int) -> bool:
        """Verifica si una parada existe en el catálogo."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM paradas WHERE id_parada = ?;", (id_parada,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def crear_solicitud(self, id_parada: int, id_pasajero: str, override_time: datetime | None = None) -> SolicitudResponse:
        """Registra una solicitud aplicando validación horaria y de unicidad activa (E1, ADR-002)."""
        # Validación de horario comercial (R2)
        ahora = override_time or datetime.now(UTC)
        hora_local = ahora.time()

        if not (HORA_MINIMA <= hora_local <= HORA_MAXIMA):
            raise RepositoryError(
                f"Horario fuera de servicio ({hora_local.strftime('%H:%M')}). La atención es de 05:00 a 22:00.",
                status_code=400
            )

        # Validación de existencia de parada
        if not self.parada_existe(id_parada):
            raise RepositoryError(
                f"La parada con id {id_parada} no existe en el catálogo autorizado.",
                status_code=404
            )

        hora_iso = ahora.strftime("%Y-%m-%dT%H:%M:%SZ")
        estado_inicial = EstadoSolicitud.PENDIENTE.value

        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        try:
            # Transacción atómica respaldada por el índice único parcial
            cursor.execute("""
            INSERT INTO solicitudes (id_parada, id_pasajero, hora_solicitud, estado)
            VALUES (?, ?, ?, ?);
            """, (id_parada, id_pasajero, hora_iso, estado_inicial))
            conn.commit()
            nuevo_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            conn.rollback()
            raise RepositoryError(
                f"Conflicto: El pasajero '{id_pasajero}' ya tiene una solicitud activa en la parada {id_parada}.",
                status_code=409
            )
        finally:
            conn.close()

        return SolicitudResponse(
            id_solicitud=nuevo_id,
            id_parada=id_parada,
            id_pasajero=id_pasajero,
            hora_solicitud=hora_iso,
            estado=EstadoSolicitud.PENDIENTE
        )

    def obtener_solicitud(self, id_solicitud: int) -> SolicitudResponse:
        """Recupera los datos de una solicitud por su identificador único."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id_solicitud, id_parada, id_pasajero, hora_solicitud, estado
        FROM solicitudes
        WHERE id_solicitud = ?;
        """, (id_solicitud,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise RepositoryError(
                f"Solicitud con id {id_solicitud} no encontrada.",
                status_code=404
            )

        return SolicitudResponse(
            id_solicitud=row["id_solicitud"],
            id_parada=row["id_parada"],
            id_pasajero=row["id_pasajero"],
            hora_solicitud=row["hora_solicitud"],
            estado=EstadoSolicitud(row["estado"])
        )

    def actualizar_estado(self, id_solicitud: int, nuevo_estado: EstadoSolicitud) -> SolicitudResponse:
        """Avanza el estado de la solicitud verificando la máquina de estados finita (E3)."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT estado FROM solicitudes WHERE id_solicitud = ?;", (id_solicitud,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            raise RepositoryError(
                f"Solicitud con id {id_solicitud} no encontrada.",
                status_code=404
            )

        estado_actual = EstadoSolicitud(row["estado"])

        # Verificar si la transición está permitida
        transiciones_permitidas = TRANSICIONES_VALIDAS.get(estado_actual, [])
        if nuevo_estado not in transiciones_permitidas:
            conn.close()
            raise RepositoryError(
                f"Transición no permitida: no se puede pasar de '{estado_actual.value}' a '{nuevo_estado.value}'. "
                f"Transiciones válidas desde {estado_actual.value}: {[e.value for e in transiciones_permitidas]}.",
                status_code=400
            )

        cursor.execute("""
        UPDATE solicitudes
        SET estado = ?
        WHERE id_solicitud = ?;
        """, (nuevo_estado.value, id_solicitud))
        conn.commit()
        conn.close()

        return self.obtener_solicitud(id_solicitud)
