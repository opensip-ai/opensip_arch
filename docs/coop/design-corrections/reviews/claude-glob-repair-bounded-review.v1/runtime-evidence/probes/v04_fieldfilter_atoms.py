"""V04 — (a) is `cmp: glob` ever admissible on a non-string field, which would make the caller's
str(v) an actual coercion the contract does not describe? (b) run the atom checker's glob vectors.

Runs in a disposable copy of the successor source, made in my own runtime.
"""
import hashlib, importlib.util, json, os, shutil, subprocess, sys

G = '/tmp/opensip-design-corrections/glob-semantics-successor.v1'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
BASE = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1'
OUT = os.path.join(BASE, 'receipts')
PY = '/tmp/opensip-architecture-review-env/bin/python'
R = {}

# ---------- (a) FieldFilter admissibility ----------
import jsonschema
SCHEMAS = {
    'policy-document.schema.json':
        os.path.join(SNAP, 'docs/coop/design-corrections/workflows/schemas/policy-document.schema.json'),
    'policy-document.v2.schema.json':
        os.path.join(SNAP, 'docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json'),
}
INT_FIELDS = ['confidenceMillionths', 'exitStatus']
rows = []
for name, p in SCHEMAS.items():
    doc = json.load(open(p))
    ff = doc['$defs'].get('FieldFilter')
    if ff is None:
        continue
    validator_schema = {'$defs': doc['$defs'], '$ref': '#/$defs/FieldFilter'}
    fields = ff['properties']['field']['enum']
    for fld in fields:
        for val in ('src/**', 5):
            inst = {'field': fld, 'cmp': 'glob', 'value': val}
            try:
                jsonschema.validate(inst, validator_schema)
                ok = 'ADMIT'
            except Exception as ex:
                ok = 'REFUSE'
            rows.append({'schema': name, 'field': fld, 'value': repr(val), 'globAdmissible': ok,
                         'fieldIsIntegerValued': fld in INT_FIELDS})
R['fieldFilterGlobAdmissibility'] = rows
print('--- is cmp:glob admissible per field? ---')
for name in SCHEMAS:
    print('  %s' % name)
    for r in [x for x in rows if x['schema'] == name]:
        flag = '  <-- INTEGER-VALUED FIELD' if r['fieldIsIntegerValued'] and r['globAdmissible'] == 'ADMIT' else ''
        print('     %-24s value=%-10s %s%s' % (r['field'], r['value'], r['globAdmissible'], flag))
bad = [r for r in rows if r['fieldIsIntegerValued'] and r['globAdmissible'] == 'ADMIT']
R['globAdmissibleOnIntegerField'] = bad
R['strCoercionIsReachable'] = bool(bad)
print('\ncmp:glob admissible on an integer-valued field (would make str(v) a real coercion):',
      R['strCoercionIsReachable'])

# ---------- (b) the atom checker ----------
KIT = os.path.join(BASE, 'disposable/globkit')
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
src = os.path.join(G, 'source')
copied = 0
for dp, dn, fn in os.walk(src):
    for n in fn:
        s = os.path.join(dp, n)
        d = os.path.join(KIT, os.path.relpath(s, src))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        copied += 1
R['disposableCopyFiles'] = copied
print('\ndisposable copy of the successor source: %d files' % copied)

chk = os.path.join(KIT, 'docs/coop/design-corrections/foundation/check-atoms.v1.py')
r = subprocess.run([PY, '-I', '-B', chk], capture_output=True, text=True,
                   cwd=os.path.dirname(chk), timeout=3600)
R['atomChecker'] = {'returncode': r.returncode, 'stdoutTail': (r.stdout or '')[-1400:],
                    'stderrTail': (r.stderr or '')[-900:]}
print('\ncheck-atoms.v1.py (successor bytes) rc=%d' % r.returncode)
print((r.stdout or '')[-1200:])
if r.returncode:
    print('--- stderr ---')
    print((r.stderr or '')[-900:])

# compare with the author's retained report
rep = os.path.join(G, 'checks/check-atoms.report.json')
if os.path.isfile(rep):
    author = json.load(open(rep))
    R['authorReportTopKeys'] = sorted(author) if isinstance(author, dict) else '<list>'
    print('\nauthor retained report keys:', R['authorReportTopKeys'])
    for k in ('unitCases', 'cases', 'passed', 'failed', 'total', 'globCases', 'result'):
        if isinstance(author, dict) and k in author:
            v = author[k]
            R.setdefault('authorReport', {})[k] = len(v) if isinstance(v, (list, dict)) else v
    print('author report summary:', json.dumps(R.get('authorReport')))

json.dump(R, open(os.path.join(OUT, 'v04-fieldfilter-atoms.json'), 'w'), indent=1, default=str)
print('\nwrote v04-fieldfilter-atoms.json')
