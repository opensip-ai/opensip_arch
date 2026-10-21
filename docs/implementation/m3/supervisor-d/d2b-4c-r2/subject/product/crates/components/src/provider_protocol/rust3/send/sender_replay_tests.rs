//! Historical send predicates through independent Sender realization.
//! Small wire-only descriptions are given separate synthetic C4 projections:
//! one nonempty Rust path of the same scalar length, native H joins, and actual
//! zero-byte-source hashes. Original mutations/lengths/typed echoes are kept.
//! Two symbolic multi-GiB cases use actual charging/greedy chunk predicates,
//! without pretending their placeholder digests establish byte custody.
use super::*;
use opensip_identity::{JsonInteger, JsonValue as J, hash_canonical_value, parse_json};
const CORPUS: &[u8] = include_bytes!("../../../../tests/data/trial07-integer-replay.v1.json");
const FX: &[u8] = include_bytes!("../../../../tests/data/trial07-accounting-fixtures.v1.json");
fn jget<'a>(v: &'a J, k: &str) -> &'a J {
    let J::Object(v) = v else { panic!() };
    v.get(k).unwrap()
}
fn arr(v: &J) -> &[J] {
    let J::Array(v) = v else { panic!() };
    v
}
fn str_(v: &J) -> &str {
    let J::String(v) = v else { panic!() };
    v
}
fn num(v: &J) -> u64 {
    let J::Integer(v) = v else { panic!() };
    u64::try_from(v.get()).unwrap()
}
fn js(s: &str) -> J {
    J::String(s.into())
}
fn jn(n: u64) -> J {
    J::Integer(JsonInteger::new(i128::from(n)).unwrap())
}
fn jobj(v: Vec<(&str, J)>) -> J {
    J::Object(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn jput(v: &mut J, k: &str, new: J) {
    let J::Object(v) = v else { panic!() };
    v.insert(k.into(), new);
}
fn put(v: &mut Value, k: &str, new: Value) {
    let Value::Map(v) = v else { panic!() };
    v.iter_mut().find(|(s, _)| s == k).unwrap().1 = new;
}
fn vget<'a>(v: &'a Value, k: &str) -> &'a Value {
    field(v, k).unwrap()
}
fn wire(v: &J) -> Value {
    match v {
        J::Null => Value::Null,
        J::Bool(v) => Value::Bool(*v),
        J::Integer(_) => Value::Unsigned(num(v)),
        J::String(v) => t(v),
        J::Array(v) => Value::Array(v.iter().map(wire).collect()),
        J::Object(v) => Value::Map(v.iter().map(|(k, v)| (k.clone(), wire(v))).collect()),
    }
}
fn native(domain: &str, v: &J) -> String {
    format!(
        "sha256:{}",
        digest_hex(&hash_canonical_value(domain, v).unwrap())
    )
}
fn zero_hash(n: u64) -> String {
    assert!(n <= 30);
    digest_hex(&raw_sha256(&vec![0; n as usize]))
}
#[derive(Default)]
struct Zeros {
    reads: Vec<(Entry, u64, usize)>,
}
impl Source for Zeros {
    fn read(&mut self, e: &Entry, offset: u64, n: usize) -> std::io::Result<Vec<u8>> {
        assert!(n <= 30);
        self.reads.push((e.clone(), offset, n));
        Ok(vec![0; n])
    }
}
fn request(p: &J) -> Request {
    let mut plan = super::super::request::tests::plan(true, false);
    plan.analysis_ordinal = 0;
    plan.open.execution_id = "exec-2026-09-13-0001".into();
    plan.snapshot = arr(jget(p, "snapshot"))
        .iter()
        .flat_map(|g| {
            assert_eq!(num(jget(g, "n")), 1);
            let scalars = num(jget(g, "pathScalars")) as usize;
            assert!(scalars >= 3);
            let path = format!("{}.rs", "s".repeat(scalars - 3));
            let length = num(jget(g, "byteLength"));
            [snapshot::Entry::File {
                path,
                byte_length: length,
                content_sha256: zero_hash(length),
                executable: false,
            }]
        })
        .collect();
    let deps = arr(jget(p, "dependency"));
    assert_eq!(deps.len(), 1);
    let g = &deps[0];
    assert_eq!(num(jget(g, "n")), 1);
    let key = str_(jget(g, "packageKey"));
    let parts: Vec<_> = key.splitn(3, ' ').collect();
    assert_eq!(parts.len(), 3);
    let length = num(jget(g, "byteLength"));
    let files = J::Array(vec![jobj(vec![
        (
            "path",
            js(&"d".repeat(num(jget(g, "pathScalars")) as usize)),
        ),
        ("byteLength", jn(length)),
        ("contentSha256", js(&zero_hash(length))),
    ])]);
    let hash =
        digest_hex(&hash_canonical_value("native.dependency-file-manifest.v1", &files).unwrap());
    plan.dependency_manifests = BTreeMap::from([(hash.clone(), files)]);
    let J::Object(set) = &mut plan.dependency_set else {
        panic!()
    };
    let J::Array(packages) = set.get_mut("packages").unwrap() else {
        panic!()
    };
    assert_eq!(packages.len(), 1);
    for (k, v) in [
        ("name", js(parts[0])),
        ("version", js(parts[1])),
        ("sourceId", js(parts[2])),
        ("fileManifestSha256", js(&hash)),
        ("fileCount", jn(1)),
        ("totalBytes", jn(length)),
    ] {
        jput(&mut packages[0], k, v);
    }
    let dep_id = native("native.dependency-source-set.v1", &plan.dependency_set);
    put(
        &mut plan.open.repository_resolution,
        "dependencySourceSetId",
        t(&dep_id),
    );
    let mut resolved = vget(&plan.open.universe, "resolvedInputs").clone();
    put(&mut resolved, "dependencySourceSetId", t(&dep_id));
    put(&mut plan.open.universe, "resolvedInputs", resolved);
    plan.universes[0].value = plan.open.universe.clone();
    let source = super::super::super::super::built_commitment(
        "opensip.rust-provider.universe.v2",
        &plan.open.universe,
    );
    plan.stages[0].scopes[0].source = source.clone();
    plan.stages[0].scopes[0].target = source;
    Request::build(plan).unwrap()
}
fn advance(s: &mut Sender, z: &mut Zeros, n: usize) {
    for _ in 0..n {
        s.send_next(z).unwrap();
    }
}
fn until(s: &mut Sender, z: &mut Zeros, name: &str) {
    while s.next_slot().unwrap().frame.name() != name {
        s.send_next(z).unwrap();
    }
}
fn finish(s: &mut Sender, z: &mut Zeros) -> Result<(), Refusal> {
    while !s.complete() {
        s.send_next(z)?;
    }
    Ok(())
}
fn altered(v: &Value) -> Value {
    let Value::Text(v) = v else { panic!() };
    let mut b = v.as_bytes().to_vec();
    let last = b.last_mut().unwrap();
    *last = if *last == b'0' { b'1' } else { b'0' };
    Value::Text(String::from_utf8(b).unwrap())
}
fn replacement(original: &Value, v: &J) -> Value {
    match v {
        J::String(s) if s == "$wrong-same-length" => altered(original),
        _ => wire(v),
    }
}
fn small_case(v: &J) {
    let input = jget(v, "input");
    let send = jget(input, "send");
    let p = jget(send, "plan");
    let transcript = jget(send, "transcript");
    let kind = str_(jget(transcript, "kind"));
    let id = str_(jget(v, "id"));
    let accept = str_(jget(v, "kind")) == "accept";
    if kind == "alternate-split" {
        // Historical test override24 is not a currently admissible Hello.
        // Exercise the actual production greedy constructor at that numeric
        // predicate, without weakening or bypassing handshake admission.
        let mut policy = policy::Policy::load().unwrap();
        let override_value = num(jget(
            jget(p, "limitsOverride"),
            "maxDependencySourceChunkBytes",
        ));
        assert_eq!(override_value, 24);
        policy
            .limits
            .insert("maxDependencySourceChunkBytes".into(), override_value);
        let group = &arr(jget(p, "dependency"))[0];
        let entry = Value::Map(vec![
            ("packageKey".into(), t(str_(jget(group, "packageKey")))),
            (
                "path".into(),
                t(&"d".repeat(num(jget(group, "pathScalars")) as usize)),
            ),
            (
                "byteLength".into(),
                Value::Unsigned(num(jget(group, "byteLength"))),
            ),
            ("contentSha256".into(), t(&"1".repeat(64))),
        ]);
        let sizes = arr(jget(transcript, "sizes"));
        assert_eq!(
            sizes.iter().map(num).sum::<u64>(),
            num(jget(group, "byteLength"))
        );
        let set_id = format!("sha256:{}", "a".repeat(64));
        assert!(
            dependency::chunk(
                &policy,
                &set_id,
                &entry,
                0,
                0,
                vec![0; override_value as usize]
            )
            .is_ok()
        );
        assert!(matches!(
            dependency::chunk(
                &policy,
                &set_id,
                &entry,
                0,
                0,
                vec![0; num(&sizes[0]) as usize]
            ),
            Err(dependency::Refusal::Join("dependency greedy chunk length"))
        ));
        assert!(!accept);
        return;
    }
    let mut s = Sender::new(request(p)).unwrap();
    let mut z = Zeros::default();
    let mut complete_expected = None;
    if let J::Object(send) = send
        && let Some(J::Object(o)) = send.get("consumeLimitsOverride")
    {
        for (k, v) in o {
            s.request.policy.limits.insert(k.clone(), num(v));
        }
    }
    let result: Result<(), Refusal> = match kind {
        "canonical" => finish(&mut s, &mut z),
        "cancel-after" | "cancel-at" => {
            let J::Integer(n) = jget(transcript, "frames") else {
                panic!()
            };
            let n = if n.get() == -1 {
                s.request.schedule.slots.len()
            } else {
                usize::try_from(n.get()).unwrap()
            };
            advance(&mut s, &mut z, n);
            let mut payload = s.cancel_payload().unwrap_or_else(|| {
                Value::Map(vec![
                    ("executionId".into(), Value::Null),
                    ("analysisOrdinal".into(), Value::Null),
                    ("reason".into(), t("user-interrupt")),
                ])
            });
            if let J::Object(tr) = transcript
                && let Some(J::Object(overrides)) = tr.get("override")
            {
                for (k, v) in overrides {
                    let original = if k == "executionId" {
                        t(&s.request.plan.open.execution_id)
                    } else {
                        Value::Unsigned(s.request.plan.analysis_ordinal)
                    };
                    let value = if v == &js("$planned") {
                        original.clone()
                    } else {
                        replacement(&original, v)
                    };
                    put(&mut payload, k, value);
                }
            }
            s.admit_cancel(s.sequence, payload).map(|_| ())
        }
        "truncate" => {
            advance(&mut s, &mut z, num(jget(transcript, "frames")) as usize);
            complete_expected = Some(false);
            Ok(())
        }
        "extra-frame" => {
            finish(&mut s, &mut z).unwrap();
            s.send_next(&mut z).map(|_| ())
        }
        "second-cancel" => {
            advance(&mut s, &mut z, 3);
            s.cancel().unwrap();
            s.cancel().map(|_| ())
        }
        "cancel-over-reserve" => {
            advance(&mut s, &mut z, 3);
            let mut payload = s.cancel_payload().unwrap();
            put(
                &mut payload,
                "executionId",
                t(&(s.request.plan.open.execution_id.clone() + "x")),
            );
            s.admit_cancel(s.sequence, payload).map(|_| ())
        }
        "sequence-gap" => {
            advance(&mut s, &mut z, 2);
            let (frame, payload) = s.realize_next(&mut z).unwrap();
            s.admit(frame, s.sequence + 1, payload).map(|_| ())
        }
        "sequence-boolean-zero" => {
            let (frame, payload) = s.realize_next(&mut z).unwrap();
            let mut envelope = schedule::envelope(0, frame.name(), payload);
            put(&mut envelope, "sequence", Value::Bool(false));
            check_envelope(&envelope, 0, frame.name())
        }
        "reorder" => {
            let (_, _) = s.realize_next(&mut z).unwrap();
            let open = s.fresh.fixed[&Frame::OpenUniverse].clone();
            s.admit(Frame::OpenUniverse, 0, open).map(|_| ())
        }
        "substitute"
        | "payload-bytes"
        | "payload-bytes-chunk"
        | "seal-count"
        | "materialized-flip"
        | "alternate-chunking"
        | "alternate-split" => {
            let target = match kind {
                "payload-bytes" => "OpenUniverse",
                "payload-bytes-chunk" | "alternate-chunking" => "SnapshotFileChunk",
                "seal-count" => "SnapshotSeal",
                _ => str_(jget(transcript, "frameType")),
            };
            until(&mut s, &mut z, target);
            let (frame, mut payload) = s.realize_next(&mut z).unwrap();
            match kind {
                "substitute" => {
                    let key = str_(jget(transcript, "field"));
                    let val = replacement(vget(&payload, key), jget(transcript, "value"));
                    put(&mut payload, key, val);
                }
                "payload-bytes" => put(
                    &mut payload,
                    "executionId",
                    t(&(s.request.plan.open.execution_id.clone() + "x")),
                ),
                "payload-bytes-chunk" => put(
                    &mut payload,
                    "snapshotId",
                    t(&(s.request.plan.open.snapshot_id.clone() + "0")),
                ),
                "seal-count" => {
                    let Value::Unsigned(n) = vget(&payload, "totalChunkCount") else {
                        panic!()
                    };
                    let n = *n + 1;
                    put(&mut payload, "totalChunkCount", Value::Unsigned(n));
                }
                "materialized-flip" => {
                    let Value::Bytes(b) = vget(&payload, "bytes") else {
                        panic!()
                    };
                    let mut b = b.clone();
                    b[0] ^= 1;
                    put(&mut payload, "bytes", Value::Bytes(b));
                }
                "alternate-chunking" | "alternate-split" => {
                    let Value::Bytes(b) = vget(&payload, "bytes") else {
                        panic!()
                    };
                    let n = if kind == "alternate-split" {
                        num(&arr(jget(transcript, "sizes"))[0]) as usize
                    } else {
                        b.len() / 2
                    };
                    let b = b[..n].to_vec();
                    put(&mut payload, "bytes", Value::Bytes(b));
                }
                _ => unreachable!(),
            }
            s.admit(frame, s.sequence, payload).map(|_| ())
        }
        _ => panic!("unclassified {id}: {kind}"),
    };
    assert_eq!(result.is_ok(), accept, "{id}: {result:?}");
    if let Some(want) = complete_expected {
        assert_eq!(s.complete(), want, "{id}");
    }
    if let J::Object(input) = input {
        if let Some(J::Bool(want)) = input.get("expectComplete") {
            assert_eq!(s.complete(), *want, "{id}");
        }
        if input.contains_key("expectMatchesPlan") {
            assert!(s.complete(), "{id}");
        }
        if let Some(n) = input.get("expectContentVerifiedEntries") {
            assert_eq!(z.reads.len() as u64, num(n), "{id}");
        }
    }
    if result.is_err() {
        assert!(
            s.send_next(&mut z).is_err(),
            "{id} refusal must latch or no independent realization remain"
        );
    }
}
#[test]
fn replay_trial07_small_rust_send_cases_through_actual_independent_sender() {
    assert_eq!(
        digest_hex(&raw_sha256(CORPUS)),
        "79d0ee27533f3c4a5ac2c3f90db9423412304a7148aeaec41582c892f56dc9ae"
    );
    let doc = parse_json(CORPUS).unwrap();
    let mut count = 0;
    for v in arr(jget(jget(&doc, "vectors"), "HOST-SEND-SCHEDULE")) {
        let p = jget(jget(jget(v, "input"), "send"), "plan");
        if str_(jget(p, "protocol")) != "rust-semantic" {
            continue;
        }
        if arr(jget(p, "snapshot"))
            .iter()
            .any(|g| num(jget(g, "byteLength")) > 30)
        {
            continue;
        }
        small_case(v);
        count += 1;
    }
    assert_eq!(count, 40);
}
#[test]
fn replay_trial07_symbolic_gibibyte_send_cases_use_actual_charging_and_greedy_chunk_guards() {
    assert_eq!(
        digest_hex(&raw_sha256(FX)),
        "cb582ebec92077800b288e39092b8e5205c3de54bc13cc736165c44761e0bd15"
    );
    let doc = parse_json(CORPUS).unwrap();
    let fixtures = parse_json(FX).unwrap();
    let fixtures = jget(&fixtures, "fixtures");
    let policy = policy::Policy::load().unwrap();
    let mut count = 0;
    for v in arr(jget(jget(&doc, "vectors"), "HOST-SEND-SCHEDULE")) {
        let send = jget(jget(v, "input"), "send");
        let p = jget(send, "plan");
        if str_(jget(p, "protocol")) != "rust-semantic"
            || !arr(jget(p, "snapshot"))
                .iter()
                .any(|g| num(jget(g, "byteLength")) > 30)
        {
            continue;
        }
        let (schedule, _, _) = schedule::accounting_replay::model(fixtures, p, &policy);
        assert_eq!(schedule.totals.payload_bytes, 9_663_676_416);
        match str_(jget(jget(send, "transcript"), "kind")) {
            "cancel-at-end" => {
                let mut s = Sender::new(super::tests::request(false)).unwrap();
                s.request.schedule.cancel_reserve_bytes = schedule.cancel_reserve_bytes;
                for slot in &schedule.slots {
                    s.totals = s.charged(slot.payload_bytes, false).unwrap();
                }
                s.totals = s.charged(schedule.cancel_reserve_bytes, true).unwrap();
                assert_eq!(s.totals, schedule.totals);
                assert!(s.charged(1, true).is_err());
            }
            "alternate-chunking" => {
                let slot = schedule
                    .slots
                    .iter()
                    .enumerate()
                    .find(|(i, s)| {
                        s.frame == Frame::SnapshotFileChunk
                            && s.chunk.as_ref().unwrap().length >= 2
                            && !schedule.slots.get(i + 1).is_some_and(|next| {
                                next.frame == s.frame && next.chunk.as_ref().unwrap().index > 0
                            })
                    })
                    .unwrap()
                    .1;
                let chunk = slot.chunk.as_ref().unwrap();
                let Entry::Snapshot(path) = &chunk.entry else {
                    panic!()
                };
                let length = num(jget(&arr(jget(p, "snapshot"))[0], "byteLength"));
                let entry = snapshot::Entry::File {
                    path: path.clone(),
                    byte_length: length,
                    content_sha256: "1".repeat(64),
                    executable: false,
                };
                let open = jget(fixtures, "startupRustOpenUniverse");
                let split = vec![0; (chunk.length / 2) as usize];
                assert!(
                    snapshot::chunk(
                        &policy,
                        str_(jget(open, "snapshotId")),
                        &entry,
                        chunk.index,
                        chunk.offset,
                        split
                    )
                    .is_err()
                );
            }
            kind => panic!("unclassified symbolic transcript {kind}"),
        }
        count += 1;
    }
    assert_eq!(count, 2);
}

/// Trial07's positive two-fragment stream is lawful byte custody, but is not
/// a host greedy send schedule. Preserve the original fragment bytes, admit
/// their canonical host realization, and independently refuse the original
/// alternate split at the greedy constructor. Negative coordinates are fed
/// unchanged to that constructor; the digest negative reaches live custody.
#[test]
fn replay_trial07_original_chunk_custody_bytes_coordinates_empty_and_greedy_distinction() {
    struct Literal {
        path: String,
        bytes: Vec<u8>,
    }
    impl Source for Literal {
        fn read(&mut self, entry: &Entry, offset: u64, length: usize) -> std::io::Result<Vec<u8>> {
            match entry {
                Entry::Snapshot(path) if path == &self.path => self
                    .bytes
                    .get(offset as usize..offset as usize + length)
                    .map(|s| s.to_vec())
                    .ok_or_else(|| std::io::Error::other("literal interval")),
                _ => Err(std::io::Error::other("unexpected literal entry")),
            }
        }
    }
    fn bytes(v: &J) -> Vec<u8> {
        let raw = str_(jget(v, "$bytesHex"));
        assert!(raw.len().is_multiple_of(2));
        (0..raw.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&raw[i..i + 2], 16).unwrap())
            .collect()
    }
    let doc = parse_json(CORPUS).unwrap();
    let cases = arr(jget(jget(&doc, "vectors"), "CHUNK-CUSTODY"));
    assert_eq!(cases.len(), 4);
    let policy = policy::Policy::load().unwrap();
    for v in cases {
        let id = str_(jget(v, "id"));
        let input = jget(v, "input");
        let row = jget(input, "entry");
        let path = str_(jget(row, "path"));
        let length = num(jget(row, "byteLength"));
        let hash = str_(jget(row, "contentSha256"));
        let entry = snapshot::Entry::File {
            path: path.into(),
            byte_length: length,
            content_sha256: hash.into(),
            executable: false,
        };
        let chunks = arr(jget(input, "chunks"));
        let joined: Vec<u8> = chunks
            .iter()
            .flat_map(|c| bytes(jget(c, "bytes")))
            .collect();
        if id == "chunks-gap-offset" || id == "chunks-for-empty-entry" {
            let chunk = if id == "chunks-gap-offset" {
                &chunks[1]
            } else {
                &chunks[0]
            };
            assert!(
                matches!(
                    snapshot::chunk(
                        &policy,
                        &format!("snapshot2:{}", "a".repeat(64)),
                        &entry,
                        num(jget(chunk, "chunkIndex")),
                        num(jget(chunk, "byteOffset")),
                        bytes(jget(chunk, "bytes"))
                    ),
                    Err(snapshot::Refusal::Join("snapshot chunk coordinates"))
                ),
                "{id}"
            );
            continue;
        }
        let mut plan = super::super::request::tests::plan(false, false);
        plan.snapshot = vec![
            snapshot::Entry::File {
                path: path.into(),
                byte_length: length,
                content_sha256: hash.into(),
                executable: false,
            },
            snapshot::Entry::File {
                path: "src/z.rs".into(),
                byte_length: 1,
                content_sha256: digest_hex(&raw_sha256(b"z")),
                executable: false,
            },
        ];
        let mut sender = Sender::new(Request::build(plan).unwrap()).unwrap();
        let mut source = Literal {
            path: path.into(),
            bytes: joined.clone(),
        };
        for _ in 0..3 {
            sender.send_next(&mut source).unwrap();
        }
        let result = sender.send_next(&mut source);
        if id == "chunks-wrong-bytes" {
            assert!(
                matches!(result, Err(Refusal::Source(_))),
                "{id}: {result:?}"
            );
            assert_eq!(sender.slot, 3);
            assert_eq!(sender.send_next(&mut source), Err(Refusal::AfterRefusal));
        } else {
            assert_eq!(id, "chunks-two");
            let sent = result.unwrap();
            let envelope = cbor::decode(
                &sent.bytes[FRAME_PREFIX_BYTES..],
                cbor::Profile::Rust3,
                super::super::super::RUST3_FRAME_MAX_DEPTH,
            )
            .unwrap();
            assert_eq!(
                vget(vget(&envelope, "payload"), "bytes"),
                &Value::Bytes(joined)
            );
            assert_eq!(sender.counts[0], 1);
            let first = &chunks[0];
            assert!(matches!(
                snapshot::chunk(
                    &policy,
                    &sender.request.plan.open.snapshot_id,
                    &entry,
                    num(jget(first, "chunkIndex")),
                    num(jget(first, "byteOffset")),
                    bytes(jget(first, "bytes"))
                ),
                Err(snapshot::Refusal::Join("snapshot greedy chunk length"))
            ));
        }
    }
}
