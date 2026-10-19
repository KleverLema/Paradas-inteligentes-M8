# Contexto y drivers arquitectónicos

## 1. Problema y alcance

En una gestión de solicitudes de parada deben evitarse registros contradictorios, conservarse las solicitudes y ofrecerse respuestas consistentes a los consumidores HTTP. El sistema analizado es una API REST desarrollada en Python con FastAPI, cinco paradas de catálogo y cuatro operaciones funcionales:

| Caso de uso | Operación REST | Resultado |
|---|---|---|
| Consultar paradas | `GET /paradas` | Lista de paradas disponibles |
| Registrar solicitud | `POST /solicitudes` | Nueva solicitud en estado `PENDIENTE` |
| Consultar solicitud | `GET /solicitudes/{id_solicitud}` | Solicitud y estado vigente |
| Cambiar estado | `PATCH /solicitudes/{id_solicitud}/estado` | Cambio validado por la máquina de estados |

El dominio establece el horario de **05:00 a 22:00** inclusive. Los estados son `PENDIENTE`, `CONFIRMADA`, `ATENDIDA` y `CANCELADA`; los dos últimos son terminales. Se rechaza el registro de una segunda solicitud activa para la misma pareja (`id_pasajero`, `id_parada`). La implementación consultada usa un diccionario en memoria y no incorpora autenticación. Los elementos externos como GPS, ETA, aplicación móvil o mensajería no se incluyen en este módulo.

## 2. Stakeholders y concerns

| ID | Interesado | Rol | Preocupaciones principales | Influencia |
|---|---|---|---|---|
| S1 | Pasajero | Solicita una parada | Registro único, continuidad de la solicitud y protección de su identificador | Alta |
| S2 | Operador de transporte | Da seguimiento a solicitudes | Estados coherentes, información confiable y respuesta oportuna | Alta |
| S3 | Equipo de desarrollo | Desarrolla y mantiene la API | Cambios localizados, pruebas repetibles y bajo esfuerzo de operación | Alta |
| S4 | Responsable de protección de datos | Supervisa el acceso a identificadores | Control de accesos y uso apropiado de los datos | Alta |
| S5 | Consumidor o integrador REST | Envía consultas y solicitudes HTTP | Contrato estable, errores comprensibles y latencia acotada | Media |
| S6 | Administrador de infraestructura | Opera el servicio | Reinicios seguros y recuperación de información | Media |

Existe una tensión entre velocidad de respuesta y controles de acceso, y otra entre simplicidad de despliegue y persistencia duradera. Estas preocupaciones condicionan los drivers sin imponer todavía una tecnología.

## 3. Restricciones y supuestos de diseño

| ID | Tipo | Condición | Origen | Negociabilidad |
|---|---|---|---|---|
| R1 | Negocio | No coexistirán dos solicitudes activas para el mismo pasajero y parada | Regla en `crear_solicitud()` | No |
| R2 | Negocio | Horario de servicio 05:00–22:00 y transiciones permitidas entre estados | Validación y máquina de estados de la API | No en el alcance estudiado |
| R3 | Funcional | Catálogo fijo de cinco paradas y cuatro operaciones REST | API FastAPI analizada | Parcial, por ampliación del sistema |
| R4 | Técnica | La versión base mantiene solicitudes en memoria y carece de persistencia | `solicitudes = {}` en la API | Sí; motiva el ADR-001 |
| R5 | Organizacional | Un equipo de tres integrantes desarrolla la propuesta | Organización del proyecto | No para esta fase |
| R6 | Económica | Priorizar alternativas con baja complejidad y sin infraestructura adicional de pago | Criterio de diseño para el alcance reducido | Parcial |
| R7 | Seguridad | No exponer datos de solicitudes a usuarios no autorizados en un servicio de producción | Concern de S4 y ausencia actual de autorización | No para el objetivo de protección |

**Supuestos de dimensionamiento:** una instancia de API para el alcance inicial; tráfico moderado; datos sintéticos de prueba y sin necesidad actual de operación distribuida. Son hipótesis de diseño para comparar alternativas, no capacidades medidas.

## 4. Drivers priorizados

| ID | Driver | Atributo de calidad | Origen | Importancia | Dificultad |
|---|---|---|---|---|---|
| D1 | Evitar duplicados activos incluso con solicitudes concurrentes | Fiabilidad | S1, S2, R1 | Alta | Alta |
| D2 | Recuperar solicitudes después de reiniciar el servicio | Fiabilidad | S1, S6, R4 | Alta | Media |
| D3 | Restringir el acceso a información de solicitudes | Seguridad | S4, R7 | Alta | Media |
| D4 | Mantener tiempos de consulta aceptables | Eficiencia de desempeño | S1, S5 | Media | Media |
| D5 | Reducir el impacto de cambios en almacenamiento y lógica | Mantenibilidad | S3, R5, R6 | Media | Media |

Se prioriza **D1** por el riesgo de inconsistencias de negocio y **D2** por la pérdida de estado al reiniciar. Los escenarios siguientes permiten convertir estas prioridades en medidas comprobables.

## 5. Escenarios de calidad

Cada escenario se formula mediante las seis partes: fuente, estímulo, entorno, artefacto, respuesta y medida. Las cifras son **criterios de aceptación definidos para la arquitectura objetivo**, no resultados de ensayos ya efectuados.

### E1. Fiabilidad: solicitudes concurrentes — D1

| Parte | Descripción |
|---|---|
| Fuente | Clientes HTTP simultáneos |
| Estímulo | 100 peticiones `POST /solicitudes` con la misma pareja pasajero–parada |
| Entorno | Instancia operativa, dentro del horario permitido |
| Artefacto | Servicio de registro y repositorio persistente |
| Respuesta | Registrar una sola solicitud activa y rechazar las restantes |
| Medida | 1 respuesta HTTP 201, 99 respuestas HTTP 409 y **0 duplicados activos** en almacenamiento |

### E2. Fiabilidad: recuperación tras reinicio — D2

| Parte | Descripción |
|---|---|
| Fuente | Administrador del servidor |
| Estímulo | Reiniciar la API después de registrar 100 solicitudes |
| Entorno | Una instancia y una base de datos persistente |
| Artefacto | Repositorio de solicitudes |
| Respuesta | Recuperar los registros con sus estados originales |
| Medida | **100 de 100 solicitudes recuperadas** con identificadores y estados intactos |

### E3. Fiabilidad: transiciones válidas — D1

| Parte | Descripción |
|---|---|
| Fuente | Consumidor HTTP |
| Estímulo | Enviar 20 cambios de estado no permitidos, por ejemplo `ATENDIDA → PENDIENTE` |
| Entorno | API operativa con solicitudes existentes |
| Artefacto | Regla de transición de estados |
| Respuesta | Rechazar cada solicitud sin alterar el estado almacenado |
| Medida | **20 de 20 operaciones rechazadas con HTTP 400** y 0 alteraciones indebidas |

### E4. Seguridad: acceso a solicitudes ajenas — D3

| Parte | Descripción |
|---|---|
| Fuente | Cliente sin autorización |
| Estímulo | Ejecutar 50 consultas a solicitudes de otro pasajero |
| Entorno | Servicio objetivo con identidad y autorización incorporadas |
| Artefacto | API y control de acceso |
| Respuesta | Denegar la consulta y registrar el intento sin mostrar datos sensibles |
| Medida | **50 de 50 accesos denegados y registrados** |

### E5. Eficiencia de desempeño: consulta — D4

| Parte | Descripción |
|---|---|
| Fuente | Cliente de carga |
| Estímulo | Ejecutar 120 solicitudes por minuto a `GET /solicitudes/{id_solicitud}` |
| Entorno | Una instancia de prueba con 1 000 registros durante 5 minutos |
| Artefacto | API de consulta y almacenamiento |
| Respuesta | Devolver las solicitudes existentes dentro del límite de latencia |
| Medida | **Al menos 95 % de respuestas HTTP 200 en menos de 2 segundos** |

### E6. Mantenibilidad: sustitución de base de datos — D5

| Parte | Descripción |
|---|---|
| Fuente | Equipo de desarrollo |
| Estímulo | Sustituir SQLite por otro motor relacional |
| Entorno | Arquitectura modular con pruebas de contrato |
| Artefacto | Módulo de repositorio de solicitudes |
| Respuesta | Cambiar la persistencia sin modificar rutas ni reglas de negocio |
| Medida | **0 cambios en contratos REST** y modificación limitada al adaptador y configuración, con estimación de **1 día-persona** |

## 6. Trazabilidad y priorización de escenarios

| Prioridad | Escenario | Driver | Decisión relacionada |
|---|---|---|---|
| 1 | E1: unicidad concurrente | D1 | ADR-002 |
| 2 | E2: recuperación | D2 | ADR-001 |
| 3 | E4: autorización | D3 | ADR-003 y evolución de seguridad |
| 4 | E3: transiciones | D1 | ADR-002 y lógica de dominio |
| 5 | E5: desempeño | D4 | ADR-001 / ADR-003 |
| 6 | E6: facilidad de modificación | D5 | ADR-001 / ADR-003 |

Los escenarios E1, E2 y E4 motivan las decisiones de mayor impacto. La evaluación de alternativas se desarrolla en [la matriz de decisión](03-adr/matriz-decision.md).
