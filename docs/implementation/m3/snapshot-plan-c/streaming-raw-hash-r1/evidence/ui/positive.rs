use opensip_identity::RawSha256; fn main() { let h=RawSha256::new().update(b"a").unwrap().update(b"bc").unwrap(); assert_eq!(h.byte_length(),3); let _digest=h.finish(); }
