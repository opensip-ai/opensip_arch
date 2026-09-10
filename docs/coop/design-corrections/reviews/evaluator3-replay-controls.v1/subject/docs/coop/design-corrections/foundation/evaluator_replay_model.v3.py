"""Complete retained-output replay for the explicit evaluator3 profile.

First calls inherited native/schema/identity closure admission, then independently
reconstructs enumeration and scans native/imported inputs. Claimed findings, witnesses,
parameters and verdicts never feed reconstruction. This reference does not execute tools,
compilers or providers. Synthetic admitted inputs do not qualify real extraction.
"""
import copy,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
I=load('replay_inputs3',HERE/'evaluator_input_model.v3.py');E=I.E;M=E.M;C=M.C
A=load('replay_atom1',HERE/'atom_model.v1.py')

def scanner(normalized,atom_inputs):
    """Adapt actual atom results to typed proof witnesses; no caller-supplied truth values."""
    def scan(rule,subject,node,pid):
        desc={'universe':subject['universe'],'kind':subject['kind'],'nativeSubjectId':subject['row']['nativeSubjectId']}
        if subject['kind']=='package':desc['packageManifestPath']=subject['row']['path']
        result=A.evaluate_atom(node,desc,atom_inputs)
        # Every atom binds the complete admitted input selection, including absence inputs.
        # This deliberately avoids identifying only known hits and losing empty populations.
        refs=normalized['evaluationInputRefs'];defs=[]
        plane='import' if result['kind']=='imported-atom' else 'native'
        def record(code,native_cause=None,universe=None):
            return {'source':plane,'cause':code,'subjectId':subject['subjectId'],'predicateId':pid,
                'inputRefs':E.cset(refs),'evidenceKind':node.get('evidence') if plane=='import' else None,
                'nativeCause':native_cause,'universe':universe}
        for cause in result['causes']:
            if cause['code'] in M.SCHEMA['x-opensip-evaluator-deficiency-registry']['nonBlockingDisclosures']:continue
            if cause['code'] not in M.SCHEMA['x-opensip-evaluator-deficiency-registry']['sources'][plane]:raise C.AdmissionError('EVALUATOR_ATOM_CAUSE_UNREGISTERED:'+cause['code'])
            defs.append(record(cause['code'],native_cause=cause.get('nativeCause'),universe=cause.get('universe')))
        for deficiency in result['nativeDeficiencies']:
            defs.append(record(deficiency))
        for cid in result['coverageIds']:
            entry=atom_inputs['coverages'][cid]['entry']
            if entry['deficiency'] is not None:
                d=record(entry['deficiency'],entry['nativeCause'],atom_inputs['coverages'][cid]['key']['sourceUniverse'])
                d['inputRefs']=[{'domain':'coverage','digest':cid.split(':',1)[1]}];defs.append(d)
        return {'kind':result['kind'],'value':result['value'],'matchingFactIds':result['knownFactIds'],
            'uncertainFactIds':result['uncertainFactIds'],'matchingImportRows':result['knownObservationAddresses'],
            'uncertainImportRows':result['uncertainObservationAddresses'],'coverageIds':result['coverageIds'],
            'scopeIds':result['scopeIds'],'inputRefs':E.cset(refs),'deficiencies':E.cset(defs)}
    return scan

def derive(plan_id,execution_id,evaluator_closure,input_refs,objects,blobs,owner):
    normalized,atom_inputs=I.reconstruct(plan_id,execution_id,evaluator_closure,input_refs,objects,blobs,owner,M)
    A.admit_atom_inputs(atom_inputs)
    result=E.compose(normalized,scanner(normalized,atom_inputs))
    result['normalizedInputs']=normalized
    return result

def replay(run,objects,blobs):
    run_id,owner=M.open_run_closure(run,objects,blobs)
    seal=objects[run['evaluationSealId']][1];proof=objects[seal['proofBundleId']][1]
    result=derive(run['planId'],seal['executionPlanId'],seal['evaluatorClosure'],proof['evaluationInputRefs'],objects,blobs,owner)
    E.compare_complete_replay(proof,result,objects,blobs)
    if result['proofBundleId']!=seal['proofBundleId']:raise C.AdmissionError('EVALUATOR_PROOF_ID_REPLAY')
    evidence=objects[run['evidenceId']][1]
    expected_views=E.cset('view2:'+r['digest'] for r in proof['evaluationInputRefs'] if r['domain']=='view')
    expected_coverages=E.cset([c for v in expected_views for c in objects[v][1]['coverageIds']]+['coverage2:'+r['digest'] for r in proof['evaluationInputRefs'] if r['domain']=='coverage'])
    expected_evidence={'schemaVersion':3,'planId':run['planId'],'viewIds':expected_views,'coverageIds':expected_coverages,
        'importIds':owner['plan']['importIds'],'findingIds':result['proof']['findingIds'],'proofBundleId':result['proofBundleId']}
    E.require_equal(evidence,expected_evidence,'EVALUATOR_EVIDENCE_REPLAY')
    expected_eid=M.identifier('semantic-evidence',expected_evidence)
    expected_seal={'schemaVersion':3,'planId':run['planId'],'executionPlanId':seal['executionPlanId'],'evidenceId':expected_eid,
        'evaluatorClosure':seal['evaluatorClosure'],'policyDigest':owner['plan']['policyDigest'],
        'proofBundleId':result['proofBundleId'],'verdict':result['proof']['verdict']}
    E.require_equal(seal,expected_seal,'EVALUATOR_SEAL_REPLAY')
    expected_run={'schemaVersion':3,'projectId':owner['snapshot']['projectId'],'snapshotId':owner['plan']['snapshotId'],
        'planId':run['planId'],'evidenceId':expected_eid,'evaluationSealId':M.identifier('evaluation-seal',expected_seal),
        'capabilityManifestId':owner['plan']['capabilityManifestId']}
    E.require_equal(run,expected_run,'EVALUATOR_RUN_REPLAY')
    return {'result':'ADMIT','runId':run_id,'proofBundleId':result['proofBundleId'],'findingCount':len(result['proof']['findingIds']),
        'predicateCount':len(result['proof']['predicateProofs']),'verdict':result['proof']['verdict'],'workUnits':result['workUnits']}
