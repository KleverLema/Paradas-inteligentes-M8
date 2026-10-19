# Vista complementaria — C4 nivel 2 del prototipo actual

**No sustituye la vista objetivo de la Práctica 02.** Se añade solo para diferenciar hechos observados de decisiones futuras.

```mermaid
flowchart TB
    cliente["Cliente HTTP de prueba<br/>[Sistema externo]"]
    equipo["Equipo técnico<br/>[Persona]"]
    subgraph sistema["Gestión de solicitudes de parada · implementación actual"]
        api["API REST FastAPI, main.py<br/>[Único contenedor desplegable]"]
        memoria["Diccionario solicitudes<br/>[Estado interno del mismo proceso; NO es otro contenedor]"]
        api -.->|"Consulta y modifica estructuras Python en memoria"| memoria
    end
    cliente -->|"GET / POST / PATCH; HTTP / JSON"| api
    equipo -->|"Consulta Swagger y ejecuta pruebas HTTP"| api
```

**Evidencia consultada:** `solicitudes: Dict[int, SolicitudOut] = {}` y funciones de los cuatro endpoints de `main.py`, documentadas en [evidencia técnica](../05-evidencia-tecnica.md). La API actual no persiste registros al reiniciar, no autentica usuarios y no proporciona garantía transaccional entre peticiones concurrentes.
