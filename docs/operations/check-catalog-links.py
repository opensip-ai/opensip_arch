#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[2]
files=list((root/'docs/catalog').glob('*.md'))
pat=re.compile(r'\[[^\]]+\]\(([^)#]+)\)')
bad=[]; n=0
for f in files:
 for ref in pat.findall(f.read_text()):
  if ref.startswith(('http:','https:','#')): continue
  n+=1
  target=(f.parent/ref).resolve()
  if not target.exists(): bad.append((str(f.relative_to(root)),ref))
if bad:
 for f,r in bad: print(f'MISSING {f}: {r}')
 print(f'FAIL {len(bad)} catalog links of {n}')
 sys.exit(1)
print(f'PASS {n} catalog links')
