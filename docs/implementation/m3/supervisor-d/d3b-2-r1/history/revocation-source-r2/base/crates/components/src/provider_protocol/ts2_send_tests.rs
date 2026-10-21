// Unit D2b-3b's controls (section 4's RF-2 builder and sender controls, for
// TS2):
// - the host payload builders and their closed checks, before spawn;
// - the canonical send schedule and its bounds through the route;
// - the sender's exact slot consumption, every divergence refused before
//   writing, and LD-D2B-7's Cancel law;
// - the table's gate on host frames;
// - the participant D3a drives, from Hello to DONE.
// The worker frames are D2b-3a's fixtures.
use super::*;
use crate::provider_protocol::{FrameAccumulator, built_commitment, read_frame, write_frame};
use crate::supervisor::{
    Boundary, Participant, ParticipantStatus, Progress, ProtocolWaits, TerminalKind,
};
use opensip_identity::{digest_hex as hex, hash_canonical_value};
use std::io;

const MIB: u64 = 1_048_576;

fn universe() -> J {
    parse_json(
        format!(
            r#"{{"schemaVersion":1,"manifestId":"{h1}","capabilityManifestId":"{h2}",
            "runtimeArtifactId":"typescript-runtime","runtimeArtifactSha256":"{h3}",
            "providerArtifactId":"typescript-provider","providerArtifactSha256":"{h4}",
            "runtimeDescriptorSha256":"{h4}","providerDescriptorSha256":"{h3}","protocolMajor":2,
            "providerBuildId":"{BUILD}","nodeVersion":"24.16.0","v8Version":"13.6","modulesAbi":"137",
            "typescriptVersion":"5.9.2","typescriptCompilerSha256":"{h1}","typescriptStdlibMerkleRoot":"{h2}",
            "platformId":"darwin-arm64","resolvedInputs":{{"schemaVersion":2,"languageMode":"ts-tsconfig",
            "configOrigin":"tsconfig","synthesizerVersion":null,"synthesizedOptions":null,
            "packageModuleType":"module","allowJs":false,"checkJs":false,"jsAdmittedToProgram":false,
            "jsDiagnosticsEnabled":false,"resolutionCompletenessImplied":false,"jsRootFiles":[],
            "programRootFiles":["src/a.ts"],"lockfileKind":"none","nodeModulesInReadSet":false,
            "executionCapableResolution":false,"tsconfigGraphHash":"{h2}","nativeContextId":"{s9}"}}}}"#,
            h1 = h('1'),
            h2 = h('2'),
            h3 = h('3'),
            h4 = h('4'),
            s9 = sha('9'),
        )
        .as_bytes(),
    )
    .unwrap()
}

/// Each file's content: deterministic bytes, distinct per path.
fn content(path: &str, length: u64) -> Vec<u8> {
    let salt = path.bytes().fold(0u8, |s, b| s.wrapping_add(b));
    (0..length).map(|i| (i % 251) as u8 ^ salt).collect()
}
fn file(path: &str, length: u64) -> SnapshotEntry {
    SnapshotEntry::File {
        path: path.to_owned(),
        byte_length: length,
        content_sha256: hex(&raw_sha256(&content(path, length))),
    }
}
/// DLV `budgetProjection.absent.output`: the signed default profile.
fn default_budget() -> BTreeMap<String, u64> {
    BTreeMap::from_iter(
        [
            ("sourceFilesVisited", 200_000u64),
            ("astNodesVisited", 50_000_000),
            ("moduleResolutionQueries", 1_000_000),
            ("typeQueries", 5_000_000),
            ("factsEmitted", 1_000_000),
            ("factBytesEmitted", 1_073_741_824),
        ]
        .map(|(k, v)| (k.to_owned(), v)),
    )
}
fn plan() -> Ts2Plan {
    let key = |c: char| RequestedKey {
        relation: "calls".to_owned(),
        resolution: "syntactic-callee-name".to_owned(),
        source_universe_id: sha('5'),
        target_universe_id: sha('6'),
        subject_scope_commitment: sha(c),
    };
    Ts2Plan {
        host_build_id: "opensip-host 1.0.0".to_owned(),
        expected_provider_descriptor_sha256: h('3'),
        expected_runtime_descriptor_sha256: h('4'),
        capabilities: TOKENS.iter().map(|s| (*s).to_owned()).collect(),
        provider_build_id: BUILD.to_owned(),
        execution_id: EXEC.to_owned(),
        snapshot_id: format!("snapshot2:{}", h('7')),
        plan_id: format!("plan2:{}", h('8')),
        plan_intent_commitment: sha('e'),
        universe: universe(),
        entries: vec![
            file("src/a.ts", 2 * MIB + 5),
            file("src/b.ts", 0),
            SnapshotEntry::Symlink {
                path: "src/c.ts".to_owned(),
                link_target: "a.ts".to_owned(),
            },
            file("src/d.ts", 100),
        ],
        stages: vec![
            StagePlan {
                stage_id: "stage-one".to_owned(),
                depends_on: None,
                relations: vec!["calls".to_owned()],
                budget: StageBudget::Absent,
                keys: vec![key('c')],
            },
            StagePlan {
                stage_id: "stage-two".to_owned(),
                depends_on: Some(vec!["stage-one".to_owned()]),
                relations: vec!["calls".to_owned()],
                budget: StageBudget::WorkUnits(7),
                keys: vec![key('d')],
            },
        ],
        default_budget: default_budget(),
    }
}
fn build(p: &Ts2Plan) -> Ts2Request {
    Ts2Request::build(p).unwrap()
}
fn invariant(p: &Ts2Plan, what: &str) -> String {
    match Ts2Request::build(p) {
        Err(PlanRefusal::HostInvariant(why)) => why,
        other => panic!("{what}: not a host invariant: {other:?}"),
    }
}

/// The sealed snapshot, in memory.
struct Memory {
    files: BTreeMap<String, Vec<u8>>,
    /// Replace the bytes read at (path, offset), keeping their length.
    corrupt: Option<(String, u64)>,
    fail: bool,
    /// Fail the read at (path, offset) once, then read normally again.
    fail_once: Option<(String, u64)>,
    reads: usize,
}
impl Memory {
    fn of(p: &Ts2Plan) -> Self {
        Self {
            files: p
                .entries
                .iter()
                .filter_map(|e| match e {
                    SnapshotEntry::File {
                        path, byte_length, ..
                    } => Some((path.clone(), content(path, *byte_length))),
                    SnapshotEntry::Symlink { .. } => None,
                })
                .collect(),
            corrupt: None,
            fail: false,
            fail_once: None,
            reads: 0,
        }
    }
}
impl SnapshotSource for Memory {
    fn read(&mut self, path: &str, offset: u64, length: usize) -> std::io::Result<Vec<u8>> {
        self.reads += 1;
        if self.fail {
            return Err(std::io::Error::other("the sealed snapshot is unreadable"));
        }
        if self.fail_once.as_ref() == Some(&(path.to_owned(), offset)) {
            self.fail_once = None;
            return Err(std::io::Error::other("a transient read failure"));
        }
        let bytes = &self.files[path];
        let at = offset as usize;
        let mut out = bytes[at..(at + length).min(bytes.len())].to_vec();
        if self.corrupt.as_ref() == Some(&(path.to_owned(), offset)) {
            out[0] ^= 1;
        }
        Ok(out)
    }
}

fn handshake() -> J {
    parse_json(include_bytes!(
        "../../../../schemas/sources/handshake-v1.schema.json"
    ))
    .unwrap()
}
/// A schema definition's constants, read here independently of the builder.
fn schema_constants(def: &str) -> Value {
    let doc = handshake();
    let J::Object(props) = path(&doc, &["$defs", def, "properties"]).unwrap() else {
        panic!("{def}")
    };
    Value::Map(
        props
            .iter()
            .map(|(k, v)| match path(v, &["const"]) {
                Some(J::Integer(i)) => (k.clone(), u(u64::try_from(i.get()).unwrap())),
                _ => panic!("{def}.{k}"),
            })
            .collect(),
    )
}
fn same(a: &Value, b: &Value) -> bool {
    cbor::encode(a) == cbor::encode(b)
}
fn stage(r: &Ts2Request, i: usize) -> &Value {
    match get(r.analyze(), "stageRequests") {
        Value::Array(s) => &s[i],
        _ => unreachable!(),
    }
}

// ------------------------------------------------------------------ the builders

/// Hello: the selection's tokens exactly, and the limits and identity
/// versions as handshake-v1 states them (LD-D2B-18's sender half; A2-3's
/// limits control).
#[test]
fn the_hello_is_the_selection_and_the_schema_constants() {
    let p = plan();
    let r = build(&p);
    let hello = r.hello();
    assert!(same(
        get(hello, "limits"),
        &schema_constants("TypeScriptProtocolLimitsV1")
    ));
    assert!(same(
        get(hello, "identityVersions"),
        &schema_constants("IdentityVersionsV1")
    ));
    assert!(same(
        get(hello, "expectedCapabilities"),
        &a(TOKENS.iter().map(|s| t(s)).collect())
    ));
    assert_eq!(get(hello, "expectedProviderDescriptorSha256"), &t(&h('3')));
    // The array is taken exactly, never sorted or repaired.
    for (what, tokens) in [
        (
            "unordered",
            vec![
                "fact-identity-fact2",
                "coverage-v3",
                "plan-identity-plan2",
                "source-identity-snapshot2",
            ],
        ),
        (
            "duplicate",
            vec![
                "coverage-v3",
                "coverage-v3",
                "fact-identity-fact2",
                "plan-identity-plan2",
                "source-identity-snapshot2",
            ],
        ),
        (
            "an identity token missing",
            vec!["coverage-v3", "fact-identity-fact2", "plan-identity-plan2"],
        ),
        (
            "unknown",
            vec![
                "coverage-v3",
                "fact-identity-fact2",
                "made-up-v1",
                "plan-identity-plan2",
                "source-identity-snapshot2",
            ],
        ),
    ] {
        let mut q = plan();
        q.capabilities = tokens.iter().map(|s| (*s).to_owned()).collect();
        invariant(&q, what);
    }
    // An optional token is carried as selected.
    let mut q = plan();
    q.capabilities.push("target-attribution-v2".to_owned());
    q.capabilities.sort();
    assert!(same(
        get(build(&q).hello(), "expectedCapabilities"),
        &a(q.capabilities.iter().map(|s| t(s)).collect())
    ));
    // The census-bearing variant is D2b-3c's.
    let mut q = plan();
    q.capabilities.push("symbol-census-v1".to_owned());
    q.capabilities.sort();
    assert!(invariant(&q, "symbol-census-v1").contains("D2b-3c"));
}

/// OpenUniverse: universeKey is the host's recomputation of the selected
/// universe's identity (UNIVERSE-NATIVE-IDENTITY), and the universe is
/// carried exactly.
#[test]
fn open_universe_recomputes_the_universe_key() {
    let p = plan();
    let r = build(&p);
    let J::Object(u) = &p.universe else {
        panic!("object")
    };
    let want = format!(
        "sha256:{}",
        hex(&hash_canonical_value(
            "native.semantic-universe.typescript.v2",
            &u["resolvedInputs"]
        )
        .unwrap())
    );
    assert_eq!(get(r.open_universe(), "universeKey"), &t(&want));
    assert_eq!(
        carrier::to_json(get(r.open_universe(), "universe")).unwrap(),
        p.universe
    );
    for (m, want) in [("executionId", EXEC), ("providerId", "typescript-semantic")] {
        assert_eq!(get(r.open_universe(), m), &t(want));
    }
    // A universe its schema refuses is a host invariant.
    let mut q = plan();
    let J::Object(mut u) = q.universe.clone() else {
        unreachable!()
    };
    u.insert("protocolMajor".to_owned(), parse_json(b"3").unwrap());
    q.universe = J::Object(u);
    invariant(&q, "protocolMajor 3");
}

/// SnapshotManifest and SnapshotSeal from the sealed inventory
/// (TS2-MANIFEST-DIGEST, TS2-SNAPSHOT-ORDER, TS2-LOGICAL-PATH-ADMISSION,
/// SEAL-AGGREGATES, ECHO-SNAPSHOT2).
#[test]
fn the_manifest_and_seal_are_the_sealed_inventory() {
    let p = plan();
    let r = build(&p);
    let entries = get(r.manifest(), "entries");
    assert_eq!(
        get(r.manifest(), "manifestSha256"),
        &t(&hex(&raw_sha256(&cbor::encode(entries))))
    );
    let Value::Array(e) = entries else {
        unreachable!()
    };
    assert_eq!(get(&e[2], "kind"), &t("symlink"));
    assert_eq!(get(&e[2], "contentSha256"), &Value::Null);
    for (m, want) in [
        ("entryCount", 4),
        ("totalFileBytes", 2 * MIB + 105),
        // a.ts: 3 chunks; b.ts (empty): none; d.ts: 1.
        ("totalChunkCount", 4),
    ] {
        assert_eq!(get(r.seal(), m), &u(want), "{m}");
    }
    for v in [r.manifest(), r.seal()] {
        assert_eq!(get(v, "snapshotId"), &t(&p.snapshot_id));
    }
    for (what, entries) in [
        ("unordered", vec![file("src/b.ts", 1), file("src/a.ts", 1)]),
        ("duplicate", vec![file("src/a.ts", 1), file("src/a.ts", 1)]),
        ("a dot-dot segment", vec![file("src/../a.ts", 1)]),
        ("absolute", vec![file("/src/a.ts", 1)]),
        ("an empty segment", vec![file("src//a.ts", 1)]),
    ] {
        let mut q = plan();
        q.entries = entries;
        invariant(&q, what);
    }
}

/// Analyze (TS2-STAGE-PROJECTION, TS2-BUDGET-PROJECTION,
/// TS2-SUBJECT-SCOPE-RETAINED, TS2-DOMAIN-COMMITMENT, PER-KEY-SCOPE2's
/// placement, DISPATCH-STAGE-CORRELATION's builder side, ECHO-OPEN-UNIVERSE).
#[test]
fn analyze_is_the_plans_projection() {
    let p = plan();
    let r = build(&p);
    let analyze = r.analyze();
    for m in ["executionId", "snapshotId", "planId", "universeKey"] {
        assert_eq!(get(analyze, m), get(r.open_universe(), m), "{m}");
    }
    assert_eq!(get(analyze, "analysisOrdinal"), &u(0));
    // DLV's two stageRequestProjection vectors.
    let s0 = stage(&r, 0);
    assert_eq!(get(s0, "stageOrdinal"), &u(0));
    assert_eq!(get(s0, "dependsOn"), &a(vec![]));
    assert!(same(
        get(s0, "budget"),
        &Value::Map(
            default_budget()
                .into_iter()
                .map(|(k, v)| (k, u(v)))
                .collect()
        )
    ));
    let s1 = stage(&r, 1);
    assert_eq!(get(s1, "stageOrdinal"), &u(1));
    assert_eq!(get(s1, "dependsOn"), &a(vec![t("stage-one")]));
    assert!(same(
        get(s1, "budget"),
        &Value::Map(default_budget().into_keys().map(|k| (k, u(7))).collect())
    ));
    // The subject scope over every file entry, with DLV's domains
    // (DLV:1080-1081) recomputed here.
    let subjects = a(["src/a.ts", "src/b.ts", "src/d.ts"]
        .iter()
        .zip([2 * MIB + 5, 0, 100])
        .map(|(path, n)| {
            m(&[
                ("path", t(path)),
                ("contentSha256", t(&hex(&raw_sha256(&content(path, n))))),
                ("byteLength", u(n)),
            ])
        })
        .collect());
    let domain = get(s0, "requestedCoverageDomain");
    let scope = get(domain, "subjectScope");
    assert_eq!(get(scope, "subjectCount"), &u(3));
    assert_eq!(
        get(scope, "subjectScopeCommitment"),
        &t(&built_commitment(
            "opensip.coverage.subject-scope.v1",
            &subjects
        ))
    );
    let keys = get(domain, "keys");
    assert_eq!(
        get(domain, "domainCommitment"),
        &t(&built_commitment(
            "opensip.ts-provider.requested-coverage-domain.v1",
            &m(&[("subjectScope", scope.clone()), ("keys", keys.clone())])
        ))
    );
    let Value::Array(k) = keys else {
        unreachable!()
    };
    assert_eq!(get(&k[0], "subjectScopeCommitment"), &t(&sha('c')));
    assert_eq!(get(&k[0], "producerVersion"), &t(BUILD));
    // Host invariants, before spawn.
    let mut q = plan();
    let mut k2 = q.stages[0].keys[0].clone();
    k2.target_universe_id = sha('7');
    q.stages[0].keys = vec![k2, q.stages[0].keys[0].clone()];
    invariant(&q, "reject-unordered-requested-domain (DLV)");
    for (what, budget) in [
        ("work-units 0", StageBudget::WorkUnits(0)),
        ("work-units 2^63", StageBudget::WorkUnits(1 << 63)),
    ] {
        let mut q = plan();
        q.stages[1].budget = budget;
        invariant(&q, what);
    }
    let mut q = plan();
    q.default_budget.remove("typeQueries");
    invariant(&q, "a profile without typeQueries");
    let mut q = plan();
    q.stages.clear();
    invariant(&q, "no stage");
}

// ------------------------------------------------------------------ the schedule

/// REQUEST-WIRE-ACCOUNTING: the canonical greedy schedule, each slot its
/// exact envelope payload, the chunk digests over the payload without its
/// bytes, and the reserved maximal Cancel.
#[test]
fn the_schedule_is_canonical() {
    let p = plan();
    let r = build(&p);
    let slots = r.schedule().slots();
    let frames: Vec<&str> = slots.iter().map(|s| s.frame.name()).collect();
    assert_eq!(
        frames,
        [
            "Hello",
            "OpenUniverse",
            "SnapshotManifest",
            "SnapshotFileChunk",
            "SnapshotFileChunk",
            "SnapshotFileChunk",
            "SnapshotFileChunk",
            "SnapshotSeal",
            "Analyze"
        ]
    );
    assert!(
        slots
            .iter()
            .enumerate()
            .all(|(i, s)| s.sequence == i as u64)
    );
    let chunks: Vec<(&str, u64, u64, u64, bool)> = slots
        .iter()
        .filter_map(|s| {
            s.chunk.as_ref().map(|c| {
                (
                    c.path.as_str(),
                    c.chunk_index,
                    c.byte_offset,
                    c.byte_length,
                    s.entry_content_sha256.is_some(),
                )
            })
        })
        .collect();
    assert_eq!(
        chunks,
        [
            ("src/a.ts", 0, 0, MIB, false),
            ("src/a.ts", 1, MIB, MIB, false),
            ("src/a.ts", 2, 2 * MIB, 5, true),
            ("src/d.ts", 0, 0, 100, true),
        ]
    );
    assert_eq!(slots[7].total_chunk_count, Some(4));
    // Every slot's size and digest equal the frame the sender realizes.
    let mut sender = Ts2Sender::new(build(&p));
    let mut source = Memory::of(&p);
    for s in slots {
        let sent = sender.send_next(&mut source).unwrap();
        assert_eq!(
            sent.bytes.len() as u64 - 40,
            s.payload_bytes,
            "slot {}",
            s.sequence
        );
        let envelope = read_frame(
            &mut sent.bytes.as_slice(),
            cbor::Profile::Ts2,
            TS2_FRAME_MAX_DEPTH,
            None,
        )
        .unwrap()
        .unwrap();
        let payload = get(envelope.value(), "payload");
        let digested = if s.chunk.is_some() {
            without(payload, "bytes")
        } else {
            payload.clone()
        };
        assert_eq!(raw_sha256(&cbor::encode(&digested)), s.payload_sha256);
    }
    let cancel = m(&[
        ("executionId", t(EXEC)),
        ("analysisOrdinal", u(0)),
        ("reason", t("user-interrupt")),
    ]);
    let envelope = m(&[
        ("protocolMajor", u(2)),
        ("frameType", t("Cancel")),
        ("sequence", u(slots.len() as u64)),
        ("payload", cancel),
    ]);
    assert_eq!(
        r.schedule().cancel_reserve_bytes(),
        cbor::encode(&envelope).len() as u64
    );
}

/// The entry bound and the frame bound refuse through the carriers' route
/// (REQUEST-WIRE-ACCOUNTING `params.route`); TS2 declares no request totals.
#[test]
fn the_bounds_refuse_through_the_route() {
    let carriers = parse_json(carrier::CARRIERS).unwrap();
    let J::Array(rows) = path(&carriers, &["admission"]).unwrap() else {
        panic!("admission")
    };
    let route = rows
        .iter()
        .find(|r| path(r, &["id"]) == Some(&J::String("REQUEST-WIRE-ACCOUNTING".to_owned())))
        .and_then(|r| path(r, &["params", "route", "routeKey"]))
        .cloned()
        .unwrap();
    assert_eq!(
        route,
        J::String("native.provider-request-exceeds-wire-limit".to_owned())
    );
    let wire = |q: &Ts2Plan| match Ts2Request::build(q) {
        Err(PlanRefusal::ExceedsWireLimit { route, faults }) => (route, faults),
        other => panic!("not a wire-limit refusal: {other:?}"),
    };
    // maxSnapshotEntries + 1 entries.
    let mut q = plan();
    q.entries = (0..200_001u32)
        .map(|i| file(&format!("f/{i:06}"), 0))
        .collect();
    let (r, faults) = wire(&q);
    assert_eq!(r, "native.provider-request-exceeds-wire-limit");
    assert_eq!(faults, ["entries:SnapshotManifest 200001>200000"]);
    // A manifest over maxFramePayloadBytes: 16,500 entries, each a path of
    // 16 segments of 255 scalars (the 4,096-scalar LogicalPath bound).
    let segment: String = std::iter::repeat_n('x', 250).collect();
    let mut q = plan();
    q.entries = (0..16_500u32)
        .map(|i| {
            let name = format!("{segment}{i:05}");
            let path = vec![name.as_str(); 16].join("/");
            file(&path, 0)
        })
        .collect();
    let (r, faults) = wire(&q);
    assert_eq!(r, "native.provider-request-exceeds-wire-limit");
    assert!(
        faults.len() == 1 && faults[0].starts_with("frame:SnapshotManifest seq2:"),
        "{faults:?}"
    );
}

// ------------------------------------------------------------------ the sender

fn sender(p: &Ts2Plan) -> (Ts2Sender, Memory) {
    (Ts2Sender::new(build(p)), Memory::of(p))
}
/// Send planned frames until the next slot is `frame`.
fn until(s: &mut Ts2Sender, source: &mut Memory, frame: SlotFrame) {
    while s.next_slot().unwrap().frame != frame {
        s.send_next(source).unwrap();
    }
}
fn divergence(got: Result<Sent, SendRefusal>, reason: &str) {
    refused("", got, reason);
}
fn refused(what: &str, got: Result<Sent, SendRefusal>, reason: &str) {
    match got {
        Err(SendRefusal::Divergence(d)) => {
            assert!(
                d.starts_with(&format!("SENDER_DIVERGENCE:{reason}")),
                "{what}: {d}"
            )
        }
        other => panic!("{what}: not {reason}: {other:?}"),
    }
}
fn ended(s: &mut Ts2Sender, source: &mut Memory) {
    assert!(s.next_slot().is_none());
    assert_eq!(s.send_next(source).unwrap_err(), SendRefusal::AfterRefusal);
    assert_eq!(s.cancel().unwrap_err(), SendRefusal::AfterRefusal);
}

/// HOST-SEND-SCHEDULE: exactly the planned slots, in order, each with its
/// sequence; the bytes sent are the sealed snapshot's.
#[test]
fn the_sender_emits_exactly_the_schedule() {
    let p = plan();
    let (mut s, mut source) = sender(&p);
    let mut frames = Vec::new();
    let mut bytes: BTreeMap<String, Vec<u8>> = BTreeMap::new();
    while !s.complete() {
        let sent = s.send_next(&mut source).unwrap();
        let f = read_frame(
            &mut sent.bytes.as_slice(),
            cbor::Profile::Ts2,
            TS2_FRAME_MAX_DEPTH,
            None,
        )
        .unwrap()
        .unwrap();
        assert_eq!(get(f.value(), "sequence"), &u(frames.len() as u64));
        if sent.frame == HostFrame::SnapshotFileChunk {
            let payload = get(f.value(), "payload");
            let (Value::Text(path), Value::Bytes(b)) =
                (get(payload, "path"), get(payload, "bytes"))
            else {
                panic!("chunk")
            };
            bytes.entry(path.clone()).or_default().extend_from_slice(b);
        }
        frames.push(sent.frame);
    }
    assert_eq!(frames.len(), 9);
    assert_eq!(frames.last(), Some(&HostFrame::Analyze));
    assert_eq!(bytes["src/a.ts"], content("src/a.ts", 2 * MIB + 5));
    assert_eq!(bytes["src/d.ts"], content("src/d.ts", 100));
    assert!(!bytes.contains_key("src/b.ts"));
    divergence(s.send_next(&mut source), "frame-not-planned");
}

/// Every divergence is refused before the frame is written, and nothing
/// follows it (HOST-SEND-SCHEDULE; section 4's builder and sender controls).
#[test]
fn every_divergence_refuses_before_writing() {
    let p = plan();
    let r = build(&p);
    // The sequence, and a frame out of order.
    let (mut s, mut source) = sender(&p);
    divergence(s.admit(SlotFrame::Hello, 1, r.hello().clone()), "sequence");
    ended(&mut s, &mut source);
    let (mut s, mut source) = sender(&p);
    divergence(
        s.admit(SlotFrame::OpenUniverse, 0, r.open_universe().clone()),
        "frame-type",
    );
    ended(&mut s, &mut source);
    // A changed Hello limits member (A2-3's mutation's control).
    let (mut s, mut source) = sender(&p);
    let limits = with(get(r.hello(), "limits"), "maxStderrBytes", u(262_145));
    divergence(
        s.admit(SlotFrame::Hello, 0, with(r.hello(), "limits", limits)),
        "payload-schema",
    );
    ended(&mut s, &mut source);
    // A same-length substitution of OpenUniverse's executionId.
    let (mut s, mut source) = sender(&p);
    s.send_next(&mut source).unwrap();
    let other = "exec1_0123456789abcdef0123456789abcdee";
    divergence(
        s.admit(
            SlotFrame::OpenUniverse,
            1,
            with(r.open_universe(), "executionId", t(other)),
        ),
        "payload-digest",
    );
    ended(&mut s, &mut source);
    // Analyze: a stageOrdinal taken as the retained ordinal, and a
    // projection that is not the Plan's selected stages.
    let stages = |v: Vec<Value>| with(r.analyze(), "stageRequests", a(v));
    for (what, analyze, reason) in [
        (
            "a retained stageOrdinal",
            stages(vec![
                stage(&r, 0).clone(),
                with(stage(&r, 1), "stageOrdinal", u(5)),
            ]),
            "payload-digest",
        ),
        (
            "a stage dropped",
            stages(vec![stage(&r, 0).clone()]),
            "payload-bytes",
        ),
        (
            "the stages reordered",
            stages(vec![
                with(stage(&r, 1), "stageOrdinal", u(0)),
                with(stage(&r, 0), "stageOrdinal", u(1)),
            ]),
            "payload-digest",
        ),
    ] {
        let (mut s, mut source) = sender(&p);
        until(&mut s, &mut source, SlotFrame::Analyze);
        let seq = s.next_slot().unwrap().sequence;
        refused(what, s.admit(SlotFrame::Analyze, seq, analyze), reason);
        ended(&mut s, &mut source);
    }
    // A different lawful chunking: the first chunk one byte short.
    let (mut s, mut source) = sender(&p);
    until(&mut s, &mut source, SlotFrame::SnapshotFileChunk);
    let chunk = m(&[
        ("snapshotId", t(&p.snapshot_id)),
        ("path", t("src/a.ts")),
        ("chunkIndex", u(0)),
        ("byteOffset", u(0)),
        ("bytes", Value::Bytes(content("src/a.ts", MIB - 1))),
    ]);
    divergence(
        s.admit(SlotFrame::SnapshotFileChunk, 3, chunk),
        "chunk-schedule",
    );
    ended(&mut s, &mut source);
    // Bytes the manifest does not commit: refused at the entry's last chunk.
    let (mut s, mut source) = sender(&p);
    source.corrupt = Some(("src/a.ts".to_owned(), MIB));
    until(&mut s, &mut source, SlotFrame::SnapshotFileChunk);
    s.send_next(&mut source).unwrap();
    s.send_next(&mut source).unwrap();
    divergence(s.send_next(&mut source), "chunk-content");
    ended(&mut s, &mut source);
    // The seal's chunk count.
    let (mut s, mut source) = sender(&p);
    until(&mut s, &mut source, SlotFrame::SnapshotSeal);
    divergence(
        s.admit(
            SlotFrame::SnapshotSeal,
            7,
            with(r.seal(), "totalChunkCount", u(5)),
        ),
        "seal-count",
    );
    ended(&mut s, &mut source);
    // The sealed snapshot cannot supply a chunk.
    let (mut s, mut source) = sender(&p);
    until(&mut s, &mut source, SlotFrame::SnapshotFileChunk);
    source.fail = true;
    assert!(matches!(
        s.send_next(&mut source),
        Err(SendRefusal::Source(_))
    ));
    ended(&mut s, &mut source);
}

/// A snapshot read failure ends the transcript (Codex D2B3B-R1-RF-1): with
/// the source restored, nothing resumes, nothing more is read, and the
/// accepted prefix stays as it was.
#[test]
fn a_snapshot_read_failure_ends_the_transcript() {
    let p = plan();
    let chunk = |offset: u64| {
        m(&[
            ("snapshotId", t(&p.snapshot_id)),
            ("path", t("src/a.ts")),
            ("chunkIndex", u(offset / MIB)),
            ("byteOffset", u(offset)),
            (
                "bytes",
                Value::Bytes(
                    content("src/a.ts", 3 * MIB)[offset as usize..(offset + MIB) as usize].to_vec(),
                ),
            ),
        ])
    };
    let cancel = m(&[
        ("executionId", t(EXEC)),
        ("analysisOrdinal", Value::Null),
        ("reason", t("user-interrupt")),
    ]);
    for (what, offset, direct) in [
        ("the first chunk, by send_next", 0, false),
        ("a later chunk, by send_next", MIB, false),
        ("the first chunk, by realize_next", 0, true),
        ("a later chunk, by realize_next", MIB, true),
    ] {
        let (mut s, mut source) = sender(&p);
        until(&mut s, &mut source, SlotFrame::SnapshotFileChunk);
        if offset > 0 {
            s.send_next(&mut source).unwrap();
        }
        let accepted = s.next_slot().unwrap().sequence;
        source.fail_once = Some(("src/a.ts".to_owned(), offset));
        let failed = if direct {
            s.realize_next(&mut source).map(|_| ()).unwrap_err()
        } else {
            s.send_next(&mut source).map(|_| ()).unwrap_err()
        };
        assert!(
            matches!(failed, SendRefusal::Source(_)),
            "{what}: {failed:?}"
        );
        // The source is restored; every later call refuses without reading.
        assert!(source.fail_once.is_none());
        let reads = source.reads;
        assert!(s.next_slot().is_none(), "{what}");
        assert_eq!(s.cancel_payload(), None, "{what}");
        assert!(!s.complete(), "{what}");
        assert_eq!(
            s.realize_next(&mut source).unwrap_err(),
            SendRefusal::AfterRefusal,
            "{what}"
        );
        assert_eq!(
            s.send_next(&mut source).unwrap_err(),
            SendRefusal::AfterRefusal,
            "{what}"
        );
        assert_eq!(
            s.admit(SlotFrame::SnapshotFileChunk, accepted, chunk(offset))
                .unwrap_err(),
            SendRefusal::AfterRefusal,
            "{what}"
        );
        assert_eq!(s.cancel().unwrap_err(), SendRefusal::AfterRefusal, "{what}");
        assert_eq!(
            s.admit_cancel(accepted, cancel.clone()).unwrap_err(),
            SendRefusal::AfterRefusal,
            "{what}"
        );
        assert_eq!(source.reads, reads, "{what}: no read after the failure");
    }
}

/// LD-D2B-7 and CANCEL-NULLABILITY: one Cancel, never before the Hello
/// slot, reason `user-interrupt`, the exact echo of what was sent compared
/// by deterministic-CBOR bytes, at the next sequence; nothing follows it.
#[test]
fn the_cancel_law() {
    let p = plan();
    let cancel = |e: Value, o: Value, reason: &str| {
        m(&[
            ("executionId", e),
            ("analysisOrdinal", o),
            ("reason", t(reason)),
        ])
    };
    let (mut s, mut source) = sender(&p);
    assert_eq!(s.cancel_payload(), None);
    divergence(s.cancel(), "cancel-before-hello");
    // The refusal ends the transcript (Codex D2B3B-R1-RF-1's audit).
    ended(&mut s, &mut source);
    // After the Hello: both null.
    let (mut s, mut source2) = sender(&p);
    s.send_next(&mut source2).unwrap();
    assert!(same(
        &s.cancel_payload().unwrap(),
        &cancel(Value::Null, Value::Null, "user-interrupt")
    ));
    for (what, payload, reason) in [
        (
            "host-shutdown",
            cancel(Value::Null, Value::Null, "host-shutdown"),
            "cancel-echo",
        ),
        (
            "an executionId before OpenUniverse",
            cancel(t(EXEC), Value::Null, "user-interrupt"),
            "cancel-echo",
        ),
        (
            "analysisOrdinal 0 before Analyze",
            cancel(Value::Null, u(0), "user-interrupt"),
            "cancel-echo",
        ),
        (
            "false for null",
            cancel(Value::Bool(false), Value::Null, "user-interrupt"),
            "cancel-echo",
        ),
    ] {
        let (mut s, mut source) = sender(&p);
        s.send_next(&mut source).unwrap();
        refused(what, s.admit_cancel(1, payload), reason);
        ended(&mut s, &mut source);
    }
    let (mut s, mut source3) = sender(&p);
    s.send_next(&mut source3).unwrap();
    divergence(
        s.admit_cancel(2, cancel(Value::Null, Value::Null, "user-interrupt")),
        "sequence",
    );
    // After OpenUniverse, then after Analyze.
    let (mut s, mut source4) = sender(&p);
    until(&mut s, &mut source4, SlotFrame::SnapshotManifest);
    assert!(same(
        &s.cancel_payload().unwrap(),
        &cancel(t(EXEC), Value::Null, "user-interrupt")
    ));
    let (mut s, mut source5) = sender(&p);
    while !s.complete() {
        s.send_next(&mut source5).unwrap();
    }
    let sent = s.cancel().unwrap();
    assert_eq!(
        sent.frame,
        HostFrame::Cancel {
            execution_id: Some(EXEC.to_owned()),
            analysis_ordinal: Some(0)
        }
    );
    let f = read_frame(
        &mut sent.bytes.as_slice(),
        cbor::Profile::Ts2,
        TS2_FRAME_MAX_DEPTH,
        None,
    )
    .unwrap()
    .unwrap();
    assert_eq!(get(f.value(), "sequence"), &u(9));
    assert!(same(
        get(f.value(), "payload"),
        &cancel(t(EXEC), u(0), "user-interrupt")
    ));
    assert_eq!(
        sent.bytes.len() as u64 - 40,
        s.request().schedule().cancel_reserve_bytes()
    );
    // At most once, and nothing follows.
    divergence(s.cancel(), "frame-after-cancel");
}

/// The table's gate (LD-D2B3B-6): T2O admits Cancel from START, but the
/// sender never sends one before the Hello slot (LD-D2B-7).
#[test]
fn the_table_gates_the_host_frames() {
    let s = Session::new();
    let mut r = s.receiver(context(&TOKENS));
    assert!(r.admits(&HostFrame::Hello));
    assert!(!r.admits(&HostFrame::OpenUniverse));
    let cancel = HostFrame::Cancel {
        execution_id: None,
        analysis_ordinal: None,
    };
    assert!(r.admits(&cancel));
    let (sender, _) = self::sender(&plan());
    assert!(sender.cancel_payload().is_none());
    r.sent(HostFrame::Hello).unwrap();
    assert_eq!(r.phase(), "WAIT_HELLO_ACK");
    assert!(!r.admits(&HostFrame::OpenUniverse));
    // The gate never steps the run itself.
    assert_eq!(r.phase(), "WAIT_HELLO_ACK");
    assert_eq!(r.terminal_kind(), None);
}

// ------------------------------------------------------------------ the participant

/// The session's context, as D4 would build it from the same Plan.
fn context_of(p: &Ts2Plan, r: &Ts2Request) -> DispatchContext {
    let mut c = context(&TOKENS);
    let text = |v: &Value| match v {
        Value::Text(s) => s.clone(),
        _ => panic!("text"),
    };
    let number = |v: &Value| match v {
        Value::Unsigned(n) => *n,
        _ => panic!("uint"),
    };
    c.capabilities = p.capabilities.clone();
    c.universe_key = text(get(r.open_universe(), "universeKey"));
    c.manifest_sha256 = text(get(r.manifest(), "manifestSha256"));
    c.manifest_files = p
        .entries
        .iter()
        .filter_map(|e| match e {
            SnapshotEntry::File {
                path,
                byte_length,
                content_sha256,
            } => Some((path.clone(), (content_sha256.clone(), *byte_length))),
            SnapshotEntry::Symlink { .. } => None,
        })
        .collect();
    c.entry_count = number(get(r.seal(), "entryCount"));
    c.total_file_bytes = number(get(r.seal(), "totalFileBytes"));
    c.total_chunk_count = number(get(r.seal(), "totalChunkCount"));
    c.stages = p
        .stages
        .iter()
        .enumerate()
        .map(|(i, s)| StageBinding {
            expected_stage_id: s.stage_id.clone(),
            stage_ordinal: i as u64,
            relations: s.relations.clone(),
            budget: match get(stage(r, i), "budget") {
                Value::Map(b) => b.iter().map(|(k, v)| (k.clone(), number(v))).collect(),
                _ => unreachable!(),
            },
            keys: s.keys.clone(),
        })
        .collect();
    c
}
fn wire(kind: &str, sequence: u64, payload: Value) -> Vec<u8> {
    write_frame(&m(&[
        ("protocolMajor", u(2)),
        ("frameType", t(kind)),
        ("sequence", u(sequence)),
        ("payload", payload),
    ]))
    .unwrap()
}

/// A scripted worker over the participant's pipes: it reads the host's
/// frames and answers each with D2b-3a's lawful frames.
struct Worker {
    c: DispatchContext,
    host: FrameAccumulator,
    sequence: u64,
    seen: Vec<String>,
    /// Replace the reply to this host frame.
    answer: Option<(&'static str, Vec<u8>)>,
}
impl Worker {
    fn new(c: DispatchContext) -> Self {
        Self {
            c,
            host: FrameAccumulator::new(cbor::Profile::Ts2, TS2_FRAME_MAX_DEPTH, None),
            sequence: 0,
            seen: Vec::new(),
            answer: None,
        }
    }
    fn reply(&mut self, kind: &str, payload: Value) -> Vec<u8> {
        self.sequence += 1;
        wire(kind, self.sequence - 1, payload)
    }
    /// The worker's answer to what the host wrote.
    fn answer(&mut self, written: &[u8]) -> Vec<u8> {
        let pushed = self.host.push(written);
        assert!(pushed.refusal.is_none());
        let mut out = Vec::new();
        for f in pushed.frames {
            let Value::Text(kind) = get(f.value(), "frameType").clone() else {
                panic!("frameType")
            };
            self.seen.push(kind.clone());
            if let Some((on, bytes)) = &self.answer
                && *on == kind
            {
                out.extend(bytes.clone());
                continue;
            }
            let c = self.c.clone();
            match kind.as_str() {
                "Hello" => out.extend(self.reply("HelloAck", hello_ack(&c))),
                "OpenUniverse" => out.extend(self.reply("UniverseAccepted", universe_accepted(&c))),
                "SnapshotSeal" => {
                    out.extend(self.reply("SnapshotAccepted", snapshot_accepted(&c)));
                    out.extend(self.reply("NativeContextVerified", native_context_verified(&c)));
                }
                "Analyze" => {
                    out.extend(self.reply("Coverage", coverage(&c, 0)));
                    out.extend(self.reply("Coverage", coverage(&c, 1)));
                    out.extend(
                        self.reply("Complete", complete(&c, &[Vec::new(), Vec::new()], &[0, 0])),
                    );
                }
                _ => {}
            }
        }
        out
    }
}

/// Drive the participant against the worker until neither has anything to
/// say; the statuses, progress and span boundaries the supervisor would see.
fn drive_all(
    part: &mut Ts2Participant<'_>,
    w: &mut Worker,
) -> (Vec<ParticipantStatus>, Vec<Progress>, Vec<Boundary>) {
    let (mut statuses, mut progress, mut boundaries) = (Vec::new(), Vec::new(), Vec::new());
    for _ in 0..64 {
        let mut fd0 = Vec::new();
        while part.wants_write() {
            let step = part.writable(&mut fd0);
            boundaries.extend(step.boundaries);
            statuses.push(step.status);
        }
        let replies = w.answer(&fd0);
        if fd0.is_empty() && replies.is_empty() {
            break;
        }
        let mut fd1 = replies.as_slice();
        while !fd1.is_empty() {
            let step = part.readable(&mut fd1);
            progress.extend(step.progress);
            boundaries.extend(step.boundaries);
            statuses.push(step.status);
        }
    }
    (statuses, progress, boundaries)
}
fn drive(part: &mut Ts2Participant<'_>, w: &mut Worker) -> (Vec<ParticipantStatus>, Vec<Progress>) {
    let (statuses, progress, _) = drive_all(part, w);
    (statuses, progress)
}
fn session<'t>(p: &Ts2Plan, table: &'t Table) -> (Ts2Participant<'t>, Worker) {
    let r = build(p);
    let c = context_of(p, &r);
    (
        Ts2Participant::new(table, c.clone(), r, Box::new(Memory::of(p))).unwrap(),
        Worker::new(c),
    )
}

/// The lawful session, Hello to DONE, as D3a drives it: each host frame is
/// written only when T2O admits it, every worker frame is admitted, and the
/// verified terminal's output is handed out once.
#[test]
fn the_participant_runs_a_lawful_session() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    let (mut part, mut w) = session(&p, &table);
    assert_eq!(part.protocol(), Protocol::Ts2);
    assert_eq!(part.protocol_waits(), ProtocolWaits::TS2);
    // Only the Hello is owed until the HelloAck arrives.
    let mut fd0 = Vec::new();
    while part.wants_write() {
        part.writable(&mut fd0);
    }
    assert_eq!(
        read_frame(
            &mut fd0.as_slice(),
            cbor::Profile::Ts2,
            TS2_FRAME_MAX_DEPTH,
            None
        )
        .unwrap()
        .unwrap()
        .payload()
        .len()
            + 40,
        fd0.len()
    );
    assert!(!part.wants_write());
    let mut fd1 = w.answer(&fd0);
    part.readable(&mut fd1.as_slice());
    fd1.clear();
    assert!(
        part.wants_write(),
        "OpenUniverse is owed after the HelloAck"
    );
    let (statuses, progress) = drive(&mut part, &mut w);
    assert_eq!(
        w.seen,
        [
            "Hello",
            "OpenUniverse",
            "SnapshotManifest",
            "SnapshotFileChunk",
            "SnapshotFileChunk",
            "SnapshotFileChunk",
            "SnapshotFileChunk",
            "SnapshotSeal",
            "Analyze"
        ]
    );
    assert_eq!(
        progress,
        [
            Progress::SnapshotAcknowledged,
            Progress::Coverage,
            Progress::StageChanged,
            Progress::Coverage
        ]
    );
    assert!(
        statuses
            .iter()
            .all(|s| !matches!(s, ParticipantStatus::Fault | ParticipantStatus::HostFault))
    );
    assert_eq!(
        statuses.last(),
        Some(&ParticipantStatus::Terminal(TerminalKind::Complete))
    );
    assert!(!part.cancel(), "no Cancel after a terminal");
    assert_eq!(
        part.process(ProcessEvent::ZeroExit).status,
        ParticipantStatus::Terminal(TerminalKind::Complete)
    );
    let step = part.readable(&mut [].as_slice());
    assert!(step.eof);
    assert_eq!(
        part.process(ProcessEvent::Eof).status,
        ParticipantStatus::Done
    );
    assert_eq!(
        part.take_terminal_output().map(|o| o.kind()),
        Some(TerminalKind::Complete)
    );
    assert!(part.take_terminal_output().is_none());
}

/// A frame the sealed snapshot cannot supply is the host's fault, never
/// `provider-protocol` (LD-D2B3B-1; R1's HostFault): no chunk is written.
#[test]
fn a_host_failure_is_a_host_fault() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    let r = build(&p);
    let c = context_of(&p, &r);
    let mut source = Memory::of(&p);
    source.fail = true;
    let mut part = Ts2Participant::new(&table, c.clone(), r, Box::new(source)).unwrap();
    let mut w = Worker::new(c);
    let (statuses, _) = drive(&mut part, &mut w);
    assert_eq!(statuses.last(), Some(&ParticipantStatus::HostFault));
    assert!(!statuses.contains(&ParticipantStatus::Fault));
    assert_eq!(w.seen, ["Hello", "OpenUniverse", "SnapshotManifest"]);
    assert!(!part.wants_write());
}

/// A refused worker frame is `provider-protocol`, and nothing more is sent:
/// a HelloAck that adds an unoffered token stops the session before
/// OpenUniverse (LD-D2B-18; reject before disclosure).
#[test]
fn a_refused_worker_frame_is_a_protocol_fault() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    let (mut part, mut w) = session(&p, &table);
    let mut ack = w.c.clone();
    ack.capabilities.push("unresolved-edge-v1".to_owned());
    ack.capabilities.sort();
    w.answer = Some(("Hello", wire("HelloAck", 0, hello_ack(&ack))));
    let (statuses, _) = drive(&mut part, &mut w);
    assert_eq!(statuses.last(), Some(&ParticipantStatus::Fault));
    assert_eq!(w.seen, ["Hello"]);
    // A stream that ends inside a frame is truncation.
    let (mut part, _) = session(&p, &table);
    let bytes = wire("HelloAck", 0, hello_ack(&context_of(&p, &build(&p))));
    part.readable(&mut &bytes[..10]);
    assert!(part.readable(&mut [].as_slice()).eof);
    assert_eq!(
        part.readable(&mut [].as_slice()).status,
        ParticipantStatus::Fault
    );
}

/// The user's Cancel (LD-D2B-7): written after the frame in flight, the
/// exact echo of what was sent, once; nothing follows it.
#[test]
fn the_participant_cancels_once() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    let (mut part, mut w) = session(&p, &table);
    // The Hello is accepted at construction, so a Cancel is lawful.
    assert!(part.cancel());
    assert!(!part.cancel() || part.wants_write());
    let mut fd0 = Vec::new();
    while part.wants_write() {
        part.writable(&mut fd0);
    }
    let pushed = w.host.push(&fd0);
    let kinds: Vec<&Value> = pushed
        .frames
        .iter()
        .map(|f| get(f.value(), "frameType"))
        .collect();
    assert_eq!(kinds, [&t("Hello"), &t("Cancel")]);
    let cancel = get(pushed.frames[1].value(), "payload");
    assert!(same(
        cancel,
        &m(&[
            ("executionId", Value::Null),
            ("analysisOrdinal", Value::Null),
            ("reason", t("user-interrupt"))
        ])
    ));
    assert_eq!(part.phase(), "WAIT_CANCELLED");
    assert!(!part.cancel());
    assert!(!part.wants_write());
}

/// The context and the request must describe one session (LD-D2B3B-5).
#[test]
fn the_context_and_request_must_join() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    for (what, change) in [
        (
            "manifestSha256",
            Box::new(|c: &mut DispatchContext| c.manifest_sha256 = h('f'))
                as Box<dyn Fn(&mut DispatchContext)>,
        ),
        (
            "universeKey",
            Box::new(|c: &mut DispatchContext| c.universe_key = sha('f')),
        ),
        (
            "a stage budget",
            Box::new(|c: &mut DispatchContext| {
                c.stages[1].budget.insert("typeQueries".to_owned(), 8);
            }),
        ),
        (
            "a key",
            Box::new(|c: &mut DispatchContext| {
                c.stages[0].keys[0].subject_scope_commitment = sha('f')
            }),
        ),
        (
            "a file",
            Box::new(|c: &mut DispatchContext| {
                c.manifest_files.remove("src/d.ts");
            }),
        ),
        (
            "the chunk count",
            Box::new(|c: &mut DispatchContext| c.total_chunk_count = 3),
        ),
    ] {
        let r = build(&p);
        let mut c = context_of(&p, &r);
        change(&mut c);
        match Ts2Participant::new(&table, c, r, Box::new(Memory::of(&p))) {
            Err(Ts2Refusal::Context(why)) => assert!(why.contains("disagree"), "{what}: {why}"),
            other => panic!("{what}: {other:?}"),
        }
    }
}

/// The candidates a FactBatch carries, anchored in the session's own
/// manifest (ANCHOR-WIRE-SPAN reads the file's digest and length).
fn anchored_batch(c: &DispatchContext, n: u64) -> (Value, Vec<Value>) {
    let digest = hex(&raw_sha256(&content("src/a.ts", 2 * MIB + 5)));
    let facts: Vec<Value> = (0..n)
        .map(|o| {
            let anchor = with(&anchor(c, 0, 10), "contentSha256", t(&digest));
            with(&candidate(c, o), "anchors", a(vec![anchor]))
        })
        .collect();
    let batch = m(&[
        ("analysisOrdinal", u(0)),
        ("stageId", t("stage-one")),
        ("batchIndex", u(0)),
        (
            "batchCommitment",
            t(&built_commitment(
                "opensip.ts-provider.fact-batch.v1",
                &a(facts.clone()),
            )),
        ),
        ("facts", a(facts.clone())),
    ]);
    (batch, facts)
}

/// Item 20 (D3a-3): each admitted FactBatch's received payload is spooled
/// and moves into the terminal output, in admission order; a discard drops
/// the output and the spool. The span boundaries are the manifest's
/// acceptance, SnapshotAccepted and NativeContextVerified (M3-L r1:400).
#[test]
fn the_participant_spools_its_candidates_and_discards_them() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    for discard in [false, true] {
        let (mut part, mut w) = session(&p, &table);
        let c = w.c.clone();
        let (batch, facts) = anchored_batch(&c, 2);
        let fact_batch = wire("FactBatch", 4, batch);
        let mut replies = fact_batch.clone();
        replies.extend(wire("Coverage", 5, coverage(&c, 0)));
        replies.extend(wire("Coverage", 6, coverage(&c, 1)));
        replies.extend(wire(
            "Complete",
            7,
            complete(&c, &[facts, Vec::new()], &[1, 0]),
        ));
        w.answer = Some(("Analyze", replies));
        let (statuses, progress, boundaries) = drive_all(&mut part, &mut w);
        assert_eq!(
            statuses.last(),
            Some(&ParticipantStatus::Terminal(TerminalKind::Complete))
        );
        assert!(progress.contains(&Progress::FactBatch));
        assert_eq!(
            boundaries,
            [
                Boundary::TransferStarted,
                Boundary::TransferEnded,
                Boundary::ContextVerified
            ]
        );
        if discard {
            part.discard();
            assert!(part.take_terminal_output().is_none());
        } else {
            let output = part.take_terminal_output().unwrap();
            assert_eq!(output.kind(), TerminalKind::Complete);
            assert_eq!(
                output.into_spool().into_candidates(),
                [fact_batch[40..].to_vec()]
            );
        }
    }
}

/// The pre-Analyze Unavailable ends the context's span as
/// NativeContextVerified would (M3-L r1:400), and is the session's terminal.
#[test]
fn a_pre_analyze_unavailable_verifies_the_context_boundary() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    let (mut part, mut w) = session(&p, &table);
    let c = w.c.clone();
    let pre = m(&[
        ("executionId", t(EXEC)),
        ("snapshotId", t(&c.snapshot_id)),
        ("planId", t(&c.plan_id)),
        ("reason", t("native-context-mismatch")),
        ("nativeContextId", t(&c.native_context_id)),
        ("recomputedNativeContextId", t(&sha('e'))),
    ]);
    let mut replies = wire("SnapshotAccepted", 2, snapshot_accepted(&c));
    replies.extend(wire("Unavailable", 3, pre));
    w.answer = Some(("SnapshotSeal", replies));
    let (statuses, _, boundaries) = drive_all(&mut part, &mut w);
    assert_eq!(
        statuses.last(),
        Some(&ParticipantStatus::Terminal(TerminalKind::Unavailable))
    );
    assert_eq!(
        boundaries,
        [
            Boundary::TransferStarted,
            Boundary::TransferEnded,
            Boundary::ContextVerified
        ]
    );
    assert!(!w.seen.contains(&"Analyze".to_owned()));
}

/// The host's own pipe ends (checklist item 3): a read or write error, and a
/// write that takes no byte, are the host's fault; WouldBlock and Interrupted
/// are neither progress nor failure.
#[test]
fn the_host_pipe_ends_fail_as_host_faults() {
    struct Pipe(Option<io::ErrorKind>, usize);
    impl io::Read for Pipe {
        fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
            self.0.map_or(Ok(0), |k| Err(io::Error::from(k)))
        }
    }
    impl io::Write for Pipe {
        fn write(&mut self, b: &[u8]) -> io::Result<usize> {
            self.0
                .map_or(Ok(self.1.min(b.len())), |k| Err(io::Error::from(k)))
        }
        fn flush(&mut self) -> io::Result<()> {
            Ok(())
        }
    }
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = plan();
    for kind in [io::ErrorKind::WouldBlock, io::ErrorKind::Interrupted] {
        let (mut part, _) = session(&p, &table);
        assert_eq!(
            part.writable(&mut Pipe(Some(kind), 0)).status,
            ParticipantStatus::Running
        );
        assert_eq!(
            part.readable(&mut Pipe(Some(kind), 0)).status,
            ParticipantStatus::Running
        );
        assert!(part.wants_write(), "{kind:?}: the Hello is still owed");
    }
    let (mut part, _) = session(&p, &table);
    assert_eq!(
        part.writable(&mut Pipe(None, 0)).status,
        ParticipantStatus::HostFault
    );
    assert!(!part.wants_write() && !part.cancel());
    let (mut part, _) = session(&p, &table);
    assert_eq!(
        part.writable(&mut Pipe(Some(io::ErrorKind::BrokenPipe), 0))
            .status,
        ParticipantStatus::HostFault
    );
    let (mut part, _) = session(&p, &table);
    assert_eq!(
        part.readable(&mut Pipe(Some(io::ErrorKind::Other), 0))
            .status,
        ParticipantStatus::HostFault
    );
    assert!(!part.wants_write());
}
