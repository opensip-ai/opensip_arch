"""Policy result projection from a fully replayed retained Run, with reminted mutants."""
import copy,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('policy_run_fixture',HERE/'check-replay.v3.py')
F=importlib.util.module_from_spec(s);s.loader.exec_module(F)

def main():
    graph=F.positive();R=F.R;M=R.M;expected=R.derive_policy_result(*graph)
    assert R.admit_policy_result(expected,*graph)==expected['policyDerivationId']
    rows=[{'case':'actual-admitted-run-policy-derivation','result':'ADMIT','policyDerivationId':expected['policyDerivationId']}]
    for field,value in [('verdict','pass'),('policyDigest','1'*64),('waiverDigest','2'*64)]:
        bad=copy.deepcopy(expected);bad['descriptor'][field]=value
        bad['policyDerivationId']=M.identifier('policy-derivation',bad['descriptor'])
        try:R.admit_policy_result(bad,*graph)
        except Exception as exc:
            if str(exc)!='EVALUATOR_POLICY_DERIVATION_REPLAY':raise
            rows.append({'case':'reminted-'+field,'result':'REFUSE','reason':str(exc)})
        else:raise AssertionError(field)
    changed=F.positive(gate=False)
    changed_result=R.derive_policy_result(*changed)
    assert changed[0]['planId']!=graph[0]['planId']
    assert changed_result['descriptor']['policyDigest']!=expected['descriptor']['policyDigest']
    assert changed_result['descriptor']['verdict']=='pass'
    assert R.admit_policy_result(changed_result,*changed)==changed_result['policyDerivationId']
    rows.append({'case':'changed-policy-own-admitted-plan','result':'ADMIT','policyDerivationId':changed_result['policyDerivationId']})
    try:R.admit_policy_result(changed_result,*graph)
    except Exception as exc:
        if str(exc)!='EVALUATOR_POLICY_DERIVATION_REPLAY':raise
        rows.append({'case':'other-admitted-plan-cannot-replace-policy','result':'REFUSE','reason':str(exc)})
    else:raise AssertionError('changed policy accepted against original Run')
    report={'standing':'synthetic native-admitted Run and complete replay; no runtime qualification','passed':True,'count':len(rows),'checks':rows}
    print(json.dumps(report,indent=2));return report

if __name__=='__main__':main()
