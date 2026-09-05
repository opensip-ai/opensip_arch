#!/usr/bin/env python3
"""Correct the D-285 COORD entry's Date/ADOPTED to its actual append date (2026-08-27); nothing else."""
import re,subprocess,hashlib,sys,os
os.chdir('/Users/sb/code/opensip-ai/opensip'); COORD='docs/coop/COORDINATOR-DECISIONS.md'
s=open(COORD).read(); i=s.rfind('\n## D-285 '); assert i>0 and '\n## D-286' not in s
head,entry=s[:i],s[i:]
assert entry.count('- **Date:** 2026-08-26')==1 and entry.count('**ADOPTED 2026-08-26.**')==1, 'unexpected entry shape'
d=subprocess.check_output(['git','log','-1','--format=%cs','791187b']).decode().strip(); assert d=='2026-08-27',d
entry=entry.replace('- **Date:** 2026-08-26','- **Date:** 2026-08-27').replace('**ADOPTED 2026-08-26.**','**ADOPTED 2026-08-27.**')
if '--apply' in sys.argv:
    open(COORD,'w').write(head+entry); print('applied; COORD sha',hashlib.sha256(open(COORD,'rb').read()).hexdigest())
else: print('dry-run OK (2 substitutions in the D-285 entry only)')
