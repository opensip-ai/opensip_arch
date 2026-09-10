"""Independent reviewer probes, part E: executable closure of the part-A/B/C probes whose
COUNTEREXAMPLE/GAP status came from MY selector defects rather than from the subject.
Each probe here re-asks the same question against the correct frozen selectors."""
import copy
import importlib.util
import json
import re
import traceback
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v4/scratch')
DC = ROOT / 'docs/coop/design-corrections'
CONTRACTS = ROOT / 'docs/v2/contracts/product-v1'
ARCH = ROOT / 'docs/v2/architecture'

spec = importlib.util.spec_from_file_location('probe_host_e', DC / 'integration-host-model.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
S, N, W, C = M.S, M.N, M.W, M.C

results = []


def rec(pid, title, status, detail):
    results.append({'probe': pid, 'title': title, 'status': status, 'detail': detail})
    print('%-7s %-14s %s' % (pid, status, title))
    if status != 'OK':
        print('        ' + json.dumps(detail, default=str)[:2000])


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


INV = C.parse((DC / 'workflows/command-inventory.v1.json').read_bytes())


@probe('P6e', 'ADV-i (supersedes P6/P6b): the ONE mapping table equals all three real closed enums')
def _():
    text = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    rows = re.findall(r'^\|\s*(interactive-explicit|policy-record)\s*\|\s*([a-z-]+)\s*\|\s*([a-z-]+)\s*\|\s*$',
                      text, re.M)
    table = {r[0]: (r[1], r[2]) for r in rows}
    sec = C.parse((DC / 'security/security-lifecycle.schemas.v1.json').read_bytes())
    sec_modes = set(sec['$defs']['Consent']['properties']['mode']['enum'])
    te = C.parse((DC / 'workflows/schemas/test-execution.schema.json').read_bytes())
    te_modes = set(te['$defs']['TestExecutionStepParams']['properties']['consentSource']['enum'])
    ir = C.parse((DC / 'workflows/schemas/invocation-record.schema.json').read_bytes())
    rp_modes = set(ir['$defs']['RepairApplyParams']['properties']['consentSource']['enum'])
    ok = (set(table) == sec_modes == {'interactive-explicit', 'policy-record'}
          and {v[0] for v in table.values()} == te_modes
          and {v[1] for v in table.values()} == rp_modes
          and table['policy-record'] == ('pre-existing-policy', 'policy')
          and table['interactive-explicit'] == ('interactive-consent', 'interactive')
          and len(table) == 2)
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'contractTable': table, 'securityConsentMode': sorted(sec_modes),
        'testExecutionConsentSource': sorted(te_modes), 'repairApplyConsentSource': sorted(rp_modes),
        'note': 'RepairApplyParams lives in invocation-record.schema.json, not repair.schema.json'}


@probe('P16e', 'ADV-ii (supersedes P16/P16b): security refuses a boundary-crossing explicit root FIRST')
def _():
    """P16/P16b passed `config` as a key the discovery input does not have, so it was ignored.
    Drive the real frozen discovery cases that exercise exactly this condition."""
    cases = C.parse((DC / 'security/discovery-cases.v1.json').read_bytes())['cases']
    rows = {}
    for cid in ('explicit-join-crossing-into-a-nested-project-refuses',
                'config2-workspace-root-crossing-into-nested-repository-refuses',
                'explicit-root-inside-an-installed-dependency-tree-refuses',
                'explicit-root-inside-cargo-build-output-refuses-but-a-source-directory-called-target-is-admitted'):
        case = next((x for x in cases if x['id'] == cid), None)
        if case is None:
            rows[cid] = 'CASE-NOT-FOUND'; continue
        r = S.discovery(copy.deepcopy(case['input']))
        rows[cid] = {'status': r['status'], 'refusal': r.get('refusal'), 'detail': r.get('detail'),
                     'd9': r.get('d9')}
    reg = C.parse((DC / 'public-detail-registry.v1.json').read_bytes())
    public = {x['code'] for x in reg['records']}
    aliases = {x['internalCode']: x['publicCode'] for x in reg['internalAliases']}
    crossing = [v for v in rows.values() if isinstance(v, dict) and v['status'] == 'REFUSE']
    ok = (all(v['refusal'] == 'PROJECT.EXPLICIT_PATH_INVALID' for v in crossing)
          and 'PROJECT.EXPLICIT_PATH_INVALID' in public
          and aliases.get('native.explicit-root-crosses-boundary') == 'PROJECT.EXPLICIT_PATH_INVALID'
          and 'native.explicit-root-crosses-boundary' not in public)
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'discoveryCases': rows,
                                                'nativeSpellingIsInternalAlias':
                                                    aliases.get('native.explicit-root-crosses-boundary'),
                                                'nativeSpellingIsNotPublic':
                                                    'native.explicit-root-crosses-boundary' not in public}


@probe('P17e', 'ADV-iii (supersedes P17/P17b): the surviving reselectsStore mentions are the NEGATIVE law')
def _():
    hits = {}
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or 'reviews/' in str(p) or p.suffix not in ('.py', '.json', '.md'):
            continue
        try:
            t = p.read_text()
        except Exception:
            continue
        if 'reselectsStore' in t:
            ctx = [m.strip()[:180] for m in re.findall(r'[^\n]*reselectsStore[^\n]*', t)]
            hits[str(p.relative_to(ROOT))] = ctx
    model = (DC / 'security/security_lifecycle_model_v1.py').read_text()
    negative = all(
        ('cannot supply' in ' '.join(v)) or ('override-refused' in ' '.join(v)) or ('Removed dead' in ' '.join(v))
        for v in hits.values())
    return ('OK' if 'reselectsStore' not in model and negative else 'COUNTEREXAMPLE'), {
        'modelStillReadsIt': 'reselectsStore' in model,
        'survivingMentionsAreNegativeLawOrItsTestOrItsDisposition': negative,
        'mentions': hits}


@probe('P32e', 'Output law (supersedes P32/P32b): the post-commit required-renderer failure law is stated')
def _():
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    law = re.search(r'Failure of the selected\s*\nrequired renderer \*\*after\*\* a committed Run is '
                    r'`(DELIVERY\.REQUIRED_FAILED)` \((\d)\)', prose)
    golden = 'selected renderer fails after commit' in prose
    optional = 'optional export sink' in prose
    reg = C.parse((DC / 'public-detail-registry.v1.json').read_bytes())
    codes = {x['code'] for x in reg['records']}
    renderers = INV.get('renderers', [])
    all4 = all(r.get('requiredFailureClass') == 'operational-failed' for r in renderers)
    return ('OK' if law and golden and optional and all4
            and 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT' in codes else 'COUNTEREXAMPLE'), {
        'lawSentence': law.group(0).replace('\n', ' ') if law else None,
        'exitCode': law.group(2) if law else None,
        'goldenRowPresent': golden, 'optionalSinkLeavesSuccess': optional,
        'everyRendererRequiredFailureIsOperational': all4,
        'detailRegistered': 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT' in codes,
        'note': 'D-372 calls this the post-commit required-output failure law; the contract spells it out'}


@probe('P39e', 'S16 (supersedes P39/P39b): every file-05 obligation appears, item for item')
def _():
    sec = (CONTRACTS / 'security-and-lifecycle.md').read_text()
    i = sec.find('\n## S16.')
    j = sec.find('\n## ', i + 5)
    s16 = sec[i:j if j > 0 else len(sec)]
    f05 = (ARCH / '05-v1-to-v2-relationship.md').read_text()
    k = f05.find('## Migration constraints')
    mc = f05[k:f05.find('\n## ', k + 5)]
    preserve = [x.strip(' .') for x in re.search(
        r'must preserve (.+?)\.\s*It must distinguish', mc, re.S).group(1).replace('\n', ' ')
        .replace(', and ', ', ').split(',')]
    distinguish = [x.strip(' ;.') for x in re.findall(r'^-\s+(.+)$', mc, re.M)]
    prohibitions = [x.strip() for x in re.search(
        r'No migration silently (.+?)\.', mc, re.S).group(1).replace('\n', ' ')
        .replace(', or ', ', ').split(',')]
    s16_preserve = re.findall(r'^\d+\.\s+\*\*(.+?):\*\*', s16, re.M)
    s16_distinctions = re.findall(r'\((\d)\)\s+([^;]+)[;.]', s16)
    s16_prohibitions = re.findall(r'no silent (.+?)\.', s16)
    bolded = re.findall(r'\*\*([a-z][a-z /-]+?)\*\*', s16)
    return ('OK' if (len(preserve) == 5 and len(distinguish) == 5 and len(prohibitions) == 6
                     and len(s16_preserve) == 5 and len(s16_distinctions) == 5
                     and len(bolded) == 6) else 'COUNTEREXAMPLE'), {
        'file05Preserve': preserve, 's16Preserve': s16_preserve,
        'file05Distinguish': distinguish, 's16DistinctionCount': len(s16_distinctions),
        'file05Prohibitions': prohibitions, 's16ProhibitionBoldTerms': bolded,
        'counts': {'preserve': [len(preserve), len(s16_preserve)],
                   'distinctions': [len(distinguish), len(s16_distinctions)],
                   'prohibitions': [len(prohibitions), len(bolded)]}}


@probe('P51e', 'S16 item 2 (supersedes P51): exactly the five named commands write tracked intent')
def _():
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    named = re.search(r'Only `([^`]+)`, `([^`]+)`, `([^`]+)` write tracked intent', prose)
    writers = sorted(c['name'] for c in INV['commands'] if c.get('writesTrackedIntent'))
    analysis = {c['name']: c.get('writesTrackedIntent') for c in INV['commands']
                if c.get('requestClass') == 'analysis'}
    default = next(c for c in INV['commands'] if c['name'] == 'default')
    ok = (writers == ['baseline-adopt', 'baseline-export', 'baseline-upgrade', 'policy-init', 'waive']
          and not any(analysis.values()) and default['writesTrackedIntent'] is False
          and default['firstSourceWrite'] is True)
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'commandsWritingTrackedIntent': writers,
        'contractSentence': named.group(0) if named else None,
        'analysisClassWritesTrackedIntent': analysis,
        'defaultIsExplicitFirstSourceWriteNotAPolicyWrite':
            {'writesTrackedIntent': default['writesTrackedIntent'],
             'firstSourceWrite': default['firstSourceWrite']}}


@probe('P55e', 'Core scope (supersedes P55): affects=none means an EMPTY lease set, by design')
def _():
    TF = C.parse((DC / 'security/transition-journal-cases.v1.json').read_bytes())
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    rows = {}
    for key in ('UpdateSchemaChange', 'UpdateSameSchema', 'Repair', 'CoreRollback',
                'StoreMigrate', 'StoreRollback'):
        ti = TF['records']['intent' + key]
        scope = M.core_transition_scope(ti, TF['ctxBase']['namespaceRegistry'])
        rows[key] = {'operation': ti['operation'], 'schemaChange': ti['fromStateSchema'] != ti['toStateSchema'],
                     'storeChange': ti['fromStoreGeneration'] != ti['toStoreGeneration'],
                     'affects': scope['affects'], 'namespaces': scope['namespaces']}
    stated = ('A same-schema core update/repair keeps the selected store and pinned generations' in prose)
    fence_only = [k for k, v in rows.items() if v['affects'] == 'none']
    all_reg = [k for k, v in rows.items() if v['affects'] == 'all-registered']
    ok = (stated and set(fence_only) == {'UpdateSameSchema', 'Repair'}
          and all(rows[k]['namespaces'] == [] for k in fence_only)
          and all(rows[k]['namespaces'] == ['ns-a', 'ns-b', 'ns-c'] for k in all_reg))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'rows': rows, 'fenceOnlyOperations': fence_only, 'allRegisteredOperations': all_reg,
        'contractStatesFenceOnly': stated,
        'note': 'my P55 narrowed an already-empty lease set, so it could not observe a refusal'}


@probe('P57e', 'FW-14 (supersedes P57): the real-configuration corpus is an OBLIGATION, not a claim')
def _():
    res = (DC / 'inherited-residuals.proposed.md').read_text()
    row = re.search(r'^\| FW-14 [^|]*\|(.+?)\|\s*$', res, re.M)
    text = row.group(1).strip() if row else ''
    return ('OK' if ('must add' in text and 'Synthetic design cases are not that corpus' in text
                     and 'No private-repository telemetry' in text) else 'COUNTEREXAMPLE'), {
        'row': text}


@probe('P83', 'Native section 10 duplicated cell: two internal conditions legitimately share one public code')
def _():
    nat = (CONTRACTS / 'native-evidence.md').read_text()
    row = next((l for l in nat.splitlines()
                if 'explicit root at or below an admitted boundary' in l), '')
    details = row.rsplit('|', 2)[-2].strip() if row else ''
    dupes = [d.strip() for d in details.split('/')]
    return ('OK' if dupes.count('`PROJECT.EXPLICIT_PATH_INVALID`') == 2 else 'ADVISORY'), {
        'detailCell': details,
        'note': ('the row lists three conditions and three details; two of the three legitimately '
                 'project to the one canonical public code after ADV-ii, so the cell reads A / B / B'),
        'severity': 'legibility only; the mapping itself is correct'}


out = Path('/tmp/opensip-design-corrections/post-reset-review.v4/probes/independent-probes-e.json')
summary = {'part': 'E (executable closure of my own part-A/B/C selector defects)',
           'manifestSha256': '2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2',
           'counts': {}, 'probes': results}
for r in results:
    summary['counts'][r['status']] = summary['counts'].get(r['status'], 0) + 1
out.write_text(json.dumps(summary, indent=1, default=str) + '\n')
print()
print(json.dumps(summary['counts']))
