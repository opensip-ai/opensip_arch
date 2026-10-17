//! Registry rendering and controls, excluded from production source scanning.
use super::super::super::constants::Level;
use super::super::{Code, Flag, Form, PrivacyClass, SafeField};
use super::{
    BoundedWait, ControlCancelReason, ExitClass, FaultSource, ForceTrigger, LimitKind, LimitUnit,
    LivenessMiss, ProtocolMajor, ProviderFaultReduced, ProviderProcessReady,
    ProviderProcessSpawned, ProviderResourcesReported, ProviderRole, ProviderStderrReduced,
    RefusalFamily, RssUnit, RustDetailCode, RustFaultKind, ScratchRetainedReason,
    SupervisionCancelForced, SupervisionCancelSent, SupervisionLimitBreached,
    SupervisionLivenessMissed, SupervisionSampleIncomplete, SupervisionScratchRetained,
    SupervisionSettled, SupervisionTeardownStarted, SupervisionTreeSwept, SupervisionWaitExpired,
    TeardownCause, ToolProcessReaped, ToolProcessSpawned,
};
use super::{
    BuildProfile, CapabilitySet, CodeEnum, CommitNotPublished, Event, HostPhaseCompleted,
    HostPhaseStarted, HostRepairCompleted, IdentitySet, IoErrorKind, LogLossCounted,
    LogStreamOpened, PHASE_PARENT, PathAnchor, Phase, PhaseOutcome, Platform, RepairKind,
    RepairState, Sink, StorageCommitNotPublished, StorageCommitPublished, event_name_ok,
};
use super::{TableRegistration, code_seal};

#[test]
fn o1d1_compiled_facts_and_actual_error_capture() {
    use super::{BuildProfile, IoErrorKind, Platform};
    let expected = if cfg!(debug_assertions) {
        "debug-assertions-on"
    } else {
        "debug-assertions-off"
    };
    assert_eq!(Code::from_enum(BuildProfile::compiled()).text(), expected);
    assert_eq!(
        Platform::TEXT,
        &[
            "linux-aarch64-gnu",
            "linux-x86_64-gnu",
            "macos-aarch64",
            "macos-x86_64"
        ]
    );
    if cfg!(all(target_os = "macos", target_arch = "aarch64")) {
        assert_eq!(Platform::compiled(), Some(Platform::MacosAarch64));
    }
    for (error, expected) in [
        (
            std::io::Error::from(std::io::ErrorKind::PermissionDenied),
            IoErrorKind::PermissionDenied,
        ),
        (
            std::io::Error::from(std::io::ErrorKind::StorageFull),
            IoErrorKind::NoSpace,
        ),
        (
            std::io::Error::from(std::io::ErrorKind::WriteZero),
            IoErrorKind::Other,
        ),
    ] {
        let (kind, errno) = IoErrorKind::capture(&error);
        assert_eq!(kind, expected);
        assert!(errno.is_none());
    }
    #[cfg(target_os = "macos")]
    for (raw, expected) in [
        (13, IoErrorKind::PermissionDenied),
        (28, IoErrorKind::NoSpace),
        (5, IoErrorKind::IoError),
    ] {
        let error = std::io::Error::from_raw_os_error(raw);
        let (kind, errno) = IoErrorKind::capture(&error);
        assert_eq!(kind, expected);
        assert_eq!(errno.map(super::super::Errno::get), Some(raw));
    }
}

#[test]
fn o1d1_stream_schema_projects_pid_only_at_p1() {
    use super::{BuildProfile, LogStreamOpened, Platform, Version};
    let set = CapabilitySet::issue();
    let event = LogStreamOpened::new(
        Version::RELEASE,
        Code::from_enum(Platform::MacosAarch64),
        Code::from_enum(BuildProfile::compiled()),
        Code::from_enum(Sink::Stderr),
        set.process_id.pid(1).unwrap(),
    );
    assert_eq!(
        LogStreamOpened::FIELD_KEYS,
        &["version", "platform", "build", "sink", "pid"]
    );
    assert_eq!(LogStreamOpened::REQUIRES, IdentitySet::Request);
    const {
        assert!(!LogStreamOpened::EXPORT);
    }
    let mut out = Vec::new();
    assert_eq!(event.project_fields(PrivacyClass::P0, &mut out), 1);
    assert!(!out.windows(5).any(|bytes| bytes == b"\"pid\""));
    out.clear();
    assert_eq!(event.project_fields(PrivacyClass::P1, &mut out), 0);
    assert!(out.ends_with(b"\"pid\":1}"));
    assert!(out.len() <= LogStreamOpened::MAX_LINE);
}

#[test]
fn named_tables_round_trip_their_literals() {
    let registration = Code::from_enum(RepairKind::Registration);
    assert_eq!(registration.text(), "registration");
    let mut out = Vec::new();
    registration.encode(Form::Json, &mut out);
    assert_eq!(out, br#""registration""#);
    out.clear();
    registration.encode(Form::Human, &mut out);
    assert_eq!(out, br#""registration""#);
    assert_eq!(Code::from_enum(RepairState::RwT3).text(), "RW-T3");
    assert_eq!(
        Code::from_enum(Phase::ProviderAnalysis).text(),
        "provider.analysis"
    );
    assert_eq!(PHASE_PARENT[Phase::Request.index() as usize], None);
    assert_eq!(
        PHASE_PARENT[Phase::ProviderStart.index() as usize],
        Some(Phase::Provider)
    );
    assert_eq!(
        Code::from_enum(PathAnchor::SystemTemp).text(),
        "system-temp"
    );
    assert_eq!(Code::from_enum(Sink::Stderr).text(), "stderr");
    assert_eq!(
        Code::from_enum(CommitNotPublished::Undetermined).text(),
        "undetermined"
    );
}

#[test]
fn o1a_events_match_the_named_rows() {
    assert!(event_name_ok(HostRepairCompleted::NAME));
    assert_eq!(HostRepairCompleted::LEVEL, Level::Info);
    assert_eq!(HostRepairCompleted::REQUIRES, IdentitySet::Request);
    const {
        assert!(!HostRepairCompleted::EXPORT);
    }
    assert_eq!(
        HostRepairCompleted::MAX_LINE,
        768 + (4 + 4 + 66) + (5 + 4 + 66)
    );
    let repair = HostRepairCompleted::new(
        Code::from_enum(RepairKind::TrustDependency),
        Code::from_enum(RepairState::RwL1),
    );
    assert_eq!(repair.kind.text(), "trust-dependency");

    let set = CapabilitySet::issue();
    let published = StorageCommitPublished::new(&set.storage, Flag::new(true));
    assert!(published.latched.get());
    assert_eq!(
        StorageCommitPublished::REQUIRES,
        IdentitySet::ProjectPlanExecutionRun
    );
    const {
        assert!(StorageCommitPublished::EXPORT);
    }
    assert_eq!(StorageCommitPublished::MAX_LINE, 768 + 7 + 4 + 5);

    let withheld =
        StorageCommitNotPublished::new(&set.storage, Code::from_enum(CommitNotPublished::Refused));
    assert_eq!(withheld.outcome.text(), "refused");
    assert_eq!(
        StorageCommitNotPublished::REQUIRES,
        IdentitySet::ProjectPlanExecution
    );
    assert_eq!(StorageCommitNotPublished::MAX_LINE, 768 + 7 + 4 + 66);
    // M3-D unit D3a-3 registers the `tool` domain (SOP2 item 3); an unlisted
    // domain is still refused.
    assert!(event_name_ok("tool.process.spawned"));
    assert!(!event_name_ok("tools.process.spawned"));
    assert!(!event_name_ok("host.repair"));
    assert!(!event_name_ok("HOST.repair.completed"));
}

struct Table {
    name: &'static str,
    role: &'static str,
    cap: usize,
    members: &'static [&'static str],
    provenance: &'static str,
}

fn tables() -> Vec<Table> {
    vec![
        Table {
            name: "Phase",
            role: "header",
            cap: Phase::CAP,
            members: Phase::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "PhaseOutcome",
            role: "code",
            cap: PhaseOutcome::CAP,
            members: PhaseOutcome::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "PathAnchor",
            role: "path-anchor",
            cap: PathAnchor::CAP,
            members: PathAnchor::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "Sink",
            role: "code",
            cap: Sink::CAP,
            members: Sink::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "Platform",
            role: "code",
            cap: Platform::CAP,
            members: Platform::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "BuildProfile",
            role: "code",
            cap: BuildProfile::CAP,
            members: BuildProfile::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "IoErrorKind",
            role: "code",
            cap: IoErrorKind::CAP,
            members: IoErrorKind::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "CommitNotPublished",
            role: "code",
            cap: CommitNotPublished::CAP,
            members: CommitNotPublished::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "RepairKind",
            role: "code",
            cap: RepairKind::CAP,
            members: RepairKind::TEXT,
            provenance: "registry-literal",
        },
        Table {
            name: "RepairState",
            role: "code",
            cap: RepairState::CAP,
            members: RepairState::TEXT,
            provenance: "registry-literal",
        },
    ]
    .into_iter()
    .chain(supervision_tables())
    .collect()
}

/// M3-D unit D3a-3's tables (LD-D3A-10), with their provenance classes.
fn supervision_tables() -> Vec<Table> {
    macro_rules! table {
        ($name:ident, $provenance:literal) => {
            Table {
                name: stringify!($name),
                role: "code",
                cap: $name::CAP,
                members: $name::TEXT,
                provenance: $provenance,
            }
        };
    }
    vec![
        table!(ProviderRole, "registry-literal"),
        table!(ProtocolMajor, "registry-literal"),
        table!(RssUnit, "registry-literal"),
        table!(FaultSource, "registry-literal"),
        table!(ForceTrigger, "registry-literal"),
        table!(TeardownCause, "registry-literal"),
        table!(BoundedWait, "registry-literal"),
        table!(LimitKind, "registry-literal"),
        table!(LimitUnit, "registry-literal"),
        table!(ExitClass, "registry-literal"),
        table!(ScratchRetainedReason, "registry-literal"),
        table!(LivenessMiss, "registry-literal"),
        table!(RefusalFamily, "protocol-enum"),
        table!(ControlCancelReason, "protocol-enum"),
        table!(RustFaultKind, "protocol-enum"),
        table!(RustDetailCode, "registry-literal"),
    ]
}

fn requires_name(set: IdentitySet) -> &'static str {
    match set {
        IdentitySet::Request => "request",
        IdentitySet::Project => "project",
        IdentitySet::ProjectPlanExecution => "project+plan+execution",
        IdentitySet::ProjectPlanExecutionRun => "project+plan+execution+run",
    }
}

fn class_name(class: PrivacyClass) -> &'static str {
    match class {
        PrivacyClass::P0 => "P0",
        PrivacyClass::P1 => "P1",
        PrivacyClass::P2 => "P2",
    }
}

fn push_json_str(out: &mut String, text: &str) {
    out.push('"');
    for ch in text.chars() {
        match ch {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            _ => out.push(ch),
        }
    }
    out.push('"');
}

fn push_event<E: Event>(out: &mut String) {
    out.push_str("    {\n      \"name\": ");
    push_json_str(out, E::NAME);
    out.push_str(",\n      \"level\": ");
    push_json_str(out, Level::TEXT[E::LEVEL.index()]);
    out.push_str(",\n      \"requires\": ");
    push_json_str(out, requires_name(E::REQUIRES));
    out.push_str(",\n      \"export\": ");
    out.push_str(if E::EXPORT { "true" } else { "false" });
    out.push_str(",\n      \"template\": ");
    push_json_str(out, E::TEMPLATE);
    out.push_str(",\n      \"maxLine\": ");
    out.push_str(&E::MAX_LINE.to_string());
    out.push_str(",\n      \"fields\": [");
    for index in 0..E::FIELD_COUNT {
        if index > 0 {
            out.push(',');
        }
        out.push_str("\n        {\"key\": ");
        push_json_str(out, E::FIELD_KEYS[index]);
        out.push_str(", \"kind\": ");
        push_json_str(out, E::FIELD_KINDS[index]);
        out.push_str(", \"class\": ");
        push_json_str(out, class_name(E::FIELD_CLASSES[index]));
        out.push_str(", \"bound\": ");
        out.push_str(&E::FIELD_BOUNDS[index].to_string());
        if E::FIELD_OPTIONAL.get(index).copied().unwrap_or(false) {
            out.push_str(", \"optional\": true");
        }
        if E::FIELD_ASSERTED.get(index).copied().unwrap_or(false) {
            out.push_str(", \"asserted\": true");
        }
        if let Some((_, map)) = E::COUNTER_MAPS
            .iter()
            .find(|(key, _)| *key == E::FIELD_KEYS[index])
        {
            out.push_str(", \"indexMap\": [");
            for (slot, (reason, level)) in map.iter().enumerate() {
                if slot > 0 {
                    out.push_str(", ");
                }
                out.push('[');
                push_json_str(out, reason);
                out.push_str(", ");
                push_json_str(out, Level::TEXT[level.index()]);
                out.push(']');
            }
            out.push(']');
        }
        out.push('}');
    }
    out.push_str("\n      ]\n    }");
}

/// D3a-3's events, rendered after O1's, in item 23's order.
macro_rules! supervision_events {
    (json, $out:ident) => {
        supervision_events!(@each $out, |out| {
            out.push_str(",\n");
        }, push_event)
    };
    (markdown, $out:ident) => {
        supervision_events!(@each $out, |_out| {}, push_markdown_event)
    };
    (@each $out:ident, $sep:expr, $push:ident) => {{
        let separate: fn(&mut String) = $sep;
        for push in [
            $push::<ProviderProcessSpawned> as fn(&mut String),
            $push::<ProviderProcessReady>,
            $push::<ProviderStderrReduced>,
            $push::<ProviderFaultReduced>,
            $push::<ProviderResourcesReported>,
            $push::<SupervisionLivenessMissed>,
            $push::<SupervisionLimitBreached>,
            $push::<SupervisionSampleIncomplete>,
            $push::<SupervisionCancelSent>,
            $push::<SupervisionCancelForced>,
            $push::<SupervisionWaitExpired>,
            $push::<SupervisionTeardownStarted>,
            $push::<SupervisionTreeSwept>,
            $push::<SupervisionScratchRetained>,
            $push::<SupervisionSettled>,
            $push::<ToolProcessSpawned>,
            $push::<ToolProcessReaped>,
        ] {
            separate(&mut $out);
            push(&mut $out);
        }
    }};
}

fn render_json() -> String {
    let mut out = String::from("{\n  \"events\": [\n");
    push_event::<LogStreamOpened>(&mut out);
    out.push_str(",\n");
    push_event::<LogLossCounted>(&mut out);
    out.push_str(",\n");
    push_event::<HostRepairCompleted>(&mut out);
    out.push_str(",\n");
    push_event::<StorageCommitPublished>(&mut out);
    out.push_str(",\n");
    push_event::<StorageCommitNotPublished>(&mut out);
    out.push_str(",\n");
    push_event::<HostPhaseStarted>(&mut out);
    out.push_str(",\n");
    push_event::<HostPhaseCompleted>(&mut out);
    supervision_events!(json, out);
    out.push_str("\n  ],\n  \"codeTables\": [");
    for (index, table) in tables().iter().enumerate() {
        if index > 0 {
            out.push(',');
        }
        out.push_str("\n    {\"name\": ");
        push_json_str(&mut out, table.name);
        out.push_str(", \"provenance\": ");
        push_json_str(&mut out, table.provenance);
        out.push_str(", \"role\": ");
        push_json_str(&mut out, table.role);
        out.push_str(", \"cap\": ");
        out.push_str(&table.cap.to_string());
        out.push_str(", \"members\": [");
        for (member_index, member) in table.members.iter().enumerate() {
            if member_index > 0 {
                out.push_str(", ");
            }
            push_json_str(&mut out, member);
        }
        out.push_str("]}");
    }
    out.push_str(
        "\n  ],\n  \"retired\": [],\n  \"sinks\": [\n    {\"name\": \"stderr\", \"classes\": [\"P0\", \"P1\", \"P2\"]},\n    {\"name\": \"file\", \"classes\": [\"P0\", \"P1\", \"P2\"]},\n    {\"name\": \"pre-scope\", \"classes\": [\"P0\", \"P1\", \"P2\"]},\n    {\"name\": \"harness\", \"classes\": [\"P0\", \"P1\"]},\n    {\"name\": \"ring\", \"classes\": [\"P0\", \"P1\"]},\n    {\"name\": \"bundle\", \"classes\": [\"P0\", \"P1\"], \"p2\": \"per-member consent\"},\n    {\"name\": \"otlp\", \"classes\": [\"P0\"], \"events\": \"export candidates only\"},\n    {\"name\": \"diagnostics\", \"classes\": [\"P0\"], \"events\": \"loss summary only\"}\n  ]\n}\n",
    );
    out
}

fn render_markdown() -> String {
    let mut out = String::from("# Operability registry\n\n## Events\n");
    push_markdown_event::<LogStreamOpened>(&mut out);
    push_markdown_event::<LogLossCounted>(&mut out);
    push_markdown_event::<HostRepairCompleted>(&mut out);
    push_markdown_event::<StorageCommitPublished>(&mut out);
    push_markdown_event::<StorageCommitNotPublished>(&mut out);
    push_markdown_event::<HostPhaseStarted>(&mut out);
    push_markdown_event::<HostPhaseCompleted>(&mut out);
    supervision_events!(markdown, out);
    out.push_str("\n## Code tables\n");
    for table in tables() {
        out.push_str("\n### ");
        out.push_str(table.name);
        out.push_str("\n\n- provenance: ");
        out.push_str(table.provenance);
        out.push_str("\n- role: ");
        out.push_str(table.role);
        out.push_str("\n- cap: ");
        out.push_str(&table.cap.to_string());
        out.push_str("\n\n");
        for member in table.members {
            out.push_str("- `");
            out.push_str(member);
            out.push_str("`\n");
        }
    }
    out.push_str(
        "\n## Retired\n\nnone\n\n## Sinks\n\n- stderr: P0, P1, P2\n- file: P0, P1, P2\n- pre-scope: P0, P1, P2\n- harness: P0, P1\n- ring: P0, P1\n- bundle: P0, P1; P2 only with per-member consent\n- otlp: P0, export candidates only\n- diagnostics: P0, the loss summary only\n",
    );
    out
}

fn push_markdown_event<E: Event>(out: &mut String) {
    out.push_str("\n### `");
    out.push_str(E::NAME);
    out.push_str("`\n\n- level: ");
    out.push_str(Level::TEXT[E::LEVEL.index()]);
    out.push_str("\n- requires: ");
    out.push_str(requires_name(E::REQUIRES));
    out.push_str("\n- export: ");
    out.push_str(if E::EXPORT { "true" } else { "false" });
    out.push_str("\n- template: ");
    out.push_str(E::TEMPLATE);
    out.push_str("\n- maxLine: ");
    out.push_str(&E::MAX_LINE.to_string());
    out.push_str("\n\n| key | kind | class | bound |\n| --- | --- | --- | --- |\n");
    for index in 0..E::FIELD_COUNT {
        out.push_str("| ");
        out.push_str(E::FIELD_KEYS[index]);
        out.push_str(" | `");
        out.push_str(E::FIELD_KINDS[index]);
        if E::FIELD_OPTIONAL.get(index).copied().unwrap_or(false) {
            out.push_str(" (optional)");
        }
        if E::FIELD_ASSERTED.get(index).copied().unwrap_or(false) {
            out.push_str(" (asserted)");
        }
        out.push_str("` | ");
        out.push_str(class_name(E::FIELD_CLASSES[index]));
        out.push_str(" | ");
        out.push_str(&E::FIELD_BOUNDS[index].to_string());
        out.push_str(" |\n");
    }
    for (key, map) in E::COUNTER_MAPS {
        out.push_str("\nFrozen index map for `");
        out.push_str(key);
        out.push_str("`:\n\n");
        for (index, (reason, level)) in map.iter().enumerate() {
            out.push_str("- ");
            out.push_str(&index.to_string());
            out.push_str(": `");
            out.push_str(reason);
            out.push_str("`, `");
            out.push_str(Level::TEXT[level.index()]);
            out.push_str("`\n");
        }
    }
}

#[test]
fn loss_descriptor_keeps_frozen_map_and_optional_same_error_pair() {
    use crate::kinds::Errno;
    use crate::writer::CapturedError;
    assert_eq!(LogLossCounted::LEVEL, Level::Warn);
    assert_eq!(LogLossCounted::REQUIRES, IdentitySet::Request);
    const {
        assert!(!LogLossCounted::EXPORT);
    }
    assert_eq!(LogLossCounted::FIELD_OPTIONAL, &[false, false, true, true]);
    let map = LogLossCounted::COUNTER_MAPS[0].1;
    assert_eq!(map.len(), 40);
    assert_eq!(map[0], ("refused", Level::Error));
    assert_eq!(map[39], ("drain-abandoned", Level::Trace));
    let clean = LogLossCounted::from_snapshot(Sink::Stderr, [u64::MAX; 40], None);
    let mut human = Vec::new();
    assert_eq!(clean.project_fields_human(PrivacyClass::P0, &mut human), 0);
    assert_eq!(clean.projected_truncated(PrivacyClass::P0), 0);
    assert!(human.starts_with(b" sink=\"stderr\" counts=["));
    let mut out = Vec::new();
    clean.project_fields(PrivacyClass::P0, &mut out);
    assert!(!out.windows(10).any(|part| part == b"sink_error"));
    assert!(!out.windows(5).any(|part| part == b"errno"));
    assert!(out.len() < LogLossCounted::MAX_LINE);
    let error = CapturedError {
        kind: IoErrorKind::PermissionDenied,
        errno: Some(Errno::from_raw_os_error(13)),
    };
    let failed = LogLossCounted::from_snapshot(Sink::Stderr, [0; 40], Some(error));
    out.clear();
    failed.project_fields(PrivacyClass::P0, &mut out);
    assert!(out.ends_with(b"\"sink_error\":\"permission-denied\",\"errno\":13}"));
}

#[test]
fn the_committed_registry_reference_matches_the_registry() {
    let json = render_json();
    let markdown = render_markdown();
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let json_path = root.join("registry-events.json");
    let markdown_path = root.join("registry-events.md");
    let committed_json = std::fs::read_to_string(&json_path).unwrap_or_default();
    let committed_markdown = std::fs::read_to_string(&markdown_path).unwrap_or_default();
    if committed_json != json || committed_markdown != markdown {
        let dir = std::env::temp_dir();
        std::fs::write(dir.join("registry-events.json"), &json).unwrap();
        std::fs::write(dir.join("registry-events.md"), &markdown).unwrap();
        panic!(
            "registry reference drifted; regenerated under {}",
            dir.display()
        );
    }
}

// No production registration: the macro supports the empty K3 vocabulary
// explicitly selected for provider detail codes until their owner admits one.
code_table!(EmptyOpenCodeProbe, cap 64, {});
#[test]
fn empty_open_code_table_only_reduces_and_never_reemits_external_text() {
    use crate::{Form, RegisteredCode, SafeField};
    for input in [b"CANARY".as_slice(), b"", b"registration"] {
        let value = RegisteredCode::<EmptyOpenCodeProbe>::of(input);
        let mut output = Vec::new();
        value.encode(Form::Json, &mut output);
        assert_eq!(
            output,
            format!(
                "{{\"unrecognized\":{{\"bytes\":{},\"truncated\":false}}}}",
                input.len()
            )
            .as_bytes()
        );
        let mut human = Vec::new();
        value.encode(Form::Human, &mut human);
        assert_eq!(human, output);
    }
}

// Independent completeness control against declarations in the unexpanded
// registry, rather than only comparing files with a manually enumerated renderer.
fn quoted_values<'a>(text: &'a str, marker: &str) -> std::collections::BTreeSet<&'a str> {
    text.split(marker)
        .skip(1)
        .map(|tail| tail.split('"').next().unwrap())
        .collect()
}
fn reference_is_complete(source: &str, json: &str, markdown: &str) -> bool {
    let mut events = quoted_values(source, "name: \"");
    events.extend(quoted_values(source, "const NAME: &'static str = \""));
    for tail in source.split("loss_event!(").skip(1) {
        if let Some((_, name)) = tail.split_once(", \"") {
            events.insert(name.split('"').next().unwrap());
        }
    }
    let declared_tables: std::collections::BTreeSet<_> = source
        .split("code_table!(")
        .skip(1)
        .map(|tail| tail.split(',').next().unwrap().trim())
        .collect();
    let json_events = quoted_values(json.split("\"codeTables\"").next().unwrap(), "\"name\": \"");
    let Some((_, table_section)) = json.split_once("\"codeTables\"") else {
        return false;
    };
    let json_tables = quoted_values(
        table_section.split("\"retired\"").next().unwrap(),
        "\"name\": \"",
    );
    let md_events: std::collections::BTreeSet<_> = markdown
        .split("### `")
        .skip(1)
        .map(|tail| tail.split('`').next().unwrap())
        .collect();
    let Some((_, md_tables)) = markdown.split_once("## Code tables") else {
        return false;
    };
    let md_tables: std::collections::BTreeSet<_> = md_tables
        .split("## Retired")
        .next()
        .unwrap()
        .split("### ")
        .skip(1)
        .map(|tail| tail.lines().next().unwrap())
        .collect();
    events == json_events
        && events == md_events
        && declared_tables == json_tables
        && declared_tables == md_tables
        && json.contains("{\"name\": \"harness\", \"classes\": [\"P0\", \"P1\"]}")
        && markdown.contains("- harness: P0, P1\n")
}

#[test]
fn reference_covers_every_declared_event_table_and_the_bound_harness_sink() {
    let source = include_str!("registry.rs");
    let json = render_json();
    let markdown = render_markdown();
    assert!(reference_is_complete(source, &json, &markdown));
    for omitted in [
        "host.phase.started",
        "host.phase.completed",
        "PhaseOutcome",
        "harness",
    ] {
        let missing_json = json.replace(omitted, "omitted");
        assert!(
            !reference_is_complete(source, &missing_json, &markdown),
            "JSON omission escaped: {omitted}"
        );
        let missing_markdown = markdown.replace(omitted, "omitted");
        assert!(
            !reference_is_complete(source, &json, &missing_markdown),
            "Markdown omission escaped: {omitted}"
        );
    }
}

// ------------------------------------------------------------------ M3-D unit D3a-3: C-2 extended

/// One transcribed field: key, kind, class, and its mode (`req`, `opt` or
/// `asserted`).
type Row = (&'static str, &'static str, &'static str, &'static str);

/// The required field inventory (LD-D3A-10's C-2 extension), transcribed by
/// hand from S-OP-2 item 23 (SOP2:877-890) and M3-D r5 item 21's ordinary
/// registrations (:687-693), with D3a-3's own ordinary fields marked. Every
/// `provider.*` and `supervision.*` row begins with `role` K1 `ProviderRole`
/// and `universe` K9 (SOP2:856-859).
fn inventory() -> Vec<(&'static str, Level, IdentitySet, bool, Vec<Row>)> {
    const ROLE: Row = ("role", "Code<ProviderRole>", "P0", "req");
    const UNIVERSE: Row = ("universe", "Universe", "P1", "req");
    let pp = IdentitySet::ProjectPlanExecution;
    let common = |rows: &[Row]| -> Vec<Row> {
        let mut all = vec![ROLE, UNIVERSE];
        all.extend_from_slice(rows);
        all
    };
    vec![
        // SOP2:877.
        (
            "provider.process.spawned",
            Level::Info,
            pp,
            false,
            common(&[
                ("protocol", "Code<ProtocolMajor>", "P0", "req"),
                ("pid", "ProcessId", "P1", "req"),
            ]),
        ),
        // SOP2:878.
        (
            "provider.process.ready",
            Level::Info,
            pp,
            false,
            common(&[
                ("start", "Elapsed", "P0", "req"),
                ("transfer", "Elapsed", "P0", "req"),
            ]),
        ),
        // SOP2:882.
        (
            "provider.stderr.reduced",
            Level::Info,
            pp,
            false,
            common(&[("stderr", "Reduced", "P0", "req")]),
        ),
        // SOP2:883.
        (
            "provider.fault.reduced",
            Level::Warn,
            pp,
            true,
            common(&[
                ("source", "Code<FaultSource>", "P0", "req"),
                ("fault_kind", "Code<RustFaultKind>", "P0", "opt"),
                ("refusal_family", "Code<RefusalFamily>", "P0", "opt"),
                ("detail", "Reduced", "P0", "req"),
                ("detail_code", "RegisteredCode<RustDetailCode>", "P0", "opt"),
            ]),
        ),
        // SOP2:884.
        (
            "provider.resources.reported",
            Level::Debug,
            pp,
            false,
            common(&[
                ("resident", "Bytes", "P0", "asserted"),
                ("cpu", "Elapsed", "P0", "asserted"),
                ("handles", "Count", "P0", "asserted"),
            ]),
        ),
        // SOP2:885, with D3a-3's ordinary `miss` and `refusal_family`
        // (D3A1-R2-NBO-1).
        (
            "supervision.liveness.missed",
            Level::Warn,
            pp,
            true,
            common(&[
                ("window", "Elapsed", "P0", "req"),
                ("miss", "Code<LivenessMiss>", "P0", "req"),
                ("refusal_family", "Code<RefusalFamily>", "P0", "opt"),
            ]),
        ),
        // SOP2:887.
        (
            "supervision.limit.breached",
            Level::Warn,
            pp,
            true,
            common(&[
                ("limit", "Code<LimitKind>", "P0", "req"),
                ("observed", "Count", "P0", "req"),
                ("unit", "Code<LimitUnit>", "P0", "req"),
            ]),
        ),
        // D3a-3's ordinary event (D3A2-R1-NBO-1).
        (
            "supervision.sample.incomplete",
            Level::Warn,
            pp,
            false,
            common(&[
                ("listed", "Count", "P0", "req"),
                ("unsampled", "Count", "P0", "req"),
                ("listing_failed", "Flag", "P0", "req"),
            ]),
        ),
        // SOP2:888.
        (
            "supervision.cancel.sent",
            Level::Info,
            pp,
            false,
            common(&[
                ("inband", "Flag", "P0", "req"),
                ("control_reason", "Code<ControlCancelReason>", "P0", "req"),
            ]),
        ),
        // SOP2:889.
        (
            "supervision.cancel.forced",
            Level::Warn,
            pp,
            false,
            common(&[
                ("trigger", "Code<ForceTrigger>", "P0", "req"),
                ("grace", "Elapsed", "P0", "req"),
            ]),
        ),
        // SOP2:890.
        (
            "supervision.wait.expired",
            Level::Warn,
            pp,
            false,
            common(&[
                ("wait", "Code<BoundedWait>", "P0", "req"),
                ("limit", "Elapsed", "P0", "req"),
            ]),
        ),
        // M3-D r5 item 21 (:687-693).
        (
            "supervision.teardown.started",
            Level::Info,
            pp,
            false,
            common(&[("cause", "Code<TeardownCause>", "P0", "req")]),
        ),
        (
            "supervision.tree.swept",
            Level::Info,
            pp,
            false,
            common(&[
                ("killed", "Count", "P0", "req"),
                ("unattributed", "Count", "P0", "req"),
                ("platform_limited", "Flag", "P0", "req"),
            ]),
        ),
        (
            "supervision.scratch.retained",
            Level::Warn,
            pp,
            false,
            common(&[
                ("reason", "Code<ScratchRetainedReason>", "P0", "req"),
                ("errno", "Errno", "P0", "opt"),
            ]),
        ),
        (
            "supervision.child.settled",
            Level::Info,
            pp,
            false,
            common(&[
                ("cause", "Code<TeardownCause>", "P0", "req"),
                ("admissible", "Flag", "P0", "req"),
                ("user_interrupted", "Flag", "P0", "req"),
            ]),
        ),
        (
            "tool.process.spawned",
            Level::Info,
            IdentitySet::Project,
            false,
            vec![("pid", "ProcessId", "P1", "req")],
        ),
        (
            "tool.process.reaped",
            Level::Info,
            IdentitySet::Project,
            false,
            vec![
                ("pid", "ProcessId", "P1", "req"),
                ("exit_class", "Code<ExitClass>", "P0", "req"),
                ("max_rss_native", "Count", "P0", "req"),
                ("rss_unit", "Code<RssUnit>", "P0", "req"),
                ("max_rss_bytes", "Bytes", "P0", "opt"),
                ("cpu", "Elapsed", "P0", "req"),
            ],
        ),
    ]
}

/// S-OP-2 item 23's events not registered: each lacks a resolved table for
/// a field, an explicit blocker (LD-D3A-10).
const BLOCKED: [(&str, &str); 4] = [
    ("provider.stage.changed", "StageKind, ProviderState"),
    ("provider.stage.terminal", "StageKind, ProviderReason"),
    ("provider.process.reaped", "Signal"),
    ("supervision.progress.absent", "StageKind"),
];

struct Descriptor {
    name: &'static str,
    level: Level,
    requires: IdentitySet,
    export: bool,
    rows: Vec<(String, String, String, String)>,
}
fn descriptor<E: Event>() -> Descriptor {
    let rows = (0..E::FIELD_COUNT)
        .map(|index| {
            let mode = if E::FIELD_ASSERTED.get(index).copied().unwrap_or(false) {
                "asserted"
            } else if E::FIELD_OPTIONAL.get(index).copied().unwrap_or(false) {
                "opt"
            } else {
                "req"
            };
            (
                E::FIELD_KEYS[index].to_owned(),
                E::FIELD_KINDS[index].replace(' ', ""),
                class_name(E::FIELD_CLASSES[index]).to_owned(),
                mode.to_owned(),
            )
        })
        .collect();
    Descriptor {
        name: E::NAME,
        level: E::LEVEL,
        requires: E::REQUIRES,
        export: E::EXPORT,
        rows,
    }
}
fn registered() -> Vec<Descriptor> {
    vec![
        descriptor::<ProviderProcessSpawned>(),
        descriptor::<ProviderProcessReady>(),
        descriptor::<ProviderStderrReduced>(),
        descriptor::<ProviderFaultReduced>(),
        descriptor::<ProviderResourcesReported>(),
        descriptor::<SupervisionLivenessMissed>(),
        descriptor::<SupervisionLimitBreached>(),
        descriptor::<SupervisionSampleIncomplete>(),
        descriptor::<SupervisionCancelSent>(),
        descriptor::<SupervisionCancelForced>(),
        descriptor::<SupervisionWaitExpired>(),
        descriptor::<SupervisionTeardownStarted>(),
        descriptor::<SupervisionTreeSwept>(),
        descriptor::<SupervisionScratchRetained>(),
        descriptor::<SupervisionSettled>(),
        descriptor::<ToolProcessSpawned>(),
        descriptor::<ToolProcessReaped>(),
    ]
}
/// Each difference between the registry and the transcribed inventory.
fn inventory_differences(registered: &[Descriptor]) -> Vec<String> {
    let mut out = Vec::new();
    let wanted = inventory();
    for (name, level, requires, export, rows) in &wanted {
        let Some(have) = registered.iter().find(|d| d.name == *name) else {
            out.push(format!("{name}: not registered"));
            continue;
        };
        if have.level != *level || have.requires != *requires || have.export != *export {
            out.push(format!("{name}: level, identities or export"));
        }
        let want: Vec<(String, String, String, String)> = rows
            .iter()
            .map(|(k, t, c, m)| {
                (
                    (*k).to_owned(),
                    (*t).to_owned(),
                    (*c).to_owned(),
                    (*m).to_owned(),
                )
            })
            .collect();
        for row in &want {
            if !have.rows.contains(row) {
                out.push(format!("{name}: missing or changed {row:?}"));
            }
        }
        for row in &have.rows {
            if !want.contains(row) {
                out.push(format!("{name}: extra {row:?}"));
            }
        }
    }
    for have in registered {
        if !wanted.iter().any(|(name, ..)| *name == have.name) {
            out.push(format!("{}: not in the inventory", have.name));
        }
    }
    out
}

/// C-2 extended (LD-D3A-10): every D3a-3 descriptor equals the transcribed
/// inventory (names, levels, identities, export, fields, kinds, classes,
/// optionality and assertion), with no field missing or extra; the four
/// blocked events are not registered; and each control fires on a planted
/// difference.
#[test]
fn supervision_descriptors_equal_the_required_field_inventory() {
    let registry = registered();
    assert_eq!(inventory_differences(&registry), Vec::<String>::new());
    let source = include_str!("registry.rs");
    for (blocked, _tables) in BLOCKED {
        assert!(event_name_ok(blocked));
        assert!(
            !source.contains(&format!("name: \"{blocked}\"")),
            "{blocked} is blocked, never registered in a reduced form"
        );
    }
    // A missing field, an extra field, a changed optionality and a changed
    // class are each caught.
    let mut planted = registered();
    planted[0].rows.pop();
    assert!(!inventory_differences(&planted).is_empty());
    let mut planted = registered();
    planted[2]
        .rows
        .push(("text".into(), "Reduced".into(), "P0".into(), "req".into()));
    assert!(!inventory_differences(&planted).is_empty());
    let mut planted = registered();
    planted[13].rows[3].3 = "req".into();
    assert!(!inventory_differences(&planted).is_empty());
    let mut planted = registered();
    planted[0].rows[3].2 = "P0".into();
    assert!(!inventory_differences(&planted).is_empty());
    let mut planted = registered();
    planted.pop();
    assert!(!inventory_differences(&planted).is_empty());
}

/// LD-D3A-10 and LD-D3A-17/18: `supervision.scratch.retained` has exactly
/// its three typed shapes; an errno is present exactly for `io-failure`.
/// The general constructor is crate-private, so an `io-failure` without an
/// errno, or an errno on exhaustion, cannot be built outside the registry.
#[test]
fn scratch_retained_has_only_its_typed_shapes() {
    let set = CapabilitySet::issue();
    let universe = || set.universe_digest.owned_identity([7; 32]);
    let role = || Code::from_enum(ProviderRole::RustSemantic);
    let mut out = Vec::new();
    SupervisionScratchRetained::io_failure(
        role(),
        universe(),
        super::super::Errno::from_raw_os_error(13),
    )
    .project_fields(PrivacyClass::P0, &mut out);
    assert!(out.ends_with(b"\"reason\":\"io-failure\",\"errno\":13}"));
    for (record, reason) in [
        (
            SupervisionScratchRetained::work_exhausted(role(), universe()),
            "work-exhausted",
        ),
        (
            SupervisionScratchRetained::root_unreaped(role(), universe()),
            "root-unreaped",
        ),
    ] {
        out.clear();
        record.project_fields(PrivacyClass::P0, &mut out);
        let text = String::from_utf8(out.clone()).unwrap();
        assert!(
            text.ends_with(&format!("\"reason\":\"{reason}\"}}")),
            "{text}"
        );
        assert!(!text.contains("errno"));
    }
    assert_eq!(
        ScratchRetainedReason::TEXT,
        &["io-failure", "work-exhausted", "root-unreaped"]
    );
    assert_eq!(
        SupervisionScratchRetained::FIELD_OPTIONAL,
        &[false, false, false, true]
    );
}

/// The liveness record's reduced provenance (D3A1-R2-NBO-1): a window
/// expiry carries no family; a nonce mismatch carries the control owner's
/// family. No nonce or text exists in either.
#[test]
fn liveness_missed_carries_its_reduced_provenance() {
    let set = CapabilitySet::issue();
    let mut out = Vec::new();
    SupervisionLivenessMissed::window_expired(
        Code::from_enum(ProviderRole::TypescriptSemantic),
        set.universe_digest.owned_identity([1; 32]),
        super::super::Elapsed::new(5_000_000_000),
    )
    .project_fields(PrivacyClass::P1, &mut out);
    let text = String::from_utf8(out.clone()).unwrap();
    assert!(
        text.ends_with("\"window\":5000000000,\"miss\":\"window-expired\"}"),
        "{text}"
    );
    out.clear();
    SupervisionLivenessMissed::nonce_mismatch(
        Code::from_enum(ProviderRole::TypescriptSemantic),
        set.universe_digest.owned_identity([1; 32]),
        super::super::Elapsed::new(5_000_000_000),
        Code::from_enum(RefusalFamily::Rf7),
    )
    .project_fields(PrivacyClass::P0, &mut out);
    let text = String::from_utf8(out).unwrap();
    assert!(
        text.contains("\"miss\":\"nonce-mismatch\",\"refusal_family\":\"RF-7\""),
        "{text}"
    );
    assert!(
        !text.contains("universe"),
        "P1 is projected out at P0: {text}"
    );
}

/// An asserted value is labelled in both references (SOP2 item 4), and the
/// tool events require Project only (M3-D r5 :692).
#[test]
fn asserted_and_project_only_descriptors_are_rendered() {
    let json = render_json();
    assert!(json.contains("{\"key\": \"resident\", \"kind\": \"Bytes\", \"class\": \"P0\", \"bound\": 20, \"asserted\": true}"));
    assert!(json.contains("\"name\": \"tool.process.reaped\",\n      \"level\": \"info\",\n      \"requires\": \"project\""));
    let markdown = render_markdown();
    assert!(markdown.contains("| resident | `Bytes (asserted)` | P0 | 20 |"));
    assert_eq!(ToolProcessSpawned::REQUIRES, IdentitySet::Project);
}
