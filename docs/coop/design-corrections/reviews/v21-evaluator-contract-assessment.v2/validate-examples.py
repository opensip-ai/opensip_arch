"""Validate the v2 discriminating examples against the FROZEN v21 schemas.

Design evidence only. Uses the frozen foundation/canonical.py ExactValidator so that
x-opensip-order, exact const/enum and the typed-integer rule are applied exactly as the
contract requires -- not a hand-rolled subset.
"""
import json
import sys
import pathlib

SRC = pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections')
sys.path.insert(0, str(SRC / 'foundation'))
import canonical  # noqa: E402

from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402
from jsonschema import Draft202012Validator, validators  # noqa: E402

IDENT = json.loads((SRC / 'foundation' / 'identity-schemas.v2.json').read_text())
RELPAY = json.loads((SRC / 'foundation' / 'relation-payload-schemas.v2.json').read_text())
NATIVE = json.loads((SRC / 'native' / 'native-evidence.schemas.v2.json').read_text())
WF = {p.stem.replace('.schema',''): json.loads(p.read_text())
      for p in (SRC / 'workflows' / 'schemas').glob('*.json')}

REGISTRY = Registry().with_resources(
    [(d['$id'], Resource.from_contents(d, default_specification=DRAFT202012))
     for d in WF.values() if '$id' in d]
)

ExactValidator = validators.extend(
    Draft202012Validator,
    validators={'const': canonical.exact_const, 'enum': canonical.exact_enum,
                'x-opensip-order': canonical.exact_order},
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine(
        'integer', lambda checker, value: type(value) is int))


def check(label, bundle, selector, value):
    """Validate value against bundle#selector; raise on failure."""
    schema = dict(bundle)
    schema['$ref'] = selector
    canonical.typed(value)
    ExactValidator(schema, registry=REGISTRY).validate(value)
    print('  PASS  %-34s %s' % (label, selector))


U1 = 'a' * 64                      # TypeScript universe #1 (distinct resolved inputs)
U2 = 'b' * 64                      # TypeScript universe #2 (same DOMAIN, different H)
SNAP = 'snapshot2:' + 'c' * 64
CLOSURE = 'closure2:' + 'd' * 64
RELSCHEMA = 'e' * 64               # digest of relation-payload-schemas.v2.json
PAYLOAD1 = '1' * 64
PAYLOAD2 = '2' * 64
BLOB = 'f' * 64

S_F = 'ts-symbol:src/a.ts#f'
S_G = 'ts-symbol:src/a.ts#g'


def scope(universe, subjects, rung='syntactic-name-match'):
    return {'schemaVersion': 2, 'snapshotId': SNAP,
            'sourceUniverse': universe, 'targetUniverse': universe,
            'relation': 'references', 'resolution': rung,
            'enumeratorClosure': CLOSURE, 'subjects': sorted(subjects)}


def fact(universe, payload_digest, rung='syntactic-name-match'):
    return {'schemaVersion': 2, 'snapshotId': SNAP, 'relation': 'references',
            'resolution': rung, 'sourceUniverse': universe, 'targetUniverse': universe,
            'producerClosure': CLOSURE, 'payloadSchemaDigest': RELSCHEMA,
            'payloadDigest': payload_digest,
            'anchors': [{'path': 'src/a.ts', 'blobDigest': BLOB,
                         'startByte': 0, 'endByte': 12}],
            'confidenceMillionths': 1000000}


REFERENCES_PAYLOAD = {'referrer': S_F, 'name': 'helper'}

COVERAGE_COMPLETE = {
    'schemaVersion': 3,
    'key': {'relation': 'references', 'resolution': 'syntactic-name-match',
            'sourceUniverse': U1, 'targetUniverse': U1,
            'subjectScopeCommitment': 'sha256:' + '9' * 64},
    'entry': {'relation': 'references', 'resolution': 'syntactic-name-match',
              'coverage': 'complete',
              'examinedUniverse': {'subjectScopeCommitment': 'sha256:' + '9' * 64,
                                   'subjectCount': 2},
              'resolutionCompleteness': {'state': 'not-applicable', 'attempted': False,
                                         'examinedExhaustive': True, 'stageTerminal': 'complete',
                                         'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []},
              'closedWorld': {'exportsClosed': 'unknown', 'entryPointsRecognized': 'all',
                              'nonliteralLoading': 'none', 'externalConsumers': 'unknown',
                              'dynamicDispatch': 'not-applicable', 'reasons': [],
                              'deadCodeRepairEligible': False},
              'derivationKinds': [], 'confidenceMillionths': 1000000,
              'deficiency': None, 'nativeCause': None}}

POLICY = {
    'schemaFamily': 'opensip.product.policy', 'schemaMajor': 1,
    'gateSeverityAtLeast': 'warning',
    'rules': [{
        'ruleId': 'r1',
        'ruleProgramRef': {'contributionId': 'opensip.core', 'ruleStableId': 'r1',
                           'semanticsMajor': 1, 'programDigest': '3' * 64},
        'enabled': True, 'severity': 'error', 'gate': True,
        'subjectEnumeration': {'universe': 'native.semantic-universe.typescript.v2',
                               'subjectKind': 'symbol'},
        'emitWhen': {'op': 'exists', 'relation': 'references',
                     'minResolution': 'syntactic-name-match', 'filters': []},
        'evidenceUse': []}]}

WAIVERS = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1,
           'waivers': [{'waiverId': 'w1',
                        'target': {'ruleId': 'r1', 'subjectPath': S_F},
                        'reason': 'known, tracked', 'expires': None}]}

RULE_PROGRAM = {'schemaVersion': 1, 'policyDigest': '4' * 64,
                'rules': [{'ruleId': 'r1',
                           'ruleProgramRef': POLICY['rules'][0]['ruleProgramRef'],
                           'emitWhen': POLICY['rules'][0]['emitWhen']}]}

print('G3 / G7 example (relation `references`: no coverageTotality row)')
check('subject-scope S1 (U1, f+g)', IDENT, '#/$defs/subject-scope', scope(U1, [S_F, S_G]))
check('ReferencesPayloadV1', RELPAY, '#/$defs/ReferencesPayloadV1', REFERENCES_PAYLOAD)
check('fact F1 (U1, subject f)', IDENT, '#/$defs/fact', fact(U1, PAYLOAD1))
check('CoverageResultV3 complete', NATIVE, '#/$defs/CoverageResultV3', COVERAGE_COMPLETE)
check('PolicyDocumentV1 (rule r1)', WF['policy-document'], '#/$defs/PolicyDocumentV1', POLICY)
check('RuleProgramV1 projection', WF['policy-document'], '#/$defs/RuleProgramV1', RULE_PROGRAM)
check('WaiverSetV1 (waives f)', WF['policy-document'], '#/$defs/WaiverSetV1', WAIVERS)

print('\nG1 example (two universes of ONE domain class)')
check('subject-scope S2 (U2, f only)', IDENT, '#/$defs/subject-scope', scope(U2, [S_F]))
check('fact F2 (U2, subject f)', IDENT, '#/$defs/fact', fact(U2, PAYLOAD2))

print('\nPredicate-proof tuple uniqueness probe')
proofs = [{'ruleId': 'r1', 'subjectId': S_F, 'predicateId': 'p', 'operation': 'exists',
           'inputRefs': [], 'scopeIds': ['scope2:' + '7' * 64], 'value': 'true',
           'witnessDigest': h * 64} for h in ('5', '6')]
try:
    check('per-universe duplicate tuple', IDENT,
          '#/$defs/proof-bundle/properties/predicateProofs', proofs)
    print('  !! duplicate (ruleId,subjectId,predicateId) was ADMITTED')
except Exception as exc:
    print('  REFUSED (as predicted): %s' % str(exc).splitlines()[0][:96])

print('\nSubjectIdV1 / LogicalPath overlap probe')
check('S_F is a valid SubjectIdV1', RELPAY, '#/$defs/SubjectIdV1', S_F)
check('S_F is ALSO a valid LogicalPath', WF['common'], '#/$defs/LogicalPath', S_F)

print('\nALL EXAMPLE RECORDS VALIDATED AGAINST FROZEN v21 SCHEMAS')
