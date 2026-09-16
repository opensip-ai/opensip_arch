"""Build review.json and review.md for the independent source44 whole-design successor review.

Measurement part; then executes, in these globals, build_review44_findings.py (issues, observations, prior-finding dispositions,
items, scope basis), build_review44_rows.py (107 rows, TCB object, retained, authority, limitations) and build_review44_emit.py
(assembly, gap checks, rendering). Reads frozen source44/43 bytes, this origin's completed source43 review (read-only history),
header-named root/codex/package evidence, the source-only author reports, the root clarification and companion checks, and this
runtime's receipts. Writes only RT/review.json and RT/review.md. Hashes recomputed now."""
import glob, hashlib, json, os, re

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v44'
S44 = '/tmp/opensip-design-corrections/candidate-subject.v44'
S43 = '/tmp/opensip-design-corrections/candidate-subject.v43'
B = '/tmp/opensip-design-corrections'
REC = RT + '/receipts'
REVIEWS = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
LIVE44 = REVIEWS + '/candidate-subject.v44.json'
ARCHIVE44 = REVIEWS + '/candidate-source.v44.tar.gz'
LIVE43 = REVIEWS + '/candidate-subject.v43.json'
PKG = B + '/claude-author-package-successor.v21'
V43PATH = B + '/claude-independent-design.v43/review.json'
V43REC = B + '/claude-independent-design.v43/receipts'
CODEX = REVIEWS + '/codex-post-reset.v1/final-reference.v44/reference-checks.json'
ROOTREF = B + '/root-source44-final-reference.v1/reference-checks.json'
REBUILD_DIR = B + '/root-author-package-final44-rebuild.v1'
REBUILD = REBUILD_DIR + '/rebuild-report.json'
ROOTVER = REBUILD_DIR + '/work/verification/verification.json'
FORMAL = B + '/root-author-package-formal44-binding.v1/binding.json'
SRCBIND = PKG + '/source-binding.v44.json'
WIRE_MD = REVIEWS + '/claude-provider-wire43-correction.v1/review.md'
WIRE_JSON = REVIEWS + '/claude-provider-wire43-correction.v1/review.json'
STARTUP_MD = REVIEWS + '/claude-provider-startup43-correction.v1/review.md'
STARTUP_JSON = REVIEWS + '/claude-provider-startup43-correction.v1/review.json'
CLARIFY = REVIEWS + '/root-startup43-scope-clarification.v1/clarification.json'
COMPANION = REVIEWS + '/root-source44-companion-checks.v1/checks.json'
ORIGIN = '85a08aec-9d22-4ac6-8ec2-c10170e727d7'
EXPECT = {'manifest44': 'e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b',
          'manifest43': 'db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d',
          'archive44': 'c21d04914eaa07df967eeb945170a21d8ec8c7bc3c98573085522fab74b52bd5',
          'archive43': 'd1ff8312d6a5540a977e54cfe8e24dd4865f8b09e6c432e42fd0d651387b66fa',
          'pkgManifest': 'e5639aa3f16399f180cde9e43f59e64698eaaa851f2a15f51a63dd8d0bf5d245',
          'sourceBinding': 'ba2e92467ea18facbb2a50797b8ee5b0eee9286b16727149ee4bc4e19bf5046a',
          'rebuild': '332e5d51f7d781b119811f6eabfbc75b9eddc11fef2b139a12075bfdc7c34808',
          'codex': '77ba7a64ae9b009cb77c912686aeacb2976e057c4760132c214afe14862708e7',
          'companion': 'e1d797d210744d72063870b3f415bc70d77c8830542303b5f66725757bdd3f4f',
          'v12': '2ef6d70f900181990813e8d12a609aed93f3d031f5d9efe15c014d487ccbbf7c',
          'review43': '59e007443caf1206ee0eb1b2ef0def526c01dd43a9686811781e5357eb576934',
          'wireMd': '8ce242fdf8f9f7524030ede6596419b371975c10a575b8f76536df608dd8cc0c',
          'wireJson': '6625215cb979d64e8b12b474cc736548b2541d1ae364a7551b29d45e04fff06e',
          'startupMd': '8c503c62ec3990291a9472331dab591e8760332ff8535be98df5c353f44f4547',
          'startupJson': '6c91d9ee0b9915ddcad06bc810ebe63813e94c2418dde3797f6e94c087383ae2',
          'clarification': 'c22dcca3115a745b361423d982df12e340831bcaf442a35b8b86e933f89d6914'}
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
live44, archive44 = sha(LIVE44), sha(ARCHIVE44)
ARCH = {rel(p): J(p) for p in sorted(glob.glob(REC + '/archive-verification*.json'))}
arch44 = [v for k, v in ARCH.items() if k.endswith(('source44.json', 'source44-pkg.json'))]
arch43 = [v for k, v in ARCH.items() if k.endswith('base43.json')]
archives_ok = len(arch44) == 2 and all(a['verified'] and a['archiveShaMatches'] and a['archiveSha256'] == EXPECT['archive44'] and a['manifestSha256'] == EXPECT['manifest44']
                                        and a['membersMatched'] == 12919 for a in arch44)
verified_manifest = bool(SV['manifest44']['matchesHeader'] and live44 == EXPECT['manifest44'] and SV['snapshot44']['verified'] and SV['counts44']['matchesHeader']
                         and SV['counts44']['matchesDeclared'] and SV['counts44']['fileCount'] == 12919 and SV['counts44']['totalBytes'] == 738157930
                         and archive44 == EXPECT['archive44'] and archives_ok)
parent43_ok = bool(SV['manifest43']['sha256'] == EXPECT['manifest43'] and sha(LIVE43) == EXPECT['manifest43'] and SV['snapshot43']['verified'] and SV['parentChain']['44declares43']
                   and len(arch43) == 1 and arch43[0]['verified'] and arch43[0]['archiveSha256'] == EXPECT['archive43'])
if not (verified_manifest and parent43_ok):
    GAPS.append('subject or parent43 verification incomplete')
DELTA = SV['delta']['43to44']
DCOUNTS = DELTA['counts']
if (DCOUNTS['changed'], DCOUNTS['added'], DCOUNTS['removed']) != (24, 6, 0):
    GAPS.append('delta counts differ from measurement: ' + json.dumps(DCOUNTS))
CHANGED_EXPECTED = {FD + 'evaluator3-source-pins.v1.json', FD + 'execution-inputs-contract.v1.md', FD + 'execution_inputs_model.v1.py', FD + 'provider-target-attribution-return.schema.v2.json',
                    FD + 'provider_attribution_return_model.v2.py', FD + 'source-pins.v1.json', NAT + 'README.md', NAT + 'check_native_evidence.v2.py', NAT + 'fact-batch.schema.v3.json',
                    NAT + 'native-cases.v2.json', NAT + 'native-evidence-report.v2.json', NAT + 'native_evidence_model.v2.py', NAT + 'occupancy-companion.schema.v1.json',
                    NAT + 'protocol3-transitions.v1.json', NAT + 'source-pins.v2.json', DC + 'security/source-pins.v1.json', WFD + 'source-pins.v1.json', WFD + 'workflows-report.v1.json',
                    ARCHD + '14-repository-and-module-layout.md', ARCHD + 'implementation-boundaries-and-build-plan.md', ARCHD + 'implementation-coverage.v1.json',
                    ARCHD + 'implementation-planning-sources.v1.json', ARCHD + 'repository-file-inventory.v1.json', NE}
ADDED_EXPECTED = {NAT + 'provider-handshake.schemas.v1.json', NAT + 'provider-startup.schemas.v1.json', NAT + 'provider_startup_model.v1.py', NAT + 'provider_wire_model.v1.py',
                  NAT + 'typescript-protocol2-order.v1.json', ARCHD + 'implementation-normative-inputs.v12.json'}
paths43to44 = {r['path'] for k in ('changed', 'added', 'removed') for r in DELTA[k]}
if {r['path'] for r in DELTA['changed']} != CHANGED_EXPECTED or {r['path'] for r in DELTA['added']} != ADDED_EXPECTED:
    GAPS.append('delta population differs from the provider wire/startup publication, pins, planning and reports')
DIFFSUM = J(REC + '/delta-diff-summary.json')
COPYVER = J(REC + '/copy-verification-final.json')
if not (set(COPYVER) == {'work/base43', 'work/source44', 'work/source44-pkg'} and all(v['verified'] for v in COPYVER.values())):
    GAPS.append('a disposable copy changed during the review or was not re-verified')
PINS = J(REC + '/source-pins44.json')
PIN_CHANGED_EXPECTED = {FD + 'execution-inputs-contract.v1.md', FD + 'execution_inputs_model.v1.py', FD + 'provider-target-attribution-return.schema.v2.json', FD + 'provider_attribution_return_model.v2.py',
                        FD + 'source-pins.v1.json', NAT + 'README.md', NAT + 'check_native_evidence.v2.py', NAT + 'fact-batch.schema.v3.json', NAT + 'native-cases.v2.json',
                        NAT + 'native_evidence_model.v2.py', NAT + 'occupancy-companion.schema.v1.json', NAT + 'protocol3-transitions.v1.json', NAT + 'source-pins.v2.json',
                        DC + 'security/source-pins.v1.json', WFD + 'source-pins.v1.json', NE}
PIN_ADDED_EXPECTED = ADDED_EXPECTED - {ARCHD + 'implementation-normative-inputs.v12.json'}
PIN_UNPINNED_EXPECTED = {FD + 'evaluator3-source-pins.v1.json', NAT + 'native-evidence-report.v2.json', WFD + 'workflows-report.v1.json', ARCHD + '14-repository-and-module-layout.md',
                         ARCHD + 'implementation-boundaries-and-build-plan.md', ARCHD + 'implementation-coverage.v1.json', ARCHD + 'implementation-normative-inputs.v12.json',
                         ARCHD + 'implementation-planning-sources.v1.json', ARCHD + 'repository-file-inventory.v1.json'}
pins_ok = (PINS['allPinsMatch'] and set(PINS['changedPinUnion']) == PIN_CHANGED_EXPECTED and set(PINS['addedPinUnion']) == PIN_ADDED_EXPECTED
           and set(PINS['deltaFilesPinnedByNoLedger']) == PIN_UNPINNED_EXPECTED
           and all(not v['removedVs43'] and not v['deltaFilesPinnedButNotCurrent'] and not v['mismatchedAgainstManifest'] for v in PINS['ledgers'].values()))
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
for p, rows in sorted(group('fresh44Read').items()):
    cur, lines = sha(S44 + '/' + p), nlines(S44 + '/' + p)
    if any(r['sha256'] != cur for r in rows):
        GAPS.append('fresh read not current: ' + p)
    e = {'path': p, 'sha256': cur, 'lines': lines, 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows}), 'changed43to44': p in paths43to44}
    if covers_all(e['ranges'], lines):
        e.update(readClass='fresh44Read', read='complete: every line read this charter')
        fresh.append(e)
    else:
        e.update(readClass='fresh44RangeRead', read='named ranges only; not a whole-file read')
        ranged.append(e)
fresh_paths = {e['path'] for e in fresh}
delta_reads = []
for p, rows in sorted(group('delta43to44Read').items()):
    r = rows[-1]
    cur, dsha = sha(S44 + '/' + p), sha(RT + '/' + r['diff'])
    if cur != r['sha256'] or dsha != r['diffSha256']:
        GAPS.append('delta read not current: ' + p)
    delta_reads.append({'path': p, 'sha256': cur, 'lines': nlines(S44 + '/' + p), 'readClass': 'delta43to44Read', 'read': 'complete 43->44 diff; not a whole-file read',
                        'alsoFreshWholeFileRead': p in fresh_paths, 'diffReceipt': r['diff'], 'diffSha256': dsha, 'note': r['note']})
evidence_reads = [{'path': p, 'sha256': sha(p), 'ranges': [r['range'] for r in rows], 'notes': sorted({r['note'] for r in rows})} for p, rows in sorted(group('evidenceRead').items())]
delta_read_paths = {e['path'] for e in delta_reads}
# native-cases.v2.json (+6274 lines) is reference data, not a normative owner: it was read by named fixture/case ranges, its
# startup-exchange cases were listed structurally and all 477 cases were executed; its complete diff was NOT read. Disclosed
# as a range-read-only delta file rather than counted as a complete read.
RANGE_ONLY_DELTA = {NAT + 'native-cases.v2.json'}
range_only_delta = [{'path': p, 'ranges': next((e['ranges'] for e in ranged if e['path'] == p), None),
                     'standing': 'changed reference data read by named ranges plus a structured case listing and full checker execution; complete diff not read'}
                    for p in sorted(RANGE_ONLY_DELTA & paths43to44)]
uncovered = sorted(paths43to44 - fresh_paths - delta_read_paths - {e['path'] for e in range_only_delta if e['ranges']})
for p in uncovered:
    GAPS.append('delta file without read entry: ' + p)
V43 = J(V43PATH)
if sha(V43PATH) != EXPECT['review43']:
    GAPS.append('source43 review hash differs from header')
RS43 = V43['readScope']
prior_complete = [dict(e, priorClass='fresh43Read') for e in RS43['fresh43Read']] + \
                 [dict(e, priorClass='inheritedUnchanged42Read') for e in RS43['inheritedUnchanged42Read']] + \
                 [dict(e, priorClass='complete42ReadPlusComplete43Diff') for e in RS43['complete42ReadPlusComplete43Diff']]
inherited, via_diff, changed_not = [], [], []
seen_prior = set()
for e in prior_complete:
    p = e['path']
    if p in fresh_paths or p in seen_prior:
        continue
    seen_prior.add(p)
    a, b = sha_opt(S43 + '/' + p), sha_opt(S44 + '/' + p)
    if a == b:
        inherited.append({'path': p, 'sha256': b, 'readClass': 'inheritedUnchanged43Read', 'priorClass': e['priorClass'],
                          'basis': 'counted as completely read by this origin\'s completed source43 review; byte-identical in source44 (hash recomputed now); not re-read this charter'})
    elif p in delta_read_paths:
        via_diff.append({'path': p, 'sha43': a, 'sha44': b, 'readClass': 'complete43ReadPlusComplete44Diff', 'priorClass': e['priorClass'],
                         'basis': 'source43 bytes counted as completely read plus the exact complete diff to source44; not a fresh whole-file read'})
    else:
        changed_not.append({'path': p, 'sha43': a, 'sha44': b, 'priorClass': e['priorClass']})
if changed_not:
    GAPS.append('a prior complete read changed without a current read: %s' % [c['path'] for c in changed_not])
prior_ranges = [{'path': e['path'], 'ranges': e.get('ranges'), 'unchanged43to44': same(S43, S44, e['path']), 'readClass': 'prior43RangeReadOnly'} for e in RS43['fresh43RangeRead']]
SEARCH_ONLY = [
    {'path': 'docs/coop/design-corrections/reviews/** inside the frozen snapshot (bv4-corrections-author.v1, bv6-corrections-author.v1/.v3, post-reset-review.v15, digest-corrections-author.v6, v19-consistency-coauthor.v1, blind-corrections-author.v1/author-source and similar historical copies)',
     'lines': 'file names plus one matching signature line each (def protocol3_run) surfaced by one content search whose glob named native_evidence_model.v2.py/provider_attribution_return_model.v2.py under docs/coop/design-corrections without excluding reviews/**',
     'standing': 'UNINTENDED search-output sighting of snapshot-internal historical review copies; the tool persisted the overflow to a file that was not opened; no such file was opened or read and nothing from them is used; every later search named exact current paths'},
    {'path': ARCHD + 'repository-file-inventory.v1.json', 'lines': '28-1461 provider/protocol occurrences (search output); range 688-757 was then read', 'standing': 'search output outside the ledgered range'},
    {'path': 'docs/coop/artifacts/delivery.v2.json', 'lines': '510, 600, 623, 648, 672, 675, 846-847, 855, 861, 895, 901, 1111, 1116, 1119-1122, 1132, 1138, 1169, 1498, 1517 (majors, handshake, FactBatchV1, CancelledV1, ordering and supervision search output)', 'standing': 'seen in search output only, outside the ledgered ranges'},
    {'path': NE, 'lines': 'section headings and 1462, 1620, 1850, 2184, 2794, 2811, 2816-2834, 2865, 2931-2941, 2949-2950, 2955-2968, 2992-2996, 3132-3133, 3154, 3924 (search output)', 'standing': 'search output; sections 0 (96-135) and 9 (2781-3297) were read completely by range'},
    {'path': NAT + 'native-cases.v2.json', 'lines': 'fixture key lines 5914-7474 and provider_startup_exchange case frames (search and structured listing output)', 'standing': 'search output and a structured listing of case ids/frames/expectations; fixture ranges were read'},
    {'path': 'docs/coop/artifacts/rust-provider-protocol.v2.json, docs/coop/artifacts/delivery.v2.json, native-evidence.schemas.v2.json, provider-*.schemas.v1.json', 'lines': 'selected JSON members printed by structured dumps (limits, payload schemas, commitments, reason enums, laws)', 'standing': 'structured measurement output, not whole-file reads'},
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
NEW_LAYER_DOCS = [NAT + 'provider-handshake.schemas.v1.json', NAT + 'provider-startup.schemas.v1.json', NAT + 'typescript-protocol2-order.v1.json']
planning_ok = (P['check_implementation_planning']['exitCode'] == 0 and P['check_repository_file_inventory']['exitCode'] == 0 and PC['coverageMappings'] == 322
               and PC['coverageMappingsSource43'] == 322 and PC['layerSha256']['12'] == EXPECT['v12'] and PC['v12MatchesHeader'] and PC['v12MatchesManifestIndex']
               and not PC['layerMismatchedAgainstSource44']['12'] and PC['layerInputs']['12'] == 34 and PC['layerInputs']['11'] == 31
               and all(PC['priorLayersByteEqualToSource43'].values()) and PC['v12AddedVsV11'] == NEW_LAYER_DOCS and PC['v12RemovedVsV11'] == [] and PC['v12ChangedVsV11'] == [NE]
               and PC['coverageSubjectMatchesV12'] and PC['coverageSourcesAllBoundByV12'] and PC['coverageSourcesStale'] == [] and PC['coverageSourceKeys'] == 34
               and PC['planningSourcesArchitectureSha256MatchesV12'] and PC['planningSourcesArchitectureFilesEqualV12'] and PC['planningSourcesPreviousFilesEqualV11']
               and PC['planningSourcesHistoryHashesMatchLayerBytes'] and PC['coverageRowIdsAddedVs43'] == [] and PC['coverageRowIdsRemovedVs43'] == []
               and PC['coverageRowsChangedVs43'] == sorted('native-evidence:%d' % i for i in range(1, 16))
               and PC['inventoryPaths'] == 198 and PC['inventoryPackages'] == 20 and PC['recoveryCases'] == 54 and PC['recoveryCasesNotExecuted'] == 54
               and PC['coverageGroups']['reportFeatures'] == 24 and PC['milestoneOrder'] == ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6'] and PC['verificationStandings'] == ['not-executed']
               and all(PC['operationsCheckersByteEqualToSource43'].values()))
if not planning_ok:
    GAPS.append('planning checks or counts not as measured')
UNBOUND_NORMATIVE = sorted(p for p, v in PC['deltaDocumentsNotBoundByV12'].items() if v['selfDeclaresNormativeOrCurrent'])
RC = J(REC + '/reference-comparison.json')
reference_ok = (RC['codexReferenceChecks']['sha256'] == EXPECT['codex'] and RC['codexPassed'] and RC['codexSubjectManifestSha256'] == EXPECT['manifest44'] and RC['rootPassed']
                and all(v['stdoutFileEqualRoot'] and v['stdoutShaEqualRootRecord'] and v['rootSourceShaEqualsMineScript'] and v['stdoutFileEqualCodex'] for v in RC['groups'].values())
                and RC['childCount'] == 17 and RC['childrenEqualRoot'] == 15 and RC['codexRunnerOriginalEqualsRoot']
                and RC['childrenNotEqualRoot'] == ['enumeration.stdout', 'execution-inputs.stdout'] and RC['childrenDifferingFromHistoricalMine43'] == ['enumeration.stdout', 'execution-inputs.stdout']
                and all(RC['children'][n]['rootDiff']['equalAfterStrippingPathFieldsOnly'] for n in ('enumeration.stdout', 'execution-inputs.stdout'))
                and RC['children']['enumeration.stdout']['historicalMine43Diff']['equalAfterStrippingPathFieldsOnly']
                # the execution-inputs child records owned-file digests; two of its owned files changed 43->44, so against this
                # origin's source43 receipt it may differ only in ownedHashes and neededRootInputs[3] (measured and described in OBS44-01)
                and set(RC['children']['execution-inputs.stdout']['historicalMine43Diff']['strippedPaths']) <= {'/neededRootInputs[3]'})
if not reference_ok:
    GAPS.append('reference comparison not as measured')
GROUP_DIFF_43 = {'foundation': 'sourceFileCount 1247 -> 1252 only', 'workflows': 'sourceFileCount 1247 -> 1252 only', 'native': 'PASS 388/388 -> 477/477 cases'}


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


PORTED = [('P44-PORTED-POLICY', 'probes/ported44_probe_policy_v40.py', 'ported44-policy-v40', 'policy-v40-on44.json', 'policy-v40-on43.json',
           'Ported (expectations unedited): policy.test known-hit, universe tokens, imported universe, policy.show, identity preimages.'),
          ('P44-PORTED-NATIVE', 'probes/ported44_probe_native_v40.py', 'ported44-native-v40', 'native-v40-on44.json', 'native-v40-on43.json', 'Ported: U-1 effective allowJs, nested Cargo, unitKind full-Run closure.'),
          ('P44-PORTED-RUNTERM', 'probes/ported44_probe_runterm_adv_v40.py', 'ported44-runterm-adv-v40', 'runterm-adv-v40-on44.json', 'runterm-adv-v40-on43.json',
           'Ported: run-termination keys, commit-inventory recipe over a closed Run, registered-schema account.'),
          ('P44-PORTED-QUERY', 'probes/ported44_probe_query_carriers.py', 'ported44-query-carriers', 'query-carriers.json', 'query-carriers.json', 'Ported: nine command carriers, twenty operations, delivery law.'),
          ('P44-PORTED-CARRIER', 'probes/ported44_probe_carrier_readonly.py', 'ported44-carrier-readonly', 'carrier-readonly.json', 'carrier-readonly.json', 'Ported: read-only carrier scenarios on real SQLite.'),
          ('P44-PORTED-COMPARISON', 'probes/ported44_probe_comparison_knowledge.py', 'ported44-comparison-knowledge', 'comparison-knowledge.json', 'comparison-knowledge.json', 'Ported: comparison presence knowledge.'),
          ('P44-PORTED-REPAIR2', 'probes/ported44_probe_repair2.py', 'ported44-repair2', 'repair2.json', 'repair2.json', 'Ported: repair:2 refusal order and retained-Run joins.'),
          ('P44-PORTED-TERM7', 'probes/ported44_probe_run_termination_s7.py', 'ported44-run-termination-s7', 'run-termination-s7.json', 'run-termination-s7.json', 'Ported: run-termination section 7 composition admission.'),
          ('P44-PORTED-CUSTODY', 'probes/ported44_probe_native_custody_fallback.py', 'ported44-native-custody-fallback', 'native-custody-fallback.json', 'native-custody-fallback.json', 'Ported: pruned-tree custody and U-9 fallback.'),
          ('P44-PORTED-CAPTURE-JOINS', 'probes/ported44_probe_capture_joins.py', 'ported44-capture-joins', 'capture-joins-on44.json', 'capture-joins-on43.json',
           'Ported ADV42-01 measurement: which owner refuses a captured unattributed view with a foreign planId and/or a non-provider producer.')]
ALLOWED_PORT_DIFF = {'P44-PORTED-POLICY': ['new-copy-equals-source40-manifest']}
PROBE_DEFS = [
    ('P44-SUBJECT', 'probes/verify_subject44.py', None, ['subject-verification.json', 'manifest44-index.json', 'manifest43-index.json'],
     'Formal manifest e873c8db... and all 12,919 snapshot members (hash and length, none unlisted); parent43 manifest db43ee76... and all 12,913 members; declared chain 44->43; exact delta 43->44 (24/6/0).'),
    ('P44-ARCHIVE', 'probes/verify_archive_extract44.py', None, ['archive-verification.source44.json', 'archive-verification.source44-pkg.json', 'archive-verification.base43.json'],
     'Archive c21d0491... hashed; every member verified and extracted into two disposable copies (groups copy work/source44, probe copy work/source44-pkg); archive43 d1ff8312... into work/base43 for old-versus-new comparison.'),
    ('P44-DELTA', 'probes/make_delta_diffs44.py', None, ['delta-diff-summary.json'], 'Unified diffs for all 24 changed files and creation diffs for all 6 added files of the 43->44 delta, both sides hash-verified.'),
    ('P44-GROUPS', 'probes/run_reference_groups44.py', None, ['reference/groups-report.all.json', 'reference/evaluator3.stdout', 'reference/foundation.json'],
     'Six pinned groups with /tmp/opensip-architecture-review-env/bin/python -I -B on the verified groups copy; copy re-verified before and after each group; 17 evaluator3 children.'),
    ('P44-REFERENCE-COMPARE', 'probes/compare_reference_v44.py', 'reference-comparison-v44', None,
     'This review\'s groups and children compared with root-source44-final-reference.v1, codex final-reference.v44 and this origin\'s historical source43 receipts, including the key-level difference of every non-byte-equal child (evidence only).'),
    ('P44-PINS', 'probes/verify_pins44.py', 'source-pins44', None, 'Every entry of the five source-pin ledgers against the formal manifest; changed, added and removed pins versus source43; delta files pinned by no ledger.'),
    ('P44-PLANNING', 'probes/run_planning_checks44.py', 'planning-checks-v44', None,
     'Planning and inventory checks (--check) plus v12/v11/v10/v9/v8 layer, coverage, planning-source and history recounts against the exact parent source43, and every changed delta document the current layer does not bind.'),
    ('P44-PORT', 'probes/port_v43_probes44.py', 'port-v43-probes', None, 'Mechanical port of the source43 scope probes: runtime paths and receipt names only; residual source43 runtime mentions none.'),
] + [(pid, script, runname, receipt, claim) for pid, script, runname, receipt, _, claim in PORTED] + [
    ('P44-PORTED-VS43', 'probes/compare_ported44_vs43.py', 'ported44-vs43', None, 'Every ported probe receipt compared case by case with this origin\'s source43 receipt of the same probe.'),
    ('P44-WIRE', 'probes/probe_wire44.py', 'probe-wire44', 'wire44.json',
     'Focus A discriminators on source44 bytes with independent hashlib, canonical-JSON and length-first CBOR oracles: per-language limit maps from delivery.v2 / rust-provider-protocol.v2 / section 9.3, contract digest from artifact bytes, descriptor digests, inherited-member retention, narrow supersession against the registered bundle, token enums, TS/Rust Hello and HelloAck positives and field-by-field refusals, historical/negotiated FactBatch admission with the TS commitment recomputed, and the occupancy gate omission versus wire refusal on source44 and source43.'),
    ('P44-STARTUP', 'probes/probe_startup44.py', 'probe-startup44', 'startup44.json',
     'Focus B discriminators through provider_startup_exchange: OpenUniverse/UniverseAccepted correlation, handshake joins, universe identity recomputed, native-context Plan binding, repository resolution and derived modes (empty custody, prepared, imported), NativeContextVerified, pre-Analyze Unavailable (payload, phase, correlation, process faults, zero-exit/EOF, host conversion), post-Analyze reasons, Coverage frame names and entry/frame schemas, key correspondence, cancellation interval, and handshake refusals before source bytes.'),
    ('P44-PACKAGE21', 'probes/probe_package_v21.py', 'probe-package-v21', 'package-v21.json',
     'Package v21 manifest, formal44 versus files-only projection, overlay provenance from package15, packages 16-20 preserved, pre-binding package retained, export stores byte-equal to package20 and measured RunIds, content equality with the root rebuild verification and probe, exact normalization-map negatives.'),
    ('P44-COPIES-FINAL', 'probes/verify_copies44.py', 'copies-final', None, 'All three disposable copies re-verified against their formal manifests after every probe and checker.'),
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
PBY['P44-PORT']['receipts'] = {'receipts/probe-port44.json': sha(REC + '/probe-port44.json')}
PBY['P44-PORTED-VS43']['receipts'] = {'receipts/ported44-vs43.json': sha(REC + '/ported44-vs43.json')}
PBY['P44-PINS']['receipts'] = {'receipts/source-pins44.json': sha(REC + '/source-pins44.json')}
PBY['P44-PLANNING']['receipts'] = {'receipts/planning-checks.json': sha(REC + '/planning-checks.json')}
PBY['P44-REFERENCE-COMPARE']['receipts'] = {'receipts/reference-comparison.json': sha(REC + '/reference-comparison.json')}
PBY['P44-COPIES-FINAL']['receipts'] = {'receipts/copy-verification-final.json': sha(REC + '/copy-verification-final.json')}
PORTED_EQUAL = {}
for pid, _, _, receipt, receipt43, _ in PORTED:
    cur, old = rows_of(receipt), {r['case']: r for r in J(V43REC + '/probes/' + receipt43)['rows']}
    differ = [c for c in cur if c in old and json.dumps(cur[c]['observed'], sort_keys=True) != json.dumps(old[c]['observed'], sort_keys=True)]
    PORTED_EQUAL[pid] = {'rows': len(cur), 'sameCaseSetAsSource43': set(cur) == set(old), 'observedDifferFromSource43': differ,
                         'expectedCopyIdentityDifferences': ALLOWED_PORT_DIFF.get(pid, []), 'historicalReceipt43': 'claude-independent-design.v43/receipts/probes/' + receipt43}
    if sorted(differ) != sorted(ALLOWED_PORT_DIFF.get(pid, [])) or set(cur) != set(old) or any(not r['ok'] for r in cur.values()):
        GAPS.append('ported probe observations differ from source43 beyond the copy identity row: ' + pid)
PORT = J(REC + '/probe-port44.json')
if any(r['residualV43RuntimeMentions'] for r in PORT) or len(PORT) != 10:
    GAPS.append('ported probe still names the source43 runtime')
PKG_RUNS = {'verify-package.py': run_record('package-v21-verify', PKG + '/verify-package.py'),
            'probe-native-v2.py': run_record('package-v21-probe-native-v2', PKG + '/probe-native-v2.py')}
WR, SR, PK, CJ = rows_of('wire44.json'), rows_of('startup44.json'), rows_of('package-v21.json'), rows_of('capture-joins-on44.json')

# ------------------------------------------------------------------------------------------------ owner map
MAP_FILES = [NE, NAT + 'provider-handshake.schemas.v1.json', NAT + 'provider-startup.schemas.v1.json', NAT + 'typescript-protocol2-order.v1.json', NAT + 'provider_wire_model.v1.py',
             NAT + 'provider_startup_model.v1.py', NAT + 'protocol3-transitions.v1.json', NAT + 'native_evidence_model.v2.py', NAT + 'check_native_evidence.v2.py', NAT + 'native-cases.v2.json',
             NAT + 'native-evidence-report.v2.json', NAT + 'native-evidence.schemas.v2.json', NAT + 'native-capability-matrix.v2.json', NAT + 'fact-batch.schema.v3.json',
             NAT + 'occupancy-companion.schema.v1.json', NAT + 'dispatch-binding.schema.v1.json', NAT + 'source-pins.v2.json',
             'docs/coop/artifacts/delivery.v2.json', 'docs/coop/artifacts/rust-provider-protocol.v2.json', 'docs/coop/artifacts/resolved-inputs.v2.json', 'docs/coop/artifacts/check-fact-plane.py',
             FD + 'provider-target-attribution-return.schema.v2.json', FD + 'provider_attribution_return_model.v2.py', FD + 'execution-inputs-contract.v1.md', FD + 'execution-inputs.schema.v1.json',
             FD + 'execution_inputs_model.v1.py', FD + 'execution_inputs_fixture.v3.py', FD + 'check-execution-inputs.v1.py', FD + 'enumeration-contract.v1.md', FD + 'enumeration-plan.schema.v1.json',
             FD + 'enumeration_model.v1.py', FD + 'check-enumeration.v1.py', FD + 'evaluator_graph_fixture.v3.py', FD + 'evaluator_semantic_fixture.v3.py', FD + 'evaluator_input_model.v3.py',
             FD + 'identity-model.v3.py', FD + 'identity-schemas.v3.json', FD + 'evaluator-composition-contract.v3.md', FD + 'evaluator_replay_model.v3.py',
             FD + 'run-termination-contract.v1.md', FD + 'run_termination_model.v1.py', FD + 'canonical.py', FD + 'source-pins.v1.json', FD + 'evaluator3-source-pins.v1.json',
             WFD + 'query-projection-contract.v3.md', WFD + 'query_projection_model.v3.py', WFD + 'check-query-projection.v3.py', WFD + 'query_surface_projection.v3.py',
             WFD + 'schemas/evaluator3/graph-query.schema.json', WFD + 'command-inventory.v3.json', WFD + 'workflows-report.v1.json', WFD + 'source-pins.v1.json', WFD + 'policy_test_model.v3.py',
             WFD + 'repair_closed_world_selection.v1.py', DC + 'security/source-pins.v1.json', DC + 'security/carrier-dispatch.v3.json', DC + 'public-detail-registry.v1.json',
             DC + 'evaluation-residual-dispositions.proposed.json', DC + 'inherited-residuals.proposed.md', DC + 'current-source-map.proposed.md', DC + 'qualification-gates.proposed.json',
             ARCHD + '08-decision-and-readiness-register.md', ARCHD + 'commit-recovery-readonly.v3.md', ARCHD + 'prototype-report-inventory.md', ARCHD + 'repository-file-inventory.v1.json',
             ARCHD + 'implementation-coverage.v1.json', ARCHD + 'implementation-planning-sources.v1.json', ARCHD + 'implementation-normative-inputs.v11.json', ARCHD + 'implementation-normative-inputs.v12.json',
             ARCHD + '14-repository-and-module-layout.md', ARCHD + 'implementation-boundaries-and-build-plan.md', 'docs/operations/check_implementation_planning.py',
             'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md', 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
             'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'docs/v2/contracts/product-v1/README.md']
MAP = {p: {'sha256': sha(S44 + '/' + p), 'sha43': sha_opt(S43 + '/' + p), 'unchanged43to44': same(S43, S44, p), 'inDelta': p in paths43to44} for p in MAP_FILES}
for p, v in MAP.items():
    if v['unchanged43to44'] == v['inDelta']:
        GAPS.append('map/delta disagreement: ' + p)
U = {os.path.basename(p): v['unchanged43to44'] for p, v in MAP.items() if not p.endswith('source-pins.v1.json')}
GATES = J(S44 + '/' + DC + 'qualification-gates.proposed.json')['items']
gates_true = sum(1 for g in GATES if g.get('qualified') is True)
REG = open(S44 + '/' + ARCHD + '08-decision-and-readiness-register.md', encoding='utf-8').read().splitlines()
cond2_ok = '28 existing rows' in ' '.join(REG[384:391])
if len(GATES) != 32 or gates_true != 0 or not cond2_ok:
    GAPS.append('gates or condition-2 measurement differs')

# ------------------------------------------------------------------------------------------------ root/package evidence
MV = J(RT + '/work/package-v21-verify/verification.json')
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
    GAPS.append('package v21 verification not as recorded')
rid_row = PK.get('measured-source44-RunIds-equal-the-source43-package20-rebuild-RunIds', {}).get('observed', {})
PACKAGE = {
    'package': PKG, 'artifactManifestSha256': sha(PKG + '/artifact-manifest.json'), 'expectedArtifactManifestSha256': EXPECT['pkgManifest'],
    'sourceBindingV44Sha256': sha(SRCBIND), 'expectedSourceBinding': EXPECT['sourceBinding'],
    'filesOnlySourceProjectionSha256': sha(PKG + '/source-manifest.json'), 'formalSubjectManifestSha256': live44,
    'rebuildReportSha256': sha(REBUILD), 'expectedRebuildReport': EXPECT['rebuild'], 'rootRebuildVerificationSha256': sha(ROOTVER), 'formalBindingRecordSha256': sha(FORMAL),
    'preBindingPackageManifestSha256': RB['packageManifestSha256'],
    'historyPackageManifests': {v: sha(B + '/claude-author-package-successor.v%s/artifact-manifest.json' % v) for v in ('15', '16', '17', '18', '19', '20')},
    'probeRows': {k: {'ok': v['ok'], 'observed': v['observed']} for k, v in PK.items() if v.get('kind') != 'record'},
    'verificationGroups': vgroups, 'exports': export_count, 'queries': query_count, 'normalizationMapControls': nm_controls,
    'nativeV2Probe': {'runs': native_runs, 'passed': NV['passed'], 'unitsVsDiscoveryDisagreements': NV['unitsVsDiscoveryDisagreements']},
    'measuredRunIds': run_ids, 'runIdsEqualSource43Package20': rid_row.get('source44') == rid_row.get('source43') and bool(rid_row),
    'formalBindingSource43Comparison': {'rows': len(FB['source43Comparison']), 'allSameRunIdAndBytes': all(c['sameRunId'] and c['sameExportBytes'] for c in FB['source43Comparison'])},
    'toolRuns': PKG_RUNS, 'verified': pkg_ok,
    'result': ('Package v21 verified as author evidence. All %d files match artifact manifest e5639aa3...; the formal44 manifest e873c8db... and the files-only projection %s... are different objects with equal file members (equal to this review\'s own verified manifest44 index), and the package copy of the formal manifest equals the live one. '
               'The rebuild (report 332e5d51...) ran on frozen candidate-subject.v44 from package15 constructors (6a8d4fec...) plus the native-v2 migration overlay (overlay base digests match retained package15); packages 16-20 remain unchanged history, and the pre-binding package c97d6f3b... is retained inside package21 and equals the rebuild output. '
               'Metadata binding changed no export store or current replay helper byte. Every current export store is byte-equal to package20 at the same path, and the 17 measured RunIds equal the source43 package20 rebuild RunIds, so identities are unchanged and nothing was reminted. '
               'This review re-executed verify-package.py and probe-native-v2.py on its own verified source44 copy: groups %s; %d exports and %d queries. The verification of bound package21 equals the root verification of the pre-binding package except package identity and file count, every other output file is byte-equal, and the 9 membership comparisons are content-equal to the root rebuild probe.'
               % (len(J(PKG + '/artifact-manifest.json')['files']), sha(PKG + '/source-manifest.json')[:8], ', '.join('%s %s (passed %s, exit %s)' % (g['group'], g['count'], g['passed'], g['exitCode']) for g in vgroups), export_count, query_count or 0)),
    'limits': ['Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.',
               'Four TypeScript normalization-map negatives ARE executed (exact refusals below). The Rust map negative is unexercised.',
               'The partial and/or/not consumer helper remains unexercised; count-at-most/all-covered remain unimplemented; two-binding qualification is incomplete.',
               'No compiler, provider, OS or process-isolation qualification; independent grades granted: 0; all 30 author-proposed grades stay PENDING final application.'],
}
CODEXD, ROOTD = J(CODEX), J(ROOTREF)
COMP = J(COMPANION)
planning_stdout_equal_companion = (COMP['planning']['result']['output'] == P['check_implementation_planning']['stdout'] and COMP['inventory']['stdout'] == P['check_repository_file_inventory']['stdout'])
EVIDENCE = {
    'standing': 'NONBLIND header-named evidence, not acceptance. Only the source-only author reports were read as author material; no author runtime history, blind consumer artifact, export, helper, report or root blind outcome was read.',
    'records': [
        {'path': WIRE_MD, 'sha256': sha(WIRE_MD), 'expected': EXPECT['wireMd'], 'note': 'source-only provider wire correction author report; read completely; its choices and counts were re-measured, not adopted'},
        {'path': WIRE_JSON, 'sha256': sha(WIRE_JSON), 'expected': EXPECT['wireJson'], 'note': 'source-only provider wire correction author record; read completely'},
        {'path': STARTUP_MD, 'sha256': sha(STARTUP_MD), 'expected': EXPECT['startupMd'], 'note': 'source-only provider startup correction author report (R-1..R-6 limits); read completely'},
        {'path': STARTUP_JSON, 'sha256': sha(STARTUP_JSON), 'expected': EXPECT['startupJson'], 'note': 'source-only provider startup correction author record; read completely'},
        {'path': CLARIFY, 'sha256': sha(CLARIFY), 'expected': EXPECT['clarification'], 'note': 'root documentation-only scope clarification (native-evidence.md, native model, checker before/after digests); read completely; its before bytes are not available to this review'},
        {'path': COMPANION, 'sha256': sha(COMPANION), 'expected': EXPECT['companion'], 'stdoutEqualsThisReview': planning_stdout_equal_companion,
         'note': 'root companion planning/inventory outputs executed from a pre-freeze working tree; stdout text equal to this review\'s own checks'},
        {'path': CODEX, 'sha256': sha(CODEX), 'expected': EXPECT['codex'], 'passed': CODEXD.get('passed'), 'subjectManifestSha256': CODEXD.get('subjectManifestSha256'),
         'note': 'current final44 reference receipts named by the header; runner-original equals the root reference-checks: %s' % RC['codexRunnerOriginalEqualsRoot']},
        {'path': ROOTREF, 'sha256': sha(ROOTREF), 'passed': ROOTD.get('passed'), 'executionSourceRoots': RC['rootExecutionSourceRoots'],
         'note': 'actual root execution root-source44-final-reference.v1 (6 groups, 17 children); executed from a pre-freeze working tree whose script bytes equal the frozen source44 bytes'},
        {'path': REBUILD, 'sha256': sha(REBUILD), 'expected': EXPECT['rebuild'], 'note': 'root reconstruction of package v21 from package15 plus overlay on frozen candidate-subject.v44 (author construction evidence)'},
        {'path': ROOTVER, 'sha256': sha(ROOTVER), 'note': 'root rebuild verification of the pre-binding package; equal to this review\'s verification of bound package21 except package identity and file count'},
        {'path': FORMAL, 'sha256': sha(FORMAL), 'note': 'root formal44 metadata binding record and measured source43 comparison (not header-bound; embeds the header-bound source binding)'},
        {'path': SRCBIND, 'sha256': sha(SRCBIND), 'expected': EXPECT['sourceBinding'], 'note': 'package 21 source binding'},
        {'path': V43PATH, 'sha256': sha(V43PATH), 'expected': EXPECT['review43'], 'note': 'this origin\'s completed source43 review; read-only history for prior rows, dispositions and read scope'},
    ],
}
for r in EVIDENCE['records']:
    if r.get('expected') and r['sha256'] != r['expected']:
        GAPS.append('evidence hash differs from header: ' + r['path'])

for part in ('build_review44_findings.py', 'build_review44_rows.py', 'build_review44_emit.py'):
    path = RT + '/probes/' + part
    exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), globals())
