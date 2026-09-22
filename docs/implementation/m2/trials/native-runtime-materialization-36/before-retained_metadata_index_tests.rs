use super::*;
fn text(v: &V) -> &str {
    string(v).unwrap()
}
fn bytes(v: &V) -> Vec<u8> {
    let s = text(v);
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap())
        .collect()
}
#[test]
fn index_matches_shared_reference_captures_counters_and_pairing() {
    let mut count = 0;
    for line in include_bytes!("../../tests/fixtures/metadata-index263-cases.ndjson")
        .split(|b| *b == b'\n')
        .filter(|b| !b.is_empty())
    {
        let row = opensip_identity::parse_json(line).unwrap();
        let q = object(&row).unwrap();
        let label = text(&q["label"]);
        let l = array(&q["limits"]).unwrap();
        let mut budget = Budget::new(
            integer(&l[0]).unwrap() as usize,
            integer(&l[1]).unwrap() as usize,
            integer(&l[2]).unwrap() as usize,
        )
        .unwrap();
        let files: BTreeMap<_, _> = object(&q["files"])
            .unwrap()
            .iter()
            .map(|(k, v)| (k.clone(), bytes(v)))
            .collect();
        let mut reads = Vec::new();
        let result = Index::new(&bytes(&q["manifest"]), &mut budget, |path, cap| {
            reads.push((path.to_owned(), cap));
            files.get(path).cloned().ok_or(())
        });
        assert_eq!(
            result.is_ok(),
            q["built"] == V::Bool(true),
            "{label}: {:?}",
            result.as_ref().err()
        );
        if let Ok(mut index) = result {
            for (action, expected) in array(&q["actions"])
                .unwrap()
                .iter()
                .zip(array(&q["results"]).unwrap())
            {
                let e = object(expected).unwrap();
                let got = index.select(text(action));
                assert_eq!(
                    got.is_ok(),
                    e["ok"] == V::Bool(true),
                    "{label} {} {:?}",
                    text(action),
                    got.as_ref().err()
                );
                if let Ok(pair) = got {
                    assert_eq!(pair.kind().route().0, text(&e["kind"]), "{label}");
                    assert_eq!(pair.body_path(), text(&e["bodyPath"]), "{label}");
                    assert_eq!(pair.envelope_path(), text(&e["envelopePath"]), "{label}");
                    assert_eq!(pair.body(), bytes(&e["body"]), "{label}");
                    assert_eq!(pair.envelope(), bytes(&e["envelope"]), "{label}");
                }
            }
        }
        let expected: Vec<_> = array(&q["reads"])
            .unwrap()
            .iter()
            .map(|v| {
                let a = array(v).unwrap();
                (text(&a[0]).to_owned(), integer(&a[1]).unwrap() as usize)
            })
            .collect();
        assert_eq!(reads, expected, "{label} reads");
        let c = array(&q["counters"]).unwrap();
        assert_eq!(
            budget.counters(),
            (
                integer(&c[0]).unwrap() as usize,
                integer(&c[1]).unwrap() as usize,
                integer(&c[2]).unwrap() as usize
            ),
            "{label} counters"
        );
        assert_eq!(budget.failed, q["failed"] == V::Bool(true), "{label} latch");
        if budget.failed {
            assert_eq!(budget.edge(0), Err(Error::Closed), "{label}");
        }
        count += 1;
    }
    assert_eq!(count, 34);
}
#[test]
fn payload1_actual_index_pairing_and_shared_budget_match_reference() {
    let mut count = 0;
    for line in include_bytes!("../../tests/fixtures/payload281-index.ndjson")
        .split(|b| *b == b'\n')
        .filter(|b| !b.is_empty())
    {
        let row = opensip_identity::parse_json(line).unwrap();
        let q = object(&row).unwrap();
        let label = text(&q["label"]);
        let l = array(&q["limits"]).unwrap();
        let mut budget = Budget::new(
            integer(&l[0]).unwrap() as usize,
            integer(&l[1]).unwrap() as usize,
            integer(&l[2]).unwrap() as usize,
        )
        .unwrap();
        let files: BTreeMap<_, _> = object(&q["files"])
            .unwrap()
            .iter()
            .map(|(k, v)| (k.clone(), bytes(v)))
            .collect();
        let mut reads = Vec::new();
        let mut owned_pairs = Vec::new();
        let result = Index::new(&bytes(&q["manifest"]), &mut budget, |path, cap| {
            reads.push((path.to_owned(), cap));
            files.get(path).cloned().ok_or(())
        });
        assert_eq!(
            result.is_ok(),
            q["built"] == V::Bool(true),
            "{label}: {:?}",
            result.as_ref().err()
        );
        if let Ok(mut index) = result {
            for (action, expected) in array(&q["actions"])
                .unwrap()
                .iter()
                .zip(array(&q["results"]).unwrap())
            {
                let e = object(expected).unwrap();
                let got = index.select(text(action));
                assert_eq!(
                    got.is_ok(),
                    e["ok"] == V::Bool(true),
                    "{label} {} {:?}",
                    text(action),
                    got.as_ref().err()
                );
                if let Ok(pair) = got {
                    assert_eq!(pair.kind().route().0, text(&e["kind"]), "{label}");
                    assert_eq!(pair.body_path(), text(&e["bodyPath"]), "{label}");
                    assert_eq!(pair.envelope_path(), text(&e["envelopePath"]), "{label}");
                    assert_eq!(pair.body(), bytes(&e["body"]), "{label}");
                    assert_eq!(pair.envelope(), bytes(&e["envelope"]), "{label}");
                    owned_pairs.push((pair, bytes(&e["body"]), bytes(&e["envelope"])));
                }
            }
        }
        let expected: Vec<_> = array(&q["reads"])
            .unwrap()
            .iter()
            .map(|v| {
                let a = array(v).unwrap();
                (text(&a[0]).to_owned(), integer(&a[1]).unwrap() as usize)
            })
            .collect();
        assert_eq!(reads, expected, "{label} reads");
        let c = array(&q["counters"]).unwrap();
        assert_eq!(
            budget.counters(),
            (
                integer(&c[0]).unwrap() as usize,
                integer(&c[1]).unwrap() as usize,
                integer(&c[2]).unwrap() as usize
            ),
            "{label} counters"
        );
        assert_eq!(budget.failed, q["failed"] == V::Bool(true), "{label} latch");
        if budget.failed {
            assert_eq!(budget.edge(0), Err(Error::Closed), "{label}");
        }
        drop(files);
        drop(budget);
        for (pair, body, envelope) in owned_pairs {
            assert_eq!(pair.body(), body);
            assert_eq!(pair.envelope(), envelope);
        }
        count += 1;
    }
    assert_eq!(count, 54);
}
#[test]
fn operation_budget_identity_presence_caps_and_failure_are_shared() {
    for limits in [
        (0, 1, 1),
        (65537, 1, 1),
        (1, 0, 1),
        (1, 131073, 1),
        (1, 1, 0),
        (1, 1, 268435457),
    ] {
        assert!(matches!(
            Budget::new(limits.0, limits.1, limits.2),
            Err(Error::Profile)
        ));
    }
    let mut b = Budget::new(4, 3, 8).unwrap();
    let raw = b"{}";
    let hash = opensip_identity::raw_sha256(raw);
    let first = b.retain(Collection::Objects, raw).unwrap();
    let same = b.retain(Collection::Objects, raw).unwrap();
    assert!(Arc::ptr_eq(&first, &same));
    for c in [
        Collection::Records,
        Collection::Events,
        Collection::Publications,
    ] {
        b.retain(c, raw).unwrap();
    }
    assert_eq!(b.counters(), (4, 0, 8));
    b.capture(Collection::Objects, hash, false, |_| {
        panic!("cached nonpresence")
    })
    .unwrap();
    let captured = b
        .capture(Collection::Objects, hash, true, |cap| {
            assert_eq!(cap, 2);
            Ok(raw.to_vec())
        })
        .unwrap();
    assert!(Arc::ptr_eq(&first, &captured));
    b.edge(2).unwrap();
    b.edge(1).unwrap();
    assert_eq!(b.edge(1), Err(Error::EdgeLimit));
    assert_eq!(
        b.capture(Collection::Objects, hash, false, |_| panic!("closed")),
        Err(Error::Closed)
    );
    let mut b = Budget::new(1, 1, 2).unwrap();
    b.retain(Collection::Objects, raw).unwrap();
    assert_eq!(
        b.capture(Collection::Records, hash, true, |_| panic!(
            "object limit before capture"
        )),
        Err(Error::ObjectLimit)
    );
    let mut b = Budget::new(2, 1, 2).unwrap();
    b.retain(Collection::Objects, raw).unwrap();
    assert_eq!(
        b.capture(Collection::Records, hash, true, |_| panic!(
            "byte limit before capture"
        )),
        Err(Error::ByteLimit)
    );
    let mut b = Budget::new(2, 1, 2).unwrap();
    assert_eq!(
        b.capture(Collection::Objects, hash, true, |cap| {
            assert_eq!(cap, 2);
            Ok(b"{} ".to_vec())
        }),
        Err(Error::Cap)
    );
    assert_eq!(b.retain(Collection::Objects, raw), Err(Error::Closed));
    let mut b = Budget::new(2, 1, 4).unwrap();
    b.retain(Collection::Objects, raw).unwrap();
    assert_eq!(
        b.capture(Collection::Objects, hash, true, |cap| {
            assert_eq!(cap, 2);
            Err(())
        }),
        Err(Error::Capture)
    );
    assert_eq!(b.retain(Collection::Objects, raw), Err(Error::Closed));
}
#[test]
fn second_index_cannot_reset_operation_or_hide_presence() {
    let line = include_bytes!("../../tests/fixtures/metadata-index263-cases.ndjson")
        .split(|b| *b == b'\n')
        .next()
        .unwrap();
    let q = opensip_identity::parse_json(line).unwrap();
    let q = object(&q).unwrap();
    let raw = bytes(&q["manifest"]);
    let files: BTreeMap<_, _> = object(&q["files"])
        .unwrap()
        .iter()
        .map(|(k, v)| (k.clone(), bytes(v)))
        .collect();
    let mut b = Budget::new(100, 24, 100000).unwrap();
    let first = Index::new(&raw, &mut b, |p, _| files.get(p).cloned().ok_or(()))
        .unwrap()
        .select("root.json")
        .unwrap();
    let before = b.counters();
    let second = Index::new(&raw, &mut b, |p, _| files.get(p).cloned().ok_or(()))
        .unwrap()
        .select("root.json")
        .unwrap();
    assert_eq!(b.counters(), (before.0, 24, before.2));
    assert!(Arc::ptr_eq(&first.body, &second.body));
    assert!(Arc::ptr_eq(&first.envelope, &second.envelope));
    assert!(matches!(
        Index::new(&raw, &mut b, |_, _| panic!("edge budget before capture")),
        Err(Error::EdgeLimit)
    ));
    assert!(matches!(
        Index::new(&raw, &mut b, |_, _| panic!("latched failure")),
        Err(Error::Closed)
    ));
    assert_eq!(first.body(), second.body());
}
