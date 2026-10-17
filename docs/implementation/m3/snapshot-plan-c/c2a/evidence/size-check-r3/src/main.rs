// Scratch check (not product code): compare the C2a r3 descriptor-size formula with the real canonical encoder.
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes};
use std::collections::BTreeMap;
fn s(x: &str) -> V { V::String(x.to_owned()) }
fn n(x: i128) -> V { V::Integer(JsonInteger::new(x).unwrap()) }
fn p(x: &str) -> usize { canonical_bytes(&s(x)).unwrap().len() - 2 }
fn d(x: i128) -> usize { x.to_string().len() }
fn descriptor(kind: &str, platform: &str, major: i128, version: &str, tree: &[(&str, i128)]) -> V {
    let blobs = tree.iter().map(|(path, bytes)| V::Object(BTreeMap::from_iter([
        ("bytes".to_owned(), n(*bytes)), ("path".to_owned(), s(path)), ("sha256".to_owned(), s(&"a".repeat(64)))]))).collect();
    V::Object(BTreeMap::from_iter([
        ("schemaVersion".to_owned(), n(2)), ("kind".to_owned(), s(kind)), ("manifestDigest".to_owned(), s(&"b".repeat(64))),
        ("tree".to_owned(), V::Array(blobs)), ("semanticVersion".to_owned(), s(version)), ("protocolMajor".to_owned(), n(major)),
        ("platform".to_owned(), s(platform))]))
}
fn predicted(kind: &str, platform: &str, major: i128, version: &str, tree: &[(&str, i128)]) -> usize {
    175 + p(kind) + p(platform) + d(major) + p(version)
        + tree.iter().map(|(path, bytes)| 96 + d(*bytes) + p(path)).sum::<usize>() + tree.len().saturating_sub(1)
}
fn main() {
    let blob = V::Object(BTreeMap::from_iter([("bytes".to_owned(), n(0)), ("path".to_owned(), s("p")), ("sha256".to_owned(), s(&"a".repeat(64)))]));
    println!("blob bytes=0 path=p: {}", canonical_bytes(&blob).unwrap().len());
    let cases: Vec<(&str, &str, i128, &str, Vec<(&str, i128)>)> = vec![
        ("toolchain", "macos-arm64", 1, "1.0.0", vec![]),
        ("stdlib", "linux-x86_64", 9223372036854775807, "5.6.3", vec![("lib/lib.es2022.d.ts", 1234)]),
        ("provider", "macos-arm64", 3, "1.0.0", vec![("bin/entry", 91), ("lib/é\"q\\\n\u{1f}.js", 0), ("runtime/node", 33)]),
        ("grammar", "macos-x86_64", 1, "0.23.2-rc.1", vec![("a", 18446744073709551615), ("日本/語.wasm", 7)]),
    ];
    let mut ok = true;
    for (k, t, m, v, tree) in &cases {
        let enc = canonical_bytes(&descriptor(k, t, *m, v, tree)).unwrap().len();
        let pre = predicted(k, t, *m, v, tree);
        println!("{k} {t}: encoded {enc} predicted {pre}");
        ok &= enc == pre;
    }
    // A feasible byte boundary: grow a tree of fixed-size blobs until one more would exceed MAX_BYTES.
    let path = "lib/file-000000.d.ts"; let per = 96 + 4 + p(path) + 1;
    let base = predicted("stdlib", "macos-arm64", 1, "1.0.0", &[(path, 1000)]);
    let max_rows = 1 + (4 * 1024 * 1024 - base) / per;
    let paths: Vec<String> = (0..max_rows + 1).map(|i| format!("lib/file-{i:06}.d.ts")).collect();
    let tree: Vec<(&str, i128)> = paths.iter().map(|q| (q.as_str(), 1000)).collect();
    let at = canonical_bytes(&descriptor("stdlib", "macos-arm64", 1, "1.0.0", &tree[..max_rows]));
    let over = canonical_bytes(&descriptor("stdlib", "macos-arm64", 1, "1.0.0", &tree[..max_rows + 1]));
    println!("boundary rows {max_rows}: at {:?} over {:?}", at.as_ref().map(|b| b.len()), over.as_ref().map(|b| b.len()).err());
    println!("formula {}", if ok && at.is_ok() && over.is_err() { "MATCHES" } else { "MISMATCH" });
}
