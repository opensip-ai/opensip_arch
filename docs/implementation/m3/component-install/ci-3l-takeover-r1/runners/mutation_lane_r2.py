from pathlib import Path
import ast,os,subprocess,tempfile,json,hashlib,re,difflib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-ci3l-takeover');O=F/'mutations-r2';O.mkdir();R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
# Reuse the nineteen reviewed mutation definitions, not their old outcomes.
names={'LC','RT','CT','LSTAT_CHARGED','LSTAT_AFTER','HOP','BIND','MUTATIONS'};tree=ast.parse((F/'full_lane_r1.py').read_text());selected=[n for n in tree.body if isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id in names for t in n.targets)];env={};exec(compile(ast.Module(body=selected,type_ignores=[]),'<reviewed-mutation-definitions>','exec'),env);M=list(env['MUTATIONS']);RT=env['RT'];CT=env['CT'];LC=env['LC'];TEST='crates/lifecycle/src/retained_tree_tests.rs'
a='''pub fn status_read_cost() -> crate::WorkCost {
    crate::WorkCost {
        objects: 0,
        edges: 1,''';M.append(('price-status-read-undercharge','lifecycle',[(CT,a,a.replace('edges: 1,','edges: 0,'))]))
a='''        edges: 1 + status.edges,
        bytes: status.bytes,''';M.append(('price-regular-open-undercharge','lifecycle',[(CT,a,a.replace('1 + status.edges','status.edges'))]))
a='''pub(crate) fn descend_cost(name: usize) -> WorkCost {
    WorkCost {
        objects: 3,
        edges: 3,''';M.append(('price-descent-undercharge','lifecycle',[(LC,a,a.replace('edges: 3,','edges: 2,'))]))
M.append(('reference-last-hop-regression','lifecycle',[(TEST,'                    if lookups > links {\n','                    if lookups > links + 1 {\n')]))
M.append(('hop-overflow-as-association','lifecycle',[(RT,'length.ok_or(TreeReadFailure::Budget(WorkBudgetError::Arithmetic))','length.ok_or(TreeReadFailure::Association)')]))
assert len(M)==24
base=json.loads((F/'initial-r4/report.json').read_text());assert base['allPassed'];original={p:(W/p).read_bytes() for p in base['sourcePins']};assert all(hashlib.sha256(b).hexdigest()==base['sourcePins'][p] for p,b in original.items())
for name,focus,edits in M:
 changed={}
 for p,before,after in edits:
  source=changed.get(p,original[p].decode());assert source.count(before)==1,(name,p,source.count(before));changed[p]=source.replace(before,after)
T=Path(tempfile.mkdtemp(prefix='opensip-ci3l-mut-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'initial-r1/target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
filters={'lifecycle':['retained_tree::tests::ci_t27','retained_tree::tests::ci_t28','retained_tree::tests::ci_a3_d'],'platform':['component_tree::']};expected={'lifecycle':16,'platform':15};report=dict(standing='CORRECTED CI-3L FINAL SOURCE MUTATION CONTROLS; NOT UNIT ACCEPTANCE',sourcePins=base['sourcePins'],privateTMPDIR=str(T),mutations=[],restored=False)
def save():(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def build(label,focus,fresh_required):
 pkg='opensip-'+focus;name='opensip_'+focus
 r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--lib','--message-format=json','-p',pkg],cwd=W,env=E,capture_output=True);(O/(label+'-build.log')).write_bytes(r.stderr);(O/(label+'-artifacts.jsonl')).write_bytes(r.stdout);assert r.returncode==0,(label,'compile failure is not a caught mutation',r.stderr[-5000:]);hits=[j for line in r.stdout.splitlines() if line.startswith(b'{') for j in [json.loads(line)] if j.get('reason')=='compiler-artifact' and j.get('target',{}).get('name')==name and j.get('profile',{}).get('test') and j.get('executable')];assert len(hits)==1 and hits[0]['target']['src_path']==str(W/('crates/'+focus+'/src/lib.rs'))
 if fresh_required:assert hits[0]['fresh'] is False,(label,'stale test image')
 return Path(hits[0]['executable']),hits[0]['fresh']
def run(label,focus,binary):
 args=[str(binary),*filters[focus]]
 if focus=='platform':args.append('--test-threads=1')
 with (O/(label+'.log')).open('wb') as log:r=subprocess.run(args,cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT,timeout=120)
 return r,(O/(label+'.log')).read_text()
try:
 for name,focus,edits in M:
  try:
   for p,before,after in edits:
    source=(W/p).read_text();assert source.count(before)==1;(W/p).write_text(source.replace(before,after))
   (O/(name+'.diff')).write_text(''.join(''.join(difflib.unified_diff(original[p].decode().splitlines(True),(W/p).read_text().splitlines(True),fromfile='before/'+p,tofile='mutated/'+p)) for p in sorted({e[0] for e in edits})))
   binary,fresh=build(name,focus,True);result,out=run(name,focus,binary);assert result.returncode==101 and re.search(r'test result: FAILED\..* [1-9]\d* failed;',out),(name,result.returncode,out[-5000:]);failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',out,re.M)));assert failed
   report['mutations'].append(dict(name=name,focus=focus,files=sorted({e[0] for e in edits}),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),fresh=fresh,exitCode=result.returncode,runtimeFailure=True,failed=failed));save();print(name,'caught',flush=True)
  finally:
   for p in {e[0] for e in edits}:(W/p).write_bytes(original[p])
finally:
 for p,b in original.items():assert (W/p).read_bytes()==b,p
 report['restored']=True;save()
for focus in filters:
 binary,fresh=build(focus+'-restored',focus,False);result,out=run(focus+'-restored',focus,binary);assert result.returncode==0 and f'{expected[focus]} passed; 0 failed; 0 ignored;' in out,(focus,out[-4000:]);report[focus+'RestoredPasses']=expected[focus]
report['all24Caught']=len(report['mutations'])==24;save();assert report['all24Caught'];print('All24 compiled runtime mutants caught,7 source paths restored and16+15 positives passed',flush=True)
