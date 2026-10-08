from pathlib import Path
P=Path('/tmp/opensip-implementation/o1b-authoring-r1/product')
for rel in ['src/lib.rs','src/constants.rs','src/writer.rs','src/marker.rs']:
 p=P/'crates/operability'/rel;s=p.read_text().replace('any(test, feature = "operability-dev-sinks")','any(test, feature = "operability-dev-sinks", feature = "harness-instrumentation")');p.write_text(s)
for rel in ['src/queue.rs','src/marker.rs']:
 p=P/'crates/operability'/rel;s=p.read_text().replace('#[cfg(feature = "operability-dev-sinks")]','#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]');p.write_text(s)
p=P/'crates/operability/src/lib.rs';s=p.read_text().replace('mod dev_writer;','mod dev_writer;\n#[cfg(feature = "harness-instrumentation")]\nmod harness_writer;',1);p.write_text(s)
p=P/'crates/operability/src/kinds/registry.rs';s=p.read_text().replace('    Stderr => "stderr",','    Stderr => "stderr",\n    Harness => "harness",',1);p.write_text(s)
p=P/'crates/operability/src/readback.rs';s=p.read_text().replace('("stderr", "harness"),','("stderr", "unknown-sink"),',1);p.write_text(s)
s=(P/'crates/operability/src/dev_writer.rs').read_text();s=s[:s.index('\n#[cfg(test)]\nmod tests {')];s=s.replace('Development-only descriptor owner.','Harness-only JSON descriptor owner.').replace('DevSink','HarnessSink').replace('opensip-operability-stderr','opensip-operability-harness').replace('crate::emit::encode_loss_marker(','crate::emit::encode_harness_loss_marker(')
s=s.replace('        fd: std::os::fd::OwnedFd,','        output: std::fs::File,',1).replace('        Self::start_output(std::fs::File::from(fd), enqueue, drops, in_flight)','        std::hint::black_box(b"opensip.operability.harness-sink");\n        Self::start_output(output, enqueue, drops, in_flight)',1)
s=s.replace('    host_invariant: AtomicBool,','    host_invariant: AtomicBool,\n    opening: AtomicBool,\n    opened: AtomicBool,',1).replace('            host_invariant: AtomicBool::new(false),','            host_invariant: AtomicBool::new(false),\n            opening: AtomicBool::new(false),\n            opened: AtomicBool::new(false),',1)
s=s.replace('    pub(crate) fn reserve(&self, max_line: usize, level: Level) -> Option<Reservation> {\n        self.queue.reserve(max_line, level)\n    }','''    pub(crate) fn begin_opening(&self) -> bool {
        self.opening.compare_exchange(false,true,Ordering::AcqRel,Ordering::Acquire).is_ok()
    }
    pub(crate) fn reserve_opening(&self, max_line: usize) -> Option<Reservation> {
        self.queue.reserve(max_line,Level::Info)
    }
    pub(crate) fn opened(&self) -> bool { self.opened.load(Ordering::Acquire) }
    pub(crate) fn finish_opening(&self) { self.opened.store(true,Ordering::Release); }
    pub(crate) fn reserve(&self, max_line: usize, level: Level) -> Option<Reservation> {
        if !self.opened() { return None; }
        self.queue.reserve(max_line, level)
    }''',1)
s+='\n#[cfg(test)]\n#[path = "harness_writer_tests.rs"]\nmod tests;\n';(P/'crates/operability/src/harness_writer.rs').write_text(s)
p=P/'crates/operability/src/harness_writer_tests.rs';p.write_text('''use super::*;
use crate::guard::ProjectionForm;
use crate::kinds::PrivacyClass;
use crate::kinds::registry::HostRepairCompleted;
use std::io::Read;
use std::os::unix::net::UnixStream;

#[test]
fn the_harness_worker_uses_json_and_its_own_frozen_marker() {
    // Writer control only: actual descriptor admission is a fresh-child C13 leg.
    let (output,mut input)=UnixStream::pair().unwrap();
    input.set_read_timeout(Some(Duration::from_secs(2))).unwrap();
    let enqueue=Arc::new(AtomicBool::new(true));
    let sink=HarnessSink::start_output(output,Arc::clone(&enqueue),Arc::new(std::array::from_fn(|_|AtomicU64::new(0))),Arc::new(AtomicU64::new(0))).unwrap();
    assert!(!sink.opened());
    assert!(sink.reserve(HostRepairCompleted::MAX_LINE,Level::Info).is_none());
    assert!(sink.begin_opening());
    assert!(!sink.begin_opening());
    let record=SealedRecord::from_encoder(b"{\\\"ts\\\":\\\"2023-11-14T22:13:20.000Z\\\",\\\"level\\\":\\\"info\\\",\\\"event\\\":\\\"host.repair.completed\\\",\\\"requestId\\\":\\\"req1_21212121212121212121212121212121\\\",\\\"fields\\\":{\\\"kind\\\":\\\"registration\\\",\\\"state\\\":\\\"RW-T3\\\"}}\\n".to_vec(),ProjectionForm::Json,HostRepairCompleted::FIELD_PRIVACY).unwrap();
    let expected=record.bytes().to_vec();
    let reservation=sink.reserve_opening(HostRepairCompleted::MAX_LINE).unwrap();
    sink.source_increment(RequestId::minted([0x21;16]),Level::Info);
    sink.push(record,reservation,Level::Info);
    sink.finish_opening();
    let deadline=Instant::now()+Duration::from_secs(1);
    sink.begin_finalize(deadline);
    while !sink.settled()&&Instant::now()<deadline { std::thread::yield_now(); }
    sink.gate.store(false,Ordering::Release);
    enqueue.store(false,Ordering::Release);
    let snapshot=sink.cell.load();
    assert_eq!(snapshot.written[2],1);
    assert_eq!(snapshot.first_error,None);
    assert_eq!(sink.marker.freeze(),crate::marker::MarkerOutcome::Written);
    let mut bytes=Vec::new();input.read_to_end(&mut bytes).unwrap();
    assert!(bytes.starts_with(&expected));
    let admitted=crate::readmit(&bytes,PrivacyClass::P1);
    assert_eq!(admitted.lines.len(),2);
    assert_eq!(admitted.records.malformed,0);
    let marker=std::str::from_utf8(&admitted.lines[1]).unwrap();
    assert!(marker.contains("\\\"sink\\\":\\\"harness\\\""));
    assert!(!marker.contains("stderr"));
}
''')
p=P/'crates/operability/src/emit.rs';s=p.read_text();s=s.replace('#[cfg(feature = "operability-dev-sinks")]\nuse crate::kinds::registry::{LogLossCounted, Sink};','#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]\nuse crate::kinds::registry::{LogLossCounted, Sink};',1)
a=s.index('fn encode_line(');brace=s.index('{\n',a);z=s.index('\nfn push_text(',brace);signature=s[a:brace];body=s[brace+2:z];assert body.startswith('    let mut out = Vec::with_capacity(256);\n');body=body.replace('    let mut out = Vec::with_capacity(256);\n','    out.clear();\n',1)
wrapper=signature+'{\n    encode_line_into(stamp,name,level,ids,ceiling,fields,truncated,Vec::with_capacity(256))\n}\n\n';inner=signature.replace('fn encode_line(','fn encode_line_into(',1).replace('    truncated: usize,','    truncated: usize,\n    mut out: Vec<u8>,',1);s=s[:a]+wrapper+inner+'{\n'+body+s[z:]
s+='''
#[cfg(feature = "harness-instrumentation")]
pub(crate) fn encode_harness_opened(scope: RequestScope, pid: crate::kinds::ProcessId) -> Option<crate::guard::SealedRecord> {
    use crate::kinds::{Code,Version};
    use crate::kinds::registry::{BuildProfile,Platform};
    let event=LogStreamOpened::new(Version::RELEASE,Code::from_enum(Platform::compiled()?),Code::from_enum(BuildProfile::compiled()),Code::from_enum(Sink::Harness),pid);
    let clock=observe_clock().ok()?;
    let stamp=format_timestamp(clock.wall_unix_seconds(),clock.wall_nanoseconds())?;
    let bytes=encode_line(&stamp,LogStreamOpened::NAME,LogStreamOpened::LEVEL,&scope.identities(),PrivacyClass::P1,&|ceiling,out|event.project_fields(ceiling,out),0)?;
    crate::guard::SealedRecord::from_encoder(bytes,crate::guard::ProjectionForm::Json,LogStreamOpened::FIELD_PRIVACY).ok()
}

#[cfg(feature = "harness-instrumentation")]
pub(crate) fn encode_harness_loss_marker(request: crate::scope::RequestId, counts: [u64;40], error: Option<crate::writer::CapturedError>, slot: Vec<u8>) -> Option<crate::guard::SealedRecord> {
    let ids=Identities { request, request_text:request.text(),project:None,plan:None,execution:None,run:None };
    let event=LogLossCounted::from_snapshot(Sink::Harness,counts,error);
    let clock=observe_clock().ok()?;
    let stamp=format_timestamp(clock.wall_unix_seconds(),clock.wall_nanoseconds())?;
    let bytes=encode_line_into(&stamp,LogLossCounted::NAME,LogLossCounted::LEVEL,&ids,PrivacyClass::P1,&|ceiling,out|event.project_fields(ceiling,out),0,slot)?;
    crate::guard::SealedRecord::from_encoder(bytes,crate::guard::ProjectionForm::Json,LogLossCounted::FIELD_PRIVACY).ok()
}
''';p.write_text(s)
print('isolated harness descriptor worker, startup gate and P0/P1 encoders prepared')
