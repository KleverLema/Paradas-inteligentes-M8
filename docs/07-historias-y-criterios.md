# Práctica 07 — Historias de Usuario y Criterios de Aceptación en Gherkin (Semana 2)

**Proyecto:** Paradas Inteligentes — Módulo de Solicitudes de Parada (Módulo 8)  
**Equipo:** Klever Lema Tamay · Edwin Toapanta · Ariel Aguirre  
**Fecha:** 24/10/2026  
**Estado:** Historias y criterios vinculados a los escenarios de arquitectura E1–E6  

---

## 1. Alcance y Trazabilidad con el Dossier de Arquitectura

Este documento formaliza los requisitos funcionales del módulo de gestión de solicitudes de parada mediante **Historias de Usuario (HU)** y **Criterios de Aceptación (CA)** redactados en sintaxis estructurada **Gherkin** (`Dado que / Cuando / Entonces`). 

Cada criterio está directamente vinculado a los **Escenarios de Calidad (E1–E6)**, **Drivers Arquitectónicos (D1–D5)** y **Decisiones de Arquitectura (ADR-001, ADR-002, ADR-003)** definidos en la Semana 1:

* **E1 (Consistencia / Concurrencia - D1):** Evitar solicitudes activas duplicadas simultáneas (`ADR-002`).
* **E2 (Durabilidad / Persistencia - D2):** Conservar solicitudes y sus estados tras el reinicio del servicio (`ADR-001`).
* **E3 (Fiabilidad / Transiciones - D1):** Impedir transiciones ilegales entre estados.
* **E4 (Seguridad / Privacidad - D3):** Restricción de exposición indebida de datos del pasajero.
* **E5 (Desempeño - D4):** Respuesta ágil en operaciones de consulta y registro.
* **E6 (Mantenibilidad - D5):** Estructura modular desacoplada del motor de almacenamiento (`ADR-003`).

---

## 2. Historias de Usuario y Criterios de Aceptación en Gherkin

### HU01 — Consulta de Catálogo de Paradas Habilitadas
> **Como:** Pasajero del sistema de transporte urbano  
> **Quiero:** Consultar el catálogo de paradas disponibles en la red  
> **Para:** Conocer los puntos oficiales de embarque y obtener sus identificadores para registrar mi solicitud  

* **Driver asociado:** `D4` (Eficiencia y usabilidad).  
* **Restricción:** `R3` (Catálogo inicial de 5 paradas académicas en Tulcán).  
* **Endpoint REST:** `GET /paradas`

#### Criterios de Aceptación en Gherkin:

```gherkin
Característica: Consulta de catálogo de paradas (HU01)

  Escenario: CA01.1 - Listado exitoso de paradas habilitadas
    Dado que el servicio de paradas inteligentes se encuentra en operación normal
    Cuando un cliente envía una petición HTTP "GET" al endpoint "/paradas"
    Entonces el servicio debe responder con un código de estado HTTP 200 OK
    Y la respuesta debe ser una lista en formato JSON que contenga 5 paradas habilitadas
    Y cada elemento debe incluir "id_parada", "nombre", "latitud" y "longitud"

  Escenario: CA01.2 - Contrato y tipos de datos del catálogo
    Dado que se consulta el catálogo de paradas mediante "GET /paradas"
    Cuando se inspecciona la respuesta JSON
    Entonces el "id_parada" debe ser un número entero positivo
    Y el "nombre" debe ser una cadena de texto no vacía
    Y las coordenadas geográficas deben ser números decimales válidos
```

---

### HU02 — Creación de Solicitud de Parada
> **Como:** Pasajero esperando en una parada autorizada  
> **Quiero:** Registrar una solicitud de recogida para una parada específica dentro del horario permitido  
> **Para:** Notificar a las unidades en tránsito que deben detenerse a recogerme  

* **Drivers asociados:** `D1` (Consistencia y no duplicidad), `D2` (Durabilidad de solicitud).  
* **Restricciones:** `R1` (Una sola solicitud activa por par pasajero/parada), `R2` (Horario operativo de 05:00 a 22:00).  
* **Escenarios vinculados:** `E1` (Protección concurrente), `E2` (Persistencia transaccional).  
* **ADRs asociados:** `ADR-001` (SQLite), `ADR-002` (Unicidad en BD).  
* **Endpoint REST:** `POST /solicitudes`

#### Criterios de Aceptación en Gherkin:

```gherkin
Característica: Registro de solicitudes de parada (HU02)

  Escenario: CA02.1 - Creación exitosa de solicitud dentro de franja horaria permitida
    Dado que la hora actual del sistema se encuentra entre las "05:00" y las "22:00"
    Y la parada con "id_parada" 1 existe en el catálogo
    Y el pasajero "pasajero-101" no posee ninguna solicitud activa en la parada 1
    Cuando el cliente envía una petición HTTP "POST" a "/solicitudes" con el cuerpo:
      """
      {
        "id_parada": 1,
        "id_pasajero": "pasajero-101"
      }
      """
    Entonces el servicio debe responder con un código de estado HTTP 201 Created
    Y la respuesta JSON debe contener un "id_solicitud" asignado
    Y el campo "estado" de la solicitud creada debe ser "PENDIENTE"
    Y la solicitud debe quedar almacenada de forma persistente en la base de datos

  Escenario: CA02.2 - Rechazo de solicitud fuera de franja horaria permitida (R2)
    Dado que la hora de la solicitud se sitúa fuera del intervalo 05:00 a 22:00 (por ejemplo "23:15")
    Cuando el cliente envía una petición HTTP "POST" a "/solicitudes"
    Entonces el servicio debe rechazar la solicitud respondiendo con un código de estado HTTP 400 Bad Request
    Y el cuerpo del error debe especificar que el horario de atención es de 05:00 a 22:00
    Y ninguna solicitud debe ser persistida en la base de datos

  Escenario: CA02.3 - Rechazo de solicitud duplicada activa para el mismo pasajero y parada (E1, R1, ADR-002)
    Dado que el pasajero "pasajero-101" ya tiene una solicitud registrada con estado "PENDIENTE" en la parada 1
    Cuando dicho pasajero intenta enviar una nueva petición HTTP "POST" a "/solicitudes" para la parada 1
    Entonces el servicio debe rechazar la segunda petición respondiendo con un código de estado HTTP 409 Conflict
    Y el mensaje de error debe indicar que ya existe una solicitud activa para dicho pasajero en esa parada
    Y el total de solicitudes activas para ese par (pasajero, parada) debe mantenerse estrictamente en 1

  Escenario: CA02.4 - Rechazo por parada inexistente en el catálogo
    Dado que no existe ninguna parada registrada con "id_parada" 999
    Cuando un cliente envía una petición HTTP "POST" a "/solicitudes" con "id_parada": 999
    Entonces el servicio debe responder con un código de estado HTTP 404 Not Found
    Y el cuerpo de respuesta debe indicar que la parada especificada no existe
```

---

### HU03 — Consulta de Solicitud de Parada por Identificador
> **Como:** Pasajero o Personal de monitoreo  
> **Quiero:** Consultar los datos de una solicitud de parada mediante su identificador único  
> **Para:** Conocer el estado actual del servicio y verificar si ha sido confirmada o atendida  

* **Drivers asociados:** `D2` (Recuperación y durabilidad), `D4` (Rendimiento).  
* **Escenarios vinculados:** `E2` (Persistencia tras reinicio), `E5` (Desempeño en consulta < 2s).  
* **ADR asociado:** `ADR-001` (Almacenamiento relacional).  
* **Endpoint REST:** `GET /solicitudes/{id_solicitud}`

#### Criterios de Aceptación en Gherkin:

```gherkin
Característica: Consulta de solicitudes individuales (HU03)

  Escenario: CA03.1 - Consulta exitosa de solicitud existente
    Dado que existe una solicitud previamente registrada con "id_solicitud" 1
    Cuando el cliente envía una petición HTTP "GET" al endpoint "/solicitudes/1"
    Entonces el servicio debe responder con un código de estado HTTP 200 OK
    Y la respuesta debe incluir los campos "id_solicitud", "id_parada", "id_pasajero", "hora_solicitud" y "estado"

  Escenario: CA03.2 - Consulta de solicitud inexistente
    Dado que no existe ningún registro con "id_solicitud" 9999
    Cuando el cliente envía una petición HTTP "GET" al endpoint "/solicitudes/9999"
    Entonces el servicio debe responder con un código de estado HTTP 404 Not Found
    Y el mensaje de error debe indicar que la solicitud no fue encontrada

  Escenario: CA03.3 - Durabilidad y recuperación tras reinicio del servicio (E2, ADR-001)
    Dado que se registraron solicitudes de parada válidas en el sistema
    Cuando el proceso del servidor se reinicia o se reconecta
    Y el cliente consulta nuevamente una solicitud previamente guardada mediante "GET /solicitudes/{id}"
    Entonces el servicio debe responder con HTTP 200 OK y devolver exactamente el mismo estado y atributos previos
```

---

### HU04 — Gestión y Actualización del Estado de una Solicitud
> **Como:** Operador del sistema de transporte urbano  
> **Quiero:** Actualizar el estado de una solicitud existente conforme avanza la unidad de transporte  
> **Para:** Garantizar el flujo de atención secuencial y coherente de las solicitudes  

* **Driver asociado:** `D1` (Consistencia e integridad de estados).  
* **Restricción:** `R2` (Máquina de estados finita y transiciones permitidas).  
* **Escenario vinculado:** `E3` (Transiciones válidas).  
* **Endpoint REST:** `PATCH /solicitudes/{id_solicitud}/estado`

#### Máquina de Estados Permitida:
* `PENDIENTE` $\longrightarrow$ `CONFIRMADA` | `CANCELADA`
* `CONFIRMADA` $\longrightarrow$ `ATENDIDA` | `CANCELADA`
* `ATENDIDA` $\longrightarrow$ *(Estado terminal, no admite cambios)*
* `CANCELADA` $\longrightarrow$ *(Estado terminal, no admite cambios)*

#### Criterios de Aceptación en Gherkin:

```gherkin
Característica: Actualización de estado de solicitudes (HU04)

  Escenario: CA04.1 - Transición válida de PENDIENTE a CONFIRMADA
    Dado que existe una solicitud con "id_solicitud" 1 en estado "PENDIENTE"
    Cuando el operador envía una petición HTTP "PATCH" a "/solicitudes/1/estado" con el cuerpo:
      """
      {
        "nuevo_estado": "CONFIRMADA"
      }
      """
    Entonces el servicio debe responder con un código de estado HTTP 200 OK
    Y el campo "estado" de la solicitud debe ser actualizado a "CONFIRMADA"

  Escenario: CA04.2 - Transición válida de CONFIRMADA a ATENDIDA
    Dado que existe una solicitud con "id_solicitud" 1 en estado "CONFIRMADA"
    Cuando el operador envía una petición HTTP "PATCH" a "/solicitudes/1/estado" con:
      """
      {
        "nuevo_estado": "ATENDIDA"
      }
      """
    Entonces el servicio debe responder con un código de estado HTTP 200 OK
    Y el estado de la solicitud debe pasar a ser "ATENDIDA"
    Y la solicitud deja de considerarse activa para efectos de nuevas peticiones del pasajero

  Escenario: CA04.3 - Rechazo de transición inválida (E3, R2)
    Dado que una solicitud con "id_solicitud" 1 se encuentra en estado terminal "ATENDIDA"
    Cuando se intenta enviar una petición HTTP "PATCH" para cambiar su estado a "PENDIENTE"
    Entonces el servicio debe rechazar el cambio respondiendo con un código de estado HTTP 400 Bad Request
    Y el cuerpo de error debe detallar que la transición "ATENDIDA -> PENDIENTE" no está permitida
    Y el estado de la solicitud en la base de datos debe permanecer inalterado como "ATENDIDA"

  Escenario: CA04.4 - Actualización de estado en solicitud inexistente
    Dado que no existe una solicitud con identificador 8888
    Cuando se envía una petición HTTP "PATCH" a "/solicitudes/8888/estado"
    Entonces el servicio debe responder con un código de estado HTTP 404 Not Found
```

---

## 3. Matriz de Trazabilidad Integral (Requisitos $\leftrightarrow$ Arquitectura)

| Historia de Usuario | Criterios de Aceptación | Endpoint REST | Escenario de Calidad | Driver Priorizado | Decisión de Diseño |
|---|---|---|:---:|:---:|:---:|
| **HU01: Catálogo de Paradas** | CA01.1, CA01.2 | `GET /paradas` | E5 | D4 (Eficiencia) | `ADR-003` (Monolito modular) |
| **HU02: Crear Solicitud** | CA02.1, CA02.2, CA02.3, CA02.4 | `POST /solicitudes` | E1, E2 | D1 (Consistencia), D2 (Durabilidad) | `ADR-001` (SQLite), `ADR-002` (Unicidad activa) |
| **HU03: Consultar Solicitud** | CA03.1, CA03.2, CA03.3 | `GET /solicitudes/{id}` | E2, E5 | D2 (Durabilidad), D4 (Desempeño) | `ADR-001` (SQLite transaccional) |
| **HU04: Actualizar Estado** | CA04.1, CA04.2, CA04.3, CA04.4 | `PATCH /solicitudes/{id}/estado` | E3 | D1 (Integridad de estados) | `ADR-003` (Reglas de negocio desacopladas) |
