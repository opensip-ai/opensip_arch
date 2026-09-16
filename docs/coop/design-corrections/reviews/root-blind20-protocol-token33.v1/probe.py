"""Read inert AST literals only; execute the frozen reference, never consumer code."""
import ast,copy,hashlib,importlib.util,json,sys
from pathlib import Path
B=Path('/tmp/opensip-design-corrections')
OUT=Path(__file__).resolve().parent
SRC=B/'candidate-subject.v33'
P=B/'consumer-b.v20/output/lib/phase3_traces.py'
T=B/'consumer-b.v20/output/traces/complete.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
tree=ast.parse(P.read_text());names={}
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HELLO_ACK_FULL' for t in node.targets):
        names['HELLO_ACK_FULL']=ast.literal_eval(node.value)
def literal(n):
    if isinstance(n,ast.Name):return copy.deepcopy(names[n.id])
    if isinstance(n,ast.List):return [literal(x) for x in n.elts]
    if isinstance(n,ast.Tuple):return tuple(literal(x) for x in n.elts)
    return ast.literal_eval(n)
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
node=next(n for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='full' for t in n.targets))
events=[{'frame':x[0],**x[1]} if isinstance(x,tuple) else {'frame':x} for x in literal(node.value)]
claimed=next(x for x in json.loads(T.read_text()) if x['trace']=='complete')
assert [e['frame'] for e in events]==claimed['events']
model=SRC/'docs/coop/design-corrections/native/native_evidence_model.v2.py'
spec=importlib.util.spec_from_file_location('root_protocol33',model);M=importlib.util.module_from_spec(spec);sys.modules[spec.name]=M;spec.loader.exec_module(M)
actual=M.protocol3_run(events)
corrected=copy.deepcopy(events)
next(x for x in corrected if x['frame']=='HelloAck')['capabilities']=list(M.IDENTITY_TOKENS)
control=M.protocol3_run(corrected)
r={'standing':'Bounded protocol transition control on completed consumer20 source literals and exact retained event sequence. No consumer execution, no full payload-schema admission, no provider execution, not whole charter acceptance.',
   'sourceManifestSha256':'1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299',
   'inputs':{str(p):sha(p.read_bytes()) for p in [P,T,model]},'eventsExtractedFromConsumerAST':events,
   'consumerClaim':{k:claimed[k] for k in ['finalPhase','terminalKind','identityNegotiated','sourceBytesSent','stagesCompleted','ruleTrace']},
   'frozenReference':actual,'rootOnlyControlChangingHelloAckTokens':{'events':corrected,'result':control},
   'finding':'Consumer Machine requires snapshot2/plan2/fact2/coverage2/scope2 aliases, and full HelloAck carries those aliases plus view2. Native section9.1 requires four different exact capability tokens. The published transition refuses OpenUniverse with no source disclosure on the exact consumer input.',
   'firstDivergence':{'eventIndex':1,'frame':'HelloAck','field':'identityNegotiated','consumer':True,'owner':False},
   'firstRefusal':{'eventIndex':2,'frame':'OpenUniverse','rule':'P3-34','masksLater':'All later protocol phases become FAULT-absorb; later frame semantics not established.'},
   'rootControlScope':'Change ONLY HelloAck capability list to owning four exact tokens, selected reference completes. This is a root discriminating control, never an accepted consumer export.',
   'noNewDesignDefectDemonstrated':True}
assert actual['finalPhase']=='FAULT' and not actual['sourceBytesSent'] and control['finalPhase']=='DONE'
for p in [P,T]: (OUT/p.name).write_bytes(p.read_bytes())
(OUT/'assessment.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'actual':actual,'rootControl':control}))
