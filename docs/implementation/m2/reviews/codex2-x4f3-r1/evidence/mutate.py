"""X4-F3's mutation checks: apply one named mutation to operation_guard.rs
(restored by the caller from its backup)."""
import sys
P = '/Users/sb/code/opensip-ai/opensip-x4f3/crates/security/src/custody/operation_guard.rs'
s = open(P).read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
m = sys.argv[1]
if m == 'r7-records':
    # r7's code: X3d's stop latches with no cause, and the reader records
    # the placeholder `FailStop { latched }`.
    rep('''    pub(crate) fn stop(&self, cause: StopCause) -> AttemptState {
        self.shared.stop.stop(cause).state
    }''', '''    pub(crate) fn stop(&self, cause: StopCause) -> AttemptState {
        let _ = cause;
        self.shared.stop.0.gate.latch()
    }''')
    rep('''    fn latched(&self) -> GuardRefusal {
        self.cause()
            .map_or(GuardRefusal::Invariant, GuardRefusal::Stopped)
    }''', '''    fn latched(&self) -> GuardRefusal {
        GuardRefusal::Stopped(
            slot(&self.0.cause)
                .get_or_insert(StopCause::FailStop { subject: "latched" })
                .clone(),
        )
    }''')
elif m == 'no-entry-check':
    rep('    let latched = stop.entry_latched();', '    let latched = { stop.entry_latched(); false };')
elif m == 'bare-unwind':
    rep('''    fn unwound(&self) {
        self.stop(StopCause::FailStop { subject: "latched" });
    }''', '''    fn unwound(&self) {
        self.0.gate.latch();
    }''')
else:
    raise SystemExit(f'unknown mutation {m}')
open(P, 'w').write(s)
