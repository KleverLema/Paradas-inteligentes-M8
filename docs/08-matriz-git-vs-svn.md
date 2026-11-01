# Matriz comparativa Git vs SVN (Semana 3)

**Proyecto:** Paradas Inteligentes — Módulo de Solicitudes de Parada (Módulo 8)  
**Equipo:** Klever Lema Tamay · Edwin Toapanta · Ariel Aguirre  
**Fecha:** 01/11/2026  
**Propósito:** Fundamentar la selección del sistema de control de versiones registrada en el ADR-004 (`docs/03-adr/`).

## 1. Alcance

La matriz compara **Git** y **Apache Subversion (SVN)** en las siete dimensiones vistas en clase. Se apoya en los capítulos 1 y 2 de *Version Control with Subversion* (Collins-Sussman et al., 2011) y en los capítulos 1 y 3 de *Pro Git* (Chacon & Straub, 2014). SVN no se practicó en el repositorio; la columna de SVN se basa en la lectura.

## 2. Matriz

| Dimensión | Git | Subversion (SVN) | Implicación para el proyecto |
|---|---|---|---|
| **Modelo** | Distribuido: cada clon contiene el repositorio completo con todo su historial; no hay un punto único de fallo (Chacon & Straub, 2014, cap. 1.1). | Centralizado cliente-servidor: un único repositorio en el servidor y copias de trabajo en cada cliente, con el modelo copiar-modificar-fusionar y bloqueo opcional (Collins-Sussman et al., 2011, cap. 1). | Los tres integrantes trabajan en equipos propios y en horarios distintos; el modelo distribuido evita depender de un servidor del equipo. |
| **Historial** | Guarda instantáneas del proyecto identificadas por un hash SHA-1, lo que garantiza su integridad; el historial se puede reorganizar localmente antes de publicarlo (Chacon & Straub, 2014, cap. 1.3). | Numera revisiones globales y secuenciales (r1, r2…) para todo el árbol; cada commit es atómico y el historial vive en el servidor (Collins-Sussman et al., 2011, cap. 1). | Los hashes de Git permiten citar evidencia verificable (commits, PR y etiquetas `v0.1.0`, `v0.2.0`) en las entregas. |
| **Ramas** | Una rama es un puntero ligero a un commit; crear y fusionar ramas es rápido y forma parte del trabajo diario (Chacon & Straub, 2014, cap. 3.1). | Las ramas son copias económicas de directorios en el repositorio (por convención `trunk/`, `branches/`, `tags/`); se crean en el servidor (Collins-Sussman et al., 2011). | GitHub Flow, definido en `CONTRIBUTING.md`, requiere ramas cortas por issue, que en Git no tienen costo. |
| **Trabajo sin conexión** | Casi todas las operaciones son locales: commit, historial, diferencias y ramas funcionan sin red (Chacon & Straub, 2014, cap. 1.3). | Sin conexión solo se puede editar y revisar los cambios propios (`svn status`, `svn diff`, `svn revert`) gracias a la copia prístina de la copia de trabajo; `commit`, `update` y `log` requieren el servidor (Collins-Sussman et al., 2011, cap. 2). | Permite registrar commits atómicos sin conexión y publicarlos después con `git push`. |
| **Permisos** | No controla permisos por sí mismo: quien clona obtiene todo el repositorio. El control de escritura se delega en el servidor o la plataforma (ramas protegidas, PR obligatorio) o en hooks (Chacon & Straub, 2014, cap. 8.4). | El servidor puede autorizar lectura y escritura por ruta (*path-based authorization*), hasta el nivel de directorio (Collins-Sussman et al., 2011). | Basta con permisos a nivel de repositorio y la protección de `main` en GitHub; el proyecto no tiene partes confidenciales. |
| **Rendimiento** | Operaciones locales muy rápidas; el clon inicial descarga todo el historial, costoso en repositorios grandes con muchos archivos binarios (Chacon & Straub, 2014, cap. 1.3). | El checkout descarga solo la revisión pedida y admite copias parciales de un subdirectorio; las consultas al historial dependen de la red (Collins-Sussman et al., 2011, cap. 2). | El repositorio es pequeño y solo de texto (Python, YAML y Markdown); el costo del clon completo es despreciable. |
| **Ecosistema** | Estándar de la industria: GitHub, GitLab, revisión mediante PR, CI/CD e integración nativa con VS Code (Chacon & Straub, 2014, cap. 6). | Herramientas maduras (TortoiseSVN, Apache con `mod_dav_svn`), pero con menos integración en plataformas actuales; GitHub retiró el soporte para clientes Subversion en enero de 2024 (GitHub, 2023). | El curso evalúa issues, PR, revisiones, protección de rama y etiquetas, que existen en GitHub, donde está alojado el proyecto. |

## 3. Síntesis

| Criterio de decisión | Ventaja |
|---|---|
| Colaboración con ramas cortas y revisión cruzada | Git |
| Trabajo sin conexión y commits locales | Git |
| Trazabilidad verificable (hashes, PR, etiquetas) | Git |
| Integración con la plataforma del curso (GitHub) | Git |
| Control de acceso por directorio | SVN |
| Archivos binarios grandes y bloqueo de archivos | SVN |
| Copias parciales de repositorios muy grandes | SVN |

Para Paradas Inteligentes, Git es la opción adecuada: el equipo es pequeño y distribuido, el repositorio es de texto y la evaluación se basa en el flujo de PR de GitHub. SVN sería preferible en un contexto con permisos por directorio, archivos binarios grandes que requieren bloqueo o una organización que exige un servidor central único. La decisión se registra en el ADR-004.

## 4. Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion: For Subversion 1.7*. O'Reilly Media. https://svnbook.red-bean.com

GitHub. (2023, 20 de enero). *Sunsetting Subversion support*. The GitHub Blog. https://github.blog/2023-01-20-sunsetting-subversion-support/
