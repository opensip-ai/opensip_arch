use std::sync::Arc;
use std::sync::atomic::{AtomicU64, Ordering};
use std::thread;

fn main() {
    let commits = Arc::new(AtomicU64::new(0));
    let latched = Arc::new(AtomicU64::new(0));
    let both = Arc::new(AtomicU64::new(0));
    let rounds = 200000u64;
    for i in 0..rounds {
        let att = Arc::new(security::AttemptState::new());
        let a1 = Arc::clone(&att);
        let a2 = Arc::clone(&att);
        let h = thread::spawn(move || a1.latch());
        if (i % 3) == 0 { std::hint::spin_loop(); }
        let admitted = a2.admit_commit();
        let l = h.join().unwrap();
        if admitted && l { both.fetch_add(1, Ordering::SeqCst); }
        if admitted { commits.fetch_add(1, Ordering::SeqCst); }
        if l { latched.fetch_add(1, Ordering::SeqCst); }
        let post = att.latch();
        if post && admitted { both.fetch_add(1, Ordering::SeqCst); }
        let final_state = att.state();
        if final_state == security::ATT_PREPARING { both.fetch_add(1, Ordering::SeqCst); }
    }
    println!("rounds={} commit_admitted={} latched={} mutual_exclusion_violations={}",
             rounds, commits.load(Ordering::SeqCst), latched.load(Ordering::SeqCst), both.load(Ordering::SeqCst));
    println!("sum_equals_rounds={}", commits.load(Ordering::SeqCst) + latched.load(Ordering::SeqCst) == rounds);
}
