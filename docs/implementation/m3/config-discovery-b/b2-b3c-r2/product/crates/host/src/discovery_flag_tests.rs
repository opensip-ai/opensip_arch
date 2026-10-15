// M3-B unit B2-b3c (B2-b3 plan r3, LD-B2B3-12): COV:5288 (`--project`) and
// COV:5388 (`--workspace-root`), through security's test-only scenario seam
// on the write path's analysis chain, with this crate's resolver (its flag
// layer and pack admission) deciding over the captured carriers. COV's owner
// path, `crates/host/tests/discovery_tests.rs`, stays planned for J1's public
// composition; until then the rows are verified here (plan r4 LD-B2B-7).
// Synthetic scratch installations only.

use crate::configuration::{
    CapturedCarrierV1, CompiledDefaultsV1, ComponentRequestV1, ComponentVersionV1, FlagLayerV1,
    LeafProvenanceV1, ProvenanceSourceV1, ResolvedConfigurationV1, ResolverInputV1,
    resolve_analysis_configuration,
};
use crate::invocation::InvocationModeV1;
use opensip_identity::JsonValue as V;
use opensip_security::scenario::{DiscoveryRecords, DiscoveryRequest, ScenarioHome};
use std::cell::RefCell;
use std::rc::Rc;

fn carrier(name: &str, bytes: &[u8]) -> CapturedCarrierV1 {
    CapturedCarrierV1 {
        path: format!("{name}.json"),
        bytes: bytes.to_vec(),
    }
}
/// The B1-a vectors' `base` compiled defaults (configuration_vectors.json),
/// non-interactive, with no carrier and no flag.
fn base() -> ResolverInputV1 {
    let strings = |items: &[&str]| items.iter().map(|s| (*s).to_owned()).collect::<Vec<_>>();
    ResolverInputV1 {
        defaults: CompiledDefaultsV1 {
            profile_id: Some("default".to_owned()),
            capabilities: Some(strings(&[
                "inventory",
                "syntax",
                "imports",
                "references",
                "calls",
                "types",
                "reachability",
                "clones-fact",
                "clones-near",
                "clones-cross-tsjs",
                "unresolved-edge",
            ])),
            budget_limit: Some(1000),
            request: Some(vec![ComponentRequestV1::Version(ComponentVersionV1 {
                stable_id: "0f0e0d0c-0b0a-4908-8706-050403020100".to_owned(),
                version: "1.2.3".to_owned(),
            })]),
            pins: Some(Vec::new()),
            holds: Some(Vec::new()),
            allowed_scopes: Some(strings(&["project", "global"])),
            pack_ids: Some(strings(&["opensip.preview.typescript.pack:1"])),
        },
        global: None,
        project: None,
        local: None,
        flags: FlagLayerV1::default(),
        mode: InvocationModeV1 { interactive: false },
    }
}

/// The winning `discovery.workspaceRoots` of a resolved configuration.
fn workspace_roots(resolved: &ResolvedConfigurationV1) -> Option<Vec<String>> {
    let V::Object(semantic) = &resolved.semantic else {
        return None;
    };
    let Some(V::Object(discovery)) = semantic.get("discovery") else {
        return None;
    };
    match discovery.get("workspaceRoots") {
        Some(V::Array(roots)) => Some(
            roots
                .iter()
                .map(|r| match r {
                    V::String(s) => s.clone(),
                    other => panic!("{other:?}"),
                })
                .collect(),
        ),
        _ => None,
    }
}

/// The resolution the analysis path runs on the captured carriers: this
/// crate's resolver with the flag layer (`--workspace-root`, layer 6) and
/// pack admission. It records the winning roots' provenance.
#[allow(clippy::type_complexity)]
fn resolution(
    cli: Option<&[&str]>,
    seen: &Rc<RefCell<Option<LeafProvenanceV1>>>,
) -> impl FnOnce(Option<&[u8]>, Option<&[u8]>) -> Result<Option<Vec<String>>, String> {
    let cli: Option<Vec<String>> = cli.map(|roots| roots.iter().map(|r| (*r).to_owned()).collect());
    let seen = Rc::clone(seen);
    move |project, local| {
        let mut input = base();
        input.project = project.map(|bytes| carrier("project", bytes));
        input.local = local.map(|bytes| carrier("local", bytes));
        input.flags.workspace_roots = cli;
        let (resolved, _pack) =
            resolve_analysis_configuration(&input).map_err(|refusal| format!("{refusal:?}"))?;
        *seen.borrow_mut() = resolved.provenance.get("discovery.workspaceRoots").cloned();
        Ok(workspace_roots(&resolved))
    }
}

fn project_with(
    home: &ScenarioHome,
    name: &str,
    dirs: &[&str],
    config: Option<&str>,
) -> std::path::PathBuf {
    use std::os::unix::fs::PermissionsExt;
    let root = home.project(name);
    for dir in dirs {
        let path = root.join(dir);
        std::fs::create_dir(&path).unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o755)).unwrap();
        let marker = path.join("package.json");
        std::fs::write(&marker, b"{}").unwrap();
        std::fs::set_permissions(&marker, std::fs::Permissions::from_mode(0o644)).unwrap();
    }
    if let Some(text) = config {
        let path = root.join("opensip.json");
        std::fs::write(&path, text.as_bytes()).unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o644)).unwrap();
    }
    root
}

fn discover(
    home: &ScenarioHome,
    launch: &std::path::Path,
    explicit: Option<&std::path::Path>,
    trust_project_owner: bool,
    cli: Option<&[&str]>,
) -> (Result<DiscoveryRecords, String>, Option<LeafProvenanceV1>) {
    let seen = Rc::new(RefCell::new(None));
    let request = DiscoveryRequest {
        launch,
        explicit,
        trust_project_owner,
    };
    let records = home.discover(&request, resolution(cli, &seen));
    let provenance = seen.borrow().clone();
    (records, provenance)
}
fn units_under(records: &DiscoveryRecords, root: &std::path::Path) -> Vec<String> {
    let base = format!("{}/", root.to_str().unwrap());
    records
        .units
        .iter()
        .map(|u| u.strip_prefix(&base).unwrap_or(u).to_owned())
        .collect()
}

#[test]
fn project_selects_exactly_its_path_examined_once_and_never_walked_upward() {
    // COV:5288: `--project` names the root; the launch elsewhere is not
    // walked, and the root's subtree is discovered automatically.
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = project_with(&home, "b2b3c-project", &["a"], None);
    let elsewhere = project_with(&home, "b2b3c-elsewhere", &["z"], None);
    let (records, _) = discover(&home, &elsewhere, Some(&root), false, None);
    let records = records.unwrap();
    assert_eq!(records.mode.as_deref(), Some("explicit"));
    assert_eq!(records.stop.as_deref(), Some("EXPLICIT"));
    assert!(records.resolved && records.phase_two && records.walked);
    assert_eq!(records.unit_source.as_deref(), Some("automatic"));
    assert_eq!(units_under(&records, &root), vec!["a".to_owned()]);
    assert_eq!(records.custody_waiver, None);
    // An absent explicit path refuses at selection, before any resolution.
    let (records, _) = discover(&home, &elsewhere, Some(&root.join("absent")), false, None);
    let records = records.unwrap();
    assert_eq!(
        records.refusal,
        Some((
            "PROJECT.EXPLICIT_PATH_INVALID".to_owned(),
            "ABSENT".to_owned()
        ))
    );
    assert!(!records.resolved && !records.phase_two && !records.walked);
}

#[test]
fn trust_project_owner_reaches_only_the_owner_check_of_its_explicit_root() {
    // COV:5288 with `--trust-project-owner`: the waiver is recorded and
    // never reaches the mode; without `--project` it cannot be built. (A
    // foreign owner cannot be made on a scratch tree; B2-b3a's and B2-b3b's
    // vectors hold that case.)
    use std::os::unix::fs::PermissionsExt;
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = project_with(&home, "b2b3c-waived", &["a"], None);
    let (records, _) = discover(&home, &root, Some(&root), true, None);
    let records = records.unwrap();
    assert_eq!(records.custody_waiver.as_deref(), Some("trustProjectOwner"));
    assert!(records.walked);
    assert_eq!(units_under(&records, &root), vec!["a".to_owned()]);
    let open = project_with(&home, "b2b3c-open", &[], None);
    std::fs::set_permissions(&open, std::fs::Permissions::from_mode(0o777)).unwrap();
    let (records, _) = discover(&home, &open, Some(&open), true, None);
    let records = records.unwrap();
    assert_eq!(
        records.refusal,
        Some((
            "PROJECT.ROOT_CUSTODY_REFUSED".to_owned(),
            "WRITABLE_BY_OTHERS".to_owned()
        ))
    );
    assert!(!records.resolved);
    let (records, _) = discover(&home, &root, None, true, None);
    assert!(
        records
            .unwrap_err()
            .contains("OwnerWaiverWithoutExplicitProject")
    );
}

#[test]
fn configuration_never_impersonates_explicit_consent() {
    // A project configuration naming the project or the owner waiver is
    // refused by the resolver, before item 5 and before any downward
    // observation; its waiver is never recorded.
    let home = ScenarioHome::create(&std::env::temp_dir());
    for (name, text) in [
        (
            "b2b3c-config-project",
            r#"{"schemaVersion":2,"project":"/elsewhere"}"#,
        ),
        (
            "b2b3c-config-waiver",
            r#"{"schemaVersion":2,"trustProjectOwner":true}"#,
        ),
    ] {
        let root = project_with(&home, name, &["a"], Some(text));
        let (records, _) = discover(&home, &root, None, false, None);
        let records = records.unwrap();
        assert!(records.resolved, "{name}");
        assert!(records.resolution_refusal.is_some(), "{name}");
        assert!(!records.phase_two && !records.walked, "{name}");
        assert_eq!(records.custody_waiver, None, "{name}");
    }
}

#[test]
fn a_workspace_root_flag_wins_over_the_project_configuration_and_never_falls_through() {
    // COV:5388: the flag layer wins over the project's
    // `discovery.workspaceRoots` (its provenance is the flag layer), and is
    // `config-workspace-roots`; a named root that is absent refuses rather
    // than falling through to automatic.
    let home = ScenarioHome::create(&std::env::temp_dir());
    let config = r#"{"schemaVersion":2,"discovery":{"workspaceRoots":["a"]}}"#;
    let root = project_with(&home, "b2b3c-flag", &["a", "b"], Some(config));
    let (records, provenance) = discover(&home, &root, None, false, Some(&["b"]));
    let records = records.unwrap();
    assert_eq!(records.mode.as_deref(), Some("config"));
    assert_eq!(
        records.unit_source.as_deref(),
        Some("config-workspace-roots")
    );
    assert_eq!(units_under(&records, &root), vec!["b".to_owned()]);
    let provenance = provenance.unwrap();
    // The deciding layer (the generated registries' type is private to the
    // configuration module): layer 6, the flags.
    assert_eq!(format!("{:?}", provenance.layer), "Flags");
    assert_eq!(provenance.source, ProvenanceSourceV1::Flags);
    let (records, _) = discover(&home, &root, None, false, Some(&["missing"]));
    let records = records.unwrap();
    assert!(records.walked);
    // The refusal's own record keeps the flag's source: no fall-through.
    assert_eq!(
        records.unit_source.as_deref(),
        Some("config-workspace-roots")
    );
    assert!(records.units.is_empty());
    assert_eq!(
        records.refusal,
        Some((
            "PROJECT.EXPLICIT_PATH_INVALID".to_owned(),
            "ABSENT".to_owned()
        ))
    );
}

#[test]
fn the_configuration_alone_gives_its_roots_and_neither_gives_automatic() {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let config = r#"{"schemaVersion":2,"discovery":{"workspaceRoots":["a"]}}"#;
    let root = project_with(&home, "b2b3c-config", &["a", "b"], Some(config));
    let (records, provenance) = discover(&home, &root, None, false, None);
    let records = records.unwrap();
    assert_eq!(
        records.unit_source.as_deref(),
        Some("config-workspace-roots")
    );
    assert_eq!(units_under(&records, &root), vec!["a".to_owned()]);
    assert!(matches!(
        provenance.unwrap().source,
        ProvenanceSourceV1::Carrier { .. }
    ));
    let plain = project_with(&home, "b2b3c-plain", &["a", "b"], None);
    let (records, provenance) = discover(&home, &plain, None, false, None);
    let records = records.unwrap();
    assert_eq!(records.unit_source.as_deref(), Some("automatic"));
    let mut units = units_under(&records, &plain);
    units.sort();
    assert_eq!(units, vec!["a".to_owned(), "b".to_owned()]);
    assert!(provenance.is_none_or(|p| p.source == ProvenanceSourceV1::Defaulted));
}

#[test]
fn a_resolution_refusal_never_reaches_item_5_or_the_walk() {
    // The r2 control (plan r2 B2B3PLAN-3), kept in r3: a refused pack and a
    // refused flag value each end the discovery at resolution.
    let home = ScenarioHome::create(&std::env::temp_dir());
    let refused = r#"{"schemaVersion":2,"policy":{"packIds":["other.pack:1"]}}"#;
    let root = project_with(&home, "b2b3c-refused", &["a"], Some(refused));
    let (records, _) = discover(&home, &root, None, false, None);
    let records = records.unwrap();
    assert!(records.resolved && records.resolution_refusal.is_some());
    assert!(!records.phase_two && !records.walked);
    let plain = project_with(&home, "b2b3c-empty-flag", &["a"], None);
    let (records, _) = discover(&home, &plain, None, false, Some(&[]));
    let records = records.unwrap();
    assert!(records.resolution_refusal.is_some());
    assert!(!records.phase_two && !records.walked);
}

#[test]
fn selection_and_discovery_lend_nothing() {
    // The records are plain values; the seam hands back no admission,
    // operation or root, and the writer and fence are released afterwards.
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = project_with(&home, "b2b3c-plain-values", &["a"], None);
    let (records, _) = discover(&home, &root, Some(&root), false, None);
    let records: DiscoveryRecords = records.unwrap();
    let copy = records.clone();
    assert_eq!(records, copy);
    // The operation's end is disclosed: entered, with no rollover and no
    // end-path failure (r2, Codex B2B3C-R1-RF-1).
    assert!(records.end_entered && !records.end_rolled_over);
    assert_eq!(records.end_failure, None);
    assert!(
        records
            .inventory
            .as_deref()
            .is_some_and(|j| j.contains("\"schemaVersion\":3"))
    );
    // A second discovery of the same root opens a new writer: nothing held.
    let (again, _) = discover(&home, &root, Some(&root), false, None);
    assert_eq!(units_under(&again.unwrap(), &root), vec!["a".to_owned()]);
}
