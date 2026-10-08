use opensip_identity::RawSha256; fn main() { let h=RawSha256::new(); let _result=h.update(b"data"); let _digest=h.finish(); }
