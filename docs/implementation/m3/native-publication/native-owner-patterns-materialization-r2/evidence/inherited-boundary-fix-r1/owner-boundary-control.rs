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
