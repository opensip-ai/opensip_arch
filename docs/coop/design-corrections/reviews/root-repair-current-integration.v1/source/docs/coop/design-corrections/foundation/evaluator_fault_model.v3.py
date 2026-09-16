"""Typed evaluator boundary observations -> existing D9 routes.

Reference design, not a running host. The invoking host boundary supplies the
observation and origin; error-message parsing never establishes either one.
Detailed owner decisions remain in a retained diagnostic blob, not public codes.
"""
import copy, hashlib, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('fault_canonical',HERE/'canonical.py')
P=load('fault_workflows3',HERE.parent/'workflows/workflow_projection_model.v3.py')
SCHEMA=json.loads((HERE/'evaluator-fault-observation.schema.v3.json').read_text())
ROUTES=SCHEMA['x-opensip-routes']
EXIT={'success':0,'policy-failed':1,'request-rejected':2,'indeterminate':3,'operational-failed':4,'interrupted':130}

def route(observation,diagnostic_bytes):
    C.validate(SCHEMA,observation)
    if type(diagnostic_bytes) is not bytes or hashlib.sha256(diagnostic_bytes).hexdigest()!=observation['diagnosticDigest']:
        raise C.AdmissionError('EVALUATOR_FAULT_DIAGNOSTIC_CUSTODY')
    # Bytes are already an owner diagnostic artifact. This route preserves them
    # exactly and does not reclassify a nested native cause or arbitrary text.
    key=observation['condition']+':'+observation['origin']
    if key not in ROUTES:raise C.AdmissionError('EVALUATOR_FAULT_ORIGIN')
    row=ROUTES[key];term=copy.deepcopy(row['termination'])
    detail={'code':row['detail'],'remedy':row['remedy']}
    if observation['reference'] is not None:detail['subject']=observation['reference']
    if observation['condition'] in ('selection-limit-exceeded','output-bound-exceeded'):
        limit=observation['limit']
        if limit['observed']<=limit['maximum']:raise C.AdmissionError('EVALUATOR_FAULT_NOT_OVER_LIMIT')
        detail['subject']=str(limit['field'])+':'+str(limit['observed'])+'>'+str(limit['maximum'])
    term['domainDetail']=detail
    P.validate_profile('urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/StepTermination',term)
    return {'termination':term,'exitCode':EXIT[term['class']],
            'diagnosticDigest':observation['diagnosticDigest'],'diagnosticBytes':diagnostic_bytes,
            'observation':copy.deepcopy(observation)}

def owner_observation(exception, diagnostic_bytes):
    """Adapt a typed retained owner carrier, preserving its full termination.

    This interface requires the owner exception object. No exception text is
    parsed into a boundary or condition, and diagnostic bytes remain opaque.
    """
    term=getattr(exception,'termination',None)
    if not isinstance(term,dict):raise C.AdmissionError('EVALUATOR_FAULT_OWNER_CARRIER')
    detail=term.get('domainDetail',{})
    pair={'evidence.missing':('promised-bytes-lost','evidence-store'),
          'evidence.regeneration-mismatch':('complete-replay-mismatch','retained-regeneration')}.get(detail.get('code'))
    if pair is None:raise C.AdmissionError('EVALUATOR_FAULT_OWNER_CARRIER')
    observation={'schemaVersion':3,'condition':pair[0],'origin':pair[1],
                 'diagnosticDigest':hashlib.sha256(diagnostic_bytes).hexdigest(),
                 'reference':detail.get('subject'),'limit':None}
    actual=route(observation,diagnostic_bytes)
    if not C.equal_typed(actual['termination'],term):raise C.AdmissionError('EVALUATOR_FAULT_OWNER_CARRIER')
    return observation

def failure_envelope(observation,diagnostic_bytes,request_id):
    routed=route(observation,diagnostic_bytes)
    term=routed['termination']
    envelope={'schemaFamily':'opensip.product.envelope','schemaMajor':3,'kind':'failure',
              'requestId':request_id,'termination':term,'exitCode':routed['exitCode'],
              'errors':[copy.deepcopy(term['domainDetail'])]}
    validate_envelope(envelope,routed)
    return envelope

def validate_envelope(envelope,routed):
    P.validate_profile('urn:opensip:product-v1:workflows:evaluator3:command-envelope:3',envelope)
    if (envelope['kind']!='failure' or
        envelope['exitCode']!=EXIT[envelope['termination']['class']] or
        not C.equal_typed(envelope['termination'],routed['termination']) or
        not C.equal_typed(envelope['errors'],[routed['termination']['domainDetail']])):
        raise C.AdmissionError('EVALUATOR_FAULT_ENVELOPE_PARITY')
    return envelope
