"""Build review.json and review.md for the independent source40 whole-design successor review.

Measurement part; then executes, in these globals, build_review40_findings.py (findings, items, F and residual rows),
build_review40_rows.py (AR/FW/DR/scoped rows, TCB object, retained, limitations) and build_review40_emit.py (assembly, gap checks,
rendering). Reads frozen source40/39 bytes, this origin's own source39 review (read-only history), header-named root/author/codex
evidence and this runtime's receipts. Writes only RT/review.json and RT/review.md. Every hash is recomputed at build time."""
import glob, hashlib, json, os, re

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v40'
S40 = '/tmp/opensip-design-corrections/candidate-subject.v40'
S39 = '/tmp/opensip-design-corrections/candidate-subject.v39'
B = '/tmp/opensip-design-corrections'
REC = RT + '/receipts'
REVIEWS = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
LIVE40 = REVIEWS + '/candidate-subject.v40.json'
LIVE39 = REVIEWS + '/candidate-subject.v39.json'
ARCHIVE40 = REVIEWS + '/candidate-source.v40.tar.gz'
PKG = B + '/claude-author-package-successor.v17'
V39PATH = B + '/claude-independent-design.v39/review.json'
CODEX = REVIEWS + '/codex-post-reset.v1/final-reference.v40/reference-checks.json'
ROOTREF2 = B + '/root-source40-final-reference.v2/reference-checks.json'
ROOTVER = B + '/author-package-final40-verification.v1'
REBUILD = B + '/root-author-package-final40-rebuild.v1/rebuild-report.json'
EXPECT = {'manifest40': '3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072',
          'manifest39': 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009',
          'archive40': 'e9980bc4d30294380c2bb3b91d2d331419db615a7b1b6f41107c7298ba249814',
          'v9': '75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de',
          'codex': '019c339765e3003d6a94bf95b8903d39caf01f7a04a1bba9e6b1d0549cfeb224',
          'pkgManifest': 'f179b7568201c5218e10ad830a81c66cbeddc4aedac9e8fe5f91988b69ca1a4e',
          'filesOnly': 'ec4f69fc01cd46385c1d01dd108ccda4076b9e95f9c1b77d153c662be2d9d796',
          'rootVerification': 'fc69c7aea8f96fbb5f145da48a93b5ca71330c5ef0a4ec1d2a82980d2fd2e984',
          'rebuild': 'd6772c06bcab2f5ab20e1b122370201c7dce206a13096d075ab2e1841c019891'}
ORIGIN = '85a08aec-9d22-4ac6-8ec2-c10170e727d7'
GAPS = []


def sha(p):
    try:
        h = hashlib.sha256()
        with open(p, 'rb') as fh:
            for c in iter(lambda: fh.read(1 << 20), b''):
                h.update(c)
        return h.hexdigest()
    except OSError:
        GAPS.append('missing: ' + p)
        return None


def nlines(p):
    try:
        b = open(p, 'rb').read()
    except OSError:
        return None
    return b.count(b'\n') + (0 if (not b or b.endswith(b'\n')) else 1)


def J(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def rel(p):
    return p.replace(RT + '/', '')


def same39(p):
    return sha(S39 + '/' + p) == sha(S40 + '/' + p)


def find_one(name):
    hits = sorted(glob.glob(S40 + '/docs/**/' + name, recursive=True))
    if len(hits) != 1:
        GAPS.append('path lookup for %s found %d' % (name, len(hits)))
        return None
    return hits[0].replace(S40 + '/', '')


def summ(v):
    if isinstance(v, dict):
        return {k: (len(x) if isinstance(x, (list, dict)) else x) for k, x in v.items()}
    return v


# ------------------------------------------------------------------------------------------------ subject
SV = J(REC + '/subject-verification.json')
delta = SV['delta']
delta_paths = {r['path'] for k in ('changed', 'added', 'removed') for r in delta[k]}
added_paths = {r['path'] for r in delta['added']}
delta_counts = {k: len(delta[k]) for k in ('changed', 'added', 'removed')}
live40, live39, archive40 = sha(LIVE40), sha(LIVE39), sha(ARCHIVE40)
archives = {}
for p in sorted(glob.glob(REC + '/archive-verification*.json')):
    content = J(p)
    archives[rel(p)] = {'sha256': sha(p), 'namesHeaderArchiveSha256': EXPECT['archive40'] in json.dumps(content), 'summary': summ(content)}
archives_ok = len(archives) == 2 and all(a['namesHeaderArchiveSha256'] and any(a['summary'].get(k) is True for k in ('verified', 'passed', 'ok')) for a in archives.values())
if not archives_ok:
    GAPS.append('archive verification receipts do not both state verification of the header archive: ' + json.dumps({k: v['summary'] for k, v in archives.items()})[:900])
verified_manifest = bool(SV['manifest40Matches'] and SV['snapshot40']['verified'] and live40 == EXPECT['manifest40'] and archive40 == EXPECT['archive40']
                         and archives_ok and SV['fileCount40'] == 12911 and SV['totalBytes40'] == 737700535)
parent_ok = bool(live39 == EXPECT['manifest39'] and SV['manifest39Matches'] and SV['snapshot39']['verified'] and SV['parentDeclared'] == EXPECT['manifest39'])
if not verified_manifest or not parent_ok:
    GAPS.append('subject or parent verification incomplete')
if delta_counts != {'changed': 22, 'added': 2, 'removed': 0}:
    GAPS.append('delta counts differ from the header: ' + json.dumps(delta_counts))

# ------------------------------------------------------------------------------------------------ read map
LEDGER = REC + '/read-ledger.jsonl'
ledger = [json.loads(l) for l in open(LEDGER, encoding='utf-8')]


def covers_all(ranges, lines):
    seen = set()
    for part in ranges:
        for seg in str(part).split(','):
            m = re.match(r'^(\d+)-(\d+)$', seg.strip())
            if m:
                seen.update(range(int(m.group(1)), int(m.group(2)) + 1))
    return lines is not None and all(i in seen for i in range(1, lines + 1))


by_path_fresh, delta_rows = {}, {}
for r in ledger:
    if r['kind'] == 'fresh40Read':
        by_path_fresh.setdefault(r['path'], []).append(r)
    elif r['kind'] == 'delta40Read':
        delta_rows[r['path']] = r
fresh, ranged = [], []
for p, rows in sorted(by_path_fresh.items()):
    cur = sha(S40 + '/' + p)
    if any(r['sha256'] != cur for r in rows):
        GAPS.append('fresh read not current: ' + p)
    lines = nlines(S40 + '/' + p)
    ranges = [r['range'] for r in rows]
    entry = {'path': p, 'sha256': cur, 'lines': lines, 'ranges': ranges, 'notes': sorted({r['note'] for r in rows}), 'changed39to40': p in delta_paths, 'addedIn40': p in added_paths}
    if covers_all(ranges, lines):
        entry.update(readClass='fresh40Read', read='complete: every line read this charter')
        fresh.append(entry)
    else:
        entry.update(readClass='fresh40RangeRead', read='named ranges only; not a whole-file read')
        ranged.append(entry)
fresh_paths = {e['path'] for e in fresh}
delta_reads = []
for p, r in sorted(delta_rows.items()):
    cur, dsha = sha(S40 + '/' + p), sha(RT + '/' + r['diff'])
    if cur != r['sha256'] or dsha != r['diffSha256']:
        GAPS.append('delta read not current: ' + p)
    delta_reads.append({'path': p, 'sha256': cur, 'lines': nlines(S40 + '/' + p), 'readClass': 'delta40Read', 'read': 'complete 39->40 diff; not a whole-file read',
                        'alsoFreshWholeFileRead': p in fresh_paths, 'diffReceipt': r['diff'], 'diffSha256': dsha})
v39 = J(V39PATH)
V39TCB = v39['sharedAssumptionTCBSCOPE01']
prior_complete = [dict(e, priorClass='fresh39Read') for e in v39['readScope']['fresh39Read']] + \
                 [dict(e, priorClass='inheritedUnchanged38Read') for e in v39['readScope']['inheritedUnchanged38Read']] + \
                 [dict(e, priorClass='complete38ReadPlusComplete39Diff') for e in v39['readScope']['complete38ReadPlusComplete39Diff']]
inherited, via_diff, changed_not = [], [], []
for e in prior_complete:
    p = e['path']
    if p in fresh_paths:
        continue
    a, b = sha(S39 + '/' + p), sha(S40 + '/' + p)
    if a == b:
        inherited.append({'path': p, 'sha256': b, 'readClass': 'inheritedUnchanged39Read', 'priorClass': e['priorClass'],
                          'basis': 'counted as completely read by this origin\'s source39 review; byte-identical in source40 (hash recomputed now); not re-read this charter'})
    elif p in delta_rows:
        via_diff.append({'path': p, 'sha39': a, 'sha40': b, 'readClass': 'complete39ReadPlusComplete40Diff', 'priorClass': e['priorClass'],
                         'basis': 'source39 bytes counted as completely read plus the exact complete 39->40 diff; not a fresh whole-file read'})
    else:
        changed_not.append({'path': p, 'sha39': a, 'sha40': b, 'priorClass': e['priorClass']})
prior_ranges = [{'path': e['path'], 'ranges': e.get('ranges'), 'unchanged39to40': same39(e['path']), 'readClass': 'prior39RangeReadOnly',
                 'basis': 'source39 range read only; never counted as a whole-file read'} for e in v39['readScope']['fresh39RangeRead']]
covered = fresh_paths | {e['path'] for e in ranged} | set(delta_rows)
uncovered_delta = sorted(delta_paths - covered)
for p in uncovered_delta:
    GAPS.append('delta file without read entry: ' + p)
SEARCH_ONLY = [
    {'path': 'docs/coop/design-corrections/foundation/enumeration-contract.v1.md', 'lines': '17 (one cell per requested capability tuple), 19, 26, 82, 86, 92, 141', 'standing': 'seen in search output only; not a read'},
    {'path': 'docs/coop/design-corrections/native/native-capability-matrix.v2.json', 'lines': 'capabilities[].relations (11 capabilities)', 'standing': 'values extracted by a one-off script; not a line read'},
    {'path': 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py', 'lines': 'admit and store_pointers call sites (104-105, 319, 448, 678, 933, 1054, 1295)', 'standing': 'seen in search output only, beyond the ledgered ranges'},
    {'path': 'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py', 'lines': 'selectedRefs/outputRefs call sites (100-120, 165, 190, 909, 1051, 1083-1085, 1633-1645)', 'standing': 'seen in search output only, beyond the ledgered range 1095-1166'},
]

# ------------------------------------------------------------------------------------------------ commands
G = J(REC + '/reference/groups-report.all.json')
group_rows = [{'name': r['name'], 'command': r['command'], 'exitCode': r['exitCode'], 'timedOut': r['timedOut'], 'seconds': r['seconds'],
               'scriptMatchesManifest': r['scriptMatchesManifest'], 'stdoutSha256': r['stdoutSha256'], 'copyAfter': summ(r['copyAfter']),
               'stdoutTail': r['stdoutTail'][-300:]} for r in G['rows']]
groups_ok = G['passed'] is True and len(group_rows) == 6 and all(r['exitCode'] == 0 and not r['timedOut'] and r['scriptMatchesManifest'] for r in group_rows)
if not groups_ok:
    GAPS.append('reference groups not all passing')
ev3 = re.findall(r'^(\S+) (\d+)[ \t]*$', open(REC + '/reference/evaluator3.stdout').read(), re.M)
children = {n: {'exitCode': int(c)} for n, c in ev3}
for f in sorted(glob.glob(REC + '/reference/evaluator3/*.stdout')):
    n = os.path.basename(f)[:-7]
    info = {'stdoutSha256': sha(f)}
    try:
        d = J(f)
        for k in ('passed', 'ok', 'count', 'total', 'failed', 'failedCount'):
            if k in d and not isinstance(d[k], (dict, list)):
                info[k] = d[k]
        for k in ('failed', 'cases', 'mismatches', 'checks', 'results', 'rows'):
            if isinstance(d.get(k), (list, dict)):
                info[k + 'Count'] = len(d[k])
    except ValueError:
        info['nonJson'] = True
    children.setdefault(n, {}).update(info)
children_ok = len(ev3) == 17 and all(c.get('exitCode') == 0 for c in children.values())
if not children_ok:
    GAPS.append('evaluator3 children not all exit 0')
FOUND = J(REC + '/reference/foundation.json')
foundation_checks = [{'script': os.path.basename(c['script']), 'exitCode': c['exitCode'], 'timedOut': c.get('timedOut')} for c in FOUND['checks']]
P = J(REC + '/planning-checks.json')
PC = P['counts']
planning_ok = P['check_implementation_planning']['exitCode'] == 0 and P['check_repository_file_inventory']['exitCode'] == 0 and PC['v9Sha256'] == EXPECT['v9'] \
    and not PC['v9Mismatched'] and PC['coverageMappings'] == 322
if not planning_ok:
    GAPS.append('planning checks or counts not as measured')
RC = J(REC + '/reference-comparison.json')


def runs_of(name):
    runs = glob.glob(REC + '/runs/' + name + '.run.json') + glob.glob(REC + '/runs/' + name + '.attempt*.run.json')
    return sorted(runs, key=lambda p: int(re.search(r'\.attempt(\d+)\.run\.json$', p).group(1)) if '.attempt' in p else 1)


def run_record(name, script):
    runs = runs_of(name)
    if not runs:
        GAPS.append('no run receipt: ' + name)
        return None
    last = J(runs[-1])
    cur = sha(script)
    if not (last['exitCode'] == 0 and not last['copyChangedVsManifest'] and not last['copyExtraVsManifest'] and last['scriptSha256'] == cur):
        GAPS.append('latest run not clean or script changed after it: ' + name)
    return {'runReceipt': rel(runs[-1]), 'runReceiptSha256': sha(runs[-1]), 'command': last['command'], 'exitCode': last['exitCode'], 'seconds': last['seconds'],
            'scriptSha256': last['scriptSha256'], 'scriptUnchangedSinceRun': last['scriptSha256'] == cur,
            'probeCopyUnchanged': not last['copyChangedVsManifest'] and not last['copyExtraVsManifest'], 'stdoutSha256': last['stdoutSha256'],
            'earlierAttempts': [{'runReceipt': rel(p), 'scriptSha256': J(p)['scriptSha256'], 'exitCode': J(p)['exitCode'],
                                 'stdout': rel(p[:-len('.run.json')] + '.stdout'), 'stdoutSha256': sha(p[:-len('.run.json')] + '.stdout')} for p in runs[:-1]]}


def rows_of(name):
    return {r['case']: r for r in J(REC + '/probes/' + name)['rows']}


def probe_result(name):
    d = J(REC + '/probes/' + name)
    return {'receipt': 'receipts/probes/' + name, 'sha256': sha(REC + '/probes/' + name), 'rows': len(d['rows']), 'failedRows': [r['case'] for r in d['failed']],
            'observationRows': [r['case'] for r in d['rows'] if r.get('kind') in ('observation', 'source-text', 'record')]}


PROBE_DEFS = [
    ('P40-SUBJECT', 'probes/verify_subject.py', None, ['subject-verification.json', 'manifest40-index.json'],
     'Formal manifest 3be45284... and all 12,911 snapshot members (hash and length, none unlisted); parent39 manifest f71a5992... and all 12,909 parent members; exact 39->40 delta (22 changed, 2 added, 0 removed).'),
    ('P40-ARCHIVE', 'probes/verify_archive_extract.py', None, ['archive-verification.source40.json', 'archive-verification.source40-pkg.json'],
     'Archive e9980bc4... hashed; every member verified against the manifest and extracted into two disposable copies (groups copy work/source40, probe copy work/source40-pkg).'),
    ('P40-DELTA', 'probes/make_delta_diffs.py', None, ['delta-diff-summary.json'], 'Unified diffs for all 22 changed files with both sides hash-verified.'),
    ('P40-GROUPS', 'probes/run_reference_groups.py', None, ['reference/groups-report.all.json', 'reference/evaluator3.stdout', 'reference/foundation.json'],
     'Six pinned groups with /tmp/opensip-architecture-review-env/bin/python -I -B on the verified groups copy, copy re-verified after each; 17 evaluator3 children.'),
    ('P40-PLAN', 'probes/run_planning_checks.py', None, ['planning-checks.json'],
     'check_implementation_planning --check and check_repository_file_inventory --check; v9/v8 layer recounts; coverage population measured against source39.'),
    ('P40-REFERENCE-COMPARE', 'probes/compare_reference_v40.py', None, ['reference-comparison.json'],
     'This review\'s groups and children compared with the header-named codex final-reference.v40 run (evidence only).'),
    ('P40-POLICY', 'probes/probe_policy_v40.py', 'policy-v40', 'policy-v40.json',
     'S39-01, S39-02 and imported fact-universe discrimination on source39 versus source40 bytes in separate processes against bounded production composition; policy.show; identity preimages.'),
    ('P40-NATIVE', 'probes/probe_native_v40.py', 'native-v40', 'native-v40.json',
     'U-1/section 1.2 effective allowJs; U-4b.2 nested Cargo folding and U-4b.5 law; unitKind projection with full Run closure; source39 baselines.'),
    ('P40-RUNTERM-ADV', 'probes/probe_runterm_adv_v40.py', 'runterm-adv-v40', 'runterm-adv-v40.json',
     'Run-termination clarification keys against the unchanged model; independent commit-inventory recompute over a closed Run; ADV39-01 account; internal keys not public.'),
    ('P40-VIEWDIGESTS', 'probes/probe_viewdigests_v40.py', 'viewdigests-v40', 'viewdigests-v40.json',
     'CellProgramOutcomeV1.viewDigests over the three maintained owner graphs: row population, sharing, totality refusals, source text.'),
    ('P40-VIEWDIGESTS-B', 'probes/probe_viewdigests_v40b.py', 'viewdigests-v40b', 'viewdigests-v40b.json',
     'Two producer-, Plan- and universe-matched views minted into the owner graph and rebuilt through the maintained builder: reference attribution versus the four published coordinates.'),
    ('P40-VIEWDIGESTS-C', 'probes/probe_viewdigests_v40c.py', 'viewdigests-v40c', 'viewdigests-v40c.json',
     'The same graph with the unattributed returned view recorded as a stage return (receipt outputRefs and selectedRefs, no row), store pointers recomputed by promised_pointers.'),
    ('P40-PACKAGE', 'probes/probe_package_v17.py', 'package-v17-evidence', 'package-v17.json',
     'Package v17 manifest, formal versus files-only manifests, overlay base provenance, package16 preserved, content equality with root verification and rebuild, normalization-map controls.'),
    ('P40-PORTED-QUERY', 'probes/ported_probe_query_carriers.py', 'query-carriers', 'query-carriers.json', 'Ported source39 probe: query commands, operations, carriers and delivery law.'),
    ('P40-PORTED-CARRIER', 'probes/ported_probe_carrier_readonly.py', 'carrier-readonly', 'carrier-readonly.json', 'Ported: read-only carrier scenarios on real SQLite.'),
    ('P40-PORTED-COMPARISON', 'probes/ported_probe_comparison_knowledge.py', 'comparison-knowledge', 'comparison-knowledge.json', 'Ported: comparison presence-knowledge helpers.'),
    ('P40-PORTED-REPAIR2', 'probes/ported_probe_repair2.py', 'repair2', 'repair2.json', 'Ported: repair:2 constructor refusal order and exact-class unavailability.'),
    ('P40-PORTED-TERM7', 'probes/ported_probe_run_termination_s7.py', 'run-termination-s7', 'run-termination-s7.json', 'Ported: run-termination section 7 host composition admission over golden Runs.'),
    ('P40-PORTED-CUSTODY', 'probes/ported_probe_native_custody_fallback.py', 'native-custody-fallback', 'native-custody-fallback.json', 'Ported: pruned-tree read custody and U-9 fallback helpers.'),
]
PROBES, PBY = [], {}
for pid, script, runname, receipt, claim in PROBE_DEFS:
    e = {'id': pid, 'script': script, 'scriptSha256': sha(RT + '/' + script), 'claim': claim}
    if runname:
        e['execution'] = run_record(runname, RT + '/' + script)
        e['result'] = probe_result(receipt)
        if e['result']['failedRows']:
            GAPS.append('probe has failed rows: ' + pid)
    else:
        e['receipts'] = {'receipts/' + r: sha(REC + '/' + r) for r in receipt}
    PROBES.append(e)
    PBY[pid] = e
PKG_RUNS = {'verify-package.py': run_record('package-v17-verify', PKG + '/verify-package.py'),
            'probe-native-v2.py': run_record('package-v17-probe-native-v2', PKG + '/probe-native-v2.py')}
PORT = J(REC + '/probe-port.json')
POL, NAT, RTA = rows_of('policy-v40.json'), rows_of('native-v40.json'), rows_of('runterm-adv-v40.json')
VD, VDB, VDC, PK = rows_of('viewdigests-v40.json'), rows_of('viewdigests-v40b.json'), rows_of('viewdigests-v40c.json'), rows_of('package-v17.json')

# ------------------------------------------------------------------------------------------------ owner map
CR = find_one('commit-recovery-readonly.v3.md')
CD = find_one('carrier-dispatch.v3.json')
MAP_FILES = ['docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json', 'docs/coop/design-corrections/correction-crosswalk.proposed.json',
             'docs/coop/design-corrections/inherited-residuals.proposed.md', 'docs/coop/design-corrections/current-source-map.proposed.md',
             'docs/v2/architecture/08-decision-and-readiness-register.md', 'docs/coop/design-corrections/qualification-gates.proposed.json',
             'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md',
             'docs/v2/contracts/product-v1/security-and-lifecycle.md', 'docs/v2/contracts/product-v1/native-evidence.md',
             'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'docs/v2/contracts/product-v1/README.md',
             'docs/v2/architecture/prototype-report-inventory.md', 'docs/v2/architecture/repository-file-inventory.v1.json',
             'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md', 'docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json',
             'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py', 'docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py',
             'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py', 'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md',
             'docs/coop/design-corrections/foundation/identity-schemas.v3.json', 'docs/coop/design-corrections/foundation/identity-model.v3.py',
             'docs/coop/design-corrections/foundation/run_termination_model.v1.py'] + [p for p in (CR, CD) if p]
MAP = {p: {'sha256': sha(S40 + '/' + p), 'unchanged39to40': same39(p)} for p in MAP_FILES}
U = {os.path.basename(p): v['unchanged39to40'] for p, v in MAP.items()}
GATES = J(S40 + '/docs/coop/design-corrections/qualification-gates.proposed.json')['items']
gates_true = sum(1 for g in GATES if g.get('qualified') is True)
REG = open(S40 + '/docs/v2/architecture/08-decision-and-readiness-register.md', encoding='utf-8').read().splitlines()
cond2_ok = '28 existing rows' in ' '.join(REG[384:391])
if len(GATES) != 32 or gates_true != 0 or not cond2_ok:
    GAPS.append('gates or condition-2 measurement differs')
EI_OWNER_UNCHANGED = all(U[k] for k in ('execution-inputs-contract.v1.md', 'execution-inputs.schema.v1.json', 'execution_inputs_model.v1.py', 'execution_inputs_fixture.v3.py', 'check-execution-inputs.v1.py'))

# ------------------------------------------------------------------------------------------------ package and evidence
MV = J(RT + '/work/package-v17-verify/verification.json')
NM = J(RT + '/work/package-v17-verify/normalization-map-controls1/report.json')
NV = J(RT + '/work/probe-native-v2.json')
vgroups = [{'group': g['group'], 'count': g.get('count'), 'passed': g.get('passed'), 'exitCode': g.get('exitCode')} for g in MV['groups']]
nm_controls = [{k: c.get(k) for k in ('name', 'claimedRunId', 'ownerAdmission', 'semanticAdmission', 'passed', 'exceptionType', 'reason')} for c in NM['checks']]
export_count = sum(g['count'] or 0 for g in vgroups if g['group'] != 'query')
query_count = next((g['count'] for g in vgroups if g['group'] == 'query'), None)
pkg_ok = (sha(PKG + '/artifact-manifest.json') == EXPECT['pkgManifest'] and all(v['ok'] for v in PK.values()) and len(nm_controls) == 4 and export_count == 17
          and query_count == 7 and len(NV['runs']) == 9 and NV['passed'] is True and all(g['passed'] for g in vgroups))
if not pkg_ok:
    GAPS.append('package v17 verification not as recorded')
PACKAGE = {
    'package': PKG, 'artifactManifestSha256': sha(PKG + '/artifact-manifest.json'), 'expectedArtifactManifestSha256': EXPECT['pkgManifest'],
    'filesOnlySourceManifestSha256': sha(PKG + '/source-manifest.json'), 'expectedFilesOnly': EXPECT['filesOnly'], 'formalSubjectManifestSha256': live40,
    'sourceBindingV40Sha256': sha(PKG + '/source-binding.v40.json'), 'rebuildReportSha256': sha(REBUILD), 'rootVerificationSha256': sha(ROOTVER + '/verification.json'),
    'rootRebuildRebuildReportExpected': EXPECT['rebuild'], 'rootVerificationExpected': EXPECT['rootVerification'],
    'package16ArtifactManifestSha256': sha(B + '/claude-author-package-successor.v16/artifact-manifest.json'),
    'probeRows': {k: {'ok': v['ok'], 'observed': v['observed']} for k, v in PK.items() if v.get('kind') != 'record'},
    'verificationGroups': vgroups, 'exports': export_count, 'queries': query_count, 'normalizationMapControls': nm_controls,
    'nativeV2Probe': {'runs': [r['name'] for r in NV['runs']], 'passed': NV['passed'], 'unitsVsDiscoveryDisagreements': NV['unitsVsDiscoveryDisagreements']},
    'toolRuns': PKG_RUNS, 'verified': pkg_ok,
    'result': ('Package v17 verified as author evidence: every one of its files matches the artifact manifest f179b756...; the formal subject manifest and the files-only source manifest ec4f69fc... are different objects with equal file members; '
               'the rebuild base is package15 constructors plus the native-v2 migration overlay (overlay base digests match retained package15), not package16, which is preserved unchanged. '
               'This review re-executed verify-package.py and probe-native-v2.py on its own verified copy: groups %s; %d exports and %d queries. '
               'A non-zero exit is recorded only for %s, whose exported stores are refusing controls; the verifier records passed=true for every group, and this review reports that record without reinterpreting it. '
               'The verification and all compared output files are content-equal to the root verification, and the 9 membership probes are content-equal to the root rebuild probe.'
               % (', '.join('%s %s (passed %s, exit %s)' % (g['group'], g['count'], g['passed'], g['exitCode']) for g in vgroups), export_count, query_count or 0,
                  ', '.join(g['group'] for g in vgroups if g['exitCode'] not in (0, None)) or 'no group')),
    'limits': ['Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.',
               'Rebuilt by root from package15 constructors plus the migration overlay against source40; 17 of 17 exports carry new RunIds; package16 stays unchanged history; no export relabel.',
               'Preserved limitations: the partial TypeScript consumer helper leaves and/or/not unexercised; count-at-most/all-covered are unimplemented; two-binding qualification is incomplete (single explicit binding); all 30 evaluations remain PENDING.',
               'The 4 TypeScript normalization-map negatives are the exact refusals recorded below for those exported stores; they are not generalized to other map defects.',
               'No compiler, provider, OS or process-isolation qualification; independent grades granted: 0.'],
}
CODEXD = J(CODEX)
EVIDENCE = {
    'standing': 'NONBLIND header-named evidence, not acceptance.',
    'records': [
        {'path': CODEX, 'sha256': sha(CODEX), 'expected': EXPECT['codex'], 'passed': CODEXD.get('passed'), 'subjectManifestSha256': CODEXD.get('subjectManifestSha256'), 'note': 'current reference evidence named by the header'},
        {'path': ROOTREF2, 'sha256': sha(ROOTREF2), 'note': 'original execution of the current reference; the codex runner-original equals it: %s' % RC['codexRunnerOriginalEqualsRootOriginal']},
        {'path': REBUILD, 'sha256': sha(REBUILD), 'expected': EXPECT['rebuild'], 'note': 'root reconstruction of package v17 from package15 plus overlay (author construction evidence)'},
        {'path': ROOTVER + '/verification.json', 'sha256': sha(ROOTVER + '/verification.json'), 'expected': EXPECT['rootVerification'], 'note': 'root verification of package v17; content-equal to this review\'s run'},
        {'path': B + '/root-source40-final-reference.v1', 'used': False, 'note': 'preliminary root source40 reference v1; predates final integration; not current evidence; not read'},
    ],
}

for part in ('build_review40_findings.py', 'build_review40_rows.py', 'build_review40_emit.py'):
    path = RT + '/probes/' + part
    exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), globals())
