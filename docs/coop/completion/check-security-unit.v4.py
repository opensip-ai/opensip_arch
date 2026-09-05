#!/usr/bin/env python3
"""Retained checker for the security completion unit v4 (design evidence only).

Usage: check-security-unit.v2.py [--report PATH]

Verifies, from security-completion.v3.md's stated rules: the canonical-profile vectors; every
example document against its closed schema; the signature envelope positive and every negative
(preimage mismatch, role confusion, namespace mismatch, unauthorized key, malformed) with the
section 2.2 precedence; the manifest admission checks (v11 shape subset and the host capability
registry) with the wrong-rung and unknown-capability negatives; the grant-journal example
(chain recomputation, column/body binding, locator, and the SQLite append-only / contiguity /
terminal guards re-exercised on a fresh database); and the four DR-126 profile templates against
the encoded v48 structural constraints. Writes a JSON report with the sha256 of every input,
the environment, and per-check results. Qualifies nothing.
"""
import hashlib
import json
import os
import platform
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import security_unit_lib_v4 as L  # noqa: E402

FX = os.path.join(HERE, 'security-fixtures.v4')
SCH = os.path.join(HERE, 'security-schemas.v4')
PT = {'PT-FS-READ-PROJECT', 'PT-FS-READ-COMPONENT', 'PT-FS-WRITE-HOST-STATE', 'PT-PROC-EXEC-DECLARED', 'PT-NET-EGRESS', 'PT-ENV-READ', 'PT-HOST-EFFECT-BROKERED'}
NAME = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$')
UUID = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

results = []
inputs = {}


def rec(name, ok, detail=''):
    results.append({'check': name, 'result': 'PASS' if ok else 'FAIL', 'detail': detail})


def rb(rel):
    p = os.path.join(HERE, rel)
    b = open(p, 'rb').read()
    inputs[rel] = L.sha256_hex(b)
    return b


def rj(rel):
    return json.loads(rb(rel).decode('utf-8'))


def admit_manifest(obj, registry):
    """Subset of component-manifest-schemas.v11 admission plus the host capability registry
    (analysis-quality-completion.v1.md section 3). Returns a refusal string or None."""
    req = ['manifestSchemaVersion', 'kind', 'stableId', 'name', 'version', 'role', 'commands', 'capabilities', 'platforms', 'dependencies', 'declarations', 'permissions', 'provenance', 'stateMigration', 'updateData', 'compatibility']
    for r in req:
        if r not in obj:
            return 'RJ-6 MISSING_REQUIRED_FIELD:' + r
    if obj['kind'] != 'component':
        return 'RJ-6 UNKNOWN_KIND'
    if not UUID.match(obj['stableId']):
        return 'RJ-6 NON_UUID_STABLE_ID'
    if obj['role'] != 'analyzer':
        return 'RJ-6 UNKNOWN_ROLE'
    if not NAME.match(obj['name']):
        return 'RJ-3 name charset'
    roots = [c for c in obj['commands'] if 'parent' not in c]
    if len(roots) != 1 or roots[0]['name'] != obj['name']:
        return 'RJ-2 ROOT_COMMAND_NAME_MISMATCH'
    for p in obj['permissions']:
        if p.get('permission') not in PT:
            return 'RJ-6 UNKNOWN_PERMISSION_TOKEN'
    for pl in obj['platforms']:
        paths = [e['path'] for e in pl['tree']['entries']]
        for path in paths:
            segs = path.split('/')
            if path.startswith('/') or any(s in ('', '.', '..') for s in segs) or '\\' in path or '\x00' in path or unicodedata.normalize('NFC', path) != path:
                return 'RJ-3 REFUSE_PATH_VIOLATION:' + path
        if len(set(p.casefold() for p in paths)) != len(paths):
            return 'RJ-3 duplicate under case-fold'
        if pl['entrypoint'] not in paths:
            return 'RJ-3 entrypoint not in tree'
    for k in ('stateMigration', 'updateData'):
        if obj[k].get('reserved') is not True:
            return 'RJ-6 RESERVED_FIELD_POPULATED:' + k
    hc = obj['compatibility'].get('hostCore')
    if not (isinstance(hc, dict) and set(hc) == {'min', 'max', 'includeMin', 'includeMax'}):
        return 'compatibility.hostCore not an interval'
    reg = {r['capabilityId']: (r['relation'], r['rung']) for r in registry}
    seen = set()
    for c in obj['capabilities']:
        cid = c.get('capabilityId')
        if cid not in reg:
            return 'CAPABILITY-REGISTRY unknown capability:' + str(cid)
        if c.get('roleSubprotocol') != 'typescript' or c.get('subprotocolVersion') != 1:
            return 'CAPABILITY-REGISTRY control tuple mismatch:' + cid
        dd = c.get('declarationData')
        if not (isinstance(dd, dict) and set(dd) == {'relation', 'rung'}) or (dd['relation'], dd['rung']) != reg[cid]:
            return 'CAPABILITY-REGISTRY relation/rung mismatch:' + cid
        seen.add(cid)
    if seen != set(reg):
        return 'CAPABILITY-REGISTRY preview release must advertise all five'
    return None


def main():
    report_path = None
    if '--report' in sys.argv:
        report_path = sys.argv[sys.argv.index('--report') + 1]
    vec = rj('security-vectors.v4.json')
    for s in ('envelope', 'root', 'revocation', 'catalog', 'registry', 'registry-view', 'payload', 'journal-record', 'permission-policy', 'tcb-profile-template'):
        rb('security-schemas.v4/%s.schema.json' % s)
    rb('security-schemas.v4/grant-journal.sql')
    rb('security_unit_lib_v4.py')

    # 1. canonical vectors
    rec('V-UR1', L.canonical_bytes({'': 1, '\U00010000': 2}).hex() == vec['V-UR1']['canonicalHex'] and L.domain_digest(L.DOMAIN_TAGS['test'], {'': 1, '\U00010000': 2})[0] == vec['V-UR1']['sha256'])
    ur2 = {'a': 0, 'b': -1, 'c': L.I64MAX, 'd': L.I64MIN}
    rec('V-UR2', L.canonical_bytes(ur2).decode() == vec['V-UR2']['canonical'] and L.domain_digest(L.DOMAIN_TAGS['test'], ur2)[0] == vec['V-UR2']['sha256'])
    rec('V-UR3-NFC', L.canonical_bytes({'s': 'é'}).hex() == vec['V-UR3-NFC']['canonicalHex'])
    rec('V-UR4', L.canonical_bytes({'s': 'a"b\\c/de\tfég\U0001f600'}).hex() == vec['V-UR4']['canonicalHex'])
    cases = {'V-UR2-REJECT-OVER': lambda: L.canon({'x': 2**63}), 'V-UR2-REJECT-UNDER': lambda: L.canon({'x': -2**63 - 1}), 'V-UR3-REJECT': lambda: L.canon({'s': 'é'}),
             'V-UR5-REJECT': lambda: L.canon({'s': '\ud800'}), 'V-FLOAT-REJECT': lambda: L.canon({'a': 1, 'b': 2.0}), 'V-NFC-KEY-COLLISION': lambda: L.canon({'é': 1, 'é': 2}),
             'V-DUP-KEY-REJECT': lambda: L.load_json_strict(b'{"a":1,"a":2}')}
    for name, fn in cases.items():
        try:
            fn(); rec(name, False, 'accepted')
        except L.Reject as e:
            rec(name, str(e).split(':')[0] == vec['rejects'][name], str(e))

    # 2. schemas + examples
    examples = {'root': 'root.example.json', 'revocation': 'revocation.example.json', 'catalog': 'catalog.example.json', 'registry': 'registry.example.json', 'payload': 'payload.example.json', 'permission-policy': 'permission-policy.example.json', 'registry-view': 'registry-view.project-a.example.json'}
    objs = {}
    for sch, fn in examples.items():
        obj = rj('security-fixtures.v4/' + fn); objs[sch] = obj
        try:
            L.validate(obj, L.load_schema(sch)); rec('schema:' + sch, True)
        except L.SchemaError as e:
            rec('schema:' + sch, False, str(e))
    root_doc = objs['root']
    rec('root.semantic-admission.positive', L.admit_root(root_doc) == [], str(L.admit_root(root_doc))[:200])
    root, adm_ref = L.admit_root_document(root_doc)
    rec('root.admission-boundary.positive', isinstance(root, L.AdmittedRoot) and adm_ref == [], str(adm_ref)[:120])
    rec('root.M1-raw-dict-refused-by-verify_envelope', L.verify_envelope(b'x', {}, root_doc, 'manifest')[0] == 'ROOT-NOT-ADMITTED')
    rec('root.M1-kernel-attestation-keys-must-be-empty', 'ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY' in L.admit_root(dict(root_doc, kernelAttestationKeys=[root_doc['rootKeys'][0]])) and L.admit_root_document(dict(root_doc, kernelAttestationKeys=[root_doc['rootKeys'][0]]))[0] is None)
    for name in vec['rootNegatives']:
        neg = rj('security-fixtures.v4/root.negative.%s.json' % name)
        shape_ok = True
        try:
            L.validate(neg, L.load_schema('root'))
        except L.SchemaError:
            shape_ok = False
        refusals = L.admit_root(neg)
        boundary = L.admit_root_document(neg)
        rec('root.semantic-admission.negative:' + name, bool(refusals) and boundary[0] is None, 'shape-valid=%s refusals=%s boundary=%s' % (shape_ok, refusals[:3], boundary[1][:2]))
    # a shape-valid root with a weak role threshold must not let one signature verify
    weak = rj('security-fixtures.v4/root.negative.role-threshold-1.json')
    single = rj('security-fixtures.v4/typescript-analyzer.envelope.json'); single = json.loads(json.dumps(single)); single['signatures'] = single['signatures'][:1]
    weak_adm = L.admit_root_document(weak)[0]
    outcome, detail = L.verify_envelope(rb('security-fixtures.v4/typescript-analyzer.manifest.json'), single, weak_adm if weak_adm is not None else weak, 'manifest', publisher_namespace='opensip')
    rec('root.weak-threshold-cannot-verify', outcome == 'ROOT-NOT-ADMITTED', outcome + ' ' + detail[:120])
    # 2a. cross-validation with the standard validator when the review environment exists (SEC pre-freeze advisory)
    JS_PY = '/tmp/opensip-architecture-review-env/bin/python'
    js_available = os.path.exists(JS_PY)
    version_field = {'root': 'rootSchema', 'revocation': 'revocationSchema', 'catalog': 'catalogSchema', 'registry': 'registrySchema', 'payload': 'payloadSchema', 'permission-policy': 'policySchema', 'registry-view': 'registryViewSchema'}
    for sch, obj in objs.items():
        mutant = json.loads(json.dumps(obj)); mutant[version_field[sch]] = True
        try:
            L.validate(mutant, L.load_schema(sch)); custom_rejects = False
        except L.SchemaError:
            custom_rejects = True
        rec('schema-mutant-bool-const:' + sch, custom_rejects, 'custom validator must reject true for const 1')
        if js_available:
            code = ('import json,sys,jsonschema\nsch=json.load(open(sys.argv[1]));ok=json.load(open(sys.argv[2]));bad=json.loads(sys.argv[3])\n'
                    'jsonschema.Draft202012Validator.check_schema(sch)\njsonschema.validate(ok,sch,cls=jsonschema.Draft202012Validator)\n'
                    'try:\n jsonschema.validate(bad,sch,cls=jsonschema.Draft202012Validator); print("MUTANT-ACCEPTED")\nexcept jsonschema.ValidationError:\n print("OK")')
            r = subprocess.run([JS_PY, '-c', code, os.path.join(SCH, sch + '.schema.json'), os.path.join(FX, examples[sch]), json.dumps(mutant)], capture_output=True, text=True)
            rec('jsonschema-crossval:' + sch, r.returncode == 0 and r.stdout.strip() == 'OK', (r.stdout + r.stderr).strip()[-300:])
    rec('jsonschema-env-present', js_available, JS_PY + (' used' if js_available else ' absent: cross-validation skipped, custom validator only'))
    # 2b. controlled parse refusals
    for name, b, expect in (('parse.invalid-utf8', b'\xff\xfe{"a":1}', 'INVALID_UTF8'), ('parse.nesting-too-deep', ('[' * 70 + ']' * 70).encode(), 'NESTING_TOO_DEEP'),
                            ('parse.huge-integer', b'{"a":1' + b'0' * 5000 + b'}', 'INTEGER_OUT_OF_RANGE'), ('parse.too-large', b'{"a":"' + b'x' * (L.MAX_METADATA_BYTES + 1) + b'"}', 'METADATA_TOO_LARGE'),
                            ('parse.malformed', b'{"a":', 'MALFORMED_JSON'), ('parse.nan', b'{"a":NaN}', 'NON_FINITE_FORBIDDEN')):
        try:
            L.load_json_strict(b); rec(name, False, 'accepted')
        except L.Reject as e:
            rec(name, str(e).split(':')[0] == expect, str(e))
    # 2c. registry store and scoped views
    store = objs['registry']; LIVE = ('active', 'deprecated-alias-window')
    live = [e for e in store['entries'] if e['status'] in LIVE]
    keys = [(e['stableId'], e['version'], e['scope'], e['projectKey']) for e in live]
    rec('registry.store.global-uniqueness', len(set(keys)) == len(keys) and all((e['projectKey'] is None) == (e['scope'] == 'global') for e in store['entries']))
    retired_pairs = {(r['stableId'], json.dumps(r['provenance'], sort_keys=True)) for r in store['retiredIds']}
    rec('registry.store.never-readmit-ledger', all((e['stableId'], json.dumps(e['provenance'], sort_keys=True)) in retired_pairs for e in store['entries'] if e['status'] in ('retired', 'revoked'))
        and all(not any(l['stableId'] == r['stableId'] and json.dumps(l['provenance'], sort_keys=True) != json.dumps(r['provenance'], sort_keys=True) for l in live) for r in store['retiredIds']))
    store_pre = L.domain_digest(L.DOMAIN_TAGS['registry'], store)[0]
    for vf in ('registry-view.project-a.example.json', 'registry-view.project-b.example.json'):
        view = rj('security-fixtures.v4/' + vf)
        try:
            L.validate(view, L.load_schema('registry-view')); ok = True
        except L.SchemaError as e:
            ok = False; rec('registry-view.schema:' + vf, False, str(e))
        pk = view['scopeContext']['projectKey']
        vis = [e for e in store['entries'] if e['scope'] == 'global' or e['projectKey'] == pk]
        expected = {}
        for e in vis:
            sb = None
            if e['scope'] == 'global' and e['status'] in LIVE:
                for p in vis:
                    if p['scope'] == 'project' and p['status'] in LIVE and p['projectKey'] == pk and (p['stableId'], json.dumps(p['provenance'], sort_keys=True), p['version']) == (e['stableId'], json.dumps(e['provenance'], sort_keys=True), e['version']):
                        sb = {'stableId': p['stableId'], 'version': p['version'], 'scope': 'project'}
            expected[(e['stableId'], e['version'], e['scope'], e['projectKey'])] = sb
        got = {(e['stableId'], e['version'], e['scope'], e['projectKey']): e['shadowedBy'] for e in view['entries']}
        rec('registry-view.scope-and-shadowing:' + vf, ok and got == expected and view['sourceStoreDigest'] == store_pre, 'projectKey=%s visible=%d shadowed=%d' % (pk, len(got), sum(1 for v in got.values() if v)))
    va = rj('security-fixtures.v4/registry-view.project-a.example.json'); vb = rj('security-fixtures.v4/registry-view.project-b.example.json')
    rec('registry-view.per-project-shadow-differs', any(e['shadowedBy'] for e in va['entries']) and not any(e['shadowedBy'] for e in vb['entries']), 'project A shadows the global entry; project B does not')
    rec('registry-view.digests-recorded', vec['registryViews']['project-a'] == L.domain_digest(L.DOMAIN_TAGS['registry-view'], va)[0] and vec['registryViews']['project-b'] == L.domain_digest(L.DOMAIN_TAGS['registry-view'], vb)[0])
    # SEC-S2: the closed policy schema carries no confinement-required member
    pol = L.load_schema('permission-policy')

    def prop_names(sch, acc):
        if isinstance(sch, dict):
            for k, v in sch.get('properties', {}).items():
                acc.add(k); prop_names(v, acc)
            for k in ('items', 'additionalProperties'):
                if isinstance(sch.get(k), dict):
                    prop_names(sch[k], acc)
            for alt in sch.get('oneOf', []):
                prop_names(alt, acc)
        return acc
    names = prop_names(pol, set())
    rec('policy-schema-has-no-confinement-member', not any('confine' in n.lower() or 'sandbox' in n.lower() for n in names) and pol.get('additionalProperties') is False, sorted(names).__repr__()[:200])
    # registry custody: every entry names a catalog release with equal digests
    cat = objs['catalog']; regy = objs['registry']
    cat_pre = L.domain_digest(L.DOMAIN_TAGS['catalog'], cat)[0]
    for e in regy['entries']:
        if e['status'] not in ('active', 'deprecated-alias-window'):
            continue  # retired/revoked entries are custody history; the never-readmit ledger check covers them
        rel = [r for r in cat['releases'] if r['stableId'] == e['stableId'] and r['version'] == e['version']]
        rec('registry-custody:%s@%s' % (e['stableId'][:8], e['scope']), bool(rel) and rel[0]['manifestDigest'] == e['manifestDigest'] and rel[0]['envelopeDigest'] == e['signatureRef'] and e['catalogSnapshotVersion'] == cat['snapshotVersion'] and e['catalogPreimageSha256'] == cat_pre)

    # 3. manifest admission + registry
    stored = rb('security-fixtures.v4/typescript-analyzer.manifest.json')
    man = L.load_json_strict(stored)
    m = vec['manifest']
    rec('manifest.stored', L.sha256_hex(stored) == m['storedSha256'])
    pre, cb = L.domain_digest(L.DOMAIN_TAGS['manifest'], man)
    rec('manifest.preimage', pre == m['preimageSha256'] and len(cb) == m['canonicalLength'] and L.sha256_hex(cb) == m['canonicalSha256'])
    rec('manifest.canonicalFile', L.sha256_hex(rb('security-fixtures.v4/typescript-analyzer.manifest.canonical.bin')) == m['canonicalSha256'])
    rec('manifest.admission.positive', admit_manifest(man, m['registry']) is None, str(admit_manifest(man, m['registry'])))
    for neg, expect in (('typescript-analyzer.manifest.wrong-rung.json', 'relation/rung mismatch'), ('typescript-analyzer.manifest.unknown-capability.json', 'unknown capability')):
        r = admit_manifest(L.load_json_strict(rb('security-fixtures.v4/' + neg)), m['registry'])
        rec('manifest.admission.negative:' + neg, r is not None and expect in r, str(r))

    # 4. envelopes (section 2.2 order and precedence)
    for fn, expect in vec['envelopes'].items():
        env = rj('security-fixtures.v4/' + fn)
        kind_expected = 'manifest'
        target = stored
        if fn.startswith('root.'):
            kind_expected, target = 'root', (json.dumps(root_doc, indent=2) + '\n').encode()
        if fn.startswith('catalog.'):
            kind_expected, target = 'catalog', (json.dumps(objs['catalog'], indent=2) + '\n').encode()
        outcome, detail = L.verify_envelope(target, env, root, kind_expected, publisher_namespace=man['provenance']['publisher'] if kind_expected == 'manifest' else 'opensip')
        rec('envelope:' + fn, outcome == expect, '%s (%s)' % (outcome, detail))
    ok_env = rj('security-fixtures.v4/typescript-analyzer.envelope.json')
    kids = [s['keyId'] for s in ok_env['signatures']]
    rec('envelope.signature-order-and-threshold', kids == sorted(kids) and len(set(kids)) == len(kids) >= 2, str(kids))
    rec('envelope.signed-subject-binds-routing', json.dumps(L.signed_subject(ok_env), sort_keys=True).count('"') >= 12 and set(L.signed_subject(ok_env)) == {'kind', 'domain', 'storedSha256', 'preimageSha256', 'role', 'namespace'})

    # 4b. witness reconciliation model (section 5.4): every crash point and restore variant
    wc = rj('security-fixtures.v4/witness-reconciliation-cases.json')
    for c in wc['cases']:
        tail = tuple(c['journalTail']) if c['journalTail'] else None
        action, detail = L.reconcile_witness(tail, c['witness'], wc['projectKey'], wc['grantGeneration'])
        rec('witness:' + c['id'], action == c['expect'], '%s (%s)' % (action, detail))
    # simulated writer: crash after each protocol step, then reconcile
    def simulate(crash_after):
        H = lambda n: L.sha256_hex(('h%d' % n).encode())
        W = lambda seq, state: {'witnessSchema': 1, 'projectKeyDigest': L.project_key_digest('pk'), 'grantGeneration': 1, 'seq': seq, 'bodySha256': H(seq), 'state': state}
        journal = [(1, H(1)), (2, H(2))]; witness = W(2, 'COMMITTED')
        n_ = 3
        if crash_after >= 1: witness = W(n_, 'PENDING')          # step 2 durable
        if crash_after >= 2: journal.append((n_, H(n_)))         # step 3 commit durable
        if crash_after >= 3: witness = W(n_, 'COMMITTED')        # step 4 durable
        return L.reconcile_witness(journal[-1], witness, 'pk', 1)[0]
    rec('witness.simulated-crash-points', [simulate(k) for k in (0, 1, 2, 3)] == ['OK', 'REVERT', 'ADVANCE', 'OK'], str([simulate(k) for k in (0, 1, 2, 3)]))
    # 4c. D9 joins: every cited class and code exists in d9-exit-contract.v1.14 and every exit equals classToExitCode
    d9 = json.load(open(os.path.join(HERE, '..', 'artifacts', 'd9-exit-contract.v1.14.json'), encoding='utf-8'))
    joins = rj('security-fixtures.v4/d9-joins.example.json')
    rec('d9.source-pin', L.sha256_hex(open(os.path.join(HERE, '..', 'artifacts', 'd9-exit-contract.v1.14.json'), 'rb').read()) == joins['source']['sha256'])
    vocab = set(d9['codeVocabulary']['reasonCodes']) | set(d9['codeVocabulary']['errorCodes']); c2e = d9['classToExitCode']; goldens = {g['id'] for g in d9['goldenCases']}
    ok = True; bad = []
    for row in joins['doctor'] + [r for r in joins['permission'] if r['d9Class']] + [r for r in joins['componentResponseJoins'] if r['d9Class'] in c2e]:
        cls = row['d9Class']
        if cls not in c2e: ok = False; bad.append(('class', cls)); continue
        if 'exitCode' in row and row['exitCode'] is not None and row['exitCode'] != c2e[cls]: ok = False; bad.append(('exit', cls, row['exitCode']))
        for code in row.get('codes', []):
            if code not in vocab: ok = False; bad.append(('code', code))
        for g in (row.get('golden') or '').split(';'):
            g = g.strip().split(' (')[0]
            if g and g not in goldens: ok = False; bad.append(('golden', g))
    rec('d9.joins-within-closed-vocabulary', ok, str(bad)[:300])
    rec('d9.no-minted-codes', all(code in vocab for row in joins['doctor'] + joins['permission'] + joins['componentResponseJoins'] for code in row.get('codes', [])))
    rec('d9.state-class-matrix-5-total-3-active', joins['stateClassMatrix']['total'] == 5 and len(joins['stateClassMatrix']['rows']) == 5 and len(joins['stateClassMatrix']['activeInPreview']) == 3)

    # 5. grant journal example: schema, chain, binding, locator, guards
    gj = rj('security-fixtures.v4/grant-journal.example.json')
    prev = L.genesis_prev(gj['projectKey'], 1)
    rec('journal.genesis', prev == gj['genesisPrev'])
    chain_ok = True
    for r in gj['records']:
        body = r['body']
        try:
            L.validate(body, L.load_schema('journal-record'))
        except L.SchemaError as e:
            chain_ok = False; rec('journal.schema:%d' % r['seq'], False, str(e))
        if L.record_body_sha(body) != r['bodySha256'] or r['prevSha256'] != prev or body['seq'] != r['seq']:
            chain_ok = False
        prev = r['bodySha256']
    rec('journal.chain', chain_ok)
    rec('journal.witness', gj['witness']['seq'] == gj['records'][-1]['seq'] and gj['witness']['bodySha256'] == gj['records'][-1]['bodySha256'] and gj['witness']['state'] == 'COMMITTED')
    loc = L.locator(gj['projectKey'], 1, 1)
    rec('journal.locator.host-internal-digest-form', bool(L.LOCATOR_RE.match(loc)) and loc.split(':')[1] == L.project_key_digest(gj['projectKey']) and gj['projectKey'] not in loc and gj['witness']['projectKeyDigest'] == L.project_key_digest(gj['projectKey']))
    lb = rj('security-fixtures.v4/locator-bounds.json')
    rec('journal.locator.bounds', lb['min']['bytes'] == L.LOCATOR_MIN_BYTES == 71 and lb['max']['bytes'] == L.LOCATOR_MAX_BYTES == 104 and L.parse_locator(lb['min']['value']) is not None and L.parse_locator(lb['max']['value']) == (L.project_key_digest('k' * 1024), L.I64MAX, L.SEQ_MAX) and lb['max']['bytes'] <= 1024)
    rec('journal.locator.negatives', all(L.parse_locator(n) is None for n in lb['negatives']), str([n[:24] for n in lb['negatives'] if L.parse_locator(n) is not None]))
    # 5b. section 7.4/7.5 broker handles, dual-token verification, result courier (WA-1)
    bh = rj('security-fixtures.v4/broker-handles.example.json')
    for c in bh['cases']:
        if str(c['expect']).startswith('RF-2'):
            rec('broker.' + c['id'], len(c['body']['authorizationRef'].encode()) > 1024, 'RF-2 by the control schema bound; security never reached'); continue
        ctx = {'connectionMap': bh['connectionMaps'].get(c['connectionMap']) if c.get('connectionMap') else None, 'currentBinding': c.get('currentBinding'), 'journalState': bh['journalStates'].get(c['journalState']) if c.get('journalState') else None, 'snapshotMembers': set(c['snapshotMembers']) if c.get('snapshotMembers') is not None else (set(bh['snapshotMembersDefault']) if 'snapshotMembers' not in c else None)}
        got = L.verify_effect_request(c['body'], ctx)
        rec('broker.' + c['id'], got == c['expect'], str(got))
    rec('broker.one-handle-per-grant', len({e['underlyingLocator'] for e in bh['connectionMaps']['example'].values()}) == len(bh['connectionMaps']['example']) and len({e['operationRef'] for e in bh['connectionMaps']['example'].values()}) == 1)
    rec('broker.both-tokens-required', bh['underlyingTokenByEffectClass'] == {'HE-1': 'PT-FS-WRITE-HOST-STATE', 'HE-2': 'PT-FS-READ-PROJECT'} and any(c['expect'] == 'RF-6:AUTHORIZATION.TOKEN_MISMATCH' for c in bh['cases']))
    bd = bh['bootstrapDescriptorExample']
    dec = json.dumps(bd['decoded'], separators=(',', ':'), sort_keys=True).encode()
    rec('broker.bootstrap-descriptor-bounds', bd['encodedBytes'] <= 16384 and len(dec) <= 12288 and len(bd['decoded']['handles']) <= 4 and all(L.HANDLE_RE.match(h['authorizationRef']) and L.OPERATION_REF_RE.match(h['operationRef']) and h['effectClass'] in L.EFFECT_CLASSES for h in bd['decoded']['handles']) and bd['emptyDescriptor'] == {'bootstrapVersion': 1, 'handles': []})
    bsp = os.path.join(HERE, 'broker-bootstrap.schema.v1.json'); bs = json.load(open(bsp))
    try:
        L.validate(bd['decoded'], bs); L.validate(bd['emptyDescriptor'], bs); shape_ok = True
    except L.SchemaError as e:
        shape_ok = False
    rec('broker.descriptor-validates-against-frozen-bootstrap-schema', shape_ok and L.sha256_hex(open(bsp, 'rb').read()) == bh['bootstrapHandleEntry']['schemaPin']['sha256'] and set(bh['bootstrapHandleEntry']['shape']) == {'effectClass', 'operationRef', 'authorizationRef'})
    rec('broker.bootstrap-successor-recorded-not-implied', list(bh['bootstrapSuccessorRequired']['add']) == ['resultScratchRoot'] and bh['bootstrapSuccessorRequired']['add']['resultScratchRoot']['maxUtf8Bytes'] == 4096 and 'resultScratchRoot' not in json.dumps(bd['decoded']) and 'he1Receipt' in bh['resultCourier']['lifecycle'] and 'names NO file' in bh['resultCourier']['lifecycle']['he1Receipt'])
    for c in bh['resultCourier']['stageAdmissionCases']:
        got = L.stage_file_admission(c['st'], c['hostUid'], c['byteCap'])
        rec('broker.stage.' + c['id'], got == c['expect'], str(got))
    D = 'd' * 64; T = lambda mp, sd=D: {'snapshotDigest': sd, 'memberPath': mp}; S = lambda pp, sd=D: {'pathPrefixes': pp, 'snapshotDigest': sd}
    rec('broker.target-order-normalization-before-prefix', L._target_within_scope('HE-2', T('src/../private'), S(['src']), {'src/../private'})[1] == 'TARGET_PATH_NOT_NORMALIZED' and L._target_within_scope('HE-2', T('src/a.ts'), S(['src']), {'src/a.ts'})[0] and L._target_within_scope('HE-2', T('srcx/a.ts'), S(['src']), {'srcx/a.ts'})[1] == 'TARGET_OUTSIDE_SCOPE' and L._target_within_scope('HE-2', T('src/a.ts', 'e' * 64), S(['src']), {'src/a.ts'})[1] == 'SNAPSHOT_BINDING_MISSING_OR_MISMATCH' and L._target_within_scope('HE-2', T('src/a.ts'), S(['src']), {'src/b.ts'})[1] == 'TARGET_NOT_SEALED_MEMBER' and L._target_within_scope('HE-2', T('src/a.ts'), {'pathPrefixes': ['src']}, {'src/a.ts'})[1] == 'SNAPSHOT_BINDING_MISSING_OR_MISMATCH')
    rec('broker.wire-refs-within-1024', all(len(x.encode()) <= 1024 for h in bd['decoded']['handles'] for x in (h['authorizationRef'], h['operationRef'])) and all(len(c['resultRef'].encode()) <= 1024 for c in bh['resultCourier']['cases']))
    for c in bh['resultCourier']['cases']:
        outcome, data = L.resolve_result(c['resultRef'], lambda rid, sc=c['scratch']: sc[rid].encode() if rid in sc else None, c['ctx'])
        rec('broker.result.' + c['id'], outcome == c['expect'] and (data is None or outcome == 'OK'), outcome)
    lc = bh['resultCourier']['lifecycle']
    rec('broker.M5-he1-order', bh['resultCourier']['he1Order'] == {'REVERSIBLE': ['RA', 'RCI', 'EFFECT', 'RCO', 'UNLINK-STAGE', 'RESULT'], 'IRREVERSIBLE': ['RA', 'ICI', 'EFFECT', 'ICO', 'UNLINK-STAGE', 'RESULT']} and 'ORDER (SEC3-M5)' in bh['resultCourier']['lifecycle']['he1Stage'] and bh['resultCourier']['lifecycle']['he1Stage'].index('durable RA') < bh['resultCourier']['lifecycle']['he1Stage'].index('commit FROM THE BUFFER') < bh['resultCourier']['lifecycle']['he1Stage'].index('unlink the stage file'))
    for c in bh['resultCourier']['he1RecoveryCases']:
        got = L.he1_recover(c['commitClass'], c['durableRecords'], c['footprint']); gotl = [list(got[0]) if got[0] else None, got[1]]
        rec('broker.M5-recover.%s.%s.%s' % (c['commitClass'], '+'.join(c['durableRecords']) or 'none', c['footprint']), gotl == c['expect'] and (c['footprint'] != 'unknown' or c['commitClass'] != 'IRREVERSIBLE' or 'ICI' not in c['durableRecords'] or got[1] == 'INDETERMINATE'), str(gotl))
    caps = bh['resultCourier']['caps']
    rec('broker.caps-stated-per-lead-decision', caps['he2RetainedResultsPerSpawnBytes'] == 67108864 and caps['he1HandlesMax'] == 4 and caps['he1StagePerHandleBytes'] == 16777216 and caps['scratchConservativeMaxBytes'] == 134217728 and 'no combined 64 MiB claim' in caps['rule'] and 'D-006' in caps['d006Rationale'])
    rec('broker.lifecycle-defined', all(k in lc for k in ('scratchRoot', 'he2Publish', 'he1Stage', 'cleanup')) and 'O_NOFOLLOW' in lc['he1Stage'] and 'FROM THE BUFFER' in lc['he1Stage'] and 'publish before result' in lc['he2Publish'] and 'single-use' in lc['he1Stage'])
    # 5c. durability primitives and I/O failure matrix (WA-9); doctor report-only evaluation (WA-5); launch classes (WA-6); runners (WA-7)
    du = rj('security-fixtures.v4/durability-io-failures.json')
    rec('durability.matrix-complete', len(du['matrix']) == len(L.DURABILITY_BOUNDARIES) * len(L.IO_FAILURE_CLASSES) and all(m['d9'] == {'class': 'operational-failed', 'exit': 4, 'code': 'HOST.IO_FAILURE'} for m in du['matrix']) and 'F_FULLFSYNC' in du['primitives']['macos']['file'] and 'fullfsync' in du['primitives']['macos']['sqlite'])
    rec('durability.post-visibility-undetermined', all((m['partialState'].startswith('none')) == (m['errorClass'] in L.PRE_VISIBILITY) for m in du['matrix']) and all(m['partialState'].startswith('UNDETERMINED') and m['reconcile'] for m in du['matrix'] if m['errorClass'] in ('FSYNC_FAILED', 'COMMIT_FAILED')) and len(du['postVisibilityCases']) == 3)
    dr = rj('security-fixtures.v4/doctor-trust-report.example.json')
    reps = [k for k in dr if isinstance(dr[k], dict) and 'writes' in dr[k]]
    rec('doctor.report-only-no-writes', len(reps) == 6 and all(dr[k]['writes'] == [] and dr[k]['evaluationMode'] == 'report-only' and 'rawWallClock' in dr[k] and 'evaluationTime' in dr[k] for k in reps) and any(f['status'] == 'CLOCK-REGRESSION' for f in dr['clockRegression']['findings']) and any(f['status'] == 'EXPIRED' and f['wouldRefuse'] for f in dr['expired']['findings']) and not any(f['wouldRefuse'] for f in dr['normal']['findings']))
    st = lambda r, c: [f['status'] for f in r['findings'] if f['check'] == c][0]
    rec('doctor.expiry-and-freshness-boundaries', st(dr['edgeExactly90dFreshCatalogExpired'], 'revocationFreshUntil') == 'FRESH' and st(dr['edgeExactly90dFreshCatalogExpired'], 'catalogExpiresAt') == 'EXPIRED' and st(dr['edge90dPlusOneSecondStale'], 'revocationFreshUntil') == 'STALE-REVOCATION' and dr['highWaterDominatesWallClock']['evaluationTime'] == '2027-03-21T10:00:01Z' and dr['highWaterDominatesWallClock']['rawWallClock'] == '2026-12-22T09:00:00Z' and st(dr['highWaterDominatesWallClock'], 'revocationFreshUntil') == 'STALE-REVOCATION')
    # 5e. effective permission policy: the lock digest identifies both source files and the merge
    pe = rj('security-fixtures.v4/permission-policy.effective.example.json')
    eff, refs = L.merge_policy(pe['global'], pe['project'])
    rec('policy.effective-reproducible', eff == pe['effective'] and refs == [] and L.effective_policy_digest(eff) == pe['permissionPolicyDigest'] and eff['sources']['global'] == L.domain_digest(L.DOMAIN_TAGS['policy'], pe['global'])[0] and eff['sources']['project'] == L.domain_digest(L.DOMAIN_TAGS['policy'], pe['project'])[0] and pe['digestDomain'] == 'opensip.metadata.policy-effective.1' and L.effective_policy_digest(eff) != L.domain_digest(L.DOMAIN_TAGS['policy'], eff)[0])
    g2 = json.loads(json.dumps(pe['global'])); g2['grants'][0]['scope']['pathPrefixes'].append('docs')
    rec('policy.digest-changes-with-either-file', L.effective_policy_digest(L.merge_policy(g2, pe['project'])[0]) != pe['permissionPolicyDigest'] and L.effective_policy_digest(L.merge_policy(pe['global'], None)[0]) == pe['globalOnly']['permissionPolicyDigest'] != pe['permissionPolicyDigest'])
    for nm, doc in (('effective', pe['effective']), ('globalOnly', pe['globalOnly']['effective']), ('missing', pe['missingProjectPolicyDenyByAbsence']['effective'])):
        try:
            L.validate(doc, L.load_schema('permission-policy-effective')); L.validate(pe['global'], L.load_schema('permission-policy')); L.validate(pe['project'], L.load_schema('permission-policy')); ok = True
        except L.SchemaError as e:
            ok = False
        rec('policy.schema:' + nm, ok)
    mp = pe['missingProjectPolicyDenyByAbsence']
    rec('policy.deny-by-absence', mp['effective']['grants'] == [] and mp['effective']['sources']['project'] == L.domain_digest(L.DOMAIN_TAGS['policy'], L.EMPTY_PROJECT_POLICY)[0] and mp['permissionPolicyDigest'] != pe['globalOnly']['permissionPolicyDigest'] and L.effective_policy_for_operation(pe['global'], None, True)[0] == mp['effective'] and pe['globalOnly']['effective']['sources']['project'] is None and len(pe['globalOnly']['effective']['grants']) == 2)
    rec('policy.project-only-narrows', pe['negatives']['project-widens-path']['refusals'] == ['POLICY.PROJECT_WIDENS_SCOPE:PT-FS-READ-PROJECT:pathPrefixes'] and pe['negatives']['project-grants-token-global-denies']['effectiveGrants'] == [] and pe['negatives']['project-deny-wins']['effectiveGrants'] == [] and all(g['token'] != 'PT-NET-EGRESS' for g in pe['effective']['grants']))
    ng = pe['negatives']
    rec('policy.M2-traversal-refused-at-source', ng['M2-project-traversal-src-dotdot-private']['refusals'] == ['POLICY.PATH_PREFIX_NOT_NORMALIZED:PT-FS-READ-PROJECT:src/../private'] and ng['M2-project-traversal-outside']['refusals'] == ['POLICY.PATH_PREFIX_NOT_NORMALIZED:PT-FS-READ-PROJECT:src/../../outside'] and ng['M2-global-traversal-refused-at-source']['refusals'] == ['POLICY.PATH_PREFIX_NOT_NORMALIZED:PT-FS-READ-PROJECT:src/./x'] and ng['M2-control-legal-descendant']['refusals'] == [] and ng['M2-control-legal-descendant']['effectiveGrants'][0]['scope']['pathPrefixes'] == ['src/a'] and ng['M2-control-prefix-sibling-srcx-refused']['refusals'] == ['POLICY.PROJECT_WIDENS_SCOPE:PT-FS-READ-PROJECT:pathPrefixes'])
    rec('policy.N1-duplicate-pairs', ng['N1-duplicate-grant-pair-same-scope']['refusals'] == ['POLICY.DUPLICATE_GRANT_PAIR'] and ng['N1-duplicate-grant-pair-conflicting-scope']['refusals'] == ['POLICY.DUPLICATE_GRANT_PAIR'] and ng['N1-duplicate-deny-pair']['refusals'] == ['POLICY.DUPLICATE_DENY_PAIR'] and ng['N1-grant-and-deny-same-pair-deny-wins']['refusals'] == [] and all(g['token'] != 'PT-FS-READ-PROJECT' for g in ng['N1-grant-and-deny-same-pair-deny-wins']['effectiveGrants']))
    rec('policy.effective-schema-shape', all(k in pe['effective'] for k in ('policySchema', 'policyScope', 'sources', 'grants', 'denies', 'consents')) and pe['effective']['policyScope'] == 'effective')
    lv = rj('security-fixtures.v4/launch-verification-classes.json')
    meta = [c for c in lv['classes'] if c['commandClass'] == 'metadata-only'][0]
    rec('launch.metadata-only-verifies-nothing', meta['trustEvaluation'] is False and meta['durableWrites'] is False and meta['tcbPredicate'] is False and 'trust.sqlite' in meta['mustNotOpen'] and 'any helper process' in meta['mustNotOpen'] and [c for c in lv['classes'] if c['commandClass'] == 'doctor'][0]['durableWrites'] is False)
    qr = rj('security-fixtures.v4/qualification-runners.json')
    d102 = os.path.join(HERE, '..', 'artifacts', 'coordinator-decisions.D-102.turn2.draft.md')
    rec('runners.d102-pin', L.sha256_hex(open(d102, 'rb').read()) == qr['source']['sha256'])
    d102txt = open(d102, encoding='utf-8').read()
    rec('runners.classes-are-d102-classes', [c['class'] for c in qr['classes']] == ['macos-15', 'macos-15-intel', 'ubuntu-24.04', 'ubuntu-24.04-arm'] and all(('`%s`' % c['class']) in d102txt for c in qr['classes']) and sorted(qr['g13']['classes']) == sorted(c['class'] for c in qr['classes']) and '10%' in qr['g13']['rule'])
    rec('runners.templates-exist-and-name-their-class', all(os.path.exists(os.path.join(HERE, 'security-fixtures.v4', c['developmentTemplate'])) and rj('security-fixtures.v4/' + c['developmentTemplate'])['qualificationRunnerClass'] == c['class'] for c in qr['classes']))
    # 5d. G22 observed-event admission probes and the G07 loader/TOCTOU crosswalk
    ge = rj('security-fixtures.v4/g22-observed-events.json')
    profs = {fn: rj('security-fixtures.v4/' + fn) for fn in ('profile.P-MACOS-ARM64-25G83-APFS.json', 'profile.P-MACOS-X86_64-25G83-APFS.json', 'profile.P-LINUX-X86_64-UBUNTU2404-EXT4.json', 'profile.P-LINUX-ARM64-UBUNTU2404-EXT4.json')}
    byk = {p['platformProfileKey']: p for p in profs.values()}
    for c in ge['cases']:
        got = L.admit_observed_events(byk[c['profile']], c['observed'])
        rec('g22.' + c['id'], got == c['expect'], str(got))
    legacy = ['G22.macos-arm64.hostile-loader-system-library-tool', 'G22.macos-x86_64.hostile-loader-system-library-tool', 'G22.linux-x86_64.hostile-loader-system-library-tool', 'G22.linux-arm64.hostile-loader-system-library-tool']
    rec('g22.legacy-four-states-covered', all(l in ge['legacyStateIdsCovered'] for l in legacy))
    rec('g07.loader-seven-and-toctou-five-crosswalked', sorted(ge['g07LoaderCrosswalk']) == sorted('G07.loader.' + x for x in ('path-substitution', 'loader-replacement', 'shell-substitution', 'live-project-substitution', 'system-runtime-substitution', 'install-time-substitution', 'entrypoint-replacement')) and sorted(ge['g07ToctouCrosswalk']) == sorted('G07.toctou.' + x for x in ('extract', 'canonicalize', 'verify-to-spawn', 'concurrent-update-remove', 'directory-inode-swap')))
    rec('g22.refusal-vocabulary-closed', all(x in L.NT_TCB for c in ge['cases'] for x in c['expect']) and ge['standing'].startswith('SYNTHETIC'))
    # column/body binding on the stored example database
    rb('security-fixtures.v4/grant-journal.example.sqlite')
    con = sqlite3.connect(os.path.join(FX, 'grant-journal.example.sqlite'))
    rows = con.execute('SELECT grantGeneration, seq, record_type, operation_ref, token, install_generation_id, manifest_digest, platform, body, body_sha256, prev_sha256 FROM grant_journal ORDER BY seq').fetchall()
    con.close()
    bind_ok = len(rows) == len(gj['records'])
    for row, r in zip(rows, gj['records']):
        b = json.loads(row[8])
        bind_ok &= (row[2] == b['recordType'] and row[3] == b['operationRef'] and row[9] == r['bodySha256'] and row[10] == r['prevSha256'] and (row[4] or None) == b.get('token') and (row[6] or None) == b.get('manifestDigest') and L.canonical_bytes(b) == row[8].encode())
    rec('journal.column-body-binding', bind_ok)
    # re-exercise the guards on a fresh database from the retained DDL
    with tempfile.TemporaryDirectory() as td:
        c2 = sqlite3.connect(os.path.join(td, 'g.sqlite'))
        c2.executescript(open(os.path.join(SCH, 'grant-journal.sql')).read())
        op = gj['records'][0]['body']['operationRef']
        def ins(gen, seq, t='RA'):
            c2.execute('INSERT INTO grant_journal VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (gen, seq, t, op, 'req', None if t == 'RA' else 'PT-FS-READ-PROJECT', None if t == 'RA' else 'gen-1', None if t == 'RA' else '0' * 64, None if t == 'RA' else 'linux-x86_64', '{}', '0' * 64, '1' * 64)); c2.commit()
        def refuses(fn):
            try:
                fn(); c2.commit(); return False
            except sqlite3.DatabaseError:
                c2.rollback(); return True
        ins(1, 1, 'GRANT')
        rec('journal.guard.seq-gap', refuses(lambda: ins(1, 3)))
        rec('journal.guard.grant-binding-required', refuses(lambda: c2.execute("INSERT INTO grant_journal VALUES (1,2,'GRANT',?,NULL,'PT-FS-READ-PROJECT',NULL,NULL,NULL,'{}',?,?)", (op, '0' * 64, '1' * 64))))
        ins(1, 2)
        rec('journal.guard.update', refuses(lambda: c2.execute("UPDATE grant_journal SET token='PT-NET-EGRESS' WHERE seq=1")))
        rec('journal.guard.delete', refuses(lambda: c2.execute('DELETE FROM grant_journal WHERE seq=2')))
        c2.execute('INSERT INTO grant_journal VALUES (1,3,\'TERMINAL\',?,NULL,NULL,NULL,NULL,NULL,\'{}\',?,?)', (op, '0' * 64, '1' * 64)); c2.commit()
        rec('journal.guard.append-after-terminal', refuses(lambda: ins(1, 4)))
        rec('journal.guard.new-generation-restarts', not refuses(lambda: ins(2, 1, 'GRANT')))
        rec('journal.guard.seq-above-uint53', refuses(lambda: c2.execute("INSERT INTO grant_journal VALUES (3,9007199254740992,'GRANT',?,NULL,'PT-FS-READ-PROJECT','gen-1',?,'linux-x86_64','{}',?,?)", (op, '0' * 64, '0' * 64, '1' * 64))))
        ddl = open(os.path.join(SCH, 'grant-journal.sql')).read()
        rec('journal.ddl.reserved-terminal-slot', 'NEW.seq = 9007199254740991 AND NEW.record_type <> \'TERMINAL\'' in ddl and 'seq <= 9007199254740991' in ddl)
        c2.close()
    rec('journal.generator-guards-recorded', all(v.startswith('refused') for v in gj['guards'].values()), json.dumps(gj['guards']))

    # 5f. SEC3-M6: Linux OS-ABI predicate over the measured series/flavor; illustrative examples validate but admit nothing
    m6 = rj('security-fixtures.v4/linux-os-abi-predicate-cases.json')
    for c in m6['cases']:
        got = L.linux_os_abi_predicate(c['payload'], c['observed'])
        rec('m6.' + c['id'], got[0] == c['expect'], str(got)[:120])
    for fn in ('profile.example.linux-x86_64.azure-6.17.json', 'profile.example.linux-x86_64.generic-6.8.json'):
        ex = rj('security-fixtures.v4/' + fn)
        try:
            L.validate(ex, L.load_schema('tcb-profile-template')); ok = True
        except L.SchemaError:
            ok = False
        pay = ex['signedEntries'][0]['identityEvidence']['value']['authenticityCore']['payload']
        rec('m6.illustrative:' + fn, ok and ex['illustrativeExample']['standing'].startswith('ILLUSTRATIVE') and isinstance(pay['kernelSeries'], str) and pay['kernelSeries'].endswith('-' + pay['kernelFlavor']))
    for fn in ('profile.P-LINUX-X86_64-UBUNTU2404-EXT4.json', 'profile.P-LINUX-ARM64-UBUNTU2404-EXT4.json'):
        pay = rj('security-fixtures.v4/' + fn)['signedEntries'][0]['identityEvidence']['value']['authenticityCore']['payload']
        rec('m6.release-template-series-measured:' + fn, all(isinstance(pay[k], dict) and '$releaseMeasured' in pay[k] for k in ('kernelFlavor', 'kernelSeries', 'kernelPackageNamePattern')) and '6.8' not in json.dumps(pay))
    # 6. profile templates
    tsch = L.load_schema('tcb-profile-template')
    for fn in ('profile.P-MACOS-ARM64-25G83-APFS.json', 'profile.P-MACOS-X86_64-25G83-APFS.json', 'profile.P-LINUX-X86_64-UBUNTU2404-EXT4.json', 'profile.P-LINUX-ARM64-UBUNTU2404-EXT4.json'):
        prof = rj('security-fixtures.v4/' + fn)
        try:
            L.validate(prof, tsch)
            classes = [e['class'] for e in prof['signedEntries']] + [p['class'] for p in prof['inapplicabilityProofs']]
            covered = set(classes) >= {'OS ABI', 'loader', 'libc', 'framework', 'certificate store', 'font', 'ICU'}
            osabi = [e for e in prof['signedEntries'] if e['class'] == 'OS ABI']
            pathless = all(e['originSearchPolicy']['volumeConstraint']['tag'] == 'PATHLESS-PLATFORM-ATTESTED' for e in osabi)
            nonos = all(e['originSearchPolicy']['volumeConstraint']['tag'] != 'PATHLESS-PLATFORM-ATTESTED' for e in prof['signedEntries'] if e['class'] != 'OS ABI')
            scheme_ok = (prof['osFamily'] == 'macos') == (prof['supportedVersionOrBuildSelector']['identifierScheme'] == 'macos-product-build')
            rm_count = json.dumps(prof).count('$releaseMeasured')
            no_kexec = 'kexec-absent' not in json.dumps(prof['signedEntries']) and 'KB-1' not in json.dumps(prof['signedEntries']) and 'builderAttestation' not in json.dumps(prof['signedEntries'])
            launch = prof['acquisition']['launch']
            unpriv = all(a['privilege'] == 'unprivileged' and a['launchClosureMember'] is False for a in launch)
            ltxt = json.dumps(launch)
            no_priv_launch = 'setns(' not in ltxt and 'binary_bios_measurements' not in ltxt and 'bputil' not in ltxt and 'system_profiler' not in ltxt and 'SecCodeCopyGuestWithAttributes' not in ltxt and '/boot/vmlinuz' not in ltxt
            standing = prof['measurementStanding'] == 'DEVELOPMENT-MEASUREMENT' and prof['qualificationRunnerClass'] in ('macos-15', 'macos-15-intel', 'ubuntu-24.04', 'ubuntu-24.04-arm')
            rec('profile:' + fn, covered and pathless and nonos and scheme_ok and len(osabi) == 1 and no_kexec and unpriv and no_priv_launch and standing, 'every taxonomy class covered=%s; OS ABI pathless-only=%s; releaseMeasured placeholders=%d; v49 entries=%d; no kexec-absent/KB-1 residue=%s; launch unprivileged=%s; no privileged/slow interface at launch=%s; development-measurement standing on a D-102 class=%s' % (covered, pathless and nonos, rm_count, sum(1 for e in prof['signedEntries'] if e.get('schemeStanding') == 'v49-successor-required'), no_kexec, unpriv, no_priv_launch, standing))
        except L.SchemaError as e:
            rec('profile:' + fn, False, str(e))

    failures = [r for r in results if r['result'] == 'FAIL']
    report = {'checker': 'check-security-unit.v4.py', 'checkerSha256': L.sha256_hex(open(os.path.abspath(__file__), 'rb').read()), 'ranAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'environment': {'python': sys.version.split()[0], 'unicodedata': unicodedata.unidata_version, 'productionUnicodeTable': '15.1 (distribution-runtime-completion section 4); the reference environment table differs and is disclosed here',
                              'sqlite': sqlite3.sqlite_version, 'openssl': subprocess.run(['openssl', 'version'], capture_output=True, text=True).stdout.strip(), 'platform': platform.platform()},
              'inputs': inputs, 'results': results, 'summary': {'checks': len(results), 'failures': len(failures)}, 'qualifies': 'NOTHING'}
    if report_path:
        open(report_path, 'w', encoding='utf-8').write(json.dumps(report, indent=1, ensure_ascii=False) + '\n')
    for r in failures:
        print('FAIL', r['check'], r['detail'])
    print('%s: %d checks, %d failures%s' % ('PASS' if not failures else 'FAIL', len(results), len(failures), (' (report %s)' % report_path) if report_path else ''))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
