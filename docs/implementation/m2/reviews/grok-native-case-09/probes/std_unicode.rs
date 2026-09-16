fn main() {
    for c in ['\u{1c89}', '\u{a7cb}', '\u{10d50}', '\u{10400}', '\u{0130}', '\u{00df}'] {
        let ours = c.to_string();
        let std = ours.to_lowercase();
        println!("{:04X} std={:?} identity={}", c as u32, std, std == ours);
    }
}
