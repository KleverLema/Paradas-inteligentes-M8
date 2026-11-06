# Evidencia de despliegue continuo - Semana 4

## Proyecto
Paradas Inteligentes - API de gestion de solicitudes.

## Repositorio
https://github.com/KleverLema/Paradas-inteligentes-M8

## Servicio publicado
https://paradas-inteligentes-m8.onrender.com

## Verificaciones realizadas
- Render: primer despliegue exitoso (Live).
- /docs: documentacion interactiva accesible.
- /paradas: consulta publica de paradas comprobada.
- /openapi.json: contrato accesible.
- GitHub Actions: pruebas y verificaciones configuradas.
- Render Auto-Deploy: After CI Checks Pass.

## Proceso de despliegue
1. Se propone un cambio mediante Pull Request.
2. GitHub Actions ejecuta las verificaciones.
3. Un revisor aprueba los cambios.
4. Se integra el Pull Request en main.
5. Render espera las comprobaciones de CI.
6. Si las comprobaciones pasan, Render publica la nueva version.

## Evidencia pendiente
Confirmar un nuevo despliegue automatico posterior a la
integracion de este documento y registrar su commit.
