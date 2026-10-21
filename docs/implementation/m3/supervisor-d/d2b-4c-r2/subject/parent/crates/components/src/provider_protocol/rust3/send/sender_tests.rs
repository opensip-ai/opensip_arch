//! Inert complete sender transcripts with a bounded fake custody source.
//! These establish no production authority, subprocess or worker admission.
use super::*;
use opensip_identity::{JsonValue as J, hash_canonical_value};
fn vf_mut<'a>(v: &'a mut Value, k: &str) -> &'a mut Value {
    let Value::Map(v) = v else { panic!() };
    &mut v.iter_mut().find(|(key, _)| key == k).unwrap().1
}
fn jf_mut<'a>(v: &'a mut J, k: &str) -> &'a mut J {
    let J::Object(v) = v else { panic!() };
    v.get_mut(k).unwrap()
}
fn id(domain: &str, v: &J) -> String {
    format!(
        "sha256:{}",
        digest_hex(&hash_canonical_value(domain, v).unwrap())
    )
}
fn sha(byte: u8, length: usize) -> String {
    digest_hex(&raw_sha256(&vec![byte; length]))
}
pub(in crate::provider_protocol::rust3::send) fn request(prep: bool) -> Request {
    let mut p = super::super::request::tests::plan(true, prep);
    for e in &mut p.snapshot {
        if let snapshot::Entry::File {
            byte_length,
            content_sha256,
            ..
        } = e
        {
            *content_sha256 = sha(0x11, *byte_length as usize);
        }
    }
    let (_, mut manifest) = p.dependency_manifests.pop_first().unwrap();
    let J::Array(rows) = &mut manifest else {
        panic!()
    };
    *jf_mut(&mut rows[0], "contentSha256") = J::String(sha(0x22, 3));
    let digest =
        digest_hex(&hash_canonical_value("native.dependency-file-manifest.v1", &manifest).unwrap());
    p.dependency_manifests.insert(digest.clone(), manifest);
    let J::Array(packages) = jf_mut(&mut p.dependency_set, "packages") else {
        panic!()
    };
    *jf_mut(&mut packages[0], "fileManifestSha256") = J::String(digest);
    let dep_id = id("native.dependency-source-set.v1", &p.dependency_set);
    *vf_mut(&mut p.open.repository_resolution, "dependencySourceSetId") = t(&dep_id);
    let mut resolved = field(&p.open.universe, "resolvedInputs").unwrap().clone();
    *vf_mut(&mut resolved, "dependencySourceSetId") = t(&dep_id);
    if let Some(set) = &mut p.prepared_set {
        let J::Array(rows) = jf_mut(set, "rows") else {
            panic!()
        };
        *jf_mut(
            jf_mut(&mut rows[0], "inputBinding"),
            "dependencySourceSetId",
        ) = J::String(dep_id);
        *jf_mut(jf_mut(&mut rows[0], "blob"), "sha256") = J::String(sha(0x33, 1_048_577));
        let set_id = id("native.prepared-output-set.v3", set);
        *vf_mut(&mut resolved, "preparedOutputSetId") = t(&set_id);
        *vf_mut(&mut p.open.repository_resolution, "preparedOutputSetId") = t(&set_id);
    }
    *vf_mut(&mut p.open.universe, "resolvedInputs") = resolved;
    p.universes[0].value = p.open.universe.clone();
    let source = super::super::super::super::built_commitment(
        "opensip.rust-provider.universe.v2",
        &p.open.universe,
    );
    p.stages[0].scopes[0].source = source.clone();
    p.stages[0].scopes[0].target = source;
    Request::build(p).unwrap()
}
#[derive(Default)]
struct Fake {
    reads: Vec<(Entry, u64, usize)>,
    corrupt: Option<usize>,
    short: bool,
    error: bool,
}
impl Source for Fake {
    fn read(&mut self, entry: &Entry, offset: u64, length: usize) -> std::io::Result<Vec<u8>> {
        self.reads.push((entry.clone(), offset, length));
        if self.error {
            return Err(std::io::Error::other("fake custody failure"));
        }
        let byte = match entry {
            Entry::Snapshot(path) if path == "src/a.rs" => 0x11,
            Entry::Dependency { package_key, path }
                if package_key == "a 1 source with spaces" && path == "src/lib.rs" =>
            {
                0x22
            }
            Entry::Prepared(0) => 0x33,
            _ => return Err(std::io::Error::other("unexpected source identity")),
        };
        let mut bytes = vec![byte; length];
        if self.corrupt == Some(self.reads.len()) {
            bytes[0] ^= 1;
        }
        if self.short {
            bytes.pop();
        }
        Ok(bytes)
    }
}
fn decode(sent: &Sent) -> Value {
    cbor::decode(
        &sent.bytes[FRAME_PREFIX_BYTES..],
        cbor::Profile::Rust3,
        super::super::super::RUST3_FRAME_MAX_DEPTH,
    )
    .unwrap()
}
fn through_manifest(sender: &mut Sender, source: &mut Fake) {
    for _ in 0..3 {
        sender.send_next(source).unwrap();
    }
}

#[test]
fn sender_independently_realizes_complete_greedy_transcripts_and_source_hashes() {
    for prep in [false, true] {
        let request = request(prep);
        let expected = request.schedule.clone();
        let mut sender = Sender::new(request).unwrap();
        let mut source = Fake::default();
        let mut total = 0;
        for (index, slot) in expected.slots.iter().enumerate() {
            assert_eq!(sender.next_slot().unwrap().sequence, index as u64);
            let sent = sender.send_next(&mut source).unwrap();
            assert_eq!(sent.frame, host_frame(slot.frame));
            let value = decode(&sent);
            assert_eq!(field(&value, "protocolMajor").unwrap(), &Value::Unsigned(3));
            assert_eq!(field(&value, "direction").unwrap(), &t("host-to-worker"));
            assert_eq!(field(&value, "frameType").unwrap(), &t(slot.frame.name()));
            assert_eq!(
                number(field(&value, "sequence").unwrap()).unwrap(),
                index as u64
            );
            assert_eq!(
                (sent.bytes.len() - FRAME_PREFIX_BYTES) as u64,
                slot.payload_bytes
            );
            total += slot.payload_bytes;
        }
        assert!(sender.complete());
        assert!(sender.hello_sent());
        assert!(!sender.cancelled());
        assert_eq!(source.reads.len(), if prep { 5 } else { 3 });
        assert_eq!(
            source.reads[0],
            (Entry::Snapshot("src/a.rs".into()), 0, 1_048_576)
        );
        assert_eq!(
            source.reads[1],
            (Entry::Snapshot("src/a.rs".into()), 1_048_576, 1)
        );
        assert_eq!(sender.totals.payload_bytes, total);
        assert_eq!(
            total + expected.cancel_reserve_bytes,
            expected.totals.payload_bytes
        );
        assert_eq!(sender.request().plan.analysis_ordinal, u64::MAX);
        let cancel = sender.cancel().unwrap();
        assert_eq!(
            cancel.frame,
            Rust3HostFrame::Cancel {
                execution_id: Some("execution".into()),
                analysis_ordinal: Some(u64::MAX)
            }
        );
        assert_eq!(
            number(field(&decode(&cancel), "sequence").unwrap()).unwrap(),
            expected.slots.len() as u64
        );
        assert!(sender.cancelled());
        assert!(sender.complete());
        let count = source.reads.len();
        assert!(sender.send_next(&mut source).is_err());
        assert_eq!(source.reads.len(), count);
        assert_eq!(sender.cancel(), Err(Refusal::AfterRefusal));
    }
}

#[test]
fn sender_cancel_is_once_after_hello_and_exact_typed_consumed_echo() {
    let mut sender = Sender::new(request(false)).unwrap();
    assert!(sender.cancel_payload().is_none());
    assert!(sender.cancel().is_err());
    for sent_slots in [1, 2] {
        let mut sender = Sender::new(request(false)).unwrap();
        let mut source = Fake::default();
        for _ in 0..sent_slots {
            sender.send_next(&mut source).unwrap();
        }
        let expected_execution = if sent_slots == 1 {
            Value::Null
        } else {
            t("execution")
        };
        let payload = sender.cancel_payload().unwrap();
        assert_eq!(field(&payload, "executionId").unwrap(), &expected_execution);
        assert_eq!(field(&payload, "analysisOrdinal").unwrap(), &Value::Null);
        assert_eq!(field(&payload, "reason").unwrap(), &t("user-interrupt"));
        sender.cancel().unwrap();
        assert!(source.reads.is_empty());
        assert!(sender.cancel().is_err());
    }
    let mut sender = Sender::new(request(false)).unwrap();
    let mut source = Fake::default();
    sender.send_next(&mut source).unwrap();
    let mut bad = sender.cancel_payload().unwrap();
    *vf_mut(&mut bad, "executionId") = t("execution");
    assert!(sender.admit_cancel(1, bad).is_err());
    assert_eq!(sender.cancel(), Err(Refusal::AfterRefusal));
    let mut sender = Sender::new(request(false)).unwrap();
    sender.send_next(&mut source).unwrap();
    let mut bad = sender.cancel_payload().unwrap();
    *vf_mut(&mut bad, "reason") = t("host-shutdown");
    assert!(sender.admit_cancel(1, bad).is_err());
}

#[test]
fn sender_slot_payload_sequence_and_lawful_alternative_chunking_diverge_before_sent_state() {
    let mut candidate = request(false);
    candidate.schedule.slots.swap(2, 3);
    let mut sender = Sender::new(candidate).unwrap();
    let mut source = Fake::default();
    sender.send_next(&mut source).unwrap();
    sender.send_next(&mut source).unwrap();
    assert!(sender.send_next(&mut source).is_err());
    assert_eq!(sender.slot, 2);
    assert!(source.reads.is_empty());
    let mut sender = Sender::new(request(false)).unwrap();
    let (frame, payload) = sender.realize_next(&mut source).unwrap();
    assert!(sender.admit(frame, 1, payload).is_err());
    assert_eq!(sender.slot, 0);
    let mut sender = Sender::new(request(false)).unwrap();
    through_manifest(&mut sender, &mut source);
    let (frame, mut payload) = sender.realize_next(&mut source).unwrap();
    let Value::Bytes(bytes) = vf_mut(&mut payload, "bytes") else {
        panic!()
    };
    bytes.truncate(524_288);
    assert!(sender.admit(frame, 3, payload).is_err());
    assert_eq!(sender.slot, 3);
    // A valid-shaped but different snapshot echo has the same encoded size;
    // only the planned header commitment may authorize this exact context.
    let mut sender = Sender::new(request(false)).unwrap();
    through_manifest(&mut sender, &mut source);
    let (frame, mut payload) = sender.realize_next(&mut source).unwrap();
    *vf_mut(&mut payload, "snapshotId") = t(&format!("snapshot2:{}", "0".repeat(64)));
    assert!(sender.admit(frame, 3, payload).is_err());
    assert_eq!(sender.slot, 3);
    let mut sender = Sender::new(request(false)).unwrap();
    let (frame, mut payload) = sender.realize_next(&mut source).unwrap();
    *vf_mut(vf_mut(&mut payload, "limits"), "maxScratchBytes") = Value::Unsigned(2_147_483_649);
    assert!(sender.admit(frame, 0, payload).is_err());
    assert_eq!(sender.slot, 0);
    let mut sender = Sender::new(request(false)).unwrap();
    sender.realize_next(&mut source).unwrap();
    let count = source.reads.len();
    assert!(sender.realize_next(&mut source).is_err());
    assert_eq!(source.reads.len(), count);
}

#[test]
fn sender_bad_source_counts_hashes_and_reads_latch_once_before_the_bad_frame() {
    for mode in 0..3 {
        let mut sender = Sender::new(request(true)).unwrap();
        let mut source = Fake {
            short: mode == 0,
            error: mode == 1,
            corrupt: if mode == 2 { Some(2) } else { None },
            ..Fake::default()
        };
        through_manifest(&mut sender, &mut source);
        if mode == 2 {
            sender.send_next(&mut source).unwrap();
        }
        assert!(matches!(
            sender.send_next(&mut source),
            Err(Refusal::Source(_))
        ));
        let count = source.reads.len();
        assert_eq!(sender.send_next(&mut source), Err(Refusal::AfterRefusal));
        assert_eq!(source.reads.len(), count);
    }
    for corrupt in 3..=5 {
        let mut sender = Sender::new(request(true)).unwrap();
        let mut source = Fake {
            corrupt: Some(corrupt),
            ..Fake::default()
        };
        let error = loop {
            match sender.send_next(&mut source) {
                Ok(_) => {}
                Err(e) => break e,
            }
        };
        assert!(matches!(error, Refusal::Source(_)));
        let count = source.reads.len();
        assert_eq!(sender.send_next(&mut source), Err(Refusal::AfterRefusal));
        assert_eq!(source.reads.len(), count);
    }
    let mut sender = Sender::new(request(false)).unwrap();
    sender.fresh.entries[0][1].sha256 = "a".repeat(64);
    let mut source = Fake::default();
    through_manifest(&mut sender, &mut source);
    sender.send_next(&mut source).unwrap();
    sender.send_next(&mut source).unwrap();
    assert!(matches!(
        sender.send_next(&mut source),
        Err(Refusal::Source(_))
    ));
}

#[test]
fn sender_final_digest_seals_and_defensive_request_counters_are_checked() {
    let mut candidate = request(false);
    candidate.schedule.slots[4].entry_content_sha256 = None;
    let mut sender = Sender::new(candidate).unwrap();
    let mut source = Fake::default();
    through_manifest(&mut sender, &mut source);
    sender.send_next(&mut source).unwrap();
    assert!(sender.send_next(&mut source).is_err());
    assert_eq!(sender.slot, 4);
    let mut candidate = request(false);
    candidate.schedule.slots[5].total_chunk_count = Some(3);
    let mut sender = Sender::new(candidate).unwrap();
    for _ in 0..5 {
        sender.send_next(&mut source).unwrap();
    }
    assert!(sender.send_next(&mut source).is_err());
    assert_eq!(sender.slot, 5);
    let mut candidate = request(false);
    candidate.schedule.totals.payload_bytes += 1;
    let mut sender = Sender::new(candidate).unwrap();
    let error = loop {
        match sender.send_next(&mut source) {
            Ok(_) => {}
            Err(e) => break e,
        }
    };
    assert!(
        matches!(error,Refusal::Divergence(ref s)if s.contains("final planned request totals"))
    );
    for key in [
        "maxFramePayloadBytes",
        "maxRequestPayloadBytesTotal",
        "maxRequestFrames",
    ] {
        let mut sender = Sender::new(request(false)).unwrap();
        sender.request.policy.limits.insert(key.into(), 0);
        assert!(sender.send_next(&mut source).is_err());
        assert_eq!(sender.slot, 0);
        assert_eq!(sender.totals.frames, 0);
    }
}

#[test]
fn sender_reference_requests_keep_v3_at_small_and_over_inline_subject_counts() {
    struct RefSource {
        paths: Vec<String>,
        reads: usize,
    }
    impl Source for RefSource {
        fn read(&mut self, entry: &Entry, offset: u64, length: usize) -> std::io::Result<Vec<u8>> {
            match entry {
                Entry::Snapshot(path)
                    if self.paths.contains(path) && offset == 0 && length == 1 =>
                {
                    self.reads += 1;
                    Ok(vec![0x11])
                }
                Entry::Dependency { package_key, path }
                    if package_key == "a 1 source with spaces"
                        && path == "src/lib.rs"
                        && offset == 0
                        && length == 3 =>
                {
                    self.reads += 1;
                    Ok(vec![0x22; 3])
                }
                _ => Err(std::io::Error::other("unexpected reference fixture source")),
            }
        }
    }
    for count in [1, 257] {
        let mut plan = request(false).plan;
        let paths: Vec<_> = (0..count).map(|i| format!("src/ref-{i:05}.rs")).collect();
        plan.snapshot = paths
            .iter()
            .map(|path| snapshot::Entry::File {
                path: path.clone(),
                byte_length: 1,
                content_sha256: sha(0x11, 1),
                executable: false,
            })
            .collect();
        plan.capabilities.push("subject-scope-reference-v1".into());
        plan.capabilities.sort();
        let mut sender = Sender::new(Request::build(plan).unwrap()).unwrap();
        let mut source = RefSource { paths, reads: 0 };
        let mut saw_analyze = false;
        while sender.next_slot().is_some() {
            let sent = sender.send_next(&mut source).unwrap();
            if sent.frame == Rust3HostFrame::Analyze {
                saw_analyze = true;
                let value = decode(&sent);
                let payload = field(&value, "payload").unwrap();
                let stages = array(field(payload, "stages").unwrap()).unwrap();
                let domain = field(&stages[0], "analysisDomain").unwrap();
                let scope = field(domain, "subjectScope").unwrap();
                assert_eq!(
                    field(scope, "subjectCount").unwrap(),
                    &Value::Unsigned(count)
                );
                assert!(field(domain, "subjects").is_err());
            }
        }
        assert!(saw_analyze);
        assert!(sender.complete());
        assert_eq!(source.reads, count as usize + 1);
    }
}
