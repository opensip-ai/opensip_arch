"""P03 — cross-owner effect of the candidate remedy. Two disposable kits built in THIS runtime from frozen35
docs, each with the SUCCESSOR atom_model bytes (sha recorded) — one unpatched, one with only the remedy
text substitution in _select_dep_coverages. Every checker that imports the atom model runs on both kits
with no arguments; stdout and exit codes are compared. No source, author or frozen tree is written."""
import hashlib, json, os, shutil, subprocess, time

S35 = '/tmp/opensip-design-corrections/candidate-subject.v35'
FSU = '/tmp/opensip-design-corrections/dependency-scope-successor.v1/source/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1'
OUT = os.path.join(BASE, 'receipts')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json'
OLD = '''    paired = []
    for sid, sc in _scopes_exact(inputs, drel, drung, source_u):
        if not any(_scope_contains(sc, nid) for nid in current_subjects):
            continue
        paired.extend(_pair_scope_coverages(sid, sc, covs, inputs))
    return _unique_pairs(paired)
'''
NEW = '''    paired, covered = [], set()
    for sid, sc in _scopes_exact(inputs, drel, drung, source_u):
        if not any(_scope_contains(sc, nid) for nid in current_subjects):
            continue
        found = _pair_scope_coverages(sid, sc, covs, inputs)
        if found:
            covered.update(sc.get("subjects") or [])
        paired.extend(found)
    if not set(current_subjects) <= covered:
        return []
    return _unique_pairs(paired)
'''
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = {f['path']: f['sha256'] for f in json.load(open(MAN))['files']}
R = {'successorAtomModelSha256': sha(FSU + '/atom_model.v1.py'), 'successorCheckAtomsSha256': sha(FSU + '/check-atoms.v1.py')}
succ_model = open(FSU + '/atom_model.v1.py', encoding='utf-8').read()
assert succ_model.count(OLD) == 1
remedy_model = succ_model.replace(OLD, NEW)
R['remedyModelSha256'] = hashlib.sha256(remedy_model.encode()).hexdigest()
CHECKERS = ['check-atoms.v1.py', 'check-replay.v3.py', 'check-semantic-replay.v3.py', 'check-candidate-replay.v3.py',
            'check-execution-replay.v3.py', 'check-execution-inputs.v1.py', 'check-provider-attribution-return.v2.py', 'check-composition.v3.py']
kits = {}
for label, model_text in (('successor', succ_model), ('remedy', remedy_model)):
    kit = os.path.join(BASE, 'disposable', 'kit-' + label)
    if os.path.isdir(kit):
        shutil.rmtree(kit)
    n = 0
    for rel, dg in man.items():
        if not rel.startswith('docs/') or rel.startswith('docs/coop/design-corrections/reviews/'):
            continue
        d = os.path.join(kit, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(S35, rel), d)
        n += 1
    fdir = os.path.join(kit, 'docs/coop/design-corrections/foundation')
    open(os.path.join(fdir, 'atom_model.v1.py'), 'w', encoding='utf-8').write(model_text)
    shutil.copy2(FSU + '/check-atoms.v1.py', os.path.join(fdir, 'check-atoms.v1.py'))
    kits[label] = {'dir': kit, 'files': n, 'atomModelSha256': sha(os.path.join(fdir, 'atom_model.v1.py'))}
    rows = {}
    for chk in CHECKERS:
        p = os.path.join(fdir, chk)
        if not os.path.isfile(p):
            rows[chk] = {'missing': True}
            continue
        t0 = time.time()
        r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True, cwd=fdir, timeout=3600)
        open(os.path.join(OUT, 'p03-%s-%s.stdout' % (label, chk)), 'w').write(r.stdout)
        open(os.path.join(OUT, 'p03-%s-%s.stderr' % (label, chk)), 'w').write(r.stderr)
        rows[chk] = {'command': [PY, '-I', '-B', p], 'returncode': r.returncode, 'seconds': round(time.time() - t0, 1),
                     'stdoutSha256': hashlib.sha256(r.stdout.encode()).hexdigest(), 'stderrTail': r.stderr[-400:] if r.returncode else ''}
        print('%-9s %-42s rc=%s %6.1fs' % (label, chk, r.returncode, rows[chk]['seconds']), flush=True)
    kits[label]['checkers'] = rows
R['kits'] = kits
cmp = {}
for chk in CHECKERS:
    a, b = kits['successor']['checkers'].get(chk, {}), kits['remedy']['checkers'].get(chk, {})
    cmp[chk] = {'bothExitZero': a.get('returncode') == 0 and b.get('returncode') == 0,
                'stdoutIdentical': a.get('stdoutSha256') == b.get('stdoutSha256')}
R['comparison'] = cmp
R['successorUnchangedAfter'] = sha(FSU + '/atom_model.v1.py') == R['successorAtomModelSha256']
R['frozen35Drift'] = sum(1 for rel, dg in man.items() if sha(os.path.join(S35, rel)) != dg)
print(json.dumps(cmp, indent=1))
print('successor unchanged:', R['successorUnchangedAfter'], '| frozen35 drift:', R['frozen35Drift'])
json.dump(R, open(os.path.join(OUT, 'p03-consumer-regression.json'), 'w'), indent=1, default=str)
print('wrote p03-consumer-regression.json')
