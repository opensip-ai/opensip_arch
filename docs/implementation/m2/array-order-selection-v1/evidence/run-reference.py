from pathlib import Path
import json,itertools,subprocess,hashlib,importlib.util,random
A=Path('/Users/sb/code/opensip-ai/opensip_arch'); B=Path('/tmp/opensip-implementation/m2-array-order-candidate-01'); P=B/'product'; H=B/'probe'; (H/'src').mkdir(parents=True)
reference=A/'docs/coop/design-corrections/foundation/canonical.py'; raw=reference.read_bytes(); pin={'path':str(reference.relative_to(A)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
lock=json.loads((P/'design-lock.json').read_bytes()); subject=json.loads((A/lock['approvals']['sourceManifest']['path']).read_bytes()); rows=subject.get('files',subject.get('entries',[])); matches=[r for r in rows if r.get('path')==pin['path']]; assert len(matches)==1 and matches[0]['sha256']==pin['sha256'],matches
spec=importlib.util.spec_from_file_location('exact_reference',reference); C=importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
(H/'Cargo.toml').write_text('[workspace]\n[package]\nname="opensip-array-order-probe"\nversion="0.0.0"\nedition="2024"\npublish=false\n[dependencies]\nopensip-identity={path="../product/crates/identity"}\n')
(H/'src/main.rs').write_text('''use std::io::{self, BufRead};
use opensip_identity::{parse_json, canonical_bytes, JsonValue, ArrayOrder};
fn main() -> Result<(), Box<dyn std::error::Error>> {
 for line in io::stdin().lock().lines() {
  let line = line?;
  let value = parse_json(line.as_bytes())?;
  let JsonValue::Object(object) = &value else {return Err("expected object".into());};
  let JsonValue::Array(values) = &object["values"] else {return Err("expected array".into());};
  let before = canonical_bytes(&value)?;
  let good = ArrayOrder::parse(&object["order"]).and_then(|order| order.verify(values)).is_ok();
  assert_eq!(canonical_bytes(&value)?, before);
  println!("{}", u8::from(good));
 }
 Ok(())
}
''')
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'; commands=[]
def run(name,cmd,cwd=P,stdin=None):
 r=subprocess.run(cmd,cwd=cwd,input=stdin,capture_output=True,timeout=300); (B/(name+'.stdout')).write_bytes(r.stdout); (B/(name+'.stderr')).write_bytes(r.stderr); commands.append({'name':name,'command':cmd,'exitCode':r.returncode}); (B/'commands.json').write_text(json.dumps(commands,indent=2)+'\n'); assert r.returncode==0,r.stderr.decode(); return r
run('identity-tests',[cargo,'test','--locked','--offline','-p','opensip-identity','--all-targets']); run('identity-clippy',[cargo,'clippy','--locked','--offline','-p','opensip-identity','--all-targets','--','-D','warnings']); run('fmt',[cargo,'fmt','--all','--check']); run('oracle-build',[cargo,'build','--offline','--manifest-path',str(H/'Cargo.toml')])
orders=['sequence','utf8','canonical-set','canonical-order','numeric','ordinal','candidateOrdinal','path','ruleId','waiverId','predicate',{'by':['name']},{'by':['name','version']},'unregistered',None,True,1,[],{}, {'by':[]},{'by':['']},{'by':['name','name']},{'by':['name'],'extra':True},{'by':'name'},{'by':[1]}]
# Include the actual annotation population from all selected product schema inputs.
annotations={}
def walk(v,source,path=''):
 if isinstance(v,dict):
  if 'x-opensip-order' in v:
   order=v['x-opensip-order']; key=json.dumps(order,sort_keys=True); annotations.setdefault(key,{'order':order,'occurrences':[]})['occurrences'].append({'source':source,'pointer':path})
  for k,x in v.items(): walk(x,source,path+'/'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v): walk(x,source,path+'/'+str(i))
for p in sorted((P/'schemas/sources').glob('*.json')): walk(json.loads(p.read_bytes()),str(p.relative_to(P)))
orders += [v['order'] for v in annotations.values()]
(B/'selected-order-census.json').write_text(json.dumps(list(annotations.values()),indent=2)+'\n')
values=[]; scalar=[None,False,True,-(2**63),-1,0,1,2,10,2**53,2**53+1,2**64-1,'','\n','!','a','é','e\u0301','😀']
values.extend(list(xs) for n in range(3) for xs in itertools.product(scalar,repeat=n))
records=[{}, {'name':'a'},{'name':'a','payload':1},{'name':'a','payload':2},{'name':'b'},{'name':1},{'name':'a','version':'1'},{'name':'a','version':'2'},{'path':'a'},{'path':'b'},{'ruleId':'a'},{'waiverId':'a'}, {'ruleId':'r','subjectId':'s','predicateId':'a'},{'ruleId':'r','subjectId':'s','predicateId':'b'}]
for field in ['ordinal','candidateOrdinal']:
 records += [{field:n} for n in [-2,-1,0,1,2,4,7,2**53,2**53+1,2**64-1,True,'0']]
values.extend(list(xs) for n in range(1,3) for xs in itertools.product(records,repeat=n))
rng=random.Random(20260915)
values += [rng.choices(scalar+records,k=rng.randrange(3,8)) for _ in range(100)]
cases=[{'order':order,'values':value} for order in orders for value in values]
expected=[]
for case in cases:
 C.typed(case['values']); expected.append(not list(C.exact_order(None,case['order'],case['values'],{})))
inputs=''.join(json.dumps(c,ensure_ascii=True,separators=(',',':'))+'\n' for c in cases).encode(); (B/'oracle-input.jsonl').write_bytes(inputs)
r=run('oracle',[str(H/'target/debug/opensip-array-order-probe')],stdin=inputs); actual=[line==b'1' for line in r.stdout.splitlines()]; assert len(actual)==len(expected)
mismatches=[{'case':case,'reference':e,'rust':a} for case,e,a in zip(cases,expected,actual) if e!=a]
(B/'oracle-result.json').write_text(json.dumps({'standing':'Exact selected reference order-law comparison on finite corpus; not whole schema or semantic replay','reference':pin,'selectedSchemaAnnotationForms':len(annotations),'selectedSchemaAnnotationOccurrences':sum(len(a['occurrences']) for a in annotations.values()),'cases':len(cases),'mismatches':mismatches,'rootIdentityTests':25,'noInputMutation':True},indent=2)+'\n'); assert not mismatches,mismatches[:5]; print('Matched',len(cases),'cases;',len(annotations),'selected forms')
