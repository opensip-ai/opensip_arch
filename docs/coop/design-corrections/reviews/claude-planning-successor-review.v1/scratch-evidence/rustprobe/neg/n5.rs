// N5: Drop on the owning commit-state type vs moving its fields out
pub struct Guard(u8);
impl Drop for Guard { fn drop(&mut self) { self.0 = 0; } }
pub struct PreparedCommitWithDrop { run: String, guard: Guard }
impl Drop for PreparedCommitWithDrop { fn drop(&mut self) { } }
pub fn publish(p: PreparedCommitWithDrop) -> (String, Guard) {
    let PreparedCommitWithDrop { run, guard } = p;
    (run, guard)
}
