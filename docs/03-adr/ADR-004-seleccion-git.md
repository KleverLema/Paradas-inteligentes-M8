# ADR-004 — Sistema de control de versiones: Git

**Fecha:** 01/11/2026  
**Estado:** Aceptada.  
**Hito:** H3 — Repositorio gobernado · **Fundamento:** [Matriz Git vs SVN](../08-matriz-git-vs-svn.md).

## Contexto

El equipo de tres integrantes desarrolla la API de Paradas Inteligentes (Python, FastAPI y SQLite) en equipos propios y en horarios distintos. El repositorio contiene solo archivos de texto: código, pruebas, el contrato `api/openapi.yaml` y documentación en Markdown. La evaluación del módulo exige trazabilidad verificable: commits convencionales, issues vinculados a pull requests, revisión cruzada, protección de `main` y etiquetas SemVer por hito (`v0.1.0`, `v0.2.0`, `v0.3.0`).

## Alternativas

**A1. Git, alojado en GitHub:** sistema distribuido; cada clon contiene el historial completo y las ramas son punteros ligeros (Chacon & Straub, 2014).

**A2. Apache Subversion (SVN):** sistema centralizado cliente-servidor con revisiones globales numeradas, ramas como copias de directorios y autorización por ruta (Collins-Sussman et al., 2011).

## Decisión

Seleccionar **A1, Git alojado en GitHub**, con el flujo GitHub Flow definido en [CONTRIBUTING.md](../../CONTRIBUTING.md). La decisión se basa en la matriz comparativa:

- Las ramas cortas por issue no tienen costo en Git y son la base de la revisión mediante pull request.
- El trabajo sin conexión permite registrar commits atómicos localmente y publicarlos después.
- Los hashes de commit y las etiquetas permiten citar evidencia verificable en cada entrega.
- GitHub ofrece issues, pull requests, revisión obligatoria y protección de ramas, que el curso evalúa. GitHub retiró el soporte para clientes Subversion en 2024, por lo que SVN exigiría otro servidor.

## Consecuencias

- **Positivas:** cada cambio queda vinculado a un issue, un PR y una revisión; `main` se mantiene ejecutable; el aporte de cada integrante se identifica en el historial.
- **Negativas:** el equipo debe dominar conceptos de Git más complejos que en SVN (ramas remotas, fusión y resolución de conflictos). La disciplina de commits convencionales y ramas cortas no la impone Git: depende de `CONTRIBUTING.md`, de las plantillas y de la protección de `main`.
- **Riesgos:** Git no restringe la lectura de partes del repositorio; cualquier secreto versionado queda en todo el historial. Se mitiga con `.gitignore`, la lista de control del PR y la revisión de secretos registrada en el hito H3.

## Cuándo aplicaría SVN

Se reconsideraría Subversion si el proyecto cambiara a un contexto con alguna de estas condiciones:

- Permisos de lectura o escritura por directorio dentro de un mismo repositorio, por ejemplo, módulos con información confidencial para distintos proveedores.
- Archivos binarios grandes que no se pueden fusionar (planos, modelos o multimedia) y que requieren bloqueo de archivos.
- Repositorios muy grandes en los que cada integrante solo necesita descargar un subdirectorio.
- Una organización que exige un servidor central único con revisiones numeradas secuencialmente.

Ninguna de estas condiciones se cumple en el alcance actual del proyecto.

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion: For Subversion 1.7*. O'Reilly Media. https://svnbook.red-bean.com
