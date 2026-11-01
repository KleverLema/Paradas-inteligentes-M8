## Qué cambia

<!-- Resumen breve del cambio. -->

## Por qué

<!-- Motivo del cambio y relación con el hito o la rúbrica. -->

Closes #

## Cómo se verificó

- [ ] `python -m pytest tests/ -v` pasa sin errores
- [ ] `python -m ruff check src tests` no reporta errores
- [ ] Si cambia `api/openapi.yaml`: `spectral lint api/openapi.yaml` sin errores
- [ ] La documentación afectada (`README.md`, `docs/`) está actualizada

## Lista de control

- [ ] Los commits siguen Conventional Commits y son atómicos
- [ ] La rama está actualizada con `main`
- [ ] No se versionan secretos, credenciales, `.env` ni bases de datos locales
- [ ] Si se usó IA, quedó registrada en `docs/04-registro-ia.md`
