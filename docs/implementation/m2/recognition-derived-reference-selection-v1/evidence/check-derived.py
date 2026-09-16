from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--architecture',required=True,type=Path);p.add_argument('--output',type=Path);a=p.parse_args();A=a.architecture;U=Path(__file__).resolve().parent.parent
old=A/'docs/implementation/m1/source-selection-v2/reference/models/identity_model.proposed.v3.py';new=U/'reference/identity_model.py'
cp=A/'docs/implementation/m2/exact-schema-profile-selection-v1/reference/canonical.py'
sp=importlib.util.spec_from_file_location('recognition_exact',cp);C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
S=json.loads((A/'docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json').read_bytes())
F=json.loads((A/'docs/implementation/m1/source-selection-v2/schemas/sources/framework-recognition-plan.v1.schema.json').read_bytes())
ot=ast.parse(old.read_text());nt=ast.parse(new.read_text())
def branch(t):
 run=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='open_run_closure')
 digest=next(n for n in run.body if isinstance(n,ast.FunctionDef) and n.name=='digest_field')
 h=next(n for n in digest.body if isinstance(n,ast.If) and ast.unparse(n.test)=="representation == 'h-identity'")
 return digest,h
removed=copy.deepcopy(nt);_,h=branch(removed);assert ast.unparse(h.body[0].test)=="annotation.get('domain') == 'native.framework-recognition.v1'";h.body.pop(0)
assert ast.dump(removed,include_attributes=False)==ast.dump(ot,include_attributes=False)
checks=['only-one-recognition-branch-AST-delta']
prefix=next(n for n in ot.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREFIX' for t in n.targets))
def binding(tree):
 calls=[];caps=set();ns={'C':C,'DIGESTS':S['x-opensip-digest-domains'],'visit':lambda *x:calls.append(('visit',x)),'admit_frame':lambda *x:calls.append(('frame',x)),'capability_ids':caps}
 exec(compile(ast.Module(body=[prefix,branch(tree)[0]],type_ignores=[]),'pinned-identity-digest-branch','exec'),ns);return ns,calls,caps
before,_,_=binding(ot);after,calls,caps=binding(nt)
recognition={'schemaVersion':1,'recognized':[],'observedHints':[],'entryPoints':{'state':'all','source':'explicit'}}
value={'markerPath':'','rootPath':'','unitOrdinal':0,'recognition':recognition,'recognitionId':'sha256:'+C.identity('native.framework-recognition.v1',recognition)}
C.ExactValidator({'$ref':F['$id']+'#/$defs/UnitRecognitionV1'},registry=C.exact_registry([F])).validate(value);checks.append('correct-inline-row-selected-schema-valid')
ann=F['$defs']['UnitRecognitionV1']['properties']['recognitionId']['x-opensip-digest']
try:before['digest_field'](ann,value['recognitionId'],value)
except KeyError as e:assert e.args==('native.framework-recognition.v1',);checks.append('predecessor-keyerror-reproduced')
else:raise AssertionError('predecessor unexpectedly accepted')
after['digest_field'](ann,value['recognitionId'],value);assert not calls;checks.append('correct-inline-no-core-or-frame-lookup')
def refuses(label,annotation,text,siblings):
 try:after['digest_field'](annotation,text,siblings)
 except C.AdmissionError:checks.append(label)
 else:raise AssertionError(label)
refuses('incorrect-inline-id',ann,'sha256:'+'0'*64,value)
changed=copy.deepcopy(value);changed['recognition']['entryPoints']={'state':'all','source':'recognized'}
refuses('changed-inline-preimage',ann,value['recognitionId'],changed)
refuses('absent-inline-preimage',ann,value['recognitionId'],{})
refuses('nonobject-siblings',ann,value['recognitionId'],None)
refuses('wrong-declared-form',dict(ann,form='bare-hex'),value['recognitionId'],value)
refuses('wrong-preimage-retention',dict(ann,retention='preimage'),value['recognitionId'],value)
after['digest_field']({'representation':'h-identity','domain':'fact'},'0'*64,{})
assert calls.pop()==('visit',('fact2:'+'0'*64,'fact'));checks.append('core-h-dispatch-unchanged')
after['digest_field']({'representation':'h-identity','domainSet':'native-context'},'0'*64,{})
assert calls.pop()==('frame',('0'*64,'native-context'));checks.append('frame-dispatch-unchanged')
after['digest_field']({'representation':'capability-manifest-id','retention':'derived'},'0'*64,{})
assert caps=={'0'*64};checks.append('capability-derived-dispatch-unchanged')
out={'checks':checks,'count':len(checks),'passed':True,'fullCompilerRunTested':False,'completeReplayTested':False,'sourcePins':[{'path':str(x),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in [old,new,cp]]}
if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
