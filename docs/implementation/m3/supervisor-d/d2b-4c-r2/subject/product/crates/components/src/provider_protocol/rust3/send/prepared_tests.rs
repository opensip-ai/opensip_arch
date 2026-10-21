//! Supplied native projections only. These do not select a prepared mode,
//! admit freshness/authorization/toolchains or confer worker read authority.
use super::*;
use opensip_identity::{JsonInteger, canonical_bytes, raw_sha256};
fn n(v: u64) -> J {
    J::Integer(JsonInteger::new(i128::from(v)).unwrap())
}
fn s(v: &str) -> J {
    J::String(v.into())
}
fn obj(v: Vec<(&str, J)>) -> J {
    J::Object(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn row(kind: &str, length: u64, status: &str) -> J {
    let blob = obj(vec![
        ("byteLength", n(length)),
        ("sha256", s(&"a".repeat(64))),
        ("mediaType", s("application/octet-stream")),
    ]);
    let generated = if kind == "generated-file" {
        obj(vec![
            ("logicalPath", s("out/generated.rs")),
            ("blob", blob.clone()),
        ])
    } else {
        J::Null
    };
    obj(vec![
        ("kind", s(kind)),
        ("ownerKey", s("fixture-owner")),
        ("configuration", J::Array(vec![s("primary")])),
        ("site", J::Null),
        (
            "inputBinding",
            obj(vec![
                ("cfgSetId", s("primary")),
                (
                    "dependencySourceSetId",
                    s(&format!("sha256:{}", "b".repeat(64))),
                ),
                ("ownerFileManifestSha256", s(&"c".repeat(64))),
                ("toolchainDigest", s(&"d".repeat(64))),
            ]),
        ),
        ("blob", blob),
        ("status", s(status)),
        (
            "failureDetail",
            if status == "failed" {
                s("fixture-failure")
            } else {
                J::Null
            },
        ),
        ("generated", generated),
    ])
}
fn set(rows: Vec<J>) -> J {
    // The preparation cell is deliberately opaque to this host-wire test.
    // Full native set/toolchain admission belongs to C4, before this boundary.
    obj(vec![
        ("schemaVersion", n(3)),
        ("preparation", obj(vec![("fixture", s("not-admitted"))])),
        ("rows", J::Array(rows)),
    ])
}
fn reference_id(set: &J) -> String {
    let bytes = canonical_bytes(set).unwrap();
    let mut frame = b"opensip.product.v1\0native.prepared-output-set.v3\0".to_vec();
    frame.extend_from_slice(&(bytes.len() as u64).to_be_bytes());
    frame.extend(bytes);
    format!("sha256:{}", digest_hex(&raw_sha256(&frame)))
}
fn plan() -> String {
    format!("plan2:{}", "e".repeat(64))
}
fn build_set(policy: &Policy, set: &J, sequence: u64) -> Result<Built, Refusal> {
    build(
        policy,
        &Input {
            set,
            set_id: &reference_id(set),
            plan_id: &plan(),
        },
        sequence,
    )
}
fn wm<'a>(v: &'a Value, k: &str) -> &'a Value {
    let Value::Map(v) = v else { panic!() };
    super::super::super::super::ts2::carrier::field(v, k).unwrap()
}
fn replace(v: &mut J, k: &str, new: J) {
    let J::Object(v) = v else { panic!() };
    v.insert(k.into(), new);
}

#[test]
fn prepared_manifest_binds_every_exact_row_including_failed_and_raw_blob_fields() {
    let policy = Policy::load().unwrap();
    let rows = vec![
        row("build-script-directives", 1_048_577, "ok"),
        row("macro-expansion", 3, "failed"),
        row("generated-file", 0, "ok"),
    ];
    let native = set(rows.clone());
    let built = build_set(&policy, &native, 9).unwrap();
    let Value::Array(entries) = wm(&built.manifest, "entries") else {
        panic!()
    };
    assert_eq!(entries.len(), 3);
    for (ordinal, (entry, row)) in entries.iter().zip(&rows).enumerate() {
        let carried =
            super::super::super::super::ts2::carrier::to_json(wm(entry, "planRow")).unwrap();
        assert_eq!(&carried, row);
        assert_eq!(wm(entry, "outputOrdinal"), &Value::Unsigned(ordinal as u64));
        assert_eq!(
            wm(entry, "logicalPath"),
            &t(&format!(
                ".opensip/prepared/v3/{ordinal}-{}.blob",
                "a".repeat(64)
            ))
        );
        let length = number(field(field(row, "blob").unwrap(), "byteLength").unwrap()).unwrap();
        assert_eq!(wm(entry, "blobByteLength"), &Value::Unsigned(length));
        assert_eq!(wm(entry, "contentByteLength"), &Value::Unsigned(length));
        assert_eq!(wm(entry, "blobSha256"), wm(entry, "contentSha256"));
    }
    assert_eq!(wm(wm(&entries[1], "planRow"), "status"), &t("failed"));
    assert_eq!((built.bytes, built.chunks), (1_048_580, 3));
    let digest = digest_hex(&raw_sha256(&cbor::encode(wm(&built.manifest, "entries"))));
    assert_eq!(wm(&built.manifest, "manifestSha256"), &t(&digest));
    assert_eq!(wm(&built.seal, "manifestSha256"), &t(&digest));
    assert_eq!(
        wm(&built.seal, "totalBlobBytes"),
        &Value::Unsigned(1_048_580)
    );
    assert_eq!(wm(&built.seal, "totalChunkCount"), &Value::Unsigned(3));
}

#[test]
fn prepared_empty_and_full_256_row_sets_keep_contiguous_ordinals_without_filtering() {
    let policy = Policy::load().unwrap();
    let empty = build_set(&policy, &set(vec![]), 9).unwrap();
    assert_eq!(wm(&empty.manifest, "entries"), &Value::Array(vec![]));
    assert_eq!((empty.bytes, empty.chunks), (0, 0));
    assert_eq!(
        wm(&empty.manifest, "manifestSha256"),
        &t("76be8b528d0075f7aae98d6fa57a6d3c83ae480a8469e668d7b0af968995ac71")
    );
    let rows: Vec<_> = (0..256)
        .map(|index| {
            let mut r = row(
                "macro-expansion",
                0,
                if index % 2 == 0 { "ok" } else { "failed" },
            );
            replace(&mut r, "ownerKey", s(&format!("owner-{index}")));
            r
        })
        .collect();
    let built = build_set(&policy, &set(rows.clone()), 9).unwrap();
    let Value::Array(entries) = wm(&built.manifest, "entries") else {
        panic!()
    };
    assert_eq!(entries.len(), 256);
    for (ordinal, entry) in entries.iter().enumerate() {
        assert_eq!(wm(entry, "outputOrdinal"), &Value::Unsigned(ordinal as u64));
    }
    let mut over = rows;
    over.push(row("macro-expansion", 0, "failed"));
    assert!(matches!(
        build_set(&policy, &set(over), 9),
        Err(Refusal::Bound("prepared entries"))
    ));
}

#[test]
fn prepared_full_manifest_length_is_exact_before_row_copies_and_limits_are_inclusive() {
    let mut policy = Policy::load().unwrap();
    let native = set(vec![
        row("generated-file", 1, "ok"),
        row("macro-expansion", 0, "failed"),
    ]);
    for sequence in [23, 24, 65_536] {
        policy
            .limits
            .insert("maxFramePayloadBytes".into(), 67_108_864);
        let built = build_set(&policy, &native, sequence).unwrap();
        let size = cbor::encode(&schedule::envelope(
            sequence,
            "PreparedOutputManifest",
            built.manifest,
        ))
        .len() as u64;
        policy.limits.insert("maxFramePayloadBytes".into(), size);
        assert!(build_set(&policy, &native, sequence).is_ok());
        policy
            .limits
            .insert("maxFramePayloadBytes".into(), size - 1);
        assert!(matches!(
            build_set(&policy, &native, sequence),
            Err(Refusal::Bound("prepared manifest envelope"))
        ));
    }
    let policy = Policy::load().unwrap();
    let maximum = policy.limit("maxPreparedOutputTotalBlobBytes").unwrap();
    assert_eq!(
        build_set(
            &policy,
            &set(vec![row("macro-expansion", maximum, "failed")]),
            9
        )
        .unwrap()
        .bytes,
        maximum
    );
    assert!(matches!(
        build_set(
            &policy,
            &set(vec![
                row("macro-expansion", maximum, "ok"),
                row("macro-expansion", 1, "failed")
            ]),
            9
        ),
        Err(Refusal::Bound("prepared blob bytes"))
    ));
    for length in [0, 23, 24, 255, 256, 65_535, 65_536] {
        let value = J::Array(vec![
            s(&"é".repeat(length)),
            n(length as u64),
            J::Bool(true),
            J::Null,
        ]);
        assert_eq!(
            wire_length(&value).unwrap(),
            cbor::encode(&wire(&value).unwrap()).len() as u64
        );
    }
}

#[test]
fn prepared_wrong_set_noninert_rows_generated_joins_and_closed_rows_refuse() {
    let policy = Policy::load().unwrap();
    let native = set(vec![row("macro-expansion", 0, "ok")]);
    assert!(matches!(
        build(
            &policy,
            &Input {
                set: &native,
                set_id: &format!("sha256:{}", "0".repeat(64)),
                plan_id: &plan()
            },
            9
        ),
        Err(Refusal::Join("prepared set identity"))
    ));
    assert!(
        build(
            &policy,
            &Input {
                set: &native,
                set_id: &reference_id(&native),
                plan_id: "bad"
            },
            9
        )
        .is_err()
    );
    for kind in ["proc-macro-dylib", "build-script-binary"] {
        assert!(matches!(
            build_set(&policy, &set(vec![row(kind, 1, "ok")]), 9),
            Err(Refusal::Join("non-inert prepared row"))
        ));
    }
    let mut generated = row("generated-file", 1, "ok");
    let J::Object(fields) = &mut generated else {
        panic!()
    };
    let J::Object(generated_field) = fields.get_mut("generated").unwrap() else {
        panic!()
    };
    let J::Object(blob) = generated_field.get_mut("blob").unwrap() else {
        panic!()
    };
    blob.insert("mediaType".into(), s("text/plain"));
    assert!(matches!(
        build_set(&policy, &set(vec![generated]), 9),
        Err(Refusal::Join("generated blob equality"))
    ));
    let mut extra = row("macro-expansion", 1, "ok");
    replace(&mut extra, "extra", J::Bool(true));
    assert!(matches!(
        build_set(&policy, &set(vec![extra]), 9),
        Err(Refusal::Shape(_))
    ));
    let mut status = row("macro-expansion", 1, "ok");
    replace(&mut status, "status", s("invented"));
    assert!(build_set(&policy, &set(vec![status]), 9).is_err());
    // Preserve the owner pattern's literal line-terminator distinctions.
    for (path, valid) in [("a/..\n", true), ("a/\n/..", false)] {
        let mut r = row("generated-file", 1, "ok");
        let J::Object(fields) = &mut r else { panic!() };
        replace(fields.get_mut("generated").unwrap(), "logicalPath", s(path));
        assert_eq!(build_set(&policy, &set(vec![r]), 9).is_ok(), valid);
    }
}

#[test]
fn prepared_chunks_keep_greedy_ordinals_and_failed_rows_do_not_change_transfer() {
    let policy = Policy::load().unwrap();
    let native = set(vec![
        row("macro-expansion", 1_048_577, "failed"),
        row("macro-expansion", 0, "ok"),
    ]);
    let built = build_set(&policy, &native, 9).unwrap();
    let Value::Array(entries) = wm(&built.manifest, "entries") else {
        panic!()
    };
    let first = chunk(&policy, &plan(), &entries[0], 0, 0, vec![1; 1_048_576]).unwrap();
    assert_eq!(wm(&first, "outputOrdinal"), &Value::Unsigned(0));
    assert!(chunk(&policy, &plan(), &entries[0], 1, 1_048_576, vec![2]).is_ok());
    for (index, offset, bytes) in [
        (0, 0, vec![0]),
        (1, 1_048_575, vec![0]),
        (1, 1_048_576, vec![]),
        (2, 2_097_152, vec![0]),
        (u64::MAX, 0, vec![0]),
    ] {
        assert!(chunk(&policy, &plan(), &entries[0], index, offset, bytes).is_err());
    }
    assert!(chunk(&policy, &plan(), &entries[1], 0, 0, vec![]).is_err());
}

#[test]
fn replay_trial07_original_prepared_fixture_entries_and_both_join_mutations() {
    use super::super::super::super::{built_commitment, cbor};
    use super::super::{
        request::Request,
        schedule::Frame,
        sender::{Sender, tests::Fake},
    };
    let raw = include_bytes!("../../../../tests/data/trial07-prepared-fixture.v1.json");
    assert_eq!(
        digest_hex(&raw_sha256(raw)),
        "b6ccb101133a573230a94afaebf12ab3716074ea511f5a7844f835ba6024115b"
    );
    let fixture = parse_json(raw).unwrap();
    assert_eq!(
        text(field(field(&fixture, "source").unwrap(), "sha256").unwrap()).unwrap(),
        "a08b8cc380a2d332a752405fde11df1d5d63b050c7297ec21820516702367ddc"
    );
    assert_eq!(
        text(field(field(&fixture, "selector").unwrap(), "jsonPointer").unwrap()).unwrap(),
        "/fixtures/prepGenerated"
    );
    let corpus = parse_json(include_bytes!(
        "../../../../tests/data/trial07-integer-replay.v1.json"
    ))
    .unwrap();
    let J::Array(cases) = field(field(&corpus, "vectors").unwrap(), "PREPARED-V3-ENTRY").unwrap()
    else {
        panic!()
    };
    assert_eq!(cases.len(), 3);
    for case in cases {
        let id = text(field(case, "id").unwrap()).unwrap();
        let input = field(case, "input").unwrap();
        let mut set = field(&fixture, "fixture").unwrap().clone();
        assert_eq!(
            text(field(input, "setFixture").unwrap()).unwrap(),
            "prepGenerated"
        );
        let mutation = if let J::Object(m) = input {
            m.get("mutate")
        } else {
            panic!()
        };
        if let Some(J::Object(m)) = mutation
            && let Some(sha) = m.get("generatedBlobSha256")
        {
            let J::Object(s) = &mut set else { panic!() };
            let J::Array(rows) = s.get_mut("rows").unwrap() else {
                panic!()
            };
            let row = rows
                .iter_mut()
                .find(|r| text(field(r, "kind").unwrap()).unwrap() == "generated-file")
                .unwrap();
            let J::Object(row) = row else { panic!() };
            let J::Object(g) = row.get_mut("generated").unwrap() else {
                panic!()
            };
            replace(g.get_mut("blob").unwrap(), "sha256", sha.clone());
        }
        let mut plan = super::super::sender::tests::request(true).plan;
        let set_id = reference_id(&set);
        plan.prepared_set = Some(set.clone());
        fn vreplace(v: &mut Value, k: &str, new: Value) {
            let Value::Map(fields) = v else { panic!() };
            fields.iter_mut().find(|(name, _)| name == k).unwrap().1 = new;
        }
        vreplace(
            &mut plan.open.repository_resolution,
            "preparedOutputSetId",
            t(&set_id),
        );
        let Value::Map(universe) = &mut plan.open.universe else {
            panic!()
        };
        let resolved = &mut universe
            .iter_mut()
            .find(|(k, _)| k == "resolvedInputs")
            .unwrap()
            .1;
        vreplace(resolved, "preparedOutputSetId", t(&set_id));
        plan.universes[0].value = plan.open.universe.clone();
        let source = built_commitment("opensip.rust-provider.universe.v2", &plan.open.universe);
        for cell in &mut plan.stages[0].scopes {
            cell.source = source.clone();
            cell.target = source.clone();
        }
        let request = Request::build(plan);
        if id == "prepared-generated-blob-mismatch" {
            assert!(request.is_err(), "{id}");
            continue;
        }
        let mut request = request.unwrap();
        let index = request
            .schedule
            .slots
            .iter()
            .position(|s| s.frame == Frame::PreparedOutputManifest)
            .unwrap();
        if let Some(J::Object(m)) = mutation
            && m.contains_key("entry")
        {
            let slot = &mut request.schedule.slots[index];
            let policy = Policy::load().unwrap();
            let built = build(
                &policy,
                &Input {
                    set: &set,
                    set_id: &set_id,
                    plan_id: &request.plan.open.plan_id,
                },
                slot.sequence,
            )
            .unwrap();
            let mut manifest = built.manifest;
            let Value::Map(fields) = &mut manifest else {
                panic!()
            };
            let Value::Array(entries) =
                &mut fields.iter_mut().find(|(k, _)| k == "entries").unwrap().1
            else {
                panic!()
            };
            let at = usize::try_from(number(m.get("entry").unwrap()).unwrap()).unwrap();
            vreplace(
                &mut entries[at],
                "contentSha256",
                t(text(m.get("contentSha256").unwrap()).unwrap()),
            );
            let digest = manifest_digest(&Value::Array(entries.clone()));
            vreplace(&mut manifest, "manifestSha256", t(&digest));
            let payload_digest = raw_sha256(&cbor::encode(&manifest));
            let envelope = map(vec![
                ("protocolMajor", Value::Unsigned(3)),
                ("direction", t("host-to-worker")),
                ("sequence", Value::Unsigned(slot.sequence)),
                ("frameType", t("PreparedOutputManifest")),
                ("payload", manifest),
            ]);
            let raw = cbor::encode(&envelope);
            slot.payload_bytes = raw.len() as u64;
            slot.payload_sha256 = payload_digest;
        }
        let mut sender = Sender::new(request).unwrap();
        let mut source = Fake::default();
        while sender.next_slot().unwrap().frame != Frame::PreparedOutputManifest {
            sender.send_next(&mut source).unwrap();
        }
        let result = sender.send_next(&mut source);
        if result.is_err() {
            assert!(
                matches!(&result,Err(super::super::sender::Refusal::Divergence(message)) if message.contains("fixed payload digest")),
                "targeted proposal predicate {id}: {result:?}"
            );
        }
        assert_eq!(
            result.is_ok(),
            text(field(case, "kind").unwrap()).unwrap() == "accept",
            "{id}"
        );
        // Rows/preparation here are the exact historical synthetic input.
        // No native-set admission, execution or byte custody is inferred.
    }
}
