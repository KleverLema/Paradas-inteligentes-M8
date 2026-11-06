"""Búsqueda limitada de patrones de secretos de alta confianza en archivos Git.
No sustituye una revisión de seguridad profesional ni un detector completo.
"""
from pathlib import Path
import re
import subprocess
import sys

PATTERNS = (
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'gh[pousr]_[A-Za-z0-9]{36,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{60,}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
)
files = subprocess.check_output(['git','ls-files','-z']).decode('utf-8',errors='replace').split('\0')
findings=[]
for file in files:
    if not file or file.startswith(('node_modules/', 'docs-generada/')):
        continue
    p=Path(file)
    if not p.is_file() or p.stat().st_size > 3_000_000:
        continue
    content=p.read_text(encoding='utf-8',errors='ignore')
    for number,line in enumerate(content.splitlines(),1):
        if any(pattern.search(line) for pattern in PATTERNS):
            findings.append(f'{file}:{number}: patron sensible detectado')
if findings:
    print('\n'.join(findings), file=sys.stderr)
    sys.exit(1)
print(f'Sin patrones de secretos de alta confianza en {len(files)} rutas de Git.')
