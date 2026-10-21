from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');D=W/'crates/operability/src'
p=D/'kinds/registry.rs';s=p.read_text();assert 'enum RevocationElapsed' not in s
s+='''
// D3b plan r3 LD-D3B-9/10; SL S6:492-494, listed in full.
code_table!(RevocationMark, cap 64, {
    RequestsRefused => "requests-refused",
    ProtocolCancel => "protocol-cancel",
    Sigterm => "sigterm",
    KillAndReap => "kill-and-reap",
    ScratchCleanup => "scratch-cleanup",
});
code_table!(ElapsedStatus, cap 64, {
    Measured => "measured",
    LowerBound => "lower-bound",
    Unavailable => "unavailable",
});
/// The only shapes accepted by the revocation-miss builders. A duration
/// cannot accompany unavailable or be omitted from a measured/lower bound.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RevocationElapsed {
    Measured(Elapsed),
    LowerBound(Elapsed),
    Unavailable,
}
impl RevocationElapsed {
    fn fields(self) -> (Code<ElapsedStatus>, Option<Elapsed>) {
        match self {
            Self::Measured(d) => (Code::from_enum(ElapsedStatus::Measured), Some(d)),
            Self::LowerBound(d) => (Code::from_enum(ElapsedStatus::LowerBound), Some(d)),
            Self::Unavailable => (Code::from_enum(ElapsedStatus::Unavailable), None),
        }
    }
}
supervision_event! {
    struct SupervisionRevocationMissed;
    name: "supervision.revocation.missed";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "revocation mark not shown within bound";
    constructor: pub(crate) fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        mark P0 req: Code<RevocationMark>,
        elapsed_status P0 req: Code<ElapsedStatus>,
        // Present exactly for measured/lower-bound; absent for unavailable.
        elapsed P0 opt: Elapsed,
        bound P0 req: Elapsed,
    }
}
impl SupervisionRevocationMissed {
    pub fn of(role: Code<ProviderRole>, universe: Universe, mark: Code<RevocationMark>,
              measurement: RevocationElapsed, bound: Elapsed) -> Self {
        let (status, elapsed) = measurement.fields();
        Self::new(role, universe, mark, status, elapsed, bound)
    }
}
supervision_event! {
    struct ToolRevocationMissed;
    name: "tool.revocation.missed";
    level: Level::Warn;
    requires: IdentitySet::Project;
    export: false;
    template: "revocation mark not shown within bound";
    constructor: pub(crate) fields: {
        mark P0 req: Code<RevocationMark>,
        elapsed_status P0 req: Code<ElapsedStatus>,
        // Present exactly for measured/lower-bound; absent for unavailable.
        elapsed P0 opt: Elapsed,
        bound P0 req: Elapsed,
    }
}
impl ToolRevocationMissed {
    pub fn of(mark: Code<RevocationMark>, measurement: RevocationElapsed, bound: Elapsed) -> Self {
        let (status, elapsed) = measurement.fields();
        Self::new(mark, status, elapsed, bound)
    }
}
''';p.write_text(s)
p=D/'lib.rs';s=p.read_text();s+='''
// D3b-2's S6 mark and measurement vocabulary and two scope-specific events.
pub use kinds::registry::{ElapsedStatus, RevocationElapsed, RevocationMark,
    SupervisionRevocationMissed, ToolRevocationMissed};
''';p.write_text(s)
p=D/'emit.rs';s=p.read_text();s='use crate::kinds::registry::{SupervisionRevocationMissed, ToolRevocationMissed};\n'+s if not s.startswith('//!') else s.replace('use opensip_platform::observe_clock;', 'use crate::kinds::registry::{SupervisionRevocationMissed, ToolRevocationMissed};\nuse opensip_platform::observe_clock;');a='''    ToolTreeSwept on ProjectScope => 33,''';assert s.count(a)==1;s=s.replace(a,a+'''
    SupervisionRevocationMissed on PlanAttemptScope => 34,
    ToolRevocationMissed on ProjectScope => 35,''');p.write_text(s)
p=D/'transport.rs';s=p.read_text().replace('const BUDGET_EVENTS: usize = 34;', 'const BUDGET_EVENTS: usize = 36;').replace('''/// `emit.rs`'s `registered_on!`).''','''/// `emit.rs`'s `registered_on!`), plus D3b-2's two revocation events34/35.''');p.write_text(s)
p=D/'readback.rs';s=p.read_text();a='use super::kinds::{CODE_MAX,';assert s.count(a)==1;s=s.replace(a,'use super::kinds::registry::{RevocationMark, ElapsedStatus, SupervisionRevocationMissed, ToolRevocationMissed};\n'+a);a='''        _ if name == SupervisionCancelSent::NAME =>''';assert s.count(a)==1;s=s.replace(a,'''        _ if name == SupervisionRevocationMissed::NAME => registered_desc!(SupervisionRevocationMissed,
            [ROLE, UNIVERSE, Code(RevocationMark::TEXT), Code(ElapsedStatus::TEXT), Unsigned, Unsigned]),
        _ if name == ToolRevocationMissed::NAME => registered_desc!(ToolRevocationMissed,
            [Code(RevocationMark::TEXT), Code(ElapsedStatus::TEXT), Unsigned, Unsigned]),
'''+a);p.write_text(s)
p=D/'kinds/registry_tests.rs';s=p.read_text();s=s.replace('use super::ToolTreeSwept;', 'use super::{ToolTreeSwept, RevocationMark, ElapsedStatus, SupervisionRevocationMissed, ToolRevocationMissed, RevocationElapsed};');s=s.replace('''        table!(ForceTrigger, "registry-literal"),''','''        table!(ForceTrigger, "registry-literal"),
        table!(RevocationMark, "registry-literal"),
        table!(ElapsedStatus, "registry-literal"),''');s=s.replace('''            $push::<ToolTreeSwept>,''','''            $push::<ToolTreeSwept>,
            $push::<SupervisionRevocationMissed>,
            $push::<ToolRevocationMissed>,''');s=s.replace('''        descriptor::<ToolTreeSwept>(),''','''        descriptor::<ToolTreeSwept>(),
        descriptor::<SupervisionRevocationMissed>(),
        descriptor::<ToolRevocationMissed>(),''');# Append independently transcribed inventory rows at inventory's end only.
a='''    ]
}

/// S-OP-2 item 23's provider''';assert s.count(a)==1;s=s.replace(a,'''        (
            "supervision.revocation.missed", Level::Warn, IdentitySet::ProjectPlanExecution, false,
            vec![("role", "Code<ProviderRole>", "P0", "req"), ("universe", "Universe", "P1", "req"),
                 ("mark", "Code<RevocationMark>", "P0", "req"), ("elapsed_status", "Code<ElapsedStatus>", "P0", "req"),
                 ("elapsed", "Elapsed", "P0", "opt"), ("bound", "Elapsed", "P0", "req")],
        ),
        (
            "tool.revocation.missed", Level::Warn, IdentitySet::Project, false,
            vec![("mark", "Code<RevocationMark>", "P0", "req"), ("elapsed_status", "Code<ElapsedStatus>", "P0", "req"),
                 ("elapsed", "Elapsed", "P0", "opt"), ("bound", "Elapsed", "P0", "req")],
        ),
'''+a);s+='''
#[test]
fn d3b2_revocation_measurement_shapes_have_exact_conditional_elapsed() {
    use super::super::Elapsed;
    assert_eq!(RevocationMark::TEXT, ["requests-refused", "protocol-cancel", "sigterm", "kill-and-reap", "scratch-cleanup"]);
    assert_eq!(ElapsedStatus::TEXT, ["measured", "lower-bound", "unavailable"]);
    for (measurement, wanted, duration) in [
        (RevocationElapsed::Measured(Elapsed::new(7)), ElapsedStatus::Measured, Some(Elapsed::new(7))),
        (RevocationElapsed::LowerBound(Elapsed::new(3)), ElapsedStatus::LowerBound, Some(Elapsed::new(3))),
        (RevocationElapsed::Unavailable, ElapsedStatus::Unavailable, None),
    ] {
        let (status, elapsed) = measurement.fields();
        assert_eq!(status, Code::from_enum(wanted)); assert_eq!(elapsed, duration);
        let tool = ToolRevocationMissed::of(Code::from_enum(RevocationMark::ScratchCleanup), measurement, Elapsed::new(10));
        assert_eq!(tool.elapsed_status, status); assert_eq!(tool.elapsed, duration);
    }
}
''';p.write_text(s)
print('Two revocation events, two tables and typed measurement builders added; not yet verified')
