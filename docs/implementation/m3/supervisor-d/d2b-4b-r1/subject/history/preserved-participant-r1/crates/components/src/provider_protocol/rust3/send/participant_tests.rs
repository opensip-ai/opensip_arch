//! Bounded fake pipes and custody over inert synthetic Plan projections.
//! These test protocol composition, not spawn, C4 admission or qualification.
use super::super::super::super::{
    FRAME_PREFIX_BYTES, ProcessFault,
    cbor::{self, Value},
    write_frame,
};
use super::super::super::{Rust3DispatchContext, receive::tests as worker};
use super::super::schedule::Entry;
use super::*;
use opensip_identity::{digest_hex, raw_sha256};
use std::{cell::Cell, rc::Rc};
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn u(v: u64) -> Value {
    Value::Unsigned(v)
}
fn map(v: Vec<(&str, Value)>) -> Value {
    Value::Map(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn get<'a>(v: &'a Value, k: &str) -> &'a Value {
    let Value::Map(v) = v else { panic!() };
    v.iter().find(|(key, _)| key == k).map(|(_, v)| v).unwrap()
}
fn replace(v: &mut Value, k: &str, new: Value) {
    let Value::Map(v) = v else { panic!() };
    v.iter_mut().find(|(key, _)| key == k).unwrap().1 = new;
}
fn commitment(domain: &str, v: &Value) -> String {
    let mut raw = domain.as_bytes().to_vec();
    raw.push(0);
    raw.extend(cbor::encode(v));
    format!("sha256:{}", digest_hex(&raw_sha256(&raw)))
}
struct Custody {
    reads: Rc<Cell<usize>>,
    fail: bool,
}
impl Source for Custody {
    fn read(&mut self, entry: &Entry, _offset: u64, length: usize) -> io::Result<Vec<u8>> {
        self.reads.set(self.reads.get() + 1);
        if self.fail {
            return Err(io::Error::other("custody unavailable"));
        }
        let byte = match entry {
            Entry::Snapshot(path) if path == "src/a.rs" => 0x11,
            Entry::Dependency { package_key, path }
                if package_key == "a 1 source with spaces" && path == "src/lib.rs" =>
            {
                0x22
            }
            Entry::Prepared(0) => 0x33,
            _ => return Err(io::Error::other("unexpected custody identity")),
        };
        Ok(vec![byte; length])
    }
}
fn participant<'t>(
    table: &'t Table,
    prep: bool,
) -> (Rust3Participant<'t>, Rc<Cell<usize>>, Rust3DispatchContext) {
    let request = super::super::sender::tests::request(prep);
    let c = request.context.clone();
    let reads = Rc::new(Cell::new(0));
    let source = Custody {
        reads: reads.clone(),
        fail: false,
    };
    (
        Rust3Participant::new(table, request, Box::new(source)).unwrap(),
        reads,
        c,
    )
}
struct Reader {
    bytes: io::Cursor<Vec<u8>>,
    calls: usize,
}
impl Read for Reader {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        self.bytes.read(buf)
    }
}
fn wire(name: &str, payload: Value, sequence: u64) -> Vec<u8> {
    write_frame(&map(vec![
        ("protocolMajor", u(3)),
        ("direction", t("worker-to-host")),
        ("sequence", u(sequence)),
        ("frameType", t(name)),
        ("payload", payload),
    ]))
    .unwrap()
}
fn feed(p: &mut Rust3Participant<'_>, name: &str, payload: Value, sequence: u64) -> Vec<u8> {
    let bytes = wire(name, payload, sequence);
    let mut reader = Reader {
        bytes: io::Cursor::new(bytes.clone()),
        calls: 0,
    };
    let step = p.readable(&mut reader);
    assert_eq!(reader.calls, 1);
    assert!(
        !matches!(
            step.status,
            ParticipantStatus::Fault | ParticipantStatus::HostFault
        ),
        "{name}: {:?}",
        step.status
    );
    bytes
}
struct Writer {
    bytes: Vec<u8>,
    calls: usize,
    maximum: usize,
}
impl Write for Writer {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        self.calls += 1;
        let n = bytes.len().min(self.maximum);
        self.bytes.extend_from_slice(&bytes[..n]);
        Ok(n)
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}
fn flush(p: &mut Rust3Participant<'_>) {
    let mut writer = Writer {
        bytes: Vec::new(),
        calls: 0,
        maximum: usize::MAX,
    };
    while p.wants_write() {
        let before = writer.calls;
        let step = p.writable(&mut writer);
        assert_eq!(writer.calls, before + 1);
        assert!(
            !matches!(
                step.status,
                ParticipantStatus::Fault | ParticipantStatus::HostFault
            ),
            "{:?}",
            step.status
        );
    }
}
fn analyzing(p: &mut Rust3Participant<'_>, c: &Rust3DispatchContext, reads: &Cell<usize>) -> u64 {
    assert_eq!(reads.get(), 0);
    flush(p);
    feed(p, "HelloAck", worker::ack(c), 0);
    assert_eq!(reads.get(), 0);
    flush(p);
    feed(p, "UniverseAccepted", worker::accepted(c), 1);
    assert_eq!(reads.get(), 0);
    flush(p);
    assert_eq!(reads.get(), 2);
    feed(p, "SnapshotAccepted", c.snapshot_seal.clone(), 2);
    flush(p);
    assert_eq!(reads.get(), 3);
    feed(p, "DependencySourceAccepted", c.dependency_seal.clone(), 3);
    let mut seq = 4;
    if let Some(seal) = &c.prepared_seal {
        flush(p);
        assert_eq!(reads.get(), 5);
        feed(p, "PreparedOutputAccepted", seal.clone(), seq);
        seq += 1;
    }
    feed(p, "NativeContextVerified", worker::native(c), seq);
    flush(p);
    assert_eq!(p.phase(), "ANALYZING");
    seq + 1
}
fn candidate(c: &Rust3DispatchContext) -> Value {
    let domain = &c.stages[0].analysis_domain;
    let Value::Array(keys) = get(domain, "requestedCoverageDomain") else {
        panic!()
    };
    let key = &keys[0];
    let (sha, _) = c.manifest_files.get("src/a.rs").unwrap();
    map(vec![
        ("candidateOrdinal", u(0)),
        ("relation", t("declares")),
        ("resolution", t("syntactic")),
        ("layer", t("syntax")),
        ("producer", t("rust-semantic")),
        ("producerVersion", t("provider")),
        ("schemaVersion", u(1)),
        ("language", t("rust")),
        ("sourceUniverseId", get(key, "sourceUniverseId").clone()),
        ("targetUniverseId", get(key, "targetUniverseId").clone()),
        ("confidenceMillionths", u(1_000_000)),
        ("relationSchemaId", t("opensip.relation.declares.v1")),
        (
            "canonicalRelationPayload",
            Value::Bytes(cbor::encode(&map(vec![("symbol", t("fixture"))]))),
        ),
        (
            "anchors",
            Value::Array(vec![map(vec![
                ("kind", t("source-span")),
                ("snapshotId", get(&c.open_universe, "snapshotId").clone()),
                ("path", t("src/a.rs")),
                ("contentSha256", t(sha)),
                ("startByte", u(0)),
                ("endByte", u(1)),
                ("factId", Value::Null),
            ])]),
        ),
    ])
}
fn coverage_entries(c: &Rust3DispatchContext, state: &str, deficiency: Value) -> Value {
    let Value::Array(keys) = get(&c.stages[0].analysis_domain, "requestedCoverageDomain") else {
        panic!()
    };
    Value::Array(
        keys.iter()
            .map(|key| worker::requested_entry(key, state, deficiency.clone()))
            .collect(),
    )
}
fn complete(p: &mut Rust3Participant<'_>, c: &Rust3DispatchContext, seq: u64) -> Vec<Vec<u8>> {
    let stage = get(&c.stages[0].plan_stage, "stageId").clone();
    let facts = Value::Array(vec![candidate(c)]);
    let entries = coverage_entries(c, "complete", Value::Null);
    let batch = map(vec![
        ("analysisOrdinal", u(c.analysis_ordinal)),
        ("stageId", stage.clone()),
        ("batchIndex", u(0)),
        ("candidates", facts.clone()),
    ]);
    let batch = feed(p, "FactBatch", batch, seq);
    let coverage = map(vec![
        ("analysisOrdinal", u(c.analysis_ordinal)),
        ("stageId", stage.clone()),
        ("entries", entries.clone()),
        (
            "coverageCommitment",
            t(&commitment(
                "opensip.rust-provider.stage-coverage.v2",
                &entries,
            )),
        ),
    ]);
    let coverage = feed(p, "CoverageV3", coverage, seq + 1);
    let result = map(vec![
        ("stageId", stage),
        ("factCount", u(1)),
        ("coverageEntryCount", u(1)),
        (
            "factCommitment",
            t(&commitment("opensip.rust-provider.stage-facts.v2", &facts)),
        ),
        (
            "coverageCommitment",
            t(&commitment(
                "opensip.rust-provider.stage-coverage.v2",
                &entries,
            )),
        ),
    ]);
    let terminal = map(vec![
        ("analysisOrdinal", u(c.analysis_ordinal)),
        ("stageResults", Value::Array(vec![result])),
        (
            "factStreamCommitment",
            t(&commitment("opensip.rust-provider.fact-stream.v2", &facts)),
        ),
        (
            "coverageStreamCommitment",
            t(&commitment(
                "opensip.rust-provider.coverage-stream.v2",
                &entries,
            )),
        ),
    ]);
    let terminal = feed(p, "Complete", terminal, seq + 2);
    vec![batch, coverage, terminal]
}

#[test]
fn participant_complete_moves_original_raw_candidates_only_after_zero_exit_and_eof() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for prep in [false, true] {
        let (mut p, reads, c) = participant(&table, prep);
        let seq = analyzing(&mut p, &c, &reads);
        let raw = complete(&mut p, &c, seq);
        assert!(p.take_terminal_output().is_none());
        let pointers = worker::original_buffer_addresses(&p.receiver);
        assert_eq!(pointers.len(), 3);
        assert_eq!(
            p.process(ProcessEvent::ZeroExit).status,
            ParticipantStatus::Terminal(TerminalKind::Complete)
        );
        assert!(p.take_terminal_output().is_none());
        let eof = p.readable(&mut io::empty());
        assert!(eof.eof);
        assert!(p.take_terminal_output().is_none());
        assert_eq!(p.process(ProcessEvent::Eof).status, ParticipantStatus::Done);
        let output = p.take_terminal_output().unwrap();
        assert_eq!(output.kind(), TerminalKind::Complete);
        let candidates = output.into_spool().into_candidates();
        assert_eq!(
            candidates
                .iter()
                .map(|v| (v.as_ptr() as usize, v.len()))
                .collect::<Vec<_>>(),
            pointers
        );
        assert_eq!(
            candidates,
            raw.iter()
                .map(|v| v[FRAME_PREFIX_BYTES..].to_vec())
                .collect::<Vec<_>>()
        );
        assert!(p.take_terminal_output().is_none());
    }
}

#[test]
fn participant_cancel_finishes_partial_hello_then_one_exact_cancel_without_source_read() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let (mut p, reads, _) = participant(&table, false);
    assert_eq!(p.protocol(), Protocol::Rust3);
    assert_eq!(
        p.protocol_waits().stage1_cancel_grace,
        Duration::from_secs(5)
    );
    assert_eq!(p.protocol_waits().normal_exit_grace, Duration::from_secs(5));
    let mut writer = Writer {
        bytes: Vec::new(),
        calls: 0,
        maximum: 5,
    };
    p.writable(&mut writer);
    assert_eq!(writer.calls, 1);
    assert!(p.cancel());
    assert!(!p.cancel());
    let mut cancelled = false;
    while p.wants_write() {
        let before = writer.calls;
        let step = p.writable(&mut writer);
        assert_eq!(writer.calls, before + 1);
        if step.cancel.written {
            assert!(step.cancel.request_closed);
            cancelled = true;
        }
    }
    assert!(cancelled);
    assert!(p.closed);
    assert_eq!(reads.get(), 0);
    let mut raw = writer.bytes.as_slice();
    let mut names = Vec::new();
    while let Some(frame) = super::super::super::super::read_frame(
        &mut raw,
        Profile::Rust3,
        RUST3_FRAME_MAX_DEPTH,
        None,
    )
    .unwrap()
    {
        let value = frame.value();
        names.push(get(value, "frameType").clone());
        if get(value, "frameType") == &t("Cancel") {
            assert_eq!(get(value, "sequence"), &u(1));
            assert_eq!(get(get(value, "payload"), "executionId"), &Value::Null);
            assert_eq!(get(get(value, "payload"), "analysisOrdinal"), &Value::Null);
        }
    }
    assert_eq!(names, [t("Hello"), t("Cancel")]);
    assert!(!p.cancel());
}

#[test]
fn participant_prefix_frame_count_and_payload_limits_precede_payload_allocation() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let (mut p, _, c) = participant(&table, false);
    flush(&mut p);
    p.remaining_frames = 1;
    let ack = wire("HelloAck", worker::ack(&c), 0);
    let mut first = ack[..1].as_ref();
    p.readable(&mut first);
    assert_eq!(p.remaining_frames, 0);
    let mut rest = ack[1..].as_ref();
    assert!(!matches!(
        p.readable(&mut rest).status,
        ParticipantStatus::Fault
    ));
    assert_eq!(p.receiver.totals().frames, 1);
    let prefix = 67_108_864_u64.to_be_bytes();
    let step = p.readable(&mut prefix.as_slice());
    assert_eq!(step.status, ParticipantStatus::Fault);
    assert!(p.accumulator.at_boundary());
    assert!(p.accumulator.payload.is_none());
    assert_eq!(p.receiver.totals().frames, 1);
    let (mut p, _, _) = participant(&table, false);
    p.accumulator = FrameAccumulator::new(Profile::Rust3, RUST3_FRAME_MAX_DEPTH, Some(0));
    let step = p.readable(&mut 1_u64.to_be_bytes().as_slice());
    assert_eq!(step.status, ParticipantStatus::Fault);
    assert!(p.accumulator.payload.is_none());
    assert_eq!(p.receiver.totals().frames, 0);
}

#[test]
fn participant_distinguishes_host_pipe_custody_and_provider_protocol_faults() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let (mut p, reads, c) = participant(&table, false);
    flush(&mut p);
    let mut bad = worker::ack(&c);
    replace(&mut bad, "providerBuildId", t("wrong"));
    let bytes = wire("HelloAck", bad, 0);
    assert_eq!(
        p.readable(&mut bytes.as_slice()).status,
        ParticipantStatus::Fault
    );
    assert_eq!(reads.get(), 0);
    assert!(p.take_terminal_output().is_none());
    struct Broken;
    impl Write for Broken {
        fn write(&mut self, _: &[u8]) -> io::Result<usize> {
            Err(io::Error::new(io::ErrorKind::BrokenPipe, "fake"))
        }
        fn flush(&mut self) -> io::Result<()> {
            Ok(())
        }
    }
    let (mut p, _, _) = participant(&table, false);
    assert_eq!(p.writable(&mut Broken).status, ParticipantStatus::HostFault);
    assert!(!p.wants_write());
    let (mut p, _, _) = participant(&table, false);
    let mut zero = Writer {
        bytes: Vec::new(),
        calls: 0,
        maximum: 0,
    };
    assert_eq!(p.writable(&mut zero).status, ParticipantStatus::HostFault);
    let (mut p, _, _) = participant(&table, false);
    p.readable(&mut [1_u8, 2].as_slice());
    assert_eq!(
        p.readable(&mut io::empty()).status,
        ParticipantStatus::Fault
    );
    let (mut p, reads, c) = participant(&table, false);
    p.source = Box::new(Custody {
        reads: reads.clone(),
        fail: true,
    });
    flush(&mut p);
    feed(&mut p, "HelloAck", worker::ack(&c), 0);
    flush(&mut p);
    feed(&mut p, "UniverseAccepted", worker::accepted(&c), 1);
    let mut sink = io::sink();
    assert_eq!(p.writable(&mut sink).status, ParticipantStatus::HostFault);
    assert_eq!(reads.get(), 1);
    assert!(p.take_terminal_output().is_none());
}
