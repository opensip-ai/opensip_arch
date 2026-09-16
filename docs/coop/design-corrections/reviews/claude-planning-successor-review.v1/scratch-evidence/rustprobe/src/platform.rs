//! Live writer guard owner: non-cloneable, single-use.
pub struct WriterGuard { live: bool }
impl WriterGuard {
    pub fn acquire() -> Option<WriterGuard> { Some(WriterGuard { live: true }) }
    pub fn is_live(&self) -> bool { self.live }
}
impl Drop for WriterGuard { fn drop(&mut self) { self.live = false; } }
