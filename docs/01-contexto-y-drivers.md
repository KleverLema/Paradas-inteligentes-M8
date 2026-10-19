# Práctica 01 — Contexto, stakeholders, restricciones, drivers y escenarios de calidad

**Caso:** Paradas Inteligentes — módulo de gestión de solicitudes de parada.  
**Fecha de preparación:** 15/10/2026.  
**Estado:** propuesta académica para validación grupal.  
**Base técnica analizada:** prototipo `main.py` de solicitudes de parada facilitado para este análisis. Los extractos de código y las limitaciones observadas están documentados en [evidencia técnica](05-evidencia-tecnica.md); **el código original no es un entregable de SEM01**. Se excluyen las funciones de ETA y GPS de otros documentos académicos.

## 1. Descripción y límites del sistema

API REST que registra solicitudes de parada de un pasajero en una parada del catálogo, evita solicitudes activas duplicadas mediante comprobación previa, consulta solicitudes y controla sus cambios de estado. Permite validar que las solicitudes ocurran entre las 05:00 y las 22:00. La versión suministrada tiene **almacenamiento en memoria** y cinco paradas académicas fijas de Tulcán; la clase `SolicitudOut` conserva `id_solicitud`, `id_parada`, `id_pasajero`, `hora_solicitud`, `estado`.

| Caso de uso de la API actual | Evidencia verificable |
|---|---|
| Consultar paradas habilitadas | `main.py`: `listar_paradas()` / `GET /paradas`. |
| Crear solicitud | `main.py`: `crear_solicitud()` / `POST /solicitudes`. |
| Consultar solicitud por ID | `main.py`: `obtener_solicitud()` / `GET /solicitudes/{id_solicitud}`. |
| Cambiar estado | `main.py`: `cambiar_estado()` / `PATCH /solicitudes/{id_solicitud}/estado`. |

**Fuera del alcance actual y del dosier semanal:** GPS, lectura de posición de buses, cálculo ETA, visualizadores de parada, aplicación móvil de pasajeros, SMS, pago, envío de datos a flota, alta dinámica de nuevas paradas. El SRS de otra asignatura imagina parte de estos elementos para un **proyecto más amplio**, pero no están implementados aquí.

**Supuestos propuestos para los ADR (validar con el equipo):** despliegue académico de una instancia, equipo pequeño, presupuesto limitado, un almacenamiento relacional local inicialmente, API consumida por cliente HTTP o Swagger/Postman, sin prometer producción. No se presuponen datos de pasajeros reales.

## 2. Stakeholders y concerns (intereses, no tecnologías)

| ID | Stakeholder | Rol / relación | Concerns principales | Influencia propuesta |
|---|---|---|---|---|
| S1 | Pasajero solicitante | Beneficiario de solicitudes | Que no se pierda su petición, que no se duplique, que sea sencilla y privada | Alta |
| S2 | Operador del sistema de transporte | Supervisa las solicitudes | Consultar estados correctos, no presentar información contradictoria | Alta |
| S3 | Equipo de desarrollo y pruebas | Construye y mantiene la API | Cambios acotados, pruebas repetibles y despliegue sencillo | Alta |
| S4 | Responsable de protección de datos | Evalúa tratamiento de identificadores | Restringir acceso a identificadores personales y dejar trazabilidad | Alta |
| S5 | Integrador / consumidor REST | Integra un cliente con la API | Contrato estable, errores consistentes, respuestas oportunas | Media |
| S6 | Administrador de infraestructura | Mantiene el entorno de ejecución | Poder reiniciar el servicio sin pérdida de solicitudes | Media |

**Conflictos de concerns:** S1/S5 piden rapidez y facilidad, mientras S4 requiere controles de acceso; S3 prefiere pocas dependencias, mientras S6/S1 necesitan durabilidad. No se elige tecnología en esta sección.

## 3. Restricciones y supuestos

| ID | Tipo | Restricción / condición | Origen y evidencia | Negociable |
|---|---|---|---|---|
| R1 | Negocio (actual) | Una misma pareja (`id_pasajero`, `id_parada`) no mantiene dos solicitudes activas (`PENDIENTE`, `CONFIRMADA`) | `main.py`: función `crear_solicitud()` | No |
| R2 | Negocio (actual) | Horario permitido 05:00–22:00 y transición válida de estados | `main.py`: `HORA_MINIMA`, `HORA_MAXIMA`, `TRANSICIONES_VALIDAS` | No |
| R3 | Alcance académico (actual) | Catálogo de 5 paradas y cuatro operaciones REST de negocio | `main.py` y README original | Parcial (si evoluciona el MVP) |
| R4 | Técnica (actual) | La versión entregada usa un `dict` sin persistencia; al reiniciarse se pierden solicitudes | `main.py`: `solicitudes = {}` | Sí; se busca cambiarlo |
| R5 | Organizacional (confirmado) | Equipo académico de tres integrantes y plazo de entrega del módulo | Composición del equipo: Klever Lema Tamay, Edwin Toapanta y Ariel Aguirre; calendario EVA | No (para esta entrega) |
| R6 | Económica (supuesto) | Evitar servicios de pago durante la demostración | Hipótesis académica; falta confirmación | Parcial |
| R7 | Protección de datos (a verificar) | Limitar la exposición del identificador del pasajero en entornos reales | Riesgo detectado en la API; verificar obligaciones legales aplicables antes del despliegue | No respecto al cumplimiento legal |

**Supuestos bajo validación:** una sola instancia del servidor, usuarios de prueba sintéticos, el sistema no requiere por ahora alta disponibilidad multisede y SQLite sería suficiente para un primer despliegue académico. **Hecho observado:** no hay autenticación implementada en el prototipo. Ninguno de estos supuestos equivale a un hecho probado.

## 4. Drivers arquitectónicos priorizados

| ID | Driver | Tipo / atributo principal | Origen | Importancia | Dificultad |
|---|---|---|---|---|---|
| D1 | Consistencia ante solicitudes duplicadas concurrentes | Fiabilidad | S1, S2, R1 | Alta | Alta |
| D2 | Conservación de solicitudes después del reinicio | Fiabilidad | S1, S6, R4 | Alta | Media |
| D3 | Acceso controlado a datos de solicitudes | Seguridad | S4, R7 | Alta | Media |
| D4 | Respuesta ágil en consulta y registro | Eficiencia de desempeño | S1, S5 | Media | Media |
| D5 | Cambios de almacenamiento y reglas sin reescribir toda la API | Mantenibilidad | S3, R5, R6 | Media | Media |

**Driver principal:** D1, porque una doble solicitud activa compromete la confianza en la información del sistema. D2 también es prioritario: la API anterior borra su estado con cada reinicio.

## 5. Escenarios de calidad — seis partes y medida

> Las metas numéricas son **objetivos ilustrativos propuestos**, no mediciones realizadas ni garantías de la versión actual. Deben ser validadas y, cuando exista implementación, medidas con pruebas. Un escenario se vincula a un atributo principal para respetar la rúbrica.

### E1 — Fiabilidad: evitar duplicaciones bajo concurrencia (D1)

| Parte | Especificación |
|---|---|
| Fuente | Dos o más clientes HTTP que representan solicitudes del mismo pasajero y parada. |
| Estímulo | Envían 100 solicitudes simultáneas con los mismos `id_pasajero`, `id_parada`, todas dentro de horario. |
| Entorno | Apertura del servicio, ejecución concurrente de la API en una instancia. |
| Artefacto | Servicio de solicitudes y almacenamiento transaccional propuesto. |
| Respuesta | Acepta solo una solicitud activa y rechaza el resto con HTTP 409. |
| Medida | **0 duplicados activos entre 100 solicitudes simultáneas**; 1 HTTP 201 y 99 HTTP 409, verificables en BD. |

**Estado hoy:** comprobación con `any(...)` sobre `dict` sin garantía transaccional; **E1 no verificado bajo concurrencia**.

### E2 — Fiabilidad: conservar las solicitudes (D2)

| Parte | Especificación |
|---|---|
| Fuente | Administrador de infraestructura o reinicio automático. |
| Estímulo | Se reinicia el proceso de la API tras registrar 100 solicitudes de prueba. |
| Entorno | Operación normal en servidor académico de una instancia. |
| Artefacto | Mecanismo de persistencia de solicitudes. |
| Respuesta | El servidor recupera los mismos registros y estados al arrancar. |
| Medida | **100 de 100 registros recuperados** con IDs y estados sin cambios tras el reinicio. |

**Estado hoy:** el `dict` se vacía al reiniciar; **no cumple**.

### E3 — Fiabilidad: transición de estados coherente (D1)

| Parte | Especificación |
|---|---|
| Fuente | Cliente API de pruebas. |
| Estímulo | Solicita transiciones inválidas como `ATENDIDA → PENDIENTE`. |
| Entorno | Solicitudes registradas durante operación normal. |
| Artefacto | API de actualización y máquina de estados. |
| Respuesta | Rechaza la transición y conserva el estado anterior. |
| Medida | **100 % de 20 transiciones inválidas rechazadas con HTTP 400**, sin alteraciones de estado. |

**Estado hoy:** hay `TRANSICIONES_VALIDAS`; se requiere ejecutar una batería específica para comprobar exactamente esta meta.

### E4 — Seguridad: acceso no autorizado (D3)

| Parte | Especificación |
|---|---|
| Fuente | Consumidor no autorizado o sin sesión válida. |
| Estímulo | Realiza 50 consultas a solicitudes ajenas. |
| Entorno | Entorno de prueba con mecanismo de identidad/autorización incorporado. |
| Artefacto | Capa de seguridad de API y registro de auditoría. |
| Respuesta | Deniega el acceso y registra el intento sin exponer datos del pasajero. |
| Medida | **50 de 50 accesos denegados y registrados** en una prueba controlada. |

**Estado hoy:** no existe autenticación ni autorización. **Meta futura: no cumple en el prototipo aportado.**

### E5 — Eficiencia de desempeño: consultar solicitudes (D4)

| Parte | Especificación |
|---|---|
| Fuente | Cliente de carga sintética. |
| Estímulo | Ejecuta 120 consultas por minuto al endpoint `GET /solicitudes/{id_solicitud}`. |
| Entorno | Instancia de prueba con 1 000 solicitudes precargadas, ambiente controlado. |
| Artefacto | API de consulta y mecanismo de almacenamiento. |
| Respuesta | Responde HTTP 200 para IDs existentes manteniendo la latencia objetivo. |
| Medida | **Al menos 95 % de respuestas inferiores a 2 s** durante 5 minutos de carga. |

**Estado hoy:** no se realizó esta prueba en el presente dosier; los resultados de JMeter del trabajo anterior no pueden equipararse automáticamente a esta carga.

### E6 — Mantenibilidad: sustituir almacenamiento (D5)

| Parte | Especificación |
|---|---|
| Fuente | Equipo de desarrollo. |
| Estímulo | Se solicita migrar de SQLite a otro almacenamiento SQL. |
| Entorno | Versión modular con pruebas de contrato disponibles. |
| Artefacto | Repositorio de solicitudes y capa de acceso a datos. |
| Respuesta | Cambia la implementación del repositorio conservando contratos REST y reglas de negocio. |
| Medida | **Sin cambios en rutas públicas**; modificación limitada al módulo de persistencia y configuración, estimada en **máximo 1 día-persona** (validar con prototipo). |

**Estado hoy:** la lógica de negocio y el `dict` comparten `main.py`; la meta aún no puede comprobarse.

## 6. Priorización, coherencia y trazabilidad

| Prioridad | Escenario | Driver | Justificación |
|---|---|---|---|
| 1 | E1 | D1 | Invariante central de solicitud única y alto costo de corregir concurrencia. |
| 2 | E2 | D2 | La pérdida por reinicio es una limitación demostrable del prototipo actual. |
| 3 | E4 | D3 | Riesgo de exposición de `id_pasajero` si el servicio se publica a terceros. |
| 4 | E3 | D1 | Asegura integridad del flujo de estados. |
| 5 | E5 | D4 | Permite justificar rendimiento con una carga definida. |
| 6 | E6 | D5 | Reduce costo de cambios posteriores. |

| Decisión | Escenarios protegidos | Vistas relacionadas |
|---|---|---|
| ADR-001 Persistencia local SQLite (propuesta) | E2, E5, E6 | C4 nivel 2 objetivo |
| ADR-002 Unicidad activa con BD transaccional (propuesta) | E1, E3 | C4 nivel 2 objetivo |
| ADR-003 Monolito modular FastAPI (propuesta) | E1–E6 | C4 niveles 1, 2 y matriz |

## 7. Contraste crítico y validaciones pendientes

- **Hallazgo sustentado en el código fuente revisado:** la validación de duplicados se realiza antes de insertar, sin transacción explícita, de modo que no hay evidencia para afirmar protección concurrente. Se propone E1 y ADR-002, **no se considera implementado**.
- **Hallazgo sustentado en el código fuente revisado:** no hay base de datos ni mecanismo de autenticación. Las propuestas ADR-001 y E4 deberán implementarse y ensayarse en fases futuras.
- **Dato por validar con el equipo:** escenarios y cifras de carga/persistencia, cantidad de integrantes y aceptación final del estilo. No se inventan pruebas.
- **Revisión cruzada con otro equipo:** aún pendiente, ver `02-vistas-c4/revision-cruzada.md`.

**Evidencia técnica publicada en el dosier:** [extractos y análisis del prototipo](05-evidencia-tecnica.md). Referencias metodológicas: guías de las tres sesiones del Módulo 8, Bass et al. (2021), ISO/IEC/IEEE 42010:2022 y [C4 Model](https://c4model.com/). Para formular obligaciones legales concretas se debe verificar la normativa aplicable en la fuente oficial.
