from pathlib import Path
import json,hashlib,copy,subprocess
F=Path(__file__).parent;B=F/'generator-profile-design-r1';S=B/'architecture'
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch'
PRE='docs/implementation/m3/native-publication/native-owner-generator-profile-r1'
assert not B.exists()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
L=json.loads((P/'design-lock.json').read_text());assert len(L['contractSuccessors'])==179
assert git(P,'status','--porcelain')=='' and git(A,'diff','--name-only','HEAD')==''
source_pre='docs/implementation/m3/native-publication/native-owner-patterns-source-r1'
owner_ids=['urn:opensip:product-v1:native:evidence-schemas:v2','opensip.product.occupancy-companion.1','opensip.product.relation-payload.2']
docs=[json.loads((A/source_pre/'sources/native-v2.schema.json').read_text()),json.loads((P/'schemas/sources/occupancy-v1.schema.json').read_text()),json.loads((A/source_pre/'sources/relation-payload-v2.schema.json').read_text())]
forms=set();nodes=[]
def scan(value,owner,path):
 if isinstance(value,dict):
  for k,v in value.items():
   if k=='pattern' and isinstance(v,str):forms.add(v);nodes.append(dict(owner=owner,pointer=path+'/'+k,pattern=v))
   else:scan(v,owner,path+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(value,list):
  for i,v in enumerate(value):scan(v,owner,path+'/'+str(i))
for doc in docs:assert doc['$id'] in owner_ids;scan(doc,doc['$id'],'#')
assert len(forms)==26 and len(nodes)==137
helper_paths=['tools/contracts/runtime/patterns.ts','tools/contracts/runtime/schema.ts']
base_patterns=(P/helper_paths[0]).read_text()
extra='''
// Fixed native-owner pattern keywords, selected by the resolved document ID.
// Property-name patterns and every other document retain the inherited table.
const nativeOwnerDocuments = new Set<string>(OWNER_IDS);
const nativeOwnerPatterns = new Set<string>(NATIVE_FORMS);
export const selectedKeywordPattern = (pattern: string, owner: string): string | undefined =>
  nativeOwnerDocuments.has(owner) ? (nativeOwnerPatterns.has(pattern) ? pattern : undefined) : selectedPattern(pattern);
'''.replace('OWNER_IDS',json.dumps(owner_ids,indent=2)).replace('NATIVE_FORMS',json.dumps(sorted(forms),indent=2))
out=S/PRE/'product'/helper_paths[0];out.parent.mkdir(parents=True,exist_ok=True);out.write_text(base_patterns+extra)
schema=(P/helper_paths[1]).read_text()
assert schema.count('import { selectedPattern }')==1
schema=schema.replace('import { selectedPattern }','import { selectedPattern, selectedKeywordPattern }')
old='''  private regex(pattern: string): RegExp {
    let result = this.patterns.get(pattern);
    if (!result) {
      const translated = selectedPattern(pattern);
      if (translated === undefined) throw new SchemaError("pattern outside selected profile");
      result = new RegExp(translated, "u"); this.patterns.set(pattern, result);
    }
    return result;
  }'''
new='''  private regex(pattern: string, owner?: string): RegExp {
    const translated = owner === undefined ? selectedPattern(pattern) : selectedKeywordPattern(pattern, owner);
    if (translated === undefined) throw new SchemaError("pattern outside selected profile");
    // Cache by admitted expression: the same raw literal can have different
    // native and inherited interpretations. Admission always precedes lookup.
    let result = this.patterns.get(translated);
    if (!result) {
      result = new RegExp(translated, "u"); this.patterns.set(translated, result);
    }
    return result;
  }'''
assert schema.count(old)==1;schema=schema.replace(old,new)
assert schema.count('if (key === "pattern") this.regex(value as string);')==1
schema=schema.replace('if (key === "pattern") this.regex(value as string);','if (key === "pattern") this.regex(value as string, owner);')
assert schema.count('!this.regex(schema.pattern).test(item)')==1
schema=schema.replace('!this.regex(schema.pattern).test(item)','!this.regex(schema.pattern, owner).test(item)')
(S/PRE/'product'/helper_paths[1]).write_text(schema)
closure=json.loads((A/source_pre/'product/tools/contracts/generator-closure.json').read_text());before=copy.deepcopy(closure)
for row in closure['files']:
 if row['path'] in helper_paths:
  assert pin(P,row['path'])==row
  newpin=pin(S,PRE+'/product/'+row['path']);row.update(bytes=newpin['bytes'],sha256=newpin['sha256'])
closure_path=PRE+'/product/tools/contracts/generator-closure.json';write(S/closure_path,closure)
assert [a['path'] for a,b in zip(before['files'],closure['files']) if a!=b]==helper_paths
registry=json.loads((A/source_pre/'product/schemas/registry.json').read_text());registry['recipes'][0]['generatorClosureSha256']=pin(S,closure_path)['sha256']
write(S/(PRE+'/product/schemas/registry.json'),registry)
write(B/'profile-nodes.json',dict(owners=owner_ids,forms=sorted(forms),nodes=nodes))
write(B/'prepared-initial.json',dict(stage=str(S),prefix=PRE,productBase=git(P,'rev-parse','HEAD'),architectureBase=git(A,'rev-parse','HEAD'),helperPaths=helper_paths,prospectiveContractSuccessor=180))
print(json.dumps(dict(stage=str(S),forms=len(forms),nodes=len(nodes),helperPaths=helper_paths),indent=2))
