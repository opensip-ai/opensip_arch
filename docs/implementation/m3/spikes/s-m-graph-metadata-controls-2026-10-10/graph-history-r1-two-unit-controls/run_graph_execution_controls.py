from pathlib import Path
import json,hashlib,struct,tempfile,os,sys
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));from graph_execution import execute_graph
os.setpriority(os.PRIO_PROCESS,0,10);D=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');root=Path(tempfile.mkdtemp(prefix='opensip-sm-graph-controls-',dir=D));root.chmod(0o700);assert not(B/'graph-controls.json').exists();build=json.loads((B/'build.json').read_bytes());wrapper=dict(path=build['executable'],bytes=build['bytes'],sha256=build['sha256']);records=[]
def mapfile(name,files):
 p=root/(name+'.map');r=b'OPSMRUST1\0'+struct.pack('>Q',len(files))
 for n,data in sorted(files.items()):
  name=str(root/n).encode();r+=struct.pack('>Q',len(name))+name+struct.pack('>Q',len(data))+data
 p.write_bytes(r);return dict(path=str(p),bytes=len(r),sha256=hashlib.sha256(r).hexdigest())
def unit(name,file,deps=(),features=(),kind='lib'):
 return dict(pkg_id='fixture:'+name,target=dict(name=name,src_path=str(root/file),kind=[kind],crate_types=['lib'],edition='2024'),mode='check',platform=None,features=list(features),dependencies=[dict(index=i,extern_crate_name=alias) for i,alias in deps])
def run(name,g,files):
 m=mapfile(name,files);r=execute_graph(g,m,root/name,wrapper,build['sysroot'],root);records.append(dict(name=name,result=r));return r
r=run('actual-renamed-edge',dict(version=1,units=[unit('dependency','dep.rs'),unit('consumer','root.rs',[(0,'renamed')])],roots=[1]),{'dep.rs':b'pub fn value()->u8{7}', 'root.rs':b'pub fn value()->u8{renamed::value()}'});assert r['compilerChildren']==2 and r['rootResults'][0]['standing']=='analysis-and-metadata-completed'
r=run('real-root-type-error',dict(version=1,units=[unit('dependency','dep.rs'),unit('consumer','root.rs',[(0,'renamed')])],roots=[1]),{'dep.rs':b'pub fn value()->u8{7}', 'root.rs':b'pub fn value()->bool{renamed::value()}'});assert r['compilerChildren']==2 and r['rootResults'][0]['standing']=='incomplete'
r=run('transitive-unavailable-macro',dict(version=1,units=[unit('macro_unit','macro.rs',kind='proc-macro'),unit('consumer','root.rs',[(0,'macro_unit')])],roots=[1]),{'macro.rs':b'compile_error!("must not be analyzed")','root.rs':b'compile_error!("must not be analyzed")'});assert r['compilerChildren']==0 and all(x['standing']=='unavailable' for x in r['unitResults'])
r=run('incomplete-dependency-no-consumer',dict(version=1,units=[unit('dependency','dep.rs'),unit('consumer','root.rs',[(0,'renamed')])],roots=[1]),{'dep.rs':b'pub fn value()->bool{7}', 'root.rs':b'compile_error!("dependent compiler must not launch")'});assert r['compilerChildren']==1 and r['rootResults'][0]['compilerLaunched'] is False
r=run('selected-feature-real-analysis',dict(version=1,units=[unit('featured','feature.rs',features=['selected'])],roots=[0]),{'feature.rs':b'#[cfg(not(feature="selected"))] compile_error!("feature not supplied");pub fn value(){}'});assert r['compilerChildren']==1 and r['rootResults'][0]['standing']=='analysis-and-metadata-completed'
for name,cycle in [('graph-cycle-prelaunch',True),('map-pin-prelaunch',False)]:
 m=mapfile(name,{'root.rs':b'compile_error!("prelaunch refusal must happen")'});g=dict(version=1,units=[unit('consumer','root.rs',[(0,'self_dependency')] if cycle else [])],roots=[0]);out=root/name
 if not cycle:m['sha256']='0'*64
 try:execute_graph(g,m,out,wrapper,build['sysroot'],root)
 except ValueError as e:records.append(dict(name=name,refusedBeforeLaunch=True,error=str(e),outputRootCreated=out.exists()));assert not out.exists()
 else:raise AssertionError('expected prelaunch refusal')
result=dict(standing='ACTUAL FIRSTPARTY GRAPH METADATA EXECUTOR CONTROLS ONLY',controlsPassed=7,compilerChildren=sum(r.get('result',{}).get('compilerChildren',0) for r in records),records=records,root=str(root),actualCorpusTypecheck=False,corpusRun=False,fullCargoProfileEnvironment=False,nativeAdmission=False,sourceAuthentication=False,completeStatisticalSet=False,SMComplete=False);assert result['compilerChildren']==6;(B/'graph-controls.json').write_text(json.dumps(result,indent=2)+'\n');print('Seven graph controls pass/six compiler children; renamed dependency actual analysis, actual error/no dependent launch, unavailable macro closure0children, cfg and cycle/map prelaunch refusal. No corpus use.');assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
