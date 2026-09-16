"""Build review.json and review.md for the independent source43 whole-design successor review.

Measurement part; then executes, in these globals, build_review43_findings.py (issues, observations, prior-finding dispositions,
items, scope basis), build_review43_rows.py (107 rows, TCB object, retained, authority, limitations) and build_review43_emit.py
(assembly, gap checks, rendering). Reads frozen source43/42 bytes, this origin's completed source42 review (read-only history),
header-named root/codex/package evidence, the source-only note and this runtime's receipts. Writes only RT/review.json and
RT/review.md. Hashes recomputed now."""
import glob, hashlib, json, os, re

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v43'
S43 = '/tmp/opensip-design-corrections/candidate-subject.v43'
S42 = '/tmp/opensip-design-corrections/candidate-subject.v42'
B = '/tmp/opensip-design-corrections'
REC = RT + '/receipts'
REVIEWS = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
LIVE43 = REVIEWS + '/candidate-subject.v43.json'
ARCHIVE43 = REVIEWS + '/candidate-source.v43.tar.gz'
LIVE42 = REVIEWS + '/candidate-subject.v42.json'
PKG = B + '/claude-author-package-successor.v20'
V42PATH = B + '/claude-independent-design.v42/review.json'
V42REC = B + '/claude-independent-design.v42/receipts'
CODEX = REVIEWS + '/codex-post-reset.v1/final-reference.v43/reference-checks.json'
ROOTREF = B + '/root-source43-final-reference.v1/reference-checks.json'
ROOTVER = B + '/author-package-final43-verification.v1/verification.json'
REBUILD = B + '/root-author-package-final43-rebuild.v1/rebuild-report.json'
FORMAL = B + '/root-author-package-formal43-binding.v1/binding.json'
NOTE = B + '/root-query43-independent-note.v1/note.json'
PLANVER = B + '/root-source43-planning-verification.v1/verification.json'
SRCBIND = PKG + '/source-binding.v43.json'
ORIGIN = '85a08aec-9d22-4ac6-8ec2-c10170e727d7'
EXPECT = {'manifest43': 'db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d',
          'manifest42': 'f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307',
          'archive43': 'd1ff8312d6a5540a977e54cfe8e24dd4865f8b09e6c432e42fd0d651387b66fa',
          'archive42': '2423c7807b489ef9af199f6eb4c44cc8a42b53160555621cf4b6a65d56fcb4c6',
          'pkgManifest': '803d1e1692c71dcede01efa0206fec68050c596a9c228b55123435dbdde4920b',
          'sourceBinding': '52ea8f8779015b5fdc0d4d3c36d39fe08c49c203fbb605be0000fff062041a47',
          'rootVerification': 'eb75f85a1f52fa53d4fd29e65f87719e5edcdb756f761aec9830e874c6034e2e',
          'codex': '213b81d0e17bc713a39e84941537935c33e5dc82283148cca915f994ea56aea7',
          'rebuild': '162bb26d47858db65cd9aaa5fe11dda743fff85538fbbd7701aa7459301f34d3',
          'formal': 'b1f0a831ed9a65248924cc97a2ba79107e760da324df650400d709bfb1a5f0c3',
          'note': 'c58100ef40f3f9703b4414a798073094cab25c704861d8b87682fb81396ecefb',
          'planningVerification': 'a232d5df4f38647e410e34e6c9d9c28a78c9dbc651ae2c07395c1458ee320a4f',
          'v11': '75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de',
          'review42': 'd677838bfbac3c3cea298461e36bd070073669566d354ed43dd413198b2ecb8a'}
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
live43, archive43 = sha(LIVE43), sha(ARCHIVE43)
ARCH = {rel(p): J(p) for p in sorted(glob.glob(REC + '/archive-verification*.json'))}
arch43 = [v for k, v in ARCH.items() if k.endswith(('source43.json', 'source43-pkg.json'))]
arch42 = [v for k, v in ARCH.items() if k.endswith('base42.json')]
archives_ok = len(arch43) == 2 and all(a['verified'] and a['archiveShaMatches'] and a['archiveSha256'] == EXPECT['archive43'] and a['manifestSha256'] == EXPECT['manifest43']
                                        and a['membersMatched'] == 12913 for a in arch43)
verified_manifest = bool(SV['manifest43']['matchesHeader'] and live43 == EXPECT['manifest43'] and SV['snapshot43']['verified'] and SV['counts43']['matchesHeader']
                         and SV['counts43']['matchesDeclared'] and archive43 == EXPECT['archive43'] and archives_ok)
parent42_ok = bool(SV['manifest42']['sha256'] == EXPECT['manifest42'] and sha(LIVE42) == EXPECT['manifest42'] and SV['snapshot42']['verified'] and SV['parentChain']['43declares42']
                   and len(arch42) == 1 and arch42[0]['verified'] and arch42[0]['archiveSha256'] == EXPECT['archive42'])
if not (verified_manifest and parent42_ok):
    GAPS.append('subject or parent42 verification incomplete')
DELTA = SV['delta']['42to43']
DCOUNTS = DELTA['counts']
if (DCOUNTS['changed'], DCOUNTS['added'], DCOUNTS['removed']) != (9, 0, 0):
    GAPS.append('delta counts differ from measurement: ' + json.dumps(DCOUNTS))
paths42to43 = {r['path'] for k in ('changed', 'added', 'removed') for r in DELTA[k]}
DIFFSUM = J(REC + '/delta-diff-summary.json')
COPYVER = J(REC + '/copy-verification-final.json')
if not (len(COPYVER) == 3 and all(v['verified'] for v in COPYVER.values())):
    GAPS.append('a disposable copy changed during the review or was not re-verified')
PINS = J(REC + '/source-pins43.json')
QUERY_OWNER_FILES = {'docs/coop/design-corrections/workflows/check-query-projection.v3.py', 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md',
                     'docs/coop/design-corrections/workflows/query_projection_model.v3.py'}
SIBLING_LEDGERS = {'docs/coop/design-corrections/foundation/source-pins.v1.json', 'docs/coop/design-corrections/native/source-pins.v2.json',
                   'docs/coop/design-corrections/security/source-pins.v1.json', 'docs/coop/design-corrections/workflows/source-pins.v1.json'}
pins_ok = PINS['allPinsMatch'] and set(PINS['changedPinUnion']) == QUERY_OWNER_FILES | SIBLING_LEDGERS and all(not v['addedVs42'] and not v['removedVs42'] for v in PINS['ledgers'].values())
if not pins_ok:
    GAPS.append('source pin verification not as measured')
if paths42to43 != QUERY_OWNER_FILES | SIBLING_LEDGERS | {'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json', 'docs/coop/design-corrections/workflows/workflows-report.v1.json'}:
    GAPS.append('delta population differs from the query owner files, pin ledgers and report')

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
for p, rows in sorted(group('fresh43Read').items()):
    cur, lines = sha(S43 + '/' + p), nlines(S43 + '/' + p)
    if any(r['sha256'] != cur for r in rows):
        GAPS.append('fresh read not current: ' + p)
    e = {'path': p, 'sha256': cur, 'lines': lines, 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows}), 'changed42to43': p in paths42to43}
    if covers_all(e['ranges'], lines):
        e.update(readClass='fresh43Read', read='complete: every line read this charter')
        fresh.append(e)
    else:
        e.update(readClass='fresh43RangeRead', read='named ranges only; not a whole-file read')
        ranged.append(e)
fresh_paths = {e['path'] for e in fresh}
delta_reads = []
for p, rows in sorted(group('delta42to43Read').items()):
    r = rows[-1]
    cur, dsha = sha(S43 + '/' + p), sha(RT + '/' + r['diff'])
    if cur != r['sha256'] or dsha != r['diffSha256']:
        GAPS.append('delta read not current: ' + p)
    delta_reads.append({'path': p, 'sha256': cur, 'lines': nlines(S43 + '/' + p), 'readClass': 'delta42to43Read', 'read': 'complete 42->43 diff; not a whole-file read',
                        'alsoFreshWholeFileRead': p in fresh_paths, 'diffReceipt': r['diff'], 'diffSha256': dsha, 'note': r['note']})
evidence_reads = [{'path': p, 'sha256': sha(p), 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows})} for p, rows in sorted(group('evidenceRead').items())]
delta_read_paths = {e['path'] for e in delta_reads}
uncovered = sorted(paths42to43 - fresh_paths - delta_read_paths)
for p in uncovered:
    GAPS.append('delta file without read entry: ' + p)
V42 = J(V42PATH)
if sha(V42PATH) != EXPECT['review42']:
    GAPS.append('source42 review hash differs from header')
RS42 = V42['readScope']
prior_complete = [dict(e, priorClass='fresh42Read') for e in RS42['fresh42Read']] + \
                 [dict(e, priorClass='inheritedUnchanged40Read') for e in RS42['inheritedUnchanged40Read']] + \
                 [dict(e, priorClass='complete40ReadPlusComplete42Diff') for e in RS42['complete40ReadPlusComplete42Diff']]
inherited, via_diff, changed_not = [], [], []
seen_prior = set()
for e in prior_complete:
    p = e['path']
    if p in fresh_paths or p in seen_prior:
        continue
    seen_prior.add(p)
    a, b = sha(S42 + '/' + p), sha(S43 + '/' + p)
    if a == b:
        inherited.append({'path': p, 'sha256': b, 'readClass': 'inheritedUnchanged42Read', 'priorClass': e['priorClass'],
                          'basis': 'counted as completely read by this origin\'s completed source42 review; byte-identical in source43 (hash recomputed now); not re-read this charter'})
    elif p in delta_read_paths:
        via_diff.append({'path': p, 'sha42': a, 'sha43': b, 'readClass': 'complete42ReadPlusComplete43Diff', 'priorClass': e['priorClass'],
                         'basis': 'source42 bytes counted as completely read plus the exact complete diff to source43; not a fresh whole-file read'})
    else:
        changed_not.append({'path': p, 'sha42': a, 'sha43': b, 'priorClass': e['priorClass']})
if changed_not:
    GAPS.append('a prior complete read changed without a current read: %s' % [c['path'] for c in changed_not])
prior_ranges = [{'path': e['path'], 'ranges': e.get('ranges'), 'unchanged42to43': same(S42, S43, e['path']), 'readClass': 'prior42RangeReadOnly'} for e in RS42['fresh42RangeRead']]
SEARCH_ONLY = [
    {'path': 'docs/coop/design-corrections/workflows/query_projection_model.v3.py', 'lines': 'top-level def/class lines 128-259, 371-564, 713-1111 (function map in search output)', 'standing': 'signatures seen in search output only, outside the ledgered ranges'},
    {'path': 'docs/coop/design-corrections/workflows/query_surface_projection.v3.py', 'lines': '507, 572, 742, 903 (availability search output) and 431-454, 595-751 renderer call sites', 'standing': 'seen in search output only, outside the ledgered ranges'},
    {'path': 'docs/coop/design-corrections/workflows/check-query-projection.v3.py', 'lines': '223-227, 869 (graph.path search output)', 'standing': 'seen in search output only'},
    {'path': 'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json', 'lines': '90-111, 160-261, 262-280, 293, 311, 355-391, 429, 470, 495-510, 754-779, 797-803, 871, 960-961, 1120, 1133 (search output)', 'standing': 'seen in search output only, outside the ledgered ranges'},
    {'path': 'docs/coop/design-corrections/workflows/schemas/graph-query.schema.json', 'lines': '78 (operation name in search output)', 'standing': 'historical non-evaluator3 schema; one line seen in search output'},
    {'path': 'docs/v2/contracts/product-v1/identity-and-evidence.md', 'lines': '878, 1184, 1465, 1473, 1483, 1524, 1672 (search output)', 'standing': 'seen in search output only'},
    {'path': 'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'lines': '408, 446-447, 706, 925, 1273, 1302-1303, 1325, 1637 (search output)', 'standing': 'seen in search output only, outside the ledgered ranges'},
    {'path': 'docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py', 'lines': '287, 300, 510-517, 598, 606, 613, 800-801 (search output)', 'standing': 'fixture keys seen in search output only'},
    {'path': 'docs/coop/design-corrections/workflows/command-inventory.v3.json', 'lines': '2-5, 368, 1634, 1678, 1745 (search output)', 'standing': 'seen in search output only'},
    {'path': 'docs/coop/design-corrections/workflows/schemas/evaluator3/{command-inventory,comparison-result,invocation-record,repair,review,sarif-adapter}.schema.json', 'lines': 'note/remedy property lines (search output)', 'standing': 'seen in search output only'},
    {'path': 'docs/v2/architecture/{implementation-boundaries-and-build-plan.md,14-repository-and-module-layout.md,implementation-coverage.v1.json}', 'lines': 'crates/host/src/analysis.rs and graph.path occurrences (search output)', 'standing': 'seen in search output only'},
    {'path': 'docs/coop/hydradb-review/hydradb-opensip-fit-gap.md', 'lines': '31 (graph.path search output, line omitted as too long)', 'standing': 'non-normative review note; file name only'},
    {'path': 'docs/coop/design-corrections/reviews/** inside the frozen snapshot (including consumer-b.v1-v8 subject copies and tool-calls, bv3-bv6 corrections-author copies, grok-* query reviews, query-successor-root-review.v1-v3, v20-advisory-assessment, hydradb-proposal-assessment)',
     'lines': 'file names and single matching lines surfaced by two broad content searches over docs/ before the searches were restricted with !**/reviews/**', 'standing': 'UNINTENDED search-output sightings of snapshot-internal historical review copies; no such file was opened or read and nothing from them is used; all later searches excluded reviews/**'},
]

# ------------------------------------------------------------------------------------------------ commands
G = J(REC + '/reference/groups-report.all.json')
group_rows = [{'name': r['name'], 'command': r['command'], 'exitCode': r['exitCode'], 'timedOut': r['timedOut'], 'seconds': r['seconds'],
               'scriptMatchesManifest': r['scriptMatchesManifest'], 'stdoutSha256': r['stdoutSha256'], 'copyAfter': summ(r['copyAfter']),
               'stdoutTail': r['stdoutTail'][-300:]} for r in G['rows']]
groups_ok = G['passed'] is True and len(group_rows) == 6 and all(r['exitCode'] == 0 and not r['timedOut'] and r['scriptMatchesManifest'] for r in group_rows) \
    and not any(G['after'].values()) and not any(G['before'].values())
if not groups_ok:
    GAPS.append('reference groups not all passing')
ev3 = re.findall(r'^(\S+) (\d+)[ \t]*$', open(REC + '/reference/evaluator3.stdout').read(), re.M)
children = {n: {'exitCode': int(c)} for n, c in ev3}
for f in sorted(glob.glob(REC + '/reference/evaluator3/*.stdout')):
    n = os.path.basename(f)[:-7]
    info = {'stdoutSha256': sha(f)}
    try:
        d = J(f)
        for k in ('passed', 'ok', 'count', 'total'):
            if k in d and not isinstance(d[k], (dict, list)):
                info[k] = d[k]
        for k in ('failed', 'cases', 'mismatches', 'checks'):
            if isinstance(d.get(k), (list, dict)):
                info[k + 'Count'] = len(d[k])
    except ValueError:
        info['nonJson'] = True
    children.setdefault(n, {}).update(info)
children_ok = len(ev3) == 17 and len(children) == 17 and all(c.get('exitCode') == 0 for c in children.values())
if not children_ok or children['execution-inputs'].get('casesCount') != 95 or children['enumeration'].get('casesCount') != 54 \
        or children['query-projection'].get('checksCount') != 209 or children['query-projection'].get('failedCount') != 0:
    GAPS.append('evaluator3 children or populations not as measured')
FOUND = J(REC + '/reference/foundation.json')
foundation_checks = [{'script': os.path.basename(c['script']), 'exitCode': c['exitCode'], 'timedOut': c.get('timedOut')} for c in FOUND['checks']]
P = J(REC + '/planning-checks.json')
PC = P['counts']
planning_ok = (P['check_implementation_planning']['exitCode'] == 0 and P['check_repository_file_inventory']['exitCode'] == 0 and PC['coverageMappings'] == 322
               and PC['coverageMappingsSource42'] == 322 and PC['layerSha256']['11'] == EXPECT['v11'] and not PC['layerMismatchedAgainstSource43']['11']
               and PC['layerInputs']['11'] == 31 and all(PC['layersByteEqualToSource42'].values()) and PC['v11InputsIntersectingThe9ChangedFiles'] == []
               and PC['coverageSourcesIntersectingThe9ChangedFiles'] == [] and PC['coverageSourcesStale'] == [] and PC['coverageRowsChangedVs42'] == []
               and PC['coverageSubjectMatchesV11'] and PC['planningSourcesArchitectureSha256MatchesV11'] and PC['planningSourcesArchitectureFilesEqualV11']
               and PC['inventoryPaths'] == 198 and PC['inventoryPackages'] == 20 and PC['recoveryCases'] == 54 and PC['recoveryCasesNotExecuted'] == 54
               and PC['coverageGroups']['reportFeatures'] == 24 and PC['milestoneOrder'] == ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6']
               and PC['architectureDirFilesByteEqualToSource42'])
if not planning_ok:
    GAPS.append('planning checks or counts not as measured')
RC = J(REC + '/reference-comparison.json')
RCS = J(REC + '/reference-children-stripped.json')
reference_ok = (RC['codexReferenceChecks']['sha256'] == EXPECT['codex'] and RC['codexPassed'] and RC['codexSubjectManifestSha256'] == EXPECT['manifest43'] and RC['rootPassed']
                and all(v['stdoutFileEqualRoot'] and v['stdoutShaEqualRootRecord'] and v['rootSourceShaEqualsMineScript'] and v['stdoutFileEqualCodex'] for v in RC['groups'].values())
                and RC['childCount'] == 17 and RC['childrenEqualRoot'] == 15 and RCS['codexRunnerOriginalEqualsRoot']
                and all(RCS[n]['root']['equalAfterStrippingPathFieldsOnly'] and RCS[n]['historicalMine42']['equalAfterStrippingPathFieldsOnly'] for n in ('enumeration.stdout', 'execution-inputs.stdout'))
                and RCS['query-projection.stdout']['root']['byteEqual'] and RCS['query-projection.stdout']['checkCount'] == 209 and RCS['query-projection.stdout']['checkCountHistorical42'] == 204
                and not RCS['query-projection.stdout']['checkIdsRemovedVs42'] and len(RCS['query-projection.stdout']['checkIdsAddedVs42']) == 5)
if not reference_ok:
    GAPS.append('reference comparison not as measured')


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


PORTED = [('P43-PORTED-POLICY', 'probes/ported43_probe_policy_v40.py', 'ported-policy', 'policy-v40-on43.json', 'policy-v40-on42.json',
           'Ported (expectations unedited): policy.test known-hit, universe tokens, imported universe, policy.show, identity preimages.'),
          ('P43-PORTED-NATIVE', 'probes/ported43_probe_native_v40.py', 'ported-native', 'native-v40-on43.json', 'native-v40-on42.json', 'Ported: U-1 effective allowJs, nested Cargo, unitKind full-Run closure.'),
          ('P43-PORTED-RUNTERM', 'probes/ported43_probe_runterm_adv_v40.py', 'ported-runterm-adv', 'runterm-adv-v40-on43.json', 'runterm-adv-v40-on42.json',
           'Ported: run-termination keys, commit-inventory recipe over a closed Run, registered-schema account.'),
          ('P43-PORTED-QUERY', 'probes/ported43_probe_query_carriers.py', 'query-carriers', 'query-carriers.json', 'query-carriers.json', 'Ported: nine command carriers, twenty operations, delivery law.'),
          ('P43-PORTED-CARRIER', 'probes/ported43_probe_carrier_readonly.py', 'carrier-readonly', 'carrier-readonly.json', 'carrier-readonly.json', 'Ported: read-only carrier scenarios on real SQLite.'),
          ('P43-PORTED-COMPARISON', 'probes/ported43_probe_comparison_knowledge.py', 'comparison-knowledge', 'comparison-knowledge.json', 'comparison-knowledge.json', 'Ported: comparison presence knowledge.'),
          ('P43-PORTED-REPAIR2', 'probes/ported43_probe_repair2.py', 'repair2', 'repair2.json', 'repair2.json', 'Ported: repair:2 refusal order and retained-Run joins.'),
          ('P43-PORTED-TERM7', 'probes/ported43_probe_run_termination_s7.py', 'run-termination-s7', 'run-termination-s7.json', 'run-termination-s7.json', 'Ported: run-termination section 7 composition admission.'),
          ('P43-PORTED-CUSTODY', 'probes/ported43_probe_native_custody_fallback.py', 'native-custody-fallback', 'native-custody-fallback.json', 'native-custody-fallback.json', 'Ported: pruned-tree custody and U-9 fallback.'),
          ('P43-PORTED-CAPTURE-JOINS', 'probes/ported43_probe_capture_joins.py', 'capture-joins-on43', 'capture-joins-on43.json', 'capture-joins-42.json',
           'Ported source42 ADV42-01 measurement: which owner refuses a captured unattributed view with a foreign planId and/or a non-provider producer.')]
PROBE_DEFS = [
    ('P43-SUBJECT', 'probes/verify_subject43.py', None, ['subject-verification.json', 'manifest43-index.json'],
     'Formal manifest db43ee76... and all 12,913 snapshot members (hash and length, none unlisted); parent42 manifest f602fc7e... and all 12,913 members; declared chain 43->42; exact delta 42->43 (9/0/0).'),
    ('P43-ARCHIVE', 'probes/verify_archive_extract43.py', None, ['archive-verification.source43.json', 'archive-verification.source43-pkg.json', 'archive-verification.base42.json'],
     'Archive d1ff8312... hashed; every member verified and extracted into two disposable copies (groups copy work/source43, probe copy work/source43-pkg); archive42 2423c780... into work/base42 for old-versus-new discrimination.'),
    ('P43-DELTA', 'probes/make_delta_diffs43.py', None, ['delta-diff-summary.json'], 'Unified diffs for every changed file of the 42->43 delta, both sides hash-verified.'),
    ('P43-GROUPS', 'probes/run_reference_groups43.py', None, ['reference/groups-report.all.json', 'reference/evaluator3.stdout', 'reference/foundation.json'],
     'Six pinned groups with /tmp/opensip-architecture-review-env/bin/python -I -B on the verified groups copy; copy re-verified before and after each group; 17 evaluator3 children.'),
    ('P43-REFERENCE-COMPARE', 'probes/compare_reference_v43.py', 'reference-comparison-v43', None,
     'This review\'s groups and children compared with root-source43-final-reference.v1, codex final-reference.v43 and this origin\'s historical source42 receipts (evidence only).'),
    ('P43-REFERENCE-CHILDREN', 'probes/compare_children_stripped43.py', 'reference-children-stripped', None,
     'Key-level difference of the non-byte-equal children (enumeration, execution-inputs) and query-projection check-id population versus root and historical source42.'),
    ('P43-PINS', 'probes/verify_pins43.py', 'source-pins43', None, 'Every entry of the five source-pin ledgers against the formal manifest; changed pins versus source42.'),
    ('P43-PLANNING', 'probes/run_planning_checks43.py', 'planning-checks-v43', None, 'Planning and inventory checks (--check) plus v11/v10/v9/v8 layer, coverage and history recounts against the exact parent source42.'),
    ('P43-QUERY-X', 'probes/probe_query43_x.py', 'query43-x', 'query43-x.json',
     'Independent discrimination source42 vs source43 on one lawful closed Run, each tree\'s own query/fixture/replay/surface modules in its own process: availability omitted/retained/partial on neighbors/path/reach, every refusing state, invalid observations, missing and corrupt bytes under each observation, public refusal routes with a partial observation, trusted latest and snapshot joins, same-host cursor continuation (cache loss/poison, latest re-resolve, other Run, changed params, position, malformed), bound admission, path hop orientation on the Run and tie/order/zero-hop/depth goldens, graph-query-response parity and renderers.'),
    ('P43-QUERY-ADAPTER-X', 'probes/probe_query_adapter43_x.py', 'query-adapter43-x', 'query-adapter43-x.json',
     'Independent discrimination source42 vs source43 of the reference adapter path: retained availability record -> admitted state -> observation -> response availability; failing records; partial record with corrupt/missing bytes; adapter invalid observation route; RequestId precondition.'),
    ('P43-QUERY-PROSE', 'probes/probe_query_prose43.py', 'query-prose43', 'query-prose43.json',
     'Limitation-note and refusal-diagnostic prose law on source43: free BoundedText wording keeps admission and parity, over-long note refused, success termination branch, diagnostic private, remedy never selects the route.'),
    ('P43-PORT', 'probes/port_v42_probes43.py', None, ['probe-port43.json'], 'Mechanical port of the source42 scope probes: runtime paths and receipt names only; residual source42 runtime mentions none.'),
] + [(pid, script, runname, receipt, claim) for pid, script, runname, receipt, _, claim in PORTED] + [
    ('P43-PACKAGE20', 'probes/probe_package_v20.py', 'package-v20-evidence', 'package-v20.json',
     'Package v20 manifest, formal43 versus files-only projection, overlay provenance from package15, packages 16-19 preserved, export stores byte-equal to package19, content equality with root verification and rebuild, exact normalization-map negatives.'),
    ('P43-COPIES-FINAL', 'probes/verify_copies43.py', 'copies-final', None, 'All three disposable copies re-verified against their formal manifests after every probe and checker.'),
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
PORTED_EQUAL = {}
for pid, _, _, receipt, receipt42, _ in PORTED:
    cur, old = rows_of(receipt), {r['case']: r for r in J(V42REC + '/probes/' + receipt42)['rows']}
    differ = [c for c in cur if c in old and json.dumps(cur[c]['observed'], sort_keys=True) != json.dumps(old[c]['observed'], sort_keys=True)]
    PORTED_EQUAL[pid] = {'rows': len(cur), 'sameCaseSetAsSource42': set(cur) == set(old), 'observedDifferFromSource42': differ, 'historicalReceipt42': 'claude-independent-design.v42/receipts/probes/' + receipt42}
    if differ or set(cur) != set(old):
        GAPS.append('ported probe observations differ from source42: ' + pid)
PORT = J(REC + '/probe-port43.json')
if any(r['residualV42RuntimeMentions'] for r in PORT):
    GAPS.append('ported probe still names the source42 runtime')
PKG_RUNS = {'verify-package.py': run_record('package-v20-verify', PKG + '/verify-package.py'),
            'probe-native-v2.py': run_record('package-v20-probe-native-v2', PKG + '/probe-native-v2.py')}
Q43X, QAX, QPR, PK, CJ = rows_of('query43-x.json'), rows_of('query-adapter43-x.json'), rows_of('query-prose43.json'), rows_of('package-v20.json'), rows_of('capture-joins-on43.json')
QSIDES = {lab: J(REC + '/probes/query43-x.side-' + lab + '.json') for lab in ('source42', 'source43')}

# ------------------------------------------------------------------------------------------------ owner map
FD = 'docs/coop/design-corrections/foundation/'
WFD = 'docs/coop/design-corrections/workflows/'
MAP_FILES = [WFD + 'query-projection-contract.v3.md', WFD + 'query_projection_model.v3.py', WFD + 'check-query-projection.v3.py', WFD + 'query_surface_projection.v3.py',
             WFD + 'schemas/evaluator3/graph-query.schema.json', WFD + 'schemas/evaluator3/common.schema.json', WFD + 'schemas/evaluator3/command-envelope.schema.json',
             WFD + 'command-inventory.v3.json', WFD + 'workflows-report.v1.json', WFD + 'source-pins.v1.json', FD + 'source-pins.v1.json', FD + 'evaluator3-source-pins.v1.json',
             'docs/coop/design-corrections/native/source-pins.v2.json', 'docs/coop/design-corrections/security/source-pins.v1.json',
             FD + 'execution-inputs-contract.v1.md', FD + 'execution-inputs.schema.v1.json', FD + 'execution_inputs_model.v1.py', FD + 'execution_inputs_fixture.v3.py',
             FD + 'check-execution-inputs.v1.py', FD + 'enumeration-contract.v1.md', FD + 'enumeration-plan.schema.v1.json', FD + 'enumeration_model.v1.py',
             FD + 'check-enumeration.v1.py', FD + 'evaluator_graph_fixture.v3.py', FD + 'evaluator_semantic_fixture.v3.py', FD + 'evaluator_input_model.v3.py',
             FD + 'identity-model.v3.py', FD + 'identity-schemas.v3.json', FD + 'evaluator-composition-contract.v3.md', FD + 'evaluator_replay_model.v3.py',
             FD + 'run-termination-contract.v1.md', FD + 'run_termination_model.v1.py', FD + 'canonical.py',
             'docs/coop/design-corrections/native/native-capability-matrix.v2.json', 'docs/coop/design-corrections/native/native_evidence_model.v2.py',
             'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
             'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json', 'docs/coop/design-corrections/inherited-residuals.proposed.md',
             'docs/coop/design-corrections/current-source-map.proposed.md', 'docs/coop/design-corrections/qualification-gates.proposed.json',
             'docs/coop/design-corrections/security/carrier-dispatch.v3.json', 'docs/coop/design-corrections/public-detail-registry.v1.json',
             WFD + 'policy_test_model.v3.py', WFD + 'repair_closed_world_selection.v1.py',
             'docs/v2/architecture/08-decision-and-readiness-register.md', 'docs/v2/architecture/commit-recovery-readonly.v3.md',
             'docs/v2/architecture/prototype-report-inventory.md', 'docs/v2/architecture/repository-file-inventory.v1.json', 'docs/v2/architecture/implementation-coverage.v1.json',
             'docs/v2/architecture/implementation-planning-sources.v1.json', 'docs/v2/architecture/implementation-normative-inputs.v11.json',
             'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md',
             'docs/v2/contracts/product-v1/security-and-lifecycle.md', 'docs/v2/contracts/product-v1/native-evidence.md',
             'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'docs/v2/contracts/product-v1/README.md']
MAP = {p: {'sha256': sha(S43 + '/' + p), 'unchanged42to43': same(S42, S43, p), 'inDelta': p in paths42to43} for p in MAP_FILES}
for p, v in MAP.items():
    if v['unchanged42to43'] == v['inDelta']:
        GAPS.append('map/delta disagreement: ' + p)
U = {os.path.basename(p): v['unchanged42to43'] for p, v in MAP.items() if not p.endswith('source-pins.v1.json')}
GATES = J(S43 + '/docs/coop/design-corrections/qualification-gates.proposed.json')['items']
gates_true = sum(1 for g in GATES if g.get('qualified') is True)
REG = open(S43 + '/docs/v2/architecture/08-decision-and-readiness-register.md', encoding='utf-8').read().splitlines()
cond2_ok = '28 existing rows' in ' '.join(REG[384:391])
if len(GATES) != 32 or gates_true != 0 or not cond2_ok:
    GAPS.append('gates or condition-2 measurement differs')
COV = J(S43 + '/docs/v2/architecture/implementation-coverage.v1.json')
GRAPH_COVERAGE_ROWS = [r for r in COV['groups']['queryOperations'] if r.get('id') in ('graph.neighbors', 'graph.path', 'graph.reach')]

# ------------------------------------------------------------------------------------------------ root/package evidence
NOTED = J(NOTE)
PV = J(PLANVER)
MV = J(RT + '/work/package-v20-verify/verification.json')
NV = J(RT + '/work/probe-native-v2.json')
FB = J(FORMAL)
vgroups = [{'group': g['group'], 'count': g.get('count'), 'passed': g.get('passed'), 'exitCode': g.get('exitCode')} for g in MV['groups']]
nm_controls = next(g['observed'] for g in MV['groups'] if g['group'] == 'normalization-map-controls1')
export_count = sum(g['count'] or 0 for g in vgroups if g['group'] != 'query')
query_count = next((g['count'] for g in vgroups if g['group'] == 'query'), None)
pkg_ok = (sha(PKG + '/artifact-manifest.json') == EXPECT['pkgManifest'] and all(v['ok'] for v in PK.values()) and export_count == 17 and query_count == 7
          and len(NV['runs']) == 9 and NV['passed'] is True and all(g['passed'] for g in vgroups) and sha(SRCBIND) == EXPECT['sourceBinding'] and sha(FORMAL) == EXPECT['formal'])
if not pkg_ok:
    GAPS.append('package v20 verification not as recorded')
PACKAGE = {
    'package': PKG, 'artifactManifestSha256': sha(PKG + '/artifact-manifest.json'), 'expectedArtifactManifestSha256': EXPECT['pkgManifest'],
    'sourceBindingV43Sha256': sha(SRCBIND), 'expectedSourceBinding': EXPECT['sourceBinding'],
    'filesOnlySourceProjectionSha256': sha(PKG + '/source-manifest.json'), 'formalSubjectManifestSha256': live43,
    'rebuildReportSha256': sha(REBUILD), 'rootVerificationSha256': sha(ROOTVER), 'formalBindingSha256': sha(FORMAL),
    'historyPackageManifests': {v: sha(B + '/claude-author-package-successor.v%s/artifact-manifest.json' % v) for v in ('15', '16', '17', '18', '19')},
    'probeRows': {k: {'ok': v['ok'], 'observed': v['observed']} for k, v in PK.items() if v.get('kind') != 'record'},
    'verificationGroups': vgroups, 'exports': export_count, 'queries': query_count, 'normalizationMapControls': nm_controls,
    'nativeV2Probe': {'runs': [r['name'] for r in NV['runs']], 'passed': NV['passed'], 'unitsVsDiscoveryDisagreements': NV['unitsVsDiscoveryDisagreements']},
    'formalBindingSource42Comparison': {'rows': len(FB['source42Comparison']), 'allSameRunIdAndBytes': all(c['sameRunId'] and c['sameExportBytes'] for c in FB['source42Comparison'])},
    'toolRuns': PKG_RUNS, 'verified': pkg_ok,
    'result': ('Package v20 verified as author evidence. All %d files match artifact manifest 803d1e16...; the formal43 manifest db43ee76... and the files-only projection d7f43243... are different objects with equal file members, and the package copy of the formal manifest equals the live one. '
               'The rebuild base is package15 constructors (6a8d4fec...) plus the native-v2 migration overlay (overlay base digests match retained package15); packages 16, 17, 18 and 19 remain unchanged history. '
               'Every current export store is byte-equal to package19 at the same path, so the byte-derived RunIds are unchanged and nothing was reminted; the root formal binding records all 17 source42 comparisons as same RunId and same export bytes. '
               'This review re-executed verify-package.py and probe-native-v2.py on its own verified source43 copy: groups %s; %d exports and %d queries; the verification and every compared output file are content-equal to the root final43 verification, and the 9 membership comparisons are content-equal to the root rebuild probe.'
               % (len(J(PKG + '/artifact-manifest.json')['files']), ', '.join('%s %s (passed %s, exit %s)' % (g['group'], g['count'], g['passed'], g['exitCode']) for g in vgroups), export_count, query_count or 0)),
    'limits': ['Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.',
               'Four TypeScript normalization-map negatives ARE executed (exact refusals below). The Rust map negative is unexercised.',
               'The partial and/or/not consumer helper remains unexercised; count-at-most/all-covered remain unimplemented; two-binding qualification is incomplete.',
               'No compiler, provider, OS or process-isolation qualification; independent grades granted: 0; all 30 author-proposed grades stay PENDING final application.'],
}
CODEXD, ROOTD = J(CODEX), J(ROOTREF)
planning_stdout_equal_root = PV.get('stdoutSha256') == P['check_implementation_planning']['stdoutSha256']
EVIDENCE = {
    'standing': 'NONBLIND header-named evidence, not acceptance. No blind consumer artifact, export, helper, review or root blind outcome was read; the query-author runtime and reports were not read.',
    'records': [
        {'path': NOTE, 'sha256': sha(NOTE), 'expected': EXPECT['note'], 'note': 'source-only technical note supplied in place of author material; read completely; its control counts (old 204, new 209) and planning counts were re-measured here, not adopted'},
        {'path': CODEX, 'sha256': sha(CODEX), 'expected': EXPECT['codex'], 'passed': CODEXD.get('passed'), 'subjectManifestSha256': CODEXD.get('subjectManifestSha256'),
         'note': 'current final43 reference receipts named by the header; runner-original equals the root reference-checks: %s' % RCS['codexRunnerOriginalEqualsRoot']},
        {'path': ROOTREF, 'sha256': sha(ROOTREF), 'passed': ROOTD.get('passed'), 'executionSourceRoots': RC['rootExecutionSourceRoots'],
         'note': 'actual root execution root-source43-final-reference.v1 (6 groups, 17 children); executed from a pre-freeze working tree whose script bytes equal the frozen source43 bytes'},
        {'path': PLANVER, 'sha256': sha(PLANVER), 'expected': EXPECT['planningVerification'], 'stdoutSha256EqualsThisReview': planning_stdout_equal_root,
         'note': 'root planning verification; its recorded prior attempt (exit 2, missing --source) is preserved there and not counted'},
        {'path': REBUILD, 'sha256': sha(REBUILD), 'expected': EXPECT['rebuild'], 'note': 'root reconstruction of package v20 from package15 plus overlay (author construction evidence)'},
        {'path': ROOTVER, 'sha256': sha(ROOTVER), 'expected': EXPECT['rootVerification'], 'note': 'root final43 verification; content-equal to this review\'s run'},
        {'path': FORMAL, 'sha256': sha(FORMAL), 'expected': EXPECT['formal'], 'note': 'root formal43 metadata binding and measured source42 comparison'},
        {'path': SRCBIND, 'sha256': sha(SRCBIND), 'expected': EXPECT['sourceBinding'], 'note': 'package 20 source binding'},
    ],
}
for r in EVIDENCE['records']:
    if r.get('expected') and r['sha256'] != r['expected']:
        GAPS.append('evidence hash differs from header: ' + r['path'])

for part in ('build_review43_findings.py', 'build_review43_rows.py', 'build_review43_emit.py'):
    path = RT + '/probes/' + part
    exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), globals())
