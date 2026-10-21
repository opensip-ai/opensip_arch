use crate::parse_json;
use crate::schema::{Error, Program};
use alloc::{format, vec};
fn doc(body: &str) -> crate::JsonValue {
    parse_json(format!(r#"{{"$id":"urn:probe","$schema":"https://json-schema.org/draft/2020-12/schema",{body}}}"#).as_bytes()).unwrap()
}
fn check(body: &str, raw: &[u8], budget: usize) -> Result<bool, Error> {
    let docs = [doc(body)];
    let program = Program::compile(docs.to_vec(), &["urn:probe#"], 1_000_000)?;
    program.matches_json("urn:probe#", raw, budget)
}
#[test]
fn faults_never_turn_into_successful_negation_or_conditionals() {
    for body in [
        r##""not":{"$ref":"#"}"##,
        r##""anyOf":[{"$ref":"#"},true]"##,
        r##""if":{"$ref":"#"},"else":true"##,
    ] {
        assert_eq!(check(body, b"0", 1_000_000), Err(Error::Limit));
    }
    assert_eq!(check(r#""const":1"#, b"1", 0), Err(Error::Limit));
    assert_eq!(check(r#""const":1"#, b"true", 1000), Ok(false));
    assert_eq!(check(r#""not":{"const":1}"#, b"-0", 1000), Err(Error::Json));
}
#[test]
fn compile_refuses_unsupported_or_unresolved_laws_before_evaluation() {
    for body in [
        r#""unknown":true"#,
        r#""pattern":".*""#,
        r##""anyOf":[true,{"$ref":"urn:missing#"}]"##,
        r#""type":"number""#,
        r#""x-opensip-order":"unknown""#,
    ] {
        assert!(Program::compile(vec![doc(body)], &["urn:probe#"], 1_000_000).is_err());
    }
    let d = doc(r#""type":"null""#);
    assert!(Program::compile(vec![d.clone(), d], &["urn:probe#"], 1_000_000).is_err());
    let docs = [doc(r#""type":"null""#)];
    let program = Program::compile(docs.to_vec(), &["urn:probe#"], 1_000_000).unwrap();
    assert_eq!(
        program.matches_json("urn:probe", b"null", 1000),
        Err(Error::UnselectedEntry)
    );
}
#[test]
fn reference_siblings_and_pointer_escapes_are_not_lost() {
    let body = r##""$defs":{"a/b~c":{"type":"integer"}},"$ref":"#/$defs/a~1b~0c","maximum":1"##;
    assert_eq!(check(body, b"1", 1000), Ok(true));
    assert_eq!(check(body, b"2", 1000), Ok(false));
    assert_eq!(check(body, b"true", 1000), Ok(false));
    assert_eq!(
        check(r##""$ref":"#/~2""##, b"0", 1000),
        Err(Error::Reference)
    );
}
#[test]
fn typed_uniqueness_and_order_have_distinct_laws() {
    assert_eq!(check(r#""uniqueItems":true"#, b"[true,1]", 1000), Ok(true));
    assert_eq!(
        check(
            r#""uniqueItems":true"#,
            b"[{\"a\":1,\"b\":2},{\"b\":2,\"a\":1}]",
            1000
        ),
        Ok(false)
    );
    assert_eq!(
        check(r#""x-opensip-order":"numeric""#, b"[1,true]", 1000),
        Ok(false)
    );
    assert_eq!(
        check(r#""x-opensip-order":"canonical-order""#, b"[1,1]", 1000),
        Ok(true)
    );
    assert_eq!(
        check(r#""x-opensip-order":"canonical-set""#, b"[1,1]", 1000),
        Ok(false)
    );
}
#[test]
fn python_pattern_property_keys_and_shape_annotations_remain_distinct() {
    let body = r#""patternProperties":{"^.+$":{"type":"integer"}},"additionalProperties":false"#;
    for raw in [br#"{"a":1}"#.as_slice(), br#"{"a\n":1}"#, br#"{"a\r":1}"#] {
        assert_eq!(check(body, raw, 1000), Ok(true));
    }
    for raw in [
        br#"{"":1}"#.as_slice(),
        br#"{"\n":1}"#,
        br#"{"a\n\n":1}"#,
        br#"{"a":true}"#,
    ] {
        assert_eq!(check(body, raw, 1000), Ok(false));
    }
    assert_eq!(
        check(
            r#""type":"string","maxLength":1,"x-maxUtf8Bytes":1"#,
            "\"😀\"".as_bytes(),
            1000
        ),
        Ok(true)
    );
}

#[test]
fn canonical_text_excludes_c0_del_c1_without_excluding_other_unicode() {
    let patterns = [
        (r#"^[^\u0000-\u001f\u007f-\u009f]*(?![\s\S])"#, true),
        (r#"^[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])"#, false),
    ];
    for (pattern, empty) in patterns {
        assert_eq!(crate::schema_patterns::matches(pattern, "").unwrap(), empty);
        for n in 0..=0x200 {
            let c = char::from_u32(n).unwrap();
            let text = alloc::string::ToString::to_string(&c);
            assert_eq!(
                crate::schema_patterns::matches(pattern, &text).unwrap(),
                !matches!(n,0..=0x1f|0x7f..=0x9f)
            );
        }
    }
}
