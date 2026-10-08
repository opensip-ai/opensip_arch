from pathlib import Path
P=Path('/tmp/opensip-implementation/o1b-authoring-r1/product');p=P/'crates/operability/src/kinds/registry.rs';s=p.read_text();s=s.replace('use super::{Code, Counts, Errno, Flag, Form, PrivacyClass, ProcessId, SafeField, Version};','use super::{Code, Counts, Elapsed, Errno, Flag, Form, PrivacyClass, ProcessId, SafeField, Version};');key='const _: () = assert!(PHASE_PARENT.len() == Phase::TEXT.len());';assert key in s;s=s.replace(key,key+'''

impl Phase {
    pub const fn parent(self) -> Option<Self> {
        PHASE_PARENT[self as usize]
    }
}

// Exact M3-O1 item14 vocabulary; no free-form outcome is admitted.
code_table!(PhaseOutcome, cap 32, {
    Completed => "completed",
    Failed => "failed",
    Cancelled => "cancelled",
    NotApplicable => "not-applicable",
});
''',1)
append='''
// O1-b ordinary phase registrations. The parent is derived from the selected
// closed Phase table, so no constructor accepts an arbitrary parent.
pub struct HostPhaseStarted {
    phase: Code<Phase>,
    parent: Option<Code<Phase>>,
    at: Elapsed,
}
impl event_seal::Sealed for HostPhaseStarted {}
impl Event for HostPhaseStarted {
    const NAME: &'static str = "host.phase.started";
    const LEVEL: Level = Level::Info;
    const TEMPLATE: &'static str = "phase started";
    const EXPORT: bool = false;
    const REQUIRES: IdentitySet = IdentitySet::Request;
    const FIELD_COUNT: usize = 3;
    const MAX_LINE: usize = HEADER_RESERVE
        + 5 + 4 + <Code<Phase> as SafeField>::MAX_VALUE
        + 6 + 4 + <Code<Phase> as SafeField>::MAX_VALUE
        + 2 + 4 + <Elapsed as SafeField>::MAX_VALUE;
    const FIELD_CLASSES: &'static [PrivacyClass] = &[PrivacyClass::P0; 3];
    const FIELD_KEYS: &'static [&'static str] = &["phase", "parent", "at"];
    const FIELD_KINDS: &'static [&'static str] = &["Code<Phase>", "Code<Phase>", "Elapsed"];
    const FIELD_BOUNDS: &'static [usize] = &[<Code<Phase> as SafeField>::MAX_VALUE, <Code<Phase> as SafeField>::MAX_VALUE, <Elapsed as SafeField>::MAX_VALUE];
    const FIELD_PRIVACY: &'static [(&'static str, PrivacyClass)] = &[("phase",PrivacyClass::P0),("parent",PrivacyClass::P0),("at",PrivacyClass::P0)];
    const FIELD_OPTIONAL: &'static [bool] = &[false,true,false];
}
impl HostPhaseStarted {
    pub fn new(phase: Phase, at: Elapsed) -> Self {
        Self { phase: Code::from_enum(phase), parent: phase.parent().map(Code::from_enum), at }
    }
    pub(crate) fn projected_truncated(&self, _ceiling: PrivacyClass) -> usize { 0 }
    pub(crate) fn project_fields(&self, _ceiling: PrivacyClass, out: &mut Vec<u8>) -> usize {
        out.extend_from_slice(b"{\\\"phase\\\":");
        self.phase.encode(Form::Json,out);
        if let Some(parent)=self.parent {
            out.extend_from_slice(b",\\\"parent\\\":");
            parent.encode(Form::Json,out);
        }
        out.extend_from_slice(b",\\\"at\\\":");
        self.at.encode(Form::Json,out);
        out.push(b'}');
        0
    }
    pub(crate) fn project_fields_human(&self, _ceiling: PrivacyClass, out: &mut Vec<u8>) -> usize {
        out.extend_from_slice(b" phase=");
        self.phase.encode(Form::Human,out);
        if let Some(parent)=self.parent {
            out.extend_from_slice(b" parent=");
            parent.encode(Form::Human,out);
        }
        out.extend_from_slice(b" at=");
        self.at.encode(Form::Human,out);
        0
    }
}
const _: () = {
    assert!(event_name_ok(HostPhaseStarted::NAME));
    assert!(template_ok(HostPhaseStarted::TEMPLATE));
    assert!(HostPhaseStarted::MAX_LINE<=MAX_LINE);
    assert!(HostPhaseStarted::FIELD_COUNT<=MAX_FIELDS);
};

event! {
    struct HostPhaseCompleted;
    name: "host.phase.completed";
    level: Level::Info;
    requires: IdentitySet::Request;
    export: true;
    template: "phase completed";
    fields: {
        phase P0: Code<Phase>,
        wall P0: Elapsed,
        cpu P0: Elapsed,
        outcome P0: Code<PhaseOutcome>,
        at P0: Elapsed,
    }
}

#[cfg(test)]
mod phase_registration_tests {
    use super::*;
    #[test]
    fn the_started_parent_is_absent_only_for_the_selected_root() {
        let mut root=Vec::new();
        let omitted=HostPhaseStarted::new(Phase::Request,Elapsed::new(0)).project_fields(PrivacyClass::P0,&mut root);
        assert_eq!(omitted,0);
        assert_eq!(root,b"{\\\"phase\\\":\\\"request\\\",\\\"at\\\":0}");
        let mut delivery=Vec::new();
        let omitted=HostPhaseStarted::new(Phase::Delivery,Elapsed::new(42)).project_fields(PrivacyClass::P0,&mut delivery);
        assert_eq!(omitted,0);
        assert_eq!(delivery,b"{\\\"phase\\\":\\\"delivery\\\",\\\"parent\\\":\\\"request\\\",\\\"at\\\":42}");
        for phase in [Phase::ProviderStart,Phase::ProviderAnalysis,Phase::ProviderTeardown] {
            assert_eq!(phase.parent(),Some(Phase::Provider));
        }
        assert_eq!(PhaseOutcome::TEXT,&["completed","failed","cancelled","not-applicable"]);
    }
}
'''
s+=append;p.write_text(s)
p=P/'crates/operability/src/emit.rs';s=p.read_text().replace('Event, HostRepairCompleted, LogStreamOpened,','Event, HostPhaseCompleted, HostPhaseStarted, HostRepairCompleted, LogStreamOpened,');marker='impl EmitOn<CommittedRunScope> for StorageCommitPublished {';assert marker in s;s=s.replace(marker,'''macro_rules! phase_on {
    ($event:ident, $slot:expr) => {
        impl EmitOn<RequestScope> for $event {
            fn emit(self, scope: RequestScope) {
                submit(Self::NAME, Self::LEVEL, Self::TEMPLATE, $slot, scope.identities(), Projection {
                    max_line: Self::MAX_LINE,
                    privacy: Self::FIELD_PRIVACY,
                    fields: |ceiling,out: &mut Vec<u8>| self.project_fields(ceiling,out),
                    human: |ceiling,out: &mut Vec<u8>| self.project_fields_human(ceiling,out),
                    truncated: |ceiling| self.projected_truncated(ceiling),
                });
            }
        }
    };
}
phase_on!(HostPhaseStarted,5);
phase_on!(HostPhaseCompleted,6);

'''+marker,1);p.write_text(s)
p=P/'crates/operability/src/lib.rs';s=p.read_text().replace('BuildProfile, CodeEnum, CommitNotPublished, CounterTable, Event, HostRepairCompleted,','BuildProfile, CodeEnum, CommitNotPublished, CounterTable, Event, HostPhaseCompleted, HostPhaseStarted, HostRepairCompleted,').replace('IdentitySet, IoErrorKind, LogStreamOpened, LossCell, Phase, Platform, RepairKind,','IdentitySet, IoErrorKind, LogStreamOpened, LossCell, Phase, PhaseOutcome, Platform, RepairKind,');p.write_text(s)
print('isolated O1-b phase registrations and emission prepared')
