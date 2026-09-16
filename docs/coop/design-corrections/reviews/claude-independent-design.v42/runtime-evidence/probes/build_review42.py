"""Build review.json and review.md for the independent source42 whole-design successor review.

Measurement part; then executes, in these globals, build_review42_findings.py (findings, source40 finding dispositions, items),
build_review42_rows.py (107 rows, TCB object, retained, authority, limitations) and build_review42_emit.py (assembly, gap checks,
rendering). Reads frozen source42/41/40 bytes, this origin's completed source40 review (read-only history), header-named
author/root/codex evidence and this runtime's receipts. Writes only RT/review.json and RT/review.md. Hashes recomputed now."""
import glob, hashlib, json, os, re

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
S42 = '/tmp/opensip-design-corrections/candidate-subject.v42'
S41 = '/tmp/opensip-design-corrections/candidate-subject.v41'
S40 = '/tmp/opensip-design-corrections/candidate-subject.v40'
B = '/tmp/opensip-design-corrections'
REC = RT + '/receipts'
REVIEWS = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
LIVE42 = REVIEWS + '/candidate-subject.v42.json'
ARCHIVE42 = REVIEWS + '/candidate-source.v42.tar.gz'
PKG = B + '/claude-author-package-successor.v19'
V40PATH = B + '/claude-independent-design.v40/review.json'
CODEX = REVIEWS + '/codex-post-reset.v1/final-reference.v42/reference-checks.json'
ROOTREF3 = B + '/root-source42-final-reference.v3/reference-checks.json'
ROOTVER = B + '/author-package-final42-verification.v1/verification.json'
REBUILD = B + '/root-author-package-final42-rebuild.v1/rebuild-report.json'
ORIGIN = '85a08aec-9d22-4ac6-8ec2-c10170e727d7'
EXPECT = {'manifest42': 'f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307',
          'manifest41': 'eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236',
          'manifest40': '3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072',
          'archive42': '2423c7807b489ef9af199f6eb4c44cc8a42b53160555621cf4b6a65d56fcb4c6',
          'pkgManifest': '346a4d4b298404b9dabd1f9a6206733351723853cd5bd7f23e9896199b641a31',
          'sourceBinding': '0c50efc7742a38ba7a62b78e0f10c9762632b0cb753e962c2aff7003993e91bc',
          'rootVerification': 'eeca54cdef3ab86ac09ae9ced23cbd847bc1a25f8936a0ded8aad1f3d825dee1',
          'codex': 'd46d0bf272dbcc471e1d8d41c5a4eae9d2b8b864669c2c3c96d9cb58e814292b',
          'rebuild': '73f1f73861eb570167bc4b416f68c3527e2d010ba305b8c643810c47a7e3d5e4',
          'v11': '75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de',
          'review40': '184bbd91cf183410ed7a6cb419e1a0ed80ce18f9ccd4ff333a069c68c03fc97b'}
AUTHOR = {'view-attribution': (B + '/claude-view-attribution-assessment.v1/review.json', 'a06602738c29bd923cf2c1d0a9d47b6a011a819d5f49ef1ac43a366be8cd23de'),
          'attribution-capture': (B + '/claude-attribution-capture-assessment.v1/review.json', '1d15650e937960fd6bb43a6814f63d69425055db9cb11101ca06c08775002e23'),
          'program-entry-clarification': (B + '/claude-program-entry-clarification.v1/review.json', '70830fd30e7e5243b6bbceeac7c13726869c996df7cc7b47c7547c6603bb7ed4'),
          'program-entry-enforcement': (B + '/claude-program-entry-enforcement.v1/review.json', '57fd9d756627d5b0d22bff4f7f2e1e706b8ce115217c652089732d50e2d4e71b')}
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


def same(a_root, b_root, p):
    return sha(a_root + '/' + p) == sha(b_root + '/' + p)


def summ(v):
    if isinstance(v, dict):
        return {k: (len(x) if isinstance(x, (list, dict)) else x) for k, x in v.items()}
    return v


# ------------------------------------------------------------------------------------------------ subject
SV = J(REC + '/subject-verification.json')
live42, archive42 = sha(LIVE42), sha(ARCHIVE42)
ARCH = {rel(p): J(p) for p in sorted(glob.glob(REC + '/archive-verification*.json'))}
arch42 = [v for k, v in ARCH.items() if k.endswith(('source42.json', 'source42-pkg.json'))]
archives_ok = len(arch42) == 2 and all(a['verified'] and a['archiveSha256'] == EXPECT['archive42'] and a['manifestSha256'] == EXPECT['manifest42'] for a in arch42)
verified_manifest = bool(SV['manifest42']['matchesHeader'] and live42 == EXPECT['manifest42'] and SV['snapshot42']['verified'] and SV['counts42']['matchesHeader']
                         and SV['counts42']['matchesDeclared'] and archive42 == EXPECT['archive42'] and archives_ok)
parent41_ok = bool(SV['manifest41']['sha256'] == EXPECT['manifest41'] and SV['snapshot41']['verified'] and SV['parentChain']['42declares41'])
last40_ok = bool(SV['manifest40']['matchesHeader'] and SV['snapshot40']['verified'] and SV['parentChain']['41declares40'])
if not (verified_manifest and parent41_ok and last40_ok):
    GAPS.append('subject, parent41 or last-reviewed40 verification incomplete')
DELTA = SV['delta']
DCOUNTS = {k: DELTA[k]['counts'] for k in DELTA}
if (DCOUNTS['41to42']['changed'], DCOUNTS['41to42']['added'], DCOUNTS['41to42']['removed']) != (16, 1, 0) or \
        (DCOUNTS['40to42']['changed'], DCOUNTS['40to42']['added'], DCOUNTS['40to42']['removed']) != (16, 2, 0):
    GAPS.append('delta counts differ from measurement: ' + json.dumps(DCOUNTS))
paths41to42 = {r['path'] for k in ('changed', 'added', 'removed') for r in DELTA['41to42'][k]}
paths40to42 = {r['path'] for k in ('changed', 'added', 'removed') for r in DELTA['40to42'][k]}
paths40to41 = {r['path'] for k in ('changed', 'added', 'removed') for r in DELTA['40to41'][k]}
COPYVER = J(REC + '/copy-verification-final.json')
if not all(v['verified'] for v in COPYVER.values()):
    GAPS.append('a disposable copy changed during the review')

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


def group(kind):
    out = {}
    for r in ledger:
        if r['kind'] == kind:
            out.setdefault(r['path'], []).append(r)
    return out


fresh, ranged = [], []
for p, rows in sorted(group('fresh42Read').items()):
    cur, lines = sha(S42 + '/' + p), nlines(S42 + '/' + p)
    if any(r['sha256'] != cur for r in rows):
        GAPS.append('fresh read not current: ' + p)
    e = {'path': p, 'sha256': cur, 'lines': lines, 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows}),
         'changed40to42': p in paths40to42, 'changed41to42': p in paths41to42}
    if covers_all(e['ranges'], lines):
        e.update(readClass='fresh42Read', read='complete: every line read this charter')
        fresh.append(e)
    else:
        e.update(readClass='fresh42RangeRead', read='named ranges only; not a whole-file read')
        ranged.append(e)
fresh_paths = {e['path'] for e in fresh}
delta_reads = []
for kind, key in (('delta40to42Read', '40to42'), ('delta41to42Read', '41to42')):
    for p, rows in sorted(group(kind).items()):
        r = rows[-1]
        cur, dsha = sha(S42 + '/' + p), sha(RT + '/' + r['diff'])
        if cur != r['sha256'] or dsha != r['diffSha256']:
            GAPS.append('delta read not current: ' + p)
        delta_reads.append({'path': p, 'sha256': cur, 'lines': nlines(S42 + '/' + p), 'readClass': kind, 'read': 'complete %s diff; not a whole-file read' % key,
                            'alsoFreshWholeFileRead': p in fresh_paths, 'diffReceipt': r['diff'], 'diffSha256': dsha, 'note': r['note']})
evidence_reads = [{'path': p, 'sha256': sha(p), 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows})}
                  for p, rows in sorted(group('evidenceRead').items())]
delta_read_paths = {e['path'] for e in delta_reads}
byte_identical_to_fresh = {}
for p in sorted(paths40to42 | paths41to42):
    if p in fresh_paths or p in delta_read_paths:
        continue
    twins = [f for f in fresh_paths if sha(S42 + '/' + f) == sha(S42 + '/' + p)]
    if twins:
        byte_identical_to_fresh[p] = twins
uncovered = sorted((paths40to42 | paths41to42) - fresh_paths - delta_read_paths - set(byte_identical_to_fresh))
for p in uncovered:
    GAPS.append('delta file without read entry: ' + p)
V40 = J(V40PATH)
if sha(V40PATH) != EXPECT['review40']:
    GAPS.append('source40 review hash differs from header')
prior_complete = [dict(e, priorClass='fresh40Read') for e in V40['readScope']['fresh40Read']] + \
                 [dict(e, priorClass='inheritedUnchanged39Read') for e in V40['readScope']['inheritedUnchanged39Read']] + \
                 [dict(e, priorClass='complete39ReadPlusComplete40Diff') for e in V40['readScope']['complete39ReadPlusComplete40Diff']]
inherited, via_diff, changed_not = [], [], []
seen_prior = set()
for e in prior_complete:
    p = e['path']
    if p in fresh_paths or p in seen_prior:
        continue
    seen_prior.add(p)
    a, b = sha(S40 + '/' + p), sha(S42 + '/' + p)
    if a == b:
        inherited.append({'path': p, 'sha256': b, 'readClass': 'inheritedUnchanged40Read', 'priorClass': e['priorClass'],
                          'basis': 'counted as completely read by this origin\'s completed source40 review; byte-identical in source42 (hash recomputed now); not re-read this charter'})
    elif p in delta_read_paths:
        via_diff.append({'path': p, 'sha40': a, 'sha42': b, 'readClass': 'complete40ReadPlusComplete42Diff', 'priorClass': e['priorClass'],
                         'basis': 'source40 bytes counted as completely read plus the exact complete diff to source42; not a fresh whole-file read'})
    else:
        changed_not.append({'path': p, 'sha40': a, 'sha42': b, 'priorClass': e['priorClass']})
prior_ranges = [{'path': e['path'], 'ranges': e.get('ranges'), 'unchanged40to42': same(S40, S42, e['path']), 'readClass': 'prior40RangeReadOnly'}
                for e in V40['readScope']['fresh40RangeRead']]
SEARCH_ONLY = [
    {'path': 'docs/coop/design-corrections/foundation/check-enumeration.v1.py', 'lines': 'top-level definitions (search output)', 'standing': 'seen in search output only, beyond the ledgered range'},
    {'path': 'docs/coop/design-corrections/foundation/identity-schemas.v3.json', 'lines': '4729-4737, 4797-4799 closureKinds byField (search output)', 'standing': 'seen in search output only'},
    {'path': 'docs/coop/design-corrections/native/native_evidence_model.v2.py', 'lines': '2299, 2810-2851, 2939-2990, 3229-3231 binder and admit_native_context signatures (search output)', 'standing': 'signatures seen in search output only'},
]

# ------------------------------------------------------------------------------------------------ commands
G = J(REC + '/reference/groups-report.all.json')
group_rows = [{'name': r['name'], 'command': r['command'], 'exitCode': r['exitCode'], 'timedOut': r['timedOut'], 'seconds': r['seconds'],
               'scriptMatchesManifest': r['scriptMatchesManifest'], 'stdoutSha256': r['stdoutSha256'], 'copyAfter': summ(r['copyAfter']),
               'stdoutTail': r['stdoutTail'][-300:]} for r in G['rows']]
groups_ok = G['passed'] is True and len(group_rows) == 6 and all(r['exitCode'] == 0 and not r['timedOut'] and r['scriptMatchesManifest'] for r in group_rows) \
    and not any(G['after'].values())
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
        for k in ('failed', 'cases', 'mismatches', 'oracles', 'checks', 'results', 'rows'):
            if isinstance(d.get(k), (list, dict)):
                info[k + 'Count'] = len(d[k])
    except ValueError:
        info['nonJson'] = True
    children.setdefault(n, {}).update(info)
children_ok = len(ev3) == 17 and all(c.get('exitCode') == 0 for c in children.values())
if not children_ok or children['execution-inputs'].get('casesCount') != 95 or children['enumeration'].get('casesCount') != 54:
    GAPS.append('evaluator3 children or case populations not as measured')
FOUND = J(REC + '/reference/foundation.json')
foundation_checks = [{'script': os.path.basename(c['script']), 'exitCode': c['exitCode'], 'timedOut': c.get('timedOut')} for c in FOUND['checks']]
P = J(REC + '/planning-checks.json')
PC = P['counts']
planning_ok = (P['check_implementation_planning']['exitCode'] == 0 and P['check_repository_file_inventory']['exitCode'] == 0 and PC['coverageMappings'] == 322
               and PC['layerSha256']['11'] == EXPECT['v11'] and not PC['layerMismatchedAgainstSource42']['11'] and PC['coverageSubjectMatchesV11']
               and PC['planningSourcesArchitectureSha256MatchesV11'] and PC['inventoryPaths'] == 198 and PC['inventoryPackages'] == 20 and PC['recoveryCases'] == 54)
if not planning_ok:
    GAPS.append('planning checks or counts not as measured')
RC = J(REC + '/reference-comparison.json')
CASEPOP = J(REC + '/case-populations.json')
ENUMPOP = J(REC + '/enumeration-case-population.json')


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
                                 'stdout': rel(p[:-len('.run.json')] + '.stdout'), 'stderr': rel(p[:-len('.run.json')] + '.stderr'),
                                 'stderrSha256': sha(p[:-len('.run.json')] + '.stderr')} for p in runs[:-1]]}


def rows_of(name):
    return {r['case']: r for r in J(REC + '/probes/' + name)['rows']}


def probe_result(name):
    d = J(REC + '/probes/' + name)
    return {'receipt': 'receipts/probes/' + name, 'sha256': sha(REC + '/probes/' + name), 'rows': len(d['rows']), 'failedRows': [r['case'] for r in d['failed']],
            'observationRows': [r['case'] for r in d['rows'] if r.get('kind') in ('observation', 'source-text', 'record')]}


PROBE_DEFS = [
    ('P42-SUBJECT', 'probes/verify_subject42.py', None, ['subject-verification.json', 'manifest42-index.json'],
     'Formal manifest f602fc7e... and all 12,913 snapshot members (hash and length, none unlisted); parent41 manifest eb7a4c48... and all 12,912 members; last-reviewed40 manifest 3be45284... and all 12,911 members; declared chain 42->41->40; exact deltas 41->42 (16/1/0), 40->42 (16/2/0) and 40->41 (12/1/0).'),
    ('P42-ARCHIVE', 'probes/verify_archive_extract42.py', None, ['archive-verification.source42.json', 'archive-verification.source42-pkg.json'],
     'Archive 2423c780... hashed; every member verified and extracted into two disposable copies (groups copy work/source42, probe copy work/source42-pkg).'),
    ('P42-BASE-COPIES', 'probes/verify_archive_extract_base.py', None, ['archive-verification.base40.json', 'archive-verification.base41.json'],
     'Source40 (archive e9980bc4...) and source41 (archive c12aa7db..., members verified against manifest41) extracted into verified copies used only for old-versus-new discrimination.'),
    ('P42-DELTA', 'probes/make_delta_diffs42.py', None, ['delta-diff-summary.json'], 'Unified diffs for every changed file of the 41->42 and 40->42 deltas, both sides hash-verified.'),
    ('P42-GROUPS', 'probes/run_reference_groups42.py', None, ['reference/groups-report.all.json', 'reference/evaluator3.stdout', 'reference/foundation.json'],
     'Six pinned groups with /tmp/opensip-architecture-review-env/bin/python -I -B on the verified groups copy; copy re-verified after each group; 17 evaluator3 children.'),
    ('P42-REFERENCE-COMPARE', 'probes/compare_reference_v42.py', None, ['reference-comparison.json'],
     'This review\'s groups and children compared with the header-named codex final-reference.v42 and root-source42-final-reference.v3 receipts (evidence only).'),
    ('P42-COPIES-FINAL', 'probes/verify_base_copies.py', None, ['copy-verification-final.json'], 'All four disposable copies re-verified against their formal manifests after every probe and checker.'),
    ('P42-VIEW-ATTRIBUTION-X', 'probes/probe_view_attribution_x.py', 'view-attribution-x', 'view-attribution-x.json',
     'Independent discrimination source40 vs source41 vs source42, each tree\'s own owner modules in its own process: unsupported/foreign named-scope, same-universe and cross-target controls, split-scope re-encoding, unowned returned view (builder and explicit capture), census-only and refs-only views, reminted receipts, unselected row, foreign planId/producer observations, and the TypeScript semantic two-cell world (shared view, neither-cell view, row edits, reminted receipt), closed-run columns on the same manifest.'),
    ('P42-CAPTURE-JOINS', 'probes/probe_capture_joins_42.py', 'capture-joins-42', 'capture-joins-42.json',
     'Which owner refuses a captured unattributed view with a foreign planId and/or a non-provider producer on source42.'),
    ('P42-PROGRAM-ENTRY-X', 'probes/probe_program_entry_x.py', 'program-entry-x', 'program-entry-x.json',
     'Enumeration-owner admission source41 vs source42 over 24 programEntry x provenance x mode cases (TS, js-allowjs, js-synthesized, Rust, syntax, unavailable).'),
    ('P42-CASE-POPULATIONS', 'probes/compare_case_populations.py', 'case-populations', None,
     'Each tree\'s own check-execution-inputs (76/86/95) and check-enumeration run on the verified copies; shared cases compared field by field and full-run RunIds.'),
    ('P42-ENUMERATION-POPULATION', 'probes/compare_enumeration_receipts.py', 'enumeration-case-population', None, 'Enumeration receipts source41 vs source42: populations and shared-case identity.'),
    ('P42-PACKAGE19', 'probes/probe_package_v19.py', 'package-v19-evidence', 'package-v19.json',
     'Package v19 manifest, formal42 versus files-only projection, overlay provenance from package15, packages 16/17/18 preserved, content equality with root verification and rebuild, exact normalization-map negatives.'),
    ('P42-PLANNING', 'probes/run_planning_checks42.py', 'planning-checks', None, 'Planning and inventory checks (--check) plus v11/v10/v9/v8 layer and history recounts against source40/41.'),
    ('P42-PORTED-POLICY', 'probes/ported42_probe_policy_v40.py', 'ported-policy', 'policy-v40-on42.json', 'Ported source40 probe (expectations unedited): policy.test known-hit, universe tokens, imported universe, policy.show, identity preimages.'),
    ('P42-PORTED-NATIVE', 'probes/ported42_probe_native_v40.py', 'ported-native', 'native-v40-on42.json', 'Ported: U-1 effective allowJs, nested Cargo, unitKind full-Run closure.'),
    ('P42-PORTED-RUNTERM', 'probes/ported42_probe_runterm_adv_v40.py', 'ported-runterm-adv', 'runterm-adv-v40-on42.json', 'Ported: run-termination keys, commit-inventory recipe over a closed Run, registered-schema account.'),
    ('P42-PORTED-QUERY', 'probes/ported42_probe_query_carriers.py', 'query-carriers', 'query-carriers.json', 'Ported: nine command carriers, twenty operations, delivery law.'),
    ('P42-PORTED-CARRIER', 'probes/ported42_probe_carrier_readonly.py', 'carrier-readonly', 'carrier-readonly.json', 'Ported: read-only carrier scenarios on real SQLite.'),
    ('P42-PORTED-COMPARISON', 'probes/ported42_probe_comparison_knowledge.py', 'comparison-knowledge', 'comparison-knowledge.json', 'Ported: comparison presence knowledge.'),
    ('P42-PORTED-REPAIR2', 'probes/ported42_probe_repair2.py', 'repair2', 'repair2.json', 'Ported: repair:2 refusal order and retained-Run joins.'),
    ('P42-PORTED-TERM7', 'probes/ported42_probe_run_termination_s7.py', 'run-termination-s7', 'run-termination-s7.json', 'Ported: run-termination section 7 composition admission.'),
    ('P42-PORTED-CUSTODY', 'probes/ported42_probe_native_custody_fallback.py', 'native-custody-fallback', 'native-custody-fallback.json', 'Ported: pruned-tree custody and U-9 fallback.'),
]
PROBES, PBY = [], {}
for pid, script, runname, receipt, claim in PROBE_DEFS:
    e = {'id': pid, 'script': script, 'scriptSha256': sha(RT + '/' + script), 'claim': claim}
    if runname:
        e['execution'] = run_record(runname, RT + '/' + script)
        if receipt:
            e['result'] = probe_result(receipt)
            if e['result']['failedRows']:
                GAPS.append('probe has failed rows: ' + pid)
    else:
        e['receipts'] = {'receipts/' + r: sha(REC + '/' + r) for r in receipt}
    PROBES.append(e)
    PBY[pid] = e
PKG_RUNS = {'verify-package.py': run_record('package-v19-verify', PKG + '/verify-package.py'),
            'probe-native-v2.py': run_record('package-v19-probe-native-v2', PKG + '/probe-native-v2.py')}
VAX, CJ, PEX, PK = rows_of('view-attribution-x.json'), rows_of('capture-joins-42.json'), rows_of('program-entry-x.json'), rows_of('package-v19.json')
VAX_SIDES = {lab: J(REC + '/probes/view-attribution-x.side-' + lab + '.json') for lab in ('source40', 'source41', 'source42')}

# ------------------------------------------------------------------------------------------------ owner map
FD = 'docs/coop/design-corrections/foundation/'
MAP_FILES = [FD + 'execution-inputs-contract.v1.md', FD + 'execution-inputs.schema.v1.json', FD + 'execution_inputs_model.v1.py', FD + 'execution_inputs_fixture.v3.py',
             FD + 'check-execution-inputs.v1.py', FD + 'enumeration-contract.v1.md', FD + 'enumeration-plan.schema.v1.json', FD + 'enumeration_model.v1.py',
             FD + 'check-enumeration.v1.py', FD + 'evaluator_graph_fixture.v3.py', FD + 'evaluator_semantic_fixture.v3.py', FD + 'evaluator_input_model.v3.py',
             FD + 'identity-model.v3.py', FD + 'identity-schemas.v3.json', FD + 'evaluator-composition-contract.v3.md', FD + 'evaluator_replay_model.v3.py',
             FD + 'run-termination-contract.v1.md', FD + 'run_termination_model.v1.py',
             'docs/coop/design-corrections/native/native-capability-matrix.v2.json', 'docs/coop/design-corrections/native/native_evidence_model.v2.py',
             'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json', 'docs/coop/design-corrections/inherited-residuals.proposed.md',
             'docs/coop/design-corrections/current-source-map.proposed.md', 'docs/coop/design-corrections/qualification-gates.proposed.json',
             'docs/coop/design-corrections/security/carrier-dispatch.v3.json', 'docs/coop/design-corrections/public-detail-registry.v1.json',
             'docs/v2/architecture/08-decision-and-readiness-register.md', 'docs/v2/architecture/commit-recovery-readonly.v3.md',
             'docs/v2/architecture/prototype-report-inventory.md', 'docs/v2/architecture/repository-file-inventory.v1.json',
             'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md',
             'docs/v2/contracts/product-v1/security-and-lifecycle.md', 'docs/v2/contracts/product-v1/native-evidence.md',
             'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'docs/v2/contracts/product-v1/README.md']
MAP = {p: {'sha256': sha(S42 + '/' + p), 'unchanged40to42': same(S40, S42, p), 'unchanged41to42': same(S41, S42, p)} for p in MAP_FILES}
U = {os.path.basename(p): v['unchanged40to42'] for p, v in MAP.items()}
GATES = J(S42 + '/docs/coop/design-corrections/qualification-gates.proposed.json')['items']
gates_true = sum(1 for g in GATES if g.get('qualified') is True)
REG = open(S42 + '/docs/v2/architecture/08-decision-and-readiness-register.md', encoding='utf-8').read().splitlines()
cond2_ok = '28 existing rows' in ' '.join(REG[384:391])
if len(GATES) != 32 or gates_true != 0 or not cond2_ok:
    GAPS.append('gates or condition-2 measurement differs')

# ------------------------------------------------------------------------------------------------ author/root evidence
INTEG = {
    'view-attribution (source41 files)': [(S41, p, s) for p, s in ((FD + 'check-execution-inputs.v1.py', 'b1b5d4be7d0c9e240b258ec9345f4b36eda2d62197994b0e3be6adfda9629d1c'),
                                                                 (FD + 'execution-inputs-contract.v1.md', '64438ff18364eefc736e877fbce43b0d89e94eca17c41cacb79a08d25b8e7d70'),
                                                                 (FD + 'execution_inputs_fixture.v3.py', 'a94c971462c4e449d81eee5b1bd7a51c60b8b8b3c2e1b5cb88e32a7b2e13c8fa'),
                                                                 (FD + 'execution_inputs_model.v1.py', '5ea205090c1450a65fb14c29c2e02da7ef91be04baf67cb299fe67fd7bc96157'))],
    'capture (source42 files)': [(S42, p, s) for p, s in ((FD + 'check-execution-inputs.v1.py', 'e169fecb74e8000174f1cb4d88830d409c7d9c249d1ec080214c18415cde4e2d'),
                                                        (FD + 'execution-inputs-contract.v1.md', '8521f36217fb1499b93895789c392a6afd1a369db136afb8cd2c286d0735a2e1'),
                                                        (FD + 'execution_inputs_fixture.v3.py', 'd8c48fb5147887d04d875547ea450510a63106f1361de2711a48aa22d1070073'),
                                                        (FD + 'execution_inputs_model.v1.py', '66a15adddc7fed3d9209740da5ea0e2271e3b6c69236b73d4371f33aa6ab9ea1'),
                                                        (FD + 'evaluator_graph_fixture.v3.py', '36884a456704be3177471031335debf5066c1d9c78908b2dbeb40916f3ef5f4e'))],
    'program-entry clarification (source42)': [(S42, FD + 'enumeration-contract.v1.md', 'b7858bc8a70a41280bb6d7d1b461cc267ae22598b0dc851d4f1061bcbfa1bc59')],
    'program-entry enforcement (source42)': [(S42, FD + 'enumeration_model.v1.py', '69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85'),
                                             (S42, FD + 'check-enumeration.v1.py', 'bdeeb765e9ddbc293f8771af61274ed3da97bd9c1c52085b09611383a6728e41')],
}
INTEG_CHECK = {k: [{'path': p, 'recordedAfter': s, 'frozenBytes': sha(root + '/' + p), 'equal': sha(root + '/' + p) == s} for root, p, s in v] for k, v in INTEG.items()}
if not all(x['equal'] for v in INTEG_CHECK.values() for x in v):
    GAPS.append('a root integration after-image does not equal the frozen bytes')
# The planning-layer history clarification was integrated before the final v11 layer rebind, so its after-image is not the
# frozen file. Check what the clarification owns (the standing text) and that every later difference is the layer rebind.
_PLAN_ROOT = B + '/root-planning-layer-history-clarification.v1'
_after, _frozen = J(_PLAN_ROOT + '/after.json'), J(S42 + '/docs/v2/architecture/implementation-planning-sources.v1.json')
_changed = sorted(k for k in set(_after) | set(_frozen) if _after.get(k) != _frozen.get(k))
INTEG_CHECK['planning-layer history clarification (superseded by the later v11 layer rebind)'] = [{
    'path': 'docs/v2/architecture/implementation-planning-sources.v1.json',
    'rootBeforeSha256': sha(_PLAN_ROOT + '/before.json'), 'source41Sha256': sha(S41 + '/docs/v2/architecture/implementation-planning-sources.v1.json'),
    'rootAfterSha256': sha(_PLAN_ROOT + '/after.json'), 'frozen42Sha256': sha(S42 + '/docs/v2/architecture/implementation-planning-sources.v1.json'),
    'beforeEqualsSource41': sha(_PLAN_ROOT + '/before.json') == sha(S41 + '/docs/v2/architecture/implementation-planning-sources.v1.json'),
    'clarifiedStandingEqualInFrozen42': _after['standing'] == _frozen['standing'],
    'laterDifferencesOnlyLayerRebind': set(_changed) <= {'architecture', 'previousArchitectureInputLayer', 'priorArchitectureInputLayers'},
    'changedTopKeys': _changed,
    'diffReceipt': 'receipts/planning-clarification-after-to-source42.diff', 'diffSha256': sha(REC + '/planning-clarification-after-to-source42.diff')}]
_pc = INTEG_CHECK['planning-layer history clarification (superseded by the later v11 layer rebind)'][0]
if not (_pc['beforeEqualsSource41'] and _pc['clarifiedStandingEqualInFrozen42'] and _pc['laterDifferencesOnlyLayerRebind']):
    GAPS.append('planning-layer clarification not preserved in frozen source42')
AUTHOR_EVIDENCE = {k: {'path': p, 'sha256': sha(p), 'expected': w, 'equal': sha(p) == w, 'standing': 'bounded author proposal, not independent acceptance; read as evidence'} for k, (p, w) in AUTHOR.items()}
if not all(v['equal'] for v in AUTHOR_EVIDENCE.values()):
    GAPS.append('author proposal hash differs from header')
MV = J(RT + '/work/package-v19-verify/verification.json')
NV = J(RT + '/work/probe-native-v2.json')
vgroups = [{'group': g['group'], 'count': g.get('count'), 'passed': g.get('passed'), 'exitCode': g.get('exitCode')} for g in MV['groups']]
nm_controls = next(g['observed'] for g in MV['groups'] if g['group'] == 'normalization-map-controls1')
export_count = sum(g['count'] or 0 for g in vgroups if g['group'] != 'query')
query_count = next((g['count'] for g in vgroups if g['group'] == 'query'), None)
pkg_ok = (sha(PKG + '/artifact-manifest.json') == EXPECT['pkgManifest'] and all(v['ok'] for v in PK.values()) and export_count == 17 and query_count == 7
          and len(NV['runs']) == 9 and NV['passed'] is True and all(g['passed'] for g in vgroups))
if not pkg_ok:
    GAPS.append('package v19 verification not as recorded')
PACKAGE = {
    'package': PKG, 'artifactManifestSha256': sha(PKG + '/artifact-manifest.json'), 'expectedArtifactManifestSha256': EXPECT['pkgManifest'],
    'sourceBindingV42Sha256': sha(PKG + '/source-binding.v42.json'), 'expectedSourceBinding': EXPECT['sourceBinding'],
    'filesOnlySourceProjectionSha256': sha(PKG + '/source-manifest.json'), 'formalSubjectManifestSha256': live42,
    'rebuildReportSha256': sha(REBUILD), 'rootVerificationSha256': sha(ROOTVER),
    'historyPackageManifests': {v: sha(B + '/claude-author-package-successor.v%s/artifact-manifest.json' % v) for v in ('15', '16', '17', '18')},
    'probeRows': {k: {'ok': v['ok'], 'observed': v['observed']} for k, v in PK.items() if v.get('kind') != 'record'},
    'verificationGroups': vgroups, 'exports': export_count, 'queries': query_count, 'normalizationMapControls': nm_controls,
    'nativeV2Probe': {'runs': [r['name'] for r in NV['runs']], 'passed': NV['passed'], 'unitsVsDiscoveryDisagreements': NV['unitsVsDiscoveryDisagreements']},
    'toolRuns': PKG_RUNS, 'verified': pkg_ok,
    'result': ('Package v19 verified as author evidence. Every one of its 387 files matches artifact manifest 346a4d4b...; the formal42 manifest f602fc7e... and the files-only projection e732b21b... are different objects with equal file members; '
               'the rebuild base is package15 constructors (6a8d4fec...) plus the native-v2 migration overlay (overlay base digests match retained package15), not package16/17/18, which remain unchanged history; all 17 exports carry new RunIds and no historical export is relabelled. '
               'This review re-executed verify-package.py and probe-native-v2.py on its own verified copy: groups %s; %d exports and %d queries; three control groups exit 1 because their exported stores are refusing controls and the verifier records passed=true for every group. '
               'The verification and every compared output file are content-equal to the root final42 verification, and the 9 membership comparisons are content-equal to the root rebuild probe.'
               % (', '.join('%s %s (passed %s, exit %s)' % (g['group'], g['count'], g['passed'], g['exitCode']) for g in vgroups), export_count, query_count or 0)),
    'limits': ['Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.',
               'Four TypeScript normalization-map negatives ARE executed (exact refusals below). The Rust map negative is unexercised.',
               'The partial and/or/not consumer helper remains unexercised; count-at-most/all-covered remain unimplemented; two-binding qualification is incomplete.',
               'The binding-controls group now carries the explicit-selection and default-entry controls (ts-lawful-explicit-selection admits, ts-invalid-default-entry refuses ENUMERATION_BINDING_PROGRAM_ENTRY at semantic admission).',
               'No compiler, provider, OS or process-isolation qualification; independent grades granted: 0; all 30 author-proposed grades stay PENDING final application.'],
}
CODEXD, ROOT3D = J(CODEX), J(ROOTREF3)
EVIDENCE = {
    'standing': 'NONBLIND header-named evidence, not acceptance. No blind consumer artifact, result or implementation was read.',
    'records': [
        {'path': CODEX, 'sha256': sha(CODEX), 'expected': EXPECT['codex'], 'passed': CODEXD.get('passed'), 'subjectManifestSha256': CODEXD.get('subjectManifestSha256'),
         'note': 'current final42 reference receipts named by the header'},
        {'path': ROOTREF3, 'sha256': sha(ROOTREF3), 'passed': ROOT3D.get('passed'), 'note': 'actual final execution root-source42-final-reference.v3; codex runner-original equals it: %s' % RC['codexRunnerOriginalEqualsRootV3']},
        {'path': B + '/root-source42-final-reference.v2', 'used': False, 'note': 'environment launch failure per header; not used, not read'},
        {'path': B + '/root-source42-final-reference.v1', 'used': False, 'note': 'predates the final programEntry correction per header; not used, not read'},
        {'path': REBUILD, 'sha256': sha(REBUILD), 'expected': EXPECT['rebuild'], 'note': 'root reconstruction of package v19 from package15 plus overlay (author construction evidence)'},
        {'path': ROOTVER, 'sha256': sha(ROOTVER), 'expected': EXPECT['rootVerification'], 'note': 'root final42 verification; content-equal to this review\'s run'},
    ],
    'authorProposals': AUTHOR_EVIDENCE, 'rootIntegrationAfterImages': INTEG_CHECK,
}

for part in ('build_review42_findings.py', 'build_review42_rows.py', 'build_review42_emit.py'):
    path = RT + '/probes/' + part
    exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), globals())
