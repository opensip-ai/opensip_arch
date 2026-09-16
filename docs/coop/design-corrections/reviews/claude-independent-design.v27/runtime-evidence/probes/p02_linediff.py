"""Probe 02 — exact line-level diff of every changed file, from manifest-authenticated
v26 bytes to manifest-authenticated v27 bytes. Read-only on both snapshots."""
import difflib, hashlib, json, os

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
R26 = '/tmp/opensip-design-corrections/candidate-subject.v26'
R27 = '/tmp/opensip-design-corrections/candidate-subject.v27'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)

m26 = {r['path']: r for r in json.load(open(os.path.join(REV, 'candidate-subject.v26.json')))['files']}
m27 = {r['path']: r for r in json.load(open(os.path.join(REV, 'candidate-subject.v27.json')))['files']}
changed = sorted(p for p in set(m26) & set(m27) if m26[p]['sha256'] != m27[p]['sha256'])

report = {'changedCount': len(changed), 'files': []}
for rel in changed:
    p26, p27 = os.path.join(R26, rel), os.path.join(R27, rel)
    b26, b27 = open(p26, 'rb').read(), open(p27, 'rb').read()
    auth26 = hashlib.sha256(b26).hexdigest() == m26[rel]['sha256']
    auth27 = hashlib.sha256(b27).hexdigest() == m27[rel]['sha256']
    l26 = b26.decode('utf-8', 'replace').splitlines()
    l27 = b27.decode('utf-8', 'replace').splitlines()
    sm = difflib.SequenceMatcher(None, l26, l27, autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        hunks.append({'tag': tag, 'v26Lines': [i1 + 1, i2], 'v27Lines': [j1 + 1, j2],
                      'removed': i2 - i1, 'added': j2 - j1})
    report['files'].append({
        'path': rel, 'v26Authentic': auth26, 'v27Authentic': auth27,
        'sha26': m26[rel]['sha256'], 'sha27': m27[rel]['sha256'],
        'lines26': len(l26), 'lines27': len(l27),
        'hunkCount': len(hunks), 'hunks': hunks,
        'v27ChangedLineRanges': sorted({(h['v27Lines'][0], h['v27Lines'][1]) for h in hunks if h['tag'] != 'delete'}),
    })

json.dump(report, open(os.path.join(OUT, 'p02-linediff.json'), 'w'), indent=1)
print('all v26 bytes authentic:', all(f['v26Authentic'] for f in report['files']))
print('all v27 bytes authentic:', all(f['v27Authentic'] for f in report['files']))
print()
for f in report['files']:
    rng = ', '.join('%d-%d' % r for r in f['v27ChangedLineRanges']) or '(deletions only)'
    print('%-72s %3d hunks  v27 lines: %s' % (f['path'].split('/')[-1], f['hunkCount'], rng[:120]))
