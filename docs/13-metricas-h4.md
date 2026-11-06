# Metricas aproximadas de H4 y limites de DORA

**Fuente:** historial de Git (`git log main --first-parent`) actualizado en esta copia; los datos deben conservarse en el commit final.
**Metodo:** se cuentan commits de fusion de Pull Requests. La latencia aproximada compara la fecha del ultimo commit del PR (`merge^2`) con la fecha del merge. **No** es tiempo de entrega a produccion.

## Indicadores que se pueden medir con este repositorio

- PR fusionados observados en los ultimos 7 dias: **11**.
- Tiempo aproximado mediano de ultimo commit a merge: **1.49 h**.

| PR | Commit de merge | Fecha y hora de merge (con zona) | Ultimo commit a merge (horas) |
|---|---|---|---:|
| #21 | `7b7d635` | 2026-11-05T23:28-05:00 | 0.92 |
| #20 | `d539a7a` | 2026-11-05T08:16-05:00 | 7.76 |
| #18 | `aacd55e` | 2026-11-04T23:04-05:00 | 75.88 |
| #19 | `72d4996` | 2026-11-04T23:02-05:00 | 22.40 |
| #14 | `e045d97` | 2026-11-01T19:02-05:00 | 0.63 |
| #13 | `bd251cd` | 2026-11-01T18:24-05:00 | 1.45 |
| #12 | `5cd03b1` | 2026-11-01T18:24-05:00 | 1.45 |
| #11 | `580b71e` | 2026-11-01T18:23-05:00 | 1.49 |
| #10 | `0f17552` | 2026-11-01T18:23-05:00 | 1.49 |
| #4 | `e9075b9` | 2026-11-01T17:31-05:00 | 0.56 |
| #3 | `cbf54e6` | 2026-11-01T17:18-05:00 | 3.94 |

## Las metricas DORA de despliegue NO son inferibles del historial Git

| Indicador DORA | Resultado defendible | Fuente necesaria |
|---|---|---|
| Frecuencia de despliegue | N/D | Historial de despliegues de produccion |
| Lead time de cambios a produccion | N/D | Commit + timestamp de produccion |
| Tiempo de recuperacion de despliegue fallido | N/D | Incidentes de produccion con inicio y cierre |
| Tasa de cambios fallidos | N/D | Despliegues fallidos / total de despliegues |
| Tasa de retrabajo | N/D | Definicion operativa y cambios no planificados |

**Interpretacion critica:** el pipeline CI que pasa y los PR mergeados son evidencias de verificacion e integracion, no de despliegue productivo. Para medir DORA de verdad deberia existir un destino de despliegue, registro de eventos e incidencias.

**Importante:** los tiempos de PR son indicadores auxiliares locales aproximados; la fecha del ultimo commit no refleja necesariamente cuando comenzo el trabajo ni las esperas de revision.
