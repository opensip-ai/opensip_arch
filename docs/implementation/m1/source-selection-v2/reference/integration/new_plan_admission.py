"""Proposed new evaluator3 Plan admission and its native public route binding.

No Plan is minted here. Bound model objects are trusted reference dependencies,
not public caller authority. Retained closure never invokes this entry point.
"""
import ast,copy,types
KEY='native.framework-recognition-parameter-required'
PARAMETER='foundation/framework-recognition-plan.schema.v1.json'


def bind(native_raw,native_model,identity_model,features,native_schema):
    names={'admit_analysis_spec','normalize_internal_key','public_termination_for','bounded_subject','_detail','failure_envelope_errors'}
    nodes=[n for n in ast.parse(native_raw).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    ns=dict(vars(native_model));ns['IM']=identity_model
    ns['PUBLIC_ROUTE_REGISTRY']=copy.deepcopy(native_schema['x-opensip-public-route-registry'])
    ns['PUBLIC_ROUTE_REMEDIES']={**native_model.PUBLIC_ROUTE_REMEDIES,KEY:ns['PUBLIC_ROUTE_REGISTRY']['newPlanCarrierSuccessor']['remedy']}
    # Only this copied entry point changes its IM binding. Other native source
    # helpers retain their original cardinality/schema/vocabulary laws.
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-native-helpers#selected-v3-preplan-and-public-route','exec'),ns)
    language_map=identity_model.SCHEMA['x-opensip-digest-domains']['languageModes']['map']
    def admit(spec):
        accepted=ns['admit_analysis_spec'](spec)
        try:
            features.admit_new_plan_recognition_parameter(accepted['parameters'],accepted['requestedCapabilities'],identity_model.parameter_row_of,language_map,PARAMETER)
        except features.Refusal as error:
            if error.code!='NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED':raise
            modes=sorted({r['languageMode'] for r in accepted['requestedCapabilities'] if language_map.get(r['languageMode']) in ('typescript','rust')})
            raise native_model.AdmissionError(KEY+':'+','.join(modes)) from error
        return accepted
    return types.SimpleNamespace(admit_new_plan=admit,public_termination_for=ns['public_termination_for'],failure_envelope_errors=ns['failure_envelope_errors'])
