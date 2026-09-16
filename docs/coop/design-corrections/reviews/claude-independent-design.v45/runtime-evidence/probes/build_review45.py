"""Build review.json and review.md for the independent source45 whole-design successor review.

Measurement part; then executes, in these globals, build_review45_findings.py (issues, observations, prior-finding dispositions,
items, scope basis), build_review45_rows.py (107 rows, TCB object, retained, authority, limitations) and build_review45_emit.py
(assembly, gap checks, rendering). Reads frozen source45/44 bytes, this origin's completed source44 review (read-only history),
header-named root/codex/package evidence and this runtime's receipts. Writes only RT/review.json and RT/review.md."""
import glob, hashlib, json, os, re

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v45'
S45 = '/tmp/opensip-design-corrections/candidate-subject.v45'
S44 = '/tmp/opensip-design-corrections/candidate-subject.v44'
B = '/tmp/opensip-design-corrections'
REC = RT + '/receipts'
REVIEWS = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
LIVE45 = REVIEWS + '/candidate-subject.v45.json'
ARCHIVE45 = REVIEWS + '/candidate-source.v45.tar.gz'
LIVE44 = REVIEWS + '/candidate-subject.v44.json'
PKG = B + '/claude-author-package-successor.v22'
V44PATH = B + '/claude-independent-design.v44/review.json'
V44REC = B + '/claude-independent-design.v44/receipts'
CODEX = REVIEWS + '/codex-post-reset.v1/final-reference.v45/reference-checks.json'
ROOTREF = B + '/root-source45-final-reference.v1/reference-checks.json'
REBUILD_DIR = B + '/root-author-package-final45-rebuild.v1'
REBUILD = REBUILD_DIR + '/rebuild-report.json'
ROOTVER = REBUILD_DIR + '/work/verification/verification.json'
FORMAL = B + '/root-author-package-formal45-binding.v1/binding.json'
SRCBIND = PKG + '/source-binding.v45.json'
COMPANION = REVIEWS + '/root-source45-companion-checks.v2/checks.json'
ORIGIN = '85a08aec-9d22-4ac6-8ec2-c10170e727d7'
EXPECT = {'manifest45': '8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155',
          'manifest44': 'e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b',
          'archive45': '9536ebe3ffe27e2a99c7e02d8338738ae3d9a62a9000af4f3e5f5ce5793b909f',
          'archive44': 'c21d04914eaa07df967eeb945170a21d8ec8c7bc3c98573085522fab74b52bd5',
          'pkgManifest': '03e35dc61beb342b3691e57f728c643f3228e5e56ec4dee0178ed3fca0fc6d4d',
          'sourceBinding': '4910511ff6de54da2581bea0eac9d50d98349db7d135248fa6560529e3b26313',
          'rebuild': 'c3e0083216e28769a93798e8acb45e330c4a28c46913e42421ce5aef707279b4',
          'codex': '5dc0de6011ea8ff58d614f8e0f8c35420e197aabbbee64c9c6b9fb1df0a34bc4',
          'companion': '5efb2cd863e3c7d6ad80cf4da3faec4cf400742daab1c633f4e7ac0c3398b9a9',
          'v13': 'af228325492828b0ea5d6779601725a981bb467d0195e976a4247350c972c153',
          'review44': '33a5c2ce1e92d072a73d88c6e97bae693f75186e5e291b07b5e1258dc5d5c0a8'}
GAPS = []
DC = 'docs/coop/design-corrections/'
NAT = DC + 'native/'
FD = DC + 'foundation/'
WFD = DC + 'workflows/'
ARCHD = 'docs/v2/architecture/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'


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


def sha_opt(p):
    return sha(p) if os.path.exists(p) else None


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
    return sha_opt(a_root + '/' + p) is not None and sha_opt(a_root + '/' + p) == sha_opt(b_root + '/' + p)


def summ(v):
    if isinstance(v, dict):
        return {k: (len(x) if isinstance(x, (list, dict)) else x) for k, x in v.items()}
    return v


# ------------------------------------------------------------------------------------------------ subject
SV = J(REC + '/subject-verification.json')
live45, archive45 = sha(LIVE45), sha(ARCHIVE45)
ARCH = {rel(p): J(p) for p in sorted(glob.glob(REC + '/archive-verification*.json'))}
arch45 = [v for k, v in ARCH.items() if k.endswith(('source45.json', 'source45-pkg.json'))]
arch44 = [v for k, v in ARCH.items() if k.endswith('base44.json')]
archives_ok = len(arch45) == 2 and all(a['verified'] and a['archiveShaMatches'] and a['archiveSha256'] == EXPECT['archive45'] and a['manifestSha256'] == EXPECT['manifest45']
                                        and a['membersMatched'] == 12920 for a in arch45)
verified_manifest = bool(SV['manifest45']['matchesHeader'] and live45 == EXPECT['manifest45'] and SV['snapshot45']['verified'] and SV['counts45']['matchesHeader']
                         and SV['counts45']['matchesDeclared'] and SV['counts45']['fileCount'] == 12920 and SV['counts45']['totalBytes'] == 738315211
                         and archive45 == EXPECT['archive45'] and archives_ok)
parent44_ok = bool(SV['manifest44']['sha256'] == EXPECT['manifest44'] and sha(LIVE44) == EXPECT['manifest44'] and SV['snapshot44']['verified'] and SV['parentChain']['45declares44']
                   and len(arch44) == 1 and arch44[0]['verified'] and arch44[0]['archiveSha256'] == EXPECT['archive44'])
if not (verified_manifest and parent44_ok):
    GAPS.append('subject or parent44 verification incomplete')
DELTA = SV['delta']['44to45']
DCOUNTS = DELTA['counts']
if (DCOUNTS['changed'], DCOUNTS['added'], DCOUNTS['removed']) != (14, 1, 0):
    GAPS.append('delta counts differ from measurement: ' + json.dumps(DCOUNTS))
CHANGED_EXPECTED = {FD + 'evaluator3-source-pins.v1.json', FD + 'provider-target-attribution-return.schema.v2.json', FD + 'source-pins.v1.json', NAT + 'check_native_evidence.v2.py',
                    NAT + 'native-cases.v2.json', NAT + 'native_evidence_model.v2.py', NAT + 'provider-startup.schemas.v1.json', NAT + 'source-pins.v2.json',
                    DC + 'security/source-pins.v1.json', WFD + 'source-pins.v1.json', WFD + 'workflows-report.v1.json', ARCHD + 'implementation-coverage.v1.json',
                    ARCHD + 'implementation-planning-sources.v1.json', NE}
ADDED_EXPECTED = {ARCHD + 'implementation-normative-inputs.v13.json'}
paths44to45 = {r['path'] for k in ('changed', 'added', 'removed') for r in DELTA[k]}
if {r['path'] for r in DELTA['changed']} != CHANGED_EXPECTED or {r['path'] for r in DELTA['added']} != ADDED_EXPECTED:
    GAPS.append('delta population differs from the closed-world correction, prose clarification, pins, planning and reports')
DIFFSUM = J(REC + '/delta-diff-summary.json')
COPYVER = J(REC + '/copy-verification-final.json')
if not (set(COPYVER) == {'work/base44', 'work/source45', 'work/source45-pkg'} and all(v['verified'] for v in COPYVER.values())):
    GAPS.append('a disposable copy changed during the review or was not re-verified')
PINS = J(REC + '/source-pins45.json')
PIN_CHANGED_EXPECTED = {FD + 'provider-target-attribution-return.schema.v2.json', FD + 'source-pins.v1.json', NAT + 'check_native_evidence.v2.py', NAT + 'native-cases.v2.json',
                        NAT + 'native_evidence_model.v2.py', NAT + 'provider-startup.schemas.v1.json', NAT + 'source-pins.v2.json', DC + 'security/source-pins.v1.json',
                        WFD + 'source-pins.v1.json', NE}
PIN_UNPINNED_EXPECTED = {FD + 'evaluator3-source-pins.v1.json', WFD + 'workflows-report.v1.json', ARCHD + 'implementation-coverage.v1.json',
                         ARCHD + 'implementation-planning-sources.v1.json', ARCHD + 'implementation-normative-inputs.v13.json'}
pins_ok = (PINS['allPinsMatch'] and PINS['totalPinEntries'] == 6264 and set(PINS['changedPinUnion']) == PIN_CHANGED_EXPECTED and PINS['addedPinUnion'] == []
           and set(PINS['deltaFilesPinnedByNoLedger']) == PIN_UNPINNED_EXPECTED
           and all(not v['removedVs44'] and not v['deltaFilesPinnedButNotCurrent'] and not v['mismatchedAgainstManifest'] for v in PINS['ledgers'].values()))
if not pins_ok:
    GAPS.append('source pin verification not as measured')

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
            elif seg.strip() == 'complete' and lines:
                seen.update(range(1, lines + 1))
    return lines is not None and all(i in seen for i in range(1, lines + 1))


def group(kind):
    out = {}
    for r in ledger:
        if r['kind'] == kind:
            out.setdefault(r['path'], []).append(r)
    return out


fresh, ranged = [], []
for p, rows in sorted(group('fresh45Read').items()):
    cur, lines = sha(S45 + '/' + p), nlines(S45 + '/' + p)
    if any(r['sha256'] != cur for r in rows):
        GAPS.append('fresh read not current: ' + p)
    e = {'path': p, 'sha256': cur, 'lines': lines, 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows}), 'changed44to45': p in paths44to45}
    if covers_all(e['ranges'], lines):
        e.update(readClass='fresh45Read', read='complete: every line read this charter')
        fresh.append(e)
    else:
        e.update(readClass='fresh45RangeRead', read='named ranges only; not a whole-file read')
        ranged.append(e)
fresh_paths = {e['path'] for e in fresh}
delta_reads = []
for p, rows in sorted(group('delta44to45Read').items()):
    r = rows[-1]
    cur, dsha = sha(S45 + '/' + p), sha(RT + '/' + r['diff'])
    if cur != r['sha256'] or dsha != r['diffSha256']:
        GAPS.append('delta read not current: ' + p)
    delta_reads.append({'path': p, 'sha256': cur, 'lines': nlines(S45 + '/' + p), 'readClass': 'delta44to45Read', 'read': 'complete 44->45 diff; not a whole-file read',
                        'alsoFreshWholeFileRead': p in fresh_paths, 'diffReceipt': r['diff'], 'diffSha256': dsha, 'note': r['note']})
evidence_reads = [{'path': p, 'sha256': sha(p), 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows})} for p, rows in sorted(group('evidenceRead').items())]
delta_read_paths = {e['path'] for e in delta_reads}
CASES_STRUCT = J(REC + '/probes/cases-structure45.json')
structural_delta = [{'path': NAT + 'native-cases.v2.json', 'receipt': 'receipts/probes/cases-structure45.json', 'sha256': sha(REC + '/probes/cases-structure45.json'),
                     'standing': ('reindented reference data (57,096 text-diff lines): the complete parsed structures of source44 and source45 were compared - every top-level member, all 125 fixtures and all '
                                  '477 cases by id and order - and the two changed cases\' full expectation deltas were printed and read; this is a complete structural comparison, not a text read of the diff')}]
if not (CASES_STRUCT['cases']['changed'] == ['startup-ts2-pre-analyze-unavailable-host-derives-provider-unavailable-coverage', 'startup-rust3-pre-analyze-unavailable-host-derives-provider-unavailable-coverage']
        and not CASES_STRUCT['cases']['added'] and not CASES_STRUCT['cases']['removed'] and CASES_STRUCT['cases']['retainedOrderEqual']
        and not CASES_STRUCT['fixtures']['changed'] and not CASES_STRUCT['fixtures']['added'] and not CASES_STRUCT['fixtures']['removed']
        and all(CASES_STRUCT['topLevelNonCaseFixtureKeysEqual'].values())):
    GAPS.append('native-cases structural delta not as measured')
uncovered = sorted(paths44to45 - fresh_paths - delta_read_paths - {e['path'] for e in structural_delta})
for p in uncovered:
    GAPS.append('delta file without read entry: ' + p)
V44 = J(V44PATH)
if sha(V44PATH) != EXPECT['review44']:
    GAPS.append('source44 review hash differs from header')
RS44 = V44['readScope']
prior_complete = [dict(e, priorClass='fresh44Read') for e in RS44['fresh44Read']] + \
                 [dict(e, priorClass='inheritedUnchanged43Read') for e in RS44['inheritedUnchanged43Read']] + \
                 [dict(e, priorClass='complete43ReadPlusComplete44Diff') for e in RS44['complete43ReadPlusComplete44Diff']]
inherited, via_diff, changed_not = [], [], []
seen_prior = set()
for e in prior_complete:
    p = e['path']
    if p in fresh_paths or p in seen_prior:
        continue
    seen_prior.add(p)
    a, b = sha_opt(S44 + '/' + p), sha_opt(S45 + '/' + p)
    if a == b:
        inherited.append({'path': p, 'sha256': b, 'readClass': 'inheritedUnchanged44Read', 'priorClass': e['priorClass'],
                          'basis': 'counted as completely read by this origin\'s completed source44 review; byte-identical in source45 (hash recomputed now); not re-read this charter'})
    elif p in delta_read_paths:
        via_diff.append({'path': p, 'sha44': a, 'sha45': b, 'readClass': 'complete44ReadPlusComplete45Diff', 'priorClass': e['priorClass'],
                         'basis': 'source44 bytes counted as completely read plus the exact complete diff to source45; not a fresh whole-file read'})
    else:
        changed_not.append({'path': p, 'sha44': a, 'sha45': b, 'priorClass': e['priorClass']})
if changed_not:
    GAPS.append('a prior complete read changed without a current read: %s' % [c['path'] for c in changed_not])
prior_ranges = [{'path': e['path'], 'ranges': e.get('ranges'), 'unchanged44to45': same(S44, S45, e['path']), 'readClass': 'prior44RangeReadOnly'} for e in RS44['fresh44RangeRead']]
SEARCH_ONLY = [
    {'path': NE, 'lines': '2027, 2210-2213, 2221, 2237-2254, 3242-3255, 3352, 3368, 4175 (closed-world member search output; 2010-2039, 2195-2264 and 3151-3316 were then read)', 'standing': 'search output outside the ledgered ranges'},
    {'path': 'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'lines': '815, 835, 841-842, 938-964 (search output; 800-974 then read)', 'standing': 'search output within the later read range'},
    {'path': WFD + '{workflows_model.v1.py, workflow-cases.v1.json, schemas/repair.schema.json, schemas/imported-evidence.schema.json, schemas/evaluator3/repair.schema.json, repair_closed_world_selection.v1.py, command-inventory.v3.json, command-inventory.v1.json, check-workflow-projection.v3.py}; ' + FD + '{incoming-search.schema.v1.json, check-identity.py, check-atoms.v1.py, atom_model.v1.py, atom-evaluation-contract.v1.md}',
     'lines': 'file names only (ClosedWorldV2 member consumer search, files-with-matches output)', 'standing': 'file names only; consumer law read in workflows-and-surfaces 800-974'},
    {'path': NAT + 'check_native_evidence.v2.py', 'lines': 'def/marker lines 79-624 (search output); 40-119 and 264-313 then read; the changed region 573-594 read as the complete diff', 'standing': 'search output'},
    {'path': NAT + '{native_evidence_model.v2.py, native-evidence.schemas.v2.json}', 'lines': 'imports 12-21, def lines 1545/1645, ClosedWorldV2 1112/1116/1176 (search output)', 'standing': 'search output; 1545-1689 and 1110-1189 then read'},
    {'path': 'codex-post-reset.v1/final-reference.v45/*', 'lines': 'file listing (glob)', 'standing': 'names only; reference files compared by hash'},
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
NATIVE_STDOUT = open(REC + '/reference/native.stdout').read().strip()
if NATIVE_STDOUT != 'PASS: 477/477 cases; matrix cells 66; open objects 0; uncovered feedback []':
    GAPS.append('native group stdout differs from measurement')
P = J(REC + '/planning-checks.json')
PC = P['counts']
planning_ok = (P['check_implementation_planning']['exitCode'] == 0 and P['check_repository_file_inventory']['exitCode'] == 0 and PC['coverageMappings'] == 322
               and PC['coverageMappingsSource44'] == 322 and PC['layerSha256']['13'] == EXPECT['v13'] and PC['v13MatchesHeader'] and PC['v13MatchesManifestIndex']
               and not PC['layerMismatchedAgainstSource45']['13'] and PC['layerInputs']['13'] == 34 and PC['layerInputs']['12'] == 34
               and all(PC['priorLayersByteEqualToSource44'].values()) and PC['v13AddedVsV12'] == [] and PC['v13RemovedVsV12'] == []
               and PC['v13ChangedVsV12'] == [NAT + 'provider-startup.schemas.v1.json', NE]
               and PC['coverageSubjectMatchesV13'] and PC['coverageSourcesAllBoundByV13'] and PC['coverageSourcesStale'] == [] and PC['coverageSourceKeys'] == 34
               and PC['coverageSourcesChangedVs44'] == ['incorporated:provider-startup.schemas.v1.json', 'native-evidence']
               and PC['planningSourcesArchitectureSha256MatchesV13'] and PC['planningSourcesArchitectureFilesEqualV13'] and PC['planningSourcesPreviousFilesEqualV12']
               and PC['planningSourcesHistoryHashesMatchLayerBytes'] and PC['planningSourcesHistoryCount'] == 11 and PC['coverageRowIdsAddedVs44'] == [] and PC['coverageRowIdsRemovedVs44'] == []
               and PC['coverageRowsChangedVs44'] == sorted('native-evidence:%d' % i for i in range(10, 16)) and PC['coverageRowsChangedOtherThanSelectorLinesAndValueDigest'] == []
               and PC['inventoryPaths'] == 198 and PC['inventoryPackages'] == 20 and PC['recoveryCases'] == 54 and PC['recoveryCasesNotExecuted'] == 54
               and PC['coverageGroups']['reportFeatures'] == 24 and PC['milestoneOrder'] == ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6'] and PC['verificationStandings'] == ['not-executed']
               and all(PC['operationsCheckersByteEqualToSource44'].values())
               and PC['architectureDirFilesChangedVs44'] == [ARCHD + 'implementation-coverage.v1.json', ARCHD + 'implementation-normative-inputs.v13.json', ARCHD + 'implementation-planning-sources.v1.json'])
if not planning_ok:
    GAPS.append('planning checks or counts not as measured')
UNBOUND_NORMATIVE = sorted(p for p, v in PC['deltaDocumentsNotBoundByV13'].items() if v['selfDeclaresNormativeOrCurrent'])
RC = J(REC + '/reference-comparison.json')
reference_ok = (RC['codexReferenceChecks']['sha256'] == EXPECT['codex'] and RC['codexPassed'] and RC['codexSubjectManifestSha256'] == EXPECT['manifest45'] and RC['rootPassed']
                and all(v['stdoutFileEqualRoot'] and v['stdoutShaEqualRootRecord'] and v['rootSourceShaEqualsMineScript'] and v['stdoutFileEqualCodex'] for v in RC['groups'].values())
                and RC['childCount'] == 17 and RC['codexRunnerOriginalEqualsRoot']
                and all(RC['children'][n]['rootDiff']['equalAfterStrippingPathFieldsOnly'] for n in RC['childrenNotEqualRoot'])
                and all(RC['children'][n]['historicalMine44Diff']['equalAfterStrippingPathFieldsOnly'] for n in RC['childrenDifferingFromHistoricalMine44']))
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


PORTED = [('P45-PORTED-POLICY', 'probes/ported45_probe_policy_v40.py', 'ported45-policy-v40', 'policy-v40-on45.json', 'policy-v40-on44.json',
           'Ported (expectations unedited): policy.test known-hit, universe tokens, imported universe, policy.show, identity preimages.'),
          ('P45-PORTED-NATIVE', 'probes/ported45_probe_native_v40.py', 'ported45-native-v40', 'native-v40-on45.json', 'native-v40-on44.json', 'Ported: U-1 effective allowJs, nested Cargo, unitKind full-Run closure.'),
          ('P45-PORTED-RUNTERM', 'probes/ported45_probe_runterm_adv_v40.py', 'ported45-runterm-adv-v40', 'runterm-adv-v40-on45.json', 'runterm-adv-v40-on44.json',
           'Ported: run-termination keys, commit-inventory recipe over a closed Run, registered-schema account.'),
          ('P45-PORTED-QUERY', 'probes/ported45_probe_query_carriers.py', 'ported45-query-carriers', 'query-carriers.json', 'query-carriers.json', 'Ported: nine command carriers, twenty operations, delivery law.'),
          ('P45-PORTED-CARRIER', 'probes/ported45_probe_carrier_readonly.py', 'ported45-carrier-readonly', 'carrier-readonly.json', 'carrier-readonly.json', 'Ported: read-only carrier scenarios on real SQLite.'),
          ('P45-PORTED-COMPARISON', 'probes/ported45_probe_comparison_knowledge.py', 'ported45-comparison-knowledge', 'comparison-knowledge.json', 'comparison-knowledge.json', 'Ported: comparison presence knowledge.'),
          ('P45-PORTED-REPAIR2', 'probes/ported45_probe_repair2.py', 'ported45-repair2', 'repair2.json', 'repair2.json', 'Ported: repair:2 refusal order and retained-Run joins.'),
          ('P45-PORTED-TERM7', 'probes/ported45_probe_run_termination_s7.py', 'ported45-run-termination-s7', 'run-termination-s7.json', 'run-termination-s7.json', 'Ported: run-termination section 7 composition admission.'),
          ('P45-PORTED-CUSTODY', 'probes/ported45_probe_native_custody_fallback.py', 'ported45-native-custody-fallback', 'native-custody-fallback.json', 'native-custody-fallback.json', 'Ported: pruned-tree custody and U-9 fallback.'),
          ('P45-PORTED-CAPTURE-JOINS', 'probes/ported45_probe_capture_joins.py', 'ported45-capture-joins', 'capture-joins-on45.json', 'capture-joins-on44.json',
           'Ported ADV42-01 measurement: which owner refuses a captured unattributed view with a foreign planId and/or a non-provider producer.')]
PROBE_DEFS = [
    ('P45-SUBJECT', 'probes/verify_subject45.py', None, ['subject-verification.json', 'manifest45-index.json', 'manifest44-index.json'],
     'Formal manifest 8b4efbb0... and all 12,920 snapshot members (hash and length, none unlisted); parent44 manifest e873c8db... and all 12,919 members; declared chain 45->44; exact delta 44->45 (14/1/0).'),
    ('P45-ARCHIVE', 'probes/verify_archive_extract45.py', None, ['archive-verification.source45.json', 'archive-verification.source45-pkg.json', 'archive-verification.base44.json'],
     'Archive 9536ebe3... hashed; every member verified and extracted into two disposable copies (groups copy work/source45, probe copy work/source45-pkg); archive44 c21d0491... into work/base44 for old-versus-new comparison.'),
    ('P45-DELTA', 'probes/make_delta_diffs45.py', None, ['delta-diff-summary.json'], 'Unified diffs for all 14 changed files and the creation diff of the added v13 layer, both sides hash-verified.'),
    ('P45-GROUPS', 'probes/run_reference_groups45.py', None, ['reference/groups-report.all.json', 'reference/evaluator3.stdout', 'reference/foundation.json'],
     'Six pinned groups with /tmp/opensip-architecture-review-env/bin/python -I -B on the verified groups copy; copy re-verified before and after each group; 17 evaluator3 children.'),
    ('P45-REFERENCE-COMPARE', 'probes/compare_reference_v45.py', 'reference-comparison-v45', None,
     'This review\'s groups and children compared with root-source45-final-reference.v1, codex final-reference.v45 and this origin\'s historical source44 receipts (evidence only).'),
    ('P45-PINS', 'probes/verify_pins45.py', 'source-pins45', None, 'All 6,264 entries of the five source-pin ledgers against the formal manifest; changed, added and removed pins versus source44.'),
    ('P45-PLANNING', 'probes/run_planning_checks45.py', 'planning-checks-v45', None,
     'Planning and inventory checks (--check) plus v13/v12/v11/v10/v9/v8 layer, coverage, planning-source and history recounts against the exact parent source44, unbound changed normative documents and ADV44-01 binding state.'),
    ('P45-CASES-STRUCTURE', 'probes/compare_cases_structure45.py', 'cases-structure45', None, 'Parsed-structure comparison of native-cases.v2.json 44 versus 45 separating the reindent from the two semantic case changes.'),
    ('P45-CLOSED-WORLD', 'probes/probe_closed_world45.py', 'probe-closed-world45', 'closed-world45.json',
     'Focused discriminator: the pre-analysis closedWorld derived from published law (4.5 forced fields separated from 9.7 fixed fields), the published value read three ways with its canonical bytes, both languages through the source45 exchange with admission, byte-identical entries and coverage ids against the source44 exchange, the corrected case boundary (a law-member mutation detected on source45, the equivalent helper mutation undetected on source44), and unchanged schema shapes.'),
    ('P45-CHECKER-BINDING', 'probes/probe_checker_binding45.py', 'probe-checker-binding45', 'checker-binding45.json',
     'Scratch-copy mutation discriminator of the native checker: unmutated pass, then the startup-law member, the section 9.7 record and the retained helper each mutated alone with native pins regenerated inside scratch, each refused with its exact binding fault, then restored pass and byte restoration.'),
    ('P45-PORT', 'probes/port_v44_probes45.py', 'port-v44-probes', None, 'Mechanical port of the source44 scope probes: runtime paths and receipt names only; residual source44 runtime mentions none.'),
] + [(pid, script, runname, receipt, claim) for pid, script, runname, receipt, _, claim in PORTED] + [
    ('P45-PORTED-VS44', 'probes/compare_ported45_vs44.py', 'ported45-vs44', None, 'Every ported probe receipt compared case by case with this origin\'s source44 receipt of the same probe.'),
    ('P45-STARTUP-REEXEC-PORT', 'probes/port_startup_reexec45.py', 'port-startup-reexec45', None, 'Mechanical port of the source44 startup discriminator for re-execution on source45 (paths and receipt name only).'),
    ('P45-STARTUP-REEXEC', 'probes/reexec45_probe_startup.py', 'reexec45-startup', 'startup44-reexec-on45.json',
     'Re-execution (corroboration, not fresh assessment) of the 162-row source44 startup discriminator on source45, compared row by row with the source44 receipt.'),
    ('P45-PACKAGE22', 'probes/probe_package_v22.py', 'probe-package-v22', 'package-v22.json',
     'Package v22 manifest, formal45 versus files-only projection, overlay provenance from package15, packages 16-21 preserved, pre-binding package retained, export stores byte-equal to package21, RunIds equal to the source44 rebuild, content equality with the root rebuild verification and probe, exact normalization-map negatives.'),
    ('P45-COPIES-FINAL', 'probes/verify_copies45.py', 'copies-final', None, 'All three disposable copies re-verified against their formal manifests after every probe and checker.'),
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
PBY['P45-PORT']['receipts'] = {'receipts/probe-port45.json': sha(REC + '/probe-port45.json')}
PBY['P45-PORTED-VS44']['receipts'] = {'receipts/ported45-vs44.json': sha(REC + '/ported45-vs44.json')}
PBY['P45-PINS']['receipts'] = {'receipts/source-pins45.json': sha(REC + '/source-pins45.json')}
PBY['P45-PLANNING']['receipts'] = {'receipts/planning-checks.json': sha(REC + '/planning-checks.json')}
PBY['P45-REFERENCE-COMPARE']['receipts'] = {'receipts/reference-comparison.json': sha(REC + '/reference-comparison.json')}
PBY['P45-COPIES-FINAL']['receipts'] = {'receipts/copy-verification-final.json': sha(REC + '/copy-verification-final.json')}
PBY['P45-CASES-STRUCTURE']['receipts'] = {'receipts/probes/cases-structure45.json': sha(REC + '/probes/cases-structure45.json')}
PBY['P45-STARTUP-REEXEC-PORT']['receipts'] = {'receipts/startup-reexec-port45.json': sha(REC + '/startup-reexec-port45.json')}
PORTED_EQUAL = {}
for pid, _, _, receipt, receipt44, _ in PORTED:
    cur, old = rows_of(receipt), {r['case']: r for r in J(V44REC + '/probes/' + receipt44)['rows']}
    differ = [c for c in cur if c in old and json.dumps(cur[c]['observed'], sort_keys=True) != json.dumps(old[c]['observed'], sort_keys=True)]
    PORTED_EQUAL[pid] = {'rows': len(cur), 'sameCaseSetAsSource44': set(cur) == set(old), 'observedDifferFromSource44': differ,
                         'historicalReceipt44': 'claude-independent-design.v44/receipts/probes/' + receipt44}
    if differ or set(cur) != set(old) or any(not r['ok'] for r in cur.values()):
        GAPS.append('ported probe observations differ from source44: ' + pid)
PORT = J(REC + '/probe-port45.json')
if any(r['residualV44RuntimeMentions'] for r in PORT) or len(PORT) != 10:
    GAPS.append('ported probe still names the source44 runtime')
REEXEC = rows_of('startup44-reexec-on45.json')
START44 = {r['case']: r for r in J(V44REC + '/probes/startup44.json')['rows']}
reexec_differ = [c for c in REEXEC if c in START44 and json.dumps(REEXEC[c]['observed'], sort_keys=True) != json.dumps(START44[c]['observed'], sort_keys=True)]
REEXEC_EQUAL = {'rows': len(REEXEC), 'sameCaseSet': set(REEXEC) == set(START44), 'observedDifferFromSource44': reexec_differ}
if reexec_differ or set(REEXEC) != set(START44):
    GAPS.append('startup re-execution differs from source44')
PKG_RUNS = {'verify-package.py': run_record('package-v22-verify', PKG + '/verify-package.py'),
            'probe-native-v2.py': run_record('package-v22-probe-native-v2', PKG + '/probe-native-v2.py')}
CW, CB, PK, CJ = rows_of('closed-world45.json'), rows_of('checker-binding45.json'), rows_of('package-v22.json'), rows_of('capture-joins-on45.json')

# ------------------------------------------------------------------------------------------------ owner map
MAP_FILES = [NE, NAT + 'provider-handshake.schemas.v1.json', NAT + 'provider-startup.schemas.v1.json', NAT + 'typescript-protocol2-order.v1.json', NAT + 'provider_wire_model.v1.py',
             NAT + 'provider_startup_model.v1.py', NAT + 'protocol3-transitions.v1.json', NAT + 'native_evidence_model.v2.py', NAT + 'check_native_evidence.v2.py', NAT + 'native-cases.v2.json',
             NAT + 'native-evidence-report.v2.json', NAT + 'native-evidence.schemas.v2.json', NAT + 'native-capability-matrix.v2.json', NAT + 'fact-batch.schema.v3.json',
             NAT + 'occupancy-companion.schema.v1.json', NAT + 'dispatch-binding.schema.v1.json', NAT + 'source-pins.v2.json',
             'docs/coop/artifacts/delivery.v2.json', 'docs/coop/artifacts/rust-provider-protocol.v2.json', 'docs/coop/artifacts/resolved-inputs.v2.json',
             FD + 'provider-target-attribution-return.schema.v2.json', FD + 'provider_attribution_return_model.v2.py', FD + 'execution-inputs-contract.v1.md', FD + 'execution-inputs.schema.v1.json',
             FD + 'execution_inputs_model.v1.py', FD + 'execution_inputs_fixture.v3.py', FD + 'check-execution-inputs.v1.py', FD + 'enumeration-contract.v1.md', FD + 'enumeration-plan.schema.v1.json',
             FD + 'enumeration_model.v1.py', FD + 'check-enumeration.v1.py', FD + 'evaluator_input_model.v3.py',
             FD + 'identity-model.v3.py', FD + 'identity-schemas.v3.json', FD + 'evaluator-composition-contract.v3.md', FD + 'evaluator_replay_model.v3.py',
             FD + 'run-termination-contract.v1.md', FD + 'run_termination_model.v1.py', FD + 'canonical.py', FD + 'source-pins.v1.json', FD + 'evaluator3-source-pins.v1.json',
             WFD + 'query-projection-contract.v3.md', WFD + 'query_projection_model.v3.py', WFD + 'check-query-projection.v3.py', WFD + 'query_surface_projection.v3.py',
             WFD + 'schemas/evaluator3/graph-query.schema.json', WFD + 'schemas/evaluator3/repair.schema.json', WFD + 'command-inventory.v3.json', WFD + 'workflows-report.v1.json',
             WFD + 'source-pins.v1.json', WFD + 'policy_test_model.v3.py', WFD + 'repair_closed_world_selection.v1.py', DC + 'security/source-pins.v1.json',
             DC + 'security/carrier-dispatch.v3.json', DC + 'public-detail-registry.v1.json',
             DC + 'evaluation-residual-dispositions.proposed.json', DC + 'inherited-residuals.proposed.md', DC + 'current-source-map.proposed.md', DC + 'qualification-gates.proposed.json',
             ARCHD + '08-decision-and-readiness-register.md', ARCHD + 'commit-recovery-readonly.v3.md', ARCHD + 'prototype-report-inventory.md', ARCHD + 'repository-file-inventory.v1.json',
             ARCHD + 'implementation-coverage.v1.json', ARCHD + 'implementation-planning-sources.v1.json', ARCHD + 'implementation-normative-inputs.v12.json', ARCHD + 'implementation-normative-inputs.v13.json',
             ARCHD + '14-repository-and-module-layout.md', ARCHD + 'implementation-boundaries-and-build-plan.md', 'docs/operations/check_implementation_planning.py',
             'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md', 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
             'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'docs/v2/contracts/product-v1/README.md']
MAP = {p: {'sha256': sha(S45 + '/' + p), 'sha44': sha_opt(S44 + '/' + p), 'unchanged44to45': same(S44, S45, p), 'inDelta': p in paths44to45} for p in MAP_FILES}
for p, v in MAP.items():
    if v['unchanged44to45'] == v['inDelta']:
        GAPS.append('map/delta disagreement: ' + p)
U = {os.path.basename(p): v['unchanged44to45'] for p, v in MAP.items() if not p.endswith('source-pins.v1.json') and 'schemas/evaluator3/repair' not in p}
U['evaluator3/repair.schema.json'] = MAP[WFD + 'schemas/evaluator3/repair.schema.json']['unchanged44to45']
GATES = J(S45 + '/' + DC + 'qualification-gates.proposed.json')['items']
gates_true = sum(1 for g in GATES if g.get('qualified') is True)
REG = open(S45 + '/' + ARCHD + '08-decision-and-readiness-register.md', encoding='utf-8').read().splitlines()
cond2_ok = '28 existing rows' in ' '.join(REG[384:391])
if len(GATES) != 32 or gates_true != 0 or not cond2_ok:
    GAPS.append('gates or condition-2 measurement differs')

# ------------------------------------------------------------------------------------------------ root/package evidence
MV = J(RT + '/work/package-v22-verify/verification.json')
NV = J(RT + '/work/probe-native-v2.json')
FB = J(FORMAL)
RB = J(REBUILD)
vgroups = [{'group': g['group'], 'count': g.get('count'), 'passed': g.get('passed'), 'exitCode': g.get('exitCode')} for g in MV['groups']]
nm_controls = next(g['observed'] for g in MV['groups'] if g['group'] == 'normalization-map-controls1')
export_count = sum(g['count'] or 0 for g in vgroups if g['group'] != 'query')
query_count = next((g['count'] for g in vgroups if g['group'] == 'query'), None)
native_runs = [r['name'] if isinstance(r, dict) else r[0] for r in NV['runs']]
run_ids = sorted(e['runId'] for e in RB['exportComparison'])
pkg_ok = (sha(PKG + '/artifact-manifest.json') == EXPECT['pkgManifest'] and all(v['ok'] for v in PK.values()) and export_count == 17 and query_count == 7
          and len(native_runs) == 9 and NV['passed'] is True and all(g['passed'] for g in vgroups) and sha(SRCBIND) == EXPECT['sourceBinding'] and sha(REBUILD) == EXPECT['rebuild'])
if not pkg_ok:
    GAPS.append('package v22 verification not as recorded')
rid_row = PK.get('measured-source45-RunIds-and-export-digests-equal-the-source44-package21-rebuild', {})
PACKAGE = {
    'package': PKG, 'artifactManifestSha256': sha(PKG + '/artifact-manifest.json'), 'expectedArtifactManifestSha256': EXPECT['pkgManifest'],
    'sourceBindingV45Sha256': sha(SRCBIND), 'expectedSourceBinding': EXPECT['sourceBinding'],
    'filesOnlySourceProjectionSha256': sha(PKG + '/source-manifest.json'), 'formalSubjectManifestSha256': live45,
    'rebuildReportSha256': sha(REBUILD), 'expectedRebuildReport': EXPECT['rebuild'], 'rootRebuildVerificationSha256': sha(ROOTVER), 'formalBindingRecordSha256': sha(FORMAL),
    'preBindingPackageManifestSha256': RB['packageManifestSha256'],
    'historyPackageManifests': {v: sha(B + '/claude-author-package-successor.v%s/artifact-manifest.json' % v) for v in ('15', '16', '17', '18', '19', '20', '21')},
    'probeRows': {k: {'ok': v['ok'], 'observed': v['observed']} for k, v in PK.items() if v.get('kind') != 'record'},
    'verificationGroups': vgroups, 'exports': export_count, 'queries': query_count, 'normalizationMapControls': nm_controls,
    'nativeV2Probe': {'runs': native_runs, 'passed': NV['passed'], 'unitsVsDiscoveryDisagreements': NV['unitsVsDiscoveryDisagreements']},
    'measuredRunIds': run_ids, 'runIdsAndExportDigestsEqualSource44': bool(rid_row) and rid_row.get('ok') is True,
    'formalBindingPreviousSource44Comparison': {'rows': len(FB.get('previousSource44Comparison', [])), 'allSameRunIdAndBytes': all(c['sameRunId'] and c['sameExportSha256'] for c in FB.get('previousSource44Comparison', []))},
    'toolRuns': PKG_RUNS, 'verified': pkg_ok,
    'result': ('Package v22 verified as author evidence. All %d files match artifact manifest 03e35dc6...; the formal45 manifest 8b4efbb0... and the files-only projection %s... are different objects with equal file members (equal to this review\'s own verified manifest45 index), and the package copy of the formal manifest equals the live one. '
               'The rebuild (report c3e00832...) ran on frozen candidate-subject.v45 from package15 constructors (6a8d4fec...) plus the native-v2 migration overlay (overlay base digests match retained package15); packages 16-21 remain unchanged history, and the pre-binding package 50ea28c7... is retained inside package22 and equals the rebuild output. '
               'Metadata binding changed no export store or current replay helper byte. Every current export store is byte-equal to package21 at the same path, and the 17 measured RunIds and export digests equal the source44 rebuild, so the source45 correction does not alter any retained identity and nothing was reminted. '
               'This review re-executed verify-package.py and probe-native-v2.py on its own verified source45 copy: groups %s; %d exports and %d queries. The verification of bound package22 equals the root verification of the pre-binding package except package identity and file count, every other output file is byte-equal, and the 9 membership comparisons are content-equal to the root rebuild probe.'
               % (len(J(PKG + '/artifact-manifest.json')['files']), sha(PKG + '/source-manifest.json')[:8], ', '.join('%s %s (passed %s, exit %s)' % (g['group'], g['count'], g['passed'], g['exitCode']) for g in vgroups), export_count, query_count or 0)),
    'limits': ['Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.',
               'Four TypeScript normalization-map negatives ARE executed (exact refusals below). The Rust map negative is unexercised.',
               'The partial and/or/not consumer helper remains unexercised; count-at-most/all-covered remain unimplemented; two-binding qualification is incomplete.',
               'No compiler, provider, OS or process-isolation qualification; independent grades granted: 0; all 30 author-proposed grades stay PENDING final application.'],
}
CODEXD, ROOTD = J(CODEX), J(ROOTREF)
COMP = J(COMPANION)
planning_stdout_equal_companion = (len(COMP['checks']) == 2 and COMP['checks'][0]['stdout'] == P['check_implementation_planning']['stdout'] and COMP['checks'][1]['stdout'] == P['check_repository_file_inventory']['stdout'])
EVIDENCE = {
    'standing': 'NONBLIND header-named evidence, not acceptance. The charter\'s source-only correction rationale was read as author statement and re-measured; no author runtime history, blind consumer artifact, export, helper, report or root blind outcome was read.',
    'records': [
        {'path': COMPANION, 'sha256': sha(COMPANION), 'expected': EXPECT['companion'], 'stdoutEqualsThisReview': planning_stdout_equal_companion,
         'note': 'root companion planning/inventory checks v2 (v1 lacked --source and is retained); executed from a pre-freeze working tree; stdout text equal to this review\'s own checks'},
        {'path': CODEX, 'sha256': sha(CODEX), 'expected': EXPECT['codex'], 'passed': CODEXD.get('passed'), 'subjectManifestSha256': CODEXD.get('subjectManifestSha256'),
         'note': 'current final45 reference receipts named by the header; runner-original equals the root reference-checks: %s' % RC['codexRunnerOriginalEqualsRoot']},
        {'path': ROOTREF, 'sha256': sha(ROOTREF), 'passed': ROOTD.get('passed'), 'executionSourceRoots': RC['rootExecutionSourceRoots'],
         'note': 'actual root execution root-source45-final-reference.v1 (6 groups, 17 children); executed from a pre-freeze working tree whose script bytes equal the frozen source45 bytes'},
        {'path': REBUILD, 'sha256': sha(REBUILD), 'expected': EXPECT['rebuild'], 'note': 'root reconstruction of package v22 from package15 plus overlay on frozen candidate-subject.v45 (author construction evidence)'},
        {'path': ROOTVER, 'sha256': sha(ROOTVER), 'note': 'root rebuild verification of the pre-binding package; equal to this review\'s verification of bound package22 except package identity and file count'},
        {'path': FORMAL, 'sha256': sha(FORMAL), 'note': 'root formal45 metadata binding record with the measured source44 comparison (not header-bound)'},
        {'path': SRCBIND, 'sha256': sha(SRCBIND), 'expected': EXPECT['sourceBinding'], 'note': 'package 22 source binding'},
        {'path': V44PATH, 'sha256': sha(V44PATH), 'expected': EXPECT['review44'], 'note': 'this origin\'s completed source44 review; read-only history for prior rows, dispositions and read scope'},
    ],
}
for r in EVIDENCE['records']:
    if r.get('expected') and r['sha256'] != r['expected']:
        GAPS.append('evidence hash differs from header: ' + r['path'])

for part in ('build_review45_findings.py', 'build_review45_rows.py', 'build_review45_emit.py'):
    path = RT + '/probes/' + part
    exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), globals())
