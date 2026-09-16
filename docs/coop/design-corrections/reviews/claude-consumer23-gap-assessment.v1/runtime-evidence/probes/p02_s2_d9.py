"""P02 — V23-S2 on frozen candidate36 (read-only). For every native DeficiencyV2 value: the D9 owner's codeMaps, the parsed
native section-10 'Existing code' column, the native schema publicD9Termination text, the native model run_termination and
d9_map, and the D9 goldens. Plus owner-sentence checks deciding whether a per-requirement versus whole-Run distinction is
published, and an in-process candidate run_termination replayed against the existing native run_termination cases and the
check-identity projection control. No source byte is written."""
import copy, hashlib, importlib.util, json, os, re, sys

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
DC = S36 + '/docs/coop/design-corrections'
NAT = S36 + '/docs/v2/contracts/product-v1/native-evidence.md'
WAS = S36 + '/docs/v2/contracts/product-v1/workflows-and-surfaces.md'
D9P = S36 + '/docs/coop/artifacts/d9-exit-contract.v1.14.json'
OUT = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1/receipts'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
OWN = [NAT, WAS, D9P, DC + '/native/native_evidence_model.v2.py', DC + '/native/native-evidence.schemas.v2.json', DC + '/native/native-cases.v2.json',
       DC + '/workflows/schemas/evaluator3/common.schema.json']
R = {'owners': {os.path.relpath(p, S36): sha(p) for p in OWN}}
spec = importlib.util.spec_from_file_location('nat36', DC + '/native/native_evidence_model.v2.py')
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
D9 = json.load(open(D9P))
CM = D9['codeMaps']['deficiencyToReasonCode']
common = json.load(open(DC + '/workflows/schemas/evaluator3/common.schema.json'))
D9DEF = common['$defs']['D9Deficiency']['enum']
NATSCH = json.load(open(DC + '/native/native-evidence.schemas.v2.json'))

text = open(NAT, encoding='utf-8').read().splitlines()
table, in_table = {}, False
for line in text:
    if line.startswith('| Native detail | Cause carrier'):
        in_table = True
        continue
    if in_table:
        if not line.startswith('|'):
            break
        cells = [c.strip() for c in line.strip('|').split('|')]
        if set(cells[0]) <= set('-'):
            continue
        name = cells[0].strip('`')
        table[name] = {'d9Class': cells[3], 'existingCode': cells[4].strip('`')}
R['section10Table'] = table
DEFICIENCIES = list(table)


def find_key(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                return v
            hit = find_key(v, key)
            if hit is not None:
                return hit
    elif isinstance(o, list):
        for v in o:
            hit = find_key(v, key)
            if hit is not None:
                return hit
    return None


R['nativeSchemaPublicD9Termination'] = find_key(NATSCH, 'publicD9Termination')
ENTRY = {'input-closure-incomplete': ('references', 'lockfile-missing'), 'resolution-incomplete': ('references', None), 'external-consumers-unknown': ('references', None),
         'derivation-policy-unmet': ('types', None), 'provider-unavailable': ('references', 'capability-missing'), 'language-tier-unsupported': ('clones', 'capability-missing'),
         'budget-exhausted': ('references', None), 'confidence-floor-unmet': ('references', None), 'required-relation-missing': ('references', None)}
goldens = {g['scenarioAxes'].get('deficiency'): g for g in D9['goldenCases'] if g['scenarioAxes'].get('deficiency') not in (None, 'none')}
rows = {}
for d in DEFICIENCIES:
    rel, cause = ENTRY[d]
    t = N.run_termination(N.stage_authority('complete'), [{'relation': rel, 'deficiency': d, 'nativeCause': cause}])
    try:
        dm = N.d9_map(d)['code']
    except Exception as exc:  # noqa: BLE001
        dm = 'REFUSED: ' + str(exc)[:80]
    member = d in D9DEF
    d9code = CM.get(d) if member else CM.get('verdict-indeterminate')
    g = goldens.get(d)
    rows[d] = {'isD9DeficiencyMember': member, 'd9OwnerCode': d9code, 'd9OwnerRoute': ('codeMaps.deficiencyToReasonCode[%s]' % d) if member else 'not a D9Deficiency member -> verdict-indeterminate',
               'section10ExistingCode': table[d]['existingCode'], 'modelRunTermination': t['d9']['code'], 'modelD9Map': dm,
               'd9Golden': {'id': g['id'], 'reasonCodes': g['expectedTermination'].get('reasonCodes')} if g else None,
               'section10EqualsD9Owner': table[d]['existingCode'] == d9code, 'modelEqualsD9Owner': t['d9']['code'] == d9code}
    print('%-28s D9member=%-5s D9=%-34s s10=%-32s model=%-32s d9_map=%s' % (d, member, d9code, table[d]['existingCode'], t['d9']['code'], dm), flush=True)
R['perDeficiency'] = rows
R['section10DisagreesWithD9'] = sorted(d for d, r in rows.items() if not r['section10EqualsD9Owner'])
R['modelDisagreesWithD9'] = sorted(d for d, r in rows.items() if not r['modelEqualsD9Owner'])
R['modelDisagreesWithSection10'] = sorted(d for d, r in rows.items() if r['modelRunTermination'] != r['section10ExistingCode'])
print('\ns10 != D9 owner:', R['section10DisagreesWithD9'], '| model != D9 owner:', R['modelDisagreesWithD9'], '| model != s10:', R['modelDisagreesWithSection10'])

nat_all = '\n'.join(text)
was = open(WAS, encoding='utf-8').read()
R['ownerSentences'] = {
    'native4.6-termination-is-section10-columns': 'the **public D9 termination** of the Run\nor step that carries the requirement, which is unchanged and still the §10 class/code columns' in nat_all
                                                    or ('public D9 termination' in nat_all and 'still the §10 class/code columns' in nat_all),
    'native4.6-per-requirement-is-DeficiencyV2-never-D9Deficiency': 'That projected value is a `DeficiencyV2` member and **never** `D9Deficiency`' in nat_all,
    'native10-inherits-d9-v1.14-unchanged': 'inherits `d9-exit-contract.v1.14.json` **unchanged**' in nat_all,
    'native10-says-D9-class-host-owned': 'D9 class (host-owned)' in nat_all and 'D9 class assignment is\nhost-owned' in nat_all,
    'workflows-D9Deficiency-carries-every-whole-Run-termination': '`D9Deficiency` is **unchanged** and still carries every whole-Run and\ncomparison-step termination' in was,
    'workflows-public-D9-route-for-such-a-Run-is-native10': 'the public D9\nroute for a Run carrying such a requirement is still native §10\'s' in was,
    'd9Deficiency-description-four-native-only-project-as-indeterminate': 'Four native sufficiency outcomes (derivation-policy-unmet, external-consumers-unknown, input-closure-incomplete, resolution-incomplete) have NO member here at all' in common['$defs']['D9Deficiency']['description'],
    'd9-codeMaps-rule': D9['codeMaps']['rule'],
    'd9-codeDerivation': D9['causeModel']['codeDerivation']}
R['publishedPerRequirementD9Code'] = False
R['publishedPerRequirementD9CodeReason'] = ('native s4.6 projects a per-requirement outcome as a DeficiencyV2 member (repair EvidenceRequirement.deficiency) with no D9 code; the '
                                            'only D9 code for a requirement is the class/code of the Run or step carrying it, which s4.6 names as the s10 columns and '
                                            'workflows-and-surfaces names as D9Deficiency whole-Run terminations derived by the D9 codeMaps')
print('owner sentences:', json.dumps({k: v for k, v in R['ownerSentences'].items() if isinstance(v, bool)}, indent=1))


def candidate_run_termination(stage, coverage_entries):
    """Proposed successor: the D9 owner's deficiencyToReasonCode for D9Deficiency members; VERDICT.INDETERMINATE for the four native-only."""
    if stage['authority'] == 'none':
        return {'authority': 'none', 'runSealed': False, 'factsMinted': 0, 'd9': stage['d9'], 'typedDetail': None}
    deficient = [e for e in coverage_entries if e.get('deficiency')]
    if stage['d9']['class'] == 'success' and deficient:
        worst = min((e['deficiency'] for e in deficient), key=N.PRECEDENCE_V2.index)
        code = CM[worst] if worst in D9DEF else CM['verdict-indeterminate']
        return {'authority': 'authoritative', 'runSealed': True, 'factsMinted': len(coverage_entries), 'd9': {'class': 'indeterminate', 'exitCode': 3, 'code': code},
                'typedDetail': {'carrier': N._TYPED_DETAIL, 'deficiency': worst, 'nativeCauses': sorted({e.get('nativeCause') for e in deficient if e.get('nativeCause')})}}
    return N.run_termination(stage, coverage_entries)


cand = {}
for d in DEFICIENCIES:
    rel, cause = ENTRY[d]
    cand[d] = candidate_run_termination(N.stage_authority('complete'), [{'relation': rel, 'deficiency': d, 'nativeCause': cause}])['d9']['code']
R['candidateRunTermination'] = {'codes': cand, 'equalsD9OwnerForAll': all(cand[d] == rows[d]['d9OwnerCode'] for d in DEFICIENCIES),
                                'equalsSection10ForUnaffectedRows': all(cand[d] == table[d]['existingCode'] for d in DEFICIENCIES if d not in R['section10DisagreesWithD9'])}
cases = json.load(open(DC + '/native/native-cases.v2.json'))
cases = cases['cases'] if isinstance(cases, dict) else cases
replay = []
for c in cases:
    if not any(s.get('fn') == 'run_termination' for s in c.get('steps', [])):
        continue
    env = {}
    for s in c['steps']:
        args = json.loads(json.dumps(s.get('args', {})))
        for k, v in list(args.items()):
            if isinstance(v, str) and v.startswith('$') and v[1:] in env:
                args[k] = env[v[1:]]
        if s['fn'] == 'run_termination':
            env[s['bind']] = candidate_run_termination(**args)
        elif s['fn'] in ('stage_authority', 'd9_map'):
            env[s['bind']] = getattr(N, s['fn'])(**args)
        else:
            env[s.get('bind', '_')] = None
    fails = []
    for path, want in c.get('expect', {}).items():
        head = path.lstrip('$').split('.')
        if head[0] not in env or env[head[0]] is None:
            continue
        cur = env[head[0]]
        try:
            for part in head[1:]:
                cur = cur[int(part)] if isinstance(cur, list) else cur[part]
        except Exception:  # noqa: BLE001
            continue
        if cur != want:
            fails.append((path, cur, want))
    replay.append({'case': c['id'], 'failuresUnderCandidate': fails})
R['existingNativeRunTerminationCasesUnderCandidate'] = replay
pkg_entry = {'relation': 'clones', 'deficiency': 'language-tier-unsupported', 'nativeCause': 'capability-missing'}
proj = candidate_run_termination(N.stage_authority('complete'), [pkg_entry])
R['checkIdentityProjectionControlUnderCandidate'] = {'class': proj['d9']['class'], 'exitCode': proj['d9']['exitCode'], 'deficiency': proj['typedDetail']['deficiency'],
                                                     'stillSatisfied': proj['d9']['class'] == 'indeterminate' and proj['d9']['exitCode'] == 3 and proj['typedDetail']['deficiency'] == 'language-tier-unsupported',
                                                     'codeNow': proj['d9']['code']}
multi = next(g for g in D9['goldenCases'] if g['id'] == 'analysis-multiple-deficiencies')
R['limitMultipleDeficiencies'] = {'d9Golden': multi['expectedTermination'], 'modelRunTerminationEmitsOneCode': True,
                                  'note': 'run_termination returns one code (the native-precedence worst); the D9 cause model derives an ordered reasonCodes list with secondaryDeficiencies. Pre-existing helper limit, not V23-S2; recorded, not corrected here.'}
print('candidate:', json.dumps(R['candidateRunTermination'], indent=1))
print('existing native run_termination cases under candidate:', replay)
print('check-identity projection control under candidate:', R['checkIdentityProjectionControlUnderCandidate'])
R['ownersUnchangedAfter'] = R['owners'] == {os.path.relpath(p, S36): sha(p) for p in OWN}
json.dump(R, open(os.path.join(OUT, 'p02-s2-d9.json'), 'w'), indent=1, default=str)
print('owners unchanged:', R['ownersUnchangedAfter'], '\nwrote p02-s2-d9.json')
