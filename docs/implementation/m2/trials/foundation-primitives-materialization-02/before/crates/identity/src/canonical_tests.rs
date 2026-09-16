use crate::{
    canonical::{self, Error, Integer, MAX_BYTES, Value},
    digests,
};
use alloc::{collections::BTreeMap, format, string::String, vec, vec::Vec};

#[test]
fn independent_canonical_byte_vectors() {
    // Literal byte goldens from the approved UR-1..5 contract, not this encoder.
    let vectors = [
        (
            " { \"𐀀\" : 1, \"\u{e000}\" : 0 } ",
            "{\"\u{e000}\":0,\"𐀀\":1}",
        ),
        (
            "[0,-1,-9223372036854775808,18446744073709551615]",
            "[0,-1,-9223372036854775808,18446744073709551615]",
        ),
        (r#"{"s":"e\u0301"}"#, "{\"s\":\"e\u{301}\"}"),
        (r#"{"s":"\u00e9"}"#, "{\"s\":\"é\"}"),
        (
            r#"{"s":"\/\b\f\n\r\t\u0001\"\\é"}"#,
            r#"{"s":"/\b\f\n\r\t\u0001\"\\é"}"#,
        ),
        (
            r#"["\u007f","\u2028","\ud800\udc00"]"#,
            "[\"\u{7f}\",\"\u{2028}\",\"𐀀\"]",
        ),
        (" [3,1,3] ", "[3,1,3]"),
        (
            "{\"z\":null,\"b\":true,\"a\":false}",
            "{\"a\":false,\"b\":true,\"z\":null}",
        ),
    ];
    for (input, expected) in vectors {
        let value = canonical::parse(input.as_bytes()).unwrap();
        let actual = canonical::encode(&value).unwrap();
        assert_eq!(actual, expected.as_bytes(), "{input}");
        assert_eq!(canonical::parse(&actual).unwrap(), value);
    }
}

#[test]
fn lexical_integer_refusals_precede_rounding() {
    for input in [
        "1.0",
        "1e0",
        "1E0",
        "1.0000000000000001",
        "9007199254740991.1",
        "-1.0",
        "-0e0",
    ] {
        assert_eq!(
            canonical::parse(input.as_bytes()),
            Err(Error::FloatForbidden),
            "{input}"
        );
    }
    assert_eq!(canonical::parse(b"-0"), Err(Error::NegativeZero));
    for input in [
        "18446744073709551616",
        "-9223372036854775809",
        "999999999999999999999999999999999999999999999",
    ] {
        assert_eq!(
            canonical::parse(input.as_bytes()),
            Err(Error::IntegerRange),
            "{input}"
        );
    }
    assert_ne!(
        canonical::parse(b"true").unwrap(),
        canonical::parse(b"1").unwrap()
    );
    assert_ne!(
        canonical::parse(b"\"1\"").unwrap(),
        canonical::parse(b"1").unwrap()
    );
    assert_eq!(
        Integer::new(canonical::MIN_INTEGER - 1),
        Err(Error::IntegerRange)
    );
    assert_eq!(
        Integer::new(canonical::MAX_INTEGER + 1),
        Err(Error::IntegerRange)
    );
}

#[test]
fn duplicate_keys_are_compared_after_escape_decoding() {
    for input in [
        r#"{"a":1,"a":2}"#,
        r#"{"a":1,"\u0061":2}"#,
        r#"{"𐀀":1,"\ud800\udc00":2}"#,
        r#"{"outer":{"a":1,"a":2}}"#,
    ] {
        assert_eq!(
            canonical::parse(input.as_bytes()),
            Err(Error::DuplicateKey),
            "{input}"
        );
    }
    // Unicode normalization is intentionally absent.
    assert!(canonical::parse("{\"é\":1,\"e\u{301}\":2}".as_bytes()).is_ok());
}

#[test]
fn malformed_unicode_and_json_refuse() {
    for input in [
        r#""\ud800""#,
        r#""\udc00""#,
        r#""\ud800\u0061""#,
        r#""\ud800x""#,
    ] {
        assert_eq!(
            canonical::parse(input.as_bytes()),
            Err(Error::InvalidUnicode),
            "{input}"
        );
    }
    for input in [
        "",
        " ",
        "01",
        "-01",
        "+1",
        "-",
        "NaN",
        "Infinity",
        "null null",
        "truefalse",
        "[1,]",
        "{\"a\":1,}",
        "{a:1}",
        "[",
        "{",
        "\"",
        "\"\n\"",
        r#""\x20""#,
        r#""\u00zz""#,
        "\u{feff}null",
        "\u{b}null",
    ] {
        assert!(canonical::parse(input.as_bytes()).is_err(), "{input}");
    }
    for input in [
        &b"\"\xff\""[..],
        &b"\"\xed\xa0\x80\""[..],
        &b"\"\xc0\x80\""[..],
    ] {
        assert_eq!(canonical::parse(input), Err(Error::InvalidUtf8));
    }
}

#[test]
fn depth_counts_containers_but_not_scalar_leaves_or_keys() {
    for depth in [31, 32, 33] {
        let raw = format!("{}0{}", "[".repeat(depth), "]".repeat(depth));
        assert_eq!(canonical::parse(raw.as_bytes()).is_ok(), depth <= 32);
        let raw = format!("{}\"leaf\"{}", "{\"key\":".repeat(depth), "}".repeat(depth));
        assert_eq!(canonical::parse(raw.as_bytes()).is_ok(), depth <= 32);
    }
    let mut value = Value::Null;
    for _ in 0..32 {
        value = Value::Array(vec![value]);
    }
    assert!(canonical::encode(&value).is_ok());
    assert_eq!(
        canonical::encode(&Value::Array(vec![value])),
        Err(Error::DepthLimit)
    );
}

#[test]
fn byte_limits_are_inclusive_and_apply_to_encoded_values() {
    let mut input = vec![b' '; MAX_BYTES];
    input[0] = b'0';
    assert!(canonical::parse(&input).is_ok());
    input.push(b' ');
    assert_eq!(canonical::parse(&input), Err(Error::ByteLimit));
    let value = Value::String("x".repeat(MAX_BYTES - 2));
    assert_eq!(canonical::encode(&value).unwrap().len(), MAX_BYTES);
    assert_eq!(
        canonical::encode(&Value::String("x".repeat(MAX_BYTES - 1))).map(|bytes| bytes.len()),
        Err(Error::ByteLimit)
    );
    // This programmatic input expands by six bytes per control plus two quotes.
    assert_eq!(
        canonical::encode(&Value::String("\0".repeat(MAX_BYTES / 6)))
            .unwrap()
            .len(),
        (MAX_BYTES / 6) * 6 + 2
    );
    assert_eq!(
        canonical::encode(&Value::String("\0".repeat(MAX_BYTES / 6 + 1))).map(|bytes| bytes.len()),
        Err(Error::ByteLimit)
    );
}

#[test]
fn programmatic_values_remain_inert_and_arrays_keep_order() {
    let mut object = BTreeMap::new();
    object.insert(String::from("z"), Value::Integer(Integer::new(3).unwrap()));
    object.insert(
        String::from("a"),
        Value::Array(vec![Value::Bool(true), Value::Null, Value::Bool(true)]),
    );
    assert_eq!(
        canonical::encode(&Value::Object(object)).unwrap(),
        br#"{"a":[true,null,true],"z":3}"#
    );
}

#[test]
fn sha256_matches_independent_standard_vectors() {
    assert_eq!(
        digests::hex(&digests::raw_sha256(b"")),
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    );
    assert_eq!(
        digests::hex(&digests::raw_sha256(b"abc")),
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    );
    assert_eq!(
        digests::hex(&digests::raw_sha256(&vec![b'a'; 1_000_000])),
        "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
    );
}

#[test]
fn product_frames_match_independent_hashlib_goldens() {
    let vectors = [
        (
            "null",
            "ae2a3ea941d02d406de61b3f9e56481330b15ea42a527e21e0d0e307599dc26c",
        ),
        (
            "{}",
            "a55d7ef6f4e91b65725fa884c13f1be967b90abed1413d479bfabda5cb2a2c8b",
        ),
        (
            "[0,-1,-9223372036854775808,18446744073709551615]",
            "1b0ea85a3273cbc41aed75f2d07136b77eec013fca6ea2cb84acce63cf8ccd73",
        ),
        (
            "{\"\u{e000}\":0,\"𐀀\":1}",
            "b4208ff8b9f5977285610c23326cc7558565732ea06c5b1728a25ccc0e9105f7",
        ),
    ];
    for (input, expected) in vectors {
        let value = canonical::parse(input.as_bytes()).unwrap();
        assert_eq!(
            digests::hex(&digests::identity("vector", &value).unwrap()),
            expected
        );
    }
    assert_eq!(
        digests::frame("vector", &Value::Null).unwrap(),
        b"opensip.product.v1\0vector\0\0\0\0\0\0\0\0\x04null"
    );
    assert_ne!(
        digests::identity("a", &Value::Null),
        digests::identity("b", &Value::Null)
    );
    for domain in ["", "A", "a\0b", "é", "a/b", "a_b", "a\n"] {
        assert_eq!(
            digests::identity(domain, &Value::Null),
            Err(digests::Error::Domain)
        );
    }
}

#[test]
fn sha256_padding_and_blob_boundaries_match_hashlib() {
    // Independent Python hashlib oracle; data[i] = (i * 37 + 11) mod 256.
    // Includes both padding boundaries and a raw blob beyond the JSON cap.
    for (length, expected) in [
        (
            1_usize,
            "e7cf46a078fed4fafd0b5e3aff144802b853f8ae459a4f0c14add3314b7cc3a6",
        ),
        (
            2_usize,
            "cdc63a6325d5fa92515578c0b418e6eeec1c6d085937a24fc43c2126ea517457",
        ),
        (
            3_usize,
            "b39fad1a1075f64570b3226d339ea818f9c66ecd2f1c59fd8b9c5a32b54c513f",
        ),
        (
            55_usize,
            "2900465fcb533e05a158fd2b3be0e5e3b03740d83060aa3580e0d98a96bf2384",
        ),
        (
            56_usize,
            "31454ff48ef36af2f08fd511bdc37d9d5855ac23e992e5ff5445cb6b7674a674",
        ),
        (
            57_usize,
            "bcc0a5d3791b985b7550e04ca660a6c63a589ba1edd2283c8e110e5b515df124",
        ),
        (
            63_usize,
            "5f6401b96532c36de4e65beec0409b69b1d181864c8009b7a04f43e5d56350d1",
        ),
        (
            64_usize,
            "94eb5de4943613fd048dc93393ab06877405faa39c11f53e9386083339833e7e",
        ),
        (
            65_usize,
            "fc518669b6eb4b4dd91827ecacef86689c725bd5bab888fd3b26dbb196eec954",
        ),
        (
            119_usize,
            "b0dc41b1a384e2f1203f0351b38fbeaafceef577ce1191d5bfc25da39f721eae",
        ),
        (
            120_usize,
            "5df24dd802ac26132ce608dcb5f09841eef039ee0f152acf98d26d17fe4e88e6",
        ),
        (
            127_usize,
            "0fe729ff19257bd6fec853acc2ea355f6b34b58e6c0f684c3e188fcdfcd9baae",
        ),
        (
            128_usize,
            "0aedd4856f8eba0963627336ad5144a9a7dbe12498e6066f0165fc97d8ddee4c",
        ),
        (
            129_usize,
            "4f1757ae4bffbae86d775b831765b75af154d52f7deaa46dd378051a2d3ad57f",
        ),
        (
            4095_usize,
            "14247e71abeac04b1bb56818238f449fe1339e1d9b347ade9224b12460f39d1c",
        ),
        (
            4096_usize,
            "4e441a3533bb2c10cd5649981d395744213e09a336746b5a3458fee4057205ec",
        ),
        (
            4097_usize,
            "042a02b55ba342cdd30322331816b6e4bca073f33bdb80149dc74a6f949802f4",
        ),
        (
            4194305_usize,
            "84f665c80882f17406c05fa2d0cad2b8687270ca629df7ab65a19940501925cd",
        ),
    ] {
        let bytes: Vec<u8> = (0..length).map(|i| ((i * 37 + 11) % 256) as u8).collect();
        assert_eq!(
            digests::hex(&digests::raw_sha256(&bytes)),
            expected,
            "length={length}"
        );
    }
}
