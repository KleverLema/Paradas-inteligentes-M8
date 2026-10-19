# Coherencia entre las vistas arquitectónicas

Las vistas C4 describen el mismo sistema con diferente grado de detalle: el nivel 1 muestra sus relaciones externas; el nivel 2 descompone el sistema en contenedores de la arquitectura objetivo.

| Elemento de consistencia | C4 nivel 1 | C4 nivel 2 | Relación con decisiones |
|---|---|---|---|
| Límite del sistema | Gestión de solicitudes de parada | Mismo límite, descompuesto en API y SQLite | ADR-003 |
| Cliente HTTP | Consumidor externo | Consumidor externo | Contrato GET/POST/PATCH |
| Equipo técnico | Actor de pruebas | Actor de pruebas | Escenarios E1–E6 |
| Almacenamiento | No aparece, por ser detalle interno | Contenedor SQLite | ADR-001 y ADR-002 |
| Persistencia de solicitudes | Necesidad de continuidad del servicio | Interacción SQL con base de datos | E2 |
| Integridad de solicitudes | Funcionalidad del sistema | Transacciones del repositorio | E1 |
| Autorización | Interés de protección de datos | Responsabilidad futura de la API | E4 |

En ambos niveles, las relaciones están etiquetadas y las denominaciones principales coinciden. La vista de nivel 2 representa el estado objetivo; no modifica las funciones actuales ni incorpora GPS, ETA o mensajería como componentes existentes.
