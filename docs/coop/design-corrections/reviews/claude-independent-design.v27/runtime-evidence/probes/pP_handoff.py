"""PROBE P (v27) — audit original-requirement-handoff.json: are the 123 + 8 + 3 rows intact,
all PENDING, waiver-free, and is authorSupport caveated? The blind charter must remain
uninfluenced; this only checks that the handoff does not pre-decide it."""
import collections, hashlib, json, os, re

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
p = os.path.join(PKG, 'original-requirement-handoff.json')
raw = open(p, 'rb').read()
h = json.loads(raw)
R = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'topKeys': sorted(h)}
print('handoff sha256:', R['sha256'], 'bytes', R['bytes'])
print('top keys:', R['topKeys'])
for k in h:
    v = h[k]
    print('  %-34s %-6s %s' % (k, type(v).__name__, len(v) if isinstance(v, (list, dict, str)) else v))

orig = json.load(open(os.path.join(PKG, 'historical-consumer-custody/original-requirements.json')))
for name, block, ob in (('requirements', h.get('requirements'), orig.get('requirements')),
                        # `standing` is a 185-char string here and the 8 rows live in
                        # `standingRules`; my first run picked the string and crashed.
                        ('standingRules', h.get('standingRules'), orig.get('standing')),
                        ('futureQualification', h.get('futureQualification'), orig.get('futureQualification'))):
    if block is None:
        continue
    print('\n=== %s: handoff=%d charter=%d ===' % (name, len(block), len(ob) if ob else -1))
    row = block[0]
    print('  row keys:', sorted(row) if isinstance(row, dict) else type(row).__name__)
    print('  sample  :', json.dumps(row, ensure_ascii=False)[:520])
    stat = collections.Counter()
    for r in block:
        if isinstance(r, dict):
            for kk in r:
                if 'status' in kk.lower() or 'grade' in kk.lower():
                    stat[(kk, str(r[kk]))] += 1
    print('  status/grade value counts:', dict(stat))
    R.setdefault('blocks', {})[name] = {
        'handoffCount': len(block), 'charterCount': len(ob) if ob else None,
        'rowKeys': sorted(row) if isinstance(row, dict) else None,
        'statusCounts': {'%s=%s' % k: v for k, v in stat.items()}}
    # id alignment with the frozen charter
    if ob and isinstance(ob[0], dict):
        def ids(x):
            return [str(r.get('id') or r.get('requirementId') or r.get('key') or i)
                    for i, r in enumerate(x)]
        R['blocks'][name]['idsIdenticalToCharter'] = ids(block) == ids(ob)
        print('  ids identical to frozen charter:', R['blocks'][name]['idsIdenticalToCharter'])

s = json.dumps(h)
R['waiverTokens'] = {t: len(re.findall(t, s, re.I)) for t in
                     ('waiv', 'accepted', 'satisfied', 'closed', 'PASS')}
R['pendingCount'] = len(re.findall(r'PENDING', s))
print('\nwaiver/closure tokens:', R['waiverTokens'])
print('PENDING occurrences  :', R['pendingCount'])
for k in ('independentAcceptance', 'standingRules'):
    if k in h:
        print('\n[%s]\n%s' % (k, json.dumps(h[k], indent=1, ensure_ascii=False)[:2200]))
        R['block.' + k] = h[k]
sup = [m for m in re.finditer(r'[^"]*authorSupport[^"]*', s)]
print('\nauthorSupport mentions:', len(sup))
json.dump(R, open(os.path.join(OUT, 'pP-handoff.json'), 'w'), indent=1, default=str)
print('\nwrote pP-handoff.json')
