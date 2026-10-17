// Scratch check (not product code): compare the C1b plan r5 VCS-record size formula with the real canonical encoder,
// and admit the maximal schema-3 record under the identity registry. Product base caa71e2 (crates/identity unchanged
// in the C1b-1 worktree). Usage: c1b-record-size-check <product root>.
use opensip_identity::{JsonInteger, JsonValue as V, LogicalPath, RegisteredSchemas, canonical_bytes};
use std::collections::BTreeMap;
fn s(x: &str) -> V { V::String(x.to_owned()) }
fn n(x: i128) -> V { V::Integer(JsonInteger::new(x).unwrap()) }
fn obj(fields: Vec<(&str, V)>) -> V { V::Object(fields.into_iter().map(|(k, v)| (k.to_owned(), v)).collect::<BTreeMap<_, _>>()) }
/// e(P): the canonical encoding's payload, quotes excluded, computed by the plan's rule (not by the encoder).
fn e(p: &str) -> usize {
    p.chars().map(|c| match c {
        '"' | '\\' | '\u{8}' | '\u{c}' | '\n' | '\r' | '\t' => 2,
        '\0'..='\u{1f}' => 6,
        c => c.len_utf8(),
    }).sum()
}
const COMMIT: &str = "0123456789abcdef0123456789abcdef01234567";
const DIGEST: &str = "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210";
// The plan's fixed parts (r5, LD-C1B-6).
const TOP3: usize = r#"{"commitId":null,"dirty":false,"kind":"none","members":["#.len() + r#"],"schemaVersion":3,"sourceInventoryDigest":""#.len() + 64 + r#""}"#.len();
const MEMBER: usize = r#"{"commitId":""#.len() + 40 + r#"","dirty":true,"kind":"git","path":""#.len() + r#""}"#.len();
const GIT2: usize = r#"{"commitId":""#.len() + 40 + r#"","dirty":true,"kind":"git","schemaVersion":2,"sourceInventoryDigest":""#.len() + 64 + r#""}"#.len();
const NONE2: usize = r#"{"commitId":null,"dirty":false,"kind":"none","schemaVersion":2,"sourceInventoryDigest":""#.len() + 64 + r#""}"#.len();
fn predicted3(paths: &[String]) -> usize { TOP3 + paths.iter().map(|p| MEMBER + e(p)).sum::<usize>() + paths.len() - 1 }
fn record3(paths: &[String]) -> V {
    let members = paths.iter().map(|p| obj(vec![("commitId", s(COMMIT)), ("dirty", V::Bool(true)), ("kind", s("git")), ("path", s(p))])).collect();
    obj(vec![("schemaVersion", n(3)), ("kind", s("none")), ("commitId", V::Null), ("dirty", V::Bool(false)),
             ("sourceInventoryDigest", s(DIGEST)), ("members", V::Array(members))])
}
fn main() {
    let root = std::path::PathBuf::from(std::env::args().nth(1).expect("product root"));
    let mut ok = true;
    let git2 = obj(vec![("schemaVersion", n(2)), ("kind", s("git")), ("commitId", s(COMMIT)), ("dirty", V::Bool(true)), ("sourceInventoryDigest", s(DIGEST))]);
    let none2 = obj(vec![("schemaVersion", n(2)), ("kind", s("none")), ("commitId", V::Null), ("dirty", V::Bool(false)), ("sourceInventoryDigest", s(DIGEST))]);
    for (name, value, fixed) in [("schema-2 git", &git2, GIT2), ("schema-2 none", &none2, NONE2)] {
        let enc = canonical_bytes(value).unwrap().len();
        println!("{name}: encoded {enc} predicted {fixed}");
        ok &= enc == fixed;
    }
    println!("fixed: TOP3 {TOP3} MEMBER {MEMBER} GIT2 {GIT2} NONE2 {NONE2}");
    // Every escape class, DEL, C1 and non-ASCII widths.
    let cases: Vec<Vec<String>> = vec![
        vec!["a".into()],
        vec!["crates/a".into(), "crates/b\"q".into()],
        vec!["x\u{8}\u{c}\n\r\t".into(), "y\u{1}\u{1f}\u{7f}\u{85}".into(), "z/é/日本/𝄞".into()],
    ];
    for paths in &cases {
        for p in paths { assert!(LogicalPath::parse(p).is_ok(), "{p:?}"); }
        let enc = canonical_bytes(&record3(paths)).unwrap().len();
        let pre = predicted3(paths);
        println!("schema-3 {} members: encoded {enc} predicted {pre}", paths.len());
        ok &= enc == pre;
    }
    // The maximum: 64 distinct paths, each 4,096 scalars in 17 segments (15 of 255, then 128 and 127) of six-byte
    // controls, so 4,080 controls and 16 separators: e(P) = 24,496.
    let six: Vec<char> = (1u8..0x20).map(char::from).filter(|c| !matches!(c, '\u{8}' | '\u{c}' | '\n' | '\r' | '\t')).collect();
    let mut paths: Vec<String> = (0..64usize).map(|i| {
        let fill = six[i % six.len()];
        let mark = six[(i / six.len()) % six.len()];
        let mut segments: Vec<String> = (0..15).map(|_| std::iter::repeat_n(fill, 255).collect()).collect();
        segments.push(std::iter::once(mark).chain(std::iter::repeat_n(fill, 127)).collect());
        segments.push(std::iter::repeat_n(fill, 127).collect());
        segments.join("/")
    }).collect();
    paths.sort();
    paths.dedup();
    assert_eq!(paths.len(), 64);
    for p in &paths {
        assert!(LogicalPath::parse(p).is_ok());
        assert_eq!(p.chars().count(), 4096);
        assert_eq!(e(p), 24_496);
    }
    let raw = canonical_bytes(&record3(&paths)).unwrap();
    let pre = predicted3(&paths);
    println!("schema-3 maximum: encoded {} predicted {pre}", raw.len());
    ok &= raw.len() == pre;
    // Admitted by the identity registry as a vcs-observation.
    let sources: Vec<Vec<u8>> = RegisteredSchemas::source_requirements().iter().map(|pin| std::fs::read(root.join(pin.source_path())).unwrap()).collect();
    let refs: Vec<&[u8]> = sources.iter().map(Vec::as_slice).collect();
    let registry = RegisteredSchemas::from_sources(&refs).unwrap();
    let admitted = registry.schema("urn:opensip:product-v1:identity:v3", "/$defs/vcs-observation").unwrap().admit_json(&raw, 64 << 20).is_ok();
    println!("schema-3 maximum admitted as vcs-observation: {admitted}");
    // One scalar more in any path is not a LogicalPath.
    let longer = format!("{}\u{1}", paths[0]);
    println!("4,097 scalars refused by LogicalPath: {}", LogicalPath::parse(&longer).is_err());
    ok &= admitted && LogicalPath::parse(&longer).is_err();
    println!("formula {}", if ok { "MATCHES" } else { "MISMATCH" });
}
