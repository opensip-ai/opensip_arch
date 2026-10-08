#![forbid(unsafe_code)]
fn main() {
    use opensip_host::{Format, MetadataHost, MetadataRequest};
    use opensip_operability::{Code, EmitOn, HostRepairCompleted, RepairKind, RepairState};
    let mut host=MetadataHost::new();
    let context=host.begin().unwrap();
    let scope=host.logging_scope(&context).expect("own reservation after start");
    let execution=opensip_platform::reserve_execution_id().unwrap();
    let _typed=opensip_operability::ExecutionId::from(&execution);
    let _request=opensip_operability::RequestScope::from(&opensip_platform::RequestIdentity::draw().unwrap());
    let mut foreign=MetadataHost::new();
    let foreign_context=foreign.begin().unwrap();
    assert!(host.logging_scope(&foreign_context).is_none());
    assert!(foreign.logging_scope(&context).is_none());
    assert!(foreign.logging_scope(&foreign_context).is_none());
    HostRepairCompleted::new(Code::from_enum(RepairKind::Registration),Code::from_enum(RepairState::RwR1)).emit(scope);
    let rendered=host.execute(&context,MetadataRequest::Help{topic:None},Format::Json,None,"test").unwrap();
    assert_eq!(rendered.exit_code,0);
    assert!(opensip_operability::frozen_summary().is_some());
    use std::io::Write;
    std::io::stdout().write_all(&rendered.bytes).unwrap();
}
