"""P05 — corrected successor rehearsal, diagnosis-driven (NOT a duplicate of the interrupted v1 p04).

Diagnosis carried in: p04 applied the v1 patch; its foundation suite FAILED check-identity
v20-native-view-fixture-declares-current-registered-schemas (native-cases fixture still declares the old digest of
native-evidence.schemas.v2.json), and the run was stopped during the evaluator3 launcher. s04 then found that all 13 package13
retained Runs commit that schema document's digest. So:

  VARIANT A (consequence measurement, read-only): replay the 13 package13 Runs through open_run_closure and close_run using the
            owners in the v1 kit, which carries the v1 patch INCLUDING the native schema text edit.
  VARIANT B (recommended successor, fresh disposable kit in this runtime): the v1 patch WITHOUT the
            native-evidence.schemas.v2.json edit, plus a native section 10 disclosure that the schema annotation's older
            parenthetical is incomplete and section 10 governs; exact v1 bytes for every other file (proved by per-file diff
            equality with the v1 patch); fixed-point pin re-seal; generated reports regenerated then re-sealed; all affected suites;
            both planning checks; package13 through both boundaries; S1/S2/S3 re-measured; v2 patch written here.
No frozen, live, v1-kit or other-evidence byte is written."""
import base64, difflib, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, time

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
V1 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
V1KIT = os.path.join(V1, 'disposable/kit36-successor')
BASE = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit36-successor2')
PATCHDIR = os.path.join(BASE, 'successor-patch')
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v13'
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v36.json'
man = {f['path']: f['sha256'] for f in json.load(open(MAN))['files']}
DC = 'docs/coop/design-corrections'
NS = DC + '/native/native-evidence.schemas.v2.json'
NAT = 'docs/v2/contracts/product-v1/native-evidence.md'
R = {'standing': 'disposable corrected rehearsal of a proposed successor; not source, not acceptance'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def udiff_one(rel, root):
    a = open(os.path.join(S36, rel), encoding='utf-8').read().splitlines(keepends=True)
    b = open(os.path.join(root, rel), encoding='utf-8').read().splitlines(keepends=True)
    return ''.join(difflib.unified_diff(a, b, 'a/' + rel, 'b/' + rel, n=3))


v1patch_path = os.path.join(V1, 'successor-patch/successor-v23-gaps.patch')
v1patch = open(v1patch_path, encoding='utf-8').read()
PATCHED = sorted(set(re.findall(r'^\+\+\+ b/(\S+)', v1patch, re.M)))
R['v1Patch'] = {'sha256': sha(v1patch_path), 'files': PATCHED}
R['v1KitReproducesV1Patch'] = ''.join(udiff_one(rel, V1KIT) for rel in PATCHED) == v1patch
assert R['v1KitReproducesV1Patch']
v1kit_before = {rel: sha(os.path.join(V1KIT, rel)) for rel in PATCHED}


def nodup(pairs):
    d = {}
    for k, v in pairs:
        assert k not in d
        d[k] = v
    return d


def package_replay(owner_root, modname):
    spec = importlib.util.spec_from_file_location(modname, os.path.join(owner_root, DC, 'foundation/identity-model.v3.py'))
    M = importlib.util.module_from_spec(spec); sys.modules[modname] = M; spec.loader.exec_module(M)
    rows = []
    for g, klass in (('checkpoint3', 'positive'), ('normalized-examples6', 'positive'), ('rust-selection-examples1', 'positive'),
                     ('semantic-controls1', 'false-result-control'), ('binding-controls', 'binding-control')):
        for c in json.load(open(os.path.join(PKG, g, 'claims.json'))):
            raw = open(os.path.join(PKG, g, c['path']), 'rb').read()
            e = json.loads(raw, object_pairs_hook=nodup)
            blobs = {}
            for dg, v in e['blobs'].items():
                b = base64.b64decode(v, validate=True); assert hashlib.sha256(b).hexdigest() == dg; blobs[dg] = b
            objects = {}
            for dg, meta in e['frames'].items():
                dom, ident = meta['domain'], meta['identity']
                desc = e['objectTable'][ident] if ident in e['objectTable'] else json.loads(bytes.fromhex(meta['canonicalBytesHex']), object_pairs_hook=nodup)
                if dom != 'canonical-record' and dom in M.PREFIX and ident in e['objectTable']:
                    objects[ident] = (dom, desc)
            run = objects[c['runId']][1]
            row = {'group': g, 'class': klass, 'name': c['name']}
            for label, fn in (('structural', lambda: M.open_run_closure(run, objects, blobs)[0]), ('semantic', lambda: M.close_run(run, objects, blobs))):
                try:
                    rid = fn(); row[label] = 'ADMIT' if rid == c['runId'] else 'ADMIT-ID-MISMATCH'
                except Exception as exc:  # noqa: BLE001
                    row[label] = 'REFUSE'; row[label + 'Reason'] = '%s: %s' % (type(exc).__name__, str(exc)[:200])
            rows.append(row)
    same = (all(r['structural'] == r['semantic'] == 'ADMIT' for r in rows if r['class'] == 'positive')
            and all(r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE' and 'EVALUATOR_COMPLETE_PROOF_REPLAY' in r.get('semanticReason', '') for r in rows if r['class'] == 'false-result-control')
            and all(r['structural'] == 'ADMIT' and ((r['semantic'] == 'REFUSE' and 'ENUMERATION_BINDING_PROGRAM_ENTRY' in r.get('semanticReason', '')) if r['name'] == 'ts-invalid-default-entry' else r['semantic'] == 'ADMIT')
                    for r in rows if r['class'] == 'binding-control'))
    return rows, same


# ------------------------------------------------------------------ VARIANT A (read-only against the v1 kit)
rowsA, sameA = package_replay(V1KIT, 'owner_v1kit_variantA')
R['variantA'] = {'owners': 'v1 kit (v1 patch including the native schema text edit)', 'nativeSchemaDigestInKit': sha(os.path.join(V1KIT, NS)),
                 'frozen36NativeSchemaDigest': man[NS], 'package13Rows': rowsA, 'sameOutcomesAsFrozen36': sameA,
                 'refusals': sorted({r.get('structuralReason', r.get('semanticReason', ''))[:120] for r in rowsA if 'REFUSE' in (r['structural'], r['semantic']) and r['class'] == 'positive'})}
R['v1KitUntouchedByVariantA'] = all(sha(os.path.join(V1KIT, rel)) == h for rel, h in v1kit_before.items())
print('VARIANT A (v1 patch incl. schema edit): package13 same outcomes as frozen36:', sameA, '| positive refusals:', R['variantA']['refusals'][:3], flush=True)

# ------------------------------------------------------------------ VARIANT B kit
K = lambda rel: os.path.join(KIT, rel)
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/') or (rel.startswith(DC + '/reviews/') and not any(
            rel.endswith(n) for n in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md', 'workflows-author-feedback.v1.md'))):
        continue
    os.makedirs(os.path.dirname(K(rel)), exist_ok=True)
    shutil.copy2(os.path.join(S36, rel), K(rel))
    copied += 1
    verified += sha(K(rel)) == man[rel]
assert copied == verified
R['kit'] = {'copied': copied, 'verified': verified}
TAKEN = [rel for rel in PATCHED if rel != NS]
for rel in TAKEN:
    shutil.copyfile(os.path.join(V1KIT, rel), K(rel))
R['variantBTakesV1BytesFor'] = TAKEN
R['variantBOmitsSchemaEdit'] = sha(K(NS)) == man[NS]
old_par = 'step that carries it terminates with this column, which is the whole-Run code the D9 goldens derive.\n'
t = open(K(NAT), encoding='utf-8').read()
assert t.count(old_par) == 1
DISCLOSURE = ('step that carries it terminates with this column, which is the whole-Run code the D9 goldens derive. The\n'
              '`publicD9Termination` annotation in `native-evidence.schemas.v2.json` still spells this column with its older\n'
              'three-code parenthetical; that enumeration is incomplete and this table governs. Its bytes are deliberately left\n'
              'unchanged: retained Runs commit the digest of that registered schema document, so correcting the annotation belongs\n'
              'to a schema-document successor with its own registration, not to this text alignment.\n')
open(K(NAT), 'w', encoding='utf-8').write(t.replace(old_par, DISCLOSURE))
SOURCE_CHANGED = sorted(TAKEN)
R['perFileDiffEqualsV1PatchExceptNativeContract'] = {rel: udiff_one(rel, K('')) == udiff_one(rel, V1KIT) for rel in SOURCE_CHANGED}
assert all(v for rel, v in R['perFileDiffEqualsV1PatchExceptNativeContract'].items() if rel != NAT)
LEDGERS = [DC + '/foundation/source-pins.v1.json', DC + '/foundation/evaluator3-source-pins.v1.json', DC + '/native/source-pins.v2.json',
           DC + '/security/source-pins.v1.json', DC + '/workflows/source-pins.v1.json']
GENERATED = [DC + '/workflows/workflows-report.v1.json', DC + '/native/native-evidence-report.v2.json']


def reseal(extra=()):
    targets = set(SOURCE_CHANGED) | set(extra) | set(LEDGERS)
    passes = 0
    for passes in range(1, 8):
        moved = False
        for led in LEDGERS:
            raw = open(K(led), 'rb').read()
            obj = json.loads(raw)
            fmt = next(((i, a) for i in (1, 2) for a in (True, False) if (json.dumps(obj, indent=i, ensure_ascii=a) + '\n').encode() == raw), None)
            assert fmt, led
            key = 'files' if 'files' in obj else 'pins'
            for e in obj[key]:
                if e['path'] in targets and e['path'] != led:
                    h = sha(K(e['path']))
                    if e['sha256'] != h:
                        e['sha256'] = h; moved = True
            new = (json.dumps(obj, indent=fmt[0], ensure_ascii=fmt[1]) + '\n').encode()
            if new != raw:
                open(K(led), 'wb').write(new)
        if not moved:
            break
    return passes


def run(name, path, args, cwd, tmo):
    t0 = time.time()
    cmd = [PY, '-I', '-B', path] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=tmo)
        rc, so, se = r.returncode, r.stdout or '', r.stderr or ''
    except subprocess.TimeoutExpired:
        rc, so, se = None, '', 'TIMEOUT'
    open(os.path.join(OUT, 'p05-kit-%s.stdout' % name), 'w').write(so)
    open(os.path.join(OUT, 'p05-kit-%s.stderr' % name), 'w').write(se)
    tail = so.strip().splitlines()[-1:] or ['']
    row = {'name': name, 'command': cmd, 'returncode': rc, 'seconds': round(time.time() - t0, 1), 'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(),
           'lastLine': tail[0][-300:], 'stderrTail': se[-1500:] if rc else ''}
    print('%-26s rc=%-4s %7.1fs %s' % (name, rc, row['seconds'], tail[0][-170:]), flush=True)
    return row


KDC = K(DC)
R['resealPasses'] = {'initial': reseal()}
R['regenerationRuns'] = [run('native-regenerate', K(DC + '/native/check_native_evidence.v2.py'), [], KDC + '/native', 900),
                         run('workflows-regenerate', K(DC + '/workflows/run-reference-checks.py'), ['--report', os.path.join(OUT, 'p05-kit-workflows-regenerate.json')], KDC + '/workflows', 900)]
R['generatedChanged'] = {g: sha(K(g)) != man[g] for g in GENERATED}
R['resealPasses']['afterRegeneration'] = reseal(extra=[g for g in GENERATED if R['generatedChanged'][g]])
JOBS = [
    ('check-query-projection', K(DC + '/workflows/check-query-projection.v3.py'), ['--report', os.path.join(OUT, 'p05-kit-check-query-projection.json')], KDC + '/workflows', 900),
    ('native', K(DC + '/native/check_native_evidence.v2.py'), [], KDC + '/native', 900),
    ('foundation-reference', K(DC + '/foundation/run-reference-checks.py'), ['--report', os.path.join(OUT, 'p05-kit-foundation.json'), '--report-dir', os.path.join(OUT, 'p05-kit-foundation')], KDC + '/foundation', 3600),
    ('evaluator3-launcher', K(DC + '/foundation/run-evaluator3-checks.py'), ['--out', os.path.join(OUT, 'p05-kit-evaluator3')], KDC + '/foundation', 9900),
    ('integration', K(DC + '/check-integration.py'), ['--report', os.path.join(OUT, 'p05-kit-integration.json')], KDC, 900),
    ('security', K(DC + '/security/check-security-lifecycle.v1.py'), ['--report', os.path.join(OUT, 'p05-kit-security.json')], KDC + '/security', 900),
    ('workflows-reference', K(DC + '/workflows/run-reference-checks.py'), ['--report', os.path.join(OUT, 'p05-kit-workflows.json')], KDC + '/workflows', 900),
]
R['suites'] = [run(*j) for j in JOBS]
R['generatedAfterSuites'] = {g: {'sha256': sha(K(g)), 'changedFromFrozen36': sha(K(g)) != man[g]} for g in GENERATED}
R['pinsStillSealedAfterSuites'] = reseal(extra=GENERATED) == 1
R['planning'] = [run('planning-' + n.split('.')[0], K('docs/operations/' + n), a, KIT, 3600)
                 for n, a in (('check_repository_file_inventory.py', ['--check']), ('check_implementation_planning.py', ['--source', KIT, '--check']))]
for g in ('foundation', 'integration', 'security', 'workflows'):
    try:
        d = json.load(open(os.path.join(OUT, 'p05-kit-%s.json' % g)))
        R.setdefault('reports', {})[g] = {k: d.get(k) for k in ('passed', 'failed', 'sourcePinsValid', 'sourceFileCount', 'checksExecuted', 'timedOut')}
        if g == 'foundation':
            R['reports'][g]['childFailures'] = [(c.get('script'), c.get('exitCode'), (c.get('stdout') or '')[:300]) for c in d.get('checks', []) if c.get('exitCode')]
    except Exception as exc:  # noqa: BLE001
        R.setdefault('reports', {})[g] = {'error': str(exc)[:200]}
lr = os.path.join(OUT, 'p05-kit-evaluator3', 'report.json')
if os.path.isfile(lr):
    d = json.load(open(lr))
    R['launcher'] = {'sourcePinsValid': d.get('sourcePinsValid'), 'passed': d.get('passed'), 'children': [(c.get('name'), c.get('exitCode')) for c in d.get('checks', [])],
                     'changedOrMissing': d.get('changedOrMissing', [])}
try:
    q = json.load(open(os.path.join(OUT, 'p05-kit-check-query-projection.json')))
    NEW = ('closed-request-admission-leaves-absent-package-coordinate-to-section-2', 'response-graph-endpoint-still-requires-package-coordinate',
           'package-endpoint-without-coordinate-is-endpoint-ambiguous', 'empty-package-coordinate-is-params-malformed',
           'package-coordinate-on-file-endpoint-is-params-malformed', 'host-availability-unavailable-refuses-evidence-missing',
           'host-availability-corrupt-refuses-evidence-corrupt', 'host-availability-partial-does-not-refuse-by-itself')
    by = {c['id']: c for c in q['checks']}
    R['queryControls'] = {'passed': q['passed'], 'count': q['count'], 'failedCount': q['failedCount'], 'new': {n: by.get(n, {}).get('ok') for n in NEW}}
except Exception as exc:  # noqa: BLE001
    R['queryControls'] = {'error': str(exc)}
try:
    nr = json.load(open(K(DC + '/native/native-evidence-report.v2.json')))
    res = nr['cases']['results']
    R['nativeReport'] = {'result': nr.get('result'), 'pins': nr.get('pins'), 'cases': len(res), 'failed': [c['id'] for c in res if not c['passed']],
                         'newCasePassed': any(c['id'] == 'run-termination-derives-the-d9-exit-contract-reason-code-for-each-deficiency' and c['passed'] for c in res)}
except Exception as exc:  # noqa: BLE001
    R['nativeReport'] = {'error': str(exc)}

spec = importlib.util.spec_from_file_location('ckq_kit2', K(DC + '/workflows/check-query-projection.v3.py'))
CK = importlib.util.module_from_spec(spec); spec.loader.exec_module(CK)
Q = CK.Q
U1 = 'a' * 64
s1 = {}
for label, ep in (('package-absent-coordinate', {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app'}),
                  ('package-empty-coordinate', {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': ''}),
                  ('file-with-coordinate', {'universe': U1, 'kind': 'file', 'nativeSubjectId': 'a.ts', 'packageManifestPath': 'package.json'}),
                  ('kind-outside-set', {'universe': U1, 'kind': 'module', 'nativeSubjectId': 'x'}),
                  ('package-with-coordinate', {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': 'app/package.json'})):
    params = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': ep}
    req = CK.request('graph.neighbors', CK.project_id(), {'runId': CK.run_id()}, params)
    row = {'rawRequestSchemaAdmits': CK.valid(CK.GQ + '#/$defs/GraphQueryRequestV1', req)[0], 'rawResponseEndpointAdmits': CK.valid(CK.GQ + '#/$defs/GraphEndpoint', ep)[0]}
    for name, fn in (('wrapperWithoutRun', lambda: Q.execute_graph_query(req, host=CK.host_obs())), ('helper', lambda: Q.parse_endpoint_syntax(ep, 'endpoint'))):
        try:
            fn(); row[name] = 'not refused'
        except Q.QueryRefusal as exc:
            row[name] = exc.detail
    s1[label] = row
R['kitS1'] = s1
spec = importlib.util.spec_from_file_location('nat_kit2', K(DC + '/native/native_evidence_model.v2.py'))
NK = importlib.util.module_from_spec(spec); spec.loader.exec_module(NK)
d9 = json.load(open(os.path.join(S36, 'docs/coop/artifacts/d9-exit-contract.v1.14.json')))['codeMaps']['deficiencyToReasonCode']
s2 = {}
for d in ('input-closure-incomplete', 'resolution-incomplete', 'external-consumers-unknown', 'derivation-policy-unmet', 'provider-unavailable',
          'language-tier-unsupported', 'budget-exhausted', 'confidence-floor-unmet', 'required-relation-missing'):
    code = NK.run_termination(NK.stage_authority('complete'), [{'relation': 'references', 'deficiency': d, 'nativeCause': None}])['d9']['code']
    want = d9.get(d, d9['verdict-indeterminate'])
    s2[d] = {'model': code, 'd9': want, 'equal': code == want}
R['kitS2'] = s2
nat = open(K(NAT), encoding='utf-8').read()
R['kitS2Section10Rows'] = {n: next(l for l in nat.split('\n') if l.startswith('| `%s` | ' % n)).split('|')[5].strip() for n in
                           ('required-relation-missing', 'language-tier-unsupported', 'confidence-floor-unmet', 'provider-unavailable', 'budget-exhausted', 'input-closure-incomplete')}
R['kitS2DisclosurePresent'] = 'that enumeration is incomplete and this table governs' in nat
contract = open(K(DC + '/workflows/query-projection-contract.v3.md'), encoding='utf-8').read()
R['kitS3ContractNamesUnavailableMapping'] = '`evidence.missing`. There is no `evidence.unavailable` member' in contract and '| trusted availability `unavailable` |' in contract
rowsB, sameB = package_replay(KIT, 'owner_kit2_variantB')
R['variantB'] = {'package13Rows': rowsB, 'sameOutcomesAsFrozen36': sameB}
print('VARIANT B (recommended): package13 same outcomes as frozen36:', sameB, flush=True)

os.makedirs(PATCHDIR, exist_ok=True)
text = ''.join(udiff_one(rel, KIT) for rel in SOURCE_CHANGED)
open(os.path.join(PATCHDIR, 'successor-v23-gaps.v2.patch'), 'w', encoding='utf-8').write(text)
R['patchV2'] = {'path': 'successor-patch/successor-v23-gaps.v2.patch', 'sha256': sha(os.path.join(PATCHDIR, 'successor-v23-gaps.v2.patch')), 'files': SOURCE_CHANGED,
                'plusLines': sum(1 for l in text.splitlines() if l.startswith('+') and not l.startswith('+++')),
                'minusLines': sum(1 for l in text.splitlines() if l.startswith('-') and not l.startswith('---')),
                'notInPatch': {'pinLedgers': LEDGERS, 'generatedReports': [g for g in GENERATED if R['generatedAfterSuites'][g]['changedFromFrozen36']],
                               'planningLayer': 'owed: implementation-normative-inputs.v4.json, implementation-coverage.v1.json and implementation-planning-sources.v1.json pin native-evidence.md and graph-query.schema.json'}}
L4 = json.load(open(os.path.join(S36, 'docs/v2/architecture/implementation-normative-inputs.v4.json')))
R['layer4InputsTouched'] = sorted(p for p in SOURCE_CHANGED if p in {f['path'] for f in L4['files']})
R['allSuitesExitZero'] = all(j['returncode'] == 0 for j in R['suites'])
R['planningExitCodes'] = {p['name']: p['returncode'] for p in R['planning']}
R['frozen36DriftAfter'] = sum(1 for rel, h in man.items() if sha(os.path.join(S36, rel)) != h)
R['v1KitPatchFilesUnchangedAfter'] = all(sha(os.path.join(V1KIT, rel)) == h for rel, h in v1kit_before.items())
print(json.dumps({k: R.get(k) for k in ('allSuitesExitZero', 'planningExitCodes', 'layer4InputsTouched', 'reports', 'launcher', 'queryControls', 'nativeReport',
                                        'kitS3ContractNamesUnavailableMapping', 'kitS2Section10Rows', 'kitS2DisclosurePresent', 'frozen36DriftAfter', 'patchV2',
                                        'resealPasses', 'generatedChanged', 'pinsStillSealedAfterSuites', 'v1KitPatchFilesUnchangedAfter')}, indent=1, default=str))
json.dump(R, open(os.path.join(OUT, 'p05-successor-rehearsal2.json'), 'w'), indent=1, default=str)
print('wrote p05-successor-rehearsal2.json')
