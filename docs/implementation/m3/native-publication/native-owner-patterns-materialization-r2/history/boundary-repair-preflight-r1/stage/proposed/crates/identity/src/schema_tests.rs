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

// Selected native-owner semantics are opt-in inside the exact-source registry.
// These are synthetic Program controls, not a forged RegisteredSchemas source
// set or a newly selected product entrypoint. Real registry positives follow
// the complete selected source/pin materialization.
fn native_owner_document(id: &str, body: &str) -> crate::JsonValue {
    let mut value = doc(body);
    let crate::JsonValue::Object(ref mut object) = value else {
        unreachable!()
    };
    object.insert("$id".into(), crate::JsonValue::String(id.into()));
    value
}

const NATIVE_OWNER_DOT_BODY: &str = r#""type":"string","not":{"pattern":"(^|/)\\.\\.?(/|$)"}"#;

#[test]
fn native_owner_ecma_dot_scope_covers_each_selected_document_and_generic_isolation() {
    const IDS: [&str; 3] = [
        "urn:opensip:product-v1:native:evidence-schemas:v2",
        "opensip.product.occupancy-companion.1",
        "opensip.product.relation-payload.2",
    ];
    let cases: &[(&[u8], bool, bool)] = &[
        (br#""a/..\n""#, true, false),
        (br#""a/.\n""#, true, false),
        (br#""a/..\r""#, true, true),
        (br#""a/.\r""#, true, true),
        (br#""a/..\u2028""#, true, true),
        (br#""a/..\u2029""#, true, true),
        (br#""a/../b""#, false, false),
        (br#""a/..""#, false, false),
        (br#""a/.""#, false, false),
        (br#""x\n/../y""#, false, false),
        (br#""x\r/../y""#, false, false),
        (br#""x\u2028/../y""#, false, false),
        (br#""x\u2029/../y""#, false, false),
    ];
    for id in IDS {
        let entry = format!("{id}#");
        let document = native_owner_document(id, NATIVE_OWNER_DOT_BODY);
        let scoped =
            Program::compile_registered_native_owners(vec![document.clone()], &[&entry], 100_000)
                .unwrap();
        let generic = Program::compile(vec![document], &[&entry], 100_000).unwrap();
        for &(raw, ecma, inherited) in cases {
            assert_eq!(
                scoped.matches_json(&entry, raw, 100_000),
                Ok(ecma),
                "{id} scoped {raw:?}"
            );
            assert_eq!(
                generic.matches_json(&entry, raw, 100_000),
                Ok(inherited),
                "{id} generic {raw:?}"
            );
        }
    }
    let foreign = Program::compile_registered_native_owners(
        vec![doc(NATIVE_OWNER_DOT_BODY)],
        &["urn:probe#"],
        100_000,
    )
    .unwrap();
    for &(raw, _, inherited) in cases {
        assert_eq!(
            foreign.matches_json("urn:probe#", raw, 100_000),
            Ok(inherited)
        );
    }
}

#[test]
fn native_owner_scope_tracks_external_document_and_does_not_spread_into_foreign_refs() {
    let native = "urn:opensip:product-v1:native:evidence-schemas:v2";
    let startup = "opensip.product.provider-startup.1";
    let native_document = native_owner_document(native, NATIVE_OWNER_DOT_BODY);
    let startup_document = native_owner_document(startup, &format!(r#""$ref":"{native}#""#));
    let entry = format!("{startup}#");
    let program = Program::compile_registered_native_owners(
        vec![startup_document, native_document],
        &[&entry],
        100_000,
    )
    .unwrap();
    assert_eq!(
        program.matches_json(&entry, br#""a/..\n""#, 100_000),
        Ok(true)
    );

    // Resolution from a native schema back into a foreign document restores
    // its inherited semantics even though the entrypoint was native-owned.
    let native_document = native_owner_document(native, r#""$ref":"urn:probe#""#);
    let entry = format!("{native}#");
    let program = Program::compile_registered_native_owners(
        vec![native_document, doc(NATIVE_OWNER_DOT_BODY)],
        &[&entry],
        100_000,
    )
    .unwrap();
    assert_eq!(
        program.matches_json(&entry, br#""a/..\n""#, 100_000),
        Ok(false)
    );
}

#[test]
fn native_owner_scope_does_not_reinterpret_pattern_property_keys_or_accept_unknown_forms() {
    let native = "urn:opensip:product-v1:native:evidence-schemas:v2";
    let entry = format!("{native}#");
    let body = r#""type":"object","patternProperties":{"^.+$":{"type":"integer"}},"additionalProperties":false"#;
    let program = Program::compile_registered_native_owners(
        vec![native_owner_document(native, body)],
        &[&entry],
        100_000,
    )
    .unwrap();
    assert_eq!(
        program.matches_json(&entry, br#"{"a\n":1}"#, 100_000),
        Ok(true)
    );
    assert_eq!(
        program.matches_json(&entry, br#"{"a\n\n":1}"#, 100_000),
        Ok(false)
    );
    // ^.+$ is known to the inherited evaluator, but not among the selected
    // native owner keyword forms. An expansion fails closed at compilation.
    assert!(matches!(
        Program::compile_registered_native_owners(
            vec![native_owner_document(
                native,
                r#""type":"string","pattern":"^.+$""#
            )],
            &[&entry],
            100_000
        ),
        Err(Error::Pattern)
    ));
    assert!(
        Program::compile(
            vec![native_owner_document(
                native,
                r#""type":"string","pattern":"^.+$""#
            )],
            &[&entry],
            100_000
        )
        .is_ok()
    );
}

#[test]
fn native_owner_grant_wildcards_keep_ecma_scope_at_both_full_length_positions() {
    let native = "urn:opensip:product-v1:native:evidence-schemas:v2";
    let body = r#""type":"string","pattern":"^security.repo-execution-grants.v2:[0-9a-f]{64}(?![\\s\\S])""#;
    let entry = format!("{native}#");
    let document = native_owner_document(native, body);
    let scoped =
        Program::compile_registered_native_owners(vec![document.clone()], &[&entry], 100_000)
            .unwrap();
    let inherited = Program::compile(vec![document], &[&entry], 100_000).unwrap();
    let foreign =
        Program::compile_registered_native_owners(vec![doc(body)], &["urn:probe#"], 100_000)
            .unwrap();
    for first in ['.', 'x', '😀', '\0', '\n', '\r', '\u{2028}', '\u{2029}'] {
        for second in ['.', 'x', '😀', '\0', '\n', '\r', '\u{2028}', '\u{2029}'] {
            let text = format!(
                "security{first}repo-execution-grants{second}v2:{}",
                "a".repeat(64)
            );
            let raw = crate::canonical_bytes(&crate::JsonValue::String(text)).unwrap();
            let ecma = !matches!(first, '\n' | '\r' | '\u{2028}' | '\u{2029}')
                && !matches!(second, '\n' | '\r' | '\u{2028}' | '\u{2029}');
            let legacy = first != '\n' && second != '\n';
            assert_eq!(scoped.matches_json(&entry, &raw, 100_000), Ok(ecma));
            assert_eq!(inherited.matches_json(&entry, &raw, 100_000), Ok(legacy));
            assert_eq!(
                foreign.matches_json("urn:probe#", &raw, 100_000),
                Ok(legacy)
            );
        }
    }
}

#[test]
fn native_owner_corrected_forms_refuse_foreign_patterns_and_all_pattern_property_keys() {
    let forms = [
        r##"^(?!/)(?![\s\S]*(^|/)\.\.?(/|$))[^\u0000\\]*(?![\s\S])"##,
        r##"^(?!/)(?![\s\S]*(^|/)\.\.?(/|$))[^\u0000\\]+(?![\s\S])"##,
    ];
    let owners = [
        "urn:opensip:product-v1:native:evidence-schemas:v2",
        "opensip.product.occupancy-companion.1",
        "opensip.product.relation-payload.2",
    ];
    for (index, pattern) in forms.into_iter().enumerate() {
        let raw = crate::canonical_bytes(&crate::JsonValue::String(pattern.into())).unwrap();
        let quoted = core::str::from_utf8(&raw).unwrap();
        let body = format!(r#""type":"string","pattern":{quoted}"#);
        for owner in owners {
            let entry = format!("{owner}#");
            let document = native_owner_document(owner, &body);
            let scoped = Program::compile_registered_native_owners(
                vec![document.clone()],
                &[&entry],
                100_000,
            )
            .unwrap();
            for (value, expected) in [
                ("", index == 0),
                ("a/..\n", true),
                ("a/..\r", true),
                ("a/..\u{2028}", true),
                ("a/..\u{2029}", true),
                ("a/..", false),
                ("x\n/../y", false),
                ("/a", false),
                ("a\0", false),
                ("a\\b", false),
            ] {
                let input =
                    crate::canonical_bytes(&crate::JsonValue::String(value.into())).unwrap();
                assert_eq!(
                    scoped.matches_json(&entry, &input, 100_000),
                    Ok(expected),
                    "{owner} {pattern} {value:?}"
                );
            }
            // The inert/generic Program keeps the inherited closed profile,
            // even when a document uses a native spelling for its identity.
            assert!(matches!(
                Program::compile(vec![document], &[&entry], 100_000),
                Err(Error::Pattern)
            ));
        }
        assert!(matches!(
            Program::compile_registered_native_owners(vec![doc(&body)], &["urn:probe#"], 100_000),
            Err(Error::Pattern)
        ));
        // Native-to-foreign references must refuse the foreign pattern at
        // construction, as direct foreign documents do.
        let foreign = doc(&body);
        let native = native_owner_document(owners[0], r##""$ref":"urn:probe#""##);
        let entry = format!("{}#", owners[0]);
        assert!(matches!(
            Program::compile_registered_native_owners(vec![native, foreign], &[&entry], 100_000),
            Err(Error::Pattern)
        ));
        let property_body =
            format!(r#""type":"object","patternProperties":{{{quoted}:{{"type":"integer"}}}}"#);
        for owner in owners.into_iter().chain(["urn:probe"]) {
            let entry = format!("{owner}#");
            let document = native_owner_document(owner, &property_body);
            assert!(
                matches!(
                    Program::compile_registered_native_owners(
                        vec![document.clone()],
                        &[&entry],
                        100_000
                    ),
                    Err(Error::Pattern)
                ),
                "patternProperties leaked: {owner} {pattern}"
            );
            assert!(matches!(
                Program::compile(vec![document], &[&entry], 100_000),
                Err(Error::Pattern)
            ));
        }
    }
}
