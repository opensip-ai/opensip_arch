// Scratch check (not product code) for C2a plan r4:
// RF-1: count the real encoder's allocations (integer temporaries plus output growth) and show that an
//       exact-capacity hand encoder (C1a3's pattern) allocates exactly once, with output equal to canonical_bytes.
// RF-2: a bottom-up merge sort charging one unit per comparison never exceeds n*ceil(log2 n), on reverse,
//       sorted, random and adversarial inputs.
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes};
use std::alloc::{GlobalAlloc, Layout, System};
use std::collections::BTreeMap;
use std::sync::atomic::{AtomicUsize, Ordering::Relaxed};
struct Counting;
static ALLOCS: AtomicUsize = AtomicUsize::new(0);
unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 { ALLOCS.fetch_add(1, Relaxed); unsafe { System.alloc(l) } }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) { unsafe { System.dealloc(p, l) } }
    unsafe fn realloc(&self, p: *mut u8, l: Layout, n: usize) -> *mut u8 { ALLOCS.fetch_add(1, Relaxed); unsafe { System.realloc(p, l, n) } }
}
#[global_allocator]
static A: Counting = Counting;
fn s(x: &str) -> V { V::String(x.to_owned()) }
fn n(x: i128) -> V { V::Integer(JsonInteger::new(x).unwrap()) }
fn e(x: &str) -> usize { x.chars().map(|c| match c { '"' | '\\' | '\u{8}' | '\u{c}' | '\n' | '\r' | '\t' => 2, '\0'..='\u{1f}' => 6, _ => c.len_utf8() }).sum() }
fn d(mut x: u128) -> usize { let mut k = 1; while x >= 10 { x /= 10; k += 1; } k }
fn push_str(out: &mut Vec<u8>, x: &str) {
    out.push(b'"');
    for c in x.chars() { match c {
        '"' => out.extend_from_slice(b"\\\""), '\\' => out.extend_from_slice(b"\\\\"),
        '\u{8}' => out.extend_from_slice(b"\\b"), '\u{c}' => out.extend_from_slice(b"\\f"),
        '\n' => out.extend_from_slice(b"\\n"), '\r' => out.extend_from_slice(b"\\r"), '\t' => out.extend_from_slice(b"\\t"),
        '\0'..='\u{1f}' => { const H: &[u8] = b"0123456789abcdef"; let b = c as u8; out.extend_from_slice(&[b'\\', b'u', b'0', b'0', H[(b >> 4) as usize], H[(b & 15) as usize]]); }
        _ => out.extend_from_slice(c.encode_utf8(&mut [0; 4]).as_bytes()) } }
    out.push(b'"');
}
fn push_dec(out: &mut Vec<u8>, mut x: u128) { let mut b = [0u8; 39]; let mut at = 39; loop { at -= 1; b[at] = b'0' + (x % 10) as u8; x /= 10; if x == 0 { break; } } out.extend_from_slice(&b[at..]); }
struct Desc<'a> { kind: &'a str, platform: &'a str, major: u128, version: &'a str, digest: &'a str, tree: &'a [(&'a str, u128, &'a str)] }
fn predicted(x: &Desc) -> usize { 175 + e(x.kind) + e(x.platform) + d(x.major) + e(x.version) + x.tree.iter().map(|(p, b, _)| 96 + d(*b) + e(p)).sum::<usize>() + x.tree.len().saturating_sub(1) }
fn hand(x: &Desc) -> Vec<u8> {
    let mut o = Vec::with_capacity(predicted(x));
    o.extend_from_slice(b"{\"kind\":"); push_str(&mut o, x.kind);
    o.extend_from_slice(b",\"manifestDigest\":"); push_str(&mut o, x.digest);
    o.extend_from_slice(b",\"platform\":"); push_str(&mut o, x.platform);
    o.extend_from_slice(b",\"protocolMajor\":"); push_dec(&mut o, x.major);
    o.extend_from_slice(b",\"schemaVersion\":2,\"semanticVersion\":"); push_str(&mut o, x.version);
    o.extend_from_slice(b",\"tree\":[");
    for (i, (p, b, h)) in x.tree.iter().enumerate() { if i > 0 { o.push(b','); }
        o.extend_from_slice(b"{\"bytes\":"); push_dec(&mut o, *b); o.extend_from_slice(b",\"path\":"); push_str(&mut o, p);
        o.extend_from_slice(b",\"sha256\":"); push_str(&mut o, h); o.push(b'}'); }
    o.extend_from_slice(b"]}"); o
}
fn value(x: &Desc) -> V {
    let tree = x.tree.iter().map(|(p, b, h)| V::Object(BTreeMap::from_iter([("bytes".into(), n(*b as i128)), ("path".into(), s(p)), ("sha256".into(), s(h))]))).collect();
    V::Object(BTreeMap::from_iter([("kind".into(), s(x.kind)), ("manifestDigest".into(), s(x.digest)), ("platform".into(), s(x.platform)),
        ("protocolMajor".into(), n(x.major as i128)), ("schemaVersion".into(), n(2)), ("semanticVersion".into(), s(x.version)), ("tree".into(), V::Array(tree))]))
}
// Bottom-up merge sort over indices; `charge` is called once before each comparison.
fn merge_sort(keys: &[&[u8]], charge: &mut dyn FnMut() -> bool) -> Option<Vec<usize>> {
    let n = keys.len(); let mut a: Vec<usize> = (0..n).collect(); let mut b = vec![0usize; n]; let mut w = 1;
    while w < n { let mut lo = 0; while lo < n { let mid = (lo + w).min(n); let hi = (lo + 2 * w).min(n); let (mut i, mut j, mut k) = (lo, mid, lo);
        while i < mid && j < hi { if !charge() { return None; } if keys[a[j]] < keys[a[i]] { b[k] = a[j]; j += 1; } else { b[k] = a[i]; i += 1; } k += 1; }
        while i < mid { b[k] = a[i]; i += 1; k += 1; } while j < hi { b[k] = a[j]; j += 1; k += 1; } lo = hi; }
        std::mem::swap(&mut a, &mut b); w *= 2; }
    Some(a)
}
fn bound(n: usize) -> usize { if n < 2 { 0 } else { n * (usize::BITS - (n - 1).leading_zeros()) as usize } }
fn main() {
    let h = "a".repeat(64); let g = "b".repeat(64);
    let tree: Vec<(&str, u128, &str)> = vec![("a", 0, &h), ("lib/é\"q\\\n\u{1f}.js", 18446744073709551615, &h), ("日本/語.wasm", 123456789012, &h), ("z", 7, &h)];
    let x = Desc { kind: "provider", platform: "macos-arm64", major: 9223372036854775807, version: "1.0.0-rc.1", digest: &g, tree: &tree };
    let v = value(&x);
    let before = ALLOCS.load(Relaxed); let canon = canonical_bytes(&v).unwrap(); let canon_allocs = ALLOCS.load(Relaxed) - before;
    let before = ALLOCS.load(Relaxed); let mine = hand(&x); let hand_allocs = ALLOCS.load(Relaxed) - before;
    println!("RF-1: canonical_bytes allocations {canon_allocs} (integers in descriptor: {}); hand encoder allocations {hand_allocs}; equal {}; len {} predicted {} capacity {}",
        tree.len() + 2, canon == mine, mine.len(), predicted(&x), mine.capacity());
    let mut ok = canon == mine && hand_allocs == 1 && mine.capacity() == predicted(&x);
    let mut worst = 0usize;
    for size in [2usize, 3, 7, 20, 21, 33, 64, 100, 1000, 4097] {
        let mk = |f: &dyn Fn(usize) -> usize| -> Vec<Vec<u8>> { (0..size).map(|i| format!("p{:06}", f(i)).into_bytes()).collect() };
        let orders: Vec<(&str, Vec<Vec<u8>>)> = vec![("reverse", mk(&|i| size - i)), ("sorted", mk(&|i| i)),
            ("interleave", mk(&|i| if i % 2 == 0 { i } else { size + i })), ("random", mk(&|i| (i * 7919 + 13) % (size * 3)))];
        for (name, keys) in orders {
            let refs: Vec<&[u8]> = keys.iter().map(|k| k.as_slice()).collect(); let mut c = 0usize;
            let out = merge_sort(&refs, &mut || { c += 1; true }).unwrap();
            let sorted = out.windows(2).all(|w| refs[w[0]] <= refs[w[1]]);
            ok &= sorted && c <= bound(size); worst = worst.max(c);
            if size == 20 && name == "reverse" { println!("RF-2: reverse 20: comparisons {c} bound {}", bound(20)); }
            // a scope that can fund only the r3 estimate stops before an unfunded comparison
            let est = size * (usize::BITS - size.leading_zeros()) as usize; let mut paid = 0usize;
            let stopped = merge_sort(&refs, &mut || { if paid == est.min(c.saturating_sub(1)) { return false; } paid += 1; true }).is_none();
            ok &= c == 0 || stopped;
        }
    }
    println!("RF-2: all orders sorted and within n*ceil(log2 n); max comparisons seen {worst}");
    println!("result {}", if ok { "PASS" } else { "FAIL" });
}
