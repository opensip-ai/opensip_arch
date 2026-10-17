// Scratch check (not product code): the member reach's directory-open charge is in UTF-8 bytes, and C1b plan r6's
// bound on a member path's name bytes (16,320) is attained by an admitted LogicalPath and never exceeded by the
// review's counterexample. Platform and identity are unchanged from product 813d559 in the C1b-1 worktree.
use opensip_identity::LogicalPath;
use opensip_platform::open_child_directory_cost;
use std::ffi::OsStr;
const OPEN_BASE: usize = 145; // the census's OPEN_DIR bytes: the NUL and the status buffer
const REACH_NAME_BYTES_MAX: usize = 16_320; // vcs_term_r6.output.json, reach.nameBytesMax
fn reach_bytes(path: &str) -> (usize, usize, usize) {
    let segments: Vec<&str> = path.split('/').collect();
    let charged: usize = segments.iter().map(|s| open_child_directory_cost(OsStr::new(s)).bytes).sum();
    let names: usize = segments.iter().map(|s| s.len()).sum();
    (segments.len(), charged, names)
}
fn main() {
    let wide = '\u{10000}';
    let mut ok = true;
    // The review's counterexample: 256 segments, 255 of 15 four-byte scalars and one of 16 (4,096 scalars).
    let mut parts: Vec<String> = (0..255).map(|_| std::iter::repeat_n(wide, 15).collect()).collect();
    parts.push(std::iter::repeat_n(wide, 16).collect());
    let review = parts.join("/");
    // r6's maximum: 16 segments of 255 four-byte scalars (4,080 scalars and 15 separators).
    let maximum = (0..16).map(|_| std::iter::repeat_n(wide, 255).collect::<String>()).collect::<Vec<_>>().join("/");
    // One more scalar anywhere is refused: a 17th segment exceeds 4,096 scalars, a longer segment exceeds 255.
    let over_segment = format!("{maximum}{wide}");
    for (name, path) in [("review counterexample", &review), ("r6 maximum", &maximum)] {
        let admitted = LogicalPath::parse(path).is_ok();
        let (segments, charged, names) = reach_bytes(path);
        let base = segments * OPEN_BASE;
        println!("{name}: scalars {} admitted {admitted} segments {segments} charged {charged} = {base} + names {names}",
                 path.chars().count());
        ok &= admitted && charged == base + names && names <= REACH_NAME_BYTES_MAX && segments <= 256;
    }
    let (_, _, max_names) = reach_bytes(&maximum);
    println!("maximum attained: {}", max_names == REACH_NAME_BYTES_MAX);
    println!("one scalar more in the last segment refused: {}", LogicalPath::parse(&over_segment).is_err());
    ok &= max_names == REACH_NAME_BYTES_MAX && LogicalPath::parse(&over_segment).is_err();
    println!("reach pricing {}", if ok { "MATCHES" } else { "MISMATCH" });
}
