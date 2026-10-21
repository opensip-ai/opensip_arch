use super::*;
use opensip_identity::{JsonValue as J, parse_json};

const DIFFERENTIAL: &[u8] = include_bytes!("../../tests/data/cbor-differential.v1.json");
const DEEP: usize = 64;

fn text(s: &str) -> Vec<u8> {
    encode(&Value::Text(s.to_owned()))
}
fn refusal(data: &[u8], profile: Profile) -> &'static str {
    decode(data, profile, DEEP).expect_err("refused").code()
}
fn both(data: &[u8]) -> [Result<Value, CborRefusal>; 2] {
    [
        decode(data, Profile::Ts2, DEEP),
        decode(data, Profile::Rust3, DEEP),
    ]
}
fn hex(s: &str) -> Vec<u8> {
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap())
        .collect()
}

/// The reference's decoder probes (trial 07 `check_reference.py`
/// `wire_examples`), each with its profile and code.
#[test]
fn reference_probes_refuse_with_the_reference_codes() {
    let chunk = |index: Value| {
        Value::Map(vec![
            ("snapshotId".to_owned(), Value::Text("s".to_owned())),
            ("path".to_owned(), Value::Text("src/a.ts".to_owned())),
            ("chunkIndex".to_owned(), index),
            ("byteOffset".to_owned(), Value::Unsigned(0)),
            ("bytes".to_owned(), Value::Bytes(b"abc".to_vec())),
        ])
    };
    let negative = encode(&chunk(Value::Negative(-1)));
    let decoded = decode(&negative, Profile::Ts2, DEEP).unwrap();
    assert_eq!(encode(&decoded), negative);
    assert_eq!(
        refusal(&negative, Profile::Rust3),
        "NEGATIVE_INTEGER_FORBIDDEN"
    );
    let positive = encode(&chunk(Value::Unsigned(0)));
    for result in both(&positive) {
        assert_eq!(encode(&result.unwrap()), positive);
    }

    let one = encode(&Value::Unsigned(1));
    let map2 = |a: &str, b: &str| [&[0xa2][..], &text(a), &one, &text(b), &one].concat();
    assert_eq!(refusal(b"\x18\x05", Profile::Rust3), "NON_SHORTEST");
    assert_eq!(refusal(&map2("b", "a"), Profile::Ts2), "MAP_ORDER");
    assert_eq!(refusal(&map2("aa", "b"), Profile::Rust3), "MAP_ORDER");
    assert_eq!(refusal(&map2("a", "a"), Profile::Ts2), "DUPLICATE_KEY");
    assert_eq!(refusal(b"\xf9\x00\x00", Profile::Ts2), "FLOAT_OR_SIMPLE");
    assert_eq!(refusal(b"\xc0\x60", Profile::Rust3), "TAG");
    assert_eq!(refusal(b"\x5f\xff", Profile::Ts2), "INDEFINITE_OR_RESERVED");
    assert_eq!(refusal(&text("e\u{301}"), Profile::Rust3), "NON_NFC");
}

#[test]
fn every_wider_head_is_non_shortest() {
    for (n, shortest) in [
        (0u64, 1usize),
        (23, 1),
        (24, 2),
        (255, 2),
        (256, 3),
        (65535, 3),
        (65536, 5),
        ((1 << 32) - 1, 5),
        (1 << 32, 9),
        (u64::MAX, 9),
    ] {
        let canonical = encode(&Value::Unsigned(n));
        assert_eq!(canonical.len(), shortest);
        for result in both(&canonical) {
            assert_eq!(result.unwrap(), Value::Unsigned(n));
        }
        for (ai, size) in [(24u8, 1usize), (25, 2), (26, 4), (27, 8)] {
            if size < shortest || (size < 8 && n >= 1 << (8 * size)) {
                continue;
            }
            let wide = [&[ai][..], &n.to_be_bytes()[8 - size..]].concat();
            for result in both(&wide) {
                assert_eq!(
                    result.unwrap_err(),
                    CborRefusal::NonShortest,
                    "{n} in {size}"
                );
            }
        }
    }
    // Lengths are arguments too.
    assert_eq!(refusal(b"\x78\x01a", Profile::Ts2), "NON_SHORTEST");
    assert_eq!(refusal(b"\x98\x00", Profile::Rust3), "NON_SHORTEST");
}

#[test]
fn negative_integers_follow_the_profile() {
    for n in [-1i64, -24, -25, -256, -257, i64::MIN] {
        let bytes = encode(&Value::Negative(n));
        assert_eq!(
            decode(&bytes, Profile::Ts2, DEEP).unwrap(),
            Value::Negative(n)
        );
        assert_eq!(
            refusal(&bytes, Profile::Rust3),
            "NEGATIVE_INTEGER_FORBIDDEN"
        );
    }
    // -2^63 - 1 is outside int64.
    let below = b"\x3b\x80\x00\x00\x00\x00\x00\x00\x00";
    assert_eq!(refusal(below, Profile::Ts2), "INT_RANGE");
    assert_eq!(refusal(below, Profile::Rust3), "NEGATIVE_INTEGER_FORBIDDEN");
}

#[test]
fn closed_forms_refuse() {
    for (bytes, code) in [
        (&b"\xf7"[..], "FLOAT_OR_SIMPLE"),
        (b"\xe0", "FLOAT_OR_SIMPLE"),
        (b"\xf8\x20", "FLOAT_OR_SIMPLE"),
        (b"\xfa\x00\x00\x00\x00", "FLOAT_OR_SIMPLE"),
        (b"\xfb\x00\x00\x00\x00\x00\x00\x00\x00", "FLOAT_OR_SIMPLE"),
        (b"\xff", "FLOAT_OR_SIMPLE"),
        (b"\xd8\x18\x00", "TAG"),
        (b"\x9f\xff", "INDEFINITE_OR_RESERVED"),
        (b"\xbf\xff", "INDEFINITE_OR_RESERVED"),
        (b"\x7f\xff", "INDEFINITE_OR_RESERVED"),
        (b"\x1c", "INDEFINITE_OR_RESERVED"),
        (b"\x1d", "INDEFINITE_OR_RESERVED"),
        (b"\x1e", "INDEFINITE_OR_RESERVED"),
        (b"\xa1\x01\x01", "NON_TEXT_KEY"),
        (b"\xa1\x41a\x01", "NON_TEXT_KEY"),
        (b"\xa1\x80\x01", "NON_TEXT_KEY"),
        (b"\x62\xc3\x28", "INVALID_UTF8"),
        (b"", "TRUNCATED"),
        (b"\x82\x01", "TRUNCATED"),
        (b"\xa1\x61a", "TRUNCATED"),
        (b"\x00\x00", "TRAILING_BYTES"),
    ] {
        for profile in [Profile::Ts2, Profile::Rust3] {
            assert_eq!(refusal(bytes, profile), code, "{bytes:02x?}");
        }
    }
    // A key is NFC-checked like any text.
    let key = [&[0xa1][..], &text("e\u{301}"), b"\x01"].concat();
    assert_eq!(refusal(&key, Profile::Ts2), "NON_NFC");
}

#[test]
fn claimed_lengths_are_never_allocated() {
    // Each claims far more than it carries; each refuses TRUNCATED at once.
    for bytes in [
        &b"\x5b\xff\xff\xff\xff\xff\xff\xff\xff"[..],
        b"\x7b\x00\x00\x00\x01\x00\x00\x00\x00",
        b"\x9b\xff\xff\xff\xff\xff\xff\xff\xff",
        b"\xbb\xff\xff\xff\xff\xff\xff\xff\xff\x61a",
    ] {
        assert_eq!(refusal(bytes, Profile::Rust3), "TRUNCATED");
    }
}

#[test]
fn nesting_is_bounded_and_iterative() {
    let nested = |depth: usize| {
        let mut bytes = vec![0x81; depth - 1];
        bytes.push(0x80);
        bytes
    };
    for profile in [Profile::Ts2, Profile::Rust3] {
        assert!(decode(&nested(8), profile, 8).is_ok());
        assert_eq!(decode(&nested(9), profile, 8), Err(CborRefusal::Depth));
        // Maps count the same.
        let maps = [&b"\xa1\x61a"[..], b"\xa1\x61a", b"\xa0"].concat();
        assert!(decode(&maps, profile, 3).is_ok());
        assert_eq!(decode(&maps, profile, 2), Err(CborRefusal::Depth));
        // A scalar is depth 0 within its container; the root array is 1.
        assert!(decode(b"\x81\x01", profile, 1).is_ok());
        // A million levels refuse at the bound, with no recursion.
        assert_eq!(
            decode(&nested(1_000_000), profile, DEEP),
            Err(CborRefusal::Depth)
        );
    }
}

#[test]
fn encoding_is_deterministic_and_round_trips() {
    let value = Value::Map(vec![
        (
            "b".to_owned(),
            Value::Array(vec![Value::Null, Value::Bool(true)]),
        ),
        ("aa".to_owned(), Value::Bytes(vec![1, 2])),
        ("a".to_owned(), Value::Text("\u{e9}".to_owned())),
    ]);
    let bytes = encode(&value);
    // Members sort by encoded key: "a", "b", then "aa".
    assert_eq!(bytes, hex("a3616162c3a9616282f6f5626161420102"));
    let decoded = decode(&bytes, Profile::Rust3, DEEP).unwrap();
    let Value::Map(members) = &decoded else {
        panic!("a map")
    };
    let keys: Vec<&str> = members.iter().map(|(k, _)| k.as_str()).collect();
    assert_eq!(keys, ["a", "b", "aa"]);
    assert_eq!(encode(&decoded), bytes);
}

/// LD-D2B-14: every case of the vendored differential corpus, built by the
/// reference decoder, decodes or refuses exactly as the reference did, under
/// both profiles. The NFC predicate agrees with the reference's `unicodedata`
/// over every text the corpus carries (LD-D2B-11).
#[test]
fn the_reader_agrees_with_the_reference_decoder() {
    let corpus = parse_json(DIFFERENTIAL).unwrap();
    let J::Object(corpus) = corpus else {
        panic!("an object")
    };
    assert_eq!(
        corpus["reference"],
        parse_json(
            br#"{"path":"docs/implementation/m1/trials/native-wire-owner-07/subject/tools/wirecodec.py","sha256":"716f638023c9535c1b9f7ff937ec53585e3aa562d0c9277e9e02a60c14f794e8"}"#
        )
        .unwrap()
    );
    // The reference's Unicode database and the NFC tables are one version.
    assert_eq!(corpus["unicodeVersion"], J::String("16.0.0".to_owned()));
    assert_eq!(opensip_identity::NFC_UNICODE_VERSION, (16, 0, 0));
    let J::Array(cases) = &corpus["cases"] else {
        panic!("cases")
    };
    let mut disagreements = Vec::new();
    for case in cases {
        let J::Object(case) = case else {
            panic!("a case")
        };
        let (J::String(input), J::String(profile), J::String(outcome)) =
            (&case["input"], &case["profile"], &case["outcome"])
        else {
            panic!("case members")
        };
        let profile = match profile.as_str() {
            "ts2-cbor" => Profile::Ts2,
            "rust3-cbor" => Profile::Rust3,
            other => panic!("profile {other}"),
        };
        let input = hex(input);
        let got = match decode(&input, profile, DEEP) {
            Ok(value) => {
                assert_eq!(encode(&value), input);
                "OK"
            }
            Err(refusal) => refusal.code(),
        };
        if got != outcome {
            disagreements.push(format!("{profile:?} {input:02x?}: {got} != {outcome}"));
        }
    }
    assert!(disagreements.is_empty(), "{disagreements:#?}");
    assert_eq!(cases.len(), 7550);
}
