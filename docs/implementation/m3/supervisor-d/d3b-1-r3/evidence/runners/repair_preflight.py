from pathlib import Path
import shutil
w=Path('/Users/sb/code/opensip-ai/opensip-d3b1-takeover');p=w/'crates/components/src/supervisor.rs';s=p.read_text()
s=s.replace('''    /// Pids the walk queued, the root excluded, and pids whose identity it read.
    pub queued: u64,
    pub inspected: u64,''','''    /// Distinct pids queued and whose identity was read, including the root.
    pub queued: u64,
    pub inspected: u64,
    /// The root is observed and accounted, but never a by-pid target.
    pub root_identity: Option<ProcessIdentity>,
    pub root_exited: bool,''')
s=s.replace('''        queue.push(root);
        kill.targets.reserve_exact''','''        queue.push(root);
        kill.evidence.queued = 1;
        kill.targets.reserve_exact''')
a=s.index('''            if pid != root {
                kill.evidence.inspected += 1;''');b=s.index('''            // The remaining room:''',a)
s=s[:a]+'''            kill.evidence.inspected += 1;
            match self.tree_identity(pid, TreeCall::SnapshotIdentity) {
                Ok(Some(identity)) if pid == root => kill.evidence.root_identity = Some(identity),
                Ok(Some(identity)) => kill.targets.push(identity),
                Ok(None) if pid == root => kill.evidence.root_exited = true,
                Ok(None) => kill.evidence.by_pid.exited += 1,
                Err(error) => {
                    kill.evidence.identity_failed += 1;
                    kill.evidence.failed(TreeCall::SnapshotIdentity, error);
                }
            }
'''+s[b:]
# Test-only attempted-call recorder, kept behind the existing unit seam.
s=s.replace('''        evidence.group_kills += 1;
        #[cfg(test)]''','''        evidence.group_kills += 1;
        #[cfg(test)]
        self.seams.tree_calls.borrow_mut().push(tests::TreeCallAttempt::Group);
        #[cfg(test)]''')
s=s.replace('''            #[cfg(test)]
            let result = match self.seams.tree_kill_result''','''            #[cfg(test)]
            self.seams.tree_calls.borrow_mut().push(tests::TreeCallAttempt::ByPid(target.process_id()));
            #[cfg(test)]
            let result = match self.seams.tree_kill_result''')
p.write_text(s)
p=w/'crates/components/src/supervisor_tests.rs';s=p.read_text();s=s.replace('''/// D3b-1: a test's hook on the snapshot's targets.''','''#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum TreeCallAttempt { Group, ByPid(i32) }

/// D3b-1: a test's hook on the snapshot's targets.''')
s=s.replace('''    pub(crate) tree_hook: Option<TreeHook>,''','''    pub(crate) tree_hook: Option<TreeHook>,
    pub(crate) tree_calls: Rc<RefCell<Vec<TreeCallAttempt>>>,''')
s=s.replace('''struct ToolOutcome {
    settlement: Settlement,''','''struct ToolOutcome {
    settlement: Settlement,
    tree_calls: Vec<TreeCallAttempt>,''')
s=s.replace('''        let settlement = supervision.take_settlement().expect("one settlement");
        let scratch = supervision.seams.scratch.clone();
        drop(supervision);''','''        let settlement = supervision.take_settlement().expect("one settlement");
        let calls = Rc::clone(&supervision.seams.tree_calls);
        let before = calls.borrow().clone();
        for _ in 0..3 { supervision.turn(); }
        let scratch = supervision.seams.scratch.clone();
        drop(supervision);
        assert_eq!(*calls.borrow(), before, "no native tree call after settlement or in settled Drop");
        let tree_calls = calls.borrow().clone();''')
s=s.replace('''        done.send(ToolOutcome {
            settlement,''','''        done.send(ToolOutcome {
            settlement,
            tree_calls,''')
s=s.replace('(e.queued, e.inspected), (1, 1)','(e.queued, e.inspected), (2, 2)')
s=s.replace('''assert_eq!((e.queued, e.by_pid.sent), (0, 0));''','''assert_eq!((e.queued, e.by_pid.sent), (1, 0));''')
s=s.replace('''assert_eq!(evidence(&out).queued, 1);''','''assert_eq!(evidence(&out).queued, 2);''')
s=s.replace('''        e.inspected,
        "{e:?}"''','''        e.inspected - 1,
        "{e:?}"''')
s=s.replace('''observed.queued < 64,''','''observed.queued <= 64,''').replace('''(observed.queued, observed.inspected), (63, 63)''','''(observed.queued, observed.inspected), (64, 64)''')
s=s.replace('''        assert_eq!(e.failures.len(), 1, "{e:?}");''','''        let failures = if step == TreeCall::SnapshotIdentity { 2 } else { 1 };
        assert_eq!(e.failures.len(), failures, "{e:?}");''')
# Add original-error diagnostics to old expectations before deciding their exact disposition.
s=s.replace('''        out.settlement.tree(),
        TreeReport::GroupKilledPlatformLimited
    );''','''        out.settlement.tree(),
        TreeReport::GroupKilledPlatformLimited,
        "{:?}", out.settlement.tree_evidence()
    );''')
s=s.replace('''assert_eq!(settlement.tree(), want, "{at:?}, extra {extra_member}");''','''assert_eq!(settlement.tree(), want, "{at:?}, extra {extra_member}: {:?}", settlement.tree_evidence());''')
# Add the native no-root/no-post-abandon assertions to the alive case.
s=s.replace('''    // The group SIGKILL "fails": the root dies by its SIGTERM, and the
    // member is killed out of band.''','''    // All group SIGKILL attempts fail. The ignored SIGTERM leaves a live
    // root at abandonment; both it and the member are cleaned up out of band.''')
s=s.replace('''    let out = tool_run(script, |s| s.seams.group_kill_fails = true);''','''    let out = tool_run(script, |s| {
        s.seams.group_kill_fails = true;
        s.seams.tree_hook = Some(TreeHook(Box::new(|step, targets| {
            if step == TreeStep::AfterSnapshot {
                assert!(targets.iter().all(|target| target.process_id() != target.pgid()),
                    "the owned root must not enter the by-pid target set");
            }
        })));
    });''')
s=s.replace('''    assert!(e.group_kill_failures >= 1);
    assert_eq!(e.failures.len()''','''    assert!(e.group_kill_failures >= 1);
    let root = out.process_id.expect("root");
    assert!(!out.tree_calls.contains(&TreeCallAttempt::ByPid(root)));
    assert_eq!(out.tree_calls.iter().filter(|call| **call == TreeCallAttempt::Group).count() as u64, e.group_kills);
    let ceiling = out.events.iter().position(|event| *event == SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling)).expect("ceiling");
    assert!(!out.events[ceiling..].iter().any(|event| matches!(event, SupervisionEvent::Signalled { .. })));
    assert_eq!(e.failures.len()''')
p.write_text(s)
# Exact generated reference bytes emitted by the failing drift control.
q=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-d3b1-full-edo0jlnv')
for name in ['registry-events.json','registry-events.md']:shutil.copyfile(q/name,w/'crates/operability'/name)
print('root snapshot accounting, attempted-call controls and generated registry repaired')
