from pathlib import Path
import json
base=Path.cwd()/'docs/coop/design-corrections'
files=[base/'native/native-evidence.schemas.v2.json',base/'security/security-lifecycle.schemas.v1.json',base/'foundation/product-configuration.schema.v2.json',*sorted((base/'workflows/schemas').glob('*.json'))]
changed=[]
def annotate(node,path,rows):
    if isinstance(node,dict):
        t=node.get('type')
        if t=='array' or isinstance(t,list) and 'array' in t:
            node.setdefault('x-opensip-order','sequence');rows.append(path)
        for k,v in node.items():annotate(v,path+'/'+k,rows)
    elif isinstance(node,list):
        for i,v in enumerate(node):annotate(v,path+'/'+str(i),rows)
def at(d,pointer):
    for part in pointer.strip('/').split('/'):d=d[int(part)] if isinstance(d,list) else d[part]
    return d
overrides={
'native/native-evidence.schemas.v2.json':{
 '/$defs/ResolutionCompletenessV2/properties/unresolvedEdgeClasses':'utf8',
 '/$defs/ViewEntryV3/properties/derivationKinds':'utf8',
 '/$defs/DependencyFileManifestV1':'path',
 '/$defs/DependencySourceSetV1/properties/packages':{'by':['name','version','sourceId']},
 '/$defs/RustUniverseV2ResolvedInputs/properties/crateRootPaths':'utf8',
 '/$defs/AuthorizedExecutionV2/properties/owners':{'by':['ownerKey']},
 '/$defs/TypeScriptToolchainIdentityV1/properties/standardLibraryComponentDigests':{'by':['component']},
 '/$defs/TypeScriptToolchainIdentityV1/properties/libSelection':'utf8',
 '/$defs/TypeScriptConfigProjectionV2/properties/configGraphPaths':'utf8',
},
'security/security-lifecycle.schemas.v1.json':{
 '/$defs/NamespaceList':'utf8',
 '/schemas/RepoExecutionGrantV2/properties/owners':{'by':['ownerKey']},
 '/schemas/PublicDetailProjectionV1/properties/codes':'utf8',
 '/schemas/PublicDetailProjectionV1/properties/pendingRegistrationCodes':'utf8',
},
'workflows/schemas/baseline-artifact.schema.json':{
 '/$defs/BaselineDescriptor/properties/entries':{'by':['fingerprint']},
 '/$defs/BaselineDescriptor/properties/pivotClosure':{'by':['closureId']},
},
'workflows/schemas/imported-evidence.schema.json':{
 '/$defs/SourceMappingV1/properties/entries':{'by':['generatedPath']},
 '/$defs/ImportWrapperV2/properties/blobs':'path',
},
'workflows/schemas/repair.schema.json':{
 '/$defs/RepairPlanDescriptor/properties/edits':'path',
},
}
for f in files:
    rel=str(f.relative_to(base));d=json.loads(f.read_text());rows=[];annotate(d,'',rows)
    for pointer,order in overrides.get(rel,{}).items():
        n=at(d,pointer);assert 'x-opensip-order' in n,(rel,pointer);n['x-opensip-order']=order
    f.write_text(json.dumps(d,indent=2)+'\n')
    changed.append({'path':rel,'arrayCount':len(rows),'strictOverrides':overrides.get(rel,{})})
out=Path('/tmp/opensip-design-corrections/codex-post-reset.v1/order-annotation-delta.v7.json');out.write_text(json.dumps(changed,indent=2)+'\n');print('Annotated',sum(r['arrayCount'] for r in changed),'arrays in',len(files),'current schema bundles')
