# Paradas Inteligentes — Dosier de arquitectura (Módulo 8)

**Equipo:** Klever Lema Tamay, Edwin Toapanta y Ariel Aguirre.  
**Repositorio:** https://github.com/KleverLema/Paradas-inteligentes-M8  
**Estado:** propuesta académica pendiente de revisión final del grupo y revisión cruzada.

## Alcance

El proyecto documenta la arquitectura del **módulo de gestión de solicitudes de parada** para transporte público, tomando como caso un prototipo de API REST con Python y FastAPI. El módulo base permite listar paradas, registrar y consultar solicitudes y cambiar su estado. El cálculo de ETA, el seguimiento GPS, las pantallas de parada y las notificaciones automáticas **no forman parte del módulo documentado**.

Se identificaron limitaciones en el prototipo original: almacenamiento en memoria (sin persistencia), falta de autenticación y ausencia de un mecanismo transaccional explícito contra duplicaciones concurrentes. Los ADR describen **mejoras propuestas**, no implementadas.
