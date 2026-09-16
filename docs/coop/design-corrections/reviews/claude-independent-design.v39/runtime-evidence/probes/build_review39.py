"""Build review.json and review.md for the independent source39 design review.

Reads frozen source39/38 bytes, the retained source38 review, root/author evidence and this runtime's own receipts.
Writes only RT/review.json and RT/review.md. Every hash is recomputed here at build time.
"""
import glob
import hashlib
import json
import os
import re

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'
S39 = '/tmp/opensip-design-corrections/candidate-subject.v39'
S38 = '/tmp/opensip-design-corrections/candidate-subject.v38'
B = '/tmp/opensip-design-corrections'
REC = RT + '/receipts'
REVIEWS = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
LIVE39 = REVIEWS + '/candidate-subject.v39.json'
LIVE38 = REVIEWS + '/candidate-subject.v38.json'
ARCHIVE39 = REVIEWS + '/candidate-source.v39.tar.gz'
PKG = B + '/claude-author-package-successor.v16'
V38PATH = B + '/claude-independent-design.v38/review.json'
EXPECT = {'manifest39': 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009',
          'manifest38': '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5',
          'archive39': '5ae67eaacbe878a81c2a997b6b73480ecb846eeb4bf9110779f8e86b62a229ed',
          'v7': '8543d29f7047b7228f98eef12b2ae1f2d5738ec7447c8cd9605b259da029900f',
          'pkgManifest': 'a88697c1bb82b4f4ad9abf05b22f01f3a0ddfd53fdbfa4b7dd6bfbbdb9ea2f6e',
          'filesOnly': '2c1c779f812ba17e4f7f7a1939dfcff453ebf1c0301f68692f1337602ed48a64'}
FALSE_FLAGS = {'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False}
GAPS = []


def sha(p):
    try:
        h = hashlib.sha256()
        with open(p, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        GAPS.append('missing: ' + p)
        return None


def nlines(p):
    try:
        with open(p, 'rb') as fh:
            b = fh.read()
    except OSError:
        return None
    return b.count(b'\n') + (0 if (not b or b.endswith(b'\n')) else 1)


def J(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def T(p):
    with open(p, encoding='utf-8') as fh:
        return fh.read()


def rel(p):
    return p.replace(RT + '/', '')


def walk_files(root, skip=()):
    out = {}
    for d, _, files in os.walk(root):
        for f in files:
            p = os.path.join(d, f)
            r = os.path.relpath(p, root)
            if not any(r == s or r.startswith(s + '/') for s in skip):
                out[r] = p
    return out


def find_key(node, key):
    if isinstance(node, dict):
        if key in node:
            return node[key]
        for v in node.values():
            got = find_key(v, key)
            if got is not None:
                return got
    elif isinstance(node, list):
        for v in node:
            got = find_key(v, key)
            if got is not None:
                return got
    return None


def codes_of(node, out):
    if isinstance(node, dict):
        if isinstance(node.get('code'), str):
            out.add(node['code'])
        for v in node.values():
            codes_of(v, out)
    elif isinstance(node, list):
        for v in node:
            codes_of(v, out)
    return out


# ------------------------------------------------------------------------------------------------ subject
SV = J(REC + '/subject-verification.json')
delta = SV.get('delta', {})
delta_paths, added_paths = set(), set()
for kind in ('changed', 'added', 'removed'):
    for row in (delta.get(kind) or []):
        p = row['path'] if isinstance(row, dict) else row
        delta_paths.add(p)
        if kind == 'added':
            added_paths.add(p)
delta_counts = {k: len(delta.get(k) or []) for k in ('changed', 'added', 'removed')}
archives = {rel(p): {'sha256': sha(p), 'content': J(p)} for p in sorted(glob.glob(REC + '/archive-verification*.json'))}
live39, live38, archive39 = sha(LIVE39), sha(LIVE38), sha(ARCHIVE39)
archives_ok = all(a['content'].get('verified') and a['content'].get('archiveShaMatches') and a['content'].get('archiveSha256') == EXPECT['archive39'] for a in archives.values())
verified_manifest = bool(SV.get('manifest39Matches') and (SV.get('snapshot39') or {}).get('verified') and live39 == SV.get('manifest39Sha256') == EXPECT['manifest39']
                         and archive39 == EXPECT['archive39'] and archives_ok)
parent38_unchanged = bool(live38 == EXPECT['manifest38'] and SV.get('manifest38Matches') and (SV.get('snapshot38') or {}).get('verified'))
if not verified_manifest:
    GAPS.append('subject verification incomplete')

# ------------------------------------------------------------------------------------------------ read map
ledger = [json.loads(line) for line in open(REC + '/read-ledger.jsonl', encoding='utf-8')]
fresh_complete, fresh_ranges, delta_rows = {}, {}, {}
for r in ledger:
    if r['kind'] == 'fresh39Read':
        if r['range'] == '1-%d' % r['lines']:
            fresh_complete[r['path']] = r
        else:
            fresh_ranges.setdefault(r['path'], []).append(r)
    elif r['kind'] == 'delta39Read':
        delta_rows[r['path']] = r
for p in list(fresh_ranges):
    if p in fresh_complete:
        del fresh_ranges[p]

fresh, ranged, delta_reads = [], [], []
for p, r in sorted(fresh_complete.items()):
    cur = sha(S39 + '/' + p)
    if cur != r['sha256']:
        GAPS.append('fresh read not current: ' + p)
    fresh.append({'path': p, 'sha256': cur, 'lines': nlines(S39 + '/' + p), 'read': 'complete', 'readClass': 'fresh39Read',
                  'note': r['note'], 'inDelta38to39': p in delta_paths, 'addedIn39': p in added_paths})
for p, rows in sorted(fresh_ranges.items()):
    cur = sha(S39 + '/' + p)
    if any(cur != r['sha256'] for r in rows):
        GAPS.append('ranged read not current: ' + p)
    ranged.append({'path': p, 'sha256': cur, 'lines': nlines(S39 + '/' + p), 'read': 'named ranges only (not a whole-file read)', 'readClass': 'fresh39RangeRead',
                   'ranges': [r['range'] for r in rows], 'inDelta38to39': p in delta_paths})
partial_diffs = []
for p, r in sorted(delta_rows.items()):
    cur = sha(S39 + '/' + p)
    d = RT + '/' + r['diff']
    dsha = sha(d)
    if cur != r['sha256'] or dsha != r['diffSha256']:
        GAPS.append('delta read not current: ' + p)
    partial = r['note'].startswith('partial')
    if partial:
        partial_diffs.append(p)
    delta_reads.append({'path': p, 'sha256': cur, 'lines': nlines(S39 + '/' + p), 'readClass': 'delta39Read',
                        'read': ('PARTIAL 38->39 diff' if partial else 'complete 38->39 diff') + ' (not a whole-file read)',
                        'note': r['note'], 'diffReceipt': r['diff'], 'diffSha256': dsha})

v38 = J(V38PATH)
inherited, via_diff, changed_not_fresh = [], [], []
for r in v38['readScope']['fresh38Read'] + v38['readScope']['inheritedUnchanged37Read']:
    p = r['path']
    if p in fresh_complete:
        continue
    a, b = sha(S38 + '/' + p), sha(S39 + '/' + p)
    if a == b:
        if b != r['sha256']:
            GAPS.append('source38 review hash differs from source38 bytes: ' + p)
        inherited.append({'path': p, 'sha256': b, 'lines': r['lines'], 'readClass': 'inheritedUnchanged38Read',
                          'basis': 'read completely under the source38 review (' + r['readClass'] + '); byte-identical in source39 (hash recomputed here)'})
    elif p in delta_rows and p not in partial_diffs:
        via_diff.append({'path': p, 'sha38': a, 'sha39': b, 'readClass': 'complete38ReadPlusComplete39Diff',
                         'basis': 'source38 bytes read completely (' + r['readClass'] + ') and the exact 38->39 diff read completely; not a fresh whole-file read'})
    else:
        changed_not_fresh.append({'path': p, 'sha38': a, 'sha39': b, 'delta39Read': p in delta_rows, 'partialDiff': p in partial_diffs,
                                  'rangeRead': fresh_ranges.get(p) and [x['range'] for x in fresh_ranges[p]]})
covered = set(fresh_complete) | set(fresh_ranges) | set(delta_rows)
uncovered_delta = sorted(delta_paths - covered)
pin_paths = [p for p in uncovered_delta if re.search(r'source-pins\.v\d\.json$', p)]
uncovered_nonpin = [p for p in uncovered_delta if p not in pin_paths]
for p in uncovered_nonpin:
    GAPS.append('delta file without read entry: ' + p)

# ------------------------------------------------------------------------------------------------ command receipts
G = J(REC + '/reference/groups-report.all.json')
group_rows = [{'name': r['name'], 'exitCode': r['exitCode'], 'timedOut': r.get('timedOut'), 'seconds': r.get('seconds'), 'scriptSha256': r.get('scriptSha256'),
               'scriptMatchesManifest': r.get('scriptMatchesManifest'), 'stdoutSha256': r.get('stdoutSha256'),
               'copyUnchangedAfter': r.get('copyAfter') == {'changed': [], 'missing': [], 'extra': []}, 'stdoutTail': (r.get('stdoutTail') or '')[-300:]} for r in G['rows']]
groups_ok = bool(G.get('passed')) and all(r['exitCode'] == 0 and r['copyUnchangedAfter'] and r['scriptMatchesManifest'] for r in group_rows)
ev3_lines = re.findall(r'^(\S+) (\d+)\s*$', T(REC + '/reference/evaluator3.stdout'), re.M)
children = {n: {'exitCode': int(c)} for n, c in ev3_lines}
for f in sorted(glob.glob(REC + '/reference/evaluator3/*.stdout')):
    name = os.path.basename(f)[:-7]
    try:
        d = J(f)
        info = {k: d[k] for k in ('passed', 'count', 'checkCount', 'total') if k in d and not isinstance(d[k], (dict, list))}
        for lk in ('failed', 'cases', 'mismatches', 'checks'):
            if isinstance(d.get(lk), (list, dict)):
                info[lk + 'Count'] = len(d[lk])
    except Exception:
        tail = T(f).strip().splitlines()
        info = {'stdoutTail': tail[-1][:200] if tail else ''}
    children.setdefault(name, {}).update(info)
children_ok = len(ev3_lines) == 17 and all(c.get('exitCode') == 0 for c in children.values())
foundation_report = J(REC + '/reference/foundation.json')
my_identity = [c for c in foundation_report.get('checks', []) if c.get('script') == 'check-identity.py']

P = J(REC + '/planning-checks.json')
PC = P['counts']
v38_counts = v38['commandReceipts'].get('planningCounts') or {}
planning_ok = P['check_implementation_planning']['exitCode'] == 0 and P['check_repository_file_inventory']['exitCode'] == 0 and PC.get('v7Sha256') == EXPECT['v7']


def probe_receipt(name):
    return J(REC + '/probes/' + name)


def run_record(name, script):
    p = REC + '/runs/' + name + '.run.json'
    r = J(p)
    cur = sha(script)
    ok = r.get('exitCode') == 0 and not r.get('copyChangedVsManifest') and not r.get('copyExtraVsManifest') and r.get('scriptSha256') == cur
    if not ok:
        GAPS.append('run receipt not clean or script changed after run: ' + name)
    return {'runReceipt': rel(p), 'runReceiptSha256': sha(p), 'exitCode': r.get('exitCode'), 'seconds': r.get('seconds'), 'scriptSha256AtRun': r.get('scriptSha256'),
            'scriptUnchangedSinceRun': r.get('scriptSha256') == cur, 'copyUnchanged': not r.get('copyChangedVsManifest') and not r.get('copyExtraVsManifest'),
            'stdoutSha256': r.get('stdoutSha256'), 'stderrSha256': r.get('stderrSha256')}


POL = probe_receipt('policy-test.json')
TERM = probe_receipt('run-termination-s7.json')
QRY = probe_receipt('query-carriers.json')
CAR = probe_receipt('carrier-readonly.json')
SD = probe_receipt('schema-digest-effect.json')
NCF = probe_receipt('native-custody-fallback.json')
CMP = probe_receipt('comparison-knowledge.json')
REP = probe_receipt('repair2.json')


def rows_by_case(receipt):
    return {r['case']: r for r in receipt['rows']}


def summary(receipt):
    return {'rows': len(receipt['rows']), 'failed': [r['case'] for r in receipt['failed']],
            'observations': [r['case'] for r in receipt['rows'] if r.get('kind') == 'observation' or r['case'].startswith('observation')]}


POLc, QRYc, NCFc, REPc = rows_by_case(POL), rows_by_case(QRY), rows_by_case(NCF), rows_by_case(REP)
car_scen = [r for r in CAR['rows'] if ' | ' in r['case']]
car_summary = {'scenarios': len(car_scen), 'scenariosPassed': sum(1 for r in car_scen if r['ok']),
               'schemaObjectsUnchangedEverywhere': all(isinstance(r['observed'], dict) and r['observed'].get('schemaObjectsUnchanged') for r in car_scen),
               'standingsObserved': sorted({r['observed']['standing'] for r in car_scen if isinstance(r['observed'], dict)}), 'rows': len(CAR['rows']), 'failed': len(CAR['failed'])}
p3 = [r for r in POL['rows'] if r['probe'] == 'P3']

PROBES = [
    {'id': 'P39-SUBJECT', 'script': 'probes/verify_subject.py', 'receipts': ['receipts/subject-verification.json', 'receipts/manifest39-index.json'],
     'claim': 'Formal manifest f71a5992... and snapshot verified member by member (12,909 members, hash and length); parent38 manifest and snapshot re-verified; 38->39 delta measured (67 changed, 5 added, 0 removed).'},
    {'id': 'P39-ARCHIVE', 'script': 'probes/verify_archive_extract.py', 'receipts': sorted(archives),
     'claim': 'Archive 5ae67eaa... hashed; every member extracted into two disposable copies and compared by hash and length; no extra, duplicate or non-regular members.'},
    {'id': 'P39-DELTA', 'script': 'probes/make_delta_diffs.py', 'receipts': ['receipts/delta-diff-summary.json', 'receipts/delta-diffs/'],
     'claim': 'Unified 38->39 diffs for all 72 delta files (reading aid; a diff is not a whole-file read).'},
    {'id': 'P39-GROUPS', 'script': 'probes/run_reference_groups.py', 'receipts': ['receipts/reference/groups-report.all.json'],
     'claim': 'Six pinned reference groups with /tmp/opensip-architecture-review-env/bin/python -I -B on a verified disposable exact copy, re-verified before and after.'},
    {'id': 'P39-PLAN', 'script': 'probes/run_planning_checks.py', 'receipts': ['receipts/planning-checks.json'],
     'claim': 'check_implementation_planning --check and check_repository_file_inventory --check on the exact copy plus independent v7/coverage/planning-source binding counts.'},
    {'id': 'P39-PKG', 'script': 'claude-author-package-successor.v16/verify-package.py and probe-native-v2.py (author tools, run by probes/run_env.py on this review\'s verified copy)',
     'receipts': ['receipts/runs/package-v16-verify.run.json', 'receipts/runs/package-v16-probe-native-v2.run.json'],
     'outputs': ['work/package-v16-verify/verification.json', 'work/probe-native-v2.json'],
     'claim': 'Package16 7 groups (17 exports across 6 Run/control groups plus 7 queries) and 9 native-v2 membership probes re-executed against source39 and compared in content with the root receipts.'},
    {'id': 'P39-POLICY', 'script': 'probes/probe_policy_test.py', 'receipts': ['receipts/probes/policy-test.json'], 'run': 'policy-test', 'discriminating': True,
     'claim': 'P1 fixture verifier versus production composition over the same facts (known native hit; required/optional evidence present/missing; or/and); P2 universe tokens; P3 %d PolicyTestSuiteV2 admission routes; P4 identity preimages recomputed with the reviewer\'s own C() and H().' % len(p3)},
    {'id': 'P39-TERM7', 'script': 'probes/probe_run_termination_s7.py', 'receipts': ['receipts/probes/run-termination-s7.json'], 'run': 'run-termination-s7', 'discriminating': True,
     'claim': 'run-termination-contract section 7 host composition admission over golden Runs with receipts minted by the evidence store: detail allowlist order, receipt/inventory/plan/stage joins and reminted negatives.'},
    {'id': 'P39-QUERY', 'script': 'probes/probe_query_carriers.py', 'receipts': ['receipts/probes/query-carriers.json'], 'run': 'query-carriers', 'discriminating': True,
     'claim': 'Nine query-dispatch commands, 20 public graph-query-3 operations, 17 non-graph operations, host-only operations, per-command lawful controls plus four cross-kind/exit negatives, reminted join negatives and the delivery failure laws.'},
    {'id': 'P39-CARRIER-RO', 'script': 'probes/probe_carrier_readonly.py', 'receipts': ['receipts/probes/carrier-readonly.json'], 'run': 'carrier-readonly', 'discriminating': True,
     'claim': '11 real in-memory SQLite carriers x 3 associations x 3 witnesses against the reviewer\'s own table of commit-recovery-readonly section 1 precedence; schema objects unchanged; public projections schema-valid.'},
    {'id': 'P39-SCHEMA-DIGEST', 'script': 'probes/probe_schema_digest_effect.py', 'receipts': ['receipts/probes/schema-digest-effect.json'], 'run': 'schema-digest-effect', 'discriminating': True,
     'claim': 'Registry effect of the in-place native-evidence.schemas.v2.json edit (JSON difference paths; source38/39 digests registered or not).'},
    {'id': 'P39-NATIVE-CUSTODY', 'script': 'probes/probe_native_custody_fallback.py', 'receipts': ['receipts/probes/native-custody-fallback.json'], 'run': 'native-custody-fallback', 'discriminating': True,
     'claim': 'Helper-level identity section 3 pruned-tree read custody and native U-9 syntax-only fallback boundaries (owner functions, not full Runs).'},
    {'id': 'P39-COMPARISON', 'script': 'probes/probe_comparison_knowledge.py', 'receipts': ['receipts/probes/comparison-knowledge.json'], 'run': 'comparison-knowledge', 'discriminating': True,
     'claim': 'Pure-function presence-knowledge helpers (first attribution unknown, correspondence barrier, selection exclusion, baseline presence knowledge, fingerprint absence).'},
    {'id': 'P39-REPAIR2', 'script': 'probes/probe_repair2.py', 'receipts': ['receipts/probes/repair2.json'], 'run': 'repair2', 'discriminating': True,
     'claim': 'repair:2 constructor over the owner checker\'s close_run-admitted Runs with a spied shared builder: refusal order before any descriptor, exact-class unavailability mapping (subclass propagates), plan admission and major-1 refusal.'},
]
for pr in PROBES:
    s = pr['script']
    pr['scriptSha256'] = sha(RT + '/' + s) if s.startswith('probes/') else None
    pr['receiptSha256'] = {r: (sha(RT + '/' + r) if not r.endswith('/') else None) for r in pr['receipts']}
    if pr.get('run'):
        pr['execution'] = run_record(pr['run'], RT + '/' + s)
pkg_runs = {'verify': run_record('package-v16-verify', PKG + '/verify-package.py'), 'nativeProbe': run_record('package-v16-probe-native-v2', PKG + '/probe-native-v2.py')}
PROBES[5]['execution'] = pkg_runs
for pr in PROBES:
    if pr['id'] in ('P39-POLICY', 'P39-TERM7', 'P39-QUERY', 'P39-CARRIER-RO', 'P39-NATIVE-CUSTODY', 'P39-COMPARISON', 'P39-REPAIR2'):
        pr['result'] = summary(probe_receipt(pr['receipts'][0].split('/')[-1]))

# ------------------------------------------------------------------------------------------------ package16
AM = J(PKG + '/artifact-manifest.json')
pkg_manifest_sha = sha(PKG + '/artifact-manifest.json')
listed = {f['path']: f for f in AM['files']}
actual = walk_files(PKG, skip=('artifact-manifest.json',))
pkg_mismatch = sorted(p for p, f in listed.items() if p not in actual or sha(actual[p]) != f['sha256'] or os.path.getsize(actual[p]) != f['bytes'])
pkg_unlisted = sorted(set(actual) - set(listed))
BIND = J(PKG + '/source-binding.v39.json')
REBUILD_PATH = B + '/root-author-package-final39-rebuild.v1/rebuild-report.json'
REB = J(REBUILD_PATH)
FM = J(LIVE39)
SMP = PKG + '/source-manifest.json'
SM = J(SMP)


def file_triples(doc):
    files = doc.get('files') if isinstance(doc, dict) else doc
    return sorted((f.get('path'), f.get('sha256'), f.get('bytes', f.get('size'))) for f in files)


formal_triples = file_triples(FM)
projection = {'formalManifestSha256': live39, 'artifactManifestFormalSubject': AM.get('formalSubjectManifestSha256'), 'artifactManifestFilesOnlySource': AM.get('sourceManifestSha256'),
              'formalSourceManifestCopySha256': sha(PKG + '/formal-source-manifest.v39.json'), 'packageSourceManifestSha256': sha(SMP),
              'packageSourceManifestFilesEqualFormalFiles': file_triples(SM) == formal_triples, 'formalFileCount': len(formal_triples),
              'formalAndFilesOnlyAreDifferentObjects': AM.get('formalSubjectManifestSha256') != AM.get('sourceManifestSha256'),
              'bindingProjectionEqualsFormalFiles': BIND.get('projectionEqualsFormalFiles')}
mine_ver, root_ver = J(RT + '/work/package-v16-verify/verification.json'), J(B + '/author-package-final39-verification.v1/verification.json')
mine_files = walk_files(RT + '/work/package-v16-verify')
root_files = walk_files(B + '/author-package-final39-verification.v1')
common = sorted(set(mine_files) & set(root_files))
content_diff = [r for r in common if sha(mine_files[r]) != sha(root_files[r])]
stores = [r for r in common if r.endswith('.store.json')]
export_rows = REB.get('exportComparison') or []
pkg_store_shas = {}
for r, p in walk_files(PKG).items():
    if r.endswith('.store.json') and not r.startswith('historical'):
        pkg_store_shas.setdefault(sha(p), []).append(r)
exports_found = sum(1 for e in export_rows if e.get('exportSha256') in pkg_store_shas)
NV = J(RT + '/work/probe-native-v2.json')
overlay_dir = B + '/claude-author-package-migration.v1/overlay'
overlay_files = walk_files(overlay_dir)
overlay_equal = sorted(r for r, p in overlay_files.items() if r in actual and sha(actual[r]) == sha(p))
overlay_not_equal = sorted(set(overlay_files) - set(overlay_equal))
ov_verify_template = T(overlay_dir + '/verify-package.py').replace('__SOURCE_MANIFEST_SHA256__', EXPECT['filesOnly']) == T(PKG + '/verify-package.py')
ov_readme_header = T(PKG + '/README.md').endswith(T(overlay_dir + '/README.md'))
pre_binding = {'readmeSha256': sha(PKG + '/historical-before-formal-binding39/README.md'), 'artifactManifestSha256': sha(PKG + '/historical-before-formal-binding39/artifact-manifest.json')}
pre_binding['readmeEqualsOverlayReadme'] = pre_binding['readmeSha256'] == sha(overlay_dir + '/README.md')
pre_binding['artifactManifestEqualsRebuiltPackage'] = pre_binding['artifactManifestSha256'] == REB.get('packageManifestSha256')
group_counts = {g['group']: g.get('count') for g in mine_ver['groups']}
PACKAGE = {
    'package': PKG, 'artifactManifestSha256': pkg_manifest_sha, 'expectedArtifactManifestSha256': EXPECT['pkgManifest'], 'artifactManifestEqual': pkg_manifest_sha == EXPECT['pkgManifest'],
    'filesListed': len(listed), 'filesMismatched': pkg_mismatch, 'filesUnlisted': pkg_unlisted,
    'formalManifestVersusFilesOnlyProjection': projection,
    'sourceBindingV39': {'sha256': sha(PKG + '/source-binding.v39.json'), 'content': BIND},
    'reconstruction': {'rebuildReport': REBUILD_PATH, 'sha256': sha(REBUILD_PATH), 'equalsBindingRebuildReportSha256': sha(REBUILD_PATH) == BIND.get('rebuildReportSha256'),
                       'inputs': REB.get('inputs'), 'script': REB.get('script'), 'scriptSha256': REB.get('scriptSha256'),
                       'commands': [{k: c.get(k) for k in ('label', 'exit', 'seconds')} for c in REB.get('commands', [])],
                       'rebuiltPackageBeforeMetadataBinding': REB.get('packageManifestSha256'),
                       'equalsArtifactPredecessor': REB.get('packageManifestSha256') == AM.get('predecessorArtifactManifestSha256') == BIND.get('rebuiltPackageBeforeMetadataBindingSha256'),
                       'overlayManifestSha256Measured': sha(overlay_dir + '/overlay-manifest.json'), 'overlayManifestInPackageSha256': sha(PKG + '/overlay-manifest.json'),
                       'overlayFilesByteEqualInPackage': len(overlay_equal), 'overlayFilesNotEqualInPackage': overlay_not_equal,
                       'overlayDifferencesExplained': {'verify-package.py: only the __SOURCE_MANIFEST_SHA256__ placeholder is instantiated with the files-only projection sha': ov_verify_template,
                                                       'README.md: the package README is a formal-binding header followed by the overlay README': ov_readme_header},
                       'preFormalBindingCopies': pre_binding,
                       'exportComparisonRows': len(export_rows), 'exportsWithNewRunId': sum(1 for e in export_rows if e.get('runId') != e.get('previousRunId')),
                       'exportsWithNewBytes': sum(1 for e in export_rows if e.get('exportSha256') != e.get('previousExportSha256')),
                       'exportsMarkedNew': sum(1 for e in export_rows if e.get('new')), 'exportBytesFoundInPackage': exports_found},
    'verification': {'mineSha256': sha(RT + '/work/package-v16-verify/verification.json'), 'rootSha256': sha(B + '/author-package-final39-verification.v1/verification.json'),
                     'contentEqualToRoot': mine_ver == root_ver, 'passed': mine_ver.get('passed'), 'groupCounts': group_counts,
                     'exportCount': sum(v for k, v in group_counts.items() if k != 'query'), 'queryCount': group_counts.get('query'),
                     'filesComparedWithRootVerificationDirectory': len(common), 'filesDifferingInContent': content_diff, 'exactInputStoresCompared': len(stores),
                     'groups': [{k: g.get(k) for k in ('group', 'count', 'passed', 'negativeControls', 'exitCode', 'reportSha256')} for g in mine_ver['groups']]},
    'nativeV2Probe': {'mineSha256': sha(RT + '/work/probe-native-v2.json'), 'contentEqualToRootRebuildProbe': NV == REB.get('nativeV2Probe'), 'runs': len(NV.get('runs', [])),
                      'passed': NV.get('passed'), 'unitsVsDiscoveryDisagreements': NV.get('unitsVsDiscoveryDisagreements')},
}
package_ok = (PACKAGE['artifactManifestEqual'] and not pkg_mismatch and not pkg_unlisted and projection['packageSourceManifestFilesEqualFormalFiles'] and projection['formalAndFilesOnlyAreDifferentObjects']
              and PACKAGE['verification']['contentEqualToRoot'] and not content_diff and PACKAGE['verification']['exportCount'] == 17 and PACKAGE['verification']['queryCount'] == 7
              and PACKAGE['nativeV2Probe']['contentEqualToRootRebuildProbe'] and PACKAGE['nativeV2Probe']['runs'] == 9 and PACKAGE['reconstruction']['exportComparisonRows'] == 17
              and set(overlay_not_equal) <= {'README.md', 'verify-package.py'} and ov_verify_template and ov_readme_header)
if not package_ok:
    GAPS.append('package16 assessment incomplete: ' + json.dumps({k: v for k, v in PACKAGE['verification'].items() if k != 'groups'})[:400])

# ------------------------------------------------------------------------------------------------ root reference and census
REF = {}
for name in ('root-source39-final-reference.v1', 'root-source39-final-reference.v2'):
    d = J(B + '/' + name + '/reference-checks.json')
    fj = J(B + '/' + name + '/foundation.json')
    ident = [c for c in fj.get('checks', []) if c.get('script') == 'check-identity.py']
    failures = []
    if ident:
        m = re.search(r'\[(.*)\]', ident[0].get('stdout', ''), re.S)
        failures = re.findall(r'"([^"]+)"', m.group(1)) if m else []
    REF[name] = {'reportSha256': sha(B + '/' + name + '/reference-checks.json'), 'passed': d.get('passed'),
                 'commands': [{'name': c.get('name'), 'exitCode': c.get('exitCode')} for c in d.get('commands', [])],
                 'checkIdentity': ident[0].get('stdout', '').splitlines()[0] if ident else None, 'checkIdentityFailures': failures}
CA_PATH = B + '/root-foundation-detail-census-correction.v1/assessment.json'
CA = J(CA_PATH)
reg39, reg38 = codes_of(J(S39 + '/docs/coop/design-corrections/public-detail-registry.v1.json'), set()), codes_of(J(S38 + '/docs/coop/design-corrections/public-detail-registry.v1.json'), set())
FOUR = ['DELIVERY.REQUIRED_PROJECTION_FAILED', 'DOCTOR.REPORT_NOT_PRODUCIBLE', 'OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED', 'REVIEW.CANDIDATE_UNKNOWN']
ci39 = T(S39 + '/docs/coop/design-corrections/foundation/check-identity.py')
CENSUS = {'assessment': CA_PATH, 'assessmentSha256': sha(CA_PATH), 'checkIdentitySha39': sha(S39 + '/docs/coop/design-corrections/foundation/check-identity.py'),
          'equalsRootAfterSha': sha(S39 + '/docs/coop/design-corrections/foundation/check-identity.py') == CA.get('sha256'),
          'checkIdentitySha38': sha(S38 + '/docs/coop/design-corrections/foundation/check-identity.py'), 'equalsRootBeforeSha': sha(S38 + '/docs/coop/design-corrections/foundation/check-identity.py') == CA.get('beforeSha256'),
          'registryCodes39': len(reg39), 'registryCodes38': len(reg38), 'addedCodes': sorted(reg39 - reg38), 'removedCodes': sorted(reg38 - reg39),
          'addedAreExactlyTheFourWorkflowDetails': sorted(reg39 - reg38) == sorted(FOUR), 'rootRegistryCount': CA.get('registryCount'), 'rootSubstrateCount': CA.get('newSubstrateCount'),
          'checkerNamesTheFourExplicitly': all("'" + c + "'" in ci39 for c in FOUR) and '_WORKFLOW3_PUBLIC_DETAILS' in ci39,
          'checkerKeepsHistorical289Closed': 'historical 289-code substrate closed' in ci39,
          'thisReviewFoundationCheckIdentity': my_identity[0].get('stdout', '').splitlines()[0] if my_identity else None}
if not (CENSUS['equalsRootAfterSha'] and CENSUS['addedAreExactlyTheFourWorkflowDetails'] and CENSUS['checkerNamesTheFourExplicitly']):
    GAPS.append('census verification incomplete')
INTEG_PATH = B + '/root-final-owner-integration.v1/integration.json'
INTEG = J(INTEG_PATH)
integ_equal = sum(1 for f in INTEG.get('files', []) if sha(S39 + '/' + f['path']) == f['sha256'])

# ------------------------------------------------------------------------------------------------ measured source facts
crr39, crr38 = T(S39 + '/docs/v2/architecture/commit-recovery-readonly.v3.md'), T(S38 + '/docs/v2/architecture/commit-recovery-readonly.v3.md')


def ws(s):
    return re.sub(r'\s+', ' ', s)


ADV3803 = {side: {'unqualifiedF00F37Sentence': 'spelling in F00–F37; that is not treated as a blocker' in ws(text),
                  'currentPlanF00F53Stated': 'holds F00–F53' in ws(text),
                  'storeTransitionOnlyScope': "it is the store transition's detail" in ws(text),
                  'citesSecurityS12Scope': 'Security S12 scopes it to a store transition footprint' in ws(text)} for side, text in (('source38', crr38), ('source39', crr39))}
adv3803_closed = (ADV3803['source38']['unqualifiedF00F37Sentence'] and ADV3803['source38']['storeTransitionOnlyScope'] and not ADV3803['source39']['unqualifiedF00F37Sentence']
                  and not ADV3803['source39']['storeTransitionOnlyScope'] and ADV3803['source39']['currentPlanF00F53Stated'] and ADV3803['source39']['citesSecurityS12Scope'])
if not adv3803_closed:
    GAPS.append('ADV38-03 measurement not discriminating or not closed: ' + json.dumps(ADV3803))
ro_map = find_key(J(S39 + '/docs/coop/design-corrections/security/carrier-dispatch.v3.json'), 'readOnlyStandingOfDispatchResult') or {}
pred_doc = 'docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json'
pred_doc_exists = os.path.exists(S39 + '/' + pred_doc)
if not pred_doc_exists:
    GAPS.append('identity-schemas Predicate digest document does not exist: ' + pred_doc)
map_sources = {}
for p in ('docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json', 'docs/coop/design-corrections/correction-crosswalk.proposed.json',
          'docs/coop/design-corrections/inherited-residuals.proposed.md', 'docs/coop/design-corrections/current-source-map.proposed.md',
          'docs/v2/architecture/08-decision-and-readiness-register.md', 'docs/coop/design-corrections/qualification-gates.proposed.json',
          'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md',
          'docs/v2/contracts/product-v1/README.md', 'docs/v2/architecture/prototype-report-inventory.md', 'docs/v2/architecture/repository-file-inventory.v1.json'):
    a, b = sha(S38 + '/' + p), sha(S39 + '/' + p)
    map_sources[p] = {'sha256': b, 'unchanged38to39': a == b}
U = {p.split('/')[-1]: v['unchanged38to39'] for p, v in map_sources.items()}
gates = J(S39 + '/docs/coop/design-corrections/qualification-gates.proposed.json')
gate_rows = gates.get('gates') or gates.get('items') or []
gates_qualified_true = sum(1 for g in gate_rows if isinstance(g, dict) and g.get('qualified') is True)

# ------------------------------------------------------------------------------------------------ findings
P1 = POLc['known-native-hit-under-missing-required-evidence-agrees-with-composition']
P2a, P2b, P2c = POLc['authored-suite-with-unregistered-token-is-resolver-accepted'], POLc['arbitrary-token-no-such-universe'], POLc['registered-token-control-yields-the-same-summary']
SHOULD = [
    {'id': 'S39-01', 'severity': 'SHOULD', 'title': 'The policy-test facts verifier drops a known native hit when a required evidence kind is unavailable, so the authoring test reports a different gating outcome than production for the same facts',
     'selectors': ['docs/coop/design-corrections/workflows/policy_test_model.v3.py:214-218 (evaluate: `if required - available` marks every selected subject unknown and `continue`s before any predicate is evaluated)',
                   'docs/v2/contracts/product-v1/workflows-and-surfaces.md:641-647 (facts cases are evaluated under the current atom law; unknown leaves an expectation indeterminate "unless a known finding decides it; known findings, strong Kleene and gating are unchanged")',
                   'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md:34-36 (known matches are preserved despite incomplete coverage; deficiency provenance is retained when a known value dominates) and :319 (fail still dominates)',
                   'docs/coop/design-corrections/foundation/check-composition.v3.py:95 (a9-known-live-failure-dominates-missing-required-import) and check-replay.v3.py:210',
                   'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py oc2/pt2 policy-test controls (ranges 3540-3800 read): no control for a known hit under a missing required kind'],
     'measured': {'composition': P1['observed']['composition'], 'fixture': P1['observed']['fixture'],
                  'controlsThatAgree': {c: POLc[c]['ok'] for c in ('control-or-required-present-agrees', 'control-or-optional-missing-agrees')},
                  'andFalseRequiredMissing': {'composition': POLc['production-composition-and-false-required-missing']['observed'], 'fixture': POLc['fixture-and-false-required-missing']['observed']}},
     'detail': ('One gating rule `or(exists native hit, ...)` over src/a.ts declares a required import kind that the fixture lists as unavailable. Production composition (E.compose through the check-composition harness) returns rule outcome fail, verdict fail, 1 finding, root value true. '
                'The facts verifier returns verdict indeterminate, no finding, indeterminateRules [known-hit-rule]; the suite\'s finding expectation becomes indeterminate and its verdict=fail expectation unmet, so the suite outcome is failed. '
                'With the required kind available, or the kind optional, both agree on fail with the finding. With an `and` whose known conjunct is false, both agree on indeterminate. The disagreement is exactly the fail-dominance case the composition owner controls (a9). '
                'Consequence: a policy author\'s suite can report a production gate failure as indeterminate and unmet; section 5 promises the opposite.'),
     'requiredChange': 'Evaluate the predicate for every selected subject even when a required kind is unavailable. Keep known true results as findings and gating failures (fail dominates). Mark only subjects without a known deciding value as unknown, with the missing-required cause retained. Add a policy-test control mirroring check-composition a9 (known hit plus missing required kind gives verdict fail with the finding).',
     'receipt': 'receipts/probes/policy-test.json#P1', 'owner': 'workflows policy test (policy_test_model.v3.py; check-workflow-projection pt2 controls)'},
    {'id': 'S39-02', 'severity': 'SHOULD', 'title': 'policy test admits and evaluates candidate rule universe tokens that the evaluator3 profile refuses, including the authored suite\'s own typescript-v2',
     'selectors': ['docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md:26 (closed policy universe token map typescript/rust/syntax; "Unknown tokens refuse admission; historical illustrative tokens such as typescript-v2 are not additional implicit aliases")',
                   'docs/coop/design-corrections/foundation/evaluator_input_model.v3.py:16 (UNIVERSES from identity-schemas x-opensip-evaluator-profile.policyUniverseMap)',
                   'docs/v2/contracts/product-v1/workflows-and-surfaces.md:638-641 and 653-668 (facts cases under the current policy resolver and atom law; admission precedes evaluation)',
                   'docs/coop/design-corrections/workflows/policy-test-cases.v3.json:23, 63, 87, 122, 179, 226, 265, 308, 317, 355, 573, 608 (every authored universe is typescript-v2)',
                   'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py:3651 (pt2-current-candidate-resolver-admitted asserts the resolver accepts that suite)'],
     'measured': {'profileTokenMap': POLc['evaluator-profile-policy-universe-map']['observed'], 'authoredTokens': POLc['authored-suite-universe-tokens']['observed'],
                  'authoredSuite': P2a['observed'], 'noSuchUniverse': P2b['observed'], 'registeredTokenControl': P2c['observed']},
     'detail': ('The authored suite uses typescript-v2, which is not in the profile token map, and PolicyTestSuiteV2 admission plus the resolver accept it (ADMITTED, resolverAccepted true, summary 5 passed / 0 failed / 3 indeterminate / 1 not-executable). '
                'Replacing the token with no-such-universe yields the same admission and the same summary; the registered token typescript yields the same summary too. So the universe token is neither admitted nor consulted by the facts verifier. '
                'Consequence: a candidate policy that analysis refuses at evaluator admission passes its authoring test with met expectations, and the checked-in reference suite exercises only a refused spelling.'),
     'requiredChange': 'Admit every candidate rule universe through the same closed policyUniverseMap before evaluation, refusing an unknown token with a typed registered detail under the section 5 precedence. Change the authored suite to registered tokens, and add a negative control (typescript-v2 and an arbitrary token refuse) beside pt2.',
     'receipt': 'receipts/probes/policy-test.json#P2', 'owner': 'workflows policy test admission (workflows_model.v3.py policy.test profile; policy-test-cases.v3.json; check-workflow-projection pt2)'},
]
ADVISORIES = [
    {'id': 'ADV39-01', 'severity': 'ADVISORY', 'title': 'The registered native payload schema document was edited in place, contrary to the native section 10 statement that its bytes are deliberately unchanged and that an edit is a schema-document successor',
     'selectors': ['docs/v2/contracts/product-v1/native-evidence.md:3093-3096', 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json (only difference: #/$defs/ResolvedNodeModulesLayoutV1/description)',
                   'docs/coop/design-corrections/foundation/identity-model.v3.py registered_schema_documents()', 'root-author-package-final39-rebuild.v1/rebuild-report.json inputs.registeredNativeSchemaSha256'],
     'measured': {k: SD[k] for k in ('sha38', 'sha39', 'registeredContainsSource39Digest', 'registeredContainsSource38Digest', 'jsonDifferencePaths', 'payloadRegistryClassesNamingTheNativeDocument')},
     'detail': ('The document changed 3e37c7b7... to 2d37b810... under the same v2 name; the only JSON difference is one description string. The identity registry now registers only the source39 digest, the rebuild consumed that digest, and %d of 17 package exports carry new RunIds. '
                'The new digest is propagated consistently and every executed suite passes, so nothing is inconsistent inside source39. But the section 10 sentence ("the annotation\'s bytes are deliberately unchanged ... editing ... is a schema-document successor with its own re-registration") no longer describes what was done, and a source38 payloadSchemaDigest is not resolvable against the source39 registry.') % PACKAGE['reconstruction']['exportsWithNewRunId'],
     'receipt': 'receipts/probes/schema-digest-effect.json', 'disposition': 'ROUTE-TO-NATIVE-OWNER: either record this document revision (and the historical digest\'s standing) in section 10, or restore the registered bytes and carry the description in a successor. Non-blocking.'},
]
obs_ncf = {r['case']: r['observed'] for r in NCF['rows'] if r.get('kind') == 'observation'}
OBSERVATIONS = [
    'Pruned-tree custody: one ResolvedNodeModulesLayoutV1 row with installPath node_modules authorizes reads of every top-level package (%s). A nested installed package still refuses. Security S3 (security-and-lifecycle.md:266-279) states which files were read is a host TCB observation, so this is within TCB-SCOPE-01.' % json.dumps(obs_ncf.get('observation-a-single-broad-installPath-row-authorizes-every-top-level-package')),
    'Exact-case segment rule: Node_Modules/a/index.js is not a pruned-tree read and stays first-party custody (%s). This is consistent with exact segment matching; a case-insensitive filesystem host must not fold it.' % json.dumps(obs_ncf.get('observation-exact-case-segment-rule-leaves-a-case-variant-directory-in-first-party-custody')),
    'U-9 fallback: when the only marker is in a custody-excluded directory, discovery yields the syntax-only fallback unit and its scope excludes that directory (%s). An explicit empty root list gives %s. Neither is claimed as a defect; U-9 names only "no language unit survives".' % (json.dumps(obs_ncf.get('observation-only-marker-in-a-custody-excluded-directory-yields-the-fallback'))[:300], json.dumps(obs_ncf.get('observation-explicit-roots-empty-explicit-root-list'))),
    'A hidden candidates listing\'s suppressedCount mutated from 1 to 0 still projects ADMIT (%s): the count is not joinable from the query record alone, so it rests on the producing step.' % json.dumps(QRYc['observation-hidden-listing-suppressedCount-is-not-joinable-from-the-record']['observed']),
    'repair:2: a trusted retained view that declares KeyError as its UNAVAILABLE class gets KeyError mapped to REPAIR.EVIDENCE_RUN_UNAVAILABLE (%s); a subclass of the declared class propagates. admit_repair_plan_v2 admits a reminted descriptor with applicable flipped (%s): it is schema and identity admission, and semantic authority stays with the constructor and apply authorization. Both are inside TCB-SCOPE-01.' % (json.dumps(REPc['observation-a-trusted-view-declaring-a-builtin-class-maps-that-exact-class']['observed']), json.dumps(REPc['observation-admit-repair-plan-v2-is-schema-and-identity-admission-not-semantic-rederivation']['observed'])),
    'PolicyTestSuiteV2 admission: a candidatePolicy with integer schemaMajor 1 but no schemaFamily routes CONFIG.INVALID rather than the major refusal (%s). The x-opensip-admission-precedence text reads "a policy document candidatePolicy whose integer schemaMajor is not 2"; a family-less object is read as not a policy document. A one-line clarification would remove the ambiguity.' % json.dumps(POLc['observation-candidate-major-1-without-family']['observed']),
    'Author checker hygiene: check-carrier-v3.py binds _S37_CF to the carrier_format INSERT and later rebinds the same global to carrier-format prose for a text check. The checker is correct in its own order, but reusing its publish helper after a full module run needs the SQL restored (done in P39-CARRIER-RO).',
    'identity-schemas.v3.json now names %s as the policy Predicate digest document (exists in source39: %s).' % (pred_doc.split('design-corrections/')[1], pred_doc_exists),
]

# ------------------------------------------------------------------------------------------------ item dispositions
term_cases = [r['case'] for r in TERM['rows']]
q_delivery = {r['case']: r['observed'] for r in QRY['rows'] if r['case'].startswith('delivery-law') or r['case'].startswith('owner-precommit')}
ITEMS = [
    {'id': 'ADV38-01', 'origin': 'claude-independent-design.v38 (ADVISORY)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/foundation/run-termination-contract.v1.md:205-342 (section 7 host composition of the whole analysis StepTermination; detail allowlist row 2 at :298)',
                             'docs/coop/design-corrections/foundation/run_termination_model.v1.py:299 (CLOSURE_DETAIL), :374 (admit_analysis_step_termination)'],
     'evidence': {'P39-TERM7': {'rows': len(TERM['rows']), 'failed': len(TERM['failed']), 'cases': term_cases}},
     'consequence': 'Delegated members now have a closed admission. The host observation {stepId, durability, attempts, commitReceipt, requiredClosureNotInstalled} is joined to the sealed Run, receipt, inventory, plan and stage; the detail is admitted only from the ordered allowlist (WORK_BUDGET, then REQUIRED_CLOSURE_NOT_INSTALLED, then the native entry deficiency of the coverageId carrier). An unrelated registered detail, a reminted receipt and mismatched joins refuse in P39-TERM7.'},
    {'id': 'ADV38-02', 'origin': 'claude-independent-design.v38 (ADVISORY)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/security/carrier-dispatch.v3.json:684-693 (readOnlyStandingOfDispatchResult: carrierFormat1/2 -> unknown-carrier-incompatible; fresh-install -> unknown-custody)',
                             'docs/v2/architecture/commit-recovery-readonly.v3.md section 1 (precedence rows 1-4)', 'docs/coop/design-corrections/security/carrier-format.v3.md section 8.1',
                             'docs/v2/contracts/product-v1/security-and-lifecycle.md:1315-1316 (bound carrier observed absent; association naming an unmigrated carrier)'],
     'evidence': {'readOnlyStandingOfDispatchResult': ro_map, 'P39-CARRIER-RO': car_summary},
     'consequence': 'The unmigrated-carrier association route is now machine-mapped, and a bound carrier observed absent is custody (host-io), never not-committed. Every one of the %d reviewer-tabulated scenarios matched the owner dispatch, no read-only open changed a schema object, and every reached public projection is a valid StepTermination. The reference model has no stability observation, so quarantine standings assume stable observations.' % car_summary['scenarios']},
    {'id': 'ADV38-03', 'origin': 'claude-independent-design.v38 (EDITORIAL)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL' if adv3803_closed else 'NOT-CLOSED',
     'finalOwnerSelectors': ['docs/v2/architecture/commit-recovery-readonly.v3.md:39-40 (F00-F37 now qualified as the range when the document was authored; the current plan holds F00-F53)',
                             'commit-recovery-readonly.v3.md:74-75 (the MIGRATION.CORRUPT scope now cites security S12)', 'commit-recovery-readonly.v3.md:30, 121 (not used on a read-only path)',
                             'docs/v2/contracts/product-v1/security-and-lifecycle.md:1319 (MIGRATION.CORRUPT: store transition footprint and carrierFormat 3 migration footprint at a writer or maintenance open)'],
     'evidence': ADV3803,
     'consequence': ('Measured on whitespace-normalized text: source38 carried the unqualified F00-F37 sentence and the store-transition-only scope; source39 carries neither, and instead states the F00-F53 plan and cites the security S12 scope. The read-only conclusion is unchanged and now agrees with S12.'
                     if adv3803_closed else 'The stale phrases were not measured as corrected; see evidence.')},
    {'id': 'ROOT39-FOUNDATION-DETAIL-CENSUS', 'origin': 'root-foundation-detail-census-correction.v1', 'disposition': 'CONFIRMED',
     'finalOwnerSelectors': ['docs/coop/design-corrections/foundation/check-identity.py (_WORKFLOW3_PUBLIC_DETAILS; historical 289-code substrate kept closed)', 'docs/coop/design-corrections/public-detail-registry.v1.json (four workflow rows added)'],
     'evidence': CENSUS,
     'consequence': 'The three root v1 failures were stale census assertions. The correction names exactly the four new workflow details, keeps the historical substrate closed, and does not absorb arbitrary future additions. The registry diff adds exactly those four codes and removes none.'},
    {'id': 'ROOT39-FINAL-REFERENCE', 'origin': 'root-source39-final-reference.v1 and .v2', 'disposition': 'V1-PRESERVED-AS-FAILURE; V2-IS-THE-ONLY-CURRENT-ALL-PASS-RECEIPT; THIS-REVIEW-RE-EXECUTED',
     'finalOwnerSelectors': ['root-source39-final-reference.v1/reference-checks.json', 'root-source39-final-reference.v2/reference-checks.json'],
     'evidence': {'roots': REF, 'thisReviewGroupsPassed': groups_ok, 'thisReviewEvaluator3StdoutSha256': next((r['stdoutSha256'] for r in group_rows if r['name'] == 'evaluator3'), None)},
     'consequence': 'v1 stays a failure (foundation exit 1; check-identity 1593 passed, 3 failed), and nothing relabels it. v2 is evidence only; this review\'s own six pinned groups on the verified copy are the acceptance input.'},
    {'id': 'TOPIC-POLICY-TEST', 'origin': 'source39 charter', 'disposition': 'CHANGES-REQUIRED (S39-01, S39-02); remainder confirmed',
     'finalOwnerSelectors': ['docs/v2/contracts/product-v1/workflows-and-surfaces.md:631-668', 'docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json', 'docs/coop/design-corrections/workflows/policy_test_model.v3.py', 'docs/coop/design-corrections/workflows/workflows_model.v3.py:181-311'],
     'evidence': {'P3': {r['case']: r['observed'] for r in p3}, 'P4': {r['case']: r['observed'] for r in POL['rows'] if r['probe'] == 'P4'}},
     'consequence': ('Confirmed independently: the admission precedence (suite major, candidate major, imperative key via the grammar, other schema failures CONFIG.INVALID, then resolver refusals with the resolver detail) over %d routes; suiteDigest = H("workflow.policy-test-suite", suite), not the raw bytes; result id policytest2 = H over the result without its id; candidate digest over raw bytes; same suite, same result bytes. '
                     'Strong Kleene in the verifier matches composition for and/or/not when evidence is available (P1 controls). Not confirmed: known-hit dominance under a missing required kind (S39-01) and universe-token admission (S39-02). argvDigest (workflows-and-surfaces.md:1056-1062; security S10 now defines it identically) was checked by reading and by the executed author control, not by an independent probe.') % len(p3)},
    {'id': 'TOPIC-QUERY-CARRIERS', 'origin': 'source39 charter', 'disposition': 'CONFIRMED-INDEPENDENTLY',
     'finalOwnerSelectors': ['docs/v2/contracts/product-v1/workflows-and-surfaces.md:1130-1139, 1208-1243, 1371-1372', 'docs/coop/design-corrections/workflows/query_surface_projection.v3.py:310-388', 'docs/coop/design-corrections/workflows/command-inventory.v3.json',
                             'docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json and invocation-record.schema.json (delta read)'],
     'evidence': {'commands': QRYc['inventory-query-dispatch-commands-are-exactly-the-nine']['observed'], 'publicOperations': QRYc['query-command-operations-are-the-20-public-graph-query-3-operations']['observed'],
                  'hostOperationsNotPublic': QRYc['host-operations-are-not-public-operations']['observed'], 'deliveryLaw': q_delivery, 'rows': len(QRY['rows']), 'failed': len(QRY['failed'])},
     'consequence': 'Exactly nine commands dispatch through query carriers; the query command exposes the 20 public graph-query-3 operations, 17 of them non-graph, with graph-query-3 bytes unchanged from source38; host-only operations are not public. Each command\'s parity paths equal its parity fields. Cross-kind envelopes, failure envelopes with carriers, graph selectors over records and wrong exits refuse. Reminted join negatives refuse. DELIVERY.REQUIRED_PROJECTION_FAILED is valid only without runId, and RENDERER_FAILED_AFTER_COMMIT only with runId.'},
    {'id': 'TOPIC-REPAIR2', 'origin': 'source39 charter', 'disposition': 'CONFIRMED-INDEPENDENTLY (observations only)',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/workflows_model.v3.py:119-179', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md:714', 'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:37', 'docs/coop/design-corrections/workflows/workflows_model.v1.py (historical constructor keeps keyword-only descriptor_major=1)'],
     'evidence': {'P39-REPAIR2': {r['case']: r['observed'] for r in REP['rows']}},
     'consequence': 'Authority refuses first, then a missing retained closure, then a non-run3 id, then Plan and exact run identity joins, then target correspondence, each before any descriptor is built. Only the exact declared unavailability class maps typed. The owner plan is repair:2 and admits; a major-1 descriptor refuses typed.'},
    {'id': 'TOPIC-COMPARISON-PRESENCE-KNOWLEDGE', 'origin': 'source39 charter', 'disposition': 'CONFIRMED-AT-HELPER-LEVEL',
     'finalOwnerSelectors': ['docs/v2/contracts/product-v1/workflows-and-surfaces.md:382-400 (evaluated absence; same-rule/same-path barrier; B absence only under RuleCoverage.absenceKnowledge complete-hit-set; INDETERMINATE current/baseline-absence-unknown), :402-411 (closed indeterminate reason order)', 'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py (delta read)', 'docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json (delta read)'],
     'evidence': {'P39-COMPARISON': summary(CMP), 'comparison-knowledge child': children.get('comparison-knowledge')},
     'consequence': 'Presence knowledge is true only for a baseline entry, false only for non-selection or complete-hit-set without a same-rule same-path barrier, and otherwise null, never coerced to false. First attribution unknown selects the baseline first. Full-Run comparison controls are the author\'s executed child, not an independent reconstruction.'},
    {'id': 'TOPIC-NATIVE-IDENTITY', 'origin': 'source39 charter', 'disposition': 'CONFIRMED-WITH-ADVISORY (ADV39-01)',
     'finalOwnerSelectors': ['docs/v2/contracts/product-v1/native-evidence.md:782 (U-4b ENUMERATION_MEMBERSHIP_ORDER), :851 (U-9 zero-config syntax-only fallback), :749 and :778 (U-9 in discovery and membership), :877 (NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT)',
                             'docs/coop/design-corrections/foundation/identity-model.v3.py:124 (FOUNDATION_DIGEST_UNANNOTATED), :683 (snapshot_pruned_tree_faults)',
                             'docs/coop/design-corrections/foundation/identity-schemas.v3.json (normalizationSpecificationLaw, bodyEligibilityLaw, stage-output registeredBy law)', 'docs/v2/contracts/product-v1/security-and-lifecycle.md:266-279 (A-5 pruned trees and the read set), :288-299 (U-9 counterpart in the admitted boundary inventory)'],
     'evidence': {'P39-NATIVE-CUSTODY': summary(NCF), 'nativeGroup': next((r['stdoutTail'] for r in group_rows if r['name'] == 'native'), None), 'native-consumer24-corrections child': children.get('native-consumer24-corrections')},
     'consequence': 'VCS trees refuse at any depth; a nested installed package needs its own row; a store realPath authorizes its own files; first-party Cargo output is never a read. The syntax-only fallback appears only when no language unit survives, its default selection is the complete syntax-only product at root, and zero units refuse NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT. Stage-output schema registration, the normalization map and body eligibility were read (diff and contract) and exercised by the executed consumer24 child, not independently probed.'},
    {'id': 'TOPIC-TERMINATION-IMPORT-EVALUATOR-NATIVE-BRIDGES', 'origin': 'source39 charter', 'disposition': 'CONFIRMED (termination independently; import/evaluator/native by read and executed controls)',
     'finalOwnerSelectors': ['run-termination-contract.v1.md section 7', 'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md (read complete; account targetUniverse typed null; body-eligible census)', 'evaluator-composition-contract.v3.md (read complete)'],
     'evidence': {'children': {k: children.get(k) for k in ('execution-inputs', 'composition', 'native-replay', 'execution-replay', 'candidate-replay', 'enumeration')}},
     'consequence': 'The bridges join through one owner each. No independent import-bridge probe was run; that is a limitation, not a finding.'},
    {'id': 'TOPIC-V7-PLANNING', 'origin': 'source39 charter', 'disposition': 'CONFIRMED (newly bound selectors partly line-read)',
     'finalOwnerSelectors': ['docs/v2/architecture/implementation-normative-inputs.v7.json (read complete)', 'docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-planning-sources.v1.json'],
     'evidence': {'planning': P['check_implementation_planning']['stdout'].strip(), 'inventory': P['check_repository_file_inventory']['stdout'].strip(),
                  'counts': {k: PC.get(k) for k in ('v7Sha256', 'v7Inputs', 'coverageSubjectMatchesV7', 'planningSourcesArchitectureSha256MatchesV7', 'coverageMappings', 'inventoryPaths', 'inventoryPackages', 'recoveryCases')},
                  'source38CoverageMappings': v38_counts.get('coverageMappings'), 'mappingPopulationPreserved': PC.get('coverageMappings') == v38_counts.get('coverageMappings')},
     'consequence': 'v7 binds 31 inputs with no mismatch and no self-binding; coverage and planning sources name v7; the mapping population is preserved and the checker passes. The coverage diff was line-read for its first 260 of 1014 lines (source rebinding and golden selector shifts); the rest rests on the executed checker.'},
    {'id': 'TOPIC-PACKAGE16', 'origin': 'source39 charter', 'disposition': 'VERIFIED-AS-AUTHOR-EVIDENCE (reconstructed, not relabelled)',
     'finalOwnerSelectors': [PKG + '/artifact-manifest.json', PKG + '/source-binding.v39.json', REBUILD_PATH],
     'evidence': {k: PACKAGE[k] for k in ('artifactManifestEqual', 'formalManifestVersusFilesOnlyProjection')},
     'consequence': 'See packageAssessment. The formal manifest and the files-only projection are different objects with equal file lists. The package was rebuilt from package15 plus the migration overlay against source39, and the exports and membership probes agree in content, not only in a passed flag.'},
]

# ------------------------------------------------------------------------------------------------ 107 rows
TCB = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18', 'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']
RES_TEXT = {
    'RES-EP13-01': ('new-39', 'Plan and derivation joins are still recomputed inside complete replay; source39 adds golden Runs (check-semantic-replay.v3 +138) that the full-replay and candidate-replay children use, and P39-TERM7 refuses a reminted receipt and mismatched plan/stage joins against those Runs.'),
    'RES-EP13-02': ('new-39', 'Depends on TCB-SCOPE-01. The source39 section 7 termination admission takes validate_shape/validate_attempt/validate_receipt from the host, so no answer-provenance claim against adversarial in-process regions is made.'),
    'RES-EP13-03': ('inherited-unchanged-38', 'The seven-vector measurement stays finite history; admission-and-qualification.md and the residual ledger are byte-identical 38->39.'),
    'RES-EP13-04': ('new-39', 'Depends on TCB-SCOPE-01. Closed input schemas remain the product admission; PolicyTestSuiteV2 refuses imperative keys and string expressions through the grammar (P39-POLICY P3), with the S39-02 universe-token gap recorded separately.'),
    'RES-EP13-05': ('new-39', 'The frozen subject was verified outside every author instrument: formal manifest, archive, 12,909 members and parent38 (P39-SUBJECT, P39-ARCHIVE).'),
    'RES-EP13-06': ('new-39', 'canonical.py is outside the delta. The reviewer\'s own C()/H() reproduced the owner canonical bytes (6,459 bytes) and the policy-test digests (P39-POLICY P4).'),
    'RES-EP13-07': ('inherited-unchanged-38', 'Seal and replay owners (security_lifecycle_model_v1.py, evaluator_replay_model.v3.py) are outside the delta; the analysis-seal child re-executed and passed on source39.'),
    'RES-EP13-08': ('inherited-unchanged-38', 'Bounded historical measurement; source39 claims no product proof over all PlanIntents.'),
    'RES-EP13-09': ('new-39', 'Provenance stays distinct from correctness: package semantic-controls1 still has owner ADMIT and semantic REFUSE on source39 (content-equal to the root receipt), and admit_repair_plan_v2 admits a reminted flipped descriptor by identity alone (P39-REPAIR2 observation).'),
    'RES-EP13-10': ('new-39', 'Author self-counters did not decide this review. The author control pt2 asserts that the typescript-v2 suite is accepted, and no author control covers S39-01; both SHOULDs came from independent discriminating probes.'),
    'RES-EP13-11': ('new-39', 'Historical failures stay recorded by cause: root-source39-final-reference.v1 (3 stale census assertions) stays a failure; v2 is the only all-pass receipt and is evidence only.'),
    'RES-EP13-12': ('new-39', 'Depends on TCB-SCOPE-01. The repair:2 retained view\'s declared class is authority by trust, not containment (P39-REPAIR2); no sole Python guard enters product authority.'),
    'RES-EP13-13': ('new-39', 'Depends on TCB-SCOPE-01. This review\'s probes deep-copy fixtures, restore the spied builder and the checker\'s _S37_CF global, and verify the copy after each run (fixture isolation only).'),
    'RES-EP13-14': ('inherited-unchanged-38', 'The differential census is not used as an oracle; unchanged.'),
    'RES-EP13-15': ('new-39', 'The C-2 v4 self-census is not elevated. The enumeration-plan schema change (membership order law, +7/-5) was diff-read and is exercised by the enumeration child, not by a census.'),
    'RES-EP13-16': ('new-39', 'Depends on TCB-SCOPE-01. Producer flags still cannot bypass replay; the section 7 admission derives class and reasons from the sealed Run, not from the host candidate.'),
    'RES-EP13-17': ('inherited-unchanged-38', 'Text-only disclosures remain text-only.'),
    'RES-EP13-18': ('new-39', 'Depends on TCB-SCOPE-01. Pruned-tree read custody relies on a host observation of which files a context read (security S3), stated as a TCB observation.'),
    'RES-EP13-19': ('new-39', 'Substantive semantic review on source39 with discriminating probes; pins and passing counts were not treated as acceptance, and two SHOULDs were found despite all six groups passing.'),
    'IR-EP13-NB-01': ('new-39', 'Depends on TCB-SCOPE-01. Each executed probe ran in-process with owner modules; containment is not claimed.'),
    'IR-EP13-NB-02': ('new-39', 'No name or punctuation scan decides scope: repair:2 matches unavailability by exact class identity (a subclass propagates, P39-REPAIR2), and the census correction names four codes explicitly instead of matching a prefix.'),
    'IR-EP13-NB-03': ('new-39', 'Depends on TCB-SCOPE-01. A trusted view can declare any exception class, even KeyError, as its unavailability class, and it maps. That is exactly why the boundary is trust rather than containment.'),
    'IR-EP13-NB-04': ('new-39', 'Depends on TCB-SCOPE-01; one TCB account is used for all thirteen rows.'),
    'IR-EP13-NB-05': ('new-39', 'Contradictory prose still needs substantive review: S39-01 is a section 5 sentence contradicted by the fixture, and ADV39-01 a section 10 sentence contradicted by the bytes. Neither was caught by a passing suite.'),
    'IR-EP13-NB-06': ('inherited-unchanged-38', 'Historical attacker cost preserved as history.'),
    'IR-EP13-NB-07': ('inherited-unchanged-38', 'The original environment is preserved; this review names its interpreter (-I -B) and pins.'),
    'AX6': ('new-39', 'Depends on TCB-SCOPE-01. The AX6 escape (evaluation-proof.v13) stays history; no 38->39 delta file claims same-process route-region protection, and replayed comparison remains reproducibility.'),
    'AX9': ('new-39', 'Depends on TCB-SCOPE-01. The AX9 escape stays history; the source39 additions (section 7 admission, repair:2 view) are typed data admission under a trusted evaluator, the correction\'s stated boundary.'),
    'MD5': ('new-39', 'Depends on TCB-SCOPE-01. The MD5 escape stays history; source39 adds no Python-containment mechanism and none enters product authority.'),
    'RX2c': ('new-39', 'Depends on TCB-SCOPE-01. The RX2c escape stays history; complete replay and the new golden Runs are reproducibility evidence, not containment.'),
}
AR_TEXT = {
    'AR-01': ('new-39', 'NO-NEW-ISSUE', 'Admission section 1 is byte-identical. The StepTermination law gains the delivery branches (common.schema +75, delta read), and P39-QUERY confirmed both runId directions.'),
    'AR-02': ('inherited-unchanged-38', 'NO-NEW-ISSUE', 'Admission sections 2-4 and qualification-gates are byte-identical 38->39; all 32 gates stay unperformed.'),
    'AR-03': ('new-39', 'NO-NEW-ISSUE', 'Security S3 was re-read complete and its A-5 pruned-tree paragraph is new. P39-NATIVE-CUSTODY confirmed VCS refusal at any depth and nested-package rows; the broad-row observation is a stated host TCB observation.'),
    'AR-04': ('new-39', 'NO-NEW-ISSUE', 'Security re-read complete on source39; the 38->39 diff (read) does not touch trust time. No probe.'),
    'AR-05': ('new-39', 'NO-NEW-ISSUE', 'Security re-read complete on source39; the 38->39 diff (read) does not touch root chain or revocation. No probe.'),
    'AR-06': ('new-39', 'NO-NEW-ISSUE', 'The platform admission text and carrier DDL are unchanged (grant-journal.carrier.v3.sql outside the delta); the security group passes.'),
    'AR-07': ('new-39', 'NO-NEW-ISSUE', 'Native re-read complete. U-4b membership order and the allowJs derivation were read and exercised by the executed consumer24 child; the native group passes 380/380.'),
    'AR-08': ('new-39', 'NO-NEW-ISSUE', 'The repair:2 constructor is new and confirmed by P39-REPAIR2 16/16. argvDigest is defined once (workflows-and-surfaces.md:1056-1062), and security S10 restates it with a cross-reference (security-and-lifecycle.md:1074).'),
    'AR-09': ('new-39', 'NO-NEW-ISSUE', 'identity-and-evidence.md changed (+114) and was re-read complete: stage-output registration, normalization map, body eligibility, foundation digest law, program predicate node. The foundation group passes; only pruned-tree custody was independently probed.'),
    'AR-10': ('new-39', 'NO-NEW-ISSUE', 'Presence knowledge is new; P39-COMPARISON 28/28 at helper level, and the comparison-knowledge child passes.'),
    'AR-11': ('new-39', 'NO-NEW-ISSUE', 'The import bridge types account targetUniverse null (execution-inputs contract read complete; schema diff read); the execution-inputs child passes. No independent import probe.'),
    'AR-12': ('new-39', 'NO-NEW-ISSUE', 'Native section 4 atom semantics are unchanged in substance; the atoms child passes. The policy-test verifier\'s divergence from the atom law under missing required evidence is S39-01, owned by workflows section 5.'),
    'AR-13': ('new-39', 'NO-NEW-ISSUE', 'The U-9 syntax-only fallback and its security S3 counterpart were probed (P39-NATIVE-CUSTODY); observations only.'),
    'AR-14': ('new-39', 'NO-NEW-ISSUE', 'ADV38-02 and ADV38-03 are closed at source level (P39-CARRIER-RO; commit-recovery-readonly text measured).'),
    'AR-15': ('inherited-unchanged-38', 'NO-NEW-ISSUE', 'The contract index README is byte-identical 38->39.'),
    'AR-16': ('new-39', 'CHANGES-REQUIRED (S39-01, S39-02)', 'ADV38-01 is closed by run-termination section 7 and the command carriers are confirmed. The policy test command has two SHOULD issues in its facts verifier and admission.'),
}
FW_TEXT = {
    'FW-01': 'discovery.rs must implement the security S3 pruned-tree read-set join and U-9 fallback; the source39 laws are confirmed at helper level (P39-NATIVE-CUSTODY). The observations on broad rows and case-variant segments are host obligations.',
    'FW-02': 'review.rs carries the review-brief command through query carriers; P39-QUERY confirmed the lawful control, truncated variant and another-run refusal.',
    'FW-03': 'analysis.rs hands the host observation to run-termination section 7; P39-TERM7 confirmed the admission order and joins.',
    'FW-04': 'imports.rs implements the typed-null targetUniverse account; confirmed by read and the execution-inputs child only.',
    'FW-05': 'comparison.rs implements presence knowledge true/false/null; confirmed at helper level (P39-COMPARISON).',
    'FW-06': 'finalization.rs projects the delivery laws (REQUIRED_PROJECTION_FAILED without runId, RENDERER_FAILED_AFTER_COMMIT with runId), confirmed by P39-QUERY. The ADV38-01 obligation is now a closed section 7 admission.',
    'FW-07': 'invocation.rs computes argvDigest over C(argv) (workflows section 7, security S10); read-confirmed and covered by an executed author control, not independently probed.',
    'FW-08': 'outcomes.rs implements the section 7 detail allowlist order; P39-TERM7 confirmed that unrelated registered details refuse.',
    'FW-09': 'review.rs candidates/inspect carriers were confirmed by P39-QUERY. The suppressedCount observation means the host must derive the count from the producing step.',
    'FW-10': 'repair.rs is the repair:2 constructor owner; P39-REPAIR2 confirmed refusal before descriptor and the exact-class unavailability mapping.',
    'FW-11': 'comparison.rs baseline.show carriers and pivot closure availability were confirmed by P39-QUERY controls.',
    'FW-12': 'review.rs review.produce-brief is a host query operation, and P39-QUERY confirmed host-only operations are not public.',
    'FW-13': 'configuration.rs recommend config2 proposals and CONFIG.INVALID policy-test admission routes were confirmed (P39-QUERY recommend joins; P39-POLICY P3).',
    'FW-14': 'discovery.rs recommend discovery units and the NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT refusal were confirmed (P39-QUERY, P39-NATIVE-CUSTODY).',
    'FW-15': 'policy.rs owns policy show/test. S39-01 and S39-02 route here and to the workflows section 5 reference verifier; the policy-show waiver resolution join refuses (P39-QUERY).',
}
DR_TEXT = {
    'DR-001': ('inherited-unchanged-38', 'current-source-map and the residual ledgers are byte-identical 38->39; this review refreshed the reading path on source39.'),
    'DR-002': ('new-39', 'The identity/evidence/proof chain gained section 7 host composition joins (receipt, inventory, plan, stage), confirmed by P39-TERM7, and identity-and-evidence was re-read complete.'),
    'DR-003': ('new-39', 'Read-only carrier routes are now machine-mapped (ADV38-02 closed, P39-CARRIER-RO). The 54 recovery cases remain unexecuted and real platform demonstration remains a release requirement.'),
    'DR-004': ('new-39', 'The native contract changed (U-4b, U-9, allowJs) and was re-read complete; the native group passes. ADV39-01 records the in-place registered schema edit.'),
    'DR-005': ('new-39', 'Executable custody reference groups pass on source39, and pruned-tree read custody was probed; native product carrier qualification is still required before release.'),
    'DR-006': ('new-39', 'The descriptor graph is unchanged: graph-query-3 bytes equal source38 (P39-QUERY) and the full-replay child passes.'),
    'DR-007': ('new-39', 'ADV38-01 is closed by section 7. The D9 published successor artifact remains a carried implementation-unit obligation, not a new blocker.'),
    'DR-008': ('inherited-unchanged-38', 'The applied retention posture is unchanged.'),
    'DR-009': ('new-39', 'The section 7 host observation is separate from the sealed Run record and does not alter it; attempt facts are validated by host callbacks, preserving lifetime neutrality.'),
    'DR-010': ('new-39', 'Bounded first-party composition is unchanged (prototype-report-inventory byte-identical). The policy-test verifier is reference evidence only; S39-01/02 concern authoring-test fidelity, not composition authority.'),
    'DR-011': ('inherited-unchanged-38', 'Individual dispositions exist; the blind implementer litmus follows final integration and is not closed here.'),
    'DR-011-R01': ('new-39', 'Fact-plane successor schemas grew (identity-schemas +142: normalization-specification-map, stage-output registeredBy, bodyEligibility), diff-read and exercised by the consumer24 child.'),
    'DR-011-R02': ('new-39', 'Imperative plugins stay outside D-371: PolicyTestSuiteV2 refuses undeclared members and string expressions with POLICY.IMPERATIVE_KEY_REFUSED (P39-POLICY P3).'),
    'DR-011-R03': ('new-39', 'plan2/exec-plan2 gained the membership order law (enumeration-plan schema and model diffs read); the enumeration child passes.'),
    'DR-011-R04': ('new-39', 'The carrierFormat axis now maps carrierFormat1/2 and fresh-install for read-only recovery (carrier-dispatch.v3.json:684-693).'),
    'DR-011-R05': ('inherited-unchanged-38', 'The Rust protocol major 3 is unchanged; the native group passes.'),
    'DR-011-R06': ('new-39', 'The identity-model diff (read complete) is additive admission law (+232/-9); typed close_run outcomes were re-exercised by the executed analysis-seal and query-projection children.'),
    'DR-011-R07': ('new-39', 'Query retained availability routes are unchanged in substance (query-projection-contract +2/-1); the query-projection child passes.'),
    'DR-011-R08': ('new-39', 'ADV38-01 closed; the D9 published successor artifact remains carried (DR-007).'),
    'DR-011-R09': ('new-39', 'Semantic IDs still exclude attempt identity: the section 7 observation carries attempts outside the Run, and policytest2 identity is a function of the suite alone (P39-POLICY P4).'),
    'DR-011-R10': ('inherited-unchanged-38', 'OPEN: this nonblind review cannot close the fresh blind implementer litmus.'),
    'DR-011-R11': ('new-39', 'ADV38-02/03 are closed at source level. Real platform durability is unmeasured and the 54 cases are not executed.'),
    'DR-011-R12': ('new-39', 'Depends on TCB-SCOPE-01, assessed once on source39.'),
    'DR-011-R13': ('new-39', 'Versioning successors are breaking majors, not relabels: PolicyTestSuiteV2 and repair:2 refuse major 1 typed (P39-POLICY P3, P39-REPAIR2).'),
    'DR-011-R14': ('inherited-unchanged-38', 'CFG-6/TM is unchanged.'),
    'DR-011-R15': ('new-39', 'The trusted request context stays host-only: HostQueryParams operations are not public operations (P39-QUERY).'),
    'DR-011-R16': ('inherited-unchanged-38', 'No executable report-hook admission: prototype-report-inventory and admission section 5 are byte-identical 38->39.'),
}
SR_TEXT = {
    'DR-201': 'The semantic-correctness owner row (Run versus command finalization, post-commit output failure) is byte-identical. Source39 adds the delivery failure laws in that area, confirmed by P39-QUERY.',
    'DR-202': 'The delivery/operations owner row (recovery, repair, loader TCB) is byte-identical. The source39 read-only carrier routes and repair:2 fall under it and are confirmed at source level.',
    'DR-203': 'The prototype-lessons owner row (PARTIAL-SCOPED) is byte-identical. No source39 delta file touches the prototype reference or its pin.',
    'DR-204': 'The V1/coop invariant owner row (exact selector/digest posture) is byte-identical. This review validated exact selectors and digests independently, and ADV39-01 is a digest-posture advisory in its spirit.',
    'DR-205': 'The small-core/components owner row (core/TCB boundaries) is byte-identical. TCB-SCOPE-01 remains coherent on source39.',
}


def row_out(r, basis, disposition, assessment, extra=None):
    o = {'id': r['id'], 'prior38Disposition': r['disposition'], 'disposition': disposition, 'assessmentBasis': basis, 'assessment': assessment}
    o.update(extra or {})
    o.update(FALSE_FLAGS)
    return o


def basis_check(basis, files):
    if basis == 'inherited-unchanged-38':
        for f in files:
            if not U.get(f, True):
                GAPS.append('inherited basis but governing file changed: ' + f)
    return basis


fD = [row_out(r, 'inherited-unchanged-38', 'CARRIED-NOT-REGRADED',
              '%s: identifier and prior root standing %s recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.' % (r['id'], r.get('priorRootStanding')),
              {'priorRootStanding': r.get('priorRootStanding')}) for r in v38['fDispositions']]
eR = []
for r in v38['evaluationResidualDispositions']:
    basis, text = RES_TEXT[r['id']]
    basis_check(basis, ['evaluation-residual-dispositions.proposed.json'])
    eR.append(row_out(r, basis, 'ASSESSED-CONSISTENT-GRADE-PENDING', text + ' The historical limitation is preserved; no historical guard is claimed repaired.',
                      {'proposedDisposition': r['proposedDisposition'], 'authorGrade': 'PENDING', 'sharedDependency': 'TCB-SCOPE-01' if r['id'] in TCB else None, 'residualRetained': True}))
aR = []
for r in v38['arDispositions']:
    basis, disp, text = AR_TEXT[r['id']]
    unchanged = sha(S38 + '/' + r['contract']) == sha(S39 + '/' + r['contract'])
    if basis == 'inherited-unchanged-38' and not unchanged and r['id'] != 'AR-02':
        GAPS.append('AR inherited basis but contract changed: ' + r['id'])
    aR.append(row_out(r, basis, disp, text, {'contract': r['contract'], 'selector': r['selector'], 'statusRecorded': r['statusRecorded'],
                                              'contractSha256': sha(S39 + '/' + r['contract']), 'contractUnchanged38to39': unchanged}))
fwR = []
for r in v38['fwDispositions']:
    fwR.append(row_out(r, 'new-39', 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED',
                       FW_TEXT[r['id']] + ' Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: %s); implementation not executed.' % (U['current-source-map.proposed.md'] and U['repository-file-inventory.v1.json']),
                       {'owners': r['owners'], 'milestone': r['milestone'], 'verificationStanding': r['verificationStanding']}))
dR = []
for r in v38['inheritedResidualDispositions']:
    basis, text = DR_TEXT[r['id']]
    basis_check(basis, ['inherited-residuals.proposed.md'])
    dR.append(row_out(r, basis, 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED', text + ' The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.'))
sR = [row_out(r, 'inherited-unchanged-38', 'ROUTING-ASSESSED-ONLY-NOT-APPLIED',
              SR_TEXT[r['id']] + ' Register 08 is byte-identical (%s). This review is an input to the integrated review and is not applied.' % U['08-decision-and-readiness-register.md']) for r in v38['scopedReviewOwnerDispositions']]
row_count = len(fD) + len(eR) + len(aR) + len(fwR) + len(dR) + len(sR)
if row_count != 107 or len(sR) != 5:
    GAPS.append('row count %d' % row_count)

TCB_OBJ = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': v38['sharedAssumptionTCBSCOPE01']['assumption'],
    'consequence': 'Rejecting or changing the assumption reopens all thirteen dependent rows together. It is a scope selection, not a containment guarantee, and repairs no historical attack. All thirteen author grades stay PENDING.',
    'dependentRows': TCB, 'dependentRowCount': len(TCB),
    'substantiveCurrentAssessment': [
        'It stays coherent as a scope selection on source39. Admission section 5 (no untrusted native/WASM, no imperative contributions or project hooks) is byte-identical 38->39: %s. prototype-report-inventory still admits no executable report hooks: %s.' % (U['admission-and-qualification.md'], U['prototype-report-inventory.md']),
        'The new in-process trust surfaces are consistent with the assumption and are stated as trust. The repair:2 retained view is a trusted host adapter whose declared class is authority, and it maps even KeyError (P39-REPAIR2). The section 7 termination admission takes host validate callbacks. Pruned-tree read custody names which files were read as a host TCB observation (security S3), and one broad installPath row authorizes every top-level package (P39-NATIVE-CUSTODY).',
        'Untrusted inputs remain inert typed data. PolicyTestSuiteV2 refuses imperative keys and string expressions through the grammar (P39-POLICY P3). Query carriers refuse cross-kind and failure envelopes (P39-QUERY). Read-only carrier opens refuse without changing a schema object in all %d scenarios (P39-CARRIER-RO).' % car_summary['scenarios'],
        'S39-01 and S39-02 are fidelity defects of the reference authoring-test verifier and admission. Neither is a trust-boundary violation, and neither changes the assumption.',
        'It remains unqualified. It rests on the authenticated closure/TCB inventory and provider process boundaries, and all 32 gates are unperformed (qualified=true count %d).' % gates_qualified_true,
    ],
    'reviewerPosition': 'NOT REJECTED',
    'standing': 'ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE39; final application adjudication not granted',
    'adjudicationOwner': 'The separate final application review, by a NEW other actual Claude origin that is not this origin (85a08aec-9d22-4ac6-8ec2-c10170e727d7) and not any author, design or blind origin; not adjudicated here.',
    'prior38Standing': v38['sharedAssumptionTCBSCOPE01'].get('standing'),
}

# ------------------------------------------------------------------------------------------------ evidence records
def ev(p, note):
    full = p if p.startswith('/') else B + '/' + p
    d = {'path': full, 'sha256': sha(full), 'note': note}
    try:
        j = J(full)
        for k in ('standing', 'passed', 'outcome'):
            if k in j and not isinstance(j[k], (dict, list)):
                d[k] = j[k]
    except Exception:
        pass
    return d


EVIDENCE = [
    ev('root-source39-final-reference.v1/reference-checks.json', 'FAILED root reference run (passed=false; foundation exit 1; check-identity 1593/3, stale detail census). Preserved as a failure; not relabelled.'),
    ev('root-source39-final-reference.v1/foundation.json', 'failing foundation report of v1'),
    ev('root-source39-final-reference.v2/reference-checks.json', 'root rerun after the census correction; the only current all-pass root receipt; evidence only'),
    ev('root-foundation-detail-census-correction.v1/assessment.json', 'root census correction assessment (four workflow details; 289 substrate closed)'),
    ev('root-foundation-detail-census-correction.v1/correction.diff', 'exact checker correction diff'),
    ev('root-final-owner-integration.v1/integration.json', 'root merge of reviewed author deltas (%d of %d files byte-equal to source39)' % (integ_equal, len(INTEG.get('files', [])))),
    ev('root-author-package-final39-rebuild.v1/rebuild-report.json', 'root reconstruction of package16 from package15 + migration overlay against source39 (author construction evidence)'),
    ev('author-package-final39-verification.v1/verification.json', 'root execution of the package16 author verifier; content-compared with this review\'s own run'),
    ev('claude-author-package-migration.v1/overlay/overlay-manifest.json', 'migration overlay manifest (inputs of the reconstruction)'),
    ev(PKG + '/source-binding.v39.json', 'package16 formal binding'),
    ev(V38PATH, 'source38 independent review (ACCEPT with ADV38-01..03); preserved unchanged; its acceptance does not accept source39'),
    ev(B + '/claude-independent-design.v38/review.md', 'source38 review markdown; preserved unchanged'),
]

preserved = []
inventory = []
for root, dirs, files in os.walk(RT):
    if '/work' in root[len(RT):]:
        continue
    for f in files:
        p = os.path.join(root, f)
        if p in (RT + '/review.json', RT + '/review.md'):
            continue
        inventory.append({'path': rel(p), 'bytes': os.path.getsize(p), 'sha256': sha(p)})
inventory.sort(key=lambda x: x['path'])

# ------------------------------------------------------------------------------------------------ assemble
MUST = []
verdict = 'ACCEPT' if not MUST and not SHOULD and not uncovered_nonpin and not GAPS else 'CHANGES_REQUIRED'
children_completion = {'referenceGroups': [{'name': r['name'], 'exitCode': r['exitCode'], 'timedOut': r['timedOut']} for r in group_rows],
                       'evaluator3Children': {k: v.get('exitCode') for k, v in children.items()},
                       'planning': {k: P[k]['exitCode'] for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                       'probeRuns': {pr['id']: (pr['execution'].get('exitCode') if pr['id'] != 'P39-PKG' else {k: v['exitCode'] for k, v in pr['execution'].items()}) for pr in PROBES if pr.get('execution')},
                       'stdoutOnlyHelpers': ['probes/summarize_receipts.py', 'probes/summarize_evidence.py', 'probes/ledger.py'],
                       'backgroundProcessesOutstanding': 0}
review = {
    'schema': 'opensip.independent-design-review.source39.v1',
    'reviewer': 'Claude (independent design review origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7; source39 charter; authored none of the reviewed bytes)',
    'standing': 'Substantive independent source-level review of frozen source39. Not inheritance of the source38 acceptance, not blind reconstruction, not application, readiness, implementation authorization or product qualification.',
    'verdict': verdict,
    'verdictBasis': ('Two SHOULD issues are unresolved, both in the policy test command: the facts verifier loses a known native hit when a required evidence kind is unavailable (S39-01), and admission does not apply the closed policy universe token map (S39-02). '
                     'Both were measured by discriminating probes against the production composition owner. No MUST issue. ADV38-01/02/03 are closed at source level; ADV39-01 is a non-blocking native advisory. '
                     'Subject, archive, members, parent38, delta, six pinned groups (%s), 17 evaluator3 children, planning and inventory checks, package16 content agreement and eight reviewer probes ran to completion. Source-level result only.') % ('all pass' if groups_ok else 'NOT ALL PASS'),
    'subjectManifestPath': LIVE39, 'subjectManifestSha256': EXPECT['manifest39'], 'verifiedManifest': verified_manifest, 'liveManifestSha256Measured': live39,
    'subjectArchivePath': ARCHIVE39, 'subjectArchiveSha256': EXPECT['archive39'], 'archiveSha256Measured': archive39, 'archiveVerification': archives,
    'subjectFileCount': SV.get('fileCount39'), 'subjectTotalBytes': SV.get('totalBytes39'),
    'parentManifestSha256': EXPECT['manifest38'], 'parentManifestSha256Measured': live38, 'parentUnchangedAndVerified': parent38_unchanged, 'delta38to39': delta_counts,
    'predecessorsPreserved': {'source38Review': {'path': V38PATH, 'sha256': sha(V38PATH), 'verdict': v38['verdict'], 'modifiedByThisReview': False, 'acceptanceInherited': False}},
    'readScope': {'fresh39Read': fresh, 'fresh39RangeRead': ranged, 'delta39Read': delta_reads, 'complete38ReadPlusComplete39Diff': via_diff,
                  'inheritedUnchanged38Read': inherited, 'changed38ReadNotFullyReread': changed_not_fresh,
                  'deltaFilesWithoutReadEntry': uncovered_delta, 'deltaPinLedgersVerifiedByExecutedPinGatesOnly': pin_paths, 'partialDiffReads': partial_diffs,
                  'ledger': {'path': 'receipts/read-ledger.jsonl', 'sha256': sha(REC + '/read-ledger.jsonl'), 'rows': len(ledger)},
                  'rule': 'Whole-file claims are made only for fresh39Read (every line read this charter) and inheritedUnchanged38Read (read completely under the source38 review and byte-identical now). complete38ReadPlusComplete39Diff is a complete predecessor read plus the exact complete diff, listed separately. delta39Read and fresh39RangeRead are not whole-file reads. Hashes were recomputed at build time against the frozen snapshot.'},
    'newMustIssues': MUST, 'newShouldIssues': SHOULD, 'advisories': ADVISORIES, 'observations': OBSERVATIONS,
    'findingDispositions': [{'id': 'S39-01', 'disposition': 'OPEN-SHOULD; route to the workflows policy test owner'}, {'id': 'S39-02', 'disposition': 'OPEN-SHOULD; route to the workflows policy test owner'},
                            {'id': 'ADV39-01', 'disposition': ADVISORIES[0]['disposition']}],
    'itemDispositions': ITEMS,
    'probes': PROBES,
    'commandReceipts': {'referenceGroups': group_rows, 'referenceGroupsPassed': groups_ok, 'evaluator3Children': children, 'evaluator3ChildrenAllExit0': children_ok,
                        'planning': {k: P[k] for k in ('check_implementation_planning', 'check_repository_file_inventory')}, 'planningCounts': PC, 'planningOk': planning_ok},
    'childCompletion': children_completion,
    'packageAssessment': dict(PACKAGE, result=('All 7 verifier groups (17 exports: checkpoint3 1, normalized-examples6 4, rust-selection-examples1 2, semantic-controls1 3, binding-controls 3, normalization-map-controls1 4; plus 7 queries) passed on this review\'s verified copy. '
                                               'The verification and every compared output file are content-equal to the root run, and the 9 native-v2 membership probes are content-equal to the root rebuild probe.'),
                              limits=['Author construction and self-consistency evidence; the verifier and native probe are author tools re-executed here, not an independent reconstruction.',
                                      'Reconstructed by root from package15 plus the migration overlay against source39. That is a rebuild, not a relabel: %d of 17 exports carry new RunIds.' % PACKAGE['reconstruction']['exportsWithNewRunId'],
                                      'Preserved package limitations: the TypeScript checkpoint compares a partial consumer helper with the owner; owner-derived positives are self-consistency; the helper leaves and/or/not unexercised and count-at-most/all-covered unimplemented; two-binding construction is incomplete with a single explicit binding.',
                                      'No compiler, provider, OS or process-isolation qualification; independent grades granted: %s.' % BIND.get('independentGradesGranted')]),
    'rootAndAuthorEvidence': {'standing': 'NONBLIND author/root evidence, not acceptance.', 'records': EVIDENCE, 'rootReference': REF, 'census': CENSUS},
    'planningLayer': {'normativeInputsV7Sha256': PC.get('v7Sha256'), 'inputs': PC.get('v7Inputs'), 'paths': PC.get('inventoryPaths'), 'packages': PC.get('inventoryPackages'),
                      'mappings': PC.get('coverageMappings'), 'mappingsSource38': v38_counts.get('coverageMappings'), 'plannedRecoveryCasesUnexecuted': PC.get('recoveryCasesNotExecuted'), 'milestones': 'M0-M6'},
    'mapSources': map_sources,
    'fDispositions': fD, 'evaluationResidualDispositions': eR, 'arDispositions': aR, 'fwDispositions': fwR,
    'inheritedResidualDispositions': dR, 'scopedReviewOwnerDispositions': sR, 'dispositionRowCount': row_count,
    'sharedAssumptionTCBSCOPE01': TCB_OBJ,
    'retained': {'residuals': len(eR), 'authorGradesPending': sum(1 for r in eR if r['authorGrade'] == 'PENDING'), 'condition2Obligations': 28,
                 'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 38->39: %s)' % U['08-decision-and-readiness-register.md'],
                 'qualificationGatesUnperformed': 32, 'qualificationGatesQualifiedTrue': gates_qualified_true, 'recoveryCasesNotExecuted': 54, 'condition5': 'NOT MET (not a design defect)',
                 'd9PublishedSuccessor': 'Carried implementation-unit obligation (DR-007 / DR-011-R08); not a new blocker.',
                 'finalApplication': 'Must be performed by a NEW other actual Claude origin, not this origin and not any author, design or blind origin.'},
    'authority': {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
                  'source38AcceptanceInherited': False, 'frozenInputsModified': False, 'applicationOrReadinessGranted': False, 'consumerArtifactsAccessedOrRepaired': False},
    'limitations': [
        'Nonblind review. The reviewer read the author package, author and root receipts and the source38 review. No blind consumer artifact, its implementation, or root replay diagnoses or oracles were accessed, used or repaired.',
        'Reference Python models over synthetic inputs; no product code exists. No compiler, provider, host, OS durability, process isolation or crypto is qualified. All 32 gates are unperformed and the 54 recovery cases are not executed (condition 5 NOT MET).',
        'Large changed reference code, schemas and ledgers were read as complete 38->39 diffs (delta39Read), not as whole files. Two diff reads are partial: implementation-coverage.v1.json (first 260 of 1014 diff lines, the rest resting on the executed planning checker) and run-termination-goldens.v1.json (diff lines 1-200 plus file lines 262-443, exercised by P39-TERM7 and the executed children). The five source-pins ledgers were not line-read; they are verified by the six executed pin gates.',
        'Several probes are helper-level, not full Runs: comparison presence knowledge (pure functions), native custody/fallback (owner functions), and the P1 composition side (a replica of the check-composition harness). The query and repair probes reuse the owner checker\'s module globals and admitted Runs. The carrier probe runs on the reference interpreter\'s in-memory SQLite with no stability observation.',
        'In-process monkeypatches (a spied shared builder; restoring the checker\'s rebound _S37_CF global) were always restored and verified.',
        'Probe attempts with harness defects were fixed and rerun, and their receipts were overwritten, so the failing outputs are not preserved as files. They were: policy-test (a duplicate-waiver negative broke waiverId order, reminted as w-zdup; a P4 row call missing its observed argument); carrier-readonly (IndexError importing check-carrier-v3 without argv; publish refused-by-ddl because the checker rebinds _S37_CF to prose); native-custody-fallback (custodyExcludedUnits rows must be {path, reason} objects). None was counted as a result.',
        'argvDigest, stage-output schema registration, the normalization specification map, body eligibility and the import bridge were confirmed by reading and executed author controls, not by independent probes.',
        'F-01..F-14 content lives outside the snapshot and was not re-derived.',
        'No grade, activation, application, readiness or implementation authorization is granted. The 30 residuals, 28 condition-2 obligations and the D9 successor obligation are retained.',
    ],
    'buildGaps': GAPS,
    'receiptInventory': inventory,
}

with open(RT + '/review.json', 'w', encoding='utf-8') as fh:
    json.dump(review, fh, indent=1, ensure_ascii=False)
    fh.write('\n')

# ------------------------------------------------------------------------------------------------ markdown
L = []
A = L.append
A('# Independent design review: frozen source39')
A('')
A('**Verdict: ' + verdict + '** (source level only; not blind reconstruction, application, readiness or product qualification).')
A('')
A(review['verdictBasis'])
A('')
A('## Subject')
A('')
A('- Manifest `' + LIVE39 + '`: SHA-256 `' + EXPECT['manifest39'] + '`; measured `' + str(live39) + '`; verifiedManifest=' + str(verified_manifest) + '.')
A('- Archive `' + ARCHIVE39 + '`: `' + EXPECT['archive39'] + '` (measured equal: ' + str(archive39 == EXPECT['archive39']) + '); ' + str(SV.get('fileCount39')) + ' files, ' + str(SV.get('totalBytes39')) + ' bytes.')
A('- Parent38 `' + EXPECT['manifest38'] + '` unchanged and verified: ' + str(parent38_unchanged) + '; delta ' + json.dumps(delta_counts) + '.')
A('- The source38 review (ACCEPT) is preserved unchanged, and its acceptance is not inherited.')
A('')
A('## Issues')
A('')
A('No MUST issue.')
A('')
for s in SHOULD:
    A('### ' + s['id'] + ' (SHOULD): ' + s['title'])
    A('')
    A(s['detail'])
    A('')
    A('- Required change: ' + s['requiredChange'])
    A('- Owner: ' + s['owner'])
    A('- Selectors: ' + '; '.join('`' + x + '`' for x in s['selectors']))
    A('- Measured: `' + json.dumps(s['measured'])[:1500] + '`')
    A('- Receipt: `' + s['receipt'] + '`')
    A('')
for adv in ADVISORIES:
    A('### ' + adv['id'] + ' (' + adv['severity'] + '): ' + adv['title'])
    A('')
    A(adv['detail'])
    A('')
    A('- Selectors: ' + '; '.join('`' + x + '`' for x in adv['selectors']))
    A('- Receipt: `' + adv['receipt'] + '`')
    A('- Disposition: ' + adv['disposition'])
    A('')
A('### Observations (not issues)')
A('')
for o in OBSERVATIONS:
    A('- ' + o)
A('')
A('## Item dispositions')
A('')
for it in ITEMS:
    A('### ' + it['id'] + ': ' + it['disposition'])
    A('')
    A('Origin: ' + it['origin'] + '.')
    A('')
    A(it['consequence'])
    A('')
    A('Owner selectors:')
    for s in it['finalOwnerSelectors']:
        A('- `' + s + '`')
    A('')
A('## Probes and command receipts')
A('')
for pr in PROBES:
    res = pr.get('result')
    A('- **' + pr['id'] + '** `' + pr['script'] + '`: ' + pr['claim'] + (' Result: ' + json.dumps(res) if res else '') + ' Receipts: ' + ', '.join('`' + r + '`' for r in pr['receipts']))
A('')
A('Reference groups (reference interpreter `-I -B`, verified disposable copy):')
A('')
A('| Group | Exit | Seconds | Script matches manifest | Copy unchanged |')
A('|---|---|---|---|---|')
for r in group_rows:
    A('| ' + r['name'] + ' | ' + str(r['exitCode']) + ' | ' + str(r['seconds']) + ' | ' + str(r['scriptMatchesManifest']) + ' | ' + str(r['copyUnchangedAfter']) + ' |')
A('')
A('Evaluator3 children (all exit 0: ' + str(children_ok) + '): ' + ', '.join(k + ' ' + json.dumps(v) for k, v in children.items()))
A('')
A('Planning: `' + P['check_implementation_planning']['stdout'].strip() + '`; inventory: `' + P['check_repository_file_inventory']['stdout'].strip() + '`; v7 `' + str(PC.get('v7Sha256')) + '`, ' + str(PC.get('v7Inputs')) + ' inputs, mappings ' + str(PC.get('coverageMappings')) + ' (source38 ' + str(v38_counts.get('coverageMappings')) + ').')
A('')
A('Root reference: v1 passed=' + str(REF['root-source39-final-reference.v1']['passed']) + ' (' + str(REF['root-source39-final-reference.v1']['checkIdentity']) + '; failures ' + json.dumps(REF['root-source39-final-reference.v1']['checkIdentityFailures']) + ') stays a failure; v2 passed=' + str(REF['root-source39-final-reference.v2']['passed']) + ' is the only current all-pass root receipt and is evidence only.')
A('')
A('## Package16')
A('')
pa = PACKAGE
A('- Artifact manifest `' + str(pa['artifactManifestSha256']) + '` (expected equal: ' + str(pa['artifactManifestEqual']) + '); ' + str(pa['filesListed']) + ' files listed, mismatched ' + str(len(pa['filesMismatched'])) + ', unlisted ' + str(len(pa['filesUnlisted'])) + '.')
A('- Formal manifest versus files-only projection: `' + json.dumps(pa['formalManifestVersusFilesOnlyProjection']) + '`.')
A('- Reconstruction: `' + json.dumps({k: v for k, v in pa['reconstruction'].items() if k not in ('inputs', 'commands')}) + '`.')
A('- Verification: `' + json.dumps({k: v for k, v in pa['verification'].items() if k != 'groups'}) + '`; native probe `' + json.dumps(pa['nativeV2Probe']) + '`.')
A('- ' + review['packageAssessment']['result'])
for lim in review['packageAssessment']['limits']:
    A('- ' + lim)
A('')
A('## TCB-SCOPE-01 (one shared assumption, ' + str(TCB_OBJ['dependentRowCount']) + ' dependent rows)')
A('')
A('Assumption: ' + TCB_OBJ['assumption'])
A('')
for s in TCB_OBJ['substantiveCurrentAssessment']:
    A('- ' + s)
A('')
A('Reviewer position: ' + TCB_OBJ['reviewerPosition'] + '. Consequence: ' + TCB_OBJ['consequence'] + ' Adjudication owner: ' + TCB_OBJ['adjudicationOwner'])
A('')
A('Dependent rows: ' + ', '.join(TCB) + '.')
A('')
A('## Disposition rows (' + str(row_count) + ')')
A('')
for title, rows in (('F', fD), ('Evaluation residuals', eR), ('AR', aR), ('FW', fwR), ('Inherited residuals', dR), ('Scoped review owners', sR)):
    A('### ' + title)
    A('')
    for r in rows:
        extra = (' [author grade PENDING]' if r.get('authorGrade') else '') + (' [depends on TCB-SCOPE-01]' if r.get('sharedDependency') else '')
        A('- **' + r['id'] + '** ' + r['disposition'] + ' (' + r['assessmentBasis'] + '; prior38 ' + r['prior38Disposition'] + ')' + extra + ': ' + r['assessment'])
    A('')
A('Every row: appliedByThisReview=false, finalApplicationOutcomeGranted=false.')
A('')
A('## Read map')
A('')
A(review['readScope']['rule'])
A('')
A('Fresh complete reads (source39):')
for e in fresh:
    A('- `' + e['path'] + '` ' + str(e['sha256'])[:16] + ' (' + str(e['lines']) + ' lines): ' + e['note'])
A('')
A('Fresh range reads (not whole-file):')
for e in ranged:
    A('- `' + e['path'] + '` ' + str(e['sha256'])[:16] + ': ' + ', '.join(e['ranges']))
A('')
A('Delta reads (38->39 diffs; not whole-file):')
for e in delta_reads:
    A('- `' + e['path'] + '` ' + str(e['sha256'])[:16] + ': ' + e['read'])
A('')
A('Complete source38 read plus complete 38->39 diff:')
for e in via_diff:
    A('- `' + e['path'] + '` ' + str(e['sha39'])[:16])
A('')
A('Inherited unchanged from source38 complete reads (hash recomputed):')
for e in inherited:
    A('- `' + e['path'] + '` ' + str(e['sha256'])[:16])
A('')
A('Scope residue: ' + json.dumps({'changed38ReadNotFullyReread': changed_not_fresh, 'deltaFilesWithoutReadEntry': uncovered_delta, 'pinLedgersVerifiedByPinGatesOnly': pin_paths}))
A('')
A('## Retained obligations and authority')
A('')
for k, v in review['retained'].items():
    A('- ' + k + ': ' + str(v))
A('- Authority: ' + json.dumps(review['authority']))
A('- Child completion: `' + json.dumps(children_completion) + '`')
A('')
A('## Limitations')
A('')
for lim in review['limitations']:
    A('- ' + lim)
if GAPS:
    A('')
    A('Build gaps: ' + json.dumps(GAPS))
with open(RT + '/review.md', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(L) + '\n')

print(json.dumps({'verdict': verdict, 'rows': row_count, 'gaps': GAPS, 'uncoveredDelta': uncovered_delta, 'changedNotFresh': changed_not_fresh, 'viaDiff': [e['path'] for e in via_diff],
                  'inherited': len(inherited), 'fresh': len(fresh), 'ranged': len(ranged), 'deltaReads': len(delta_reads),
                  'verifiedManifest': verified_manifest, 'parent38': parent38_unchanged, 'groupsOk': groups_ok, 'childrenOk': children_ok, 'planningOk': planning_ok,
                  'packageOk': package_ok, 'pkg': {k: v for k, v in PACKAGE['verification'].items() if k != 'groups'}, 'reconstruction': {k: v for k, v in PACKAGE['reconstruction'].items() if k not in ('inputs', 'commands')},
                  'projection': projection, 'census': CENSUS, 'ref': REF, 'adv3803': ITEMS[2]['evidence'], 'roMap': ro_map, 'carrier': car_summary,
                  'predDocExists': pred_doc_exists, 'mapSources': U, 'gatesQualifiedTrue': gates_qualified_true, 'gateRows': len(gate_rows), 'integEqual': integ_equal,
                  'reviewJsonSha256': sha(RT + '/review.json'), 'reviewMdSha256': sha(RT + '/review.md')}, indent=1, default=str))
