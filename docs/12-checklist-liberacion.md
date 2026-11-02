# Checklist de liberación v0.3.0 — Paradas Inteligentes M8

## 1. Objetivo

Establecer los controles técnicos y documentales que debe cumplir el proyecto Paradas Inteligentes M8 antes de publicar la versión v0.3.0.

Este checklist permite verificar la trazabilidad del desarrollo, las revisiones cruzadas, la calidad del código, la seguridad y la consistencia de la versión final.

## 2. Control de ramas y Pull Requests

- [ ] Verificar que la rama principal `main` esté protegida.
- [ ] Comprobar que los cambios se incorporen mediante Pull Requests.
- [ ] Verificar que cada Pull Request tenga al menos una aprobación de otro integrante.
- [ ] Confirmar que las conversaciones pendientes estén resueltas.
- [ ] Verificar que cada Pull Request esté vinculado con su Issue correspondiente.
- [ ] Comprobar que cada integrante haya realizado al menos dos Pull Requests y dos revisiones cruzadas, según la rúbrica.
- [ ] Comprobar que los cambios aprobados estén integrados a `main`.

## 3. Validación funcional y calidad del código

El proyecto utiliza Python, FastAPI y SQLite. Antes de liberar una nueva versión deben comprobarse las funcionalidades principales de la API.

Ejecutar, con el entorno y las dependencias instaladas:

```bash
python -m pytest tests/ -v
python -m ruff check src tests
```

Criterios de verificación:

- [ ] Las pruebas automatizadas finalizan satisfactoriamente.
- [ ] Se revisan y documentan los errores reportados por Ruff.
- [ ] La implementación es coherente con el contrato `api/openapi.yaml`.
- [ ] La documentación de ejecución es consistente con los requisitos del proyecto.
- [ ] Se utiliza Python 3.11 o superior, conforme al requisito mínimo documentado.

**Nota:** Las casillas deben marcarse únicamente después de ejecutar o verificar las comprobaciones correspondientes.

## 4. Seguridad y dependencias

- [ ] Verificar que no existan contraseñas, tokens ni claves privadas expuestas.
- [ ] Revisar que `.gitignore` excluya archivos temporales y secretos.
- [ ] Comprobar las dependencias declaradas en `requirements.txt`.
- [ ] Revisar los resultados de la auditoría de dependencias.
- [ ] Registrar los hallazgos y las acciones correctivas que permanezcan pendientes.

Referencia interna: `docs/10-revision-seguridad-dependencias.md`.

## 5. Conflictos y revisión cruzada

- [ ] Verificar que el conflicto deliberado entre los cambios del README haya sido documentado.
- [ ] Identificar las ramas y los commits que participaron en el conflicto.
- [ ] Comprobar que el archivo final no contenga marcadores de conflicto.
- [ ] Registrar la causa, resolución y medidas preventivas.
- [ ] Verificar que la solución haya pasado por una revisión cruzada.

Referencia interna: `docs/09-reporte-conflicto.md`.

## 6. Documentación y gobierno del repositorio

- [ ] Verificar que `README.md` esté actualizado.
- [ ] Comprobar que `CONTRIBUTING.md` documente las convenciones del equipo.
- [ ] Verificar que las plantillas de Issues y Pull Requests estén disponibles.
- [ ] Revisar la matriz comparativa Git vs SVN.
- [ ] Comprobar la existencia y coherencia del ADR-004 de selección de Git.
- [ ] Verificar que se haya declarado el uso de herramientas de inteligencia artificial cuando corresponda.

## 7. Versionamiento SemVer

Se deben comprobar las versiones correspondientes a los hitos del proyecto:

- [ ] Etiqueta `v0.1.0` verificada.
- [ ] Etiqueta `v0.2.0` verificada.
- [ ] Hito H3 aprobado y preparado para la liberación.
- [ ] Etiqueta `v0.3.0` creada sobre el commit final aprobado.
- [ ] Versión final publicada en GitHub Releases, si corresponde al procedimiento del equipo.
- [ ] Todos los integrantes identifican el mismo commit de entrega.

La etiqueta `v0.3.0` debe publicarse únicamente después de completar las integraciones y verificaciones necesarias.

## 8. Registro de evidencias

| Control | Evidencia requerida | Estado |
|---|---|---|
| Protección de main | Configuración de GitHub | Por verificar |
| Revisión cruzada | Enlaces de PR y aprobaciones | Por verificar |
| Pruebas automatizadas | Resultado de pytest | Por verificar |
| Análisis estático | Resultado de Ruff | Por verificar |
| Seguridad | Informe de revisión | Por verificar |
| Conflicto deliberado | Reporte y commits de resolución | Por verificar |
| Versión final | Enlace de tag y commit v0.3.0 | Pendiente |

Estos estados deberán actualizarse con evidencias reales antes de declarar completada la liberación.

## 9. Criterio de aprobación

La versión v0.3.0 podrá considerarse lista para su liberación cuando las verificaciones obligatorias se hayan completado, los cambios necesarios estén integrados en `main`, los hallazgos relevantes estén resueltos o documentados y exista una referencia verificable al commit final.

## 10. Referencias

- `README.md`
- `CONTRIBUTING.md`
- `requirements.txt`
- `docs/08-matriz-git-vs-svn.md`
- `docs/09-reporte-conflicto.md`
- `docs/10-revision-seguridad-dependencias.md`
- `docs/03-adr/`
- Issue #17: Checklist de liberación v0.3.0.

## 11. Declaración de uso de IA

Se utilizó ChatGPT (OpenAI, GPT-6) como herramienta de apoyo para estructurar el checklist técnico y documental, tomando como referencia el proyecto académico y los requisitos de la rúbrica de Semana 3.

El contenido debe ser verificado por el autor y sometido a revisión cruzada antes de incorporarse a la rama principal. No se presentan como ejecutadas comprobaciones que todavía estén pendientes.
