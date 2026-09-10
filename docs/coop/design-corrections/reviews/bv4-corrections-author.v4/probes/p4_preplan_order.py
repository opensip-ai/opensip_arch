"""p4 - the ACTUAL pre-Plan admission order, measured on both the frozen v14 bytes and the corrected bytes.

Reference-model probe. No host, renderer, agent surface, D9 interpreter or Run is executed; every
observation below is a reference-model call or a read of retained source bytes. It answers root's
CX-V4-PREPLAN-BOUNDARY-AND-ATTRIBUTION by traversing a COMPLETE analysis-spec, not a bare
requestedCapabilities array handed straight to the vocabulary helper, and by showing that the
retained-payload path keeps its own classification.

Usage: p4_preplan_order.py <root-of-a-source-copy>
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
DC = ROOT / 'docs/coop/design-corrections'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


N = load('native_p4', DC / 'native/native_evidence_model.v2.py')
BOUND = N.IM.SCHEMA['$defs']['analysis-spec']['properties']['requestedCapabilities']['maxItems']
rows = lambda n: [{'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig',
                   'workspaceRoot': 'apps/u%04d' % i, 'required': True} for i in range(n)]
spec = lambda r, **extra: dict({'schemaVersion': 2, 'requestedCapabilities': r,
                                'policyPackIds': [], 'parameters': []}, **extra)


def outcome(fn):
    """What a caller actually observes: the exception class, whether it is the TYPED refusal, and the
    field/count/limit if it carries them. Exception text length is recorded because the whole point of
    the correction is that the generic path names nothing in ~265000 characters."""
    try:
        fn()
        return {'outcome': 'ADMIT'}
    except Exception as exc:
        typed = isinstance(exc, getattr(N, 'ScopeRefusal', ()))
        out = {'outcome': 'REFUSE', 'exception': type(exc).__name__,
               'isTypedRefusal': typed, 'messageScalars': len(str(exc))}
        if typed:
            out['detail'] = exc.detail
            out['subject'] = '%s:%d>%d' % (exc.subject['field'], exc.subject['count'],
                                           exc.subject['limit'])
            out['class'] = exc.d9['class']
            out['errorCode'] = exc.d9['code']
        return out


report = {'sourceRoot': str(ROOT), 'requestedCapabilitiesMaxItems': BOUND,
          'hasPreplanBoundaryHelper': hasattr(N, 'admit_analysis_spec')}

# 1. The COMPLETE explicitly supplied spec. On frozen bytes there is no owning boundary at all, so the
#    only thing a caller can traverse is raw schema validation - which is exactly the point.
boundary = (N.admit_analysis_spec if hasattr(N, 'admit_analysis_spec')
            else (lambda s: N.validate_foundation('analysis-spec', s)))
report['completeExplicitSpec'] = {
    'atBound': outcome(lambda: boundary(spec(rows(BOUND)))),
    'overBound': outcome(lambda: boundary(spec(rows(BOUND + 1)))),
}

# 2. ORDER. Cardinality before generic schema validation, with the schema still owning shape faults.
report['order'] = {
    'oversizedAndMalformed': outcome(lambda: boundary(spec(rows(BOUND + 1), unknownProperty=True))),
    'wellSizedAndMalformed': outcome(lambda: boundary(spec(rows(4), unknownProperty=True))),
    'wellSizedUnknownCapability': outcome(lambda: boundary(spec(
        [{'capabilityId': 'not-a-capability', 'languageMode': 'ts-tsconfig',
          'workspaceRoot': 'apps/a', 'required': True}]))),
}

# 3. The DEFAULT path takes the same boundary.
units = lambda n: [{'rootPath': 'apps/u%03d' % i, 'languageMode': 'ts-tsconfig',
                    'languageFamily': 'tsjs'} for i in range(n)]
per_ts = len(N.required_default_capabilities('ts-tsconfig'))
fitting = BOUND // per_ts
report['defaultPath'] = {
    'capabilitiesPerTypeScriptUnit': per_ts,
    'largestFittingUnitCount': fitting,
    'rowsAtLargestFitting': fitting * per_ts,
    'headroomAtLargestFitting': BOUND - fitting * per_ts,
    'atLargestFitting': outcome(lambda: N.default_capability_selection(units(fitting), [])),
    'oneUnitBeyond': outcome(lambda: N.default_capability_selection(units(fitting + 1), [])),
}

# 4. The RETAINED path is a separate concern, left alone. AMENDED at checkpoint 3: this block
#    originally said a cardinality guard in the shared vocabulary helper WOULD have reclassified
#    retained corruption as a request refusal. Root showed that is not reachable on the current path -
#    admit_run obtains the retained analysis-spec through payload(..., 'analysis-spec'), which
#    schema-validates it, so an oversized array refuses there and never reaches the helper. The claim
#    is withdrawn; what remains is an architectural separation and the measurements below, which are
#    unchanged. Read-only ordering evidence over retained source, not an executed Run.
idm = (DC / 'foundation/identity-model.py').read_text()
call = 'admit_requested_capabilities(analysis_spec[\'requestedCapabilities\'])'
report['retainedPath'] = {
    'scopeRefusalIsAnAdmissionError': issubclass(N.ScopeRefusal, N.AdmissionError),
    'admitRunInvokesTheVocabularyHelperOverTheRetainedSpec': call in idm,
    'admitRunCatchesNativeAdmissionError': 'except _native.AdmissionError' in idm,
    'vocabularyHelperOnAnOversizedArray': outcome(
        lambda: N.admit_requested_capabilities(rows(BOUND + 1))),
}

# 5. The two remaining carrier mirrors root found, read where a consumer would look them up.
route = json.loads((DC / 'native/native-evidence.schemas.v2.json').read_text())
route = route['x-opensip-public-route-registry']['keys']['native.release-capability-undeclared']['route']
doc = ' '.join(N.release_absence_details.__doc__.split())
report['carrierMirrors'] = {
    'routeAnnotationNamesOriginalInvocationCarrier':
        'CommandEnvelope.availability' in route['operationalCarrier'],
    'routeAnnotationStillPresentsSupersededCarrierAsTheRoute':
        'DoctorResult.defects[] for an environment report, or StepTermination.domainDetail on the step'
        in route['operationalCarrier'],
    'legacyHelperDeclaresItselfSuperseded': doc.startswith('SUPERSEDED, NON-AUTHORITATIVE'),
    'legacyHelperClaimsAWrongComposition':
        "SUPERSEDED SHAPE: this helper returns ONE STEP's account" in doc,
}
src = (DC / 'native/native_evidence_model.v2.py').read_text()
body = src[src.index('def invocation_availability'):]
body = body[:body.index('\ndef ', 1)]
report['carrierMirrors']['actualCompositionUsesNotices'] = (
    'release_absence_notices' in body and 'release_absence_details' not in body)

print(json.dumps(report, indent=2))
