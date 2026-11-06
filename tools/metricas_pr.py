"""Documento con métricas trazables de flujo Git y límites de DORA.
Usa merges de primer padre; no inventa eventos de despliegue.
"""
from pathlib import Path
import subprocess
from datetime import datetime, timezone
from statistics import median
import re

def git(*args):
    return subprocess.check_output(['git',*args],text=True,encoding='utf-8',errors='replace').strip()

raw=git('log','main','--first-parent','--format=%H|%cI|%s','-80')
merges=[]
for row in raw.splitlines():
    parts=row.split('|',2)
    if len(parts)!=3: continue
    sha,dt,subj=parts
    m=re.search(r'Merge pull request #(\d+)',subj,re.I)
    if not m: continue
    merged=datetime.fromisoformat(dt)
    try:
        tip=datetime.fromisoformat(git('show','-s','--format=%cI',f'{sha}^2'))
        delta=max(0,(merged-tip).total_seconds()/3600)
    except subprocess.CalledProcessError:
        continue
    merges.append((int(m.group(1)),sha[:7],merged,round(delta,2)))

recent=[x for x in merges if (datetime.now(timezone.utc)-x[2].astimezone(timezone.utc)).days<=7]
lines=[
'# Metricas aproximadas de H4 y limites de DORA',
'',
'**Fuente:** historial de Git (`git log main --first-parent`) actualizado en esta copia; los datos deben conservarse en el commit final.',
'**Metodo:** se cuentan commits de fusion de Pull Requests. La latencia aproximada compara la fecha del ultimo commit del PR (`merge^2`) con la fecha del merge. **No** es tiempo de entrega a produccion.',
'',
'## Indicadores que se pueden medir con este repositorio',
'',
f'- PR fusionados observados en los ultimos 7 dias: **{len(recent)}**.',
f'- Tiempo aproximado mediano de ultimo commit a merge: **{median([m[3] for m in recent]):.2f} h**.' if recent else '- Tiempo de ultimo commit a merge: **N/D** (no hay merges recientes detectables).',
'',
'| PR | Commit de merge | Fecha y hora de merge (con zona) | Ultimo commit a merge (horas) |',
'|---|---|---|---:|',
]
for n,sha,date,delta in recent[:20]:
    lines.append(f'| #{n} | `{sha}` | {date.isoformat(timespec="minutes")} | {delta:.2f} |')
lines.extend([
'',
'## Las metricas DORA de despliegue NO son inferibles del historial Git',
'',
'| Indicador DORA | Resultado defendible | Fuente necesaria |',
'|---|---|---|',
'| Frecuencia de despliegue | N/D | Historial de despliegues de produccion |',
'| Lead time de cambios a produccion | N/D | Commit + timestamp de produccion |',
'| Tiempo de recuperacion de despliegue fallido | N/D | Incidentes de produccion con inicio y cierre |',
'| Tasa de cambios fallidos | N/D | Despliegues fallidos / total de despliegues |',
'| Tasa de retrabajo | N/D | Definicion operativa y cambios no planificados |',
'',
'**Interpretacion critica:** el pipeline CI que pasa y los PR mergeados son evidencias de verificacion e integracion, no de despliegue productivo. Para medir DORA de verdad deberia existir un destino de despliegue, registro de eventos e incidencias.',
'',
'**Importante:** los tiempos de PR son indicadores auxiliares locales aproximados; la fecha del ultimo commit no refleja necesariamente cuando comenzo el trabajo ni las esperas de revision.',
])
out=Path('docs/13-metricas-h4.md')
out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Metricas creadas en',out,'(',len(recent),'PR recientes )')
