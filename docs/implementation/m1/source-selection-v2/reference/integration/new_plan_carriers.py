"""Proposed pre-Plan recognition refusal; no retained Run admission change."""
import copy
KEY='native.framework-recognition-parameter-required'
REMEDY='the new compiler analysis Plan requires exactly one framework-recognition parameter; supply the selected parameter with its retained schema and payload bytes'

def compose(native,common,registry):
    native=copy.deepcopy(native);common=copy.deepcopy(common);registry=copy.deepcopy(registry)
    routes=native['x-opensip-public-route-registry'];assert KEY not in routes['keys']
    assert KEY not in common['$defs']['DomainDetailCode']['enum']
    assert not any(r['code']==KEY for r in registry['records'])
    common['$defs']['DomainDetailCode']['enum'].append(KEY)
    registry['records'].append({'code':KEY,'owner':'native','selector':'new evaluator3 Plan recognition-parameter admission; never retained close_run'})
    registry['records'].sort(key=lambda r:r['code'])
    routes['keys'][KEY]={
      'possibleOrigins':['externally-supplied-spec','host-generated-internal-layer'],'originDependent':True,
      'why':'A new evaluator3 Plan requesting a compiler language mode must select one recognition parameter after native cardinality/schema/vocabulary and selected v3 parameter-cardinality admission. Historical Run closure never applies this new-Plan duty.',
      'notInInternalAliases':'Origin-dependent; no context-free alias is added.',
      'byOriginatingBoundary':{
       'externally-supplied-spec':{'class':'request-rejected','errorCode':'REQUEST.PRECONDITION_FAILED','domainDetail':KEY,'envelopeDetail':KEY,'why':'Known external new-Plan input fails the required parameter precondition.'},
       'host-generated-internal-layer':{'class':'operational-failed','errorCode':'SYSTEM.OUTCOME.ILLEGAL_STATE','faultCause':'host-invariant','domainDetail':None,'envelopeDetail':'HOST.INVARIANT_VIOLATED','operationalCarrier':'the internal decision key is retained in the operational diagnostic record','why':'The host failed to construct the required new-Plan parameter.'}}}
    routes['newPlanCarrierSuccessor']={'selectedCarrier':'urn:opensip:product-v1:workflows:evaluator3:common:4#/$defs/StepTermination',
      'standing':'The joint invocation5/envelope7 boundary uses the composed common4 vocabulary. The unchanged legacy common carrier cannot carry the new public detail and is not the selected new-Plan boundary.',
      'refusalKey':KEY,'remedy':REMEDY,'prePlanBinding':'new_plan_admission.bind with the composed identity v3 registry; retain all old fault ordering before the appended recognition duty',
      'retainedRuns':'No new duty at close_run/open_run_closure; no reclassification of historical missing parameters.'}
    return native,common,registry
