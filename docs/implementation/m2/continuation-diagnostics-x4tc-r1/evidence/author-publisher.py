from pathlib import Path
b=Path('/tmp/opensip-implementation/x4tc-authoring');c=b/'product';p=Path('/Users/sb/code/opensip-ai/opensip')
def edit(rel,old,new,count=1):
 f=c/rel;s=f.read_text();assert s.count(old)==count,(rel,old,s.count(old));f.write_text(s.replace(old,new))
rel='crates/security/src/trust/current_trust_admission.rs'
edit(rel,'/// (the interim lead decision for the index and component reasons).\n    Continuation(String),','/// and the existing clocked-expiry/revoked-closure continuation details.\n    Continuation(String),\n    /// X4T-c: stored index-role standing refuses with its registered detail.\n    IndexContinuation(String),\n    /// X4T-c: stored component-role standing refuses with its registered detail.\n    ComponentContinuation(String),')
edit(rel,'Self::Continuation(_) => "CONTINUE-CORE-NOT-TRUSTED",','Self::Continuation(_) => "CONTINUE-CORE-NOT-TRUSTED",\n            Self::IndexContinuation(_) => "CONTINUE-INDEX-NOT-TRUSTED",\n            Self::ComponentContinuation(_) => "CONTINUE-COMPONENT-NOT-TRUSTED",')
edit(rel,'Self::Continuation(s) | Self::Root(_, s) => Some(s.clone()),','Self::Continuation(s) | Self::IndexContinuation(s) | Self::ComponentContinuation(s) | Self::Root(_, s) => Some(s.clone()),')
edit(rel,'TrustRow::Continuation(format!("index:{}", token(index)))','TrustRow::IndexContinuation(format!("index:{}", token(index)))')
edit(rel,'TrustRow::Continuation(format!("component:{}", token(component)))','TrustRow::ComponentContinuation(format!("component:{}", token(component)))')
needle='/// Item 6 (unit X4-F1): a reread\'s expiry and staleness applied to the'
helper='''/// X4T r12 keeps a clocked-expiry refusal on the existing core detail.
/// The stored-state join alone selects X4T-c's role-specific public details.
fn clocked_standing_of(roles: &[(State, bool); 6]) -> Result<TrustStanding, TrustRefusal> {
    standing_of(roles).map_err(|mut refusal| {
        refusal.row = match refusal.row {
            TrustRow::IndexContinuation(subject) | TrustRow::ComponentContinuation(subject) => TrustRow::Continuation(subject),
            row => row,
        };
        refusal
    })
}

'''
edit(rel,needle,helper+needle)
edit(rel,'(roles, standing_of(&roles)?, None)','(roles, clocked_standing_of(&roles)?, None)')
edit(rel,'let standing = match standing_of(&roles) {','let standing = match clocked_standing_of(&roles) {')
rel='crates/security/src/trust/live_observation.rs'
edit(rel,'TrustRow::Continuation(_) => Err(ObservationFailure::Standing(cause)),','TrustRow::Continuation(_) | TrustRow::IndexContinuation(_) | TrustRow::ComponentContinuation(_) => Err(ObservationFailure::Standing(cause)),')
rel='crates/security/src/installation_termination.rs'
edit(rel,'/// with a subject naming the role and its state or the revoked component.\n    TrustContinuation { subject: String },','/// with a subject naming the role and its state or the revoked component.\n    TrustContinuation { subject: String },\n    /// X4T-c: registered index-role continuation detail; class and subject unchanged.\n    TrustIndexContinuation { subject: String },\n    /// X4T-c: registered component-role continuation detail; class and subject unchanged.\n    TrustComponentContinuation { subject: String },')
rel='crates/security/src/custody/operation_guard.rs'
old='TrustRow::Continuation(subject) => T::TrustContinuation {\n            subject: subject.clone(),\n        },'
new=old+'\n        TrustRow::IndexContinuation(subject) => T::TrustIndexContinuation { subject: subject.to_owned() },\n        TrustRow::ComponentContinuation(subject) => T::TrustComponentContinuation { subject: subject.to_owned() },'
edit(rel,old,new)
rel='crates/host/src/installation_termination.rs'
edit(rel,'Row::TrustContinuation { subject } => admission(Detail::ContinueCoreNotTrusted, subject),','Row::TrustContinuation { subject } => admission(Detail::ContinueCoreNotTrusted, subject),\n        Row::TrustIndexContinuation { subject } => admission(Detail::ContinueIndexNotTrusted, subject),\n        Row::TrustComponentContinuation { subject } => admission(Detail::ContinueComponentNotTrusted, subject),')
# Preserve existing legacy row controls. Appended controls test the new typed routes.
f=c/rel;s=f.read_text();idx=s.rfind('\n}')
s=s[:idx]+'''
    #[test]
    fn role_specific_continuation_details_preserve_the_d9_route() {
        for (row, detail, subject) in [
            (Row::TrustIndexContinuation { subject: "index:revoked".into() }, "CONTINUE-INDEX-NOT-TRUSTED", "index:revoked"),
            (Row::TrustComponentContinuation { subject: "component:unbootstrapped".into() }, "CONTINUE-COMPONENT-NOT-TRUSTED", "component:unbootstrapped"),
        ] {
            let t = installation_termination(&row);
            assert_eq!(t.class, Class::RequestRejected); assert_eq!(t.exit, 2);
            assert_eq!(t.error_code, Code::ExtensionAdmissionRejected);
            assert_eq!(t.fault_cause, Fault::None);
            assert_eq!(t.detail.unwrap().to_string(), detail);
            assert_eq!(t.subject.as_deref(), Some(subject));
        }
    }
'''+s[idx:];f.write_text(s)
rel='crates/host/src/schema_sources.rs'
edit(rel,'"WORK.BUDGET_EXHAUSTED",\n        ] {','"WORK.BUDGET_EXHAUSTED",\n            "CONTINUE-INDEX-NOT-TRUSTED",\n            "CONTINUE-COMPONENT-NOT-TRUSTED",\n        ] {')
# Change only the two old stored-state role-join controls to role-specific expectations.
rel='crates/security/src/trust/current_trust_admission_tests.rs';f=c/rel;s=f.read_text()
a=s.index('fn recovery_goes_through_the_role_machine_join()');z=s.index('\n#[test]',a);block=s[a:z]
block=block.replace('assert_eq!(refusal.row, TrustRow::Continuation(subject.into()));\n        assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");','let expected = role_specific_row(subject);\n        assert_eq!(refusal.row, expected);\n        assert_eq!(refusal.row.code(), expected.code());');s=s[:a]+block+s[z:]
a=s.index('fn each_continuation_refusal_names_its_role_and_state()');z=s.index('\n#[test]',a);block=s[a:z]
block=block.replace('assert_eq!(refusal.row, TrustRow::Continuation(subject.into()), "{subject}");\n        // The interim lead decision: one registered detail, the role in the subject.\n        assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");','let expected = role_specific_row(subject);\n        assert_eq!(refusal.row, expected, "{subject}");\n        assert_eq!(refusal.row.code(), expected.code());');s=s[:a]+block+s[z:]
s+='''
fn role_specific_row(subject: &str) -> TrustRow {
    match subject.split_once(':').unwrap().0 {
        "core" => TrustRow::Continuation(subject.into()),
        "index" => TrustRow::IndexContinuation(subject.into()),
        "component" => TrustRow::ComponentContinuation(subject.into()),
        _ => panic!("explicit test role"),
    }
}
#[test]
fn clocked_join_preserves_core_detail_and_exact_subject() {
    for (position, subject) in [(3, "index:recovery"), (1, "component:recovery")] {
        let mut roles = [(State::Trusted, true); 6]; roles[position] = (State::Recovery, true);
        let stored = standing_of(&roles).unwrap_err();
        let clocked = clocked_standing_of(&roles).unwrap_err();
        assert_eq!(stored.row, role_specific_row(subject));
        assert_eq!(clocked.row, TrustRow::Continuation(subject.into()));
        assert_eq!(clocked.row.code(), "CONTINUE-CORE-NOT-TRUSTED");
        assert_eq!(clocked.cause, stored.cause);
    }
}
''';f.write_text(s)
print('typed stored-role publisher and D9 controls authored in candidate only')

rel='crates/security/src/trust/trust_bootstrap_tests.rs';s=(p/rel).read_text();assert s.count('TrustRow::Continuation("index:revoked".into())')==1;assert s.count('TrustRow::Continuation("component:unbootstrapped".into())')==2
(c/rel).write_text(s.replace('TrustRow::Continuation("index:revoked".into())','TrustRow::IndexContinuation("index:revoked".into())').replace('TrustRow::Continuation("component:unbootstrapped".into())','TrustRow::ComponentContinuation("component:unbootstrapped".into())'))
