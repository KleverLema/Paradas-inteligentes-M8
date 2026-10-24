"""Pruebas funcionales automatizadas derivadas de los criterios Gherkin (HU01-HU04)."""

import os
import tempfile
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from src.database import init_database
from src.main import app
from src.repository import ParadasRepository


@pytest.fixture(scope="function")
def client_and_repo():
    """Configura una base de datos temporal aislada para cada prueba."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
        db_path = tmp_db.name

    # Inicializar DDL y catálogo semilla
    init_database(db_path)
    test_repo = ParadasRepository(db_path=db_path)

    # Inyectar repositorio de prueba en la aplicación
    from src import main
    original_repo = main.repository
    main.repository = test_repo

    with TestClient(app) as client:
        yield client, test_repo

    # Restaurar y limpiar archivo temporal
    main.repository = original_repo
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass


def test_hu01_listar_paradas(client_and_repo):
    """CA01.1 y CA01.2: Consulta exitosa del catálogo de 5 paradas habilitadas."""
    client, _ = client_and_repo
    response = client.get("/paradas")

    assert response.status_code == 200
    paradas = response.json()
    assert isinstance(paradas, list)
    assert len(paradas) == 5

    primera = paradas[0]
    assert "id_parada" in primera and isinstance(primera["id_parada"], int)
    assert "nombre" in primera and len(primera["nombre"]) > 0
    assert "latitud" in primera and isinstance(primera["latitud"], float)
    assert "longitud" in primera and isinstance(primera["longitud"], float)


def test_hu02_crear_solicitud_exitosa(client_and_repo):
    """CA02.1: Creación exitosa en franja horaria permitida."""
    client, repo = client_and_repo
    # Forzar hora válida (10:30 AM UTC)
    hora_valida = datetime(2026, 10, 24, 10, 30, tzinfo=timezone.utc)
    
    solicitud = repo.crear_solicitud(id_parada=1, id_pasajero="pasajero-test-1", override_time=hora_valida)
    assert solicitud.id_solicitud > 0
    assert solicitud.id_parada == 1
    assert solicitud.id_pasajero == "pasajero-test-1"
    assert solicitud.estado.value == "PENDIENTE"


def test_hu02_rechazo_horario_nocturno(client_and_repo):
    """CA02.2: Rechazo de solicitud fuera de franja 05:00 a 22:00."""
    _, repo = client_and_repo
    hora_nocturna = datetime(2026, 10, 24, 23, 30, tzinfo=timezone.utc)

    with pytest.raises(Exception) as exc_info:
        repo.crear_solicitud(id_parada=1, id_pasajero="pasajero-test-2", override_time=hora_nocturna)
    
    assert "Horario fuera de servicio" in str(exc_info.value)
    assert getattr(exc_info.value, "status_code", 400) == 400


def test_hu02_rechazo_duplicado_activo(client_and_repo):
    """CA02.3: Invariante de unicidad activa (E1, ADR-002) -> HTTP 409."""
    _, repo = client_and_repo
    hora_valida = datetime(2026, 10, 24, 12, 0, tzinfo=timezone.utc)

    # Primera solicitud: Debe ser exitosa
    solicitud_1 = repo.crear_solicitud(id_parada=2, id_pasajero="pasajero-duplicado", override_time=hora_valida)
    assert solicitud_1.id_solicitud > 0

    # Segunda solicitud idéntica en estado activo: Debe lanzar 409 Conflict
    with pytest.raises(Exception) as exc_info:
        repo.crear_solicitud(id_parada=2, id_pasajero="pasajero-duplicado", override_time=hora_valida)

    assert "Conflicto" in str(exc_info.value)
    assert getattr(exc_info.value, "status_code", 409) == 409


def test_hu02_rechazo_parada_inexistente(client_and_repo):
    """CA02.4: Rechazo si el identificador de parada no está en catálogo -> 404."""
    _, repo = client_and_repo
    hora_valida = datetime(2026, 10, 24, 14, 0, tzinfo=timezone.utc)

    with pytest.raises(Exception) as exc_info:
        repo.crear_solicitud(id_parada=9999, id_pasajero="pasajero-x", override_time=hora_valida)

    assert getattr(exc_info.value, "status_code", 404) == 404


def test_hu03_obtener_solicitud_existente(client_and_repo):
    """CA03.1: Consulta exitosa de solicitud por ID."""
    client, repo = client_and_repo
    hora_valida = datetime(2026, 10, 24, 9, 15, tzinfo=timezone.utc)
    creada = repo.crear_solicitud(id_parada=3, id_pasajero="pasajero-consulta", override_time=hora_valida)

    response = client.get(f"/solicitudes/{creada.id_solicitud}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_solicitud"] == creada.id_solicitud
    assert data["id_parada"] == 3
    assert data["id_pasajero"] == "pasajero-consulta"
    assert data["estado"] == "PENDIENTE"


def test_hu03_obtener_solicitud_inexistente(client_and_repo):
    """CA03.2: Consulta de ID no registrado -> HTTP 404."""
    client, _ = client_and_repo
    response = client.get("/solicitudes/98765")
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"]


def test_hu04_transicion_estado_valida(client_and_repo):
    """CA04.1 y CA04.2: Transiciones autorizadas (PENDIENTE -> CONFIRMADA -> ATENDIDA)."""
    client, repo = client_and_repo
    hora_valida = datetime(2026, 10, 24, 15, 0, tzinfo=timezone.utc)
    creada = repo.crear_solicitud(id_parada=4, id_pasajero="pasajero-flujo", override_time=hora_valida)

    # 1. PENDIENTE -> CONFIRMADA
    resp1 = client.patch(f"/solicitudes/{creada.id_solicitud}/estado", json={"nuevo_estado": "CONFIRMADA"})
    assert resp1.status_code == 200
    assert resp1.json()["estado"] == "CONFIRMADA"

    # 2. CONFIRMADA -> ATENDIDA
    resp2 = client.patch(f"/solicitudes/{creada.id_solicitud}/estado", json={"nuevo_estado": "ATENDIDA"})
    assert resp2.status_code == 200
    assert resp2.json()["estado"] == "ATENDIDA"


def test_hu04_rechazo_transicion_invalida(client_and_repo):
    """CA04.3: Rechazo de transición prohibida (ATENDIDA -> PENDIENTE) -> HTTP 400 (E3)."""
    client, repo = client_and_repo
    hora_valida = datetime(2026, 10, 24, 16, 0, tzinfo=timezone.utc)
    creada = repo.crear_solicitud(id_parada=5, id_pasajero="pasajero-invalido", override_time=hora_valida)

    # Pasar a ATENDIDA
    repo.actualizar_estado(creada.id_solicitud, "CONFIRMADA")
    repo.actualizar_estado(creada.id_solicitud, "ATENDIDA")

    # Intentar volver a PENDIENTE
    resp_invalida = client.patch(f"/solicitudes/{creada.id_solicitud}/estado", json={"nuevo_estado": "PENDIENTE"})
    assert resp_invalida.status_code == 400
    assert "Transición no permitida" in resp_invalida.json()["detail"]
