"""Bounded evidence for v11-A3: does the RELEASED reference actually terminate on cyclic local
references, and does terminating change any verdict?

Loads the retained, immutable v10 release read-only. Writes nothing outside this output directory.
Run with `-I -B` so no __pycache__ is written beside the live repository source.

Four things are measured, no more:
  1. an actual cycle NEGATIVE  - a cyclic $def carrying an unannotated governed leaf must refuse,
     and must refuse by returning rather than by exhausting the stack;
  2. the annotated POSITIVE control - the same cycle with the leaf annotated must admit;
  3. both guards - walk()'s container-$ref guard and governed_form()'s alias-chain guard - reached
     by a container cycle and by an alias-only cycle respectively;
  4. whether the guard is per-path or global, which is the one way a "just make it terminate"
     reading could change a verdict: the same alias reached at two paths must produce TWO sightings.
"""
import copy, hashlib, importlib.util, json, sys, time
from pathlib import Path

# The repository's retained copy of the release (reviews/digest-corrections-author.v10/
# author-source/.../identity-model.py) has no sibling canonical.py or schema JSON, so it cannot be
# imported in place. Rather than copy anything, this loads the SAME released bytes from my retained
# v10 work tree, which carries the correct frozen-v11 neighbours. Both paths are hashed below and
# must agree; nothing is written to either, and -B keeps bytecode out of both trees.
RELEASE = Path('/tmp/opensip-design-corrections/digest-corrections-author.v10/work'
               '/docs/coop/design-corrections/foundation/identity-model.py')
RETAINED_IN_REPOSITORY = Path(
    '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
    '/digest-corrections-author.v10/author-source/docs/coop/design-corrections'
    '/foundation/identity-model.py')
OUT = Path('/tmp/opensip-design-corrections/cycle-wording-author.v1/probes'
           '/result-cycle-termination.v1.json')

spec = importlib.util.spec_from_file_location('released_identity_model', RELEASE)
M = importlib.util.module_from_spec(spec)
sys.modules['released_identity_model'] = M
spec.loader.exec_module(M)

BARE = {'$ref': '#/$defs/DigestHex'}
ANNOTATION = {'representation': 'raw-artifact', 'retention': 'not-joined',
              'authority': 'coauthor cycle probe', 'reason': 'a control, not a shipped field'}

def leaf(annotated):
    return dict(BARE, **{'x-opensip-digest': copy.deepcopy(ANNOTATION)}) if annotated else dict(BARE)

def self_cycle(annotated):
    """CycleA contains a governed leaf and a property that references CycleA itself."""
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    d['$defs']['CycleA'] = {'type': 'object', 'properties': {
        'leaf': leaf(annotated), 'next': {'$ref': '#/$defs/CycleA'}}}
    d['$defs']['FilePayloadV1']['properties']['probe'] = {'$ref': '#/$defs/CycleA'}
    return d

def mutual_cycle(annotated):
    """CycleB -> CycleC -> CycleB, the governed leaf hanging off the second hop."""
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    d['$defs']['CycleB'] = {'type': 'object', 'properties': {'down': {'$ref': '#/$defs/CycleC'}}}
    d['$defs']['CycleC'] = {'type': 'object', 'properties': {
        'leaf': leaf(annotated), 'up': {'$ref': '#/$defs/CycleB'}}}
    d['$defs']['FilePayloadV1']['properties']['probe'] = {'$ref': '#/$defs/CycleB'}
    return d

def alias_only_cycle():
    """AliasP -> AliasQ -> AliasP with no governed leaf anywhere on it. This is the cycle that
    governed_form() itself must survive: it resolves $refs looking for a governed form and would
    recurse forever without its own chain guard. walk() never gets a form here, so there is no
    sighting and the document must simply admit."""
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    d['$defs']['AliasP'] = {'$ref': '#/$defs/AliasQ'}
    d['$defs']['AliasQ'] = {'$ref': '#/$defs/AliasP'}
    d['$defs']['FilePayloadV1']['properties']['probe'] = {'$ref': '#/$defs/AliasP'}
    return d

def shared_alias_two_paths():
    """One container alias reached at TWO selector properties, unannotated at both. If a bounding
    strategy marked definitions globally visited, the second path would never be walked."""
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    d['$defs']['SharedC'] = {'type': 'object', 'properties': {'leaf': leaf(False)}}
    d['$defs']['FilePayloadV1']['properties']['probeOne'] = {'$ref': '#/$defs/SharedC'}
    d['$defs']['FilePayloadV1']['properties']['probeTwo'] = {'$ref': '#/$defs/SharedC'}
    return d

def cycle_then_sibling():
    """A cycle visited BEFORE an unannotated governed sibling. A reader who took "terminate on
    cycles" to mean "stop traversing when a cycle appears" would never reach the sibling."""
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    d['$defs']['CycleD'] = {'type': 'object', 'properties': {
        'leaf': leaf(True), 'next': {'$ref': '#/$defs/CycleD'}}}
    props = d['$defs']['FilePayloadV1']['properties']
    props['probeCycle'] = {'$ref': '#/$defs/CycleD'}
    props['probeSibling'] = leaf(False)
    return d

def verdict(document):
    start = time.perf_counter()
    try:
        M.relation_annotation_closure('file', copy.deepcopy(document))
        outcome = 'ADMIT'
    except RecursionError:
        outcome = 'RECURSION_ERROR'
    except Exception as exc:
        outcome = str(exc).split(':')[0]
    return outcome, round((time.perf_counter() - start) * 1000, 2)

def sightings(document, prefix):
    coverage = M.relation_digest_annotation_coverage(copy.deepcopy(document))
    return [s['path'] for s in coverage['byRelation']['file']['sightings'] if prefix in s['path']]

cases = {
    'self-cycle-unannotated-leaf': self_cycle(False),
    'self-cycle-annotated-leaf': self_cycle(True),
    'mutual-cycle-unannotated-leaf': mutual_cycle(False),
    'mutual-cycle-annotated-leaf': mutual_cycle(True),
    'alias-only-cycle-no-governed-leaf': alias_only_cycle(),
    'shared-alias-at-two-paths-unannotated': shared_alias_two_paths(),
    'cycle-then-unannotated-sibling': cycle_then_sibling(),
}
measured = {}
for name, document in cases.items():
    outcome, ms = verdict(document)
    measured[name] = {'verdict': outcome, 'elapsedMs': ms,
                      'sightings': sightings(document, 'probe')}

result = {
    'standing': 'actual Claude COAUTHOR session 5dec928a bounded evidence for the v11-A3 wording '
                'assessment. Schema/reference measurement only. No acceptance, readiness, product '
                'qualification or implementation authority. Not the independent reviewer, whose v11 '
                'review is still finalizing and whose final verdict is not claimed here.',
    'releasedSource': {
        'loadedFrom': str(RELEASE),
        'sha256': hashlib.sha256(RELEASE.read_bytes()).hexdigest(),
        'retainedInRepository': str(RETAINED_IN_REPOSITORY),
        'retainedSha256': hashlib.sha256(RETAINED_IN_REPOSITORY.read_bytes()).hexdigest(),
        'byteIdentical': (hashlib.sha256(RELEASE.read_bytes()).hexdigest()
                          == hashlib.sha256(RETAINED_IN_REPOSITORY.read_bytes()).hexdigest()),
        'loadedReadOnly': True, 'edited': False},
    'recursionLimitAtRun': sys.getrecursionlimit(),
    'cases': measured,
    'guardsReached': {
        'walkContainerRefGuard': ['self-cycle-unannotated-leaf', 'self-cycle-annotated-leaf',
                                  'mutual-cycle-unannotated-leaf', 'mutual-cycle-annotated-leaf',
                                  'cycle-then-unannotated-sibling'],
        'governedFormAliasChainGuard': ['alias-only-cycle-no-governed-leaf'],
    },
    'terminationObserved': all(v['verdict'] != 'RECURSION_ERROR' for v in measured.values()),
    'guardIsPerPathNotGlobal': len(measured['shared-alias-at-two-paths-unannotated']['sightings']) == 2,
    'cycleDoesNotStopTheTraversal':
        measured['cycle-then-unannotated-sibling']['verdict'] == 'RELATION_DIGEST_UNANNOTATED',
}
OUT.write_text(json.dumps(result, indent=2) + '\n')
for name, value in measured.items():
    print('%-40s %-32s %6.2f ms  %s' % (name, value['verdict'], value['elapsedMs'], value['sightings']))
print('terminationObserved          :', result['terminationObserved'])
print('guardIsPerPathNotGlobal      :', result['guardIsPerPathNotGlobal'])
print('cycleDoesNotStopTheTraversal :', result['cycleDoesNotStopTheTraversal'])
