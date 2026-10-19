# ADR-003 — Estilo arquitectónico: monolito modular

**Fecha:** 18/10/2026  
**Estado:** Seleccionada para la arquitectura objetivo; modularización no implementada en la API de referencia.  
**Drivers:** D1–D5 · **Escenarios:** E1–E6 · **Restricciones:** R3, R5, R6.

## Contexto

El alcance funcional comprende cuatro operaciones de negocio sobre solicitudes de parada. La API de referencia combina rutas, validaciones, reglas y almacenamiento dentro de `main.py`. La evolución propuesta incorpora una base de datos, garantías transaccionales y separación de responsabilidades, sin requerir aún operaciones independientes distribuidas.

## Alternativas

**A1. Monolito modular:** un proceso FastAPI con módulos internos de rutas, dominio, servicios y acceso a datos, y un almacenamiento SQLite para una primera instancia.

**A2. Microservicios:** separar solicitudes y otros servicios de negocio en procesos independientes, con comunicación y operación distribuidas.

## Decisión

Seleccionar **A1, monolito modular**, por el menor costo de despliegue y la posibilidad de mantener las operaciones transaccionales dentro de una sola aplicación. Mantener fronteras internas claras entre reglas, rutas y persistencia.

## Evaluación

La [matriz ponderada](matriz-decision.md) compara ambas alternativas frente a seis criterios relacionados con escenarios de calidad. La puntuación de diseño resultante es **4,25/5 para A1** y **3,70/5 para A2**. Son valoraciones razonadas de arquitectura, no resultados de pruebas de desempeño.

## Consecuencias y trade-offs

- La estructura modular facilita cambios en persistencia y reglas sin incorporar múltiples despliegues.
- Una sola aplicación simplifica seguimiento, pruebas de contrato y operación para el alcance actual.
- No permite escalar cada módulo de manera independiente; un crecimiento hacia GPS, ETA o varias instancias requeriría reevaluar la solución.
- La elección no implementa automáticamente autenticación, autorización ni índices; estas capacidades requieren trabajo técnico posterior.

La vista de contenedores asociada está en [C4 nivel 2](../02-vistas-c4/c4-nivel2.md).
