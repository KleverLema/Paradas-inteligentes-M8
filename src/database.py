"""Módulo de conexión y gestión de persistencia en SQLite (ADR-001, ADR-002)."""

import sqlite3
import os
from typing import Optional

DB_PATH_DEFAULT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "paradas.db")


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Retorna una conexión a SQLite configurada con tipos de fila de diccionario."""
    target_path = db_path or DB_PATH_DEFAULT
    conn = sqlite3.connect(target_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_database(db_path: Optional[str] = None) -> None:
    """Inicializa las tablas y el catálogo semilla en la base de datos."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Tabla de catálogo de paradas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS paradas (
        id_parada INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        latitud REAL NOT NULL,
        longitud REAL NOT NULL
    );
    """)

    # Tabla de solicitudes de parada
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS solicitudes (
        id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
        id_parada INTEGER NOT NULL,
        id_pasajero TEXT NOT NULL,
        hora_solicitud TEXT NOT NULL,
        estado TEXT NOT NULL,
        FOREIGN KEY (id_parada) REFERENCES paradas (id_parada)
    );
    """)

    # ADR-002: Índice único parcial para evitar duplicados concurrentes en estados activos
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_solicitud_activa_unica
    ON solicitudes (id_pasajero, id_parada)
    WHERE estado IN ('PENDIENTE', 'CONFIRMADA');
    """)

    # Catálogo inicial de 5 paradas autorizadas en Tulcán (R3)
    paradas_iniciales = [
        (1, "Parada Parque Central Tulcán", 0.8116, -77.7173),
        (2, "Parada Terminal Terrestre Tulcán", 0.8189, -77.7215),
        (3, "Parada Universidad Politécnica Estatal del Carchi - UPEC", 0.8295, -77.7161),
        (4, "Parada Redondel del Mambí", 0.8052, -77.7142),
        (5, "Parada Hospital Luis Gabriel Dávila", 0.8145, -77.7231),
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO paradas (id_parada, nombre, latitud, longitud)
    VALUES (?, ?, ?, ?);
    """, paradas_iniciales)

    conn.commit()
    conn.close()
