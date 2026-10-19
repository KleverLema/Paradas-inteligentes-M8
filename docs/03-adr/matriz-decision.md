# Selección de arquitectura — Matriz ponderada y trade-offs

## 1. Alternativas

- **A1 — Monolito modular:** FastAPI en un despliegue, separación interna de responsabilidades y SQLite transaccional.
- **A2 — Microservicios:** varios servicios desplegables, comunicación entre servicios y operación distribuida.

Ambas alternativas se comparan respecto a los criterios de calidad y las restricciones del mismo módulo de solicitudes de parada.

## 2. Criterios y ponderaciones

La escala es de **1 (desfavorable) a 5 (favorable)** para cada criterio. En costo operativo, una nota alta significa menor esfuerzo de operación. Los pesos suman el 100 %.

| Criterio | Driver / escenario | Peso | A1 | A2 | Justificación de la valoración |
|---|---|---:|---:|---:|---|
| C1. Consistencia de solicitudes | D1 / E1 | 30 % | 5 | 3 | Una BD transaccional local facilita preservar la unicidad sin coordinación distribuida. |
| C2. Durabilidad y recuperación | D2 / E2 | 20 % | 4 | 5 | Ambas pueden persistir; A2 obtiene ventaja supuesta al aislar su operación, a cambio de mayor infraestructura. |
| C3. Protección de identificadores | D3 / E4 | 15 % | 3 | 4 | Ambas necesitan autorización; A2 permite separación de servicios, pero amplía los puntos a proteger. |
| C4. Eficiencia de consultas | D4 / E5 | 15 % | 4 | 4 | La carga objetivo es moderada; no existen mediciones que permitan diferenciar el desempeño. |
| C5. Facilidad de modificación | D5 / E6 | 10 % | 4 | 5 | A2 permitiría desplegar independientemente; A1 mantiene cambios internos acotados. |
| C6. Costo operativo | R5, R6 | 10 % | 5 | 1 | A1 requiere menos servicios y coordinación para un equipo pequeño. |
| **Total ponderado / 5** | | **100 %** | **4,25** | **3,70** | |

**Cálculo A1:** (30×5 + 20×4 + 15×3 + 15×4 + 10×4 + 10×5) / 100 = **4,25**.  
**Cálculo A2:** (30×3 + 20×5 + 15×4 + 15×4 + 10×5 + 10×1) / 100 = **3,70**.

El resultado favorece A1 para un escenario de una instancia y recursos limitados. La calificación de A2 en durabilidad depende de una hipótesis de diseño, no de una propiedad automática de los microservicios.

## 3. Sensibilidad del resultado

Para analizar la estabilidad de la elección se traslada parte del peso de consistencia a durabilidad y facilidad de modificación:

| Criterio | Peso base | Peso alternativo | A1 | A2 |
|---|---:|---:|---:|---:|
| C1. Consistencia | 30 % | 20 % | 5 | 3 |
| C2. Durabilidad | 20 % | 25 % | 4 | 5 |
| C3. Protección | 15 % | 15 % | 3 | 4 |
| C4. Eficiencia | 15 % | 15 % | 4 | 4 |
| C5. Facilidad de cambio | 10 % | 15 % | 4 | 5 |
| C6. Costo operativo | 10 % | 10 % | 5 | 1 |
| **Total** | **100 %** | **100 %** | **4,15** | **3,90** |

El monolito modular mantiene la mayor puntuación; la ventaja disminuye de **0,55** a **0,25**, lo que muestra sensibilidad frente al cambio de prioridades.

## 4. Trade-offs relevantes

| Decisión | Beneficio | Compromiso | Escenarios afectados |
|---|---|---|---|
| SQLite en una instancia | Persistencia de bajo costo operativo | Limitación para múltiples réplicas y alta disponibilidad | E2, E5 |
| Índice único transaccional | Evita solicitudes activas duplicadas | Posible contención al escribir | E1, E5 |
| Monolito modular | Despliegue y mantenimiento simples | Sin escalamiento independiente por servicio | E5, E6 |
| Autorización en la API | Protege identificadores | Añade verificaciones y esfuerzo de implementación | E4, E5 |

**Decisión final de diseño:** A1, monolito modular. Se reconsideraría si el sistema exigiera operación multiinstancia, grandes cargas distribuidas o integración en tiempo real con otros subsistemas de transporte. Véase [ADR-003](ADR-003-estilo-monolito-modular.md).
