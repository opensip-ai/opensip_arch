//! Must fail to compile: FramedCandidate fields are private.
fn main() {
    let candidate: Option<opensip_identity::FramedCandidate> = None;
    if let Some(c) = candidate {
        let _ = c.digest;
        let _ = c.domain;
        let _ = c.set;
        let _ = c.row;
        let _ = c.shape;
    }
}
