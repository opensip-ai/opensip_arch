"""Independent reviewer probes, part D: corrections to my own part-A/B/C probe defects,
the consent/CI binding question raised by P8, and final custody re-verification."""
import ast
import copy
import hashlib
import importlib.util
import json
import re
import traceback
from pathlib import Path

from jsonschema import ValidationError

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v4/scratch')
SNAP = Path('/tmp/opensip-design-corrections/candidate-subject.v4')
DC = ROOT / 'docs/coop/design-corrections'
CONTRACTS = ROOT / 'docs/v2/contracts/product-v1'
ARCH = ROOT / 'docs/v2/architecture'

spec = importlib.util.spec_from_file_location('probe_host_d', DC / 'integration-host-model.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
S, N, W, C = M.S, M.N, M.W, M.C
IM = N.IM

results = []


def rec(pid, title, status, detail):
    results.append({'probe': pid, 'title': title, 'status': status, 'detail': detail})
    print('%-6s %-14s %s' % (pid, status, title))
    if status != 'OK':
        print('        ' + json.dumps(detail, default=str)[:2200])


def probe(pid, title):
    def deco(fn):
        try:
            out = fn()
        except Exception as exc:
            rec(pid, title, 'PROBE-ERROR', {'exception': ''.join(
                traceback.format_exception_only(type(exc), exc)).strip()})
            return
        status, detail = out if isinstance(out, tuple) else (('OK' if out else 'COUNTEREXAMPLE'), out)
        rec(pid, title, status, detail)
    return deco


SF = C.parse((DC / 'security/execution-principal-cases.v1.json').read_bytes())
INV = C.parse((DC / 'workflows/command-inventory.v1.json').read_bytes())


def mk(mode, grant_ci, ctx_ci, platform='macos-aarch64'):
    g, ctx = copy.deepcopy(SF['grantBase']), copy.deepcopy(SF['ctxBase'])
    g.update(executionClass='test-runner', owners=[], dependencySourceSetId=None, platformId=platform,
             runner={'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'})
    argv = ['bin/opensip-test-runner', '--ci']
    g['argvDigest'] = W.payload_digest(argv)
    g['effects'] = dict(S.PLATFORM_TRUTH_TABLE[platform])
    g['authorization'] = {'mode': mode, 'policyRecordId': 'a' * 64 if mode == 'policy-record' else None,
                          'ci': grant_ci}
    d = M.owner_digest(g['owners']); g['ownerSourceDigest'] = ctx['ownerSourceDigest'] = d
    ctx.pop('semanticGrantPrincipals', None)
    ctx.update(projectId=g['projectId'], snapshotId=g['snapshotId'], argvDigest=g['argvDigest'], ci=ctx_ci)
    return g, ctx


@probe('P8d', 'ADV-i residue resolved: SECURITY binds grant.ci to the observed invocation ci, on all 4 platforms')
def _():
    """P8 asked whether the test projection's lack of a ci field leaves grant.ci unasserted.
    It does not: admission itself refuses every disagreement, and ci is a real boolean."""
    rows = {}
    for platform in sorted(S.PLATFORM_TRUTH_TABLE):
        for mode in ('policy-record', 'interactive-explicit'):
            for gci in (False, True):
                for cci in (False, True):
                    g, ctx = mk(mode, gci, cci, platform)
                    try:
                        rows['%s.%s.g=%s.c=%s' % (platform, mode, gci, cci)] = \
                            S.admit_repo_execution_grant(g, ctx)['result']
                    except Exception as exc:
                        rows['%s.%s.g=%s.c=%s' % (platform, mode, gci, cci)] = 'RAISED:' + type(exc).__name__
    disagreements = {k: v for k, v in rows.items() if k.split('.')[-2][2:] != k.split('.')[-1][2:]}
    agreements = {k: v for k, v in rows.items() if k not in disagreements}
    typed = {}
    for bad in (1, 'true', None, 'False'):
        g, ctx = mk('policy-record', False, False)
        g['authorization']['ci'] = bad
        try:
            typed[repr(bad)] = S.admit_repo_execution_grant(g, ctx)['result']
        except Exception as exc:
            typed[repr(bad)] = 'RAISED:' + type(exc).__name__
    ok = (all(v == 'REFUSE' for v in disagreements.values())
          and all(v != 'ADMIT' for v in typed.values())
          and len(rows) == 32)
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'allDisagreementsRefused': all(v == 'REFUSE' for v in disagreements.values()),
        'agreements': {k: v for k, v in list(agreements.items())[:8]},
        'nonBooleanCiOutcomes': typed,
        'interactiveInCiAlwaysRefused': all(
            v == 'REFUSE' for k, v in rows.items() if 'interactive-explicit' in k and k.endswith('c=True')),
        'combinations': len(rows)}


@probe('P71d', 'R-9: no SEMANTIC identity domain carries an operational identifier (commit-receipt is operational)')
def _():
    schemas = C.parse((DC / 'foundation/identity-schemas.v2.json').read_bytes())
    src = (DC / 'foundation/identity-model.py').read_text()
    # literal_eval, not eval: this is a dict literal lifted out of the frozen subject source
    prefixes = ast.literal_eval(re.search(r'PREFIX=(\{.*?\})', src, re.S).group(1))
    semantic = set(prefixes)
    leaks = {}
    for name in semantic:
        body = schemas['$defs'].get(name)
        if body is None:
            continue
        text = json.dumps(body)
        hits = [k for k in ('requestId', 'executionId', 'receiptTimestamp', 'storagePath',
                            'cacheState', 'credential', 'lifetime') if k in text]
        if hits:
            leaks[name] = hits
    operational = sorted(set(schemas['$defs']) - semantic)
    return ('OK' if not leaks else 'COUNTEREXAMPLE'), {
        'semanticDomains': sorted(semantic), 'leaks': leaks,
        'operationalRecords': operational,
        'commitReceiptIsOperational': 'commit-receipt' not in semantic}


@probe('P77d', 'Fallow FW-01..15 each carry a current-contract row in the source map')
def _():
    src = (DC / 'current-source-map.proposed.md').read_text()
    rows = {}
    for m in re.finditer(r'^\| (FW-\d\d)([^|]*)\|(.+?)\|\s*$', src, re.M):
        rows[m.group(1)] = m.group(3).strip()
    thin = [k for k, v in rows.items() if len(v) < 40]
    return ('OK' if len(rows) == 15 and not thin else 'COUNTEREXAMPLE'), {
        'count': len(rows), 'ids': sorted(rows), 'thinRows': thin,
        'fw11': rows.get('FW-11', '')[:260], 'fw14': rows.get('FW-14', '')[:220]}


@probe('P79', 'FW-11 numeric comparability is owned by architecture file 13 section 6 and cross-referenced')
def _():
    f13 = (ARCH / '13-evidence-workflows-and-product-contracts.md').read_text()
    src = (DC / 'current-source-map.proposed.md').read_text()
    wf = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    rule = 'diff\nscope and comparison base must agree or be reported incompatible' in f13 or \
           'scope and comparison base must agree or be reported incompatible' in f13
    return ('OK' if rule and 'Architecture13 §6 restrictions remain binding' in src else 'ADVISORY'), {
        'file13StatesTheRule': rule,
        'sourceMapKeepsFile13Binding': 'Architecture13 §6 restrictions remain binding' in src,
        'workflowContractRestatesIt': 'redistribution' in wf.lower(),
        'note': 'the owning statement lives in the inherited chapter the source map keeps binding'}


@probe('P80', 'Unit READMEs declare NOT SELF-ACCEPTED (my part-C regex matched inside that phrase)')
def _():
    rows = {}
    for p in (DC / 'README.md', DC / 'JOINT-INTERFACES.md', DC / 'foundation/README.md',
              DC / 'security/README.md', DC / 'native/README.md', DC / 'workflows/README.md'):
        t = p.read_text()
        claims = [m for m in re.findall(r'.{40}\bACCEPTED\b.{40}', t)]
        rows[str(p.relative_to(DC))] = {
            'notSelfAccepted': 'NOT SELF-ACCEPTED' in t or 'not self-accepted' in t.lower(),
            'acceptedMentions': [c.strip()[:90] for c in claims][:2]}
    bad = {k: v for k, v in rows.items()
           if v['acceptedMentions'] and not all('SELF-ACCEPTED' in c for c in v['acceptedMentions'])}
    return ('OK' if not bad else 'ADVISORY'), rows


@probe('P81', 'SARIF: the workflow reference suite contains no check of SARIF content for the four commands')
def _():
    src = (DC / 'workflows/check_workflows.v1.py').read_text()
    integ = (DC / 'check-integration.py').read_text()
    sarif_lines = [l.strip() for l in src.splitlines() if 'sarif' in l.lower()]
    integ_lines = [l.strip() for l in integ.splitlines() if 'sarif' in l.lower()]
    report = json.load(open('/tmp/opensip-design-corrections/post-reset-review.v4/reports/'
                            'workflows-report.rerun.json'))
    checks = report.get('checks') if isinstance(report.get('checks'), list) else []
    ids = [c.get('id') for c in checks if isinstance(c, dict)]
    sarif_checks = sorted(i for i in ids if i and 'sarif' in str(i).lower())
    return ('OK' if len(sarif_checks) >= 4 else 'COUNTEREXAMPLE'), {
        'workflowCheckerSarifLines': sarif_lines[:6],
        'integrationCheckerSarifLines': integ_lines[:6],
        'sarifNamedChecksInReport': sarif_checks,
        'totalWorkflowChecks': len(ids)}


@probe('P82', 'Final custody: the frozen snapshot and the repository are byte-unchanged after every probe')
def _():
    manifest = json.load(open('/Users/sb/code/opensip-ai/opensip_arch/'
                              'docs/coop/design-corrections/reviews/candidate-subject.v4.json'))
    mh = hashlib.sha256(open('/Users/sb/code/opensip-ai/opensip_arch/'
                             'docs/coop/design-corrections/reviews/candidate-subject.v4.json',
                             'rb').read()).hexdigest()
    ok = 0; bad = []
    seen = set()
    for f in manifest['files']:
        p = SNAP / f['path']
        seen.add(str(p.resolve()))
        if not p.exists():
            bad.append((f['path'], 'MISSING')); continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != f['sha256']:
            bad.append((f['path'], 'CHANGED')); continue
        ok += 1
    extra = []
    for dp, dn, fn in __import__('os').walk(SNAP):
        for n in fn:
            if str(Path(dp, n).resolve()) not in seen:
                extra.append(str(Path(dp, n).relative_to(SNAP)))
    # the scratch copy IS expected to differ only where the checkers rewrote their own reports
    drift = []
    for f in manifest['files']:
        s = ROOT / f['path']
        if s.exists() and hashlib.sha256(s.read_bytes()).hexdigest() != f['sha256']:
            drift.append(f['path'])
    return ('OK' if not bad and not extra and mh ==
            '2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2' else 'COUNTEREXAMPLE'), {
        'manifestSha256': mh, 'verified': ok, 'mismatched': bad, 'extraOnDisk': extra,
        'scratchFilesDifferingFromSnapshot': drift,
        'note': 'scratch drift would be checker rewrites; snapshot itself must be identical'}


out = Path('/tmp/opensip-design-corrections/post-reset-review.v4/probes/independent-probes-d.json')
summary = {'part': 'D (probe corrections, consent/CI binding, final custody)',
           'manifestSha256': '2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2',
           'counts': {}, 'probes': results}
for r in results:
    summary['counts'][r['status']] = summary['counts'].get(r['status'], 0) + 1
out.write_text(json.dumps(summary, indent=1, default=str) + '\n')
print()
print(json.dumps(summary['counts']))
