use std::sync::atomic::{AtomicU8, Ordering};

const PREPARING: u8 = 0;
const COMMIT_ADMITTED: u8 = 1;
const LATCHED: u8 = 2;
const ADMITTED_THEN_LATCHED: u8 = 3;

struct Corrected(AtomicU8);
impl Corrected {
    fn new() -> Self { Corrected(AtomicU8::new(PREPARING)) }
    fn latch(&self) -> u8 {
        loop {
            let cur = self.0.load(Ordering::SeqCst);
            let next = match cur {
                PREPARING => LATCHED,
                COMMIT_ADMITTED => ADMITTED_THEN_LATCHED,
                other => return other,
            };
            if self.0.compare_exchange(cur, next, Ordering::SeqCst, Ordering::SeqCst).is_ok() { return next; }
        }
    }
    fn admit_commit(&self) -> bool {
        self.0.compare_exchange(PREPARING, COMMIT_ADMITTED, Ordering::SeqCst, Ordering::SeqCst).is_ok()
    }
    fn commit_permitted(&self) -> bool { self.0.load(Ordering::SeqCst) == COMMIT_ADMITTED }
    fn further_effects_permitted(&self) -> bool { self.0.load(Ordering::SeqCst) == COMMIT_ADMITTED }
    fn state(&self) -> u8 { self.0.load(Ordering::SeqCst) }
}

fn main() {
    let a = security::AttemptState::new();
    let admitted = a.admit_commit();
    let post = a.latch();
    println!("AS-PROPOSED admitted={} post_latch_recorded={} final_state={}", admitted, post, a.state());
    let c = Corrected::new();
    let ok = c.admit_commit();
    let s = c.latch();
    println!("CORRECTED admitted={} post_latch_state={} commit_permitted={} further_effects_permitted={}",
             ok, s, c.commit_permitted(), c.further_effects_permitted());
    let c2 = Corrected::new();
    let s2 = c2.latch();
    println!("CORRECTED latch_first_state={} admit_after_latch={} commit_permitted={}", s2, c2.admit_commit(), c2.commit_permitted());
}
