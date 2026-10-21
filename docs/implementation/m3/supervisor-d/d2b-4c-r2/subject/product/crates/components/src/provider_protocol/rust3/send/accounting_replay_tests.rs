//! Exact historical trial07 accounting through the production Recorder,
//! envelope sizers and shared manifest cardinality predicate. Duplicate
//! symbolic paths, placeholder digests and the empty Analyze are intentional
//! original inputs. This proves no C4, schema or analysis-domain admission.
use super::super::policy::Policy;
use super::*;
use opensip_identity::{JsonValue as J, digest_hex, parse_json};
use std::collections::BTreeMap;
const CORPUS: &[u8] = include_bytes!("../../../../tests/data/trial07-integer-replay.v1.json");
const FIXTURE: &[u8] = include_bytes!("../../../../tests/data/trial07-accounting-fixtures.v1.json");
fn jget<'a>(v: &'a J, k: &str) -> &'a J {
    let J::Object(m) = v else {
        panic!("object {k}")
    };
    m.get(k).unwrap()
}
fn array(v: &J) -> &[J] {
    let J::Array(v) = v else { panic!("array") };
    v
}
fn text(v: &J) -> &str {
    let J::String(v) = v else { panic!("string") };
    v
}
fn number(v: &J) -> u64 {
    let J::Integer(v) = v else { panic!("integer") };
    u64::try_from(v.get()).unwrap()
}
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn m(v: Vec<(&str, Value)>) -> Value {
    Value::Map(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn get<'a>(v: &'a Value, k: &str) -> &'a Value {
    let Value::Map(v) = v else { panic!() };
    &v.iter().find(|(s, _)| s == k).unwrap().1
}
fn put(v: &mut Value, k: &str, new: Value) {
    let Value::Map(v) = v else { panic!() };
    v.iter_mut().find(|(s, _)| s == k).unwrap().1 = new;
}
fn wire(v: &J) -> Value {
    match v {
        J::Null => Value::Null,
        J::Bool(v) => Value::Bool(*v),
        J::Integer(_) => Value::Unsigned(number(v)),
        J::String(v) => t(v),
        J::Array(v) => Value::Array(v.iter().map(wire).collect()),
        J::Object(v) => Value::Map(v.iter().map(|(k, v)| (k.clone(), wire(v))).collect()),
    }
}
fn count(groups: &J) -> u64 {
    array(groups).iter().map(|g| number(jget(g, "n"))).sum()
}
fn groups(v: &J, snapshot: bool) -> Vec<Value> {
    let mut result = Vec::new();
    for g in array(v) {
        let mut e = m(vec![
            (
                "path",
                t(&if snapshot { "s" } else { "d" }
                    .repeat(number(jget(g, "pathScalars")) as usize)),
            ),
            ("byteLength", Value::Unsigned(number(jget(g, "byteLength")))),
            ("contentSha256", t(&"1".repeat(64))),
        ]);
        let Value::Map(ref mut fields) = e else {
            panic!()
        };
        if snapshot {
            fields.extend([
                ("kind".into(), t("file")),
                ("executable".into(), Value::Bool(false)),
                ("targetBytes".into(), Value::Null),
            ]);
        } else {
            fields.push(("packageKey".into(), t(text(jget(g, "packageKey")))));
        }
        result.extend(std::iter::repeat_n(e, number(jget(g, "n")) as usize));
    }
    result
}
fn prepared_entries(fx: &J, p: &J) -> Vec<Value> {
    let base = wire(&array(jget(jget(fx, "prepInert"), "rows"))[0]);
    let config = Value::Array(
        (0..number(jget(p, "configurationCount")))
            .map(|i| t(&format!("c{i:0255}")))
            .collect(),
    );
    let length = Value::Unsigned(number(jget(p, "blobByteLength")));
    (0..number(jget(p, "n")))
        .map(|i| {
            let mut row = base.clone();
            put(&mut row, "configuration", config.clone());
            let mut site = get(&row, "site").clone();
            put(&mut site, "startByte", Value::Unsigned(i));
            put(&mut site, "endByte", Value::Unsigned(i + 1));
            put(&mut row, "site", site);
            let mut blob = get(&row, "blob").clone();
            put(&mut blob, "byteLength", length.clone());
            let sha = get(&blob, "sha256").clone();
            put(&mut row, "blob", blob);
            let Value::Text(ref hex) = sha else { panic!() };
            m(vec![
                ("outputOrdinal", Value::Unsigned(i)),
                ("kind", get(&row, "kind").clone()),
                ("planRow", row),
                (
                    "logicalPath",
                    t(&format!(".opensip/prepared/v3/{i}-{hex}.blob")),
                ),
                ("blobByteLength", length.clone()),
                ("blobSha256", sha.clone()),
                ("contentByteLength", length.clone()),
                ("contentSha256", sha),
            ])
        })
        .collect()
}
struct Manifest {
    frame: Frame,
    chunk: Frame,
    seal: Frame,
    id_key: &'static str,
    total_key: &'static str,
    id: Value,
    entries: Vec<Value>,
    maximum: u64,
}
impl Manifest {
    fn length(e: &Value) -> u64 {
        match get(e, "byteLength") {
            Value::Unsigned(n) => *n,
            _ => panic!(),
        }
    }
    fn entry_length(&self, e: &Value) -> u64 {
        if self.frame == Frame::PreparedOutputManifest {
            match get(e, "blobByteLength") {
                Value::Unsigned(n) => *n,
                _ => panic!(),
            }
        } else {
            Self::length(e)
        }
    }
    fn chunks(&self) -> u64 {
        self.entries
            .iter()
            .map(|e| chunk_count(self.entry_length(e), self.maximum).unwrap())
            .sum()
    }
    fn record(
        self,
        rec: &mut Recorder,
        seals: &mut BTreeMap<String, Value>,
    ) -> Result<(), Refusal> {
        let sha = t(&"0".repeat(64));
        let bytes = self.entries.iter().map(|e| self.entry_length(e)).sum();
        let chunks = self.chunks();
        let seal = m(vec![
            (self.id_key, self.id.clone()),
            ("manifestSha256", sha.clone()),
            ("entryCount", Value::Unsigned(self.entries.len() as u64)),
            (self.total_key, Value::Unsigned(bytes)),
            ("totalChunkCount", Value::Unsigned(chunks)),
        ]);
        let manifest = m(vec![
            (self.id_key, self.id.clone()),
            ("manifestSha256", sha),
            ("entries", Value::Array(self.entries.clone())),
        ]);
        rec.fixed(self.frame, &manifest, None)?;
        for e in &self.entries {
            let length = self.entry_length(e);
            let (entry, mut fields) = match self.chunk {
                Frame::SnapshotFileChunk => (
                    Entry::Snapshot(match get(e, "path") {
                        Value::Text(s) => s.clone(),
                        _ => panic!(),
                    }),
                    vec![("path", get(e, "path").clone())],
                ),
                Frame::DependencySourceChunk => (
                    Entry::Dependency {
                        package_key: match get(e, "packageKey") {
                            Value::Text(s) => s.clone(),
                            _ => panic!(),
                        },
                        path: match get(e, "path") {
                            Value::Text(s) => s.clone(),
                            _ => panic!(),
                        },
                    },
                    vec![
                        ("packageKey", get(e, "packageKey").clone()),
                        ("path", get(e, "path").clone()),
                    ],
                ),
                Frame::PreparedOutputChunk => (
                    Entry::Prepared(match get(e, "outputOrdinal") {
                        Value::Unsigned(n) => *n,
                        _ => panic!(),
                    }),
                    vec![("outputOrdinal", get(e, "outputOrdinal").clone())],
                ),
                _ => panic!(),
            };
            fields.push((self.id_key, self.id.clone()));
            let n = chunk_count(length, self.maximum)?;
            for i in 0..n {
                let offset = i * self.maximum;
                let size = (length - offset).min(self.maximum);
                let mut header = fields.clone();
                header.extend([
                    ("chunkIndex", Value::Unsigned(i)),
                    ("byteOffset", Value::Unsigned(offset)),
                ]);
                let digest = if i + 1 == n {
                    Some(match get(e, "contentSha256") {
                        Value::Text(s) => s.as_str(),
                        _ => panic!(),
                    })
                } else {
                    None
                };
                rec.chunk(
                    self.chunk,
                    &m(header),
                    &Chunk {
                        entry: entry.clone(),
                        index: i,
                        offset,
                        length: size,
                    },
                    digest,
                )?;
            }
        }
        seals.insert(self.seal.name().into(), seal.clone());
        rec.fixed(self.seal, &seal, Some(chunks))
    }
}
pub(in crate::provider_protocol::rust3::send) fn model(
    fx: &J,
    p: &J,
    policy: &Policy,
) -> (Schedule, BTreeMap<String, Value>, BTreeMap<String, u64>) {
    let prepared = if let J::Object(p) = p {
        p.get("prepared")
    } else {
        panic!()
    };
    let open = wire(jget(
        fx,
        if prepared.is_some() {
            "startupRustOpenUniversePrepared"
        } else {
            "startupRustOpenUniverse"
        },
    ));
    let hello = wire(jget(fx, "wireRustHello"));
    let snap = Manifest {
        frame: Frame::SnapshotManifest,
        chunk: Frame::SnapshotFileChunk,
        seal: Frame::SnapshotSeal,
        id_key: "snapshotId",
        total_key: "totalFileBytes",
        id: get(&open, "snapshotId").clone(),
        entries: groups(jget(p, "snapshot"), true),
        maximum: policy.limit("maxSnapshotChunkBytes").unwrap(),
    };
    let dep = Manifest {
        frame: Frame::DependencySourceManifest,
        chunk: Frame::DependencySourceChunk,
        seal: Frame::DependencySourceSeal,
        id_key: "dependencySourceSetId",
        total_key: "totalBytes",
        id: get(get(&open, "repositoryResolution"), "dependencySourceSetId").clone(),
        entries: groups(jget(p, "dependency"), false),
        maximum: policy.limit("maxDependencySourceChunkBytes").unwrap(),
    };
    let prep = prepared.map(|p| Manifest {
        frame: Frame::PreparedOutputManifest,
        chunk: Frame::PreparedOutputChunk,
        seal: Frame::PreparedOutputSeal,
        id_key: "planId",
        total_key: "totalBlobBytes",
        id: get(&open, "planId").clone(),
        entries: prepared_entries(fx, p),
        maximum: policy.limit("maxPreparedOutputChunkBytes").unwrap(),
    });
    let expected = 7 + snap.chunks() + dep.chunks() + prep.as_ref().map_or(0, |p| 2 + p.chunks());
    let cancel = m(vec![
        ("executionId", get(&open, "executionId").clone()),
        ("analysisOrdinal", Value::Unsigned(0)),
        ("reason", t("user-interrupt")),
    ]);
    let reserve = envelope_length(expected, "Cancel", &cancel).unwrap();
    // Measurement run lifts only test bounds, then recharges exactly these
    // measured slots through the same production guards at the real limits.
    let mut rec = Recorder::new(
        Bounds {
            frame_bytes: u64::MAX,
            payload_bytes: u64::MAX,
            frames: u64::MAX,
        },
        expected,
        reserve,
    )
    .unwrap();
    rec.fixed(Frame::Hello, &hello, None).unwrap();
    rec.fixed(Frame::OpenUniverse, &open, None).unwrap();
    let mut seals = BTreeMap::new();
    snap.record(&mut rec, &mut seals).unwrap();
    dep.record(&mut rec, &mut seals).unwrap();
    if let Some(prep) = prep {
        prep.record(&mut rec, &mut seals).unwrap();
    }
    let analyze = m(vec![
        ("analysisOrdinal", Value::Unsigned(0)),
        ("executionId", get(&open, "executionId").clone()),
        ("snapshotId", get(&open, "snapshotId").clone()),
        ("planId", get(&open, "planId").clone()),
        ("stages", Value::Array(vec![])),
    ]);
    rec.fixed(Frame::Analyze, &analyze, None).unwrap();
    let schedule = rec.finish().unwrap();
    let mut largest = BTreeMap::from([("Cancel".into(), reserve)]);
    for s in &schedule.slots {
        let max = largest.entry(s.frame.name().into()).or_insert(0);
        *max = (*max).max(s.payload_bytes);
    }
    (schedule, seals, largest)
}
fn charge(schedule: &Schedule, bounds: Bounds) -> Result<(), Refusal> {
    let mut rec = Recorder::new(
        bounds,
        schedule.slots.len() as u64,
        schedule.cancel_reserve_bytes,
    )?;
    for slot in &schedule.slots {
        let totals = rec.next_totals(slot.payload_bytes)?;
        rec.schedule.slots.push(slot.clone());
        rec.schedule.totals = totals;
    }
    rec.finish().map(|_| ())
}
#[test]
fn replay_trial07_all_rust_request_accounting_exact_boundaries_and_original_quantities() {
    assert_eq!(
        digest_hex(&raw_sha256(CORPUS)),
        "79d0ee27533f3c4a5ac2c3f90db9423412304a7148aeaec41582c892f56dc9ae"
    );
    assert_eq!(
        digest_hex(&raw_sha256(FIXTURE)),
        "cb582ebec92077800b288e39092b8e5205c3de54bc13cc736165c44761e0bd15"
    );
    let d = parse_json(CORPUS).unwrap();
    let fx = parse_json(FIXTURE).unwrap();
    let fx = jget(&fx, "fixtures");
    let mut total = 0;
    for v in array(jget(jget(&d, "vectors"), "REQUEST-WIRE-ACCOUNTING")) {
        let p = jget(jget(v, "input"), "plan");
        if text(jget(p, "protocol")) != "rust-semantic" {
            continue;
        }
        let id = text(jget(v, "id"));
        let accept = text(jget(v, "kind")) == "accept";
        let mut policy = Policy::load().unwrap();
        let J::Object(pfields) = p else { panic!() };
        if let Some(J::Object(overrides)) = pfields.get("limitsOverride") {
            for (k, v) in overrides {
                assert!(policy.limits.contains_key(k));
                policy.limits.insert(k.clone(), number(v));
            }
        }
        let entry_fit = policy
            .entries_fit("maxSnapshotEntries", count(jget(p, "snapshot")))
            .unwrap()
            && policy
                .entries_fit("maxDependencySourceEntries", count(jget(p, "dependency")))
                .unwrap()
            && pfields.get("prepared").is_none_or(|p| {
                policy
                    .entries_fit("maxPreparedOutputEntries", number(jget(p, "n")))
                    .unwrap()
            });
        if !entry_fit {
            assert!(!accept, "{id}");
            assert!(text(jget(v, "expect")).contains(":entries:"), "{id}");
            total += 1;
            continue;
        }
        let (schedule, seals, largest) = model(fx, p, &policy);
        if let Some(n) = pfields.get("expectFrames") {
            assert_eq!(schedule.totals.frames, number(n), "{id}");
        }
        if let Some(n) = pfields.get("expectPayloadBytes") {
            assert_eq!(schedule.totals.payload_bytes, number(n), "{id}");
        }
        if let Some(J::Object(want)) = pfields.get("expectLargestFrame") {
            for (k, n) in want {
                assert_eq!(largest[k], number(n), "{id} {k}");
            }
        }
        if let Some(J::Object(want)) = pfields.get("expectSeals") {
            for (k, row) in want {
                let J::Object(fields) = row else { panic!() };
                for (field, n) in fields {
                    assert_eq!(
                        get(&seals[k], field),
                        &Value::Unsigned(number(n)),
                        "{id} {k} {field}"
                    );
                }
            }
        }
        let result = charge(
            &schedule,
            Bounds {
                frame_bytes: policy.limit("maxFramePayloadBytes").unwrap(),
                payload_bytes: policy.limit("maxRequestPayloadBytesTotal").unwrap(),
                frames: policy.limit("maxRequestFrames").unwrap(),
            },
        );
        assert_eq!(result.is_ok(), accept, "{id}: {result:?}");
        if let Err(e) = result {
            let expect = text(jget(v, "expect"));
            match e {
                Refusal::FrameLimit { .. } => assert!(expect.contains(":frame:"), "{id}"),
                Refusal::PayloadLimit => assert!(expect.ends_with(":request-bytes"), "{id}"),
                Refusal::FrameCountLimit => assert!(expect.ends_with(":request-frames"), "{id}"),
                _ => panic!("{id}: {e:?}"),
            }
        }
        total += 1;
    }
    assert_eq!(total, 20);
}
