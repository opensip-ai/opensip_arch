"""V03: independently check root's F6 discovery that the ORIGINAL v1 assembly-support
path lacked the catalog generator. Existence/size only; no file contents are read.
"""
import os

BASE = '/tmp/opensip-design-corrections/application-assembly.v1/files'
TARGETS = ['docs/operations/generate-current-design-catalog.py',
           'docs/coop/design-corrections/finalize-application.v1.py']
print('v1 assembler copied from:', BASE)
print('base dir exists:', os.path.isdir(BASE))
for rel in TARGETS:
    p = os.path.join(BASE, rel)
    print('  exists:', os.path.exists(p), '| isfile:', os.path.isfile(p), '|', rel)
# Which intermediate directory level is the first to be absent?
for rel in TARGETS:
    parts = rel.split('/')
    cur = BASE
    for seg in parts:
        cur = os.path.join(cur, seg)
        if not os.path.exists(cur):
            print('  first absent level for', rel, '->', cur)
            break
    else:
        print('  fully present:', rel, '| bytes:', os.path.getsize(cur))
