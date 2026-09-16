//! Unicode 15.0.0 FULL default lowercase. No casefold, tailoring or NFC step.
//! Source strings, not partially transformed strings, determine Final_Sigma.
use alloc::{string::String, vec::Vec};
#[path = "generated/unicode_case_tables.rs"]
mod tables;
const REQUIRED_VERSION: (u8, u8, u8) = (15, 0, 0);

#[derive(Debug, PartialEq, Eq)]
pub struct CaseDataUnavailable;

fn member(c: char, ranges: &[(u32, u32)]) -> bool {
    let c = c as u32;
    let at = ranges.partition_point(|&(start, _)| start <= c);
    at > 0 && c <= ranges[at - 1].1
}
fn cased(c: char) -> bool {
    member(c, tables::CASED)
}
fn ignorable(c: char) -> bool {
    member(c, tables::CASE_IGNORABLE)
}

pub fn lowercase(input: &str) -> Result<String, CaseDataUnavailable> {
    if tables::VERSION != REQUIRED_VERSION {
        return Err(CaseDataUnavailable);
    }
    let chars: Vec<char> = input.chars().collect();
    // One reverse pass computes the following non-ignorable character's Cased
    // property. Ignore has precedence for characters in BOTH properties.
    let mut following = alloc::vec![false;chars.len()];
    let mut next = false;
    for (i, &c) in chars.iter().enumerate().rev() {
        following[i] = next;
        if !ignorable(c) {
            next = cased(c);
        }
    }
    let mut before = false;
    let mut out = String::with_capacity(input.len());
    for (i, &c) in chars.iter().enumerate() {
        if c == '\u{3a3}' && before && !following[i] {
            out.push('\u{3c2}');
        } else if let Ok(row) = tables::LOWER.binary_search_by_key(&(c as u32), |&(code, _)| code) {
            out.push_str(tables::LOWER[row].1);
        } else {
            out.push(c);
        }
        if !ignorable(c) {
            before = cased(c);
        }
    }
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn full_default_case_is_context_sensitive_and_not_casefold() {
        for (a, b) in [
            ("ES2022", "es2022"),
            ("İ", "i\u{307}"),
            ("ß", "ß"),
            ("I", "i"),
            ("ΑΣ", "ας"),
            ("ΣΑ", "σα"),
            ("Σ", "σ"),
            ("ΟΣ.", "ος."),
            ("I\u{307}", "i\u{307}"),
            ("AΣ\u{345}", "aς\u{345}"),
            ("AΣ\u{345}A", "aσ\u{345}a"),
        ] {
            assert_eq!(lowercase(a).unwrap(), b);
        }
    }
    #[test]
    fn new_assignments_do_not_inherit_rust_toolchain_case_tables() {
        // Unicode16/17-added Cyrillic/Latin capitals are unassigned in UCD15.
        for c in ['\u{1c89}', '\u{a7cb}', '\u{10d50}'] {
            let s = String::from(c);
            assert_eq!(lowercase(&s).unwrap(), s);
        }
        assert_eq!(lowercase("\u{10400}").unwrap(), "\u{10428}");
    }
}
