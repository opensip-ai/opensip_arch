"""p08 - Re-test the carried advisories that are cheaply decidable, rather than restating them.

v9-A1  the 723-byte edition-map figure is reproducible only when the wrapping is stated
v9-A6  the integration builder is fixture composition copied from the checker, not an oracle
v9-A10 pin-inventory truncation is undetectable by the projection validator alone
v9-A2/A3 LEVEL_SPECIFICATION / L1-L3 remain unqualified stand-ins
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import hashlib
import json
from pathlib import Path
import harness

m = harness.load_model()
C = m.C
DC = harness.SUBJECT / 'docs/coop/design-corrections'
out = {}

# ------------------------------------------------------------------------------------- v9-A1: 723
EDITIONS = {'2015': '2015', '2018': '2018', '2021': '2021', '2024': '2024'}
# reconstruct the shipped edition map from the native schema rather than inventing one
native = json.loads((DC / 'native/native-evidence.schemas.v2.json').read_text())


def find_edition_map(node):
    found = []
    if isinstance(node, dict):
        for k, v in node.items():
            if 'edition' in str(k).lower():
                found.append((k, v))
            found.extend(find_edition_map(v))
    elif isinstance(node, list):
        for v in node:
            found.extend(find_edition_map(v))
    return found


hits = find_edition_map(native)
out['editionKeysInNativeSchema'] = [k for k, _ in hits][:12]

# the arithmetic claim itself: wrapped vs bare
sample = {e: {'edition': e} for e in ('2015', '2018', '2021', '2024')}
for label, obj in (('bare-map', sample), ('wrapped', {'edition': sample})):
    b = C.canonical(obj)
    out['canonical_' + label + '_bytes'] = len(b)
out['A1_wrappingChangesLength'] = (out['canonical_wrapped_bytes'] !=
                                   out['canonical_bare-map_bytes'])
out['A1_delta'] = out['canonical_wrapped_bytes'] - out['canonical_bare-map_bytes']
out['A1_note'] = ('the advisory is that the figure is only reproducible when the wrapping is '
                  'STATED; this probe confirms wrapped and bare canonical encodings of the same '
                  'map differ in length, so a bare figure and a wrapped figure are not '
                  'interchangeable. Exact shipped byte counts depend on the shipped map contents.')

# ------------------------------------------------------------- v9-A6: fixture provenance is exact
fixture = DC / 'integration-fixtures.py'
checker = DC / 'foundation/check-identity.py'
declared = None
for line in fixture.read_text().split('\n')[:6]:
    if 'check-identity.py SHA256' in line:
        declared = line.strip().rstrip('.').split()[-1]
out['A6_declaredCheckerSha'] = declared
out['A6_actualCheckerSha'] = hashlib.sha256(checker.read_bytes()).hexdigest()
out['A6_provenanceMatches'] = declared == out['A6_actualCheckerSha']
out['A6_standing'] = ('provenance is exact, but the fixture is COPIED from the checker, so it '
                      'remains synthetic composition and is NOT an independent oracle; advisory '
                      'preserved, not discharged')

# ------------------------------------------------ v9-A10: pin truncation vs projection validation
pins = json.loads((DC / 'foundation/source-pins.v1.json').read_text())
out['A10_pinnedFileCount'] = len(pins['files'])
truncated = {'standing': pins['standing'], 'files': pins['files'][:-1]}
out['A10_truncatedCount'] = len(truncated['files'])
# a projection validator that only checks "every pinned row still matches" cannot see a REMOVED row
out['A10_everyRemainingRowStillMatches'] = all(
    hashlib.sha256((harness.SUBJECT / r['path']).read_bytes()).hexdigest() == r['sha256']
    for r in truncated['files'] if (harness.SUBJECT / r['path']).is_file())
out['A10_note'] = ('with one row deleted every REMAINING row still verifies, so a pure projection '
                   'over the pin list cannot detect truncation; detection requires an independent '
                   'expected count or inventory. Advisory preserved.')

# ------------------------------------------------------- v9-A2/A3: level specification is a stub
model_src = (harness.SUBJ_FOUND / 'identity-model.py').read_text()
out['A2_levelSpecificationMentions'] = model_src.count('LEVEL_SPECIFICATION')
out['A3_l0RecomputedL1L3CustodyOnly'] = ('L0' in model_src and 'L1' in model_src)
out['A2A3_standing'] = ('unchanged by this delta; no normalizer is qualified and the level '
                        'specification bytes are fixture stand-ins, not qualified '
                        'FACT-IDENTITY implementation content')

out['ASSESSMENT'] = {
    'A1_wrappingMatters': out['A1_wrappingChangesLength'],
    'A1_bareVsWrappedDelta': out['A1_delta'],
    'A6_fixtureProvenanceExact': out['A6_provenanceMatches'],
    'A6_stillNotAnOracle': True,
    'A10_truncationUndetectableByProjectionAlone': out['A10_everyRemainingRowStillMatches'],
    'A2A3_unqualifiedStandInsPreserved': True,
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p08.json')
print(json.dumps(out['ASSESSMENT'], indent=2))
print('A1 bare bytes', out['canonical_bare-map_bytes'], 'wrapped bytes', out['canonical_wrapped_bytes'])
