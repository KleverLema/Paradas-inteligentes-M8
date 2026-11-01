# Guía de contribución

Esta guía define cómo el equipo de **Paradas Inteligentes** integra cambios en el repositorio. Desde la Semana 3, todo cambio entra a `main` mediante pull request (PR) revisado por otro integrante.

## Flujo de trabajo

El equipo usa **GitHub Flow**: `main` siempre contiene una versión ejecutable y cada cambio se desarrolla en una rama corta.

1. **Issue:** crear o tomar un issue que describa el cambio y asignárselo.
2. **Rama:** crear la rama desde `main` actualizada.
3. **Commits:** registrar commits atómicos con Conventional Commits.
4. **PR:** abrir el PR con la plantilla y vincular el issue con `Closes #n`.
5. **Revisión cruzada:** al menos un integrante distinto del autor revisa y aprueba.
6. **Merge:** el autor integra el PR después de la aprobación y elimina la rama.

```bash
git checkout main
git pull
git checkout -b docs/12-matriz-git-svn
# ... cambios ...
git add <archivos>
git commit -m "docs: agregar matriz comparativa Git vs SVN"
git push -u origin docs/12-matriz-git-svn
gh pr create --fill --reviewer <usuario>
```

## Ramas

- `main` está protegida: no admite commits directos ni force push y exige una aprobación.
- Formato del nombre: `tipo/numero-issue-descripcion-corta`, en minúsculas y con guiones. Ejemplos: `feat/8-cancelar-solicitud`, `fix/9-transicion-estado`, `docs/12-matriz-git-svn`.
- Una rama atiende un solo issue y no debe durar más de dos días. Si `main` avanza, actualizar la rama con `git pull origin main` antes de pedir revisión.
- La rama se elimina después del merge.

## Commits

Los mensajes siguen [Conventional Commits 1.0.0](https://www.conventionalcommits.org/es/v1.0.0/):

```
<tipo>(<ámbito opcional>): <descripción en minúsculas y en imperativo>
```

| Tipo | Uso en el proyecto |
|---|---|
| `feat` | Nueva funcionalidad de la API |
| `fix` | Corrección de un error |
| `docs` | Documentación en `docs/`, `README.md` o esta guía |
| `test` | Pruebas en `tests/` |
| `refactor` | Cambio interno sin modificar el comportamiento |
| `style` | Formato o correcciones de Ruff sin cambio funcional |
| `chore` | Configuración, dependencias, `.gitignore` o plantillas |

Reglas:

- **Un commit, un cambio lógico.** No mezclar, por ejemplo, un cambio en `src/repository.py` con la actualización de un ADR.
- Descripción de 72 caracteres como máximo y sin punto final.
- Un cambio incompatible en el contrato de la API se marca con `!` (`feat!: ...`) y se explica en el cuerpo del commit.
- No usar mensajes genéricos como `Add files via upload`, `cambios` o `update`.

## Pull requests

- Completar la plantilla del PR: qué cambia, por qué, cómo se verificó e issue vinculado (`Closes #n`).
- Antes de abrir el PR, ejecutar las pruebas y el linter:

  ```bash
  python -m pytest tests/ -v
  python -m ruff check src tests
  ```

- Si el PR modifica `api/openapi.yaml`, validarlo con Spectral (`spectral lint api/openapi.yaml`).
- Mantener el PR pequeño, de preferencia con menos de 300 líneas cambiadas.
- Integrar con **Create a merge commit**, para conservar los commits atómicos y la evidencia de revisión en el historial.

## Revisión cruzada

- Cada integrante abre al menos 2 PR por entrega y revisa al menos 2 PR de sus compañeros.
- La revisión se hace en **Files changed**, con comentarios en las líneas concretas.
- Los comentarios deben ser sustantivos: señalar un error, una omisión respecto del issue o la rúbrica, un riesgo o una mejora verificable. Un "LGTM" no constituye revisión.
- El revisor elige **Request changes** cuando hay correcciones pendientes y **Approve** cuando las verifica.
- El autor responde cada comentario, corrige en la misma rama y marca la conversación como resuelta.

## Conflictos

1. Actualizar la rama: `git pull origin main`.
2. Abrir los archivos marcados por Git y resolver los bloques `<<<<<<<`, `=======` y `>>>>>>>` con la versión acordada.
3. Ejecutar las pruebas, luego `git add <archivo>` y `git commit -m "fix: resolver conflicto en <archivo>"`.
4. Si el conflicto involucra trabajo de otro integrante, acordar la resolución en el PR.

## Versiones

- Las versiones siguen [SemVer 2.0.0](https://semver.org/lang/es/) y se marcan con etiquetas anotadas sobre `main` al cerrar cada hito: `v0.1.0` (H1), `v0.2.0` (H2), `v0.3.0` (H3).

  ```bash
  git tag -a v0.3.0 -m "H3: repositorio gobernado"
  git push origin v0.3.0
  ```

## Seguridad

- No versionar secretos, credenciales, archivos `.env`, bases de datos locales (`*.db`) ni entornos virtuales.
- Las dependencias nuevas se agregan a `requirements.txt` en un PR propio y se revisan con `pip-audit -r requirements.txt`.
- No ingresar datos personales ni credenciales en herramientas de IA. Su uso se registra en `docs/04-registro-ia.md`.
