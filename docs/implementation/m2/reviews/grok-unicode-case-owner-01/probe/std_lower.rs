fn main() {
    let cases: &[(&str, &str)] = &[
        ("ES2022", "es2022"),
        ("dom", "dom"),
        ("\u{0130}", "i\u{0307}"),
        ("\u{00DF}", "\u{00DF}"),
        ("\u{03A3}", "\u{03C3}"),
        ("\u{0391}\u{03A3}", "\u{03B1}\u{03C2}"),
        ("\u{03A3}\u{0391}", "\u{03C3}\u{03B1}"),
        ("\u{039F}\u{03A3}.", "\u{03BF}\u{03C2}."),
        ("I", "i"),
        ("\u{0130}stanbul", "i\u{0307}stanbul"),
    ];
    println!("note=char::to_lowercase is per-scalar; str::to_lowercase is context-sensitive");
    for (src, py_want) in cases {
        let via_str: String = src.to_lowercase();
        let via_char: String = src.chars().flat_map(|c| c.to_lowercase()).collect();
        println!(
            "CASE src={:?} str_lower={:?} char_lower={:?} py_want={:?} str_eq_want={} char_eq_str={}",
            src.escape_unicode(),
            via_str.escape_unicode(),
            via_char.escape_unicode(),
            py_want.escape_unicode(),
            via_str == *py_want,
            via_char == via_str
        );
    }
}
