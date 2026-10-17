//! Closed re-admission of persisted records (S-OP-2 item 13a).
//!
//! The reader validates into values that are re-encoded and then discarded.
//! It does not mint a scope, an identity, a `SafeField` or an owner token.
//! `ComponentRole` is not registered, so a present `component` fails the header.

use super::constants::{Level, MAX_LINE};
use super::kinds::registry::{
    BoundedWait, ControlCancelReason, ExitClass, FaultSource, ForceTrigger, LimitKind, LimitUnit,
    LivenessMiss, ProtocolMajor, ProviderFaultReduced, ProviderProcessReady,
    ProviderProcessSpawned, ProviderResourcesReported, ProviderRole, ProviderStderrReduced,
    RefusalFamily, RssUnit, RustDetailCode, RustFaultKind, ScratchRetainedReason,
    SupervisionCancelForced, SupervisionCancelSent, SupervisionLimitBreached,
    SupervisionLivenessMissed, SupervisionSampleIncomplete, SupervisionScratchRetained,
    SupervisionSettled, SupervisionTeardownStarted, SupervisionTreeSwept, SupervisionWaitExpired,
    TeardownCause, ToolChildSettled, ToolLimitBreached, ToolProcessReaped, ToolProcessSpawned,
    ToolSampleIncomplete, ToolScratchRetained, ToolTeardownStarted, ToolWaitExpired,
};
use super::kinds::registry::{
    BuildProfile, CodeEnum, CommitNotPublished, Event, HostPhaseCompleted, HostPhaseStarted,
    HostRepairCompleted, IdentitySet, IoErrorKind, LogLossCounted, LogStreamOpened, PathAnchor,
    Phase, PhaseOutcome, Platform, RepairKind, RepairState, Sink, StorageCommitNotPublished,
    StorageCommitPublished, event_name_ok,
};
use super::kinds::{CODE_MAX, FLAG_MAX, PrivacyClass, push_flag, push_i32, push_u64};
use super::wire::{decode_rule_e_body, push_json_string};

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct RecordDrops {
    pub oversize: u64,
    pub malformed: u64,
    pub header_invalid: u64,
    pub unknown_event: u64,
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct FieldDrops {
    pub unknown_field: u64,
    pub invalid_value: u64,
}

pub struct Readmit {
    pub lines: Vec<Vec<u8>>,
    pub records: RecordDrops,
    pub fields: FieldDrops,
}

/// Re-admit a buffer of JSON lines at `ceiling`. Each admitted line is canonical.
pub fn readmit(input: &[u8], ceiling: PrivacyClass) -> Readmit {
    let mut out = Readmit {
        lines: Vec::new(),
        records: RecordDrops::default(),
        fields: FieldDrops::default(),
    };
    let mut index = 0;
    while index < input.len() {
        let start = index;
        let newline = input[index..].iter().position(|byte| *byte == b'\n');
        let (end, terminated) = match newline {
            Some(offset) => (index + offset, true),
            None => (input.len(), false),
        };
        let span = end - start + usize::from(terminated);
        if !terminated {
            if span > MAX_LINE {
                out.records.oversize += 1;
            } else if span > 0 {
                out.records.malformed += 1;
            }
            break;
        }
        if span > MAX_LINE {
            out.records.oversize += 1;
            index = end + 1;
            continue;
        }
        match admit_line(&input[start..end], span, ceiling) {
            Line::Keep(line) => out.lines.push(line),
            Line::Drop(reason) => match reason {
                Fail::Malformed => out.records.malformed += 1,
                Fail::Header => out.records.header_invalid += 1,
                Fail::Unknown => out.records.unknown_event += 1,
            },
            Line::KeepWith(line, fields) => {
                out.lines.push(line);
                out.fields.unknown_field += fields.unknown_field;
                out.fields.invalid_value += fields.invalid_value;
            }
        }
        index = end + 1;
    }
    out
}

enum Line {
    Keep(Vec<u8>),
    KeepWith(Vec<u8>, FieldDrops),
    Drop(Fail),
}

enum Fail {
    Malformed,
    Header,
    Unknown,
}

fn admit_line(body: &[u8], line_len: usize, ceiling: PrivacyClass) -> Line {
    let root = match parse_json(body) {
        Ok(node) => node,
        Err(()) => return Line::Drop(Fail::Malformed),
    };
    let Value::Object(members) = &root.value else {
        return Line::Drop(Fail::Malformed);
    };
    let Some(header) = header(members) else {
        return Line::Drop(Fail::Header);
    };
    let Some(desc) = descriptor(header.event) else {
        return Line::Drop(Fail::Unknown);
    };
    admit_values(header, desc, line_len, ceiling)
}

// Shared owning re-admission path; tests may exercise a private descriptor
// without admitting it to the release registry or exposing a reader mint.
fn admit_values(header: Header<'_>, desc: Desc, line_len: usize, ceiling: PrivacyClass) -> Line {
    if header.level != desc.level || !requires(desc.requires, &header) || line_len > desc.max_line {
        return Line::Drop(Fail::Header);
    }
    let elided = header
        .fields
        .iter()
        .filter(|(_, value)| is_elided(value))
        .count() as u64;
    if header.truncated != elided {
        return Line::Drop(Fail::Header);
    }
    let absent = desc
        .fields
        .iter()
        .filter(|field| !header.fields.iter().any(|(key, _)| key.text == field.key))
        .count() as u64;
    if header.omitted > absent {
        return Line::Drop(Fail::Header);
    }
    let mut kept: Vec<Option<Vec<u8>>> = desc.fields.iter().map(|_| None).collect();
    let mut drops = FieldDrops::default();
    let mut removed = 0u64;
    for (key, value) in header.fields {
        let Some(index) = desc.fields.iter().position(|field| field.key == key.text) else {
            drops.unknown_field += 1;
            continue;
        };
        if value_depth(value) > 2 {
            drops.invalid_value += 1;
            continue;
        }
        let Some(encoded) = admit_field(desc.fields[index], key, value) else {
            drops.invalid_value += 1;
            continue;
        };
        if desc.fields[index].class > ceiling {
            removed += 1;
            continue;
        }
        kept[index] = Some(encoded);
    }
    if desc.name == LogLossCounted::NAME && kept[2].is_none() && kept[3].take().is_some() {
        drops.invalid_value += 1;
    }
    let omitted = header.omitted + removed;
    let line = encode(&header, &desc, &kept, omitted);
    if line.len() > desc.max_line || line.len() > MAX_LINE {
        return Line::Drop(Fail::Header);
    }
    // Re-admitted values get a NEW sealed encoder map. No input-log map is
    // consulted or retained, and this guard precedes read-back re-emission.
    let line = match crate::guard::SealedRecord::from_encoder(
        line,
        crate::guard::ProjectionForm::Json,
        desc.privacy,
    ) {
        Ok(record) if record.inspect().is_ok_and(crate::guard::Assessment::lawful) => {
            record.into_bytes()
        }
        _ => return Line::Drop(Fail::Malformed),
    };
    if drops == FieldDrops::default() {
        Line::Keep(line)
    } else {
        Line::KeepWith(line, drops)
    }
}

struct Header<'a> {
    ts: &'a str,
    level: Level,
    event: &'a str,
    request: &'a str,
    project: Option<&'a str>,
    plan: Option<&'a str>,
    execution: Option<&'a str>,
    run: Option<&'a str>,
    phase: Option<&'a str>,
    omitted: u64,
    truncated: u64,
    fields: &'a [(JStr, Node)],
}

fn header(members: &[(JStr, Node)]) -> Option<Header<'_>> {
    let mut ts = None;
    let mut level = None;
    let mut event = None;
    let mut request = None;
    let mut project = None;
    let mut plan = None;
    let mut execution = None;
    let mut run = None;
    let mut phase = None;
    let mut omitted = None;
    let mut truncated = None;
    let mut fields = None;
    for (key, value) in members {
        if !key.rule_e {
            return None;
        }
        match key.text.as_str() {
            "ts" => ts = Some(string_member(value)?),
            "level" => level = Some(string_member(value)?),
            "event" => event = Some(string_member(value)?),
            "requestId" => request = Some(string_member(value)?),
            "projectId" => project = Some(string_member(value)?),
            "planId" => plan = Some(string_member(value)?),
            "executionId" => execution = Some(string_member(value)?),
            "runId" => run = Some(string_member(value)?),
            "phase" => phase = Some(string_member(value)?),
            "fields" => {
                let Value::Object(pairs) = &value.value else {
                    return None;
                };
                fields = Some(pairs.as_slice());
            }
            "omitted" => omitted = Some(small_count(value)?),
            "truncated" => truncated = Some(small_count(value)?),
            // No `ComponentRole` table is registered, so no role can match.
            "component" => return None,
            _ => return None,
        }
    }
    let ts = ts?;
    let level = level?;
    let event = event?;
    let request = request?;
    let fields = fields?;
    if !timestamp_ok(ts) || !event_name_ok(event) || !request_id_ok(request) {
        return None;
    }
    let level = parse_level(level)?;
    if let Some(text) = project
        && !identity_ok(text, "prj1-", 64)
    {
        return None;
    }
    if let Some(text) = plan
        && !identity_ok(text, "plan2:", 64)
    {
        return None;
    }
    if let Some(text) = execution
        && !identity_ok(text, "exec1_", 32)
    {
        return None;
    }
    if let Some(text) = run
        && !identity_ok(text, "run3:", 64)
    {
        return None;
    }
    if let Some(text) = phase
        && !phase_ok(text)
    {
        return None;
    }
    let ids = Ids {
        project: project.is_some(),
        plan: plan.is_some(),
        execution: execution.is_some(),
        run: run.is_some(),
    };
    if !shape_ok(ids) {
        return None;
    }
    Some(Header {
        ts,
        level,
        event,
        request,
        project,
        plan,
        execution,
        run,
        phase,
        omitted: omitted.unwrap_or(0),
        truncated: truncated.unwrap_or(0),
        fields,
    })
}

fn string_member(node: &Node) -> Option<&str> {
    match &node.value {
        Value::String(text) if text.rule_e => Some(text.text.as_str()),
        _ => None,
    }
}

fn small_count(node: &Node) -> Option<u64> {
    match node.value {
        Value::Number(Number::U64(value)) if (1..=32).contains(&value) => Some(value),
        _ => None,
    }
}

struct Ids {
    project: bool,
    plan: bool,
    execution: bool,
    run: bool,
}

fn shape_ok(ids: Ids) -> bool {
    matches!(
        (ids.project, ids.plan, ids.execution, ids.run),
        (false, false, false, false)
            | (true, false, false, false)
            | (true, true, false, false)
            | (true, false, true, false)
            | (true, true, true, false)
            | (true, true, true, true)
            | (true, false, false, true)
    )
}

fn requires(set: IdentitySet, header: &Header<'_>) -> bool {
    match set {
        IdentitySet::Request => true,
        IdentitySet::Project => header.project.is_some(),
        IdentitySet::ProjectPlanExecution => {
            header.project.is_some() && header.plan.is_some() && header.execution.is_some()
        }
        IdentitySet::ProjectPlanExecutionRun => {
            header.project.is_some()
                && header.plan.is_some()
                && header.execution.is_some()
                && header.run.is_some()
        }
    }
}

#[derive(Clone, Copy)]
struct FieldDesc {
    key: &'static str,
    class: PrivacyClass,
    kind: FieldKind,
    max_value: usize,
}

#[derive(Clone, Copy)]
#[cfg_attr(
    not(test),
    expect(
        dead_code,
        reason = "Closed K1–K15 reader predicates precede their owning event registrations (O1 item 5)"
    )
)]
enum FieldKind {
    Phase,
    PhaseOutcome,
    IoErrorKind,
    Platform,
    BuildProfile,
    Sink,
    RepairKind,
    RepairState,
    CommitOutcome,
    Flag,
    /// K6. The retained census is empty, so only `external` is kept.
    CodeLocation,
    /// K12 path string or `{"elided":…}`.
    ProjectPath,
    /// K7.
    Reduced,
    /// K8. `n` is the frozen table width, at least 1.
    Counts(usize),
    /// K13, with or without `column`.
    Position,
    /// K2 `Count`, `Bytes` and `Elapsed`.
    Unsigned,
    /// K2 `Errno`.
    Errno,
    /// K11.
    ProcessId,
    /// K4.
    Version,
    /// K5: whole grammar plus actual running build's verified catalog.
    AdmittedId,
    /// K10.
    AnchorTag,
    /// K14.
    Canonical,
    /// K15.
    Symbol,
    /// K9. `prefix` is empty for a 64-hex digest, or `snapshot2:` / `closure2:`.
    Digest(&'static str),
    /// K3, both the member string and the unrecognized form.
    OpenCode(&'static [&'static str]),
    /// K1 of a registered table, by its members (D3a-3's events).
    Code(&'static [&'static str]),
}

struct Desc {
    name: &'static str,
    level: Level,
    requires: IdentitySet,
    max_line: usize,
    fields: &'static [FieldDesc],
    privacy: &'static [(&'static str, PrivacyClass)],
}

const REPAIR_FIELDS: [FieldDesc; 2] = [
    FieldDesc {
        key: "kind",
        class: HostRepairCompleted::FIELD_CLASSES[0],
        kind: FieldKind::RepairKind,
        max_value: CODE_MAX,
    },
    FieldDesc {
        key: "state",
        class: HostRepairCompleted::FIELD_CLASSES[1],
        kind: FieldKind::RepairState,
        max_value: CODE_MAX,
    },
];

const PUBLISHED_FIELDS: [FieldDesc; 1] = [FieldDesc {
    key: "latched",
    class: StorageCommitPublished::FIELD_CLASSES[0],
    kind: FieldKind::Flag,
    max_value: FLAG_MAX,
}];

const NOT_PUBLISHED_FIELDS: [FieldDesc; 1] = [FieldDesc {
    key: "outcome",
    class: StorageCommitNotPublished::FIELD_CLASSES[0],
    kind: FieldKind::CommitOutcome,
    max_value: CODE_MAX,
}];

const STREAM_FIELDS: [FieldDesc; 5] = [
    FieldDesc {
        key: "version",
        class: PrivacyClass::P0,
        kind: FieldKind::Version,
        max_value: super::kinds::VERSION_MAX,
    },
    FieldDesc {
        key: "platform",
        class: PrivacyClass::P0,
        kind: FieldKind::Platform,
        max_value: CODE_MAX,
    },
    FieldDesc {
        key: "build",
        class: PrivacyClass::P0,
        kind: FieldKind::BuildProfile,
        max_value: CODE_MAX,
    },
    FieldDesc {
        key: "sink",
        class: PrivacyClass::P0,
        kind: FieldKind::Sink,
        max_value: CODE_MAX,
    },
    FieldDesc {
        key: "pid",
        class: PrivacyClass::P1,
        kind: FieldKind::ProcessId,
        max_value: super::kinds::PROCESS_ID_MAX,
    },
];

const LOSS_FIELDS: [FieldDesc; 4] = [
    FieldDesc {
        key: "sink",
        class: PrivacyClass::P0,
        kind: FieldKind::Sink,
        max_value: CODE_MAX,
    },
    FieldDesc {
        key: "counts",
        class: PrivacyClass::P0,
        kind: FieldKind::Counts(40),
        max_value: 841,
    },
    FieldDesc {
        key: "sink_error",
        class: PrivacyClass::P0,
        kind: FieldKind::IoErrorKind,
        max_value: CODE_MAX,
    },
    FieldDesc {
        key: "errno",
        class: PrivacyClass::P0,
        kind: FieldKind::Errno,
        max_value: super::kinds::ERRNO_MAX,
    },
];

const PHASE_STARTED_FIELDS: [FieldDesc; 3] = [
    FieldDesc {
        key: "phase",
        class: PrivacyClass::P0,
        kind: FieldKind::Phase,
        max_value: 66,
    },
    FieldDesc {
        key: "parent",
        class: PrivacyClass::P0,
        kind: FieldKind::Phase,
        max_value: 66,
    },
    FieldDesc {
        key: "at",
        class: PrivacyClass::P0,
        kind: FieldKind::Unsigned,
        max_value: 20,
    },
];
const PHASE_COMPLETED_FIELDS: [FieldDesc; 5] = [
    FieldDesc {
        key: "phase",
        class: PrivacyClass::P0,
        kind: FieldKind::Phase,
        max_value: 66,
    },
    FieldDesc {
        key: "wall",
        class: PrivacyClass::P0,
        kind: FieldKind::Unsigned,
        max_value: 20,
    },
    FieldDesc {
        key: "cpu",
        class: PrivacyClass::P0,
        kind: FieldKind::Unsigned,
        max_value: 20,
    },
    FieldDesc {
        key: "outcome",
        class: PrivacyClass::P0,
        kind: FieldKind::PhaseOutcome,
        max_value: 66,
    },
    FieldDesc {
        key: "at",
        class: PrivacyClass::P0,
        kind: FieldKind::Unsigned,
        max_value: 20,
    },
];

/// M3-D unit D3a-3: a registered event's reader descriptor, from the
/// registry's own keys, classes, bounds and privacy, with each field's
/// reader kind beside it (checked at compile time to be one per field).
macro_rules! registered_desc {
    ($event:ty, [$($kind:expr),+ $(,)?]) => {{
        const KINDS: &[FieldKind] = &[$($kind),+];
        const N: usize = <$event as Event>::FIELD_COUNT;
        const _: () = assert!(KINDS.len() == N);
        const FIELDS: [FieldDesc; N] = {
            let mut out = [FieldDesc {
                key: "",
                class: PrivacyClass::P0,
                kind: FieldKind::Flag,
                max_value: 0,
            }; N];
            let mut index = 0;
            while index < N {
                out[index] = FieldDesc {
                    key: <$event as Event>::FIELD_KEYS[index],
                    class: <$event as Event>::FIELD_CLASSES[index],
                    kind: KINDS[index],
                    max_value: <$event as Event>::FIELD_BOUNDS[index],
                };
                index += 1;
            }
            out
        };
        Desc {
            name: <$event as Event>::NAME,
            level: <$event as Event>::LEVEL,
            requires: <$event as Event>::REQUIRES,
            max_line: <$event as Event>::MAX_LINE,
            fields: &FIELDS,
            privacy: <$event as Event>::FIELD_PRIVACY,
        }
    }};
}

/// The provider and supervision events' common fields (SOP2:856-859).
const ROLE: FieldKind = FieldKind::Code(ProviderRole::TEXT);
const UNIVERSE: FieldKind = FieldKind::Digest("");

fn supervision_descriptor(name: &str) -> Option<Desc> {
    use FieldKind::{Code, Errno, Flag, OpenCode, ProcessId, Reduced, Unsigned};
    let desc = match name {
        _ if name == ProviderProcessSpawned::NAME => registered_desc!(
            ProviderProcessSpawned,
            [ROLE, UNIVERSE, Code(ProtocolMajor::TEXT), ProcessId]
        ),
        _ if name == ProviderProcessReady::NAME => {
            registered_desc!(ProviderProcessReady, [ROLE, UNIVERSE, Unsigned, Unsigned])
        }
        _ if name == ProviderStderrReduced::NAME => {
            registered_desc!(ProviderStderrReduced, [ROLE, UNIVERSE, Reduced])
        }
        _ if name == ProviderFaultReduced::NAME => registered_desc!(
            ProviderFaultReduced,
            [
                ROLE,
                UNIVERSE,
                Code(FaultSource::TEXT),
                Code(RustFaultKind::TEXT),
                Code(RefusalFamily::TEXT),
                Reduced,
                OpenCode(RustDetailCode::TEXT),
            ]
        ),
        _ if name == ProviderResourcesReported::NAME => registered_desc!(
            ProviderResourcesReported,
            [ROLE, UNIVERSE, Unsigned, Unsigned, Unsigned]
        ),
        _ if name == SupervisionLivenessMissed::NAME => registered_desc!(
            SupervisionLivenessMissed,
            [
                ROLE,
                UNIVERSE,
                Unsigned,
                Code(LivenessMiss::TEXT),
                Code(RefusalFamily::TEXT)
            ]
        ),
        _ if name == SupervisionLimitBreached::NAME => registered_desc!(
            SupervisionLimitBreached,
            [
                ROLE,
                UNIVERSE,
                Code(LimitKind::TEXT),
                Unsigned,
                Code(LimitUnit::TEXT)
            ]
        ),
        _ if name == SupervisionSampleIncomplete::NAME => registered_desc!(
            SupervisionSampleIncomplete,
            [ROLE, UNIVERSE, Unsigned, Unsigned, Flag]
        ),
        _ if name == SupervisionCancelSent::NAME => registered_desc!(
            SupervisionCancelSent,
            [ROLE, UNIVERSE, Flag, Code(ControlCancelReason::TEXT)]
        ),
        _ if name == SupervisionCancelForced::NAME => registered_desc!(
            SupervisionCancelForced,
            [ROLE, UNIVERSE, Code(ForceTrigger::TEXT), Unsigned]
        ),
        _ if name == SupervisionWaitExpired::NAME => registered_desc!(
            SupervisionWaitExpired,
            [ROLE, UNIVERSE, Code(BoundedWait::TEXT), Unsigned]
        ),
        _ if name == SupervisionTeardownStarted::NAME => registered_desc!(
            SupervisionTeardownStarted,
            [ROLE, UNIVERSE, Code(TeardownCause::TEXT)]
        ),
        _ if name == SupervisionTreeSwept::NAME => registered_desc!(
            SupervisionTreeSwept,
            [ROLE, UNIVERSE, Unsigned, Unsigned, Flag]
        ),
        _ if name == SupervisionScratchRetained::NAME => registered_desc!(
            SupervisionScratchRetained,
            [ROLE, UNIVERSE, Code(ScratchRetainedReason::TEXT), Errno]
        ),
        _ if name == SupervisionSettled::NAME => registered_desc!(
            SupervisionSettled,
            [ROLE, UNIVERSE, Code(TeardownCause::TEXT), Flag, Flag]
        ),
        _ if name == ToolProcessSpawned::NAME => registered_desc!(ToolProcessSpawned, [ProcessId]),
        _ if name == ToolProcessReaped::NAME => registered_desc!(
            ToolProcessReaped,
            [
                ProcessId,
                Code(ExitClass::TEXT),
                Unsigned,
                Code(RssUnit::TEXT),
                Unsigned,
                Unsigned
            ]
        ),
        _ if name == ToolLimitBreached::NAME => registered_desc!(
            ToolLimitBreached,
            [Code(LimitKind::TEXT), Unsigned, Code(LimitUnit::TEXT)]
        ),
        _ if name == ToolSampleIncomplete::NAME => {
            registered_desc!(ToolSampleIncomplete, [Unsigned, Unsigned, Flag])
        }
        _ if name == ToolWaitExpired::NAME => {
            registered_desc!(ToolWaitExpired, [Code(BoundedWait::TEXT), Unsigned])
        }
        _ if name == ToolTeardownStarted::NAME => {
            registered_desc!(ToolTeardownStarted, [Code(TeardownCause::TEXT)])
        }
        _ if name == ToolScratchRetained::NAME => registered_desc!(
            ToolScratchRetained,
            [Code(ScratchRetainedReason::TEXT), Errno]
        ),
        _ if name == ToolChildSettled::NAME => {
            registered_desc!(ToolChildSettled, [Code(TeardownCause::TEXT), Flag])
        }
        _ => return None,
    };
    Some(desc)
}

fn descriptor(name: &str) -> Option<Desc> {
    if let Some(desc) = supervision_descriptor(name) {
        return Some(desc);
    }
    if name == HostPhaseStarted::NAME {
        Some(Desc {
            name: HostPhaseStarted::NAME,
            level: HostPhaseStarted::LEVEL,
            requires: HostPhaseStarted::REQUIRES,
            max_line: HostPhaseStarted::MAX_LINE,
            fields: &PHASE_STARTED_FIELDS,
            privacy: HostPhaseStarted::FIELD_PRIVACY,
        })
    } else if name == HostPhaseCompleted::NAME {
        Some(Desc {
            name: HostPhaseCompleted::NAME,
            level: HostPhaseCompleted::LEVEL,
            requires: HostPhaseCompleted::REQUIRES,
            max_line: HostPhaseCompleted::MAX_LINE,
            fields: &PHASE_COMPLETED_FIELDS,
            privacy: HostPhaseCompleted::FIELD_PRIVACY,
        })
    } else if name == LogLossCounted::NAME {
        Some(Desc {
            name: LogLossCounted::NAME,
            level: LogLossCounted::LEVEL,
            requires: LogLossCounted::REQUIRES,
            max_line: LogLossCounted::MAX_LINE,
            fields: &LOSS_FIELDS,
            privacy: LogLossCounted::FIELD_PRIVACY,
        })
    } else if name == LogStreamOpened::NAME {
        Some(Desc {
            name: LogStreamOpened::NAME,
            level: LogStreamOpened::LEVEL,
            requires: LogStreamOpened::REQUIRES,
            max_line: LogStreamOpened::MAX_LINE,
            fields: &STREAM_FIELDS,
            privacy: LogStreamOpened::FIELD_PRIVACY,
        })
    } else if name == HostRepairCompleted::NAME {
        Some(Desc {
            name: HostRepairCompleted::NAME,
            level: HostRepairCompleted::LEVEL,
            requires: HostRepairCompleted::REQUIRES,
            max_line: HostRepairCompleted::MAX_LINE,
            fields: &REPAIR_FIELDS,
            privacy: HostRepairCompleted::FIELD_PRIVACY,
        })
    } else if name == StorageCommitPublished::NAME {
        Some(Desc {
            name: StorageCommitPublished::NAME,
            level: StorageCommitPublished::LEVEL,
            requires: StorageCommitPublished::REQUIRES,
            max_line: StorageCommitPublished::MAX_LINE,
            fields: &PUBLISHED_FIELDS,
            privacy: StorageCommitPublished::FIELD_PRIVACY,
        })
    } else if name == StorageCommitNotPublished::NAME {
        Some(Desc {
            name: StorageCommitNotPublished::NAME,
            level: StorageCommitNotPublished::LEVEL,
            requires: StorageCommitNotPublished::REQUIRES,
            max_line: StorageCommitNotPublished::MAX_LINE,
            fields: &NOT_PUBLISHED_FIELDS,
            privacy: StorageCommitNotPublished::FIELD_PRIVACY,
        })
    } else {
        None
    }
}

fn admit_field(field: FieldDesc, key: &JStr, value: &Node) -> Option<Vec<u8>> {
    if !key.rule_e || value.end - value.start > field.max_value {
        return None;
    }
    let mut out = Vec::new();
    match field.kind {
        FieldKind::Flag => {
            let Value::Bool(flag) = value.value else {
                return None;
            };
            push_flag(flag, &mut out);
            return Some(out);
        }
        FieldKind::Phase => push_member(Phase::TEXT, value, &mut out)?,
        FieldKind::PhaseOutcome => push_member(PhaseOutcome::TEXT, value, &mut out)?,
        FieldKind::Platform => push_member(Platform::TEXT, value, &mut out)?,
        FieldKind::IoErrorKind => push_member(IoErrorKind::TEXT, value, &mut out)?,
        FieldKind::BuildProfile => push_member(BuildProfile::TEXT, value, &mut out)?,
        FieldKind::Sink => push_member(Sink::TEXT, value, &mut out)?,
        FieldKind::RepairKind => push_member(RepairKind::TEXT, value, &mut out)?,
        FieldKind::RepairState => push_member(RepairState::TEXT, value, &mut out)?,
        FieldKind::CommitOutcome => push_member(CommitNotPublished::TEXT, value, &mut out)?,
        FieldKind::CodeLocation => return admit_code_location(value),
        FieldKind::ProjectPath => return admit_project_path(value),
        FieldKind::Reduced => return admit_reduced(value),
        FieldKind::Counts(width) => return admit_counts(value, width),
        FieldKind::Position => return admit_position(value),
        FieldKind::Unsigned => return admit_unsigned(value),
        FieldKind::Errno => return admit_errno(value),
        FieldKind::ProcessId => return admit_process_id(value),
        FieldKind::Version => return admit_grammar(value, version_ok),
        FieldKind::AdmittedId => {
            return admit_grammar(value, |text| {
                crate::catalog::grammar_ok(text) && crate::catalog::lookup(text).is_some()
            });
        }
        FieldKind::AnchorTag => return admit_anchor(value),
        FieldKind::Canonical => return admit_grammar(value, canonical_id_ok),
        FieldKind::Symbol => return admit_grammar(value, symbol_ok),
        FieldKind::Digest(prefix) => {
            return admit_grammar(value, |text| digest_ok(text, prefix));
        }
        FieldKind::OpenCode(table) => return admit_open_code(table, value),
        FieldKind::Code(table) => push_member(table, value, &mut out)?,
    }
    Some(out)
}

fn push_member(table: &[&str], value: &Node, out: &mut Vec<u8>) -> Option<()> {
    let Value::String(text) = &value.value else {
        return None;
    };
    if !text.rule_e || !table.iter().any(|member| *member == text.text) {
        return None;
    }
    push_json_string(&text.text, out);
    Some(())
}

fn object_pairs(node: &Node) -> Option<&[(JStr, Node)]> {
    match &node.value {
        Value::Object(pairs) => Some(pairs),
        _ => None,
    }
}

/// Keys are exactly `keys`, each rule E, in any order. Re-encoding uses `keys`' order.
fn exact_members<'a>(pairs: &'a [(JStr, Node)], keys: &[&str]) -> Option<Vec<&'a Node>> {
    if pairs.len() != keys.len() || pairs.iter().any(|(key, _)| !key.rule_e) {
        return None;
    }
    let mut found = Vec::with_capacity(keys.len());
    for wanted in keys {
        let value = pairs
            .iter()
            .find(|(key, _)| key.text == *wanted)
            .map(|(_, value)| value)?;
        found.push(value);
    }
    Some(found)
}

fn rule_e_str(node: &Node) -> Option<&str> {
    match &node.value {
        Value::String(text) if text.rule_e => Some(text.text.as_str()),
        _ => None,
    }
}

fn u64_number(node: &Node) -> Option<u64> {
    match node.value {
        Value::Number(Number::U64(value)) => Some(value),
        _ => None,
    }
}

fn u32_number(node: &Node) -> Option<u32> {
    u64_number(node).and_then(|value| u32::try_from(value).ok())
}

fn bool_value(node: &Node) -> Option<bool> {
    match node.value {
        Value::Bool(value) => Some(value),
        _ => None,
    }
}

/// K6. No retained census entry exists, so a file other than `external` is dropped.
fn admit_code_location(value: &Node) -> Option<Vec<u8>> {
    let members = exact_members(object_pairs(value)?, &["file", "line"])?;
    let file = rule_e_str(members[0])?;
    let line = u32_number(members[1])?;
    if file != "external" {
        return None;
    }
    let mut out = Vec::new();
    out.extend_from_slice(br#"{"file":"#);
    push_json_string(file, &mut out);
    out.extend_from_slice(br#","line":"#);
    push_u64(u64::from(line), &mut out);
    out.push(b'}');
    Some(out)
}

fn logical_path_ok(text: &str) -> bool {
    if text.is_empty() || text.starts_with('/') || text.contains('\0') || text.contains('\\') {
        return false;
    }
    text.split('/')
        .all(|segment| path_segment_ok(segment, true))
}

fn elided_tail_ok(text: &str) -> bool {
    if text.is_empty() || text.starts_with('/') || text.contains('\0') || text.contains('\\') {
        return false;
    }
    let mut parts = text.split('/');
    let Some(first) = parts.next() else {
        return false;
    };
    let first_len = first.chars().count();
    if first_len == 0 || first_len > 255 || first == "." || first == ".." {
        return false;
    }
    parts.all(|segment| path_segment_ok(segment, true))
}

fn path_segment_ok(segment: &str, reject_dot: bool) -> bool {
    let scalars = segment.chars().count();
    if scalars == 0 || scalars > 255 {
        return false;
    }
    if reject_dot && (segment == "." || segment == "..") {
        return false;
    }
    !segment.contains('\0') && !segment.contains('\\')
}

fn admit_project_path(value: &Node) -> Option<Vec<u8>> {
    if let Some(text) = rule_e_str(value) {
        if !logical_path_ok(text) {
            return None;
        }
        let mut out = Vec::new();
        push_json_string(text, &mut out);
        return Some(out);
    }
    let members = exact_members(object_pairs(value)?, &["elided"])?;
    let tail = rule_e_str(members[0])?;
    if !elided_tail_ok(tail) {
        return None;
    }
    let mut out = Vec::new();
    out.extend_from_slice(br#"{"elided":"#);
    push_json_string(tail, &mut out);
    out.push(b'}');
    Some(out)
}

fn admit_reduced(value: &Node) -> Option<Vec<u8>> {
    let members = exact_members(object_pairs(value)?, &["bytes", "truncated"])?;
    let bytes = u64_number(members[0])?;
    let truncated = bool_value(members[1])?;
    let mut out = Vec::new();
    out.extend_from_slice(br#"{"bytes":"#);
    push_u64(bytes, &mut out);
    out.extend_from_slice(br#","truncated":"#);
    push_flag(truncated, &mut out);
    out.push(b'}');
    Some(out)
}

fn admit_counts(value: &Node, width: usize) -> Option<Vec<u8>> {
    if width == 0 {
        return None;
    }
    let Value::Array(items) = &value.value else {
        return None;
    };
    if items.len() != width {
        return None;
    }
    let mut numbers = Vec::with_capacity(width);
    for item in items {
        numbers.push(u64_number(item)?);
    }
    let mut out = Vec::new();
    out.push(b'[');
    for (index, number) in numbers.iter().enumerate() {
        if index > 0 {
            out.push(b',');
        }
        push_u64(*number, &mut out);
    }
    out.push(b']');
    Some(out)
}

fn admit_position(value: &Node) -> Option<Vec<u8>> {
    let pairs = object_pairs(value)?;
    let members = if pairs.len() == 2 {
        exact_members(pairs, &["line", "column"])?
    } else {
        exact_members(pairs, &["line"])?
    };
    let line = u32_number(members[0])?;
    let column = if members.len() == 2 {
        Some(u32_number(members[1])?)
    } else {
        None
    };
    let mut out = Vec::new();
    out.extend_from_slice(br#"{"line":"#);
    push_u64(u64::from(line), &mut out);
    if let Some(column) = column {
        out.extend_from_slice(br#","column":"#);
        push_u64(u64::from(column), &mut out);
    }
    out.push(b'}');
    Some(out)
}

fn admit_unsigned(value: &Node) -> Option<Vec<u8>> {
    let number = u64_number(value)?;
    let mut out = Vec::new();
    push_u64(number, &mut out);
    Some(out)
}

fn admit_errno(value: &Node) -> Option<Vec<u8>> {
    let number = match value.value {
        Value::Number(Number::U64(value)) => i32::try_from(value).ok()?,
        Value::Number(Number::I64(value)) => i32::try_from(value).ok()?,
        _ => return None,
    };
    let mut out = Vec::new();
    push_i32(number, &mut out);
    Some(out)
}

fn admit_process_id(value: &Node) -> Option<Vec<u8>> {
    let number = u64_number(value)?;
    if !(1..=u64::from(u32::MAX)).contains(&number) {
        return None;
    }
    let mut out = Vec::new();
    push_u64(number, &mut out);
    Some(out)
}

fn admit_grammar(value: &Node, pred: impl Fn(&str) -> bool) -> Option<Vec<u8>> {
    let text = rule_e_str(value)?;
    if !pred(text) {
        return None;
    }
    let mut out = Vec::new();
    push_json_string(text, &mut out);
    Some(out)
}

fn version_ok(text: &str) -> bool {
    let bytes = text.as_bytes();
    (1..=64).contains(&bytes.len())
        && bytes.iter().all(|byte| {
            matches!(
                byte,
                b'0'..=b'9' | b'A'..=b'Z' | b'a'..=b'z' | b'.' | b'+' | b'-'
            )
        })
}

fn hex16(text: &str) -> bool {
    text.len() == 16
        && text
            .bytes()
            .all(|byte| matches!(byte, b'0'..=b'9' | b'a'..=b'f'))
}

fn admit_anchor(value: &Node) -> Option<Vec<u8>> {
    let members = exact_members(object_pairs(value)?, &["anchor", "tag"])?;
    let anchor = rule_e_str(members[0])?;
    let tag = rule_e_str(members[1])?;
    if anchor.len() > 16 || !PathAnchor::TEXT.contains(&anchor) || !hex16(tag) {
        return None;
    }
    let mut out = Vec::new();
    out.extend_from_slice(br#"{"anchor":"#);
    push_json_string(anchor, &mut out);
    out.extend_from_slice(br#","tag":"#);
    push_json_string(tag, &mut out);
    out.push(b'}');
    Some(out)
}

fn canonical_id_ok(text: &str) -> bool {
    let bytes = text.as_bytes();
    if bytes.is_empty() || bytes.len() > 128 || !bytes[0].is_ascii_lowercase() {
        return false;
    }
    let mut index = 1;
    while index < bytes.len() && matches!(bytes[index], b'a'..=b'z' | b'0'..=b'9') {
        index += 1;
    }
    while index < bytes.len() {
        if !matches!(bytes[index], b'.' | b'_' | b':' | b'-') {
            return false;
        }
        index += 1;
        let start = index;
        while index < bytes.len() && matches!(bytes[index], b'a'..=b'z' | b'0'..=b'9') {
            index += 1;
        }
        if index == start {
            return false;
        }
    }
    true
}

fn digest_ok(text: &str, prefix: &str) -> bool {
    let bytes = text.as_bytes();
    let prefix = prefix.as_bytes();
    if bytes.len() != prefix.len() + 64 || !bytes.starts_with(prefix) {
        return false;
    }
    bytes[prefix.len()..]
        .iter()
        .all(|byte| matches!(byte, b'0'..=b'9' | b'a'..=b'f'))
}

fn symbol_ok(text: &str) -> bool {
    let bytes = text.as_bytes();
    if bytes.is_empty() || bytes.len() > 128 {
        return false;
    }
    if !matches!(bytes[0], b'A'..=b'Z' | b'a'..=b'z' | b'_') {
        return false;
    }
    bytes[1..]
        .iter()
        .all(|byte| matches!(byte, b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'_'))
}

fn admit_open_code(table: &[&str], value: &Node) -> Option<Vec<u8>> {
    if let Some(text) = rule_e_str(value) {
        if !table.contains(&text) {
            return None;
        }
        let mut out = Vec::new();
        push_json_string(text, &mut out);
        return Some(out);
    }
    let members = exact_members(object_pairs(value)?, &["unrecognized"])?;
    let inner = exact_members(object_pairs(members[0])?, &["bytes", "truncated"])?;
    let bytes = u64_number(inner[0])?;
    let truncated = bool_value(inner[1])?;
    let mut out = Vec::new();
    out.extend_from_slice(br#"{"unrecognized":{"bytes":"#);
    push_u64(bytes, &mut out);
    out.extend_from_slice(br#","truncated":"#);
    push_flag(truncated, &mut out);
    out.extend_from_slice(b"}}");
    Some(out)
}

fn is_elided(node: &Node) -> bool {
    let Value::Object(pairs) = &node.value else {
        return false;
    };
    pairs.len() == 1 && pairs[0].0.text == "elided"
}

fn value_depth(node: &Node) -> usize {
    match &node.value {
        Value::Array(items) => 1 + items.iter().map(value_depth).max().unwrap_or(0),
        Value::Object(pairs) => {
            1 + pairs
                .iter()
                .map(|(_, child)| value_depth(child))
                .max()
                .unwrap_or(0)
        }
        _ => 0,
    }
}

fn encode(header: &Header<'_>, desc: &Desc, kept: &[Option<Vec<u8>>], omitted: u64) -> Vec<u8> {
    let mut out = Vec::with_capacity(256);
    out.push(b'{');
    push_string(&mut out, true, "ts", header.ts);
    push_string(&mut out, false, "level", Level::TEXT[header.level.index()]);
    push_string(&mut out, false, "event", desc.name);
    push_string(&mut out, false, "requestId", header.request);
    if let Some(text) = header.project {
        push_string(&mut out, false, "projectId", text);
    }
    if let Some(text) = header.plan {
        push_string(&mut out, false, "planId", text);
    }
    if let Some(text) = header.execution {
        push_string(&mut out, false, "executionId", text);
    }
    if let Some(text) = header.run {
        push_string(&mut out, false, "runId", text);
    }
    if let Some(text) = header.phase {
        push_string(&mut out, false, "phase", text);
    }
    out.extend_from_slice(br#","fields":"#);
    out.push(b'{');
    let mut wrote = false;
    for (index, field) in desc.fields.iter().enumerate() {
        let Some(encoded) = kept[index].as_ref() else {
            continue;
        };
        if wrote {
            out.push(b',');
        }
        wrote = true;
        out.push(b'"');
        out.extend_from_slice(field.key.as_bytes());
        out.extend_from_slice(b"\":");
        out.extend_from_slice(encoded);
    }
    out.push(b'}');
    // Count the canonical retained values, after refusal and projection.
    // An input count cannot be copied after a P2 elided value is removed.
    let truncated = kept
        .iter()
        .flatten()
        .filter(|value| value.starts_with(br#"{"elided":"#))
        .count();
    if truncated > 0 {
        out.extend_from_slice(br#","truncated":"#);
        push_u64(truncated as u64, &mut out);
    }
    if omitted > 0 {
        out.extend_from_slice(br#","omitted":"#);
        push_u64(omitted, &mut out);
    }
    out.push(b'}');
    out.push(b'\n');
    out
}

fn push_string(out: &mut Vec<u8>, first: bool, key: &str, value: &str) {
    if !first {
        out.push(b',');
    }
    out.push(b'"');
    out.extend_from_slice(key.as_bytes());
    out.extend_from_slice(b"\":");
    push_json_string(value, out);
}

const LEVELS: [Level; 5] = [
    Level::Error,
    Level::Warn,
    Level::Info,
    Level::Debug,
    Level::Trace,
];

fn parse_level(text: &str) -> Option<Level> {
    Level::TEXT
        .iter()
        .position(|item| *item == text)
        .map(|index| LEVELS[index])
}

fn timestamp_ok(text: &str) -> bool {
    let bytes = text.as_bytes();
    if bytes.len() != 24
        || bytes[4] != b'-'
        || bytes[7] != b'-'
        || bytes[10] != b'T'
        || bytes[13] != b':'
        || bytes[16] != b':'
        || bytes[19] != b'.'
        || bytes[23] != b'Z'
    {
        return false;
    }
    let Some(year) = digits(&bytes[0..4]) else {
        return false;
    };
    let Some(month) = digits(&bytes[5..7]) else {
        return false;
    };
    let Some(day) = digits(&bytes[8..10]) else {
        return false;
    };
    let Some(hour) = digits(&bytes[11..13]) else {
        return false;
    };
    let Some(minute) = digits(&bytes[14..16]) else {
        return false;
    };
    let Some(second) = digits(&bytes[17..19]) else {
        return false;
    };
    let Some(_) = digits(&bytes[20..23]) else {
        return false;
    };
    if !(1..=12).contains(&month) || hour > 23 || minute > 59 || second > 59 || day < 1 {
        return false;
    }
    day <= days_in_month(year, month)
}

fn days_in_month(year: u32, month: u32) -> u32 {
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => {
            if year.is_multiple_of(4) && (!year.is_multiple_of(100) || year.is_multiple_of(400)) {
                29
            } else {
                28
            }
        }
        _ => 0,
    }
}

fn digits(bytes: &[u8]) -> Option<u32> {
    let mut value = 0u32;
    for byte in bytes {
        let digit = byte.checked_sub(b'0')?;
        if digit > 9 {
            return None;
        }
        value = value * 10 + u32::from(digit);
    }
    Some(value)
}

fn request_id_ok(text: &str) -> bool {
    identity_ok(text, "req1_", 32)
}

fn identity_ok(text: &str, prefix: &str, hex_len: usize) -> bool {
    let bytes = text.as_bytes();
    let prefix = prefix.as_bytes();
    if bytes.len() != prefix.len() + hex_len || !bytes.starts_with(prefix) {
        return false;
    }
    bytes[prefix.len()..]
        .iter()
        .all(|byte| matches!(byte, b'0'..=b'9' | b'a'..=b'f'))
}

fn phase_ok(text: &str) -> bool {
    text.len() <= 32 && Phase::TEXT.contains(&text)
}

struct JStr {
    text: String,
    rule_e: bool,
}

enum Number {
    U64(u64),
    I64(i64),
    Other,
}

enum Value {
    Null,
    Bool(bool),
    Number(Number),
    String(JStr),
    Array(Vec<Node>),
    Object(Vec<(JStr, Node)>),
}

struct Node {
    start: usize,
    end: usize,
    value: Value,
}

fn parse_json(bytes: &[u8]) -> Result<Node, ()> {
    let mut index = 0;
    skip_ws(bytes, &mut index);
    let node = parse_value(bytes, &mut index, 0)?;
    skip_ws(bytes, &mut index);
    if index != bytes.len() {
        return Err(());
    }
    Ok(node)
}

/// Encoder-owned P2 scalar-string interiors. Keys are never P2. This only
/// computes coordinates; it grants no field, identity or scope admission.
pub(crate) fn json_projection_p2(
    bytes: &[u8],
    fields: &[(&str, PrivacyClass)],
) -> Option<Vec<(usize, usize)>> {
    let root = parse_json(bytes).ok()?;
    let pairs = object_pairs(&root)?;
    let values = pairs.iter().find(|(key, _)| key.text == "fields")?;
    let mut ranges = Vec::new();
    for (key, value) in object_pairs(&values.1)? {
        let class = fields.iter().find(|(name, _)| *name == key.text)?.1;
        if class == PrivacyClass::P2 {
            collect_string_ranges(value, 0, &mut ranges)?;
        }
    }
    Some(ranges)
}

pub(crate) fn encoded_value_p2(bytes: &[u8], base: usize) -> Option<(usize, Vec<(usize, usize)>)> {
    let mut index = 0;
    let value = parse_value(bytes, &mut index, 0).ok()?;
    let mut ranges = Vec::new();
    collect_string_ranges(&value, base, &mut ranges)?;
    Some((index, ranges))
}

fn collect_string_ranges(node: &Node, base: usize, ranges: &mut Vec<(usize, usize)>) -> Option<()> {
    match &node.value {
        Value::String(text) => {
            if !text.rule_e {
                return None;
            }
            ranges.push((base + node.start + 1, base + node.end - 1));
        }
        Value::Object(pairs) => {
            for (_, value) in pairs {
                collect_string_ranges(value, base, ranges)?;
            }
        }
        Value::Array(values) => {
            for value in values {
                collect_string_ranges(value, base, ranges)?;
            }
        }
        _ => {}
    }
    Some(())
}

fn skip_ws(bytes: &[u8], index: &mut usize) {
    while *index < bytes.len() {
        match bytes[*index] {
            b' ' | b'\t' | b'\n' | b'\r' => *index += 1,
            _ => break,
        }
    }
}

fn parse_value(bytes: &[u8], index: &mut usize, depth: usize) -> Result<Node, ()> {
    if depth > 8 || *index >= bytes.len() {
        return Err(());
    }
    match bytes[*index] {
        b'{' => parse_object(bytes, index, depth),
        b'[' => parse_array(bytes, index, depth),
        b'"' => parse_string(bytes, index),
        b't' => parse_literal(bytes, index, b"true", Value::Bool(true)),
        b'f' => parse_literal(bytes, index, b"false", Value::Bool(false)),
        b'n' => parse_literal(bytes, index, b"null", Value::Null),
        b'-' | b'0'..=b'9' => parse_number(bytes, index),
        _ => Err(()),
    }
}

fn parse_literal(
    bytes: &[u8],
    index: &mut usize,
    literal: &[u8],
    value: Value,
) -> Result<Node, ()> {
    let start = *index;
    if bytes.len() - *index < literal.len() || &bytes[*index..*index + literal.len()] != literal {
        return Err(());
    }
    *index += literal.len();
    Ok(Node {
        start,
        end: *index,
        value,
    })
}

fn parse_object(bytes: &[u8], index: &mut usize, depth: usize) -> Result<Node, ()> {
    let start = *index;
    *index += 1;
    let mut pairs = Vec::new();
    skip_ws(bytes, index);
    if *index < bytes.len() && bytes[*index] == b'}' {
        *index += 1;
        return Ok(Node {
            start,
            end: *index,
            value: Value::Object(pairs),
        });
    }
    loop {
        skip_ws(bytes, index);
        let key = match parse_string(bytes, index)?.value {
            Value::String(text) => text,
            _ => return Err(()),
        };
        if pairs.iter().any(|(existing, _)| existing.text == key.text) {
            return Err(());
        }
        skip_ws(bytes, index);
        if *index >= bytes.len() || bytes[*index] != b':' {
            return Err(());
        }
        *index += 1;
        skip_ws(bytes, index);
        let value = parse_value(bytes, index, depth + 1)?;
        pairs.push((key, value));
        skip_ws(bytes, index);
        if *index >= bytes.len() {
            return Err(());
        }
        match bytes[*index] {
            b',' => *index += 1,
            b'}' => {
                *index += 1;
                break;
            }
            _ => return Err(()),
        }
    }
    Ok(Node {
        start,
        end: *index,
        value: Value::Object(pairs),
    })
}

fn parse_array(bytes: &[u8], index: &mut usize, depth: usize) -> Result<Node, ()> {
    let start = *index;
    *index += 1;
    let mut items = Vec::new();
    skip_ws(bytes, index);
    if *index < bytes.len() && bytes[*index] == b']' {
        *index += 1;
        return Ok(Node {
            start,
            end: *index,
            value: Value::Array(items),
        });
    }
    loop {
        skip_ws(bytes, index);
        items.push(parse_value(bytes, index, depth + 1)?);
        skip_ws(bytes, index);
        if *index >= bytes.len() {
            return Err(());
        }
        match bytes[*index] {
            b',' => *index += 1,
            b']' => {
                *index += 1;
                break;
            }
            _ => return Err(()),
        }
    }
    Ok(Node {
        start,
        end: *index,
        value: Value::Array(items),
    })
}

fn parse_string(bytes: &[u8], index: &mut usize) -> Result<Node, ()> {
    if *index >= bytes.len() || bytes[*index] != b'"' {
        return Err(());
    }
    let start = *index;
    *index += 1;
    let body_start = *index;
    while *index < bytes.len() {
        let byte = bytes[*index];
        if byte == b'"' {
            let body = &bytes[body_start..*index];
            *index += 1;
            let text = finish_string(body)?;
            return Ok(Node {
                start,
                end: *index,
                value: Value::String(text),
            });
        }
        if byte == b'\\' {
            *index += 1;
            if *index >= bytes.len() {
                return Err(());
            }
            if bytes[*index] == b'u' {
                if *index + 4 >= bytes.len() {
                    return Err(());
                }
                for offset in 1..=4 {
                    if !is_hex(bytes[*index + offset]) {
                        return Err(());
                    }
                }
                *index += 5;
            } else {
                *index += 1;
            }
            continue;
        }
        if byte < 0x20 {
            return Err(());
        }
        let width = utf8_width(byte).ok_or(())?;
        if *index + width > bytes.len() {
            return Err(());
        }
        if std::str::from_utf8(&bytes[*index..*index + width]).is_err() {
            return Err(());
        }
        *index += width;
    }
    Err(())
}

fn finish_string(body: &[u8]) -> Result<JStr, ()> {
    if let Ok(text) = decode_rule_e_body(body) {
        return Ok(JStr { text, rule_e: true });
    }
    Ok(JStr {
        text: decode_json_body(body)?,
        rule_e: false,
    })
}

fn decode_json_body(body: &[u8]) -> Result<String, ()> {
    let mut out = String::new();
    let mut index = 0;
    while index < body.len() {
        if body[index] != b'\\' {
            let width = utf8_width(body[index]).ok_or(())?;
            if index + width > body.len() {
                return Err(());
            }
            let text = std::str::from_utf8(&body[index..index + width]).map_err(|_| ())?;
            let ch = text.chars().next().ok_or(())?;
            if (ch as u32) <= 0x1F {
                return Err(());
            }
            out.push(ch);
            index += width;
            continue;
        }
        let next = *body.get(index + 1).ok_or(())?;
        match next {
            b'"' | b'\\' | b'/' => {
                out.push(next as char);
                index += 2;
            }
            b'b' => {
                out.push('\u{0008}');
                index += 2;
            }
            b'f' => {
                out.push('\u{000c}');
                index += 2;
            }
            b'n' => {
                out.push('\n');
                index += 2;
            }
            b'r' => {
                out.push('\r');
                index += 2;
            }
            b't' => {
                out.push('\t');
                index += 2;
            }
            b'u' => {
                let unit = hex4(body, index + 2)?;
                index += 6;
                if (0xD800..=0xDBFF).contains(&unit) {
                    if body.get(index) != Some(&b'\\') || body.get(index + 1) != Some(&b'u') {
                        return Err(());
                    }
                    let low = hex4(body, index + 2)?;
                    if !(0xDC00..=0xDFFF).contains(&low) {
                        return Err(());
                    }
                    let point =
                        0x10000 + (u32::from(unit - 0xD800) << 10) + u32::from(low - 0xDC00);
                    out.push(char::from_u32(point).ok_or(())?);
                    index += 6;
                } else if (0xDC00..=0xDFFF).contains(&unit) {
                    return Err(());
                } else {
                    out.push(char::from_u32(u32::from(unit)).ok_or(())?);
                }
            }
            _ => return Err(()),
        }
    }
    Ok(out)
}

fn hex4(bytes: &[u8], start: usize) -> Result<u16, ()> {
    if start + 4 > bytes.len() {
        return Err(());
    }
    let mut value = 0u16;
    for byte in &bytes[start..start + 4] {
        if !is_hex(*byte) {
            return Err(());
        }
        let nibble = match byte {
            b'0'..=b'9' => byte - b'0',
            b'a'..=b'f' => byte - b'a' + 10,
            b'A'..=b'F' => byte - b'A' + 10,
            _ => return Err(()),
        };
        value = (value << 4) | u16::from(nibble);
    }
    Ok(value)
}

fn is_hex(byte: u8) -> bool {
    byte.is_ascii_hexdigit()
}

fn utf8_width(lead: u8) -> Option<usize> {
    if lead < 0x80 {
        Some(1)
    } else if lead & 0xE0 == 0xC0 && lead >= 0xC2 {
        Some(2)
    } else if lead & 0xF0 == 0xE0 {
        Some(3)
    } else if lead & 0xF8 == 0xF0 && lead <= 0xF4 {
        Some(4)
    } else {
        None
    }
}

fn parse_number(bytes: &[u8], index: &mut usize) -> Result<Node, ()> {
    let start = *index;
    if bytes[*index] == b'-' {
        *index += 1;
        if *index >= bytes.len() {
            return Err(());
        }
    }
    if bytes[*index] == b'0' {
        *index += 1;
        if *index < bytes.len() && bytes[*index].is_ascii_digit() {
            return Err(());
        }
    } else if bytes[*index].is_ascii_digit() {
        while *index < bytes.len() && bytes[*index].is_ascii_digit() {
            *index += 1;
        }
    } else {
        return Err(());
    }
    let mut other = false;
    if *index < bytes.len() && bytes[*index] == b'.' {
        other = true;
        *index += 1;
        if *index >= bytes.len() || !bytes[*index].is_ascii_digit() {
            return Err(());
        }
        while *index < bytes.len() && bytes[*index].is_ascii_digit() {
            *index += 1;
        }
    }
    if *index < bytes.len() && (bytes[*index] == b'e' || bytes[*index] == b'E') {
        other = true;
        *index += 1;
        if *index < bytes.len() && (bytes[*index] == b'+' || bytes[*index] == b'-') {
            *index += 1;
        }
        if *index >= bytes.len() || !bytes[*index].is_ascii_digit() {
            return Err(());
        }
        while *index < bytes.len() && bytes[*index].is_ascii_digit() {
            *index += 1;
        }
    }
    let raw = &bytes[start..*index];
    let number = if other {
        Number::Other
    } else {
        classify_integer(raw)
    };
    Ok(Node {
        start,
        end: *index,
        value: Value::Number(number),
    })
}

fn classify_integer(raw: &[u8]) -> Number {
    if raw.first() == Some(&b'-') {
        if raw == b"-0" {
            return Number::Other;
        }
        let Some(magnitude) = parse_u64(&raw[1..]) else {
            return Number::Other;
        };
        if magnitude > 1u64 << 63 {
            return Number::Other;
        }
        if magnitude == 1u64 << 63 {
            return Number::I64(i64::MIN);
        }
        return Number::I64(-(magnitude as i64));
    }
    parse_u64(raw).map(Number::U64).unwrap_or(Number::Other)
}

fn parse_u64(bytes: &[u8]) -> Option<u64> {
    if bytes.is_empty() {
        return None;
    }
    let mut value = 0u64;
    for byte in bytes {
        let digit = u64::from(byte - b'0');
        value = value.checked_mul(10)?.checked_add(digit)?;
    }
    Some(value)
}

const _: () = {
    assert!(same(HostRepairCompleted::FIELD_KEYS[0], "kind"));
    assert!(same(HostRepairCompleted::FIELD_KEYS[1], "state"));
    assert!(same(StorageCommitPublished::FIELD_KEYS[0], "latched"));
    assert!(same(StorageCommitNotPublished::FIELD_KEYS[0], "outcome"));
    assert!(HostRepairCompleted::FIELD_CLASSES.len() == REPAIR_FIELDS.len());
    assert!(StorageCommitPublished::FIELD_CLASSES.len() == PUBLISHED_FIELDS.len());
    assert!(StorageCommitNotPublished::FIELD_CLASSES.len() == NOT_PUBLISHED_FIELDS.len());
};

const fn same(left: &str, right: &str) -> bool {
    let left = left.as_bytes();
    let right = right.as_bytes();
    if left.len() != right.len() {
        return false;
    }
    let mut index = 0;
    while index < left.len() {
        if left[index] != right[index] {
            return false;
        }
        index += 1;
    }
    true
}

#[cfg(test)]
mod tests {
    use super::super::kinds::PrivacyClass;
    use super::CodeEnum;
    use super::readmit;

    fn contains(haystack: &[u8], needle: &[u8]) -> bool {
        haystack
            .windows(needle.len())
            .any(|window| window == needle)
    }

    const REPAIR: &[u8] = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"kind\":\"registration\",\"state\":\"RW-T3\"}}\n";

    #[test]
    fn phase_registrations_read_only_the_selected_fields_and_vocabulary() {
        use crate::kinds::registry::{HostPhaseCompleted, HostPhaseStarted, Phase, PhaseOutcome};
        use crate::kinds::{Code, Elapsed};
        let mut started=b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.phase.started\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":".to_vec();
        HostPhaseStarted::new(Phase::Delivery, Elapsed::new(17))
            .project_fields(PrivacyClass::P0, &mut started);
        started.extend_from_slice(b"}\n");
        let mut completed=b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.phase.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":".to_vec();
        HostPhaseCompleted::new(
            Code::from_enum(Phase::Delivery),
            Elapsed::new(6),
            Elapsed::new(3),
            Code::from_enum(PhaseOutcome::Completed),
            Elapsed::new(23),
        )
        .project_fields(PrivacyClass::P0, &mut completed);
        completed.extend_from_slice(b"}\n");
        for line in [&started, &completed] {
            let admitted = readmit(line, PrivacyClass::P0);
            assert_eq!(admitted.lines, vec![line.clone()]);
            assert_eq!(admitted.fields.invalid_value, 0);
        }
        let bad = std::str::from_utf8(&completed)
            .unwrap()
            .replace("completed\",\"at", "invented-outcome\",\"at");
        let admitted = readmit(bad.as_bytes(), PrivacyClass::P0);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.fields.invalid_value, 1);
        assert!(!contains(&admitted.lines[0], b"invented-outcome"));
    }

    #[test]
    fn loss_writer_readback_preserves_optional_error_pair_and_rejects_lone_errno() {
        use crate::kinds::Errno;
        use crate::kinds::registry::{IoErrorKind, LogLossCounted, Sink};
        use crate::writer::CapturedError;
        for error in [
            None,
            Some(CapturedError {
                kind: IoErrorKind::PermissionDenied,
                errno: Some(Errno::from_raw_os_error(13)),
            }),
        ] {
            let event = LogLossCounted::from_snapshot(Sink::Stderr, [u64::MAX; 40], error);
            let mut line=b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"warn\",\"event\":\"log.loss.counted\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":".to_vec();
            event.project_fields(PrivacyClass::P0, &mut line);
            line.extend_from_slice(b"}\n");
            let admitted = readmit(&line, PrivacyClass::P0);
            assert_eq!(admitted.lines, vec![line]);
            assert_eq!(admitted.fields.invalid_value, 0);
        }
        let line=b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"warn\",\"event\":\"log.loss.counted\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"sink\":\"stderr\",\"errno\":13}}\n";
        let admitted = readmit(line, PrivacyClass::P0);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.fields.invalid_value, 1);
        assert!(!contains(&admitted.lines[0], b"errno"));
    }

    #[test]
    fn o1d1_stream_round_trip_and_unknown_table_values_are_dropped() {
        let line = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"log.stream.opened\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"version\":\"0.1.0\",\"platform\":\"macos-aarch64\",\"build\":\"debug-assertions-on\",\"sink\":\"stderr\",\"pid\":1}}\n";
        let admitted = readmit(line, PrivacyClass::P1);
        assert_eq!(admitted.lines, vec![line.to_vec()]);
        assert_eq!(admitted.fields.invalid_value, 0);
        for (old, bad) in [
            ("macos-aarch64", "linux-aarch64-musl"),
            ("debug-assertions-on", "release"),
            ("stderr", "unknown-sink"),
        ] {
            let poisoned = std::str::from_utf8(line).unwrap().replace(old, bad);
            let admitted = readmit(poisoned.as_bytes(), PrivacyClass::P1);
            assert_eq!(admitted.lines.len(), 1);
            assert_eq!(admitted.fields.invalid_value, 1);
            assert!(!contains(&admitted.lines[0], bad.as_bytes()));
        }
    }

    #[test]
    fn a_repair_line_round_trips_and_a_bad_line_is_only_counted() {
        let mut input = REPAIR.to_vec();
        input.extend_from_slice(b"{not json\n");
        let admitted = readmit(&input, PrivacyClass::P2);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.lines[0], REPAIR);
        assert_eq!(admitted.records.malformed, 1);
        assert_eq!(admitted.records.oversize, 0);
        assert_eq!(admitted.records.header_invalid, 0);
        assert_eq!(admitted.records.unknown_event, 0);
        assert_eq!(admitted.fields.unknown_field, 0);
        assert_eq!(admitted.fields.invalid_value, 0);
    }

    #[test]
    fn shuffled_keys_canonicalize_and_rejected_bytes_are_not_echoed() {
        let line = b"{\"fields\":{\"state\":\"RW-T3\",\"note\":\"CANARY\",\"kind\":\"registration\"},\"requestId\":\"req1_abababababababababababababababab\",\"event\":\"host.repair.completed\",\"level\":\"info\",\"ts\":\"2023-11-14T22:13:20.000Z\"}\n";
        let admitted = readmit(line, PrivacyClass::P0);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.lines[0], REPAIR);
        assert_eq!(admitted.fields.unknown_field, 1);
        assert!(!contains(&admitted.lines[0], b"CANARY"));
        assert!(!contains(&admitted.lines[0], b"note"));
    }

    #[test]
    fn an_invalid_member_is_dropped_and_the_record_remains() {
        let line = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"kind\":\"CANARY\",\"state\":\"RW-T3\"}}\n";
        let admitted = readmit(line, PrivacyClass::P2);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.fields.invalid_value, 1);
        assert!(!contains(&admitted.lines[0], b"CANARY"));
        assert!(contains(&admitted.lines[0], b"\"state\":\"RW-T3\""));
        assert!(!contains(&admitted.lines[0], b"kind"));
    }

    #[test]
    fn header_and_descriptor_failures_use_their_reasons() {
        let bad_day = b"{\"ts\":\"2023-02-29T00:00:00.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{}}\n";
        let leap = b"{\"ts\":\"2024-02-29T00:00:00.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{},\"phase\":\"request\"}\n";
        let wrong_level = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"debug\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{}}\n";
        let unknown = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.missing\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{}}\n";
        let component = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"component\":\"host:1\",\"fields\":{}}\n";
        let short_escape = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\\n\",\"fields\":{}}\n";
        let duplicate = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{}}\n";
        let surrogate = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"\\uD800\",\"fields\":{}}\n";
        let mut input = Vec::new();
        for line in [
            bad_day as &[u8],
            wrong_level,
            unknown,
            component,
            short_escape,
            duplicate,
            surrogate,
            leap,
        ] {
            input.extend_from_slice(line);
        }
        let admitted = readmit(&input, PrivacyClass::P2);
        assert_eq!(admitted.lines.len(), 1);
        assert!(contains(&admitted.lines[0], b"\"phase\":\"request\""));
        assert_eq!(admitted.records.header_invalid, 4);
        assert_eq!(admitted.records.unknown_event, 1);
        assert_eq!(admitted.records.malformed, 2);
    }

    #[test]
    fn published_requires_the_committed_run_shape() {
        let request_only = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"storage.commit.published\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"latched\":true}}\n";
        let project = "c".repeat(64);
        let plan = "d".repeat(64);
        let execution = "e".repeat(32);
        let run = "f".repeat(64);
        let committed = format!(
            "{{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"storage.commit.published\",\"requestId\":\"req1_abababababababababababababababab\",\"projectId\":\"prj1-{project}\",\"planId\":\"plan2:{plan}\",\"executionId\":\"exec1_{execution}\",\"runId\":\"run3:{run}\",\"fields\":{{\"latched\":true}}}}\n"
        );
        let mut input = request_only.to_vec();
        input.extend_from_slice(committed.as_bytes());
        let admitted = readmit(&input, PrivacyClass::P2);
        assert_eq!(admitted.records.header_invalid, 1);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.lines[0], committed.as_bytes());
    }

    #[test]
    fn omitted_cannot_exceed_absent_fields_and_a_torn_line_is_malformed() {
        let too_many = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"kind\":\"registration\"},\"omitted\":2}\n";
        let one_absent = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"kind\":\"registration\"},\"omitted\":1}\n";
        let mut input = one_absent.to_vec();
        input.extend_from_slice(too_many);
        input.extend_from_slice(b"{\"ts\":\"2023-11-14T22:13:20.000Z\"}");
        let admitted = readmit(&input, PrivacyClass::P2);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.lines[0], one_absent);
        assert_eq!(admitted.records.header_invalid, 1);
        assert_eq!(admitted.records.malformed, 1);
    }

    #[test]
    fn a_line_past_the_bound_is_oversize_and_not_echoed() {
        let mut line = vec![b' '; 4096];
        line.extend_from_slice(b"CANARY\n");
        let admitted = readmit(&line, PrivacyClass::P2);
        assert!(admitted.lines.is_empty());
        assert_eq!(admitted.records.oversize, 1);
        assert_eq!(admitted.records.malformed, 0);
    }

    fn admitted(kind: super::FieldKind, json: &str) -> Option<Vec<u8>> {
        let node = super::parse_json(json.as_bytes()).expect("fixture json");
        let key = super::JStr {
            text: "value".into(),
            rule_e: true,
        };
        super::admit_field(
            super::FieldDesc {
                key: "value",
                class: PrivacyClass::P0,
                kind,
                max_value: 4096,
            },
            &key,
            &node,
        )
    }

    #[test]
    fn name_mints_writer_and_reader_agree_at_both_bounds() {
        use crate::kinds::{Form, SafeField};
        let set = crate::kinds::registry::CapabilitySet::issue();
        for text in [
            "a".to_owned(),
            "rule.name_1:code-other".to_owned(),
            "a".repeat(128),
        ] {
            let value = set.rule_id.admitted_entry(&text).unwrap();
            for form in [Form::Json, Form::Human] {
                let mut encoded = Vec::new();
                value.encode(form, &mut encoded);
                assert_eq!(
                    admitted(
                        super::FieldKind::Canonical,
                        std::str::from_utf8(&encoded).unwrap()
                    ),
                    Some(encoded)
                );
            }
        }
        for text in ["_".to_owned(), "OPEN_SIP_1".to_owned(), "A".repeat(128)] {
            let value = set.declared_name.declared_entry(&text).unwrap();
            for form in [Form::Json, Form::Human] {
                let mut encoded = Vec::new();
                value.encode(form, &mut encoded);
                assert_eq!(
                    admitted(
                        super::FieldKind::Symbol,
                        std::str::from_utf8(&encoded).unwrap()
                    ),
                    Some(encoded)
                );
            }
        }
    }

    #[test]
    fn k5_writer_and_reader_agree_on_every_selected_release_entry() {
        use crate::kinds::{ADMITTED_ID_MAX, AdmittedId, Form, SafeField};
        let members = [
            "calls",
            "clones-cross-tsjs",
            "clones-fact",
            "clones-near",
            "imports",
            "inventory",
            "linux-aarch64-gnu",
            "linux-x86_64-gnu",
            "macos-aarch64",
            "macos-x86_64",
            "reachability",
            "references",
            "syntax",
            "types",
            "unresolved-edge",
        ];
        for member in members {
            let entry = crate::catalog::lookup(member).expect("selected law entry");
            let field = AdmittedId::from(entry);
            let mut json = Vec::new();
            field.encode(Form::Json, &mut json);
            let mut human = Vec::new();
            field.encode(Form::Human, &mut human);
            assert_eq!(json, human);
            assert!(json.len() <= ADMITTED_ID_MAX);
            assert_eq!(
                admitted(
                    super::FieldKind::AdmittedId,
                    std::str::from_utf8(&json).unwrap()
                ),
                Some(json)
            );
        }
    }

    #[test]
    fn k5_rejects_unknown_values_aliases_and_whole_value_suffixes() {
        for value in [
            "",
            "unknown",
            "Calls",
            "macOS",
            "linux-x86_64-musl",
            "calls ",
            "calls\n",
            "calls\r",
            "calls\t",
            "callſ",
            "calls/unknown",
        ] {
            let mut json = Vec::new();
            crate::wire::push_json_string(value, &mut json);
            assert!(
                admitted(
                    super::FieldKind::AdmittedId,
                    std::str::from_utf8(&json).unwrap()
                )
                .is_none()
            );
            assert!(crate::catalog::lookup(value).is_none());
        }
        let over_bound = "x".repeat(129);
        let mut json = Vec::new();
        crate::wire::push_json_string(&over_bound, &mut json);
        assert!(
            admitted(
                super::FieldKind::AdmittedId,
                std::str::from_utf8(&json).unwrap()
            )
            .is_none()
        );
        assert!(admitted(super::FieldKind::AdmittedId, "1").is_none());
        assert!(admitted(super::FieldKind::AdmittedId, "true").is_none());
        assert!(admitted(super::FieldKind::AdmittedId, r#"{"catalog":"calls"}"#).is_none());
    }

    #[test]
    fn kind_predicates_canonicalize_and_drop_the_refused_forms() {
        assert_eq!(
            admitted(
                super::FieldKind::CodeLocation,
                r#"{"line":1,"file":"external"}"#
            )
            .unwrap(),
            br#"{"file":"external","line":1}"#
        );
        assert!(
            admitted(
                super::FieldKind::CodeLocation,
                r#"{"file":"crates/vendor_private.rs","line":1}"#
            )
            .is_none()
        );
        assert!(
            admitted(
                super::FieldKind::CodeLocation,
                r#"{"file":"external","line":1,"note":0}"#
            )
            .is_none()
        );
        assert!(
            admitted(
                super::FieldKind::CodeLocation,
                r#"{"file":"external ","line":1}"#
            )
            .is_none()
        );

        assert_eq!(
            admitted(super::FieldKind::ProjectPath, r#""a/..note""#).unwrap(),
            br#""a/..note""#
        );
        assert_eq!(
            admitted(super::FieldKind::ProjectPath, r#""a/...""#).unwrap(),
            br#""a/...""#
        );
        assert_eq!(
            admitted(super::FieldKind::ProjectPath, r#"{"elided":"a/b "}"#).unwrap(),
            br#"{"elided":"a/b "}"#
        );
        assert_eq!(
            admitted(super::FieldKind::ProjectPath, r#"{"elided":"a/b\u000a"}"#).unwrap(),
            br#"{"elided":"a/b\u000a"}"#
        );
        assert_eq!(
            admitted(super::FieldKind::ProjectPath, r#"{"elided":"a/b\u000d"}"#).unwrap(),
            br#"{"elided":"a/b\u000d"}"#
        );
        for refused in [
            r#""/private/x""#,
            r#""../x""#,
            r#""a/../b""#,
            r#""./a""#,
            r#""a//b""#,
            r#""a\\..\\b""#,
            r#""C:\\private\\name""#,
            r#"{"elided":".."}"#,
            r#"{"elided":"../x"}"#,
            r#"{"elided":"a/../b"}"#,
            r#"{"elided":"a\\b"}"#,
        ] {
            assert!(
                admitted(super::FieldKind::ProjectPath, refused).is_none(),
                "{refused}"
            );
        }

        assert_eq!(
            admitted(
                super::FieldKind::Reduced,
                r#"{"truncated":false,"bytes":2}"#
            )
            .unwrap(),
            br#"{"bytes":2,"truncated":false}"#
        );
        assert!(admitted(super::FieldKind::Reduced, r#"{"bytes":2}"#).is_none());

        assert_eq!(
            admitted(super::FieldKind::Counts(2), "[1,0]").unwrap(),
            b"[1,0]"
        );
        assert!(admitted(super::FieldKind::Counts(2), "[1]").is_none());
        assert!(admitted(super::FieldKind::Counts(0), "[1]").is_none());

        assert_eq!(
            admitted(super::FieldKind::Position, r#"{"column":4,"line":2}"#).unwrap(),
            br#"{"line":2,"column":4}"#
        );
        assert_eq!(
            admitted(super::FieldKind::Position, r#"{"line":2}"#).unwrap(),
            br#"{"line":2}"#
        );
        assert!(admitted(super::FieldKind::Position, r#"{"column":4}"#).is_none());

        assert_eq!(admitted(super::FieldKind::Unsigned, "0").unwrap(), b"0");
        assert_eq!(admitted(super::FieldKind::Errno, "-1").unwrap(), b"-1");
        assert_eq!(
            admitted(super::FieldKind::Errno, "-2147483648").unwrap(),
            b"-2147483648"
        );
        assert!(admitted(super::FieldKind::Errno, "-2147483649").is_none());
        assert!(admitted(super::FieldKind::Errno, "2147483648").is_none());
        assert_eq!(admitted(super::FieldKind::ProcessId, "1").unwrap(), b"1");
        assert!(admitted(super::FieldKind::ProcessId, "0").is_none());

        assert_eq!(
            admitted(super::FieldKind::Version, r#""v1.2.3+build""#).unwrap(),
            br#""v1.2.3+build""#
        );
        assert!(admitted(super::FieldKind::Version, r#""v1 ""#).is_none());

        assert_eq!(
            admitted(
                super::FieldKind::AnchorTag,
                r#"{"tag":"0123456789abcdef","anchor":"project"}"#
            )
            .unwrap(),
            br#"{"anchor":"project","tag":"0123456789abcdef"}"#
        );
        assert!(
            admitted(
                super::FieldKind::AnchorTag,
                r#"{"anchor":"project","tag":"0123456789ABCDEF"}"#
            )
            .is_none()
        );

        assert_eq!(
            admitted(super::FieldKind::Canonical, r#""host.repair""#).unwrap(),
            br#""host.repair""#
        );
        assert!(admitted(super::FieldKind::Canonical, r#""Host""#).is_none());
        assert_eq!(
            admitted(super::FieldKind::Symbol, r#""raw_os_error""#).unwrap(),
            br#""raw_os_error""#
        );
        assert!(admitted(super::FieldKind::Symbol, r#""1abc""#).is_none());
        let hex64 = "ab".repeat(32);
        assert_eq!(
            admitted(super::FieldKind::Digest(""), &format!("\"{hex64}\"")).unwrap(),
            format!("\"{hex64}\"").into_bytes()
        );
        assert_eq!(
            admitted(
                super::FieldKind::Digest("snapshot2:"),
                &format!("\"snapshot2:{hex64}\"")
            )
            .unwrap(),
            format!("\"snapshot2:{hex64}\"").into_bytes()
        );
        assert_eq!(
            admitted(
                super::FieldKind::Digest("closure2:"),
                &format!("\"closure2:{hex64}\"")
            )
            .unwrap(),
            format!("\"closure2:{hex64}\"").into_bytes()
        );
        assert!(
            admitted(
                super::FieldKind::Digest("snapshot2:"),
                &format!("\"snapshot2:{hex64} \"")
            )
            .is_none()
        );
        assert!(admitted(super::FieldKind::Digest(""), &format!("\"{hex64}g\"")).is_none());

        assert_eq!(
            admitted(
                super::FieldKind::OpenCode(super::RepairKind::TEXT),
                r#""registration""#
            )
            .unwrap(),
            br#""registration""#
        );
        assert_eq!(
            admitted(
                super::FieldKind::OpenCode(super::RepairKind::TEXT),
                r#"{"unrecognized":{"truncated":true,"bytes":3}}"#
            )
            .unwrap(),
            br#"{"unrecognized":{"bytes":3,"truncated":true}}"#
        );
        assert!(
            admitted(
                super::FieldKind::OpenCode(super::RepairKind::TEXT),
                r#""CANARY""#
            )
            .is_none()
        );
    }

    #[test]
    fn empty_open_code_reader_accepts_only_the_nontext_reduction() {
        assert_eq!(
            admitted(
                super::FieldKind::OpenCode(&[]),
                r#"{"unrecognized":{"truncated":false,"bytes":6}}"#
            )
            .unwrap(),
            br#"{"unrecognized":{"bytes":6,"truncated":false}}"#
        );
        assert!(admitted(super::FieldKind::OpenCode(&[]), r#""CANARY""#).is_none());
        assert!(admitted(super::FieldKind::OpenCode(&[]), r#""registration""#).is_none());
    }

    #[test]
    fn a_value_past_its_bound_is_dropped() {
        let node = super::parse_json(br#""registration""#).unwrap();
        let key = super::JStr {
            text: "kind".into(),
            rule_e: true,
        };
        let admitted = super::admit_field(
            super::FieldDesc {
                key: "kind",
                class: PrivacyClass::P0,
                kind: super::FieldKind::RepairKind,
                max_value: 4,
            },
            &key,
            &node,
        );
        assert!(admitted.is_none());
    }

    #[test]
    fn a_depth_three_field_is_dropped_and_the_record_remains() {
        let line = b"{\"ts\":\"2023-11-14T22:13:20.000Z\",\"level\":\"info\",\"event\":\"host.repair.completed\",\"requestId\":\"req1_abababababababababababababababab\",\"fields\":{\"kind\":{\"a\":{\"b\":{\"c\":1}}},\"state\":\"RW-T3\"}}\n";
        let admitted = readmit(line, PrivacyClass::P0);
        assert_eq!(admitted.lines.len(), 1);
        assert_eq!(admitted.fields.invalid_value, 1);
        assert!(contains(&admitted.lines[0], b"\"state\":\"RW-T3\""));
        assert!(!contains(&admitted.lines[0], b"\"kind\""));
    }
}

#[cfg(test)]
#[path = "readback_projection_tests.rs"]
mod projection_tests;
