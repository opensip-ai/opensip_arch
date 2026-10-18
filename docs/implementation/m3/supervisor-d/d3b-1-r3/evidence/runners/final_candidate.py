from pathlib import Path
import os,json,subprocess,tempfile,re,hashlib
W=Path('/Users/sb/code/opensip-ai/opensip-d3b1-takeover');F=Path(__file__).parent;B=Path('/tmp/opensip-implementation/d3b1-final-candidate-r1');B.mkdir(exist_ok=False);assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1';os.setpriority(os.PRIO_PROCESS,0,10)
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';T=Path(tempfile.mkdtemp(prefix='opensip-d3b1-final-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO=R+'cargo',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc')
subprocess.run(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(F/'repair_preflight.py')],check=True)
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s+='\n'+(F/'provider_bound_control.txt').read_text();s+='\n'+(F/'root_only_control.txt').read_text();s=s.replace("text.split(' ')",'text.split_whitespace()')
s=s.replace('''    assert!(e.group_kill_failures >= 1);
    assert_eq!(e.failures.len() as u64, e.group_kill_failures);''','''    assert!(e.group_kill_failures >= 1);
    assert_eq!(out.settlement.exit(), ExitClass::Unreaped);
    assert!(!out.saw(&SupervisionEvent::ExitObserved), "the failed group calls leave the root alive");
    assert_ne!(e.confirm, ConfirmOutcome::RootAlone);
    if let Some(root) = out.process_id { if has_identity(root) { kill_out_of_band(root); } }
    assert_eq!(e.failures.len() as u64, e.group_kill_failures);''')
a=s.index('fn no_group_signal_follows_the_reap_ceiling()');b=s.index('/// LD-D3B-12',a);chunk=s[a:b];chunk=chunk.replace('''    assert_eq!(out.settlement.exit(), ExitClass::Unreaped);''','''    assert_eq!(out.settlement.exit(), ExitClass::Unreaped);
    assert!(out.saw(&SupervisionEvent::ExitObserved), "this control holds an exited root unreaped");
    assert_eq!(evidence(&out).confirm, ConfirmOutcome::RootAlone);''');s=s[:a]+chunk+s[b:];p.write_text(s)
p=W/'crates/components/tests/supervisor_fixture.rs';s=p.read_text().replace('"ingroup" => pids.push(spawn_tree_member(None, false)),','"ingroup" => pids.push(spawn_tree_member(None, false)),\n        "root-only" => {},');s=s.replace('"loop" | "walk-exact" | "walk-over" => {','"loop" | "walk-exact" | "walk-over" | "provider-exact" | "provider-over" => {').replace('''                "walk-exact" => 63,''','''                "provider-exact" => 3,
                "provider-over" => 4,
                "walk-exact" => 63,''')
s=s.replace('''        while !std::path::Path::new(&gate).exists() {
            std::thread::sleep(Duration::from_millis(2));
        }''','''        let began = std::time::Instant::now();
        while !std::path::Path::new(&gate).exists() {
            if began.elapsed() >= Duration::from_secs(60) { std::process::exit(52); }
            std::thread::sleep(Duration::from_millis(2));
        }''');p.write_text(s)
for path in ['crates/components/src/supervisor_tests.rs','crates/components/tests/supervisor_fixture.rs']:
 p=W/path;p.write_bytes(subprocess.check_output([R+'rustfmt','--edition','2024','--emit','stdout'],input=p.read_bytes(),cwd=W,env=E))
args=[R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components'];r=subprocess.run(args,cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'build-artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0
fixture=lib=None
for raw in r.stdout.splitlines():
 try:m=json.loads(raw)
 except ValueError:continue
 if m.get('reason')!='compiler-artifact' or not m.get('executable'):continue
 if m['target']['name']=='supervisor_fixture':fixture=Path(m['executable'])
 if m['target']['name']=='opensip_components' and 'lib' in m['target']['kind'] and m['profile']['test']:lib=Path(m['executable'])
assert fixture and lib
h=hashlib.sha256(fixture.read_bytes()).hexdigest();(lib.parent/'supervisor_fixture.path').write_text(f'{fixture}\n{h}\n')
with (B/'affected-controls.log').open('wb') as out:early=subprocess.run([str(lib),'--test-threads=1','the_tree_is_confirmed_before_the_reap','an_unwind_confirms_the_tree_before_its_reap','the_provider_snapshot_bound_counts_its_root','a_root_only_snapshot_records_the_owned_root','a_failed_listing_or_group_kill_leaves_the_tree_incomplete','no_group_signal_follows_the_reap_ceiling'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert early.returncode==0, 'inspect affected-controls.log before full repeat'
with (B/'components.log').open('wb') as out:r=subprocess.run([str(lib),'--test-threads=1'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
s=(B/'components.log').read_text(errors='replace');summary=re.findall(r'test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;',s);assert summary;failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',s,re.M)));rows=[dict(name='components-final-suite',exitCode=r.returncode,passed=int(summary[-1][0]),failed=failed,ignored=int(summary[-1][2]))];print(rows[-1],flush=True)
for name,args in [('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-components','-p','opensip-platform','-p','opensip-operability','--all-targets','--','-D','warnings']),('no-cgroup',['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(F/'check_no_cgroup.py'),str(W)])]:
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 rows.append(dict(name=name,exitCode=r.returncode));print(name,r.returncode,flush=True)
paths=subprocess.check_output(['git','diff','--name-only'],cwd=W,env=E,text=True).splitlines();pins=[dict(path=p,bytes=len((W/p).read_bytes()),sha256=hashlib.sha256((W/p).read_bytes()).hexdigest()) for p in paths];(B/'product-pins.json').write_text(json.dumps(pins,indent=2)+'\n')
(B/'checks.json').write_text(json.dumps(dict(rows=rows,allPassed=all(x['exitCode']==0 for x in rows),productBase=subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip(),fixtureSha256=h,privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True,qualification=False),indent=2)+'\n')
assert all(x['exitCode']==0 for x in rows)
