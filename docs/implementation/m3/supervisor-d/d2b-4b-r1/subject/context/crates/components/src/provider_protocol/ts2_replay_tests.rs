// Unit D2b-3c: native wire owner trial 07's TS2 replay (LD-D2B-14). Its 353
// admission vectors (31 rules) are vendored and hash-pinned; each TS2 rule
// whose inputs are wire values is replayed against D2b's own code, and every
// other rule is classified with its reason. The classification is checked
// complete against the vendored file. Trial 07's scope is historical: it
// carries neither successor token, so this claims nothing beyond it.
use super::*;
use crate::provider_protocol::manifest_digest;

const TRIAL07: &[u8] = include_bytes!("../../tests/data/trial07-admission-vectors.v1.json");
/// SHA-256 of `docs/implementation/m1/trials/native-wire-owner-07/subject/admission-vectors.json`.
const TRIAL07_SHA256: &str = "e93c69e57f24c8309544c5773b2394d2c8973d2dcb67da604afb2bb1edc06290";

fn trial07() -> BTreeMap<String, Vec<J>> {
    assert_eq!(
        hex(&raw_sha256(TRIAL07)),
        TRIAL07_SHA256,
        "the vendored trial 07 vectors"
    );
    // The original trial includes one Rust3-only negative with an intentional
    // float zero. A separately pinned replay selection preserves all other
    // vectors by value and retains that exact vector as raw JSON metadata.
    // Its source/selection equality is checked independently in the owning lane.
    const SELECTION: &[u8] = include_bytes!("../../tests/data/trial07-integer-replay.v1.json");
    assert_eq!(
        hex(&raw_sha256(SELECTION)),
        "79d0ee27533f3c4a5ac2c3f90db9423412304a7148aeaec41582c892f56dc9ae"
    );
    let doc = parse_json(SELECTION).unwrap();
    assert_eq!(s(&doc, &["sourceSha256"]), TRIAL07_SHA256);
    let Some(J::Array(deferred)) = path(&doc, &["deferredVectors"]) else {
        panic!("deferred")
    };
    assert_eq!(deferred.len(), 1);
    assert_eq!(
        s(&deferred[0], &["id"]),
        "cancel-analysis-ordinal-float-zero-refused"
    );
    assert_eq!(s(&deferred[0], &["owner"]), "D2b-4c Rust3");
    let raw = s(&deferred[0], &["originalVectorJson"]);
    assert!(matches!(
        parse_json(raw.as_bytes()),
        Err(opensip_identity::CanonicalError::FloatForbidden)
    ));
    let Some(J::Object(rules)) = path(&doc, &["vectors"]) else {
        panic!("vectors")
    };
    rules
        .iter()
        .map(|(k, v)| match v {
            J::Array(v) => (k.clone(), v.clone()),
            _ => panic!("{k}"),
        })
        .collect()
}
fn s(v: &J, keys: &[&str]) -> String {
    match path(v, keys) {
        Some(J::String(x)) => x.clone(),
        other => panic!("{keys:?}: {other:?}"),
    }
}
fn n(v: &J, keys: &[&str]) -> u64 {
    match path(v, keys) {
        Some(J::Integer(i)) => u64::try_from(i.get()).unwrap(),
        other => panic!("{keys:?}: {other:?}"),
    }
}
fn accept(v: &J) -> bool {
    match s(v, &["kind"]).as_str() {
        "accept" => true,
        "refuse" => false,
        other => panic!("kind {other}"),
    }
}
/// A JSON input value as wire CBOR; `{"$bytesHex": …}` is a byte string.
fn wire_value(j: &J) -> Value {
    match j {
        J::Object(o) if o.len() == 1 && o.contains_key("$bytesHex") => {
            let J::String(h) = &o["$bytesHex"] else {
                panic!("$bytesHex")
            };
            Value::Bytes(
                (0..h.len())
                    .step_by(2)
                    .map(|i| u8::from_str_radix(&h[i..i + 2], 16).unwrap())
                    .collect(),
            )
        }
        J::Null => Value::Null,
        J::Bool(b) => Value::Bool(*b),
        J::Integer(i) => u(u64::try_from(i.get()).unwrap()),
        J::String(x) => t(x),
        J::Array(a) => Value::Array(a.iter().map(wire_value).collect()),
        J::Object(o) => Value::Map(o.iter().map(|(k, v)| (k.clone(), wire_value(v))).collect()),
    }
}
fn entry_of(e: &J) -> SnapshotEntry {
    SnapshotEntry::File {
        path: s(e, &["path"]),
        byte_length: n(e, &["byteLength"]),
        content_sha256: s(e, &["contentSha256"]),
    }
}

/// How each of trial 07's rules is replayed here (LD-D2B3C-8). Every rule
/// is named once; the test checks the list against the vendored file.
const REPLAYED: [&str; 15] = [
    "TS2-LOGICAL-PATH-ADMISSION",
    "TS2-MANIFEST-DIGEST",
    "CHUNK-CUSTODY",
    "SEAL-AGGREGATES",
    "CANCEL-NULLABILITY",
    "CANCELLED-ECHO",
    "ACCEPTED-EQUALS-SEAL",
    "ANCHOR-WIRE-SPAN",
    "ANCHOR-FACT-REF-REFUSED",
    "OCCUPANCY-JOIN",
    "COMMIT-MAP",
    "HOST-SEND-SCHEDULE",
    "REQUEST-WIRE-ACCOUNTING",
    "PATH-SITE-SEGMENT-LAW",
    "OWNER-PATTERN-EVALUATION",
];
// PATH-SITE-SEGMENT-LAW and OWNER-PATTERN-EVALUATION are replayed at their
// TS2 sites and calls only; COMMIT-MAP, ANCHOR-WIRE-SPAN and the two
// schedule rules at their TS2 vectors only (the rest are Rust3's).
/// Rules no TS2 code of D2b's executes, by owner.
const NOT_REPLAYED: [(&str, &str); 16] = [
    ("CANONICAL-PATH-ADMISSION", "Rust3 (D2b-4c)"),
    ("RAW-MANIFEST-DIGEST", "Rust3 (D2b-4c)"),
    ("DEPSRC-CUSTODY", "Rust3 (D2b-4c)"),
    ("PACKAGE-KEY-JOIN", "Rust3 (D2b-4c)"),
    ("PREPARED-V3-ENTRY", "Rust3 (D2b-4c)"),
    ("RUST3-PROVIDER-FAULT", "Rust3 (D2b-4c)"),
    ("RUST3-CANCEL-TYPES", "Rust3 (D2b-4c)"),
    ("RUST3-BUDGET-EXHAUSTED", "Rust3 (D2b-4c)"),
    ("P3-OVERLAY", "Rust3's table overlay (D2b-2 replays P3T)"),
    (
        "DEPSRC-SET-KEY-CONSTRAINTS",
        "the Plan side's set admission (C4), not D2b",
    ),
    (
        "DEPSRC-WIRE-REPRESENTABILITY",
        "the Plan side's set admission (C4), not D2b",
    ),
    (
        "PREPARED-V3-READ-AUTHORITY",
        "the Plan side's set admission (C4), not D2b",
    ),
    (
        "PREPARED-V3-WIRE-LIMIT",
        "the Plan side's set admission (C4), not D2b",
    ),
    (
        "PREPARED-V3-PATH-REPRESENTABILITY",
        "the Plan side's set admission (C4), not D2b",
    ),
    (
        "RELATION-PAYLOAD-PATH-LAW",
        "H's validate_registered_record",
    ),
    (
        "PER-KEY-SCOPE2",
        "the Plan side mints the scope2 descriptors (C4); its inputs are descriptor templates, and D2b's echo is D2b-3a's tests'",
    ),
];

#[test]
fn the_classification_is_complete() {
    let rules: BTreeSet<String> = trial07().into_keys().collect();
    let named: Vec<&str> = REPLAYED
        .iter()
        .copied()
        .chain(NOT_REPLAYED.iter().map(|(r, _)| *r))
        .collect();
    let named_set: BTreeSet<String> = named.iter().map(|r| (*r).to_owned()).collect();
    assert_eq!(named.len(), named_set.len(), "each rule named once");
    assert_eq!(rules, named_set);
    assert_eq!(rules.len(), 31);
    assert_eq!(trial07().values().map(Vec::len).sum::<usize>() + 1, 353);
}

/// TS2-LOGICAL-PATH-ADMISSION: the carriers' `Ts2ProjectPath` lexical rule.
#[test]
fn replay_ts2_logical_path_admission() {
    let carriers = carrier::Carriers::load("Ts2").unwrap();
    let t2 = parse_json(br#"{"t":"ref","ref":"Ts2ProjectPath"}"#).unwrap();
    for v in &trial07()["TS2-LOGICAL-PATH-ADMISSION"] {
        let got = carriers.check(&t2, &t(&s(v, &["input", "path"])), "path");
        assert_eq!(got.is_ok(), accept(v), "{}", s(v, &["id"]));
    }
}

/// TS2-MANIFEST-DIGEST: the raw digest of the entries, and the closed
/// manifest record (a domain-form digest is not a DigestHex).
#[test]
fn replay_ts2_manifest_digest() {
    let carriers = carrier::Carriers::load("Ts2").unwrap();
    for v in &trial07()["TS2-MANIFEST-DIGEST"] {
        let m_ = path(v, &["input", "manifest"]).unwrap();
        let entries = wire_value(path(m_, &["entries"]).unwrap());
        let claimed = s(m_, &["manifestSha256"]);
        let manifest = m(&[
            ("snapshotId", t(&format!("snapshot2:{}", h('a')))),
            ("manifestSha256", t(&claimed)),
            ("entries", entries.clone()),
        ]);
        let ok = carriers
            .check_record("Ts2SnapshotManifestV1", &manifest)
            .is_ok()
            && manifest_digest(&entries) == claimed;
        assert_eq!(ok, accept(v), "{}", s(v, &["id"]));
    }
}

/// A one-entry plan whose bytes `source` holds.
fn one_entry(e: SnapshotEntry, bytes: Vec<u8>) -> (Ts2Plan, Memory) {
    let mut p = plan();
    let path_ = match &e {
        SnapshotEntry::File { path, .. } => path.clone(),
        SnapshotEntry::Symlink { path, .. } => path.clone(),
    };
    p.entries = vec![e];
    let mut source = Memory::of(&p);
    source.files.insert(path_, bytes);
    (p, source)
}

/// CHUNK-CUSTODY. The rule admits any lawful chunking on the worker's side;
/// D2b's sender emits only the canonical greedy chunking (HOST-SEND-SCHEDULE)
/// and refuses every other. So each refusal vector's transcript is refused
/// before writing, and the acceptance vector's entry and bytes are accepted
/// in their canonical chunking, its own two-chunk split being refused by
/// design.
#[test]
fn replay_chunk_custody() {
    for v in &trial07()["CHUNK-CUSTODY"] {
        let id = s(v, &["id"]);
        let J::Array(chunks) = path(v, &["input", "chunks"]).unwrap() else {
            panic!("chunks")
        };
        let bytes: Vec<u8> = chunks
            .iter()
            .flat_map(|c| match wire_value(path(c, &["bytes"]).unwrap()) {
                Value::Bytes(b) => b,
                _ => panic!("bytes"),
            })
            .collect();
        let entry = entry_of(path(v, &["input", "entry"]).unwrap());
        let (p, mut source) = one_entry(entry, bytes.clone());
        let (mut sender, _) = self::sender(&p);
        let chunked = sender
            .request()
            .schedule()
            .slots()
            .iter()
            .any(|x| x.frame == SlotFrame::SnapshotFileChunk);
        let target = if chunked {
            SlotFrame::SnapshotFileChunk
        } else {
            SlotFrame::SnapshotSeal
        };
        until(&mut sender, &mut source, target);
        let mut refused = false;
        for c in chunks {
            let Some(slot) = sender.next_slot() else {
                refused = true;
                break;
            };
            let seq = slot.sequence;
            let payload = with(&wire_value(c), "snapshotId", t(&p.snapshot_id));
            if sender
                .admit(SlotFrame::SnapshotFileChunk, seq, payload)
                .is_err()
            {
                refused = true;
                break;
            }
        }
        if accept(v) {
            assert!(refused, "{id}: a non-canonical split is refused by design");
            let (mut sender, _) = self::sender(&p);
            while !sender.complete() {
                sender.send_next(&mut source).unwrap();
            }
        } else {
            assert!(refused, "{id}");
        }
    }
}
/// SEAL-AGGREGATES: the builder's seal from the entries.
#[test]
fn replay_seal_aggregates() {
    for v in &trial07()["SEAL-AGGREGATES"] {
        let J::Array(entries) = path(v, &["input", "entries"]).unwrap() else {
            panic!("entries")
        };
        let mut p = plan();
        p.entries = entries.iter().map(entry_of).collect();
        let r = build(&p);
        let ok = ["entryCount", "totalFileBytes", "totalChunkCount"]
            .iter()
            .all(|k| get(r.seal(), k) == &u(n(v, &["input", "seal", k])));
        assert_eq!(ok, accept(v), "{}", s(v, &["id"]));
    }
}

/// CANCEL-NULLABILITY: the sender's Cancel after the frames the vector sent.
#[test]
fn replay_cancel_nullability() {
    for v in &trial07()["CANCEL-NULLABILITY"] {
        let mut p = plan();
        let J::Array(sent) = path(v, &["input", "sent"]).unwrap() else {
            panic!("sent")
        };
        for f in sent {
            if let Some(J::String(e)) = path(f, &["payload", "executionId"]) {
                p.execution_id = e.clone();
            }
        }
        let last = s(sent.last().unwrap(), &["frame"]);
        let (mut sender, mut source) = self::sender(&p);
        match last.as_str() {
            "Hello" => {
                sender.send_next(&mut source).unwrap();
            }
            "OpenUniverse" => until(&mut sender, &mut source, SlotFrame::SnapshotManifest),
            "Analyze" => {
                while !sender.complete() {
                    sender.send_next(&mut source).unwrap();
                }
            }
            other => panic!("{other}"),
        }
        let cancel = wire_value(path(v, &["input", "cancel"]).unwrap());
        let cancel = with(&cancel, "reason", t("user-interrupt"));
        let all = sender.request().schedule().slots().len() as u64;
        let seq = sender.next_slot().map_or(all, |x| x.sequence);
        let got = sender.admit_cancel(seq, cancel);
        assert_eq!(got.is_ok(), accept(v), "{}: {got:?}", s(v, &["id"]));
    }
}

/// CANCELLED-ECHO: the receiver's Cancelled against the Cancel sent. Its
/// observedPhase is TS2-OBSERVED-PHASE's (`snapshot` after a Cancel in
/// READY_ANALYZE), the successor law the vector predates.
#[test]
fn replay_cancelled_echo() {
    let session = Session::new();
    for v in &trial07()["CANCELLED-ECHO"] {
        let mut c = context(&TOKENS);
        c.execution_id = s(v, &["input", "cancel", "executionId"]);
        let mut r = session.receiver(c.clone());
        let seq = startup(&mut r, &c);
        r.sent(HostFrame::Cancel {
            execution_id: Some(c.execution_id.clone()),
            analysis_ordinal: None,
        })
        .unwrap();
        let cancelled = with(
            &wire_value(path(v, &["input", "cancelled"]).unwrap()),
            "observedPhase",
            t("snapshot"),
        );
        let got = r.receive(frame("Cancelled", seq, cancelled));
        assert_eq!(got.is_ok(), accept(v), "{}: {got:?}", s(v, &["id"]));
    }
}

/// ACCEPTED-EQUALS-SEAL: SnapshotAccepted against the Seal the context holds.
#[test]
fn replay_accepted_equals_seal() {
    let session = Session::new();
    for v in &trial07()["ACCEPTED-EQUALS-SEAL"] {
        let mut c = context(&TOKENS);
        c.snapshot_id = s(v, &["input", "seal", "snapshotId"]);
        c.manifest_sha256 = s(v, &["input", "seal", "manifestSha256"]);
        c.entry_count = n(v, &["input", "seal", "entryCount"]);
        c.total_file_bytes = n(v, &["input", "seal", "totalFileBytes"]);
        c.total_chunk_count = n(v, &["input", "seal", "totalChunkCount"]);
        let mut r = session.receiver(c.clone());
        r.sent(HostFrame::Hello).unwrap();
        r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap();
        r.sent(HostFrame::OpenUniverse).unwrap();
        r.receive(frame("UniverseAccepted", 1, universe_accepted(&c)))
            .unwrap();
        r.sent(HostFrame::SnapshotManifest).unwrap();
        r.sent(HostFrame::SnapshotSeal).unwrap();
        let got = r.receive(frame(
            "SnapshotAccepted",
            2,
            wire_value(path(v, &["input", "accepted"]).unwrap()),
        ));
        assert_eq!(got.is_ok(), accept(v), "{}: {got:?}", s(v, &["id"]));
    }
}

/// ANCHOR-WIRE-SPAN and ANCHOR-FACT-REF-REFUSED, the TS2 vectors: a
/// candidate carrying the vector's anchors over the vector's manifest.
#[test]
fn replay_anchors() {
    let session = Session::new();
    let rules = trial07();
    let mut replayed = 0;
    for v in rules["ANCHOR-WIRE-SPAN"]
        .iter()
        .chain(&rules["ANCHOR-FACT-REF-REFUSED"])
    {
        if s(v, &["input", "language"]) != "typescript-semantic" {
            continue;
        }
        let J::Object(manifest) = path(v, &["input", "manifest"]).unwrap() else {
            panic!("manifest")
        };
        let mut c = context(&TOKENS);
        c.manifest_files = manifest
            .iter()
            .map(|(p, e)| (p.clone(), (s(e, &["contentSha256"]), n(e, &["byteLength"]))))
            .collect();
        let anchors = wire_value(path(v, &["input", "anchors"]).unwrap());
        if let Value::Array(a0) = &anchors
            && let Some(first) = a0.first()
        {
            c.snapshot_id = match get(first, "snapshotId") {
                Value::Text(x) => x.clone(),
                _ => c.snapshot_id.clone(),
            };
        }
        let candidate = with(&candidate(&c, 0), "anchors", anchors);
        let facts = vec![candidate];
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
            ("facts", a(facts)),
        ]);
        let mut r = session.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        let got = r.receive(frame("FactBatch", seq, batch));
        assert_eq!(got.is_ok(), accept(v), "{}: {got:?}", s(v, &["id"]));
        replayed += 1;
    }
    assert_eq!(replayed, 5, "the five TS2 anchor vectors");
}

/// OCCUPANCY-JOIN: a FactBatchV3 whose candidates and companions carry the
/// vector's ordinals and targets.
#[test]
fn replay_occupancy_join() {
    let session = Session::new();
    let mut tokens = TOKENS.to_vec();
    tokens.push("target-attribution-v2");
    tokens.sort();
    for v in &trial07()["OCCUPANCY-JOIN"] {
        let mut c = context(&tokens);
        let J::Array(cands) = path(v, &["input", "batch", "candidates"]).unwrap() else {
            panic!()
        };
        let J::Array(comps) = path(v, &["input", "batch", "occupancyCompanions"]).unwrap() else {
            panic!()
        };
        for x in cands.iter().chain(comps) {
            c.target_domain.insert(s(x, &["targetUniverseId"]));
        }
        let candidates: Vec<Value> = cands
            .iter()
            .map(|x| {
                with(
                    &candidate(&c, n(x, &["candidateOrdinal"])),
                    "targetUniverseId",
                    t(&s(x, &["targetUniverseId"])),
                )
            })
            .collect();
        let companions: Vec<Value> = comps
            .iter()
            .map(|x| {
                m(&[
                    ("schemaVersion", u(1)),
                    ("candidateOrdinal", u(n(x, &["candidateOrdinal"]))),
                    ("targetUniverseId", t(&s(x, &["targetUniverseId"]))),
                    ("targetNativeId", t("ts:f")),
                    ("kind", t("file")),
                    ("occupancy", t("external")),
                    ("exported", Value::Null),
                    ("logicalPath", Value::Null),
                    ("packageManifestPath", Value::Null),
                    ("evaluationNativeId", Value::Null),
                ])
            })
            .collect();
        let v3 = m(&[
            ("schemaVersion", u(3)),
            ("analysisOrdinal", u(0)),
            ("stageId", t("stage-one")),
            ("batchIndex", u(0)),
            ("candidates", a(candidates)),
            ("occupancyCompanions", a(companions)),
        ]);
        let mut r = session.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        let got = r.receive(frame("FactBatch", seq, v3));
        assert_eq!(got.is_ok(), accept(v), "{}: {got:?}", s(v, &["id"]));
    }
}

/// COMMIT-MAP, the TS2 fields: each vector's recipe (delivery.v2's commitment
/// domains, DLV:1080-1088, and its value class) against the domain and value
/// class the receiver uses for the field (the carriers' `commitmentMap`).
#[test]
fn replay_commit_map() {
    let carriers = parse_json(carrier::CARRIERS).unwrap();
    let J::Array(rows) = path(&carriers, &["commitmentMap", "rows"]).unwrap() else {
        panic!("rows")
    };
    let recipes = BTreeMap::from([
        (
            "stageCoverage",
            ("opensip.ts-provider.stage-coverage.v1", "stage-entries"),
        ),
        (
            "coverageStream",
            (
                "opensip.ts-provider.coverage-stream.v1",
                "stage-major-entries",
            ),
        ),
    ]);
    let mut replayed = 0;
    for v in &trial07()["COMMIT-MAP"] {
        if s(v, &["input", "commitment", "$ownerCommit", "doc"]) != "delivery2" {
            continue;
        }
        let field_ = s(v, &["input", "field"]);
        let row = rows
            .iter()
            .find(|r| path(r, &["field"]) == Some(&J::String(field_.clone())))
            .unwrap_or_else(|| panic!("{field_}"));
        let (domain, class) =
            recipes[s(v, &["input", "commitment", "$ownerCommit", "recipe"]).as_str()];
        let ok = s(row, &["domain"]) == domain && s(row, &["valueClass"]) == class;
        assert_eq!(ok, accept(v), "{}", s(v, &["id"]));
        replayed += 1;
    }
    assert_eq!(replayed, 4);
}

/// A plan materialized from a compact plan description (trial 07's
/// `build_plan` groups): distinct paths of each group's exact scalar length,
/// so every entry encodes at the reference's length, contents whose digests
/// are the bytes the source holds.
fn materialize(desc: &J) -> (Ts2Plan, Memory) {
    let J::Array(groups) = path(desc, &["snapshot"]).unwrap() else {
        panic!("snapshot")
    };
    let mut p = plan();
    let mut entries = Vec::new();
    let mut files = BTreeMap::new();
    for (g, group) in groups.iter().enumerate() {
        let (count, scalars, length) = (
            n(group, &["n"]),
            n(group, &["pathScalars"]) as usize,
            n(group, &["byteLength"]),
        );
        for i in 0..count {
            // Each path is `scalars` long, padded with `x`, unless that is too
            // short to be distinct (the entry-bound vectors' one-scalar
            // groups), where the eight-scalar id is used: the entry bound does
            // not read path lengths.
            let id = format!("{g}{i:07}");
            let path = format!("{}{id}", "x".repeat(scalars.saturating_sub(id.len())));
            let small = length <= 1 << 20;
            let bytes = if small {
                vec![0u8; length as usize]
            } else {
                Vec::new()
            };
            let content = if small {
                hex(&raw_sha256(&bytes))
            } else {
                h('1')
            };
            entries.push(SnapshotEntry::File {
                path: path.clone(),
                byte_length: length,
                content_sha256: content,
            });
            files.insert(path, bytes);
        }
    }
    entries.sort_by(|a, b| match (a, b) {
        (SnapshotEntry::File { path: x, .. }, SnapshotEntry::File { path: y, .. }) => x.cmp(y),
        _ => unreachable!(),
    });
    p.entries = entries;
    let mut source = Memory::of(&p);
    source.files = files;
    (p, source)
}

/// REQUEST-WIRE-ACCOUNTING, the TS2 vectors, through the schedule
/// constructor on each materialized plan. One is not run:
/// `ts2-snapshot-manifest-frame-over` (200,000 paths of 4,096 scalars, about
/// 1.6 GB materialized); D2b-3b's `the_bounds_refuse_through_the_route`
/// refuses the same frame bound over a 16,500-entry manifest.
#[test]
fn replay_request_wire_accounting() {
    let mut replayed = 0;
    for v in &trial07()["REQUEST-WIRE-ACCOUNTING"] {
        let desc = path(v, &["input", "plan"]).unwrap();
        if s(desc, &["protocol"]) != "typescript-semantic"
            || s(v, &["id"]) == "ts2-snapshot-manifest-frame-over"
        {
            continue;
        }
        let id = s(v, &["id"]);
        let (p, _) = materialize(desc);
        let got = Ts2Request::build(&p);
        match (accept(v), &got) {
            (true, Ok(r)) => {
                if let Some(J::Integer(frames)) = path(desc, &["expectFrames"]) {
                    // The slots and the one reserved Cancel.
                    assert_eq!(r.schedule().slots().len() as i128 + 1, frames.get(), "{id}");
                }
                if let Some(J::Integer(largest)) =
                    path(desc, &["expectLargestFrame", "SnapshotManifest"])
                {
                    let manifest = r
                        .schedule()
                        .slots()
                        .iter()
                        .find(|x| x.frame == SlotFrame::SnapshotManifest)
                        .unwrap();
                    assert_eq!(manifest.payload_bytes as i128, largest.get(), "{id}");
                }
            }
            (false, Err(PlanRefusal::ExceedsWireLimit { route, faults })) => {
                let want = s(v, &["expect"]);
                let (route_want, fault_want) = want
                    .strip_prefix("ROUTE:")
                    .unwrap()
                    .split_once(':')
                    .unwrap();
                assert_eq!(route, route_want, "{id}");
                assert!(
                    faults.iter().any(|f| f.starts_with(fault_want)),
                    "{id}: {faults:?}"
                );
            }
            _ => panic!("{id}: {got:?}"),
        }
        replayed += 1;
    }
    assert_eq!(replayed, 6);
}

/// HOST-SEND-SCHEDULE, the TS2 vectors, through the sender on each
/// materialized plan. TS2 declares no request totals, so the vector that
/// consumes under overridden totals is the canonical transcript (the sender
/// takes no other limits).
#[test]
fn replay_host_send_schedule() {
    let mut replayed = 0;
    for v in &trial07()["HOST-SEND-SCHEDULE"] {
        let desc = path(v, &["input", "send", "plan"]).unwrap();
        if s(desc, &["protocol"]) != "typescript-semantic" {
            continue;
        }
        let id = s(v, &["id"]);
        let (p, mut source) = materialize(desc);
        let (mut sender, _) = self::sender(&p);
        let transcript = path(v, &["input", "send", "transcript"]).unwrap();
        let got: Result<(), SendRefusal> = match s(transcript, &["kind"]).as_str() {
            "canonical" => (|| {
                while !sender.complete() {
                    sender.send_next(&mut source)?;
                }
                Ok(())
            })(),
            "cancel-at" => (|| {
                let frames = match path(transcript, &["frames"]) {
                    Some(J::Integer(i)) => i.get(),
                    _ => panic!("frames"),
                };
                let k = if frames < 0 {
                    sender.request().schedule().slots().len()
                } else {
                    frames as usize
                };
                for _ in 0..k {
                    sender.send_next(&mut source)?;
                }
                let mut cancel = sender.cancel_payload().unwrap_or(m(&[
                    ("executionId", Value::Null),
                    ("analysisOrdinal", Value::Null),
                    ("reason", t("user-interrupt")),
                ]));
                if let Some(J::Object(o)) = path(transcript, &["override"]) {
                    for (k, x) in o {
                        let value = match x {
                            J::String(w) if w == "$wrong-same-length" => {
                                t("exec1_0123456789abcdef0123456789abcdee")
                            }
                            other => wire_value(other),
                        };
                        cancel = with(&cancel, k, value);
                    }
                }
                let seq = k as u64;
                sender.admit_cancel(seq, cancel).map(|_| ())
            })(),
            "substitute" => (|| {
                let frame_ = s(transcript, &["frameType"]);
                assert_eq!(frame_, "OpenUniverse");
                sender.send_next(&mut source)?;
                let ou = with(
                    sender.request().open_universe(),
                    &s(transcript, &["field"]),
                    t("exec1_0123456789abcdef0123456789abcdee"),
                );
                sender.admit(SlotFrame::OpenUniverse, 1, ou).map(|_| ())
            })(),
            other => panic!("{other}"),
        };
        match (accept(v), &got) {
            (true, Ok(())) => assert!(sender.complete(), "{id}"),
            (false, Err(SendRefusal::Divergence(d))) => {
                assert!(d.starts_with(&s(v, &["expect"])), "{id}: {d}");
            }
            _ => panic!("{id}: {got:?}"),
        }
        replayed += 1;
    }
    assert_eq!(replayed, 7);
}

/// PATH-SITE-SEGMENT-LAW and OWNER-PATTERN-EVALUATION, the sites a TS2
/// builder or receiver schema check reaches: the TS universe's `jsRootFiles` and
/// `programRootFiles` (their exact schema-string item sites), and the occupancy
/// companion's LogicalPath (FactBatchV3's). Every other site and owner call
/// is Rust's, the dependency or prepared set's (C4), or the evidence
/// schema's Plan-side use.
#[test]
fn replay_path_sites() {
    let rules = trial07();
    let mut replayed = 0;
    for v in &rules["PATH-SITE-SEGMENT-LAW"] {
        let site = s(v, &["input", "site"]);
        let value = s(v, &["input", "value"]);
        let ok = match site.as_str() {
            "jsRootFiles" | "programRootFiles" => {
                let mut p = plan();
                let J::Object(mut u_) = p.universe.clone() else {
                    panic!("universe")
                };
                let J::Object(mut ri) = u_["resolvedInputs"].clone() else {
                    panic!("resolvedInputs")
                };
                ri.insert(site.clone(), J::Array(vec![J::String(value.clone())]));
                u_.insert("resolvedInputs".to_owned(), J::Object(ri));
                p.universe = J::Object(u_);
                let result = Ts2Request::build(&p);
                assert_eq!(
                    result.is_ok(),
                    accept(v),
                    "{} enclosing admission: {result:?}",
                    s(v, &["id"])
                );
                result.is_ok()
            }
            "occupancy-LogicalPath" => carrier::admit_extern(
                "opensip.product.occupancy-companion.1#/$defs/LogicalPath",
                &t(&value),
            )
            .is_ok(),
            _ => continue,
        };
        assert_eq!(ok, accept(v), "{}", s(v, &["id"]));
        replayed += 1;
    }
    assert_eq!(replayed, 15);
    // OWNER-PATTERN-EVALUATION: its `logical-re` calls are the identity
    // LogicalPath pattern, which the TS2 checks evaluate at the occupancy
    // companion's and the census's LogicalPath; its other calls are the
    // dependency-file, generated-file, crate-root, dependency-set and
    // prepared-set owners (Rust3 and the Plan side).
    let mut logical = 0;
    for v in &rules["OWNER-PATTERN-EVALUATION"] {
        if s(v, &["input", "owner", "call"]) != "logical-re" {
            continue;
        }
        let value = t(&s(v, &["input", "owner", "value"]));
        for def in [
            "opensip.product.occupancy-companion.1#/$defs/LogicalPath",
            "opensip.product.symbol-census.1#/$defs/LogicalPath",
        ] {
            assert_eq!(
                carrier::admit_extern(def, &value).is_ok(),
                accept(v),
                "{} at {def}",
                s(v, &["id"])
            );
        }
        logical += 1;
    }
    assert_eq!(logical, 2);
}
