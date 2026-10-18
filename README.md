# Paradas Inteligentes — Dosier de arquitectura (Módulo 8)

**Equipo:** Klever Lema Tamay, Edwin Toapanta y Ariel Aguirre.  
**Repositorio:** https://github.com/KleverLema/Paradas-inteligentes-M8  
**Estado:** propuesta académica pendiente de revisión final del grupo y revisión cruzada.

## Alcance

El proyecto documenta la arquitectura del **módulo de gestión de solicitudes de parada** para transporte público, tomando como caso un prototipo de API REST con Python y FastAPI. El módulo base permite listar paradas, registrar y consultar solicitudes y cambiar su estado. El cálculo de ETA, el seguimiento GPS, las pantallas de parada y las notificaciones automáticas **no forman parte del módulo documentado**.

Se identificaron limitaciones en el prototipo original: almacenamiento en memoria (sin persistencia), falta de autenticación y ausencia de un mecanismo transaccional explícito contra duplicaciones concurrentes. Los ADR describen **mejoras propuestas**, no implementadas.

## Entregables de SEM01

| Archivo | Contenido |
|---|---|
| [`docs/01-contexto-y-drivers.md`](docs/01-contexto-y-drivers.md) | Stakeholders, concerns, restricciones, drivers y escenarios de calidad medibles; análisis y priorización |
| [`docs/02-vistas-c4/c4-nivel1.md`](docs/02-vistas-c4/c4-nivel1.md) | Vista C4 nivel 1: sistema y entorno |
| [`docs/02-vistas-c4/c4-nivel2.md`](docs/02-vistas-c4/c4-nivel2.md) | Vista C4 nivel 2: arquitectura propuesta |
| [`docs/03-adr/`](docs/03-adr/) | ADR-001, ADR-002, ADR-003 y matriz ponderada de decisión |
| [`docs/04-registro-ia.md`](docs/04-registro-ia.md) | Uso de IA y contraste técnico; validación del grupo pendiente |
| [`docs/02-vistas-c4/revision-cruzada.md`](docs/02-vistas-c4/revision-cruzada.md) | Plantilla para revisión externa pendiente |

## Estado de la evaluación

Las medidas de calidad son **objetivos propuestos** para verificar en etapas de implementación. Los puntajes de la matriz son una **evaluación razonada de alternativas**, no resultados de un ensayo de carga. El equipo debe validar y corregir los documentos antes de presentar la versión final.

## Cómo entregar

1. Desde la carpeta descomprimida, subir a GitHub `README.md` y la carpeta `docs` completa.
2. Pulsar **Commit changes**; verificar que las vistas Mermaid se renderizan y abrir los ADR.
3. Copiar el enlace específico que aparece en GitHub al entrar al commit realizado.
4. Pegar la URL del commit en **SEM01 – Dosier de arquitectura** dentro de EVA. Si el repositorio es privado, agregar al docente cuando facilite su identificador.

El ensayo **Actividad Semana 1** se presenta por separado en Word, con la referencia bibliográfica y URL de evidencia del repositorio.
