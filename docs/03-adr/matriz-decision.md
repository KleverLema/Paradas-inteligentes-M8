# Práctica 03 — Comparación, ponderación y selección de estilo

**Proyecto:** Paradas Inteligentes — API de solicitudes. **Estado:** análisis propuesto, pendiente de validación grupal.

## 1. Priorización de escenarios

Orden: E1 (consistencia), E2 (persistencia), E4 (seguridad), E3 (transiciones), E5 (desempeño), E6 (mantenibilidad). El equipo deberá ratificarlo; los pesos son **ilustrativos** basados en ese orden y las restricciones.

## 2. Alternativas reales para este alcance

| ID | Alternativa | Descripción | Costo operativo relativo |
|---|---|---|---|
| A1 | Monolito modular | FastAPI en un despliegue, separación de módulos, SQLite transaccional local para piloto | Bajo |
| A2 | Microservicios | Separar solicitudes, catálogo/identidad y almacenamiento con APIs entre servicios | Alto |

**No evaluar A2 como si ya estuviera construida.** Las dos son alternativas de diseño futuro. El estado actual es un `main.py` monolítico con almacenamiento en memoria, que no reúne todavía las garantías de los ADR.

## 3. Criterios derivados, pesos y rúbrica

Una calificación de 1 a 5 evalúa **cuánto favorece la alternativa el criterio**, no la calidad general de la tecnología. En costo, 5 = menos carga.

| Criterio | Referencia | Peso | 5 (mejor) | 3 (intermedio) | 1 (peor) |
|---|---|---:|---|---|---|
| C1 Consistencia de solicitudes | E1, D1, R1 | 30 % | Una BD transaccional controla la unicidad con mínima coordinación | Coordina más de un componente | No permite garantizar el invariante |
| C2 Durabilidad y recuperación | E2, D2 | 20 % | Recuperación comprobable y operable con poca complejidad | Requiere coordinación para recuperar datos | Pierde solicitudes al reiniciar |
| C3 Protección de identificadores | E4, D3, R7 | 15 % | Autorización y auditoría central controlables | Varios puntos que requieren coordinación | Acceso no controlado |
| C4 Rendimiento al consultar | E5, D4 | 15 % | Alta probabilidad de cumplir con holgura y pruebas simples | Requiere ajustes de red/índices/caché | Difícil cumplir |
| C5 Facilidad de cambio | E6, D5 | 10 % | Sustitución del módulo sin alterar contratos | Hay que redesplegar módulo acotado | Cambio transversal |
| C6 Costo operativo | R5, R6 | 10 % | Un despliegue para equipo pequeño | Dependencias adicionales moderadas | Múltiples sistemas costosos |
| **Total** | | **100 %** | | | |

## 4. Matriz ponderada de diseño

| Criterio | Peso | A1 Monolito modular | A2 Microservicios | Justificación concreta / pregunta de validación |
|---|---:|---:|---:|---|
| C1 Consistencia | 30 % | 5 | 3 | A1 permite restricción parcial en BD central y transacción local; A2 añade fronteras de servicio. Probar E1. |
| C2 Durabilidad | 20 % | 4 | 5 | Ambos con persistencia propuesta; A2 puede independizar la recuperación, pero añade infraestructura. Probar E2. |
| C3 Protección | 15 % | 3 | 4 | A1 permite punto central, aunque exige implementar auth pendiente; A2 puede aislar servicio pero amplía credenciales. Probar E4. |
| C4 Desempeño | 15 % | 4 | 4 | Para 120 lecturas/min ambas podrían funcionar; falta ejecutar carga E5. No se presentan cifras medidas. |
| C5 Cambio | 10 % | 4 | 5 | Un proveedor/repositorio encapsulado permite cambio, pero A1 se redespliega todo. A2 modifica servicio aislado. |
| C6 Costo | 10 % | 5 | 1 | A1 una aplicación y BD local; A2 varios servicios, despliegues y monitoreo. |
| **Total ponderado de 5** | **100 %** | **4,25** | **3,70** | **Resultado ilustrativo para decisión del grupo** |

**Cálculo de A1:** (30×5 + 20×4 + 15×3 + 15×4 + 10×4 + 10×5) / 100 = **4,25**.  
**Cálculo de A2:** (30×3 + 20×5 + 15×4 + 15×4 + 10×5 + 10×1) / 100 = **3,70**.

## 5. Trade-offs, sensibilidad y mitigaciones

| Compromiso / riesgo | Escenario | Consecuencia | Mitigación / evidencia exigida |
|---|---|---|---|
| SQLite de archivo en monolito facilita implementación, pero complica distribuir varias réplicas | E2, E5 | Limitación de escalamiento | Mantener una instancia académica; reevaluar PostgreSQL con volumen real |
| Restricción única evita duplicados, pero puede generar contención en escrituras | E1, E5 | Posible latencia mayor | Prueba simultánea E1 y carga E5 |
| Acceso a identificador del pasajero sin autenticación | E4 | Exposición de información en entorno público | No publicar con usuarios reales; diseñar autorización, auditar accesos, ejecutar E4 |
| Un solo despliegue simplifica operación, pero obliga a redesplegar todo al cambiar persistencia | E6, R5 | Tiempo de despliegue | Separar contrato de repositorio, probar cambio E6 |

**Sensibilidad:** si el supuesto de una instancia cambia o el servicio se amplía a la solución ETA del SRS (con GPS/GSM y pantallas), la evaluación debe repetirse. La decisión **no es universal** ni incorpora los componentes ETA que no existen en la API actual.

## 6. Comprobación de sensibilidad (segundo escenario de pesos)

Para comprobar que la conclusión no depende exclusivamente de una distribución de pesos, se ajusta **moderadamente** la importancia relativa: se disminuye consistencia de 30 % a 20 %, se aumenta durabilidad a 25 % y facilidad de cambio a 15 %; se mantienen los restantes pesos. **Son hipótesis de diseño y no ensayos medidos.**

| Criterio | Peso base | Peso de contraste | Nota A1 | Nota A2 |
|---|---:|---:|---:|---:|
| C1 Consistencia | 30 % | 20 % | 5 | 3 |
| C2 Durabilidad | 20 % | 25 % | 4 | 5 |
| C3 Protección | 15 % | 15 % | 3 | 4 |
| C4 Desempeño | 15 % | 15 % | 4 | 4 |
| C5 Cambio | 10 % | 15 % | 4 | 5 |
| C6 Costo | 10 % | 10 % | 5 | 1 |
| **Suma** | **100 %** | **100 %** | | |

- **A1:** (20×5 + 25×4 + 15×3 + 15×4 + 15×4 + 10×5) / 100 = **4,15**.
- **A2:** (20×3 + 25×5 + 15×4 + 15×4 + 15×5 + 10×1) / 100 = **3,90**.

**Resultado del contraste:** A1 también ocupa el primer lugar con estos pesos, aunque su margen disminuye de **0,55** a **0,25** puntos. La elección es **sensible al peso del costo operativo y a los supuestos de una sola instancia**; si cambian las restricciones, deberá repetirse la evaluación. Las puntuaciones mismas requieren validación del grupo y no prueban que una arquitectura ya cumpla E1–E6. La nota 5 otorgada a A2 en durabilidad supone que habría un subsistema persistente con operación y recuperación independientes, **no deriva automáticamente del estilo microservicios**.

## 7. Decisión y contraste con IA

**Ganador propuesto:** A1 (4,25 sobre 5). Documentado en [`ADR-003`](ADR-003-estilo-monolito-modular.md).  
**Objeción crítica:** la meta E1 aún no se ha probado concurrentemente y E4 no está implementada; sin resultados reales, las notas son hipótesis justificadas, no certificaciones.  
**Evaluación humana:** equipo debe discutir si acepta/modifica/descarta estas notas y documentarlo en `../04-registro-ia.md`.
