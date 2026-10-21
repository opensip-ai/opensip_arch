from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/src/launch_recheck.rs');s=p.read_text();old='''        for (member, kind) in required.into_iter().flatten() {
            let index = find(bindings, member.name, work)?.ok_or(
                FactoryRefusal::SpecInconsistent("launch-binding-not-selected"),
            )?;
''';assert s.count(old)==1;s=s.replace(old,'''        for (role, (member, kind)) in required.into_iter().flatten().enumerate() {
            let index = find(bindings, member.name, work)?.ok_or(
                FactoryRefusal::SpecInconsistent("launch-binding-not-selected"),
            )?;
            if role == 0 {
                // The selected CMS entrypoint is the owner's operation,
                // not a caller-labelled File request (even when its bytes
                // happen to match). This check precedes every native read.
                check(work, "launch-binding-entrypoint", || {
                    matches!(bindings[index].request, MemberRequest::Entrypoint)
                })?;
            }
''',1);p.write_text(s)
p=Path('crates/host/src/launch_recheck_tests.rs');s=p.read_text();a=s.index('    let fixture = Fixture::new();',s.index('fn actual_native_factory_preserves_corruption_and_read_io_routes'));# setup is indented8 not4 due loop: find next fixture open
b=s.index('        fixture.opened',a);setup=s[a:b];setup=setup.replace('let bindings = bindings();','let mut bindings = bindings();')
s+='''
#[test]
fn actual_native_factory_requires_cms_entrypoint_operation_before_reads() {
    for request in [MemberRequest::File("provider"),MemberRequest::File("entrypoint"),MemberRequest::Directory("")] {
'''+setup+'''
        bindings.iter_mut().find(|row|row.name=="entrypoint").unwrap().request=request;
        fixture.opened(|trees|{
            let guard=read_fixture::fail_next_read();
            let result=WorkLedger::snapshot_profile().scope(|work|{
                prepare_session(SessionInput{selection:selection.clone(),provider:codec,launch:launch(&provider,&root),memory_budget_bytes:1<<30},trees,&bindings,&authority,work).map_err(WorkFailure::Operation)
            });
            assert!(matches!(result,Err(WorkFailure::Operation(FactoryRefusal::SpecInconsistent("launch-binding-entrypoint")))));
            assert!(!guard.was_triggered(),"generic-file substitution must fail before any physical read");
            assert!(!fixture.root.join("peer-observation.json").exists());
        });
    }
}
''';p.write_text(s)
print('Entry role must use actual CMS Entrypoint operation; generic same-file/alias/directory requests refuse before reads.')
