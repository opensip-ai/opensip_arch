"""Explicitly built fault probes; infrastructure failures NEVER count as detection."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H=Path(__file__).resolve().parent
D=H/'fault-runs-r2'
assert not D.exists(); D.mkdir()
source=(H/'project_registry.rs').read_text()
faults={
 'accept-extra-fields':('o.len() != fields.len()', 'o.len() < fields.len()'),
 'accept-duplicate-namespace':('prev.namespace >= e.namespace','prev.namespace > e.namespace'),
 'ignore-live-project-uniqueness':('if !projects.insert(e.project.clone()) {','if !projects.insert(e.project.clone()) && false {'),
 'ignore-live-locator-uniqueness':('if !locators.insert((e.root.platform, e.root.path.clone())) {','if !locators.insert((e.root.platform, e.root.path.clone())) && false {'),
 'ignore-live-incarnation-uniqueness':('if !incarnations.insert(e.root.incarnation()) {','if !incarnations.insert(e.root.incarnation()) && false {'),
 'accept-4097-rows':('REGISTRY_ROW_CAP: usize = 4096','REGISTRY_ROW_CAP: usize = 4097'),
 'lose-adoption-kind':('"adopt" => AllocationKind::Adopt','"adopt" => AllocationKind::Random'),
 'wrong-marker-prefix-length':('raw[MARKER_PREFIX.len()..raw.len() - 1]','raw[21..raw.len() - 1]'),
 'wrong-projection-values':('.map(|e| e.namespace.as_str())','.map(|e| e.project.as_str())'),
}
env=json.loads(Path('/tmp/opensip-implementation/host-materialization368-r1/environment.json').read_text())
parent=json.loads((H/'compile-r1.json').read_text())['parentIdentityRlib']
identity=Path(parent['path']);raw=identity.read_bytes()
assert len(raw)==parent['bytes'] and hashlib.sha256(raw).hexdigest()==parent['sha256']
rustc='/opt/homebrew/Cellar/rust/1.95.0/bin/rustc'

def run(cmd,prefix):
    # FileNotFoundError/timeout propagates. It is NEVER converted to a kill.
    r=subprocess.run(cmd,capture_output=True,env=env,timeout=120)
    prefix.with_suffix('.stdout').write_bytes(r.stdout);prefix.with_suffix('.stderr').write_bytes(r.stderr)
    prefix.with_suffix('.json').write_text(json.dumps(dict(command=cmd,exitCode=r.returncode),indent=2)+'\n')
    return r

def build(directory):
    lib=directory/'libproject_registry_prototype.rlib';probe=directory/'probe'
    assert not lib.exists() and not probe.exists()
    common=['--edition=2024','--extern','opensip_identity='+str(identity),'-L','dependency='+str(identity.parent),'-D','warnings']
    cmd=[rustc,*common,'--crate-name','project_registry_prototype','--crate-type=rlib',str(directory/'lib.rs'),'-o',str(lib)]
    assert run(cmd,directory/'compile').returncode==0,'compiler failure, not detection'
    assert lib.is_file()
    cmd=[rustc,*common,str(directory/'probe.rs'),'--extern','project_registry_prototype='+str(lib),'-L','dependency='+str(directory),'-o',str(probe)]
    assert run(cmd,directory/'probe-compile').returncode==0,'compiler failure, not detection'
    assert probe.is_file()
    return probe

def classify(rc,stderr,result):
    if result is not None:
        if (rc==1 and result.get('cases')==37412 and result.get('failures') and
                all(r['expected']!=r['actual'] for r in result['failures'])):
            return 'structured semantic mismatch'
        raise AssertionError('not a completed differential mismatch')
    markers=('typed getters lost or changed a field','projection must preserve exact namespace values and order')
    if (rc==1 and "thread 'main'" in stderr and 'panicked at ' in stderr and
            'assertion `left == right` failed:' in stderr and any(m in stderr for m in markers)
            and 'FileNotFoundError' not in stderr):
        return 'running Rust probe typed round-trip/projection assertion'
    raise AssertionError('infrastructure or unexpected failure, NOT a semantic detection')

# Controls for the exact false-positive class discovered in r1, plus generic
# compile/missing-artifact/timeout/panic errors. None may become a fault kill.
for rc,stderr,result in [
    (1,'FileNotFoundError: missing probe',None),
    (1,'compiler failed',None),
    (1,'TimeoutExpired',None),
    (101,"thread 'main' panicked at: unrelated panic",None),
    (0,'',dict(cases=37412,failures=[])),
    (1,'',dict(cases=1,failures=[dict(expected='R',actual='A')])),
]:
    try: classify(rc,stderr,result)
    except AssertionError: pass
    else: raise AssertionError('false-positive guard failed')

baseline=D/'baseline';baseline.mkdir()
for name in ('project_registry.rs','lib.rs','probe.rs'):(baseline/name).write_bytes((H/name).read_bytes())
probe=build(baseline)
r=run([sys.executable,'-B',str(H/'check_differential.py'),'--probe',str(probe),'--output',str(baseline/'differential.json')],baseline/'check')
assert r.returncode==0 and not json.loads((baseline/'differential.json').read_text())['failures']
results=[]
for name,(old,new) in faults.items():
    assert source.count(old)==1
    d=D/name;d.mkdir();(d/'project_registry.rs').write_text(source.replace(old,new))
    for n in ('lib.rs','probe.rs'):(d/n).write_bytes((H/n).read_bytes())
    probe=build(d)
    r=run([sys.executable,'-B',str(H/'check_differential.py'),'--probe',str(probe),'--output',str(d/'differential.json')],d/'check')
    result=json.loads((d/'differential.json').read_text()) if (d/'differential.json').exists() else None
    reason=classify(r.returncode,r.stderr.decode(),result)
    results.append(dict(name=name,compiled=True,artifactExists=True,detected=True,reason=reason,exitCode=r.returncode,
                        sourceSha256=hashlib.sha256((d/'project_registry.rs').read_bytes()).hexdigest(),probeSha256=hashlib.sha256(probe.read_bytes()).hexdigest()))
(H/'fault-results.r2.json').write_text(json.dumps(dict(scope='pure codec faults only; original r1 detection claims invalid',baseline='PASS',infrastructureFailuresRefused=6,faults=results),indent=2)+'\n')
print(json.dumps(dict(baseline='PASS',compiled=len(results),realSemanticDetections=len(results),infrastructureGuards=6)))
