from pathlib import Path
import json,shutil,struct
F=Path(__file__).parent;D=F/'ecma-full-differential-r3';assert not D.exists();D.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip'
inputs=json.loads((F/'ecma-scope-differential-r2/inputs.json').read_text());forms=inputs['forms']
a64='a'*64;a40='a'*40
seeds=[
 [a64],['sha256:'+a64],['snapshot2:'+a64],['closure2:'+a64],['import2:'+a64],
 ['src/a','a//b','a/..\n'],['src/a'],['','src/a'],['a-z.b:c_d'],
 ['DISCLOSURE-ONLY','ENFORCED-BY-CONSTRUCTION','ENFORCED-AT-HOST-BROKER','ENFORCED-PLATFORM:a','ENFORCED-PLATFORM:'+'a'*64],
 [a40],['prj1-'+a64],['security.repo-execution-grants.v2:'+a64],
 ['2026-10-20','9999-99-99'],['2026-10-20T00:00:00Z','9999-99-99T99:99:99Z'],
 [a40,a64],['','src/a'],
 ['DIRECTORY_CUSTODY:OWNER','MARKER_CUSTODY:Cargo.toml:OWNER','MARKER_CUSTODY:package.json:OWNER','MARKER_CUSTODY:tsconfig.json:OWNER','MARKER_CUSTODY:jsconfig.json:OWNER','DEPTH'],
 ['scope2:'+a64],['coverage2:'+a64],['A-a_0.b'],['a','😀'],['a:a','abc-0:😀value'],['','😀'],
 ['a','a/b','a'*255,'a'*255+'/'+'b'*255],['.','..','a/../b'],
]
assert len(seeds)==len(forms)==26
values=[];seen=set()
def add(s):
 if s not in seen:seen.add(s);values.append(s)
add('');level=['']
for _ in range(5):
 level=[s+c for s in level for c in inputs['alphabet']]
 for s in level:add(s)
mutations=['a','A','0','f','F','.', '/', '\\', ':','-', '_','\0','\x01','\x1f','\x7f','\x80','\x9f','\xa0','\n','\r','\u2028','\u2029','\u200b','\u200c','\u200d','😀','\U0010ffff']
for group in seeds:
 for s in group:
  add(s)
  for c in mutations:add(c+s);add(s+c)
  for i in range(len(s)):
   add(s[:i]+s[i+1:])
   for c in mutations:add(s[:i]+c+s[i+1:])
for n in [39,40,41,63,64,65,254,255,256,4095,4096,4097]:
 for c in ['a','0','😀','.']:add(c*n)
grant_cases=[]
for first in ['.','x','😀','\0','\n','\r','\u2028','\u2029']:
 for second in ['.','x','😀','\0','\n','\r','\u2028','\u2029']:
  s=f'security{first}repo-execution-grants{second}v2:{a64}';add(s)
  grant_cases.append(dict(value=s,expected=first not in '\n\r\u2028\u2029' and second not in '\n\r\u2028\u2029'))
(D/'inputs.json').write_text(json.dumps(dict(rows=inputs['rows'],forms=forms,validSeedsByForm=seeds,values=values,grantWildcardCases=grant_cases,exhaustiveShortInputCount=66430),ensure_ascii=False,separators=(',',':'))+'\n')
with (D/'corpus.bin').open('wb') as out:
 for value in values:
  raw=value.encode('utf8');out.write(struct.pack('<I',len(raw)));out.write(raw)
shutil.copyfile(W/'crates/identity/src/schema_patterns.rs',D/'candidate.rs')
(D/'original.rs').write_text((P/'crates/identity/src/schema_patterns.rs').read_text()+"\npub fn selected_patterns() -> Vec<&'static str> { TABLE.iter().map(|r|r.0).collect() }\n")
def raw(s):assert '"##' not in s;return 'r##"'+s+'"##'
(D/'main.rs').write_text('''#[path="original.rs"] mod original;
#[path="candidate.rs"] mod candidate;
fn main() {
 let forms: &[&str] = &['''+','.join(raw(p) for p in forms)+'''];
 let bytes=std::fs::read(std::env::args().nth(1).unwrap()).unwrap();
 let mut at=0usize;let mut values=Vec::new();
 while at<bytes.len() { let n=u32::from_le_bytes(bytes[at..at+4].try_into().unwrap()) as usize;at+=4;values.push(std::str::from_utf8(&bytes[at..at+n]).unwrap());at+=n; }
 let mut checked=0usize;
 for pattern in original::selected_patterns() {for value in &values {assert_eq!(original::matches(pattern,value),candidate::matches(pattern,value),"legacy changed {pattern:?} {value:?}");checked+=1;}}
 let mut matrix=Vec::new();for pattern in forms {for value in &values {matrix.push(match candidate::matches_native_owner(pattern,value){Ok(false)=>0,Ok(true)=>1,Err(_)=>2});}}
 std::fs::write(std::env::args().nth(2).unwrap(),matrix).unwrap();
 println!("old_forms=72 inputs={} legacy_comparisons={checked}",values.len());
}
''')
(D/'reference.cjs').write_text('''const fs=require('fs');
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const matrix=fs.readFileSync(process.argv[3]);if(matrix.length!==d.forms.length*d.values.length)throw Error('matrix length');
let mismatchCount=0;const mismatches=[];let witnessed=0;
d.forms.forEach((p,pi)=>{const re=new RegExp(p,'u');if(!d.validSeedsByForm[pi].length)throw Error('missing full-form witness');for(const s of d.validSeedsByForm[pi]){if(!re.test(s))throw Error('invalid witness '+pi+' '+JSON.stringify(s));witnessed++;}let count=0;const examples=[];d.values.forEach((s,i)=>{const expected=re.test(s)?1:0;const got=matrix[pi*d.values.length+i];if(got!==expected){count++;mismatchCount++;if(examples.length<8)examples.push({value:s,expected:!!expected,actual:got===2?'unselected':!!got});}});if(count)mismatches.push({pattern:p,count,examples});});
const grantIndex=d.forms.findIndex(p=>p.startsWith('^security.'));const grant=new RegExp(d.forms[grantIndex],'u');for(const c of d.grantWildcardCases){if(grant.test(c.value)!==c.expected)throw Error('grant oracle');}
process.stdout.write(JSON.stringify({standing:'FINITE FULL-LENGTH AND SHORT PREDICATE DIFFERENTIAL; NOT REGISTERED UNIT ACCEPTANCE',engine:process.version,flags:'u',forms:d.forms.length,inputs:d.values.length,shortExhaustiveInputs:d.exhaustiveShortInputCount,fullLengthSeedForms:d.validSeedsByForm.length,validFullLengthWitnesses:witnessed,twoPositionGrantCases:d.grantWildcardCases.length,profileComparisons:matrix.length,inheritedForms:72,inheritedComparisons:72*d.values.length,mismatchCount,mismatches},null,2)+'\\n');
if(mismatchCount)process.exitCode=1;
''')
(D/'run.py').write_text("from pathlib import Path\nimport subprocess,os,json,hashlib\nassert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'\nd=Path(__file__).parent\nr=subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-O',str(d/'main.rs'),'-o',str(d/'probe')],capture_output=True);(d/'compile.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0\nr=subprocess.run([str(d/'probe'),str(d/'corpus.bin'),str(d/'matrix.bin')],capture_output=True);(d/'rust.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr\nr=subprocess.run(['/tmp/opensip-implementation/d2b0b-materialization-r1/generation-r1/tool-node',str(d/'reference.cjs'),str(d/'inputs.json'),str(d/'matrix.bin')],capture_output=True);(d/'reference.stderr').write_bytes(r.stderr);(d/'report.json').write_bytes(r.stdout);assert r.returncode==0,(r.stdout[-4000:],r.stderr)\nx=json.loads(r.stdout);print(json.dumps({k:v for k,v in x.items() if k!='mismatches'},indent=2))\n")
print('Prepared',len(values),'inputs, valid witnesses for all26forms,64grant cases and per-position mutations plus exhaustive short corpus.')
