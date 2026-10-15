// Law X12 r3 item 10, host side (unit X12b; X12a judgment call 14): the
// selection count, the public mapping of every item 7 row into law 468 r5
// item 6's termination shape, the CONFIG.INVALID remedy bytes, and the
// purity and "no evaluation" pins on configuration.rs. Every input here is
// synthetic but the release pack; the evaluator's cfg(test) registry is
// unreachable from the host, so every Named source meets the release
// registry, whose one row is the preview pack (law M3-I1 item 7, unit I1-c).
use super::*;
use crate::doctor_ingress::failure_envelope;
use opensip_evaluator::SuppliedProvenance;
use opensip_identity::{JsonValue as V, canonical_bytes, parse_json};
use serde_json::Value;

const REQUEST: &str = "req1_0123456789abcdef0123456789abcdef";
const ENVELOPE: &str = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7";
/// The B-S9 string (superseding X12-0's 367 bytes): 706 ASCII bytes, SHA-256
/// of the exact text of line 1158 of B-S9's selected native reference copy.
const S9_REMEDY_SHA256: &str = "7ba6e8e50dc3c52f595caf01236019d2cfac6d8f0fd2e40d0dd3644fb0692565";
/// The evaluator's synthetic test pack document (unit X12a), bundled only in
/// its cfg(test) registry.
const TEST_DOCUMENT: &[u8] =
    include_bytes!("../../evaluator/tests/fixtures/policy-pack-test-fixture.policy.json");
const TEST_ID: &str = "opensip.test.fixture.pack:1";
/// The release registry's one row (law M3-I1 item 5): its packId, its bundled
/// document, and the policy and compiled-program digests contract successor
/// I1-P pins.
const PREVIEW_ID: &str = "opensip.preview.typescript.pack:1";
const PREVIEW_DOCUMENT: &[u8] =
    include_bytes!("../../evaluator/src/preview-typescript-pack.v1.policy.json");
const PREVIEW_SHA: &str = "96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1";
const PREVIEW_PROGRAM_SHA: &str =
    "e796f81764d0ee452c591c852e98f59647518a1894d4bd0fd5c70b674ecc3ecb";
const BOTH: [SuppliedProvenance; 2] = [SuppliedProvenance::User, SuppliedProvenance::ThirdParty];

fn refuse(selection: &[PackSource<'_>]) -> PolicySelectionRefusal {
    admit_policy_selection(selection).unwrap_err()
}
fn named(id: &str) -> PolicySelectionRefusal {
    refuse(&[PackSource::Named(id)])
}
fn supplied(bytes: &[u8], provenance: SuppliedProvenance) -> PolicySelectionRefusal {
    refuse(&[PackSource::Supplied { bytes, provenance }])
}
fn supplied_subject(bytes: &[u8], provenance: SuppliedProvenance) -> String {
    format!(
        "supplied:{}:sha256:{}",
        provenance.name(),
        digest_hex(&raw_sha256(bytes))
    )
}
fn rejected(detail: Detail, subject: &str) -> InstallationTerminationV1 {
    InstallationTerminationV1 {
        class: Class::RequestRejected,
        exit: 2,
        error_code: Code::ConfigInvalid,
        fault_cause: Fault::None,
        detail: Some(detail),
        subject: Some(subject.to_owned()),
    }
}
/// Insert `value` at a pointer whose parent exists (`/a/0/b`).
fn with(pointer: &str, value: V) -> Vec<u8> {
    let mut doc = parse_json(TEST_DOCUMENT).unwrap();
    let parts: Vec<&str> = pointer[1..].split('/').collect();
    let (last, path) = parts.split_last().unwrap();
    let mut node = &mut doc;
    for part in path {
        node = match node {
            V::Object(o) => o.get_mut(*part).unwrap(),
            V::Array(a) => &mut a[part.parse::<usize>().unwrap()],
            _ => panic!("{pointer}"),
        };
    }
    match node {
        V::Object(o) => {
            o.insert((*last).into(), value);
        }
        V::Array(a) => a[last.parse::<usize>().unwrap()] = value,
        _ => panic!("{pointer}"),
    }
    canonical_bytes(&doc).unwrap()
}
fn s(v: &str) -> V {
    V::String(v.into())
}

/// The shared failure-envelope path: validated against the selected
/// command-envelope v7 source schema, exit derived from the class, and the
/// human rendering. Returns the JSON value.
fn envelope(t: &InstallationTerminationV1) -> (Value, String) {
    let (envelope, exit_code) = failure_envelope(REQUEST, None, t).unwrap();
    let raw = opensip_reporting::render_json(&envelope).unwrap();
    assert!(
        crate::embedded_schema_registry()
            .unwrap()
            .schema(ENVELOPE, "")
            .unwrap()
            .admit_json(&raw, 64 * 1024 * 1024)
            .is_ok(),
        "{}",
        String::from_utf8_lossy(&raw)
    );
    let value: Value = serde_json::from_slice(&raw).unwrap();
    assert_eq!(value["kind"], "failure");
    assert_eq!(exit_code, t.exit);
    assert_eq!(value["exitCode"], t.exit);
    let human = String::from_utf8(opensip_reporting::render_human(&envelope).unwrap()).unwrap();
    (value, human)
}

#[test]
fn nt1_wrong_pack_identity_is_row_1_with_the_presented_id() {
    // G24.nt1.wrong-pack-identity. The release registry's one row is the
    // DR-131 identity, which admits (law M3-I1 item 7; S9 below); its
    // variants stay row 1, and the evaluator's synthetic test ID is
    // unreachable from the host.
    for id in [
        "opensip.preview.typescript.pack:2",
        "opensip.preview.typescript.pack",
        "opensip.preview.typescript.pack:01",
        "OPENSIP.PREVIEW.TYPESCRIPT.PACK:1",
        "opensip.preview.TypeScript.pack:1",
        "opensip.preview.typescript.pack:1\n",
        " opensip.preview.typescript.pack:1",
        "opensip.preview.typescript.pack:1 ",
        "opensip.preview.javascript.pack:1",
        ":01",
        "",
        TEST_ID,
    ] {
        let refusal = named(id);
        assert_eq!(
            refusal,
            PolicySelectionRefusal::Pack(PackRefusal::NotBundled {
                pack_id: id.to_owned()
            }),
            "{id:?}"
        );
        assert_eq!(
            policy_selection_termination(&refusal),
            rejected(Detail::ConfigInvalid, id),
            "{id:?}"
        );
    }
}

#[test]
fn the_release_pack_is_admitted_by_its_exact_id() {
    // Law M3-I1 S9: Named(opensip.preview.typescript.pack:1) returns the
    // evaluator's own AdmittedPack, unwrapped, with the digests I1-P pins.
    let admitted = admit_policy_selection(&[PackSource::Named(PREVIEW_ID)]).unwrap();
    assert_eq!(admitted.pack_id(), PREVIEW_ID);
    assert_eq!(admitted.policy_digest(), raw_sha256(PREVIEW_DOCUMENT));
    assert_eq!(digest_hex(&admitted.policy_digest()), PREVIEW_SHA);
    assert_eq!(digest_hex(&admitted.program_digest()), PREVIEW_PROGRAM_SHA);
    // The release document's exact bytes, supplied, stay row 2 (S7).
    for provenance in BOTH {
        let refusal = supplied(PREVIEW_DOCUMENT, provenance);
        assert_eq!(
            refusal,
            PolicySelectionRefusal::Pack(PackRefusal::SuppliedPack {
                provenance,
                sha256: raw_sha256(PREVIEW_DOCUMENT)
            })
        );
        assert_eq!(
            policy_selection_termination(&refusal),
            rejected(
                Detail::ConfigInvalid,
                &supplied_subject(PREVIEW_DOCUMENT, provenance)
            )
        );
    }
}

#[test]
fn nt1_user_and_third_party_packs_are_row_2_whatever_their_bytes() {
    // G24.nt1.user-pack and G24.nt1.third-party-pack, including the test
    // pack's bundled bytes exactly: admission is by identity only.
    let canonical = canonical_bytes(&parse_json(TEST_DOCUMENT).unwrap()).unwrap();
    let mut newline = TEST_DOCUMENT.to_vec();
    newline.push(b'\n');
    for bytes in [TEST_DOCUMENT.to_vec(), canonical, newline] {
        for provenance in BOTH {
            let refusal = supplied(&bytes, provenance);
            assert_eq!(
                refusal,
                PolicySelectionRefusal::Pack(PackRefusal::SuppliedPack {
                    provenance,
                    sha256: raw_sha256(&bytes)
                })
            );
            assert_eq!(
                policy_selection_termination(&refusal),
                rejected(Detail::ConfigInvalid, &supplied_subject(&bytes, provenance))
            );
        }
    }
}

#[test]
fn nt2_imperative_members_and_string_expressions_are_row_3_with_the_pointer() {
    // G24.nt2.non-declarative-pack, a document the caller presents.
    let mut cases = Vec::new();
    for key in ["script", "hook", "exec", "include"] {
        cases.push((format!("/{key}"), s("rm -rf /")));
        cases.push((format!("/rules/0/{key}"), s("curl evil")));
    }
    cases.push(("/rules/0/emitWhen".to_owned(), s("count(file) > 0")));
    for (pointer, value) in cases {
        let bytes = with(&pointer, value);
        for provenance in BOTH {
            let refusal = supplied(&bytes, provenance);
            assert_eq!(
                refusal,
                PolicySelectionRefusal::Pack(PackRefusal::ImperativeMember {
                    pointer: pointer.clone()
                }),
                "{pointer}"
            );
            assert_eq!(
                policy_selection_termination(&refusal),
                rejected(Detail::PolicyImperativeKeyRefused, &pointer),
                "{pointer}"
            );
        }
    }
}

#[test]
fn nt2_non_json_component_contributions_are_row_3a() {
    let wasm: &[u8] = b"\0asm\x01\0\0\0\x01\x04\x01\x60\0\0";
    let v1 = with("/schemaMajor", parse_json(b"1").unwrap());
    for bytes in [
        wasm.to_vec(),
        b"#!/bin/sh\nrm -rf /\n".to_vec(),
        Vec::new(),
        br#"{"schemaMajor":2,"schemaMajor":2}"#.to_vec(),
        v1,
    ] {
        for provenance in BOTH {
            let refusal = supplied(&bytes, provenance);
            assert_eq!(
                refusal,
                PolicySelectionRefusal::Pack(PackRefusal::SuppliedInvalid {
                    provenance,
                    sha256: raw_sha256(&bytes)
                })
            );
            assert_eq!(
                policy_selection_termination(&refusal),
                rejected(Detail::ConfigInvalid, &supplied_subject(&bytes, provenance))
            );
        }
    }
}

#[test]
fn a_selection_of_zero_or_several_sources_is_row_1_before_any_source_is_read() {
    let imperative = with("/exec", s("x"));
    let user = PackSource::Supplied {
        bytes: &imperative,
        provenance: SuppliedProvenance::User,
    };
    let preview = PackSource::Named("opensip.preview.typescript.pack:1");
    for (selection, n) in [
        (vec![], 0),
        (vec![preview, preview], 2),
        (vec![preview, user], 2),
        (vec![user, user, preview], 3),
    ] {
        let refusal = refuse(&selection);
        assert_eq!(refusal, PolicySelectionRefusal::Count(n));
        assert_eq!(
            policy_selection_termination(&refusal),
            rejected(Detail::ConfigInvalid, &format!("count:{n}"))
        );
    }
}

/// One refusal per row of item 7, with its subject.
fn every_row() -> Vec<(&'static str, PolicySelectionRefusal)> {
    let mut rows = vec![
        ("1", named("opensip.preview.typescript.pack:2")),
        ("1", refuse(&[])),
        ("2", supplied(TEST_DOCUMENT, SuppliedProvenance::ThirdParty)),
        (
            "3",
            supplied(&with("/rules/0/hook", s("x")), SuppliedProvenance::User),
        ),
        ("3a", supplied(b"\0asm", SuppliedProvenance::User)),
    ];
    // Row 4 is unreachable through the release registry (its one row admits,
    // and the schema sources are pinned), so its refusals are built directly,
    // one per defect.
    for defect in [
        PackDefect::Registry,
        PackDefect::Lexical,
        PackDefect::Imperative("/rules/0/exec".into()),
        PackDefect::Schema,
        PackDefect::Digest,
        PackDefect::RuleLaw("unknown relation".into()),
        PackDefect::Contribution("other".into()),
        PackDefect::Limit,
    ] {
        rows.push((
            "4",
            PolicySelectionRefusal::Pack(PackRefusal::HostInvariant {
                subject: format!("pack:{TEST_ID}"),
                defect,
            }),
        ));
    }
    rows
}

#[test]
fn every_row_maps_to_its_published_route_and_generated_members() {
    for (row, refusal) in every_row() {
        let t = policy_selection_termination(&refusal);
        let (class, exit, code, fault, detail) = match row {
            "1" | "2" | "3a" => (
                "request-rejected",
                2,
                "CONFIG.INVALID",
                "none",
                "CONFIG.INVALID",
            ),
            "3" => (
                "request-rejected",
                2,
                "CONFIG.INVALID",
                "none",
                "POLICY.IMPERATIVE_KEY_REFUSED",
            ),
            "4" => (
                "operational-failed",
                4,
                "SYSTEM.OUTCOME.ILLEGAL_STATE",
                "host-invariant",
                "HOST.INVARIANT_VIOLATED",
            ),
            other => panic!("{other}"),
        };
        assert_eq!(t.class, class.parse::<Class>().unwrap(), "{refusal:?}");
        assert_eq!(t.exit, exit, "{refusal:?}");
        assert_eq!(t.error_code, code.parse::<Code>().unwrap(), "{refusal:?}");
        assert_eq!(
            t.fault_cause,
            fault.parse::<Fault>().unwrap(),
            "{refusal:?}"
        );
        assert_eq!(
            t.detail,
            Some(detail.parse::<Detail>().unwrap()),
            "{refusal:?}"
        );
        let PolicySelectionRefusal::Pack(pack) = &refusal else {
            assert_eq!(t.subject.as_deref(), Some("count:0"));
            continue;
        };
        assert_eq!(t.subject, Some(pack.subject()), "{refusal:?}");
        if row == "4" {
            assert_eq!(
                t.subject.as_deref(),
                Some("pack:opensip.test.fixture.pack:1")
            );
        }
    }
    // The other two details item 7 names stay inside row 4's cause and never
    // reach the public detail, but are registered members all the same.
    for code in ["POLICY.UNKNOWN_RULE", "IMPORT.ABSENT_FOR_PREDICATE"] {
        assert!(code.parse::<Detail>().is_ok(), "{code}");
    }
}

#[test]
fn rows_1_2_and_3a_emit_the_s9_remedy_byte_for_byte() {
    assert_eq!(REMEDY_CONFIG_INVALID.len(), 706);
    assert!(REMEDY_CONFIG_INVALID.is_ascii());
    assert_eq!(
        digest_hex(&raw_sha256(REMEDY_CONFIG_INVALID.as_bytes())),
        S9_REMEDY_SHA256
    );
    for (row, refusal) in every_row() {
        let t = policy_selection_termination(&refusal);
        let (value, human) = envelope(&t);
        let remedy = match row {
            "1" | "2" | "3a" => REMEDY_CONFIG_INVALID,
            "3" => REMEDY_IMPERATIVE_KEY,
            _ => crate::doctor_ingress::REMEDY_INVARIANT,
        };
        let subject = t.subject.clone().unwrap();
        let detail = serde_json::json!({
            "code": t.detail.as_ref().unwrap().to_string(),
            "remedy": remedy,
            "subject": subject,
        });
        assert_eq!(value["termination"]["domainDetail"], detail, "{refusal:?}");
        assert_eq!(value["errors"], serde_json::json!([detail]), "{refusal:?}");
        assert_eq!(value["termination"]["errorCode"], t.error_code.to_string());
        assert_eq!(
            value["termination"].get("faultCause").is_some(),
            row == "4",
            "{refusal:?}"
        );
        let mut lines = vec![
            format!("Termination: {}", t.class),
            format!("Error: {}", t.error_code),
        ];
        if row == "4" {
            lines.push("Fault cause: host-invariant".to_owned());
        }
        lines.push(format!("Detail: {}", t.detail.as_ref().unwrap()));
        lines.push(format!("Subject: {subject}"));
        lines.push(format!("Remedy: {remedy}"));
        lines.push(format!("Request: {REQUEST}"));
        assert_eq!(human, lines.join("\n") + "\n", "{refusal:?}");
    }
}

#[test]
fn a_subject_beyond_the_bounded_text_is_never_truncated() {
    // The termination carries the presented ID unchanged; its envelope cannot
    // be projected, and is refused rather than truncated.
    let long = "a".repeat(1025);
    let t = policy_selection_termination(&named(&long));
    assert_eq!(t.subject.as_deref(), Some(long.as_str()));
    assert!(matches!(
        failure_envelope(REQUEST, None, &t),
        Err(crate::MetadataError::Projection)
    ));
    let fits = "a".repeat(1024);
    let t = policy_selection_termination(&named(&fits));
    assert_eq!(envelope(&t).0["errors"][0]["subject"], fits.as_str());
}

#[test]
fn a_host_fault_subject_matches_the_evaluators_own_subjects() {
    assert_eq!(
        host_fault_subject(&PackSource::Named("opensip.preview.typescript.pack:1")),
        "pack:opensip.preview.typescript.pack:1"
    );
    for provenance in BOTH {
        let evaluator = PackRefusal::SuppliedPack {
            provenance,
            sha256: raw_sha256(TEST_DOCUMENT),
        };
        assert_eq!(
            host_fault_subject(&PackSource::Supplied {
                bytes: TEST_DOCUMENT,
                provenance
            }),
            evaluator.subject()
        );
    }
}

/// configuration.rs without its test module.
fn production_source() -> &'static str {
    let text = include_str!("configuration.rs");
    let (production, tests) = text.split_once("#[cfg(test)]").unwrap();
    assert_eq!(
        tests.trim(),
        "mod tests {\n    include!(\"configuration_tests.rs\");\n    include!(\"configuration_resolver_tests.rs\");\n}"
    );
    production
}

#[test]
fn source_pin_admission_calls_only_admit_pack_and_reaches_nothing_else() {
    let source = production_source();
    // The only evaluator names are the boundary types and admit_pack.
    assert_eq!(source.matches("opensip_evaluator").count(), 1);
    assert!(source.contains(
        "use opensip_evaluator::{AdmittedPack, PackDefect, PackRefusal, PackSource, admit_pack};"
    ));
    assert_eq!(source.matches("admit_pack(").count(), 1);
    // The only crate calls: the embedded schema registry (pack admission and
    // configuration resolution), and the shared termination shape.
    let crate_uses: Vec<&str> = source
        .match_indices("crate::")
        .map(|(i, _)| &source[i..])
        .collect();
    assert_eq!(crate_uses.len(), 4);
    assert!(crate_uses[0].starts_with("crate::InstallationTerminationV1;"));
    assert!(crate_uses[1].starts_with("crate::invocation::InvocationModeV1;"));
    assert!(crate_uses[2].starts_with("crate::embedded_schema_registry()"));
    assert!(crate_uses[3].starts_with("crate::embedded_schema_registry()"));
    // No evaluation, provider, facts, Coverage, Plan, replay, custody,
    // storage, lock, ledger, I/O, environment or process.
    for forbidden in [
        "check_plan_pack",
        "compile_plan_policy",
        "inspect_",
        "replay",
        "evaluate",
        "provider",
        "snapshot",
        "coverage",
        "Coverage",
        "fact",
        "opensip_security",
        "opensip_storage",
        "opensip_platform",
        "opensip_lifecycle",
        "opensip_reporting",
        "std::fs",
        "std::env",
        "std::process",
        "std::io",
        "std::sync",
        "fs::",
        "env::",
        "Command",
        "Mutex",
        "OnceLock",
        " static ",
        "unsafe",
        "ledger",
        "fence",
        ".lock(",
    ] {
        let hits: Vec<&str> = source
            .lines()
            .filter(|l| !l.trim_start().starts_with("//"))
            .filter(|l| l.contains(forbidden))
            .collect();
        assert!(hits.is_empty(), "{forbidden}: {hits:?}");
    }
    // Item 8's order inside admission: the count, then the schema registry,
    // then the evaluator. A refusal returns before any AdmittedPack exists.
    let count = source
        .find("PolicySelectionRefusal::Count(selection.len())")
        .unwrap();
    let registry = source.find("crate::embedded_schema_registry()").unwrap();
    let admit = source.find("admit_pack(&schemas, source)").unwrap();
    assert!(count < registry && registry < admit);
    // The exhaustive match has no wildcard arm.
    assert!(!source.contains("_ =>"));
}
