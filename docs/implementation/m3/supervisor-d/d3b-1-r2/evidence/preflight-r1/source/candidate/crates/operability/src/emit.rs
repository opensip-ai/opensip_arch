//! Record emission (S-OP-2 items 9, 13c and 15).
//!
//! `EmitOn<Scope>` is the compile-time requirements check. A featureless build
//! writes the JSON line into the pre-scope buffer and the ring, and nowhere else.

use opensip_platform::observe_clock;

use crate::constants::{
    EXECUTION_ID_CAP, Level, MAX_LINE, PLAN_ID_CAP, PROJECT_ID_CAP, REQUEST_ID_CAP, RUN_ID_CAP,
};
use crate::kinds::PrivacyClass;
use crate::kinds::registry::{
    Event, HostPhaseCompleted, HostPhaseStarted, HostRepairCompleted, LogStreamOpened,
    StorageCommitNotPublished, StorageCommitPublished,
};
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
use crate::kinds::registry::{LogLossCounted, Sink};
use crate::kinds::registry::{
    ProviderFaultReduced, ProviderProcessReady, ProviderProcessSpawned, ProviderResourcesReported,
    ProviderStderrReduced, SupervisionCancelForced, SupervisionCancelSent,
    SupervisionLimitBreached, SupervisionLivenessMissed, SupervisionSampleIncomplete,
    SupervisionScratchRetained, SupervisionSettled, SupervisionTeardownStarted,
    SupervisionTreeSwept, SupervisionWaitExpired, ToolChildSettled, ToolLimitBreached,
    ToolProcessReaped, ToolProcessSpawned, ToolSampleIncomplete, ToolScratchRetained,
    ToolTeardownStarted, ToolWaitExpired,
};
use crate::kinds::registry::{
    ProviderProcessReaped, ProviderStageChanged, ProviderStageTerminal, SupervisionProgressAbsent,
    ToolTreeSwept,
};

use crate::scope::{
    AttemptScope, CommittedRunScope, PlanAttemptScope, PlanScope, ProjectScope, RequestScope,
    StoredRunScope,
};
use crate::transport::produce;
use crate::wire::push_json_string;

const REPAIR_SLOT: usize = 0;
const PUBLISHED_SLOT: usize = 1;
const NOT_PUBLISHED_SLOT: usize = 2;

pub(crate) struct Identities {
    request: crate::scope::RequestId,
    request_text: [u8; REQUEST_ID_CAP],
    project: Option<[u8; PROJECT_ID_CAP]>,
    plan: Option<[u8; PLAN_ID_CAP]>,
    execution: Option<[u8; EXECUTION_ID_CAP]>,
    run: Option<[u8; RUN_ID_CAP]>,
}

pub(crate) trait ScopeIds {
    fn identities(self) -> Identities;
}

impl ScopeIds for RequestScope {
    fn identities(self) -> Identities {
        Identities {
            request: self.request(),
            request_text: self.request().text(),
            project: None,
            plan: None,
            execution: None,
            run: None,
        }
    }
}

impl ScopeIds for ProjectScope {
    fn identities(self) -> Identities {
        Identities {
            request: self.request(),
            request_text: self.request().text(),
            project: Some(self.project().text()),
            plan: None,
            execution: None,
            run: None,
        }
    }
}

impl ScopeIds for PlanScope {
    fn identities(self) -> Identities {
        Identities {
            request: self.request(),
            request_text: self.request().text(),
            project: Some(self.project().text()),
            plan: Some(self.plan().text()),
            execution: None,
            run: None,
        }
    }
}

impl ScopeIds for AttemptScope {
    fn identities(self) -> Identities {
        Identities {
            request: self.request(),
            request_text: self.request().text(),
            project: Some(self.project().text()),
            plan: None,
            execution: Some(self.execution().text()),
            run: None,
        }
    }
}

impl ScopeIds for PlanAttemptScope {
    fn identities(self) -> Identities {
        Identities {
            request: self.request(),
            request_text: self.request().text(),
            project: Some(self.project().text()),
            plan: Some(self.plan().text()),
            execution: Some(self.execution().text()),
            run: None,
        }
    }
}

impl ScopeIds for CommittedRunScope {
    fn identities(self) -> Identities {
        Identities {
            request: self.request(),
            request_text: self.request().text(),
            project: Some(self.project().text()),
            plan: Some(self.plan().text()),
            execution: Some(self.execution().text()),
            run: Some(self.run().text()),
        }
    }
}

impl ScopeIds for StoredRunScope {
    fn identities(self) -> Identities {
        Identities {
            request: self.request(),
            request_text: self.request().text(),
            project: Some(self.project().text()),
            plan: None,
            execution: None,
            run: Some(self.run().text()),
        }
    }
}

mod emission_seal {
    pub trait Sealed {}
}
impl emission_seal::Sealed for HostRepairCompleted {}
impl emission_seal::Sealed for HostPhaseStarted {}
impl emission_seal::Sealed for HostPhaseCompleted {}
impl emission_seal::Sealed for LogStreamOpened {}
impl emission_seal::Sealed for StorageCommitPublished {}
impl emission_seal::Sealed for StorageCommitNotPublished {}

/// M3-D unit D3a-3: each provider and supervision event on the one scope
/// that carries exactly its required identities (Project, Plan, Execution),
/// and the tool events on a Project scope (M3-D r5 item 21, :692). Each has
/// its own per-name budget slot.
macro_rules! registered_on {
    ($($event:ident on $scope:ty => $slot:expr),+ $(,)?) => {
        $(
            impl emission_seal::Sealed for $event {}
            impl EmitOn<$scope> for $event {
                fn emit(self, scope: $scope) {
                    submit(
                        Self::NAME,
                        Self::LEVEL,
                        Self::TEMPLATE,
                        $slot,
                        scope.identities(),
                        Projection {
                            max_line: Self::MAX_LINE,
                            privacy: Self::FIELD_PRIVACY,
                            fields: |ceiling, out: &mut Vec<u8>| self.project_fields(ceiling, out),
                            human: |ceiling, out: &mut Vec<u8>| self.project_fields_human(ceiling, out),
                            truncated: |ceiling| self.projected_truncated(ceiling),
                        },
                    );
                }
            }
        )+
    };
}

registered_on!(
    ProviderProcessSpawned on PlanAttemptScope => 6,
    ProviderProcessReady on PlanAttemptScope => 7,
    ProviderStderrReduced on PlanAttemptScope => 8,
    ProviderFaultReduced on PlanAttemptScope => 9,
    ProviderResourcesReported on PlanAttemptScope => 10,
    SupervisionLivenessMissed on PlanAttemptScope => 11,
    SupervisionLimitBreached on PlanAttemptScope => 12,
    SupervisionSampleIncomplete on PlanAttemptScope => 13,
    SupervisionCancelSent on PlanAttemptScope => 14,
    SupervisionCancelForced on PlanAttemptScope => 15,
    SupervisionWaitExpired on PlanAttemptScope => 16,
    SupervisionTeardownStarted on PlanAttemptScope => 17,
    SupervisionTreeSwept on PlanAttemptScope => 18,
    SupervisionScratchRetained on PlanAttemptScope => 19,
    SupervisionSettled on PlanAttemptScope => 20,
    ToolProcessSpawned on ProjectScope => 21,
    ToolProcessReaped on ProjectScope => 22,
    ToolLimitBreached on ProjectScope => 23,
    ToolSampleIncomplete on ProjectScope => 24,
    ToolWaitExpired on ProjectScope => 25,
    ToolTeardownStarted on ProjectScope => 26,
    ToolScratchRetained on ProjectScope => 27,
    ToolChildSettled on ProjectScope => 28,
    // D3a-4 (S-OP-2c item 23a).
    ProviderStageChanged on PlanAttemptScope => 29,
    ProviderStageTerminal on PlanAttemptScope => 30,
    ProviderProcessReaped on PlanAttemptScope => 31,
    SupervisionProgressAbsent on PlanAttemptScope => 32,
    // D3b-1 (D3b plan r3, LD-D3B-9).
    ToolTreeSwept on ProjectScope => 33,
);

pub trait EmitOn<S>: emission_seal::Sealed {
    fn emit(self, scope: S);
}

struct Projection<F, H, T> {
    max_line: usize,
    privacy: &'static [(&'static str, PrivacyClass)],
    fields: F,
    human: H,
    truncated: T,
}

fn submit(
    name: &'static str,
    level: Level,
    template: &'static str,
    slot: usize,
    ids: Identities,
    projection: Projection<
        impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
        impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
        impl Fn(PrivacyClass) -> usize,
    >,
) {
    produce(level, slot, ids.request, projection.max_line, &|| {
        encode_pair(name, level, template, &ids, &projection)
    });
}

macro_rules! repair_on {
    ($($scope:ty),+ $(,)?) => {
        $(
            impl EmitOn<$scope> for HostRepairCompleted {
                fn emit(self, scope: $scope) {
                    let ids = scope.identities();
                    submit(
                        HostRepairCompleted::NAME,
                        HostRepairCompleted::LEVEL,
                        HostRepairCompleted::TEMPLATE,
                        REPAIR_SLOT,
                        ids,
                        Projection {
                            max_line: Self::MAX_LINE,
                            privacy: Self::FIELD_PRIVACY,
                            fields: |ceiling, out: &mut Vec<u8>| self.project_fields(ceiling, out),
                            human: |ceiling, out: &mut Vec<u8>| self.project_fields_human(ceiling, out),
                            truncated: |ceiling| self.projected_truncated(ceiling),
                        },
                    );
                }
            }
        )+
    };
}

repair_on!(
    RequestScope,
    ProjectScope,
    PlanScope,
    AttemptScope,
    PlanAttemptScope,
    CommittedRunScope,
    StoredRunScope,
);

impl EmitOn<RequestScope> for LogStreamOpened {
    fn emit(self, scope: RequestScope) {
        submit(
            Self::NAME,
            Self::LEVEL,
            Self::TEMPLATE,
            3,
            scope.identities(),
            Projection {
                max_line: Self::MAX_LINE,
                privacy: Self::FIELD_PRIVACY,
                fields: |ceiling, out: &mut Vec<u8>| self.project_fields(ceiling, out),
                human: |ceiling, out: &mut Vec<u8>| self.project_fields_human(ceiling, out),
                truncated: |ceiling| self.projected_truncated(ceiling),
            },
        );
    }
}

macro_rules! phase_on {
    ($event:ident, $slot:expr) => {
        impl EmitOn<RequestScope> for $event {
            fn emit(self, scope: RequestScope) {
                submit(
                    Self::NAME,
                    Self::LEVEL,
                    Self::TEMPLATE,
                    $slot,
                    scope.identities(),
                    Projection {
                        max_line: Self::MAX_LINE,
                        privacy: Self::FIELD_PRIVACY,
                        fields: |ceiling, out: &mut Vec<u8>| self.project_fields(ceiling, out),
                        human: |ceiling, out: &mut Vec<u8>| self.project_fields_human(ceiling, out),
                        truncated: |ceiling| self.projected_truncated(ceiling),
                    },
                );
            }
        }
    };
}
phase_on!(HostPhaseStarted, 4);
phase_on!(HostPhaseCompleted, 5);

impl EmitOn<CommittedRunScope> for StorageCommitPublished {
    fn emit(self, scope: CommittedRunScope) {
        let ids = scope.identities();
        submit(
            StorageCommitPublished::NAME,
            StorageCommitPublished::LEVEL,
            StorageCommitPublished::TEMPLATE,
            PUBLISHED_SLOT,
            ids,
            Projection {
                max_line: Self::MAX_LINE,
                privacy: Self::FIELD_PRIVACY,
                fields: |ceiling, out: &mut Vec<u8>| self.project_fields(ceiling, out),
                human: |ceiling, out: &mut Vec<u8>| self.project_fields_human(ceiling, out),
                truncated: |ceiling| self.projected_truncated(ceiling),
            },
        );
    }
}

impl EmitOn<PlanAttemptScope> for StorageCommitNotPublished {
    fn emit(self, scope: PlanAttemptScope) {
        let ids = scope.identities();
        submit(
            StorageCommitNotPublished::NAME,
            StorageCommitNotPublished::LEVEL,
            StorageCommitNotPublished::TEMPLATE,
            NOT_PUBLISHED_SLOT,
            ids,
            Projection {
                max_line: Self::MAX_LINE,
                privacy: Self::FIELD_PRIVACY,
                fields: |ceiling, out: &mut Vec<u8>| self.project_fields(ceiling, out),
                human: |ceiling, out: &mut Vec<u8>| self.project_fields_human(ceiling, out),
                truncated: |ceiling| self.projected_truncated(ceiling),
            },
        );
    }
}

fn encode_pair(
    name: &str,
    level: Level,
    template: &str,
    ids: &Identities,
    projection: &Projection<
        impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
        impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
        impl Fn(PrivacyClass) -> usize,
    >,
) -> Option<crate::guard::ProjectedRecords> {
    use crate::guard::{ProjectedRecords, ProjectionForm, SealedRecord};
    let clock = observe_clock().ok()?;
    let stamp = format_timestamp(clock.wall_unix_seconds(), clock.wall_nanoseconds())?;
    let file = SealedRecord::from_encoder(
        encode_line(
            &stamp,
            name,
            level,
            ids,
            PrivacyClass::P2,
            &projection.fields,
            (projection.truncated)(PrivacyClass::P2),
        )?,
        ProjectionForm::Json,
        projection.privacy,
    )
    .ok()?;
    let ring = if level.admits_ring() {
        Some(
            SealedRecord::from_encoder(
                encode_line(
                    &stamp,
                    name,
                    level,
                    ids,
                    PrivacyClass::P1,
                    &projection.fields,
                    (projection.truncated)(PrivacyClass::P1),
                )?,
                ProjectionForm::Json,
                projection.privacy,
            )
            .ok()?,
        )
    } else {
        None
    };
    let human = SealedRecord::from_encoder(
        encode_human_with_truncated(
            level,
            name,
            template,
            ids,
            &projection.human,
            (projection.truncated)(PrivacyClass::P2),
        )?,
        ProjectionForm::Human,
        projection.privacy,
    )
    .ok()?;
    Some(ProjectedRecords { file, ring, human })
}

#[cfg(test)]
pub(crate) fn encode_human(
    level: Level,
    name: &str,
    template: &str,
    ids: &Identities,
    fields: &impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
) -> Option<Vec<u8>> {
    encode_human_with_truncated(level, name, template, ids, fields, 0)
}

fn encode_human_with_truncated(
    level: Level,
    name: &str,
    template: &str,
    ids: &Identities,
    fields: &impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
    truncated: usize,
) -> Option<Vec<u8>> {
    encode_human_into(
        level,
        name,
        template,
        ids,
        fields,
        truncated,
        Vec::with_capacity(256),
    )
}

fn encode_human_into(
    level: Level,
    name: &str,
    template: &str,
    ids: &Identities,
    fields: &impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
    truncated: usize,
    mut out: Vec<u8>,
) -> Option<Vec<u8>> {
    out.clear();
    out.extend_from_slice(Level::TEXT[level.index()].as_bytes());
    out.push(b' ');
    out.extend_from_slice(name.as_bytes());
    out.extend_from_slice(b": ");
    out.extend_from_slice(template.as_bytes());
    push_human_id(&mut out, "requestId", &ids.request_text)?;
    if let Some(text) = ids.project.as_ref() {
        push_human_id(&mut out, "projectId", text)?;
    }
    if let Some(text) = ids.plan.as_ref() {
        push_human_id(&mut out, "planId", text)?;
    }
    if let Some(text) = ids.execution.as_ref() {
        push_human_id(&mut out, "executionId", text)?;
    }
    if let Some(text) = ids.run.as_ref() {
        push_human_id(&mut out, "runId", text)?;
    }
    let omitted = fields(PrivacyClass::P2, &mut out);
    if omitted > 0 {
        out.extend_from_slice(b" omitted=");
        push_u32(&mut out, omitted as u32);
    }
    if truncated > 0 {
        out.extend_from_slice(b" truncated=");
        push_u32(&mut out, truncated as u32);
    }
    out.push(b'\n');
    if out.len() > MAX_LINE {
        None
    } else {
        Some(out)
    }
}

#[cfg(feature = "operability-dev-sinks")]
pub(crate) fn encode_loss_marker(
    request: crate::scope::RequestId,
    counts: [u64; 40],
    error: Option<crate::writer::CapturedError>,
    slot: Vec<u8>,
) -> Option<crate::guard::SealedRecord> {
    let ids = Identities {
        request,
        request_text: request.text(),
        project: None,
        plan: None,
        execution: None,
        run: None,
    };
    let event = LogLossCounted::from_snapshot(Sink::Stderr, counts, error);
    let bytes = encode_human_into(
        LogLossCounted::LEVEL,
        LogLossCounted::NAME,
        LogLossCounted::TEMPLATE,
        &ids,
        &|ceiling, out| event.project_fields_human(ceiling, out),
        event.projected_truncated(PrivacyClass::P2),
        slot,
    )?;
    crate::guard::SealedRecord::from_encoder(
        bytes,
        crate::guard::ProjectionForm::Human,
        LogLossCounted::FIELD_PRIVACY,
    )
    .ok()
}

fn push_human_id(out: &mut Vec<u8>, key: &str, value: &[u8]) -> Option<()> {
    let text = std::str::from_utf8(value).ok()?;
    out.push(b' ');
    out.extend_from_slice(key.as_bytes());
    out.push(b'=');
    push_json_string(text, out);
    Some(())
}

fn encode_line(
    stamp: &[u8; 24],
    name: &str,
    level: Level,
    ids: &Identities,
    ceiling: PrivacyClass,
    fields: &impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
    truncated: usize,
) -> Option<Vec<u8>> {
    encode_line_into(
        LineHeader { stamp, name, level },
        ids,
        ceiling,
        fields,
        truncated,
        Vec::with_capacity(256),
    )
}

struct LineHeader<'a> {
    stamp: &'a [u8; 24],
    name: &'a str,
    level: Level,
}

fn encode_line_into(
    header: LineHeader<'_>,
    ids: &Identities,
    ceiling: PrivacyClass,
    fields: &impl Fn(PrivacyClass, &mut Vec<u8>) -> usize,
    truncated: usize,
    mut out: Vec<u8>,
) -> Option<Vec<u8>> {
    let LineHeader { stamp, name, level } = header;
    out.clear();
    out.push(b'{');
    if !push_text(&mut out, true, "ts", stamp) {
        return None;
    }
    if !push_text(
        &mut out,
        false,
        "level",
        Level::TEXT[level.index()].as_bytes(),
    ) {
        return None;
    }
    if !push_text(&mut out, false, "event", name.as_bytes()) {
        return None;
    }
    if !push_text(&mut out, false, "requestId", &ids.request_text) {
        return None;
    }
    if let Some(text) = ids.project.as_ref()
        && !push_text(&mut out, false, "projectId", text)
    {
        return None;
    }
    if let Some(text) = ids.plan.as_ref()
        && !push_text(&mut out, false, "planId", text)
    {
        return None;
    }
    if let Some(text) = ids.execution.as_ref()
        && !push_text(&mut out, false, "executionId", text)
    {
        return None;
    }
    if let Some(text) = ids.run.as_ref()
        && !push_text(&mut out, false, "runId", text)
    {
        return None;
    }
    out.extend_from_slice(br#","fields":"#);
    let omitted = fields(ceiling, &mut out);
    if omitted > 0 {
        out.extend_from_slice(br#","omitted":"#);
        push_u32(&mut out, omitted as u32);
    }
    if truncated > 0 {
        out.extend_from_slice(br#","truncated":"#);
        push_u32(&mut out, truncated as u32);
    }
    out.push(b'}');
    out.push(b'\n');
    if out.len() > MAX_LINE {
        None
    } else {
        Some(out)
    }
}

fn push_text(out: &mut Vec<u8>, first: bool, key: &str, value: &[u8]) -> bool {
    let Ok(text) = std::str::from_utf8(value) else {
        return false;
    };
    if !first {
        out.push(b',');
    }
    out.push(b'"');
    out.extend_from_slice(key.as_bytes());
    out.extend_from_slice(br#"":"#);
    push_json_string(text, out);
    true
}

fn push_u32(out: &mut Vec<u8>, mut value: u32) {
    let mut buf = [0u8; 10];
    let mut index = buf.len();
    loop {
        index -= 1;
        buf[index] = b'0' + (value % 10) as u8;
        value /= 10;
        if value == 0 {
            break;
        }
    }
    out.extend_from_slice(&buf[index..]);
}

pub(crate) fn format_timestamp(seconds: i64, nanos: u32) -> Option<[u8; 24]> {
    if seconds < 0 || nanos >= 1_000_000_000 {
        return None;
    }
    let days = seconds / 86_400;
    let tod = (seconds % 86_400) as u32;
    let (year, month, day) = civil_from_days(days)?;
    if !(0..=9999).contains(&year) {
        return None;
    }
    let hour = tod / 3600;
    let minute = (tod % 3600) / 60;
    let second = tod % 60;
    let millis = nanos / 1_000_000;
    let mut out = [0u8; 24];
    write_digits(&mut out[0..4], year as u32);
    out[4] = b'-';
    write_digits(&mut out[5..7], month);
    out[7] = b'-';
    write_digits(&mut out[8..10], day);
    out[10] = b'T';
    write_digits(&mut out[11..13], hour);
    out[13] = b':';
    write_digits(&mut out[14..16], minute);
    out[16] = b':';
    write_digits(&mut out[17..19], second);
    out[19] = b'.';
    write_digits(&mut out[20..23], millis);
    out[23] = b'Z';
    Some(out)
}

fn write_digits(out: &mut [u8], mut value: u32) {
    let mut index = out.len();
    while index > 0 {
        index -= 1;
        out[index] = b'0' + (value % 10) as u8;
        value /= 10;
    }
}

/// Howard Hinnant's `civil_from_days`. `z` is days since 1970-01-01.
fn civil_from_days(mut z: i64) -> Option<(i64, u32, u32)> {
    z += 719_468;
    let era = if z >= 0 { z } else { z - 146_096 } / 146_097;
    let doe = (z - era * 146_097) as u64;
    let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    let year_of_era = yoe as i64 + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let day = doy - (153 * mp + 2) / 5 + 1;
    let month = if mp < 10 { mp + 3 } else { mp - 9 };
    let year = if month <= 2 {
        year_of_era + 1
    } else {
        year_of_era
    };
    if !(1..=12).contains(&month) || !(1..=31).contains(&day) {
        return None;
    }
    Some((year, month as u32, day as u32))
}

#[cfg(test)]
mod tests {
    use super::{ScopeIds, encode_human, format_timestamp};
    use crate::kinds::Code;
    use crate::kinds::registry::{Event, HostRepairCompleted, RepairKind, RepairState};
    use crate::scope::test_request_scope;

    #[test]
    fn project_path_elision_count_is_recomputed_per_projection() {
        use crate::kinds::{Form, PrivacyClass, SafeField};
        let set = crate::kinds::registry::CapabilitySet::issue();
        let value = set
            .project_path
            .admitted_path(&"\u{202e}".repeat(255))
            .unwrap();
        let ids = test_request_scope([0xab; 16]).identities();
        let stamp = format_timestamp(1_700_000_000, 0).unwrap();
        let fields = |ceiling: PrivacyClass, out: &mut Vec<u8>| {
            if ceiling >= PrivacyClass::P2 {
                out.extend_from_slice(b"{\"path\":");
                value.encode(Form::Json, out);
                out.push(b'}');
                0
            } else {
                out.extend_from_slice(b"{}");
                1
            }
        };
        let full = super::encode_line(
            &stamp,
            "discovery.path.skipped",
            crate::constants::Level::Info,
            &ids,
            PrivacyClass::P2,
            &fields,
            usize::from(value.truncated()),
        )
        .unwrap();
        assert!(
            std::str::from_utf8(&full)
                .unwrap()
                .ends_with(",\"truncated\":1}\n")
        );
        let projected = super::encode_line(
            &stamp,
            "discovery.path.skipped",
            crate::constants::Level::Info,
            &ids,
            PrivacyClass::P1,
            &fields,
            0,
        )
        .unwrap();
        let text = std::str::from_utf8(&projected).unwrap();
        assert!(!text.contains("elided"));
        assert!(!text.contains("truncated"));
        assert!(text.ends_with(",\"omitted\":1}\n"));
    }

    #[test]
    fn human_line_uses_the_template_and_the_request_id() {
        let scope = test_request_scope([0xab; 16]);
        let repair = HostRepairCompleted::new(
            Code::from_enum(RepairKind::Registration),
            Code::from_enum(RepairState::RwT3),
        );
        let line = encode_human(
            HostRepairCompleted::LEVEL,
            HostRepairCompleted::NAME,
            HostRepairCompleted::TEMPLATE,
            &scope.identities(),
            &|ceiling, out| repair.project_fields_human(ceiling, out),
        )
        .expect("human line");
        assert_eq!(
            line,
            b"info host.repair.completed: repair completed requestId=\"req1_abababababababababababababababab\" kind=\"registration\" state=\"RW-T3\"\n"
        );
    }

    #[test]
    fn timestamps_match_the_pinned_instants() {
        let epoch = format_timestamp(0, 0).expect("epoch");
        assert_eq!(&epoch, b"1970-01-01T00:00:00.000Z");
        let known = format_timestamp(1_700_000_000, 0).expect("known instant");
        assert_eq!(&known, b"2023-11-14T22:13:20.000Z");
        let millis = format_timestamp(0, 7_000_000).expect("millis");
        assert_eq!(&millis, b"1970-01-01T00:00:00.007Z");
        assert!(format_timestamp(-1, 0).is_none());
        assert!(format_timestamp(0, 1_000_000_000).is_none());
    }
    #[test]
    fn one_field_counterexample_uses_actual_rule_e_and_stays_within_1060_bytes() {
        use crate::kinds::{Form, PrivacyClass, SafeField};
        const KEY: &str = "abcdefghijklmnopqrstuvwxyz123456";
        const PRIVACY: &[(&str, PrivacyClass)] = &[(KEY, PrivacyClass::P2)];
        let set = crate::kinds::registry::CapabilitySet::issue();
        let name = format!("{}abc", "\u{202e}".repeat(252));
        let path = set.project_path.admitted_path(&name).unwrap();
        let mut value = Vec::new();
        path.encode(Form::Human, &mut value);
        assert_eq!(value.len(), 256);
        assert!(path.truncated());
        let scope =
            crate::scope::test_committed_run_scope([1; 16], [2; 32], [3; 32], [4; 16], [5; 32]);
        let ids = scope.identities();
        // These are synthetic CAP occupants, never admitted ComponentRole
        // members or a registry event. They exercise the conservative encoding
        // proof without inventing an owning table or a production call site.
        let component = format!("{}:65535", "r".repeat(32));
        let phase = "p".repeat(32);
        let fields = |_: PrivacyClass, out: &mut Vec<u8>| {
            super::push_human_id(out, "component", component.as_bytes()).unwrap();
            super::push_human_id(out, "phase", phase.as_bytes()).unwrap();
            out.push(b' ');
            out.extend_from_slice(KEY.as_bytes());
            out.push(b'=');
            path.encode(Form::Human, out);
            0
        };
        let human = super::encode_human_with_truncated(
            crate::constants::Level::Error,
            &"e".repeat(96),
            &"m".repeat(160),
            &ids,
            &fields,
            1,
        )
        .unwrap();
        assert_eq!(human.len(), 1002);
        assert!(human.len() <= 1060);
        let record = crate::guard::SealedRecord::from_encoder(
            human,
            crate::guard::ProjectionForm::Human,
            PRIVACY,
        )
        .unwrap();
        assert!(record.inspect().unwrap().lawful());
        let mut pre = crate::sinks::pre_scope();
        assert!(pre.try_reserve(1060));
        assert!(pre.finish_reserve(1060, record.bytes()));
        let mut ring = crate::sinks::ring();
        // Static P0/P1 projection omits this whole P2 field and recomputes
        // truncated to zero, even though the full projection elided it.
        let ring_fields = |_: PrivacyClass, _: &mut Vec<u8>| 1;
        let projected = super::encode_human_with_truncated(
            crate::constants::Level::Error,
            &"e".repeat(96),
            &"m".repeat(160),
            &ids,
            &ring_fields,
            0,
        )
        .unwrap();
        assert!(!projected.windows(6).any(|part| part == b"elided"));
        assert!(!projected.windows(9).any(|part| part == b"truncated"));
        assert!(ring.push_overwrite(&projected));
        assert_eq!(pre.first(), Some(record.bytes()));
        assert_eq!(ring.first(), Some(projected.as_slice()));
    }
}

#[cfg(test)]
#[path = "privacy_sink_tests.rs"]
mod privacy_tests;

// A clock-unavailable phase is an actual known-event producer refusal, never
// a completed event with made-up zero timings. Reserve before this refusal.
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
pub(crate) fn refuse_phase(scope: RequestScope, started: bool) {
    let (slot, max_line) = if started {
        (4, HostPhaseStarted::MAX_LINE)
    } else {
        (5, HostPhaseCompleted::MAX_LINE)
    };
    crate::transport::produce(Level::Info, slot, scope.request(), max_line, &|| None);
}

#[cfg(feature = "harness-instrumentation")]
pub(crate) fn encode_harness_opened(
    scope: RequestScope,
    pid: crate::kinds::ProcessId,
) -> Option<crate::guard::SealedRecord> {
    use crate::kinds::registry::{BuildProfile, Platform};
    use crate::kinds::{Code, Version};
    let event = LogStreamOpened::new(
        Version::RELEASE,
        Code::from_enum(Platform::compiled()?),
        Code::from_enum(BuildProfile::compiled()),
        Code::from_enum(Sink::Harness),
        pid,
    );
    let clock = observe_clock().ok()?;
    let stamp = format_timestamp(clock.wall_unix_seconds(), clock.wall_nanoseconds())?;
    let bytes = encode_line(
        &stamp,
        LogStreamOpened::NAME,
        LogStreamOpened::LEVEL,
        &scope.identities(),
        PrivacyClass::P1,
        &|ceiling, out| event.project_fields(ceiling, out),
        0,
    )?;
    crate::guard::SealedRecord::from_encoder(
        bytes,
        crate::guard::ProjectionForm::Json,
        LogStreamOpened::FIELD_PRIVACY,
    )
    .ok()
}

#[cfg(feature = "harness-instrumentation")]
pub(crate) fn encode_harness_loss_marker(
    request: crate::scope::RequestId,
    counts: [u64; 40],
    error: Option<crate::writer::CapturedError>,
    slot: Vec<u8>,
) -> Option<crate::guard::SealedRecord> {
    let ids = Identities {
        request,
        request_text: request.text(),
        project: None,
        plan: None,
        execution: None,
        run: None,
    };
    let event = LogLossCounted::from_snapshot(Sink::Harness, counts, error);
    let clock = observe_clock().ok()?;
    let stamp = format_timestamp(clock.wall_unix_seconds(), clock.wall_nanoseconds())?;
    let bytes = encode_line_into(
        LineHeader {
            stamp: &stamp,
            name: LogLossCounted::NAME,
            level: LogLossCounted::LEVEL,
        },
        &ids,
        PrivacyClass::P1,
        &|ceiling, out| event.project_fields(ceiling, out),
        0,
        slot,
    )?;
    crate::guard::SealedRecord::from_encoder(
        bytes,
        crate::guard::ProjectionForm::Json,
        LogLossCounted::FIELD_PRIVACY,
    )
    .ok()
}
