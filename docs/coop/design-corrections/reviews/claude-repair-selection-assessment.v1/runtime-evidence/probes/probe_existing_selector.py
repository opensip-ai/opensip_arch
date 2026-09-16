"""Probe: is there an EXISTING authoritative selector/aggregation for ClosedWorldV2?

Census every read site in the frozen source, then behaviourally test the only
aggregation that exists (atom_model._conservative_entry) against what repair's gate needs.

Author synthetic evidence only.
"""
import copy, json, importlib.util, re, sys
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v31')
DC = SRC / 'docs/coop/design-corrections'
FOUND = DC / 'foundation'
OUT = Path(__file__).resolve().parent / 'probe-existing-selector.json'

sys.path.insert(0, str(FOUND))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


report = {'scope': 'existing ClosedWorldV2 selector / aggregation census', 'parts': []}

def step(name, **kw):
    row = {'part': name, **kw}
    report['parts'].append(row)
    print(json.dumps(row, default=str)[:1600])
    return row


# -------------------------------------------------------------- 1. read-site census
PAT = re.compile(r"closedWorld|closed_world|ClosedWorldV2")
sites = []
for path in sorted(DC.rglob('*')):
    if not path.is_file() or 'reviews' in path.parts:
        continue
    if path.suffix not in ('.py', '.json', '.md'):
        continue
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    for m in PAT.finditer(text):
        line_no = text[:m.start()].count('\n') + 1
        line = text.splitlines()[line_no - 1].strip()
        sites.append({'file': str(path.relative_to(SRC)), 'line': line_no,
                      'text': line[:200]})
contracts = []
for path in sorted((SRC / 'docs/v2/contracts/product-v1').glob('*.md')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    for m in PAT.finditer(text):
        line_no = text[:m.start()].count('\n') + 1
        contracts.append({'file': str(path.relative_to(SRC)), 'line': line_no,
                          'text': text.splitlines()[line_no - 1].strip()[:200]})
step('census-counts', designCorrectionsSites=len(sites), liveContractSites=len(contracts),
     files=sorted({s['file'] for s in sites}))
report['census'] = {'designCorrections': sites, 'liveContracts': contracts}


# -------------------------------------------------------------- 2. the only aggregation
A = load('probe_atom_model', FOUND / 'atom_model.v1.py')
has_conservative = hasattr(A, '_conservative_entry')
src_lines = (FOUND / 'atom_model.v1.py').read_text().splitlines()
start = next(i for i, l in enumerate(src_lines) if l.startswith('def _conservative_entry'))
step('aggregation-found',
     helper='atom_model.v1._conservative_entry',
     present=has_conservative,
     file='docs/coop/design-corrections/foundation/atom_model.v1.py',
     line=start + 1,
     docstring=src_lines[start + 1].strip(),
     rankedFields=[l.strip() for l in src_lines[start:start + 27] if '_rank = {' in l],
     closedWorldRule=[l.strip() for l in src_lines[start:start + 27] if 'closedWorld' in l])


# -------------------------------------------------------------- 3. behavioural test:
# does that fold minimise what repair's gate actually reads (deadCodeRepairEligible)?
def cov(relation, rung, cw):
    return {'schemaVersion': 3,
            'key': {'relation': relation, 'resolution': rung,
                    'sourceUniverse': '0' * 64, 'targetUniverse': '0' * 64,
                    'subjectScopeCommitment': 'sha256:' + '0' * 64},
            'entry': {'relation': relation, 'resolution': rung, 'coverage': 'complete',
                      'examinedUniverse': {'subjectScopeCommitment': 'sha256:' + '0' * 64,
                                           'subjectCount': 1},
                      'resolutionCompleteness': {'state': 'not-applicable', 'attempted': False,
                                                 'examinedExhaustive': True, 'stageTerminal': 'complete',
                                                 'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []},
                      'closedWorld': cw, 'derivationKinds': [], 'confidenceMillionths': 1000000,
                      'deficiency': None, 'nativeCause': None}}

ELIGIBLE_BUT_OPEN = {'exportsClosed': 'open', 'entryPointsRecognized': 'all',
                     'nonliteralLoading': 'none', 'externalConsumers': 'possible',
                     'dynamicDispatch': 'not-applicable', 'reasons': ['external-consumers:possible'],
                     'deadCodeRepairEligible': True}
INELIGIBLE_BUT_CLOSED = {'exportsClosed': 'closed', 'entryPointsRecognized': 'partial',
                         'nonliteralLoading': 'none', 'externalConsumers': 'none-declared',
                         'dynamicDispatch': 'not-applicable', 'reasons': [],
                         'deadCodeRepairEligible': False}

picked, cited = A._conservative_entry('file', [('coverage2:' + 'a' * 64, cov('file', 'enumerated', copy.deepcopy(INELIGIBLE_BUT_CLOSED))),
                                               ('coverage2:' + 'b' * 64, cov('file', 'enumerated', copy.deepcopy(ELIGIBLE_BUT_OPEN)))])
picked_rev, _ = A._conservative_entry('file', [('coverage2:' + 'b' * 64, cov('file', 'enumerated', copy.deepcopy(ELIGIBLE_BUT_OPEN))),
                                               ('coverage2:' + 'a' * 64, cov('file', 'enumerated', copy.deepcopy(INELIGIBLE_BUT_CLOSED)))])
step('aggregation-does-not-minimise-the-gated-flag',
     inputs={'entry1': {'exportsClosed': 'closed', 'deadCodeRepairEligible': False},
             'entry2': {'exportsClosed': 'open', 'deadCodeRepairEligible': True}},
     foldedClosedWorld=picked['closedWorld'],
     foldedClosedWorldReversedInputOrder=picked_rev['closedWorld'],
     orderStable=picked['closedWorld'] == picked_rev['closedWorld'],
     foldedDeadCodeRepairEligible=picked['closedWorld']['deadCodeRepairEligible'],
     anyInputIneligible=True,
     note='the fold ranks exportsClosed only and copies that entry\'s whole record; '
          'deadCodeRepairEligible is carried along, not minimised. Both inputs are '
          'schema-valid ClosedWorldV2 records.')


# -------------------------------------------------------------- 4. scope of that fold
contract = (FOUND / 'atom-evaluation-contract.v1.md').read_text()
limits = [l.strip() for l in contract.splitlines()
          if 'closed-world' in l or 'closed world' in l]
step('aggregation-scope',
     ownerContract='docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md',
     statedLimits=limits,
     composesOver='same-relation Coverage partitions selected for ONE atom query '
                  '(relation, rung, sourceUniverse, endpoint)',
     producesRunLevelRecord=False,
     namedByRepairOwner=False,
     note='repair (workflows section 6, repair.schema.json, workflows_model.v1) never '
          'names this helper, and it yields a per-relation entry, not a Run-level record')

OUT.write_text(json.dumps(report, indent=2, default=str) + '\n')
print('\nWROTE', OUT)
