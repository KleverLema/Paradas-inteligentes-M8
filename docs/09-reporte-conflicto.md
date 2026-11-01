# Reporte de conflicto deliberado (Semana 3)

**Proyecto:** Paradas Inteligentes — Módulo de Solicitudes de Parada (Módulo 8)  
**Fecha:** 01/11/2026  
**Responsable de la resolución:** Ariel Aguirre  
**Evidencia:** issues #8 y #9 · PR #13 y #14 · commit de resolución `0b23e0e`

## 1. Causa

Dos ramas creadas desde el mismo commit de `main` (`b51f902`) modificaron la **misma línea** de `README.md`, el requisito de versión de Python de la sección «Ejecución local en Windows»:

| Rama | Issue / PR | Commit | Cambio en la línea 44 |
|---|---|---|---|
| `fix/8-version-python-readme` | #8 / #13 | `bf866be` | Corrige el requisito de Python 3.10 a **3.11**, porque `src/repository.py` y `tests/test_api.py` importan `datetime.UTC`, disponible desde Python 3.11. |
| `docs/9-python-verificado-readme` | #9 / #14 | `d60d21f` | Mantiene Python 3.10 y agrega la versión con que se verificaron pruebas y auditoría (**3.14**). |

El PR #13 se integró primero (merge `bd251cd`). Al actualizar la rama del PR #14 con `git merge origin/main`, Git no pudo combinar automáticamente dos cambios distintos sobre la misma línea:

```text
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

## 2. Marcadores

Git dejó en `README.md` ambas versiones delimitadas por marcadores:

```text
<<<<<<< HEAD
Requiere Python 3.10 o superior (pruebas y auditoría verificadas con Python 3.14). Desde la carpeta principal del repositorio, abrir PowerShell o la terminal de Visual Studio Code y ejecutar:
=======
Requiere Python 3.11 o superior, porque el código usa `datetime.UTC`. Desde la carpeta principal del repositorio, abrir PowerShell o la terminal de Visual Studio Code y ejecutar:
>>>>>>> origin/main
```

- `<<<<<<< HEAD` a `=======`: versión de la rama actual (`docs/9-python-verificado-readme`, PR #14).
- `=======` a `>>>>>>> origin/main`: versión ya integrada en `main` (PR #13).

## 3. Resolución

Ninguna de las dos versiones era suficiente: la de `HEAD` conservaba un requisito incorrecto (3.10) y la de `main` omitía la versión verificada. Se combinaron ambas intenciones en una sola línea y se eliminaron los marcadores:

```text
Requiere Python 3.11 o superior, porque el código usa `datetime.UTC` (pruebas y auditoría verificadas con Python 3.14). Desde la carpeta principal del repositorio, abrir PowerShell o la terminal de Visual Studio Code y ejecutar:
```

Pasos ejecutados:

```bash
git checkout docs/9-python-verificado-readme
git merge origin/main               # conflicto en README.md
# edición manual de README.md: combinar ambas versiones y borrar marcadores
python -m pytest tests/ -q          # 9 passed
git add README.md
git commit -m "fix: resolver conflicto en README sobre version de Python"   # 0b23e0e
git push
```

El commit de merge `0b23e0e` tiene como padres a `d60d21f` (rama del PR #14) y `bd251cd` (`main` tras integrar el PR #13), lo que deja la resolución visible en el historial (`git log --graph`). El PR #14 se integra después de la revisión.

## 4. Prevención

| Regla | Cómo previene el conflicto | Dónde está definida |
|---|---|---|
| Un issue por cambio y aviso de los archivos afectados | Si dos issues tocan el mismo archivo, se detecta antes de crear las ramas y se coordina el orden | Plantilla de issue (`Artefactos afectados`) |
| Ramas cortas, de dos días como máximo | Menos tiempo de divergencia respecto de `main` | `CONTRIBUTING.md`, sección Ramas |
| Actualizar la rama con `git pull origin main` antes de pedir revisión | El conflicto se resuelve en la rama del autor y no al integrar | `CONTRIBUTING.md` y plantilla de PR |
| Integrar en el orden de dependencia | El segundo PR se ajusta al primero ya integrado | Revisión cruzada en el PR |
| Ejecutar las pruebas después de resolver | Evita integrar una resolución que rompa la API | `CONTRIBUTING.md`, sección Conflictos |
