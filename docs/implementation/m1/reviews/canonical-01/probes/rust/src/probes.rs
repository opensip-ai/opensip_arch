//! Independent reviewer probes. Expectations come from identity-and-evidence §3
//! text and literal bytes, not from the encoder under test.

use opensip_identity::canonical::{self, Error, Integer, MAX_BYTES, MAX_DEPTH, Value};
use opensip_identity::digest;
use std::alloc::{GlobalAlloc, Layout, System};
use std::collections::BTreeMap;
use std::sync::atomic::{AtomicUsize, Ordering::SeqCst};
use std::time::Instant;

struct Counting;
static CURRENT: AtomicUsize = AtomicUsize::new(0);
static PEAK: AtomicUsize = AtomicUsize::new(0);

fn grow(bytes: usize) {
    let now = CURRENT.fetch_add(bytes, SeqCst) + bytes;
    PEAK.fetch_max(now, SeqCst);
}

// SAFETY: every call forwards unchanged to the system allocator; only counters are added.
unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let ptr = unsafe { System.alloc(layout) };
        if !ptr.is_null() {
            grow(layout.size());
        }
        ptr
    }

    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        unsafe { System.dealloc(ptr, layout) };
        CURRENT.fetch_sub(layout.size(), SeqCst);
    }

    unsafe fn realloc(&self, ptr: *mut u8, layout: Layout, new_size: usize) -> *mut u8 {
        let new = unsafe { System.realloc(ptr, layout, new_size) };
        if !new.is_null() {
            if new_size >= layout.size() {
                grow(new_size - layout.size());
            } else {
                CURRENT.fetch_sub(layout.size() - new_size, SeqCst);
            }
        }
        new
    }
}

#[global_allocator]
static GLOBAL: Counting = Counting;

fn show(input: &[u8]) -> String {
    String::from_utf8_lossy(&input[..input.len().min(80)]).into_owned()
}

fn accept(input: &[u8]) -> Vec<u8> {
    let value = canonical::parse(input)
        .unwrap_or_else(|error| panic!("refused {:?}: {error:?}", show(input)));
    let bytes = canonical::encode(&value).expect("an admitted value encodes");
    let again = canonical::parse(&bytes).expect("canonical bytes re-admit");
    assert!(again == value, "re-admission changed the value");
    assert_eq!(canonical::encode(&again).unwrap(), bytes, "encoding is not idempotent");
    bytes
}

fn refuse(input: &[u8]) -> Error {
    match canonical::parse(input) {
        Ok(_) => panic!("accepted {:?}", show(input)),
        Err(error) => error,
    }
}

fn to_hex(bytes: &[u8]) -> String {
    bytes.iter().map(|byte| format!("{byte:02x}")).collect()
}

fn unhex(text: &str) -> Vec<u8> {
    (0..text.len())
        .step_by(2)
        .map(|index| u8::from_str_radix(&text[index..index + 2], 16).unwrap())
        .collect()
}

#[test]
fn key_order_is_utf8_bytes_across_widths_and_prefixes() {
    let input = "{\"\u{10000}\":0,\"\u{e000}\":1,\"\u{80}\":2,\"\u{7f}\":3,\"ab\":4,\"a\":5,\"\":6,\"B\":7}";
    let expected = "{\"\":6,\"B\":7,\"a\":5,\"ab\":4,\"\u{7f}\":3,\"\u{80}\":2,\"\u{e000}\":1,\"\u{10000}\":0}";
    assert_eq!(accept(input.as_bytes()), expected.as_bytes());
}

#[test]
fn every_c0_control_uses_the_contract_escape_in_values_and_keys() {
    let mut raw_text = String::new();
    let mut expected_body = String::new();
    for code in 0_u8..0x20 {
        raw_text.push(char::from(code));
        match code {
            0x08 => expected_body.push_str("\\b"),
            0x09 => expected_body.push_str("\\t"),
            0x0a => expected_body.push_str("\\n"),
            0x0c => expected_body.push_str("\\f"),
            0x0d => expected_body.push_str("\\r"),
            _ => expected_body.push_str(&format!("\\u{code:04x}")),
        }
    }
    raw_text.push_str("\"\\/\u{7f}\u{2028}");
    expected_body.push_str("\\\"\\\\/\u{7f}\u{2028}");
    let mut object = BTreeMap::new();
    object.insert(raw_text.clone(), Value::String(raw_text));
    let expected = format!("{{\"{expected_body}\":\"{expected_body}\"}}");
    let encoded = canonical::encode(&Value::Object(object)).unwrap();
    assert_eq!(encoded, expected.as_bytes());
    assert_eq!(accept(&encoded), encoded);
}

#[test]
fn escape_spellings_collapse_to_one_canonical_form() {
    assert_eq!(accept(br#""\u001F""#), br#""\u001f""#);
    assert_eq!(accept(br#""\u00E9""#), "\"é\"".as_bytes());
    assert_eq!(accept(br#""\uD834\uDD1E""#), "\"\u{1d11e}\"".as_bytes());
    assert_eq!(accept(br#""\u002F\/""#), br#""//""#);
    assert_eq!(accept(br#""\u0022\u005c""#), br#""\"\\""#);
    assert_eq!(accept(br#""\u0008\u000C""#), br#""\b\f""#);
}

#[test]
fn duplicate_keys_after_every_escape_spelling() {
    for input in [
        r#"{"/":1,"\/":2}"#,
        r#"{"A":1,"\u0041":2}"#,
        "{\"é\":1,\"\\u00E9\":2}",
        r#"{"\ud834\udd1e":1,"\uD834\uDD1E":2}"#,
        r#"{"":1,"":2}"#,
        r#"{"a":{"b":1},"b":2,"\u0061":3}"#,
    ] {
        assert_eq!(refuse(input.as_bytes()), Error::DuplicateKey, "{input}");
    }
    // Distinct scalar sequences that normalize together remain distinct keys.
    accept("{\"\u{212b}\":1,\"\u{c5}\":2,\"A\u{30a}\":3}".as_bytes());
}

#[test]
fn surrogate_and_escape_refusals() {
    for input in [
        r#""\ud800\ud800""#,
        r#""\udbff\udbff""#,
        r#""\udfff""#,
        r#""\ud800\n""#,
        r#"{"\ud800":1}"#,
        r#""\ud800 \udc00""#,
    ] {
        assert_eq!(refuse(input.as_bytes()), Error::InvalidUnicode, "{input}");
    }
    for input in [
        r#""\ud800\u12""#,
        r#""\ud800\"#,
        r#""\u12""#,
        r#""\u1_23""#,
        r#""\u+123""#,
        r#""\u 123""#,
        r#""\U0041""#,
        r#""\x41""#,
        r#""\'""#,
    ] {
        assert!(canonical::parse(input.as_bytes()).is_err(), "{input}");
    }
}

#[test]
fn raw_utf8_and_control_refusals() {
    let invalid_utf8: &[&[u8]] = &[
        b"\"\xf4\x90\x80\x80\"",
        b"\"\xc0\xaf\"",
        b"\"\xe0\x80\xaf\"",
        b"\"\xf0\x9f\x98\"",
        b"\x80",
    ];
    for input in invalid_utf8 {
        assert_eq!(refuse(input), Error::InvalidUtf8, "{input:?}");
    }
    let invalid_json: &[&[u8]] = &[
        b"\"\x00\"",
        b"\x00",
        b"\"\x1f\"",
        b"\xef\xbb\xbfnull",
        b"\x0c1",
        "\u{a0}1".as_bytes(),
        "1\u{a0}".as_bytes(),
        "\u{2028}1".as_bytes(),
    ];
    for input in invalid_json {
        assert_eq!(refuse(input), Error::InvalidJson, "{input:?}");
    }
    let text = "\"\u{7f}\u{2028}\u{2029}\u{feff}\u{fffe}\u{ffff}\u{10ffff}\"";
    assert_eq!(accept(text.as_bytes()), text.as_bytes());
}

#[test]
fn only_json_whitespace_is_insignificant() {
    assert_eq!(accept(b"\t\r\n [ \t1 \r\n, 2 ]\n"), b"[1,2]");
    assert_eq!(
        accept(b" {\r\"a\"\t:\n[ ] , \"b\" : { } } "),
        br#"{"a":[],"b":{}}"#
    );
}

#[test]
fn structural_refusals() {
    for input in [
        "nul", "nullx", "True", "FALSE", "NaN", "-NaN", "Infinity", "-Infinity", "1 x", "[] []",
        "\"\\", "\"abc", "[1,,2]", "{\"a\"}", "{\"a\":}", "{:1}", "{\"a\":1 \"b\":2}", "[1 2]",
        "{\"a\":1,}", "[,1]", "{,}", "]", "}", ":", ",", "'a'", "{'a':1}",
    ] {
        assert_eq!(refuse(input.as_bytes()), Error::InvalidJson, "{input}");
    }
}

#[test]
fn integer_lexical_edges() {
    let cases: &[(&str, Error)] = &[
        ("-", Error::InvalidJson),
        ("--1", Error::InvalidJson),
        ("00", Error::InvalidJson),
        ("0x10", Error::InvalidJson),
        ("1_000", Error::InvalidJson),
        ("+1", Error::InvalidJson),
        (".5", Error::InvalidJson),
        ("- 1", Error::InvalidJson),
        ("1.", Error::FloatForbidden),
        ("0e", Error::FloatForbidden),
        ("-0.0", Error::FloatForbidden),
        ("1e+5", Error::FloatForbidden),
        ("1E-5", Error::FloatForbidden),
        ("[-0]", Error::NegativeZero),
        ("{\"a\":-0}", Error::NegativeZero),
        ("-0 ", Error::NegativeZero),
        ("18446744073709551616", Error::IntegerRange),
        ("-9223372036854775809", Error::IntegerRange),
        ("170141183460469231731687303715884105727", Error::IntegerRange),
        ("-170141183460469231731687303715884105728", Error::IntegerRange),
        ("-170141183460469231731687303715884105729", Error::IntegerRange),
        ("340282366920938463463374607431768211456", Error::IntegerRange),
    ];
    for (input, expected) in cases {
        assert_eq!(refuse(input.as_bytes()), *expected, "{input}");
    }
    for (input, canonical_text) in [
        ("18446744073709551615", "18446744073709551615"),
        ("-9223372036854775808", "-9223372036854775808"),
        ("0", "0"),
        ("-1", "-1"),
        ("[ 10 , -10 ]", "[10,-10]"),
    ] {
        assert_eq!(accept(input.as_bytes()), canonical_text.as_bytes());
    }
    let mut long = vec![b'9'; MAX_BYTES];
    let started = Instant::now();
    assert_eq!(refuse(&long), Error::IntegerRange);
    long[0] = b'-';
    assert_eq!(refuse(&long), Error::IntegerRange);
    eprintln!("probe: two 4MiB digit-token refusals took {:?}", started.elapsed());
    assert!(matches!(canonical::parse(b"true").unwrap(), Value::Bool(true)));
    assert!(matches!(canonical::parse(b"\"1\"").unwrap(), Value::String(_)));
    assert_eq!(Integer::new(i128::from(u64::MAX)).unwrap().get(), i128::from(u64::MAX));
    assert_eq!(Integer::new(i128::from(i64::MIN)).unwrap().get(), i128::from(i64::MIN));
}

#[test]
fn mixed_depth_boundary_and_refusal_precedence() {
    let mut open = String::new();
    let mut close = String::new();
    for level in 0..MAX_DEPTH {
        if level % 2 == 0 {
            open.push('[');
            close.insert(0, ']');
        } else {
            open.push_str("{\"k\":");
            close.insert(0, '}');
        }
    }
    accept(format!("{open}0{close}").as_bytes());
    assert_eq!(refuse(format!("{open}[0]{close}").as_bytes()), Error::DepthLimit);
    assert_eq!(refuse(format!("{open}{{}}{close}").as_bytes()), Error::DepthLimit);
    assert_eq!(refuse("[".repeat(40).as_bytes()), Error::DepthLimit);
    let mut value = Value::Integer(Integer::new(0).unwrap());
    for _ in 0..MAX_DEPTH {
        let mut members = BTreeMap::new();
        members.insert(String::new(), value);
        value = Value::Object(members);
    }
    assert!(canonical::encode(&value).is_ok());
    let mut members = BTreeMap::new();
    members.insert(String::new(), value);
    assert_eq!(canonical::encode(&Value::Object(members)), Err(Error::DepthLimit));
}

#[test]
fn observed_refusal_precedence() {
    // The Python reference decodes values before its pairs hook; this parser checks the key first.
    assert_eq!(refuse(br#"{"a":1,"a":1.5}"#), Error::DuplicateKey);
    assert_eq!(refuse(br#"{"a":1.5,"a":1}"#), Error::FloatForbidden);
    let deep_float = format!("{}1.0{}", "[".repeat(33), "]".repeat(33));
    assert_eq!(refuse(deep_float.as_bytes()), Error::DepthLimit);
    assert_eq!(refuse(&vec![0xff_u8; MAX_BYTES + 1]), Error::ByteLimit);
}

#[test]
fn size_boundaries_and_shrinking_escapes() {
    let mut text = Vec::with_capacity(MAX_BYTES);
    text.push(b'"');
    text.resize(MAX_BYTES - 1, b'x');
    text.push(b'"');
    assert_eq!(accept(&text).len(), MAX_BYTES);
    let pairs = (MAX_BYTES - 2) / 2;
    let mut escaped = Vec::with_capacity(MAX_BYTES);
    escaped.push(b'"');
    for _ in 0..pairs {
        escaped.extend_from_slice(b"\\/");
    }
    escaped.push(b'"');
    assert!(escaped.len() <= MAX_BYTES);
    assert_eq!(accept(&escaped).len(), pairs + 2);
    let value = canonical::parse(&text).unwrap();
    let frame = digest::frame("a", &value).unwrap();
    assert_eq!(frame.len(), 19 + 1 + 1 + 8 + MAX_BYTES);
    assert_eq!(&frame[21..29], &(MAX_BYTES as u64).to_be_bytes());
}

#[test]
fn frame_length_is_uint64_big_endian_beyond_one_byte() {
    let value = Value::String("x".repeat(300));
    let frame = digest::frame("snapshot", &value).unwrap();
    let mut expected = b"opensip.product.v1\0snapshot\0".to_vec();
    expected.extend_from_slice(&[0, 0, 0, 0, 0, 0, 0x01, 0x2e]);
    expected.push(b'"');
    expected.extend(std::iter::repeat_n(b'x', 300));
    expected.push(b'"');
    assert_eq!(frame, expected);
    assert_eq!(digest::identity("snapshot", &value).unwrap(), digest::raw_sha256(&expected));
    for domain in [".", "-", "0", "a.b-c", "snapshot2"] {
        assert!(digest::frame(domain, &Value::Null).is_ok(), "{domain}");
    }
    for domain in ["a b", "a:b", "A", "\u{e9}", "a\0", " ", "a/b", "a_b"] {
        assert_eq!(
            digest::frame(domain, &Value::Null),
            Err(digest::Error::Domain),
            "{domain:?}"
        );
    }
    let mut deep = Value::Null;
    for _ in 0..=MAX_DEPTH {
        deep = Value::Array(vec![deep]);
    }
    assert_eq!(
        digest::frame("a", &deep),
        Err(digest::Error::Canonical(Error::DepthLimit))
    );
}

fn build(open: &[u8], item: &[u8], separator: &[u8], close: &[u8]) -> Vec<u8> {
    let mut out = open.to_vec();
    let mut first = true;
    while out.len() + separator.len() + item.len() + close.len() <= MAX_BYTES {
        if !first {
            out.extend_from_slice(separator);
        }
        out.extend_from_slice(item);
        first = false;
    }
    out.extend_from_slice(close);
    out
}

fn distinct_keys() -> Vec<u8> {
    const ALPHABET: &[u8] = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let mut out = b"{".to_vec();
    let mut index = 0_usize;
    while out.len() + 9 + 1 <= MAX_BYTES {
        if index != 0 {
            out.push(b',');
        }
        out.push(b'"');
        let mut rest = index;
        for _ in 0..4 {
            out.push(ALPHABET[rest % ALPHABET.len()]);
            rest /= ALPHABET.len();
        }
        out.extend_from_slice(b"\":0");
        index += 1;
    }
    out.push(b'}');
    out
}

#[test]
fn bounded_input_memory_and_time_amplification() {
    let shapes: Vec<(&str, Vec<u8>)> = vec![
        ("integers", build(b"[", b"0", b",", b"]")),
        ("empty-arrays", build(b"[", b"[]", b",", b"]")),
        ("empty-objects", build(b"[", b"{}", b",", b"]")),
        ("one-char-strings", build(b"[", b"\"a\"", b",", b"]")),
        ("distinct-keys", distinct_keys()),
    ];
    for (name, input) in shapes {
        assert!(input.len() <= MAX_BYTES, "{name}");
        let base = CURRENT.load(SeqCst);
        PEAK.store(base, SeqCst);
        let started = Instant::now();
        let value = canonical::parse(&input).expect(name);
        let parse_time = started.elapsed();
        let parse_peak = PEAK.load(SeqCst) - base;
        let started = Instant::now();
        let encoded = canonical::encode(&value).expect(name);
        let encode_time = started.elapsed();
        let total_peak = PEAK.load(SeqCst) - base;
        eprintln!(
            "probe-amplification {name}: inputBytes={} parsePeakBytes={parse_peak} ratio={:.1} totalPeakBytes={total_peak} parse={parse_time:?} encode={encode_time:?} encodedBytes={}",
            input.len(),
            parse_peak as f64 / input.len() as f64,
            encoded.len()
        );
    }
}

#[test]
fn differential_outcomes_for_reference_comparison() {
    let Ok(corpus_path) = std::env::var("PROBE_CORPUS") else {
        eprintln!("probe: PROBE_CORPUS unset; differential outcomes NOT produced");
        return;
    };
    let out_path = std::env::var("PROBE_OUT").expect("PROBE_OUT is required with PROBE_CORPUS");
    let text = std::fs::read_to_string(corpus_path).unwrap();
    let mut lines: Vec<&str> = text.split('\n').collect();
    assert_eq!(lines.pop(), Some(""));
    let mut out = String::new();
    for line in lines {
        let input = unhex(line);
        let outcome = std::panic::catch_unwind(|| match canonical::parse(&input) {
            Ok(value) => {
                let bytes = canonical::encode(&value).expect("admitted value must encode");
                let again = canonical::parse(&bytes).expect("canonical bytes must re-admit");
                assert!(again == value, "re-admission changed the value");
                format!("ACCEPT {}", to_hex(&bytes))
            }
            Err(error) => format!("REFUSE {error:?}"),
        });
        out.push_str(&outcome.unwrap_or_else(|_| String::from("PANIC")));
        out.push('\n');
    }
    std::fs::write(out_path, out).unwrap();
}
