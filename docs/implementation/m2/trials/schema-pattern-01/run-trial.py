from pathlib import Path
import json,hashlib,subprocess,itertools,re
A=Path('/Users/sb/code/opensip-ai/opensip_arch'); P=A.parent/'opensip'; B=Path('/tmp/opensip-implementation/m2-schema-pattern-trial-01'); assert not B.exists(); B.mkdir(); H=B/'probe'; (H/'src').mkdir(parents=True)
registry=json.loads((P/'schemas/registry.json').read_bytes()); patterns={}; sourcepins=[]
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def walk(v,source,path=''):
 if not isinstance(v,dict):return
 if 'pattern' in v:patterns.setdefault(v['pattern'],[]).append({'source':source,'pointer':path+'/pattern'})
 for key in ['$defs','definitions','properties','patternProperties','dependentSchemas']:
  for name,x in v.get(key,{}).items():walk(x,source,path+'/'+key+'/'+name.replace('~','~0').replace('/','~1'))
 for key in ['items','contains','additionalProperties','unevaluatedProperties','propertyNames','not','if','then','else']:
  if key in v:walk(v[key],source,path+'/'+key)
 for key in ['allOf','anyOf','oneOf','prefixItems']:
  for i,x in enumerate(v.get(key,[])):walk(x,source,path+'/'+key+'/'+str(i))
for row in registry['sources']:
 raw=(P/row['sourcePath']).read_bytes(); assert hashlib.sha256(raw).hexdigest()==row['sourceSha256']; sourcepins.append({'path':row['sourcePath'],**dig(raw)});walk(json.loads(raw),row['sourcePath'])
(B/'pattern-census.json').write_text(json.dumps({'sources':sourcepins,'patterns':[{'pattern':p,'occurrences':x} for p,x in sorted(patterns.items())]},indent=2)+'\n')
(H/'Cargo.toml').write_text('[workspace]\n[package]\nname="opensip-schema-pattern-trial"\nversion="0.0.0"\nedition="2024"\npublish=false\n[dependencies]\nopensip-identity={path="/Users/sb/code/opensip-ai/opensip/crates/identity"}\nregress={version="=0.12.0",default-features=false,features=["std","prohibit-unsafe"]}\n')
(H/'src/main.rs').write_text('''use std::{collections::BTreeMap, io::{self, BufRead}};
use opensip_identity::{parse_json, JsonValue};
fn main() -> Result<(), Box<dyn std::error::Error>> {
 let mut cache = BTreeMap::new();
 for line in io::stdin().lock().lines() {
  let line=line?; let JsonValue::Object(row)=parse_json(line.as_bytes())? else {return Err("object".into());};
  let (JsonValue::String(pattern),JsonValue::String(text))=(&row["pattern"],&row["text"]) else {return Err("strings".into());};
  if !cache.contains_key(pattern) {cache.insert(pattern.clone(),regress::Regex::with_flags(pattern,"u"));}
  match &cache[pattern] {Ok(re)=>println!("{}",u8::from(re.find(text).is_some())),Err(_)=>println!("E")}
 }
 Ok(())
}
''')
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';r=subprocess.run([cargo,'build','--offline','--manifest-path',str(H/'Cargo.toml')],capture_output=True,timeout=300); (B/'build.stdout').write_bytes(r.stdout); (B/'build.stderr').write_bytes(r.stderr); assert r.returncode==0,r.stderr.decode()
alphabet=['a','A','0','-','.', '/', '\\','\n','\r','\x00','é','😀']; values={''.join(xs) for n in range(3) for xs in itertools.product(alphabet,repeat=n)}
values.update(['src/lib.rs','a/../b','a//b','a/..\n','a/.\r\n','.\u2028','.\u2029','a\u0085b','1.2.3','1.2.3-rc.1+build.01','01.2.3','1.2.3-01','true','false','rule.name','req1_'+'0'*32])
for n in [0,1,2,39,40,41,63,64,65,255,256]:values.add('a'*n)
for prefix in ['sha256','closure2','plan2','run3','snapshot2','import2','fact2','finding3','scope2','owner1','subject3','coverage2','view2','proof3','seal3','evidence3','exec-plan2']:
 for suffix in ['', '\n','\r','\r\n','\u2028','\u2029','x']:values.add(prefix+':'+'a'*64+suffix)
for n in range(160):
 for form in ['{}','a{}b','a/{}','a/.{}']:values.add(form.format(chr(n)))
values=sorted(values); cases=[{'pattern':p,'text':v} for p in sorted(patterns) for v in values]; expected=[bool(re.search(c['pattern'],c['text'])) for c in cases]
raw=''.join(json.dumps(c,ensure_ascii=True,separators=(',',':'))+'\n' for c in cases).encode();(B/'cases.jsonl').write_bytes(raw)
r=subprocess.run([str(H/'target/debug/opensip-schema-pattern-trial')],input=raw,capture_output=True,timeout=180);(B/'probe.stdout').write_bytes(r.stdout);(B/'probe.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr.decode();actual=r.stdout.splitlines();assert len(actual)==len(cases)
mis=[{**c,'pythonReference':e,'regressUnicode':a.decode()} for c,e,a in zip(cases,expected,actual) if a==b'E' or (a==b'1')!=e]
result={'standing':'Exploratory dependency trial only. No runtime validator selection or product dependency/code changes. Comparison to selected Python reference semantics; not full JSON-schema/performance proof.','candidate':'regress0.12.0,default-features=false,std+prohibit-unsafe; unicode flag','schemaSources':len(sourcepins),'patterns':len(patterns),'cases':len(cases),'mismatches':len(mis),'mismatchPatterns':sorted({m['pattern'] for m in mis}),'compileErrorCases':sum(a==b'E' for a in actual),'productChanged':False}
(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');(B/'mismatches.json').write_text(json.dumps(mis,indent=2)+'\n'); print(json.dumps(result,indent=2))
