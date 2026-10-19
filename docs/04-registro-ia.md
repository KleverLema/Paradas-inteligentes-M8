# Registro de uso y verificación crítica de inteligencia artificial

La inteligencia artificial se utilizó como apoyo para estructurar documentación, formular alternativas y contrastar argumentos arquitectónicos. Las decisiones se fundamentan en las reglas de la API y en los escenarios de calidad descritos en el dosier.

| Actividad | Herramienta y versión | Solicitud resumida | Aporte generado | Verificación / tratamiento |
|---|---|---|---|---|
| Identificación de drivers | ChatGPT (GPT-6), octubre de 2026 | Relacionar reglas de la API con atributos de calidad | Priorizar integridad, persistencia y seguridad | **Modificado:** se restringió el alcance a cuatro operaciones REST verificadas en la API. |
| Selección de persistencia | ChatGPT (GPT-6) | Comparar memoria, SQLite y PostgreSQL | Propuesta de SQLite para una instancia | **Aceptado como decisión de diseño:** `solicitudes = {}` confirma ausencia de persistencia. |
| Concurrencia | ChatGPT (GPT-6) | Analizar el riesgo de solicitudes activas duplicadas | Índice único parcial y transacción | **Aceptado como diseño:** se contrastó con la búsqueda `any(...)` de `crear_solicitud()`; no se atribuyó implementación al prototipo. |
| Estilo arquitectónico | ChatGPT (GPT-6) | Comparar monolito modular y microservicios | Matriz ponderada y análisis de trade-offs | **Modificado:** se añadieron pesos explícitos y una prueba de sensibilidad, sin presentar las notas como mediciones. |
| Vistas C4 | ChatGPT (GPT-6) | Separar contexto y contenedores | Dos diagramas Mermaid | **Modificado:** se mantuvieron consumidores externos fuera del límite y SQLite como contenedor objetivo. |

## Contraste crítico de resultados

| Planteamiento contrastado | Evidencia | Resolución |
|---|---|---|
| La API ya conserva solicitudes tras reiniciarse | El almacenamiento consultado es un diccionario local al proceso | **Rechazado.** La persistencia se define en ADR-001 como arquitectura objetivo. |
| La búsqueda previa de duplicados es suficiente bajo concurrencia | El código consulta con `any(...)` y después escribe, sin transacción | **Rechazado.** Se requiere restricción transaccional en ADR-002. |
| Los microservicios son necesarios por tratarse de transporte público | El módulo tiene cuatro operaciones y no integra ETA ni GPS | **Rechazado.** La matriz favorece el monolito modular para el alcance establecido. |
| SQLite resuelve todos los escenarios de calidad | E4 exige autorización y E5 exige medir latencia | **Modificado.** SQLite contribuye a E1–E2, pero no sustituye seguridad ni pruebas. |
| Los diagramas C4 pueden representar la arquitectura propuesta | Las vistas distinguen actores externos de contenedores propios | **Aceptado.** Se documenta el límite entre implementación actual y diseño objetivo. |

Los resultados numéricos de escenarios y las valoraciones de alternativas son criterios de diseño, no pruebas ejecutadas. Esta distinción preserva la trazabilidad entre evidencia técnica, decisiones y objetivos de calidad.
