#!/usr/bin/env python3
"""Retained checker for the security completion unit v2 (design evidence only).

Usage: check-security-unit.v2.py [--report PATH]

Verifies, from security-completion.v2.md's stated rules: the canonical-profile vectors; every
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
import security_unit_lib_v2 as L  # noqa: E402

FX = os.path.join(HERE, 'security-fixtures.v2')
SCH = os.path.join(HERE, 'security-schemas.v2')
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
    vec = rj('security-vectors.v2.json')
    for s in ('envelope', 'root', 'revocation', 'catalog', 'registry', 'registry-view', 'payload', 'journal-record', 'permission-policy', 'tcb-profile-template'):
        rb('security-schemas.v2/%s.schema.json' % s)
    rb('security-schemas.v2/grant-journal.sql')
    rb('security_unit_lib_v2.py')

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
        obj = rj('security-fixtures.v2/' + fn); objs[sch] = obj
        try:
            L.validate(obj, L.load_schema(sch)); rec('schema:' + sch, True)
        except L.SchemaError as e:
            rec('schema:' + sch, False, str(e))
    root = objs['root']
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
        view = rj('security-fixtures.v2/' + vf)
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
    va = rj('security-fixtures.v2/registry-view.project-a.example.json'); vb = rj('security-fixtures.v2/registry-view.project-b.example.json')
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
    stored = rb('security-fixtures.v2/typescript-analyzer.manifest.json')
    man = L.load_json_strict(stored)
    m = vec['manifest']
    rec('manifest.stored', L.sha256_hex(stored) == m['storedSha256'])
    pre, cb = L.domain_digest(L.DOMAIN_TAGS['manifest'], man)
    rec('manifest.preimage', pre == m['preimageSha256'] and len(cb) == m['canonicalLength'] and L.sha256_hex(cb) == m['canonicalSha256'])
    rec('manifest.canonicalFile', L.sha256_hex(rb('security-fixtures.v2/typescript-analyzer.manifest.canonical.bin')) == m['canonicalSha256'])
    rec('manifest.admission.positive', admit_manifest(man, m['registry']) is None, str(admit_manifest(man, m['registry'])))
    for neg, expect in (('typescript-analyzer.manifest.wrong-rung.json', 'relation/rung mismatch'), ('typescript-analyzer.manifest.unknown-capability.json', 'unknown capability')):
        r = admit_manifest(L.load_json_strict(rb('security-fixtures.v2/' + neg)), m['registry'])
        rec('manifest.admission.negative:' + neg, r is not None and expect in r, str(r))

    # 4. envelopes (section 2.2 order and precedence)
    for fn, expect in vec['envelopes'].items():
        env = rj('security-fixtures.v2/' + fn)
        kind_expected = 'manifest'
        target = stored
        if fn.startswith('root.'):
            kind_expected, target = 'root', (json.dumps(objs['root'], indent=2) + '\n').encode()
        if fn.startswith('catalog.'):
            kind_expected, target = 'catalog', (json.dumps(objs['catalog'], indent=2) + '\n').encode()
        outcome, detail = L.verify_envelope(target, env, root, kind_expected, publisher_namespace=man['provenance']['publisher'] if kind_expected == 'manifest' else 'opensip')
        rec('envelope:' + fn, outcome == expect, '%s (%s)' % (outcome, detail))
    ok_env = rj('security-fixtures.v2/typescript-analyzer.envelope.json')
    kids = [s['keyId'] for s in ok_env['signatures']]
    rec('envelope.signature-order-and-threshold', kids == sorted(kids) and len(set(kids)) == len(kids) >= 2, str(kids))
    rec('envelope.signed-subject-binds-routing', json.dumps(L.signed_subject(ok_env), sort_keys=True).count('"') >= 12 and set(L.signed_subject(ok_env)) == {'kind', 'domain', 'storedSha256', 'preimageSha256', 'role', 'namespace'})

    # 5. grant journal example: schema, chain, binding, locator, guards
    gj = rj('security-fixtures.v2/grant-journal.example.json')
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
    rec('journal.locator', loc.startswith('gj:') and loc.count(':') == 3 and ':' not in loc.split(':')[1])
    # column/body binding on the stored example database
    rb('security-fixtures.v2/grant-journal.example.sqlite')
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

    # 6. profile templates
    tsch = L.load_schema('tcb-profile-template')
    for fn in ('profile.P-MACOS-ARM64-25G83-APFS.json', 'profile.P-MACOS-X86_64-25G83-APFS.json', 'profile.P-LINUX-X86_64-UBUNTU2404-EXT4.json', 'profile.P-LINUX-ARM64-UBUNTU2404-EXT4.json'):
        prof = rj('security-fixtures.v2/' + fn)
        try:
            L.validate(prof, tsch)
            classes = [e['class'] for e in prof['signedEntries']] + [p['class'] for p in prof['inapplicabilityProofs']]
            covered = set(classes) >= {'OS ABI', 'loader', 'libc', 'framework', 'certificate store', 'font', 'ICU'}
            osabi = [e for e in prof['signedEntries'] if e['class'] == 'OS ABI']
            pathless = all(e['originSearchPolicy']['volumeConstraint']['tag'] == 'PATHLESS-PLATFORM-ATTESTED' for e in osabi)
            nonos = all(e['originSearchPolicy']['volumeConstraint']['tag'] != 'PATHLESS-PLATFORM-ATTESTED' for e in prof['signedEntries'] if e['class'] != 'OS ABI')
            scheme_ok = (prof['osFamily'] == 'macos') == (prof['supportedVersionOrBuildSelector']['identifierScheme'] == 'macos-product-build')
            rm_count = json.dumps(prof).count('$releaseMeasured')
            rec('profile:' + fn, covered and pathless and nonos and scheme_ok and len(osabi) == 1, 'every taxonomy class covered=%s; OS ABI pathless-only=%s; releaseMeasured placeholders=%d; v49 entries=%d' % (covered, pathless and nonos, rm_count, sum(1 for e in prof['signedEntries'] if e.get('schemeStanding') == 'v49-successor-required')))
        except L.SchemaError as e:
            rec('profile:' + fn, False, str(e))

    failures = [r for r in results if r['result'] == 'FAIL']
    report = {'checker': 'check-security-unit.v2.py', 'checkerSha256': L.sha256_hex(open(os.path.abspath(__file__), 'rb').read()), 'ranAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
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
