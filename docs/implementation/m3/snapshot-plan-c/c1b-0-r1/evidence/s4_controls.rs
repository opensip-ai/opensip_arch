
/// C1b-0 (C1b plan r3; M3-B successor S4 as B-S2 defines it): `vcs-observation`
/// is schema 2 or schema 3. B-S2's three vectors admit with their published
/// canonical bytes and SHA-256, through identity admission and through the
/// record check the Run closure makes (`identity_record_shape`, as
/// `run_links.rs` reads `vcsDigest`). The two schema-2 vectors are the pre-S4
/// bytes, computed under the accepted schema 2, so they also admit under
/// `vcs-observation-v2`, the accepted record copied. B-S2's negatives refuse
/// at both.
#[cfg(test)]
mod s4_vcs_observation_tests {
    use super::embedded_schema_registry;
    use opensip_identity::{
        ObjectInput, RegisteredSchemas, RetainedInputs, canonical_bytes, digest_hex,
        parse_json, raw_sha256,
    };
    use std::collections::BTreeMap;
    use std::format;
    use std::string::String;

    const ID3: &str = "urn:opensip:product-v1:identity:v3";
    const SERDE: &str = r#"{"commitId":"0123456789abcdef0123456789abcdef01234567","dirty":true,"kind":"git","path":"serde"}"#;
    const SERDE_JSON: &str = r#"{"commitId":"fedcba9876543210fedcba9876543210fedcba98","dirty":true,"kind":"git","path":"serde-json"}"#;

    /// B-S2's sample inventory digest: the SHA-256 of the canonical `[]`.
    fn inventory() -> String {
        digest_hex(&raw_sha256(b"[]"))
    }
    fn v2(kind: &str, commit: &str, dirty: bool, extra: &str) -> String {
        format!(
            r#"{{"commitId":{commit},"dirty":{dirty},"kind":"{kind}","schemaVersion":2,"sourceInventoryDigest":"{}"{extra}}}"#,
            inventory()
        )
    }
    fn v3(top: &str, members: Option<&str>) -> String {
        let members = members.map_or(String::new(), |m| format!(r#","members":[{m}]"#));
        format!(
            r#"{{{top},"schemaVersion":3,"sourceInventoryDigest":"{}"{members}}}"#,
            inventory()
        )
    }
    const TOP: &str = r#""commitId":null,"dirty":false,"kind":"none""#;
    fn canonical(raw: &str) -> std::vec::Vec<u8> {
        canonical_bytes(&parse_json(raw.as_bytes()).unwrap()).unwrap()
    }
    /// Identity admission of the canonical bytes under `def`.
    fn admits(registry: &RegisteredSchemas, def: &str, bytes: &[u8]) -> bool {
        registry
            .schema(ID3, &format!("/$defs/{def}"))
            .unwrap()
            .admit_json(bytes, 1_000_000)
            .is_ok()
    }
    /// The Run closure's record check over the same bytes, retained as a blob.
    fn closure_admits(registry: &RegisteredSchemas, bytes: &[u8]) -> bool {
        let objects: BTreeMap<String, ObjectInput> = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        blobs.insert(raw_sha256(bytes), bytes.to_vec());
        RetainedInputs::new(registry, &objects, &blobs)
            .identity_record_shape(raw_sha256(bytes), "vcs-observation", 1_000_000)
            .is_ok()
    }

    #[test]
    fn the_s4_vectors_admit_with_their_published_bytes() {
        let registry = embedded_schema_registry().unwrap();
        let two = format!("{SERDE},{SERDE_JSON}");
        for (raw, bytes, sha256, schema2) in [
            (
                v2("none", "null", false, ""),
                154,
                "fd32de2c047f0f64404b37dd3a66999c43af0952a1fe8773f100509489686209",
                true,
            ),
            (
                v2("git", &format!("\"{}\"", "a".repeat(40)), true, ""),
                190,
                "b7a78032ceacb5872b1306e904cd489b8946aac2171f75671de9ea5343a877c0",
                true,
            ),
            (
                v3(TOP, Some(&two)),
                365,
                "b6e0334aef83c204af82c1a083989252281fded6dce58a9005d8c69bc9f8f01f",
                false,
            ),
        ] {
            let canonical = canonical(&raw);
            assert_eq!(canonical.len(), bytes, "{raw}");
            assert_eq!(digest_hex(&raw_sha256(&canonical)), sha256, "{raw}");
            assert!(admits(&registry, "vcs-observation", &canonical), "{raw}");
            assert!(closure_admits(&registry, &canonical), "{raw}");
            // The pre-S4 record: schema 2 admits under the accepted schema,
            // copied unchanged, with the same bytes; schema 3 does not.
            assert_eq!(admits(&registry, "vcs-observation-v2", &canonical), schema2, "{raw}");
        }
    }

    #[test]
    fn the_s4_negatives_refuse_at_admission_and_at_the_run_closure() {
        let registry = embedded_schema_registry().unwrap();
        let two = format!("{SERDE},{SERDE_JSON}");
        let first = |from: &str, to: &str| SERDE.replacen(from, to, 1);
        let many: std::vec::Vec<String> = (0..65)
            .map(|i| {
                format!(
                    r#"{{"commitId":"{}","dirty":true,"kind":"git","path":"m{i:03}"}}"#,
                    "a".repeat(40)
                )
            })
            .collect();
        for (why, raw) in [
            (
                "top-level git",
                v3(
                    &format!(r#""commitId":"{}","dirty":false,"kind":"git""#, "a".repeat(40)),
                    Some(&two),
                ),
            ),
            (
                "top-level dirty",
                v3(r#""commitId":null,"dirty":true,"kind":"none""#, Some(&two)),
            ),
            ("no members", v3(TOP, Some(""))),
            (
                "members on schema 2",
                v2("none", "null", false, &format!(r#","members":[{two}]"#)),
            ),
            ("schema 3 without members", v3(TOP, None)),
            (
                "unordered members",
                v3(TOP, Some(&format!("{SERDE_JSON},{SERDE}"))),
            ),
            (
                "uppercase commit",
                v3(
                    TOP,
                    Some(&first(
                        "0123456789abcdef0123456789abcdef01234567",
                        &"A".repeat(40),
                    )),
                ),
            ),
            (
                "sha256 commit",
                v3(
                    TOP,
                    Some(&first(
                        "0123456789abcdef0123456789abcdef01234567",
                        &"a".repeat(64),
                    )),
                ),
            ),
            (
                "hg member",
                v3(TOP, Some(&first(r#""kind":"git""#, r#""kind":"hg""#))),
            ),
            (
                "absolute member path",
                v3(TOP, Some(&first(r#""path":"serde""#, r#""path":"/serde""#))),
            ),
            (
                "dot-dot member path",
                v3(TOP, Some(&first(r#""path":"serde""#, r#""path":"../serde""#))),
            ),
            ("65 members", v3(TOP, Some(&many.join(",")))),
        ] {
            let canonical = canonical(&raw);
            assert!(!admits(&registry, "vcs-observation", &canonical), "{why}");
            assert!(!closure_admits(&registry, &canonical), "{why}");
        }
        // Schema 3 under the accepted schema 2 refuses.
        assert!(!admits(&registry, "vcs-observation-v2", &canonical(&v3(TOP, Some(&two)))));
    }
}
