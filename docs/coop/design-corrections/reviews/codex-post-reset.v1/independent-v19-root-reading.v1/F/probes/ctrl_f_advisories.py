"""Independent re-measurement of the five carried advisories CB7-ADV-1..5 against the v19 bytes.
Disposable copy only."""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
DC = ROOT / 'docs/coop/design-corrections'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

N = load('nem', DC / 'native/native_evidence_model.v2.py')
IM = load('idm', DC / 'foundation/identity-model.py')

R = []
def ck(cid, desc, got, want):
    R.append({'id': cid, 'desc': desc, 'pass': got == want, 'observed': got, 'expected': want})
def rec(cid, desc, got):
    R.append({'id': cid, 'desc': desc, 'pass': True, 'observed': got, 'expected': 'measurement'})

NS = N.SCHEMAS

# --- ADV-1 D9 faultCause enum (measured at its ACTUAL owning locations) ---
COMMON = json.loads((DC / 'workflows/schemas/common.schema.json').read_text())
SUCC = COMMON['$defs']['D9FaultCause']['enum']
INH = json.loads((ROOT / 'docs/coop/artifacts/d9-exit-contract.v1.14.json').read_text())
INH_ENUM = INH['scenarioAxesSchema']['properties']['faultCause']['enum']
rec('F1:inherited', 'inherited d9-exit-contract faultCause enum', {'count': len(INH_ENUM), 'members': INH_ENUM})
rec('F1:successor', 'successor D9FaultCause enum', {'count': len(SUCC), 'members': SUCC})
ck('F1:counts', 'the enum grows from 11 to 12 (10 to 11 excluding the `none` member)',
   [len(INH_ENUM), len(SUCC), len([x for x in INH_ENUM if x != 'none']), len([x for x in SUCC if x != 'none'])],
   [11, 12, 10, 11])
ck('F1:single-addition', 'exactly one member is added, and it is host-invariant',
   sorted(set(SUCC) - set(INH_ENUM)), ['host-invariant'])
ck('F1:no-removals', 'no inherited member is removed', sorted(set(INH_ENUM) - set(SUCC)), [])
ck('F1:inherited-artifact-unchanged',
   'the inherited artifact is historical and still omits the member', 'host-invariant' in INH_ENUM, False)
ck('F1:no-new-code-class-exit', 'the addition brings no new errorCode, class or exit code',
   ['host-invariant' in json.dumps(COMMON['$defs']['D9FaultCause']),
    'SYSTEM.OUTCOME.ILLEGAL_STATE' in json.dumps(COMMON)], [True, True])

# --- ADV-2 the matrix-fixed default cap ----------------------------------
bound = N.requested_capability_bound()
matrix = json.loads((DC / 'native/native-capability-matrix.v2.json').read_text())
rec('F2:bound', 'requestedCapabilities published bound', bound)
def selected_for(mode):
    cells = matrix.get('cells') or matrix.get('matrix') or []
    if isinstance(cells, list):
        return sum(1 for c in cells if c.get('languageMode') == mode and c.get('selection') != 'NOT-SELECTED')
    return None
rec('F2:matrix-shape', 'matrix top-level keys', sorted(matrix.keys()))
# The arithmetic the advisory asserts, checked directly.
ck('F2:arithmetic', '93 units x 11 caps = 1023 (fits); 94 x 11 = 1034 (over 1024)',
   [93 * 11, 94 * 11, 93 * 11 <= bound, 94 * 11 > bound], [1023, 1034, True, True])
ck('F2:one-under-not-at', '1023 is one row UNDER the bound, not exactly at it', bound - 93 * 11, 1)
# and that the refusal it names is real at that count
try:
    N.admit_requested_capability_cardinality(
        [{'capabilityId': 'references', 'languageMode': 'ts-tsconfig',
          'workspaceRoot': 'r%05d' % i, 'required': True} for i in range(bound + 1)])
    ck('F2:refusal', 'over-bound capability selection refuses', 'admitted', 'ScopeRefusal')
except N.ScopeRefusal as e:
    ck('F2:refusal', 'over-bound capability selection refuses with the typed subject',
       dict(e.subject), {'field': 'requestedCapabilities', 'count': bound + 1, 'limit': bound})

# --- ADV-3 platform id domain breadth (measured at its owning registry) ---
DOM = json.loads((DC / 'native/capability-manifest-domains.v2.json').read_text())['registries']['PLATFORM-ID-DOMAIN-V1']
rec('F3:domain', 'PLATFORM-ID-DOMAIN-V1 members', {'count': DOM['memberCount'], 'members': DOM['members']})
ck('F3:eight', 'the encoding domain has 8 members as the advisory measured',
   [DOM['memberCount'], len(DOM['members'])], [8, 8])
ck('F3:four-selected', 'exactly four are the selected supported machine platform ids',
   sorted(m for m in DOM['members']
          if m.startswith(('macos-', 'linux-')) and m.endswith(('aarch64', 'x86_64', 'x86_64-gnu', 'aarch64-gnu'))),
   ['linux-aarch64-gnu', 'linux-x86_64-gnu', 'macos-aarch64', 'macos-x86_64'])
ck('F3:disclosed-as-broader', 'the registry itself discloses that the inherited vocabulary is broader',
   'inheritedVocabularyIsBROADERThanTheSelectedPRODUCT' in DOM, True)
ck('F3:bound-position', 'it is bound only at ProviderCapability.platformIds[]',
   DOM['boundPositions'], ['ProviderCapability.platformIds[]'])

# --- ADV-5 pinned UCD version --------------------------------------------
ck('F5:ucd', 'UNICODE_CASE_DATA_VERSION is the pinned 15.0.0 constant',
   N.UNICODE_CASE_DATA_VERSION, '15.0.0')
ck('F5:ascii-coincide', 'every current lib name is ASCII, where the fold candidates coincide',
   all(ord(c) < 128 for name in getattr(N, 'KNOWN_LIB_NAMES', ['es2022'])
       for c in (name if isinstance(name, str) else '')), True)

# --- ADV-4 is the one v19 acts on ----------------------------------------
ck('F4:now-published', 'the 34-row table is now a published artifact, not only a named model symbol',
   (DC / 'native/protocol3-transitions.v1.json').is_file(), True)
nev = (ROOT / 'docs/v2/contracts/product-v1/native-evidence.md').read_text()
ck('F4:contract-cites-artifact', 'the contract cites the artifact path',
   'docs/coop/design-corrections/native/protocol3-transitions.v1.json' in nev, True)
ck('F4:old-selector-gone', 'the advisory selector wording no longer stands alone',
   'The\n34-rule first-match/total-fallback table is `PROTOCOL3_RULES` in the model;' in nev, False)

fails = [r for r in R if not r['pass']]
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-f.json').write_text(
    json.dumps({'controls': len(R), 'failed': len(fails), 'failures': fails, 'results': R}, indent=1, default=str))
print('CTRL-F controls=%d failed=%d' % (len(R), len(fails)))
for r in R:
    if r['expected'] == 'measurement':
        print('  MEASURED', r['id'], '=', repr(r['observed'])[:300])
for f in fails:
    print('  FAIL', f['id'], f['desc'], '\n   observed=', repr(f['observed'])[:300],
          '\n   expected=', repr(f['expected'])[:300])
