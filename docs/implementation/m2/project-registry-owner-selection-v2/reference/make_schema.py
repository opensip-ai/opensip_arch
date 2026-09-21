from pathlib import Path
import json
D=Path(__file__).parent
S={'type':'string'}
def closed(props):return {'type':'object','additionalProperties':False,'required':list(props),'properties':props}
end=r'(?![\s\S])'
root=closed({'platform':{'const':'macos'},'canonicalPathBytesHex':{'type':'string','minLength':2,'maxLength':8192,'pattern':r'^(?:[0-9a-f]{2})+'+end},'volumeIdentity':closed({'kind':{'const':'macos-apfs-volume-uuid-v1'},'value':{'type':'string','pattern':r'^[0-9a-f]{32}'+end}}),'inodeId':{'type':'string','maxLength':20,'pattern':r'^(?:0|[1-9][0-9]*)'+end},'birthSeconds':{'type':'integer','minimum':-(1<<63),'maximum':(1<<63)-1},'birthNanoseconds':{'type':'integer','minimum':0,'maximum':999999999}})
entry=closed({'projectId':{'type':'string','pattern':r'^prj1-[0-9a-f]{64}'+end},'namespaceId':{'type':'string','pattern':r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'+end},'root':{'$ref':'#/$defs/NativeProjectRootV2'},'status':{'enum':['RESERVED','ACTIVE','RETIRED','ABANDONED']},'allocationKind':{'enum':['random','adopt']}})
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:proposed:project-registry-v2','title':'Proposed379 private ProjectId registry, NOT accepted',**closed({'schemaVersion':{'type':'integer','const':2},'entries':{'type':'array','maxItems':4096,'items':{'$ref':'#/$defs/Entry'}}}),'$defs':{'NativeProjectRootV2':root,'Entry':entry},'$comment':'Schema is necessary but insufficient: exact lexical/canonical/4MiB byte profile, native-path grammar, nonzero volume UUID, qualified native APFS acquisition, decimal-u64 range, sorted globally unique N, live ProjectId/root/locator uniqueness, delta and native authorization/custody are separate mandatory rules. No schema result grants authority.'}
(D/'project-registry.schema.json').write_text(json.dumps(schema,indent=2)+'\n')
