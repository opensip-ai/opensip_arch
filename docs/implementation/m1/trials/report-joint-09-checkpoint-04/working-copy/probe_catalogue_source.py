from pathlib import Path
import copy,hashlib,json,types
HERE=Path(__file__).resolve().parent
p=HERE/'check_catalogue_joins.py';Q=types.ModuleType('q');Q.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),Q.__dict__)
def load(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
A=load('report_admission');M=load('models/report_model');FJ=load('fit_join');J=Q.J;V=Q.V
D=json.loads((HERE/'parent-bases.fixture.json').read_bytes())['audit-full'];selected,receipt=Q.receipt()
D['panels']['descriptions']={'state':'present','data':{'run':{'state':'present','data':{'runId':D['envelope']['run']['runId'],'planId':D['envelope']['run']['planId'],'selection':[selected],'receipts':[receipt]}},'recipe':{'state':'omitted','reason':'not-selected'},'provenance':copy.deepcopy(V.report['$defs']['DescriptionsPanelV1']['properties']['provenance']['const'])}}
D['disclosures']=J.disclosures(D['panels'],None,M,V.H,D['envelope']['run']['runId'],lambda v:V.validate(V.history_schema['$id'],v))
row=next(c for c in json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'))['commands'] if c['name']=='audit')
text=M.static_parity_text(D['envelope'],row,D['disclosures']).encode();D['staticParity']={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
assert receipt['capabilityAuthority']['registrySha256']!=D['panels']['catalog']['data']['capabilities']['data']['source']['registrySha256']
A.admit(M.canonical(D),V,M,J,Q.O.catalog,FJ.owner_summary(V.C))
print(json.dumps({'standing':'Root counterexample before correction; synthetic source dictionaries','contradictoryCapabilityRegistriesAccepted':True}))
