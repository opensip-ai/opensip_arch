#!/usr/bin/env python3
"""S1 + S6 for SLOT-DERIVATION-r3: each ledger row's range contains its construct (S1), and every
non-blank, non-comment line of the reachable functions lies in exactly one row (S6). Run from the
product checkout at the pin; reads source through `git show HEAD:<path>`."""
import re, subprocess, sys
DOC = sys.argv[1] if len(sys.argv) > 1 else __file__.rsplit('/scripts/', 1)[0] + '/SLOT-DERIVATION-r3.md'
FILES = {'R': 'crates/evaluator/src/native_retention.rs', 'C': 'crates/evaluator/src/native_context.rs',
         'U': 'crates/evaluator/src/native_universe.rs'}
REACH = {'R': [(86, 120), (131, 402)], 'C': [(44, 67), (75, 223), (368, 392)],
         'U': [(43, 81), (145, 261), (271, 293), (297, 490)]}
src = {k: subprocess.run(['git', 'show', 'HEAD:' + f], capture_output=True, text=True, check=True).stdout.split('\n')
       for k, f in FILES.items()}
doc = open(DOC).read()
# Ledger rows: sections 0.4, 1 and 2 only (the helper and owner tables).
body = doc[doc.index('### 0.4'):doc.index('## 3.')]
rows = re.findall(r'^\| ([RCU]):(\d+)(?:-(\d+))?(?:; [RCU]:\d+-\d+)? \| `([^`]+)`', body, re.M)
helper = re.findall(r'^\| `[^`]+`[^|]*\| ([RCU]):(\d+)-(\d+)(?:; ([RCU]):(\d+)-(\d+))? \|', body, re.M)
cover = {k: {} for k in FILES}
bad = 0
def claim(k, a, b, tag):
    global bad
    for n in range(a, b + 1):
        if n in cover[k]:
            bad += 1; print(f'DOUBLE {k}:{n} {cover[k][n]} / {tag}')
        cover[k][n] = tag
for k, a, b, token in rows:
    a = int(a); b = int(b or a)
    seg = '\n'.join(src[k][a - 1:b])
    if token not in seg:
        bad += 1; print(f'S1 MISS {k}:{a}-{b} {token!r}')
    claim(k, a, b, f'{k}:{a}-{b}')
for h in helper:
    k, a, b = h[0], int(h[1]), int(h[2])
    # Helper rows duplicate ranges already in §1/§2 only for R; claim only ranges not yet claimed.
    if not any(n in cover[k] for n in range(a, b + 1)):
        claim(k, a, b, f'helper {k}:{a}-{b}')
    if h[3]:
        k2, a2, b2 = h[3], int(h[4]), int(h[5])
        if not any(n in cover[k2] for n in range(a2, b2 + 1)):
            claim(k2, a2, b2, f'helper {k2}:{a2}-{b2}')
missing = 0
for k, spans in REACH.items():
    for a, b in spans:
        for n in range(a, b + 1):
            line = src[k][n - 1].strip()
            if not line or line.startswith('//'):
                continue
            if n not in cover[k]:
                missing += 1; print(f'S6 UNCOVERED {k}:{n} {line[:70]}')
print(f'rows {len(rows)} helpers {len(helper)} S1/double failures {bad} S6 uncovered {missing}')
sys.exit(1 if bad or missing else 0)
