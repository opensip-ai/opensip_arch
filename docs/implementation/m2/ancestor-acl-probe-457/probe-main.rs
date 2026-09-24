//! Probe 457: bounded ACL state of the fixed operational ancestors. Read-only.
//! Prints only kind, owner class, permission bits, state and per-entry kind/
//! principal class/rights. No principal identifiers are printed.
use opensip_platform::{CapturedAclPrincipal, CapturedAclState, WorkLedger, capture_descriptor_acl_accounted};
use std::os::unix::fs::OpenOptionsExt;
fn main() {
    let uid = unsafe { libc_geteuid() };
    let mut ledger = WorkLedger::new();
    for arg in std::env::args().skip(1) {
        let path = std::path::PathBuf::from(&arg);
        let label = arg.clone();
        let file = match std::fs::OpenOptions::new().read(true).custom_flags(0x0010_0000 /*O_DIRECTORY*/ | 0x0000_0100 /*O_NOFOLLOW*/).open(&path) {
            Ok(f) => f,
            Err(e) => { println!("{label}: open {:?}", e.kind()); continue; }
        };
        let result = ledger.scope(|work| capture_descriptor_acl_accounted(&file, work));
        match result {
            Err(e) => println!("{label}: capture error {e:?}"),
            Ok(c) => {
                let m = c.metadata();
                let owner = if m.uid == uid { "invoking" } else if m.uid == 0 { "root" } else { "other" };
                println!("{label}: type {:o} perms {:o} owner {owner} state {:?} aclflags {:?}", m.mode & 0o170000, m.mode & 0o7777, c.acl_state(), c.acl_flags());
                if let CapturedAclState::Entries(n) = c.acl_state() {
                    for k in 0..n {
                        let e = c.entry(k).unwrap();
                        let who = match e.principal { CapturedAclPrincipal::User(u) if u == uid => "invoking-user", CapturedAclPrincipal::User(0) => "root-user", CapturedAclPrincipal::User(_) => "other-user", CapturedAclPrincipal::Group(_) => "group", CapturedAclPrincipal::Unresolved => "unresolved" };
                        println!("  entry {k}: kind {} flags {:#x} rights {:#x} principal {who}", e.flags & 0xf, e.flags, e.rights);
                    }
                }
            }
        }
    }
    println!("ledger used {:?}", ledger.used());
}
unsafe extern "C" { #[link_name = "geteuid"] fn libc_geteuid() -> u32; }
