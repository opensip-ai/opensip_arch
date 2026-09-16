"""R03 — INDEPENDENT closure test for A-12 and the missing-key carrier bypass on frozen35 vs frozen34.

Invariant tested on every case: an inadmissible scope record is EITHER refused at admission OR ignored
exactly as if it were absent — it is never used as evidence. The reference answer for "ignored" is the
same inputs with that scope (and its mapping) deleted.
Cases: each of the eight subject-scope carrier fields, absent and null, on four consumption paths
(outgoing containing scope, incoming source scope, dependency pairing, a scope named by a globally
admitted attestation of another relation). Plus scope-less groups, empty-subject scopes, the root
misjoin assertion, and the schema-owner metadata change.
STANDING: atom-api, stock jsonschema and native carrier as labelled; not closed enumeration, not a Run."""
import copy, hashlib, importlib.util, json, os, sys

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
S35 = '/tmp/opensip-design-corrections/candidate-subject.v35'
F34, F35 = S34 + '/docs/coop/design-corrections/foundation', S35 + '/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
MAN35 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


man = json.load(open(MAN35))
drift = lambda: sum(1 for f in man['files'] if sha(os.path.join(S35, f['path'])) != f['sha256'])
K = load('chk35', F35 + '/check-atoms.v1.py')
AM35 = K.AM
AM34 = load('am34', F34 + '/atom_model.v1.py')
U1, U2, F_SYM, F_SUBJ = K.U1, K.U2, K.F_SYM, K.F_SUBJ
C1, C2 = K.C_PROV, K.C_PROV2
R = {'frozen35DriftBefore': drift()}
FAIL = []


def ev(mod, atom, inputs, subj=None):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj or F_SUBJ), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key}
    return {'admission': 'ADMIT', 'value': r['value'], 'causes': sorted([[c['code'], c.get('universe')] for c in r['causes']], key=json.dumps),
            'coverageIds': r['coverageIds'], 'scopeIds': r['scopeIds']}


def rec(cid, claim, ok, observed):
    R.setdefault('checks', []).append({'id': cid, 'claim': claim, 'passed': bool(ok), 'observed': observed})
    if not ok:
        FAIL.append(cid)
    print('%-4s %-66s %s' % ('ok' if ok else 'FAIL', cid[:66], json.dumps(observed, default=str)[:170]), flush=True)


FIELDS = list(AM35.SUBJECT_SCOPE_FIELDS)
R['carrierFields'] = FIELDS
REF_OUT = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'filters': []}
REF_IN = dict(REF_OUT, endpoint='target')
REACH = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'filters': []}


def path_inputs(path):
    """Returns (atom, inputs, scopeId of the scope under test)."""
    if path == 'outgoing-containing':
        i = K.base_inputs(enumerationPlan=K.plan_one(cap='references'))
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
        return REF_OUT, i, K.scope2('1')
    if path == 'incoming-source-scope':
        i = K.base_inputs(enumerationPlan=K.plan_one(cap='references'))
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
        return REF_IN, i, K.scope2('1')
    if path == 'dependency-pairing':
        i = K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'))
        K.install_pair(i, *K.paired('reachability', 'from-resolved-calls', U1, U1, [F_SYM], tag='1'))
        K.install_pair(i, *K.paired('calls', 'resolved-callee', U1, U1, [F_SYM], tag='2'))
        return REACH, i, K.scope2('2')
    if path == 'attestation-named-other-relation':
        cells = sorted([K.plan_one(cap='references')['cells'][0], K.ref_cell('calls', 'ts-tsconfig', U1, '.', C1, ['src/a.ts'])],
                       key=lambda c: (c['capabilityId'], c['languageMode'], c['workspaceRoot']))
        plan = K.plan_one(cap='references'); plan['cells'] = cells
        inv = K.inv_symbol(); inv['cellOrdinal'] = [n for n, c in enumerate(cells) if c['capabilityId'] == 'calls'][0]
        i = K.base_inputs(enumerationPlan=plan, inventories=[inv])
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
        s, sc = K.scope('calls', 'resolved-callee', U1, U1, [F_SYM], sid='9')
        i['scopes'][s] = sc
        i['incomingSearchAttestations'] = [K.incoming_att('calls', 'resolved-callee', U1, U1, [s], [inv])]
        return REF_OUT, i, s
    raise ValueError(path)


rows, violations, bypass34 = [], [], []
for path in ('outgoing-containing', 'incoming-source-scope', 'dependency-pairing', 'attestation-named-other-relation'):
    atom, base, sid = path_inputs(path)
    baseline = ev(AM35, atom, base)
    deleted = copy.deepcopy(base)
    deleted['scopes'].pop(sid)
    for cid in [c for c, s in list(deleted['coverageScopes'].items()) if s == sid]:
        deleted['coverageScopes'].pop(cid)
    deleted['incomingSearchAttestations'] = [a for a in deleted['incomingSearchAttestations'] if sid not in a['scopeRefs']]
    for f in FIELDS:
        for mode in ('absent', 'null'):
            j = copy.deepcopy(base)
            if mode == 'absent':
                j['scopes'][sid].pop(f)
            else:
                j['scopes'][sid][f] = None
            o35, o34 = ev(AM35, atom, j), ev(AM34, atom, j)
            del35, del34 = ev(AM35, atom, deleted), ev(AM34, atom, deleted)
            refused35 = o35['admission'] == 'REFUSE'
            ignored35 = (not refused35) and o35 == del35
            row = {'path': path, 'field': f, 'mode': mode, '35': o35.get('key') or [o35.get('value'), o35.get('causes')],
                   '34': o34.get('key') or [o34.get('value'), o34.get('causes')], 'deleted35': [del35.get('value'), del35.get('causes')],
                   'refused35': refused35, 'ignoredAsAbsent35': ignored35}
            if not (refused35 or ignored35):
                violations.append(row)
            if o34['admission'] == 'ADMIT' and o34 != del34 and o34 == baseline and not refused35:
                bypass34.append(row)
            if o34['admission'] == 'ADMIT' and o34.get('value') == baseline.get('value') and o34 != del34:
                row['frozen34UsedInadmissibleScopeAsEvidence'] = True
            rows.append(row)
R['carrierMatrix'] = rows
R['baselineValues'] = {p: ev(AM35, *path_inputs(p)[:2]).get('value') for p in ('outgoing-containing', 'incoming-source-scope', 'dependency-pairing', 'attestation-named-other-relation')}
print('baseline values:', R['baselineValues'])
rec('C1-inadmissible-scope-is-refused-or-ignored-never-evidence-on-35',
    '8 carrier fields x absent/null x 4 consumption paths: every frozen35 answer is an admission refusal or equals the scope-deleted answer',
    not violations, {'cases': len(rows), 'refused': sum(r['refused35'] for r in rows), 'ignoredAsAbsent': sum(r['ignoredAsAbsent35'] for r in rows),
                     'violations': violations[:3]})
used34 = [r for r in rows if r.get('frozen34UsedInadmissibleScopeAsEvidence')]
R['frozen34UsedInadmissibleScopeAsEvidence'] = [(r['path'], r['field'], r['mode'], r['34']) for r in used34]
rec('C2-frozen34-bypass-exists-and-is-closed',
    'on frozen34 some absent-key cases answered as if the inadmissible scope were admitted evidence; none of those does on frozen35',
    bool(used34) and all(r['refused35'] or r['ignoredAsAbsent35'] for r in used34),
    {'frozen34Bypasses': [(r['path'], r['field'], r['mode'], r['34'] if isinstance(r['34'], str) else r['34'][0]) for r in used34][:12]})
null_same = all(r['35'] == r['34'] for r in rows if r['mode'] == 'null')
rec('C3-null-field-behaviour-unchanged-34-to-35', 'every null-field case gives the same answer on frozen34 and frozen35', null_same,
    [(r['path'], r['field']) for r in rows if r['mode'] == 'null' and r['35'] != r['34']][:6])

# ---------------------------------------------------------------- scope-less groups and empty-subject scopes
print('\n=== scope-less groups and empty-subject scopes ===')


def empty_prog(scope=None, cov=None, att=None, inventory_rows=False, u1_evidenced=True):
    plan = K.plan_one(cap='references')
    plan['cells'].append(K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-empty', C2, ['pkg-empty/src/i.ts']))
    inv2 = K.inv_symbol(universe=U2, nid='ts-symbol:pkg-empty/src/i.ts#x', path='pkg-empty/src/i.ts', qn='x')
    inv2['cellOrdinal'] = 1
    if not inventory_rows:
        inv2.update({'rows': [], 'examinedPaths': ['pkg-empty/src/i.ts']})
    i = K.base_inputs(enumerationPlan=plan, inventories=[K.inv_symbol(), inv2])
    if u1_evidenced:
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
    sid = None
    if scope is not None:
        sid, sc = K.scope('references', 'resolved-binding', U2, U1, scope, sid='7'); sc['enumeratorClosure'] = C2
        i['scopes'][sid] = sc
        if cov:
            c, cv = K.coverage('references', 'resolved-binding', U2, U1, cid='7', cov=cov)
            i['coverages'][c] = cv; i['coverageScopes'][c] = sid
    if att:
        refs = {'own': [sid] if sid else [], 'empty': [], 'borrowed': [K.scope2('1')], 'nonexistent': [K.scope2('e')]}[att[0]]
        over = {} if att[1] == 'qual' else dict(completeSearch=False, examinedExhaustive=False, coverage='unknown',
                                                  resolutionCompleteness=K.rc_for('resolved-binding', state='partial', cov='unknown'))
        i['incomingSearchAttestations'] = [K.incoming_att('references', 'resolved-binding', U2, U1, refs, [inv2], providerClosure=C2, **over)]
    return i


cases = {
    'scopeless-no-attestation': (empty_prog(), ('indeterminate', [['source-target-search-unattested', U2]])),
    'scopeless-attestation-empty-scopeRefs': (empty_prog(att=('empty', 'qual')), ('REFUSE', 'INCOMING_SEARCH_SCHEMA')),
    'scopeless-attestation-borrowed-scope': (empty_prog(att=('borrowed', 'qual')), ('REFUSE', 'INCOMING_SEARCH_SCOPE_MISJOIN')),
    'scopeless-attestation-nonexistent-scope': (empty_prog(att=('nonexistent', 'qual')), ('REFUSE', 'INCOMING_SEARCH_SCOPE_MISJOIN')),
    'empty-subject-scope-unpaired': (empty_prog(scope=[]), ('indeterminate', [['scope-without-coverage', U2]])),
    'empty-subject-scope-complete-coverage': (empty_prog(scope=[], cov='complete'), ('true', [])),
    'empty-subject-scope-unknown-coverage': (empty_prog(scope=[], cov='unknown'), ('indeterminate', None)),
    'empty-subject-scope-qualifying-attestation': (empty_prog(scope=[], att=('own', 'qual')), ('true', [])),
    'empty-subject-scope-nonqualifying-attestation': (empty_prog(scope=[], att=('own', 'nonqual')), ('indeterminate', [['scope-without-coverage', U2]])),
    'empty-subject-scope-but-program-has-subjects': (empty_prog(scope=[], cov='complete', inventory_rows=True), ('indeterminate', [['uncovered-expected-source-subject', U2]])),
}
got = {}
bad = []
for label, (inp, (want_val, want_causes)) in cases.items():
    o = ev(AM35, REF_IN, inp)
    got[label] = o
    if want_val == 'REFUSE':
        ok = o['admission'] == 'REFUSE' and o['key'] == want_causes
    else:
        ok = o.get('value') == want_val and (want_causes is None or o.get('causes') == want_causes)
        if label == 'empty-subject-scope-unknown-coverage':
            ok = ok and any(c[0] == 'coverage-unknown' and c[1] == U2 for c in o.get('causes', []))
    if not ok:
        bad.append({label: o})
R['emptyAndScopeless'] = got
rec('E1-scopeless-and-empty-subject-scope-boundaries',
    'scope-less group: unattested, and every attestation attempt is a global refusal (SCHEMA for empty, SCOPE_MISJOIN for borrowed or nonexistent); empty-subject scope: closes only with complete Coverage or a qualifying attestation, and cannot hide real inventoried subjects',
    not bad, {'mismatches': bad, 'values': {k: v.get('value', v.get('key')) for k, v in got.items()}})
out_empty = ev(AM35, REF_OUT, empty_prog(scope=[], cov='complete'), subj={'universe': U2, 'kind': 'symbol', 'nativeSubjectId': 'ts-symbol:pkg-empty/src/i.ts#x'})
rec('E2-empty-subject-scope-never-contains-an-outgoing-subject',
    'outgoing from a subject of that program is never closed by an empty-subject scope (no containing scope -> unknown)',
    out_empty.get('value') == 'indeterminate', out_empty)
same34 = {k: ev(AM34, REF_IN, v[0]) == got[k] for k, v in cases.items()}
rec('E3-scopeless-and-empty-scope-behaviour-unchanged-34-to-35', 'these boundaries needed no code change: frozen34 answers identically',
    all(same34.values()), same34)

# ---------------------------------------------------------------- schema owner change
print('\n=== incoming-search.schema.v1.json owner change ===')
from jsonschema import Draft202012Validator  # noqa: E402
sp = 'incoming-search.schema.v1.json'
s34, s35 = json.load(open(F34 + '/' + sp)), json.load(open(F35 + '/' + sp))
valid = K.incoming_att('references', 'resolved-binding', U1, U1, [K.scope2('1')], [K.inv_symbol()])
instances = {'valid': valid, 'empty-scopeRefs': dict(valid, scopeRefs=[]), 'missing-planId': {k: v for k, v in valid.items() if k != 'planId'},
             'bad-completeSearch-type': dict(valid, completeSearch='yes'), 'extra-key': dict(valid, extra=1),
             'duplicate-scopeRefs': dict(valid, scopeRefs=[K.scope2('1'), K.scope2('1')]),
             'coverage-complete-completeSearch-false': dict(valid, completeSearch=False),
             'examinedExhaustive-false-complete': dict(valid, examinedExhaustive=False)}
verdicts = {k: [len(list(Draft202012Validator(s).iter_errors(v))) == 0 for s in (s34, s35)] for k, v in instances.items()}
rec('S1-schema-change-is-metadata-only', 'every probe instance gets the same stock-schema verdict under the frozen34 and frozen35 schema',
    all(a == b for a, b in verdicts.values()), verdicts)
joins = s35.get('x-opensip-law', {}).get('joins', [])
rec('S2-schema-metadata-now-states-carrier-and-no-untagged-fallback',
    'the owning schema join text no longer offers an untagged fallback and names the native carrier obligation',
    any('no admitted untagged-scope fallback' in j for j in joins) and not any('untagged scopes fall back' in j for j in joins), joins[5] if len(joins) > 5 else joins)
R['failed'] = FAIL
R['frozen35DriftAfter'] = drift()
print('\nfailed:', FAIL, '| frozen35 drift before/after %d/%d' % (R['frozen35DriftBefore'], R['frozen35DriftAfter']))
json.dump(R, open(os.path.join(OUT, 'r03-a12.json'), 'w'), indent=1, default=str)
print('wrote r03-a12.json')
