# Revisión de secretos, dependencias e integración por PR (Semana 3)

**Proyecto:** Paradas Inteligentes — Módulo de Solicitudes de Parada (Módulo 8)  
**Fecha de revisión:** 01/11/2026  
**Revisado por:** Ariel Aguirre  
**Referencia:** prácticas PS.1, PS.3 y PW.4 del SSDF (Souppaya et al., 2022).

## 1. Secretos y credenciales

Se revisó el historial completo de todas las ramas (`git log -p --all`, 23 commits) en busca de contraseñas, tokens, claves de API y claves privadas:

```bash
git log -p --all | grep -inE "password|passwd|secret|token|api[_-]?key|BEGIN [A-Z ]*PRIVATE|aws_access|ghp_|gho_"
git log --all --name-only --format= | sort -u | grep -iE '\.env|\.db$|\.pem|\.key$|id_rsa'
```

| Verificación | Resultado |
|---|---|
| Patrones de credenciales en el contenido | **Sin hallazgos.** Las únicas coincidencias son la palabra «tokens» en la descripción de costos de `docs/08-matriz-evaluacion-case.md`. |
| Archivos sensibles versionados (`.env`, `*.db`, claves) | **Sin hallazgos.** |
| Configuración con credenciales | **No aplica.** La API usa SQLite local (`paradas.db`) sin usuario ni contraseña. |

**Prevención:** el `.gitignore` excluye `.env`, `.env.*`, `*.db`, `*.sqlite3` y entornos virtuales (issue #5), y la plantilla de PR incluye la verificación de secretos.

## 2. Dependencias

Se instalaron las dependencias de `requirements.txt` en un entorno limpio con Python 3.14 y se auditaron con `pip-audit` 2.10.1 contra la base de vulnerabilidades de PyPI (PyPA Advisory Database).

| Paquete | Restricción en `requirements.txt` | Versión resuelta | Vulnerabilidades conocidas |
|---|---|---|---|
| fastapi | `>=0.110.0` | 0.162.0 | Ninguna |
| starlette (dependencia de fastapi) | — | 1.10.0 | Ninguna |
| uvicorn[standard] | `>=0.28.0` | 0.54.0 | Ninguna |
| pydantic | `>=2.0.0` | 2.14.2 | Ninguna |
| pytest | `>=8.0.0` | 9.2.0 | Ninguna |
| httpx | `>=0.27.0` | 0.28.1 | Ninguna |
| pytest-asyncio | `>=0.23.0` | 1.4.1.post1 | Ninguna |
| ruff | `>=0.3.0` | 0.17.3 | Ninguna |

Resultado de `pip-audit`: **No known vulnerabilities found.**

Con las versiones resueltas, `pytest` ejecutó las **9 pruebas sin fallos**. `ruff check src tests` reportó **1 error** (`RUF059`, variable `client` sin usar en `tests/test_api.py:62`), producido por una regla que no existía en la versión de Ruff usada en la Semana 2.

**Observaciones:**

- Las restricciones `>=` sin límite superior permiten que una instalación nueva resuelva versiones distintas a las probadas; así apareció el hallazgo de Ruff. Se recomienda fijar versiones probadas (por ejemplo, `ruff==0.17.3`) o mantener un archivo de restricciones, y repetir esta auditoría cuando se agregue una dependencia.
- La corrección de `RUF059` se registrará en un issue propio, para no mezclarla con esta revisión.

## 3. Integración por pull request

Desde la sesión 8, los cambios a `main` deben entrar por pull request revisado. Al momento de esta revisión, `main` está protegida y no tiene commits posteriores a `v0.2.0`; todos los cambios de la Semana 3 están en ramas con PR vinculados a su issue (#1, #2, #5, #6 y #7).

La verificación se repite antes de etiquetar `v0.3.0`: todo commit de `main` posterior a `v0.2.0` debe pertenecer a un PR integrado.

```bash
git log --first-parent --oneline v0.2.0..main   # solo deben aparecer merges de PR
```

Los commits anteriores a `v0.2.0` (por ejemplo, «Add files via upload») entraron directamente a `main` antes de activar la protección; no se reescribieron para no alterar las etiquetas `v0.1.0` y `v0.2.0`.

## Referencias

Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1: Recommendations for mitigating the risk of software vulnerabilities* (NIST Special Publication 800-218). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
