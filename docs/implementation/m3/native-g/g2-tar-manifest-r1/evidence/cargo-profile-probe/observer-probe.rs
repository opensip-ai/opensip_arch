use std::collections::BTreeMap;
include!("observer-fragment.rs");
fn main() {
 let data=std::fs::read(std::env::args().nth(1).unwrap()).unwrap();
 let members=observe_declared_tar_members("opensip-profile-fixture","0.1.0",&data).unwrap();
 assert!(members.iter().any(|m| m.path().contains("é")));
 assert!(members.iter().any(|m| m.path().contains(&"a".repeat(120))));
 for member in &members { println!("{} {}", member.path(), member.content().len()); }
}
