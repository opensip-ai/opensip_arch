from pathlib import Path
import json,importlib.util,sys,copy
D=Path('/tmp/opensip-design-corrections/claude-discovery-correction.v1/scratch/successor/docs/coop/design-corrections')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
DD=load('root_dd',D/'discovery-defaults.py');S=load('root_sec',D/'security/security_lifecycle_model_v1.py');N=load('root_nat',D/'native/native_evidence_model.v2.py');results=[]
root='/home/alice/repo';fs={'/':{'kind':'dir','uid':0,'mode':'0755','dev':1},'/home':{'kind':'dir','uid':0,'mode':'0755','dev':1},'/home/alice':{'kind':'dir','uid':1000,'mode':'0700','dev':1},root:{'kind':'dir','uid':1000,'mode':'0755','dev':1,'vcs':True},root+'/package.json':{'kind':'file','uid':1000,'mode':'0644','nlink':1,'size':100}}
prov=S.discovery({'invokingUid':1000,'accountHome':'/home/alice','cwd':root,'fs':fs})['provenance'];old=copy.deepcopy(prov);old['schemaVersion']=1;S.validate_discovery_provenance(old)
try:v=DD.boundary_inventory_from_provenance(old);results.append({'control':'valid V1 provenance empty prunes handed to conversion described as V2-only','outcome':'accepted','inputVersion':1,'outputVersion':v['schemaVersion']})
except Exception as e:results.append({'control':'valid V1 provenance empty prunes handed to conversion described as V2-only','outcome':'refused','reason':repr(e)})
v=DD.boundary_inventory_from_provenance(prov);v['schemaVersion']=1;v['prunedTrees']=[{'path':'node_modules','reason':'dependency-tree','markerCount':1}];N.validate_boundary_inventory(v)
try:
 result=N.discover_units({'package.json':{'sha256':'a'*64},'node_modules/pkg/package.json':{'sha256':'b'*64}},None,v);results.append({'control':'schema-valid V1 boundary with pruned row handed to version-dispatching discovery','outcome':'accepted','result':result})
except Exception as e:results.append({'control':'schema-valid V1 boundary with pruned row handed to version-dispatching discovery','outcome':'refused','reason':repr(e)})
Path(__file__).with_suffix('.json').write_text(json.dumps({'standing':'Root probes of new authored version dispatch only; no product claim','results':results},indent=2)+'\n');print(json.dumps(results))
