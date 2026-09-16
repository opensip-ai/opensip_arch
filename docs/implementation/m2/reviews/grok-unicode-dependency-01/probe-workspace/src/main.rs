//! Private NFC probe harness. Std only to print; crate is default-features=false.
use unicode_nfc_probe::{nfc, UNICODE_VERSION};

fn main() {
    let cases: &[(&str, &str, &str)] = &[
        ("e_acute_nfd", "e\u{0301}", "é"),
        ("e_acute_nfc", "é", "é"),
        ("angstrom_compat", "\u{212B}", "Å"),
        ("a_ring_nfd", "A\u{030A}", "Å"),
        ("a_ring_nfc", "Å", "Å"),
        ("hangul_syllable", "가", "가"),
        ("hangul_jamo", "\u{1100}\u{1161}", "가"),
        ("ascii_e", "e", "e"),
        ("empty", "", ""),
        ("omega_ohm", "\u{2126}", "Ω"),
        ("combining_reorder", "a\u{0316}\u{0301}", "á\u{0316}"),
        ("todhri_105d2_dot", "\u{105D2}\u{0307}", "\u{105C9}"),
        ("todhri_105da_dot", "\u{105DA}\u{0307}", "\u{105E4}"),
        ("tulu_113c2_113c2", "\u{113C2}\u{113C2}", "\u{113C5}"),
        ("tulu_113c2_113b8", "\u{113C2}\u{113B8}", "\u{113C7}"),
        ("tulu_113c2_113c9", "\u{113C2}\u{113C9}", "\u{113C8}"),
        ("tulu_11382_113c9", "\u{11382}\u{113C9}", "\u{11383}"),
        ("tulu_11384_113bb", "\u{11384}\u{113BB}", "\u{11385}"),
        ("tulu_1138b_113c2", "\u{1138B}\u{113C2}", "\u{1138E}"),
        ("tulu_11390_113c9", "\u{11390}\u{113C9}", "\u{11391}"),
        ("gurung_1611e_1611e", "\u{1611E}\u{1611E}", "\u{16121}"),
        ("gurung_1611e_1611f", "\u{1611E}\u{1611F}", "\u{16123}"),
        ("gurung_1611e_16120", "\u{1611E}\u{16120}", "\u{16125}"),
        ("gurung_1611e_16129", "\u{1611E}\u{16129}", "\u{16122}"),
        ("gurung_16121_1611f", "\u{16121}\u{1611F}", "\u{16126}"),
        ("gurung_16121_16120", "\u{16121}\u{16120}", "\u{16128}"),
        ("gurung_16122_1611f", "\u{16122}\u{1611F}", "\u{16127}"),
        ("gurung_16129_1611f", "\u{16129}\u{1611F}", "\u{16124}"),
        ("kirat_16d67_16d67", "\u{16D67}\u{16D67}", "\u{16D68}"),
        ("kirat_16d63_16d67", "\u{16D63}\u{16D67}", "\u{16D69}"),
        ("kirat_16d69_16d67", "\u{16D69}\u{16D67}", "\u{16D6A}"),
    ];
    println!("UNICODE_VERSION={}.{}.{}", UNICODE_VERSION.0, UNICODE_VERSION.1, UNICODE_VERSION.2);
    for (id, src, want) in cases {
        let got = nfc(src);
        println!(
            "CASE\tid={}\tmatch={}\talready_nfc={}\tsrc={}\tgot={}\twant={}",
            id,
            got == *want,
            nfc(want) == *want,
            src.escape_unicode(),
            got.escape_unicode(),
            want.escape_unicode()
        );
    }
}
