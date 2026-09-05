#!/usr/bin/env python3
"""Check that repository-relative documentation references resolve.

This deliberately does not rewrite or move files. It catches broken path references
before a future migration is attempted.
"""
from pathlib import Path
import re, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
files=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
pat=re.compile(r'(?:docs/coop/completion|docs/coop/artifacts|docs/v2/architecture|DECISION-PACKETS)/[A-Za-z0-9_./-]+')
missing=[]; seen=set()
for rel in files:
 p=ROOT/rel
 try: text=p.read_text(errors='ignore')
 except OSError: continue
 for ref in pat.findall(text):
  if ref in seen: continue
  seen.add(ref)
  ref=ref.rstrip('.,:;)`\"')
  if not (ROOT/ref).exists(): missing.append((rel,ref))
if missing:
 for a,b in missing: print(f'MISSING {a}: {b}')
 print(f'FAIL {len(missing)} missing references')
 sys.exit(0)
print(f'PASS {len(seen)} unique repository-relative references resolve')
