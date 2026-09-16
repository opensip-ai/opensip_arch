// Design control only: atomic admission versus fail-stop, not durable storage or OS qualification.
use std::sync::{Arc, Barrier};
use std::sync::atomic::{AtomicU8, Ordering};
struct Gate(AtomicU8);
// This private, non-Clone permit is consumed once; a latch cannot mint another permit.
struct Permit;
impl Gate {
    fn new() -> Self { Self(AtomicU8::new(0)) }
    fn admit(&self) -> Option<Permit> {
        self.0.compare_exchange(0, 1, Ordering::SeqCst, Ordering::SeqCst).ok().map(|_| Permit)
    }
    fn latch(&self) { self.0.fetch_or(2, Ordering::SeqCst); }
    fn state(&self) -> u8 { self.0.load(Ordering::SeqCst) }
}
fn complete_already_admitted(_permit: Permit) -> bool { true }
fn main() {
    let gate=Gate::new(); gate.latch(); assert!(gate.admit().is_none()); assert_eq!(gate.state(),2);
    let gate=Gate::new(); let p=gate.admit().unwrap();gate.latch();assert_eq!(gate.state(),3);
    assert!(complete_already_admitted(p));assert!(gate.admit().is_none());
    let mut wins=[0usize;2];
    for _ in 0..20000 {
        let gate=Arc::new(Gate::new()); let start=Arc::new(Barrier::new(2));
        let g=gate.clone();let b=start.clone();
        let observer=std::thread::spawn(move || {b.wait();g.latch();});
        start.wait();let permit=gate.admit();observer.join().unwrap();
        match permit {
            Some(p)=>{assert_eq!(gate.state(),3);assert!(complete_already_admitted(p));wins[0]+=1;},
            None=>{assert_eq!(gate.state(),2);wins[1]+=1;}
        }
        assert!(gate.admit().is_none()); gate.latch(); assert_eq!(gate.state()&2,2);
    }
    println!("{{\"races\":20000,\"admittedBeforeLatch\":{},\"latchBeforeAdmission\":{},\"violations\":0,\"productQualification\":false}}",wins[0],wins[1]);
}
