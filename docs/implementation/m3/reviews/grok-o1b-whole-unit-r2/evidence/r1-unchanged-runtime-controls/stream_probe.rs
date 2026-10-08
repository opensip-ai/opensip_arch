use opensip_host::{MetadataHost,MetadataRequest,Format};
use opensip_operability::{HostRepairCompleted,RepairKind,RepairState,Code,EmitOn,PrivacyClass};
use std::io::Write;
fn main() {
    let mode=std::env::args().nth(1).unwrap();
    if mode=="reader" {
        let path=std::env::args().nth(2).unwrap();
        let ceiling=if std::env::args().nth(3).unwrap()=="P0" {PrivacyClass::P0} else {PrivacyClass::P1};
        let raw=std::fs::read(path).unwrap();
        let view=opensip_operability::readmit(&raw,ceiling);
        for line in view.lines { std::io::stdout().write_all(&line).unwrap(); }
        eprintln!("DROPS:{:?}",view.records);
        return;
    }
    if mode=="cancel-stall" {
        use opensip_operability::{RequestScope,RequestSpan,PhaseOutcome};
        let identity=opensip_platform::RequestIdentity::draw().unwrap();
        let scope=RequestScope::from(&identity);
        assert!(opensip_operability::start_for_request(scope).unwrap().is_ok());
        let root=RequestSpan::begin(scope).unwrap();
        for _ in 0..2048 { HostRepairCompleted::new(Code::from_enum(RepairKind::Registration),Code::from_enum(RepairState::RwT3)).emit(scope); }
        root.finish(PhaseOutcome::Cancelled).unwrap();
        let started=std::time::Instant::now();opensip_operability::finalize(true);
        let elapsed=started.elapsed().as_nanos();let summary=opensip_operability::frozen_summary().unwrap();
        opensip_operability::finalize(false);assert_eq!(Some(summary),opensip_operability::frozen_summary());
        println!("{{\"cancelled\":true,\"admitted\":{},\"written\":{:?},\"failed\":{:?},\"abandoned\":{:?},\"stopped\":{:?},\"hasError\":{},\"drops\":{:?},\"freezeNanoseconds\":{}}}",summary.harness_admitted,summary.harness_written,summary.harness_failed,summary.harness_abandoned,summary.harness_stopped,summary.harness_error.is_some(),summary.drops,elapsed);
        return;
    }
    if mode=="phase-api" {
        use opensip_operability::{RequestScope,RequestSpan,Phase,PhaseOutcome};
        let identity=opensip_platform::RequestIdentity::draw().unwrap();
        let scope=RequestScope::from(&identity);
        assert!(opensip_operability::start_for_request(scope).unwrap().is_ok());
        let root=RequestSpan::begin(scope).unwrap();
        let delivery=root.start(Phase::Delivery).unwrap();
        std::thread::sleep(std::time::Duration::from_millis(2));
        delivery.finish(PhaseOutcome::Failed).unwrap();
        root.not_applicable(Phase::Reuse).unwrap();
        root.finish(PhaseOutcome::Cancelled).unwrap();
        opensip_operability::finalize(true);
        assert!(opensip_operability::frozen_summary().unwrap().harness_admitted);
        println!("{{\"phaseApi\":true}}");
        return;
    }
    let mut host=MetadataHost::new();let request=host.begin().unwrap();
    if mode=="inheritance" {
        let child=std::process::Command::new("/bin/sh").args(["-c","if [ -e /dev/fd/3 ]; then exit 71; fi"]).status().unwrap();
        assert!(child.success(),"descriptor 3 leaked to child");
    }
    if mode=="stall" || mode=="closed-reader" {
        let scope=host.logging_scope(&request).unwrap();
        for _ in 0..2048 {
            HostRepairCompleted::new(Code::from_enum(RepairKind::Registration),Code::from_enum(RepairState::RwT3)).emit(scope);
        }
    }
    let started=std::time::Instant::now();
    let response=host.execute(&request,MetadataRequest::Version,Format::Json,None,"0.1.0").unwrap();
    let elapsed=started.elapsed().as_nanos();
    let summary=opensip_operability::frozen_summary().unwrap();
    opensip_operability::finalize(false);assert_eq!(Some(summary),opensip_operability::frozen_summary());
    std::thread::sleep(std::time::Duration::from_millis(20));
    assert_eq!(Some(summary),opensip_operability::frozen_summary());
    println!("{{\"response\":{},\"admitted\":{},\"written\":{:?},\"failed\":{:?},\"abandoned\":{:?},\"stopped\":{:?},\"hasError\":{},\"drops\":{:?},\"freezeNanoseconds\":{}}}",String::from_utf8(response.bytes).unwrap(),summary.harness_admitted,summary.harness_written,summary.harness_failed,summary.harness_abandoned,summary.harness_stopped,summary.harness_error.is_some(),summary.drops,elapsed);
}
