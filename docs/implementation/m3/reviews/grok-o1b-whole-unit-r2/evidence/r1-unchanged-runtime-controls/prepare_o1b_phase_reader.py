from pathlib import Path
P=Path('/tmp/opensip-implementation/o1b-authoring-r1/product');p=P/'crates/operability/src/emit.rs';s=p.read_text().replace('impl emission_seal::Sealed for HostRepairCompleted {}','impl emission_seal::Sealed for HostRepairCompleted {}\nimpl emission_seal::Sealed for HostPhaseStarted {}\nimpl emission_seal::Sealed for HostPhaseCompleted {}',1);p.write_text(s)
p=P/'crates/operability/src/readback.rs';s=p.read_text().replace('BuildProfile, CodeEnum, CommitNotPublished, Event, HostRepairCompleted, IdentitySet,','BuildProfile, CodeEnum, CommitNotPublished, Event, HostPhaseCompleted, HostPhaseStarted, HostRepairCompleted, IdentitySet,').replace('LogStreamOpened, PathAnchor, Phase, Platform, RepairKind,','LogStreamOpened, PathAnchor, Phase, PhaseOutcome, Platform, RepairKind,');s=s.replace('enum FieldKind {','enum FieldKind {\n    Phase,\n    PhaseOutcome,',1)
fields=[('PHASE_STARTED_FIELDS',[('phase','Phase',66),('parent','Phase',66),('at','Unsigned',20)]),('PHASE_COMPLETED_FIELDS',[('phase','Phase',66),('wall','Unsigned',20),('cpu','Unsigned',20),('outcome','PhaseOutcome',66),('at','Unsigned',20)])];rows=''
for name,items in fields:
 rows+=f'const {name}: [FieldDesc; {len(items)}] = [\n'+''.join(f'    FieldDesc {{ key: "{key}", class: PrivacyClass::P0, kind: FieldKind::{kind}, max_value: {bound} }},\n'for key,kind,bound in items)+'];\n'
s=s.replace('fn descriptor(name: &str) -> Option<Desc> {',rows+'\nfn descriptor(name: &str) -> Option<Desc> {',1)
s=s.replace('    if name == LogLossCounted::NAME {','''    if name == HostPhaseStarted::NAME {
        Some(Desc { name: HostPhaseStarted::NAME, level: HostPhaseStarted::LEVEL, requires: HostPhaseStarted::REQUIRES, max_line: HostPhaseStarted::MAX_LINE, fields: &PHASE_STARTED_FIELDS, privacy: HostPhaseStarted::FIELD_PRIVACY })
    } else if name == HostPhaseCompleted::NAME {
        Some(Desc { name: HostPhaseCompleted::NAME, level: HostPhaseCompleted::LEVEL, requires: HostPhaseCompleted::REQUIRES, max_line: HostPhaseCompleted::MAX_LINE, fields: &PHASE_COMPLETED_FIELDS, privacy: HostPhaseCompleted::FIELD_PRIVACY })
    } else if name == LogLossCounted::NAME {''',1)
s=s.replace('        FieldKind::Platform =>','        FieldKind::Phase => push_member(Phase::TEXT, value, &mut out)?,\n        FieldKind::PhaseOutcome => push_member(PhaseOutcome::TEXT, value, &mut out)?,\n        FieldKind::Platform =>',1)
tests='''
    #[test]
    fn phase_registrations_read_only_the_selected_fields_and_vocabulary() {
        use crate::kinds::{Code,Elapsed};
        use crate::kinds::registry::{HostPhaseStarted,HostPhaseCompleted,Phase,PhaseOutcome};
        let mut started=b"{\\\"ts\\\":\\\"2023-11-14T22:13:20.000Z\\\",\\\"level\\\":\\\"info\\\",\\\"event\\\":\\\"host.phase.started\\\",\\\"requestId\\\":\\\"req1_abababababababababababababababab\\\",\\\"fields\\\":".to_vec();
        HostPhaseStarted::new(Phase::Delivery,Elapsed::new(17)).project_fields(PrivacyClass::P0,&mut started);
        started.extend_from_slice(b"}\\n");
        let mut completed=b"{\\\"ts\\\":\\\"2023-11-14T22:13:20.000Z\\\",\\\"level\\\":\\\"info\\\",\\\"event\\\":\\\"host.phase.completed\\\",\\\"requestId\\\":\\\"req1_abababababababababababababababab\\\",\\\"fields\\\":".to_vec();
        HostPhaseCompleted::new(Code::from_enum(Phase::Delivery),Elapsed::new(6),Elapsed::new(3),Code::from_enum(PhaseOutcome::Completed),Elapsed::new(23)).project_fields(PrivacyClass::P0,&mut completed);
        completed.extend_from_slice(b"}\\n");
        for line in [&started,&completed] {
            let admitted=readmit(line,PrivacyClass::P0);
            assert_eq!(admitted.lines,vec![line.clone()]);
            assert_eq!(admitted.fields.invalid_value,0);
        }
        let bad=std::str::from_utf8(&completed).unwrap().replace("completed\\\",\\\"at","invented-outcome\\\",\\\"at");
        let admitted=readmit(bad.as_bytes(),PrivacyClass::P0);
        assert_eq!(admitted.lines.len(),1);
        assert_eq!(admitted.fields.invalid_value,1);
        assert!(!contains(&admitted.lines[0],b"invented-outcome"));
    }
'''
s=s.replace('    #[test]\n    fn loss_writer_readback_preserves_optional_error_pair_and_rejects_lone_errno()',tests+'\n    #[test]\n    fn loss_writer_readback_preserves_optional_error_pair_and_rejects_lone_errno()',1);p.write_text(s)
print('O1-b phase reader registration and controls prepared')
