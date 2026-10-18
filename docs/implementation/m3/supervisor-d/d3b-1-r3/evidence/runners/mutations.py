from pathlib import Path
import os,json,subprocess,re,tempfile
W=Path('/Users/sb/code/opensip-ai/opensip-d3b1-takeover');B=Path('/tmp/opensip-implementation/d3b1-mutations-takeover-r1');B.mkdir(exist_ok=False);assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1';os.setpriority(os.PRIO_PROCESS,0,10)
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';T=Path(tempfile.mkdtemp(prefix='opensip-d3b1-mut-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO=R+'cargo',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc')
p=W/'crates/components/src/supervisor.rs';original=p.read_bytes();text=original.decode()
mutations=[
 ('errors-not-incomplete','            && e.failures.is_empty()\n','', ['failed_tree_identity_reads_keep_their_step_and_errno','unsent_by_pid_outcomes_are_not_reported_as_kills']),
 ('exceeded-not-latched','            && !e.confirm_exceeded\n','',['an_exceeded_confirm_stays_incomplete_after_a_singleton']),
 ('group-delivery-counted','killed: evidence.by_pid.sent,','killed: evidence.by_pid.sent + evidence.group_kills,',['an_in_group_descendant_dies_with_the_group']),
 ('changed-group-skipped','if target.pgid() == root && now.pgid() == root {','if target.pgid() == root {',['a_snapshot_member_that_changes_group_is_targeted']),
 ('native-call-erased','self.failures.push(TreeCallFailure { step, error });','let error = match error { LaunchError::Io { error, .. } => LaunchError::Io { call: "erased", error }, other => other };\n        self.failures.push(TreeCallFailure { step, error });',['each_group_kill_failure_keeps_its_original_error']),
 ('snapshot-failure-cleared','outcome = SnapshotOutcome::ListingFailed;','outcome = SnapshotOutcome::Complete;',['a_failed_listing_or_group_kill_leaves_the_tree_incomplete']),
 ('provider-uses-tool-bound','''fn walk_bound(&self) -> usize {
        WALK_BOUND_FACTOR
            * match self.class {
                Class::Provider => PROVIDER_PROCESSES,''','''fn walk_bound(&self) -> usize {
        WALK_BOUND_FACTOR
            * match self.class {
                Class::Provider => TOOL_PROCESSES,''',['the_provider_snapshot_bound_counts_its_root']),
 ('root-not-counted',None,None,['the_snapshot_walk_bound_includes_its_root','the_provider_snapshot_bound_counts_its_root']),
]
# The snapshot-failure predicate also retains its native failure. Mutate both
# witnesses to model the original swallowed-listing failure rather than a
# behaviourally redundant enum change.
rows=[]
for name,before,after,tests in mutations:
 mutant=text
 if name=='root-not-counted':
  for a,b in [('Vec::with_capacity(bound);','Vec::with_capacity(bound + 1);'),('kill.targets.reserve_exact(bound - 1);','kill.targets.reserve_exact(bound);'),('let room = bound - queue.len();','let room = bound - (queue.len() - 1);')]:
   assert mutant.count(a)==1,a;mutant=mutant.replace(a,b)
 else:
  assert mutant.count(before)==1,(name,mutant.count(before));mutant=mutant.replace(before,after)
  if name=='snapshot-failure-cleared':
   a='kill.evidence.failed(TreeCall::SnapshotListing, error);';assert mutant.count(a)==1;mutant=mutant.replace(a,'drop(error);')
 p.write_text(mutant)
 try:
  args=[R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','--',*tests,'--test-threads=1']
  with (B/(name+'.log')).open('wb') as log:r=subprocess.run(args,cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT)
  out=(B/(name+'.log')).read_text(errors='replace');failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',out,re.M)));caught=r.returncode!=0 and bool(failed) and 'could not compile' not in out
 finally:p.write_bytes(original)
 rows.append(dict(name=name,caughtAtRuntime=caught,exitCode=r.returncode,failedTests=failed));(B/'controls.json').write_text(json.dumps(dict(rows=rows,allCaught=all(x['caughtAtRuntime'] for x in rows),privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True),indent=2)+'\n');print(name,caught,flush=True)
assert p.read_bytes()==original
assert all(x['caughtAtRuntime'] for x in rows)
