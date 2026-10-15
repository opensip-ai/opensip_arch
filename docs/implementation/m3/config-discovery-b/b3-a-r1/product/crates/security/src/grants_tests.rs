// Unit B3-a's controls (M3-B r5 item 23). SLM byte vectors from
// tools/security/storage_choice_vectors.py; synthetic values otherwise.
use super::*;
use opensip_identity::{JsonValue as V, parse_json};
use std::path::Path;

const VECTORS: &[u8] = include_bytes!("storage_choice_vectors.json");
const SOURCE: &str = include_str!("grants.rs");

/// The module's code with every `//` comment removed (it has no string
/// containing `//`).
fn code() -> String {
    SOURCE
        .lines()
        .map(|line| line.split("//").next().unwrap())
        .collect::<Vec<_>>()
        .join("\n")
}

/// Compile-time: the record does not implement the trait. Two blanket impls
/// of a probe trait make the probe ambiguous, and the build fails, exactly
/// when the record implements it.
macro_rules! assert_not_impl {
    ($ty:ty: $($tr:path),+ $(,)?) => {$(
        const _: fn() = || {
            trait AmbiguousIfImpl<A> {
                fn probe() {}
            }
            impl<T: ?Sized> AmbiguousIfImpl<()> for T {}
            struct Implemented;
            impl<T: ?Sized + $tr> AmbiguousIfImpl<Implemented> for T {}
            let _ = <$ty as AmbiguousIfImpl<_>>::probe;
        };
    )+};
}
macro_rules! assert_no_configuration_path {
    ($($ty:ty),+ $(,)?) => {$(
        assert_not_impl!($ty: Clone, Copy, Default, From<bool>, From<u32>, From<&'static [u32]>,
            From<Vec<u32>>, From<&'static str>, From<String>, From<&'static Path>,
            From<std::path::PathBuf>, From<V>, From<&'static V>, TryFrom<bool>, TryFrom<&'static [u32]>,
            TryFrom<Vec<u32>>, TryFrom<&'static str>, TryFrom<String>, TryFrom<V>,
            TryFrom<&'static V>, std::str::FromStr);
    )+};
}
assert_no_configuration_path!(
    AuthorizedGroups,
    ProjectOwnerWaiver,
    BackupCustodyAcknowledgement,
    PolicyRecordId,
    ConsentSource,
);

fn hex(n: usize) -> String {
    "0123456789abcdef".repeat(4)[..n].to_owned()
}

#[test]
fn authorized_groups_collapse_duplicates_and_bound_distinct_gids() {
    let none = AuthorizedGroups::from_invocation(&[]).unwrap();
    assert!(none.provenance().is_empty() && none.as_set().is_empty());
    let one = AuthorizedGroups::from_invocation(&[20]).unwrap();
    assert!(one.contains(20) && !one.contains(21));
    // LD-B3A-3: a repeat authorizes once; provenance keeps first occurrence.
    let repeated = AuthorizedGroups::from_invocation(&[30, 20, 30, 10, 20]).unwrap();
    assert_eq!(repeated.provenance(), &[30, 20, 10]);
    assert_eq!(
        repeated.as_set().iter().copied().collect::<Vec<_>>(),
        [10, 20, 30]
    );
    let sixty_four: Vec<u32> = (0..64).collect();
    let at_bound = AuthorizedGroups::from_invocation(&sixty_four).unwrap();
    assert_eq!(at_bound.provenance(), sixty_four.as_slice());
    // The bound counts distinct gids: 64 distinct with repeats is admitted.
    let mut repeats = sixty_four.clone();
    repeats.extend_from_slice(&[0, 63, 7]);
    assert_eq!(
        AuthorizedGroups::from_invocation(&repeats)
            .unwrap()
            .provenance()
            .len(),
        64
    );
    // LD-B3A-2: 65 distinct refuses, never truncates, and has no M3 row.
    let sixty_five: Vec<u32> = (0..65).collect();
    let refusal = AuthorizedGroups::from_invocation(&sixty_five).unwrap_err();
    assert_eq!(refusal, GrantRefusal::TooManyGroups { count: 65 });
    assert_eq!(refusal.termination(), None);
    let mut many: Vec<u32> = (0..200).rev().collect();
    many.extend(0..200);
    assert_eq!(
        AuthorizedGroups::from_invocation(&many),
        Err(GrantRefusal::TooManyGroups { count: 200 })
    );
}

#[test]
fn owner_waiver_needs_an_explicit_project() {
    let root = Path::new("/Users/someone/work/app");
    assert_eq!(ProjectOwnerWaiver::from_invocation(false, None), Ok(None));
    assert_eq!(
        ProjectOwnerWaiver::from_invocation(false, Some(root)),
        Ok(None)
    );
    let refusal = ProjectOwnerWaiver::from_invocation(true, None).unwrap_err();
    assert_eq!(refusal, GrantRefusal::OwnerWaiverWithoutExplicitProject);
    assert_eq!(
        refusal.termination(),
        Some(InstallationTermination::ProjectExplicitPath)
    );
    let waiver = ProjectOwnerWaiver::from_invocation(true, Some(root))
        .unwrap()
        .unwrap();
    assert_eq!(waiver.explicit_root(), root);
    // The spelling is carried as given, not normalized.
    let spelled = Path::new("/Users/someone/work/./app/");
    let waiver = ProjectOwnerWaiver::from_invocation(true, Some(spelled))
        .unwrap()
        .unwrap();
    assert_eq!(waiver.explicit_root().as_os_str(), spelled.as_os_str());
}

#[test]
fn backup_custody_acknowledgement_is_the_flag() {
    assert!(BackupCustodyAcknowledgement::from_invocation(true).is_some());
    assert!(BackupCustodyAcknowledgement::from_invocation(false).is_none());
}

#[test]
fn policy_record_ids_are_sixty_four_lowercase_hex_digits() {
    let id = PolicyRecordId::parse(&hex(64)).unwrap();
    assert_eq!(id.as_str(), hex(64));
    for bad in [
        String::new(),
        hex(63),
        hex(64) + "0",
        hex(64).to_uppercase(),
        "g".repeat(64),
        // SLM's Python `$` admits this one; the record grammar does not.
        hex(64) + "\n",
        format!(" {}", hex(63)),
        "\u{0660}".repeat(32),
    ] {
        let refusal = PolicyRecordId::parse(&bad).unwrap_err();
        assert_eq!(refusal, GrantRefusal::PolicyRecordId, "{bad:?}");
        assert_eq!(refusal.termination(), None);
    }
}

#[test]
fn consent_sources_map_to_grant_modes() {
    let policy = ConsentSource::PreExistingPolicy {
        record: PolicyRecordId::parse(&hex(64)).unwrap(),
    };
    assert_eq!(
        (policy.workflow(), policy.grant_mode()),
        ("pre-existing-policy", "policy-record")
    );
    let interactive = ConsentSource::InteractiveConsent;
    assert_eq!(
        (interactive.workflow(), interactive.grant_mode()),
        ("interactive-consent", "interactive-explicit")
    );
}

fn field<'v>(value: &'v V, key: &str) -> &'v V {
    let V::Object(fields) = value else { panic!() };
    &fields[key]
}
fn text(value: &V) -> &str {
    let V::String(s) = value else {
        panic!("{value:?}")
    };
    s
}
fn flag(value: &V) -> bool {
    let V::Bool(b) = value else {
        panic!("{value:?}")
    };
    *b
}

#[test]
fn every_slm_vector_is_reproduced() {
    let vectors = parse_json(VECTORS).unwrap();
    // The vectors were computed by SLM at its accepted bytes.
    let V::Array(sources) = field(&vectors, "sources") else {
        panic!()
    };
    assert_eq!(
        text(field(&sources[0], "path")),
        "docs/coop/design-corrections/security/security_lifecycle_model_v1.py"
    );
    assert_eq!(
        text(field(&sources[0], "sha256")),
        "d0ef9814d27b86f10bdc1aa9a9a4781124c93c3dd92eeecdfe3090fe21d18bb9"
    );
    let V::Array(cases) = field(&vectors, "cases") else {
        panic!()
    };
    // Every combination of SLM's five inputs.
    assert_eq!(cases.len(), 3 * 2 * 2 * 6 * 2);
    let (mut refused, mut by_record) = (0, 0);
    for case in cases {
        let backup = match text(field(case, "backup")) {
            "BACKED_UP" => BackupClassification::BackedUp,
            "NOT_BACKED_UP" => BackupClassification::NotBackedUp,
            "UNKNOWN" => BackupClassification::Unknown,
            other => panic!("{other}"),
        };
        let record = match field(case, "admittedPolicyRecord") {
            V::Null => None,
            value => PolicyRecordId::parse(text(value)).ok(),
        };
        let ci = flag(field(case, "ci"));
        let choice = storage_write_choice(
            backup,
            flag(field(case, "ephemeral")),
            BackupCustodyAcknowledgement::from_invocation(flag(field(case, "allowBackupCustody"))),
            record.as_ref(),
            ci,
        );
        let slm = field(case, "slm");
        assert_eq!(choice.choice(), text(field(slm, "choice")), "{case:?}");
        assert!(!flag(field(slm, "policyFileWritten")) && !StorageWriteChoice::POLICY_FILE_WRITTEN);
        assert!(
            !flag(field(slm, "rootIdentityChanged")) && !StorageWriteChoice::ROOT_IDENTITY_CHANGED
        );
        match text(field(slm, "result")) {
            "ADMIT" => {
                assert!(matches!(choice, StorageWriteChoice::Admit(_)), "{case:?}");
                assert_eq!(choice.termination(), None);
                by_record += usize::from(matches!(
                    choice,
                    StorageWriteChoice::Admit(StorageWriteBasis::AdmittedPolicyRecord(_))
                ));
            }
            "REFUSE" => {
                assert_eq!(choice, StorageWriteChoice::Refuse { ci }, "{case:?}");
                // The row the host projects `BackupChoiceRequired` onto.
                assert_eq!(
                    choice.termination(),
                    Some(InstallationTermination::BackupChoiceRequired)
                );
                assert_eq!(text(field(slm, "refusal")), "REQUEST.PRECONDITION_FAILED");
                assert_eq!(text(field(slm, "detail")), "storage.backup-choice-required");
                let d9 = field(slm, "d9");
                assert_eq!(text(field(d9, "class")), "request-rejected");
                assert_eq!(text(field(d9, "code")), "REQUEST.PRECONDITION_FAILED");
                assert_eq!(
                    field(d9, "exit"),
                    &V::Integer(opensip_identity::JsonInteger::new(2).unwrap())
                );
                refused += 1;
            }
            other => panic!("{other}"),
        }
    }
    // Both refusal spellings and the record branch are exercised.
    assert_eq!((refused, by_record), (10, 2));
}

#[test]
fn the_choice_order_is_the_references() {
    use BackupClassification::{BackedUp, NotBackedUp, Unknown};
    let id = PolicyRecordId::parse(&hex(64)).unwrap();
    let ack = || BackupCustodyAcknowledgement::from_invocation(true);
    // Ephemeral beats every other input.
    for backup in [BackedUp, NotBackedUp, Unknown] {
        assert_eq!(
            storage_write_choice(backup, true, ack(), Some(&id), true),
            StorageWriteChoice::Admit(StorageWriteBasis::Ephemeral)
        );
    }
    // UNKNOWN admits, disclosed, without the flag or a record.
    assert_eq!(
        storage_write_choice(Unknown, false, None, None, true),
        StorageWriteChoice::Admit(StorageWriteBasis::UnknownDisclosed)
    );
    assert_eq!(
        storage_write_choice(NotBackedUp, false, ack(), Some(&id), false),
        StorageWriteChoice::Admit(StorageWriteBasis::NotRequired)
    );
    // The flag beats an admitted record.
    assert_eq!(
        storage_write_choice(BackedUp, false, ack(), Some(&id), true),
        StorageWriteChoice::Admit(StorageWriteBasis::InvocationFlag)
    );
    assert_eq!(
        storage_write_choice(BackedUp, false, None, Some(&id), true),
        StorageWriteChoice::Admit(StorageWriteBasis::AdmittedPolicyRecord(&id))
    );
    assert_eq!(
        storage_write_choice(BackedUp, false, None, None, true).choice(),
        "interactive-prompt-unavailable"
    );
    assert_eq!(
        storage_write_choice(BackedUp, false, None, None, false).choice(),
        "interactive-choice-required"
    );
}

fn crate_root() -> &'static Path {
    Path::new(env!("CARGO_MANIFEST_DIR"))
}
fn rust_sources(dir: &Path, out: &mut Vec<std::path::PathBuf>) {
    for entry in std::fs::read_dir(dir).unwrap() {
        let path = entry.unwrap().path();
        if path.is_dir() {
            rust_sources(&path, out);
        } else if path.extension().is_some_and(|e| e == "rs") {
            out.push(path);
        }
    }
}
const RECORDS: [&str; 5] = [
    "AuthorizedGroups",
    "ProjectOwnerWaiver",
    "BackupCustodyAcknowledgement",
    "PolicyRecordId",
    "ConsentSource",
];

#[test]
fn no_configuration_path_reaches_a_grant() {
    // No conversion or default in the module; only `Debug`, `PartialEq` and
    // `Eq` are derived.
    for forbidden in [
        "impl From",
        "impl TryFrom",
        "impl Default",
        "impl Clone",
        "impl<",
        "FromStr",
        "Deserialize",
        "serde",
        "Clone",
        "Copy",
    ] {
        assert!(!code().contains(forbidden), "{forbidden}");
    }
    for line in SOURCE.lines().filter(|l| l.contains("#[derive(")) {
        assert_eq!(line.trim(), "#[derive(Debug, PartialEq, Eq)]");
    }
    // No other module implements anything for a record.
    let mut files = Vec::new();
    rust_sources(&crate_root().join("src"), &mut files);
    for file in &files {
        if file.ends_with("grants.rs") || file.ends_with("grants_tests.rs") {
            continue;
        }
        let source = std::fs::read_to_string(file).unwrap();
        for line in source.lines().filter(|l| l.contains("impl")) {
            for record in RECORDS {
                assert!(!line.contains(record), "{}: {line}", file.display());
            }
        }
    }
    // The module is private and re-exported nowhere, so no other crate, and
    // no host configuration type, can name a record.
    let lib = std::fs::read_to_string(crate_root().join("src/lib.rs")).unwrap();
    assert!(lib.contains("\nmod grants;\n"));
    assert!(!lib.contains("pub mod grants") && !lib.contains("grants::"));
    // The crate has no serde, so no record can be `Deserialize`.
    let manifest = std::fs::read_to_string(crate_root().join("Cargo.toml")).unwrap();
    assert!(!manifest.contains("serde"));
    // The resolver's inputs carry no grant and no durability.
    let host = crate_root().join("../host/src");
    for name in ["configuration.rs", "configuration_tables.rs"] {
        let source = std::fs::read_to_string(host.join(name)).unwrap();
        for record in RECORDS {
            assert!(!source.contains(record), "{name}: {record}");
        }
        assert!(!source.contains("Durability"), "{name}");
    }
}

#[test]
fn the_module_is_pure() {
    for forbidden in [
        "std::fs",
        "std::io",
        "std::env",
        "std::process",
        "std::net",
        "opensip_platform",
        "unsafe",
    ] {
        assert!(!code().contains(forbidden), "{forbidden}");
    }
    let uses: Vec<&str> = SOURCE.lines().filter(|l| l.starts_with("use ")).collect();
    assert_eq!(
        uses,
        [
            "use crate::InstallationTermination;",
            "use crate::initial_installation::BackupClassification;",
            "use std::collections::BTreeSet;",
            "use std::path::{Path, PathBuf};",
        ]
    );
}
