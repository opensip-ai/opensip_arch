use super::*;
use opensip_identity::JsonInteger;

#[test]
fn pinned_schema_corpus_matches_exact_decode_acceptance() {
    let V::Object(top) =
        parse_json(include_bytes!("../../tests/fixtures/lineage-node367.json")).unwrap()
    else {
        panic!("fixture object")
    };
    let V::Array(cases) = &top["cases"] else {
        panic!("fixture cases")
    };
    assert!(cases.len() > 500);
    let mut accepted = 0;
    for case in cases {
        let V::Object(row) = case else {
            panic!("fixture row")
        };
        let V::String(raw) = &row["raw"] else {
            panic!("fixture raw")
        };
        let V::Bool(expected) = row["accept"] else {
            panic!("fixture accept")
        };
        let actual = Node::decode(raw.as_bytes());
        assert_eq!(
            actual.is_ok(),
            expected,
            "case {:?}: {actual:?}",
            row["name"]
        );
        accepted += usize::from(expected);
    }
    assert!(accepted > 100);
    assert!(cases.len() - accepted > 400);
}

fn integer(n: i128) -> V {
    V::Integer(JsonInteger::new(n).unwrap())
}
fn key(n: u32, g: i64, k: u8) -> Key {
    Key::parse(&format!("{n:032x}"), g, k).unwrap()
}
fn triple(k: &Key) -> BTreeMap<String, V> {
    [
        (
            "storeInstanceId".into(),
            V::String(k.store_instance().into()),
        ),
        (
            "storeGeneration".into(),
            integer(k.store_generation() as i128),
        ),
        ("stateSchema".into(), integer(k.state_schema() as i128)),
    ]
    .into()
}
fn value(k: &Key, p: Option<&Key>) -> V {
    let mut fields = triple(k);
    fields.insert("schemaVersion".into(), integer(1));
    fields.insert(
        "predecessor".into(),
        p.map(|p| V::Object(triple(p))).unwrap_or(V::Null),
    );
    fields.insert(
        "selectedByIntentDigest".into(),
        p.map(|_| V::String("a".repeat(64))).unwrap_or(V::Null),
    );
    V::Object(fields)
}
fn raw(k: &Key, p: Option<&Key>) -> Vec<u8> {
    canonical_bytes(&value(k, p)).unwrap()
}
fn changed(field: &str, v: V) -> Vec<u8> {
    let V::Object(mut f) = value(&key(1, 0, 1), None) else {
        unreachable!()
    };
    f.insert(field.into(), v);
    canonical_bytes(&V::Object(f)).unwrap()
}
fn walk(
    start: &Key,
    limit: usize,
    rows: &BTreeMap<Key, Vec<u8>>,
) -> Result<SuppliedChain, WalkError<DecodeError>> {
    inspect_supplied(start, limit, |k| {
        rows.get(k).map(|b| Node::decode(b)).transpose()
    })
}

#[test]
fn roots_preserve_zero_max_and_both_schemas_and_own_raw_bytes() {
    for g in [0, 1, i64::MAX] {
        for k in [1, 2] {
            let selected = key(1, g, k);
            let mut bytes = raw(&selected, None);
            let saved = bytes.clone();
            let node = Node::decode(&bytes).unwrap();
            bytes.clear();
            assert_eq!(node.raw(), saved);
            assert_eq!(node.key(), &selected);
            assert_eq!(node.predecessor(), None);
            assert_eq!(node.selected_by_intent_digest(), None);
            assert_eq!(
                selected.relative_path(),
                PathBuf::from(format!("transitions/lineage/{:032x}/{g}/{k}.node", 1))
            );
        }
    }
}

#[test]
fn closed_shapes_duplicate_keys_and_noninteger_numbers_are_refused() {
    let V::Object(fields) = value(&key(1, 0, 1), None) else {
        unreachable!()
    };
    for name in fields.keys() {
        let mut f = fields.clone();
        f.remove(name);
        assert!(matches!(
            Node::decode(&canonical_bytes(&V::Object(f)).unwrap()),
            Err(DecodeError::Shape)
        ));
    }
    assert!(matches!(
        Node::decode(&changed("extra", V::Null)),
        Err(DecodeError::Shape)
    ));
    for bytes in [b"null" as &[u8], b"[]", b"true"] {
        assert!(matches!(Node::decode(bytes), Err(DecodeError::Shape)));
    }
    let text = String::from_utf8(raw(&key(1, 0, 1), None)).unwrap();
    for replacement in [
        "\"schemaVersion\":1,\"schemaVersion\":1",
        "\"schemaVersion\":1.0",
        "\"schemaVersion\":1e0",
    ] {
        assert!(matches!(
            Node::decode(text.replace("\"schemaVersion\":1", replacement).as_bytes()),
            Err(DecodeError::Decode(_))
        ));
    }
    for v in [
        V::Bool(true),
        V::Null,
        V::String("1".into()),
        integer(0),
        integer(2),
    ] {
        assert!(matches!(
            Node::decode(&changed("schemaVersion", v)),
            Err(DecodeError::Version)
        ));
    }
}

#[test]
fn both_triples_use_complete_store_and_integer_domains() {
    for field in ["storeInstanceId", "storeGeneration", "stateSchema"] {
        let bad = match field {
            "storeInstanceId" => vec![
                V::Null,
                V::String("a".repeat(31)),
                V::String("a".repeat(33)),
                V::String("A".repeat(32)),
                V::String(format!("{}\n", "a".repeat(32))),
                V::String("g".repeat(32)),
            ],
            "storeGeneration" => vec![
                integer(-1),
                integer(i64::MAX as i128 + 1),
                V::Bool(false),
                V::String("0".into()),
                V::Null,
            ],
            _ => vec![
                integer(0),
                integer(3),
                V::Bool(true),
                V::String("1".into()),
                V::Null,
            ],
        };
        for v in bad {
            assert!(Node::decode(&changed(field, v.clone())).is_err());
            let mut p = triple(&key(2, 0, 1));
            p.insert(field.into(), v);
            let V::Object(mut f) = value(&key(1, 0, 1), Some(&key(2, 0, 1))) else {
                unreachable!()
            };
            f.insert("predecessor".into(), V::Object(p));
            assert!(Node::decode(&canonical_bytes(&V::Object(f)).unwrap()).is_err());
        }
    }
    assert!(Key::parse(&"a".repeat(32), -1, 1).is_err());
    assert!(Key::parse(&"a".repeat(32), 0, 3).is_err());
}

#[test]
fn predecessor_shape_null_pair_and_digest_are_exact() {
    for name in ["storeInstanceId", "storeGeneration", "stateSchema"] {
        let mut p = triple(&key(2, 0, 1));
        p.remove(name);
        assert!(matches!(
            Node::decode(&changed("predecessor", V::Object(p))),
            Err(DecodeError::Shape)
        ));
    }
    let mut p = triple(&key(2, 0, 1));
    p.insert("extra".into(), V::Null);
    assert!(matches!(
        Node::decode(&changed("predecessor", V::Object(p))),
        Err(DecodeError::Shape)
    ));
    assert!(matches!(
        Node::decode(&changed("predecessor", V::Object(triple(&key(2, 0, 1))))),
        Err(DecodeError::RootPair)
    ));
    assert!(matches!(
        Node::decode(&changed(
            "selectedByIntentDigest",
            V::String("a".repeat(64))
        )),
        Err(DecodeError::RootPair)
    ));
    for v in [
        V::Bool(false),
        V::String("a".repeat(63)),
        V::String("a".repeat(65)),
        V::String("A".repeat(64)),
        V::String("g".repeat(64)),
        V::String(format!("{}\n", "a".repeat(64))),
    ] {
        assert!(matches!(
            Node::decode(&changed("selectedByIntentDigest", v)),
            Err(DecodeError::Digest)
        ));
    }
    assert!(matches!(
        Node::decode(&raw(&key(1, 0, 1), Some(&key(1, 0, 1)))),
        Err(DecodeError::SelfPredecessor)
    ));
}

#[test]
fn cap_is_before_parse_and_canonical_bytes_are_required() {
    assert!(matches!(
        Node::decode(&vec![255; 4097]),
        Err(DecodeError::Bound)
    ));
    assert!(matches!(
        Node::decode(&vec![255; 4096]),
        Err(DecodeError::Decode(_))
    ));
    let text = String::from_utf8(raw(&key(1, 0, 1), None)).unwrap();
    for s in [
        format!("{text}\n"),
        format!(" {text}"),
        text.replace("\":", "\": "),
        text.replace("storeInstanceId", "storeInstanceI\\u0064"),
    ] {
        assert!(matches!(
            Node::decode(s.as_bytes()),
            Err(DecodeError::NonCanonical)
        ));
    }
}

#[test]
fn full_triples_not_generation_or_intent_digest_are_keys() {
    // Equal generations and repeated intent digests are lawful; no monotonicity
    // or digest-uniqueness rule is introduced by the structural reader.
    let a = key(1, i64::MAX, 1);
    let b = key(2, 0, 2);
    let c = key(3, 0, 2);
    let rows = [
        (a.clone(), raw(&a, None)),
        (b.clone(), raw(&b, Some(&a))),
        (c.clone(), raw(&c, Some(&b))),
    ]
    .into();
    let chain = walk(&c, 3, &rows).unwrap();
    assert_eq!(
        chain.nodes().iter().map(Node::key).collect::<Vec<_>>(),
        vec![&c, &b, &a]
    );
    assert_eq!(
        chain.nodes()[0].selected_by_intent_digest(),
        chain.nodes()[1].selected_by_intent_digest()
    );
}

#[test]
fn unrelated_components_are_not_scanned_and_root_lookup_is_not_skipped() {
    let a = key(1, 0, 1);
    let b = key(2, 0, 1);
    let rows = [(a.clone(), raw(&a, None)), (b, vec![255])].into();
    assert_eq!(walk(&a, 1, &rows).unwrap().nodes().len(), 1);
    let mut calls = 0;
    let result = inspect_supplied::<()>(&a, 0, |_| {
        calls += 1;
        unreachable!()
    });
    assert!(matches!(result, Err(WalkError::Limit)));
    assert_eq!(calls, 0);
    assert!(matches!(walk(&a,1,&BTreeMap::new()),Err(WalkError::Missing(k)) if k==a));
}

#[test]
fn missing_unreadable_misbound_and_late_malformed_are_distinct() {
    let a = key(1, 0, 1);
    let b = key(2, 0, 1);
    let mut rows: BTreeMap<_, _> = [(b.clone(), raw(&b, Some(&a)))].into();
    assert!(matches!(walk(&b,2,&rows),Err(WalkError::Missing(k)) if k==a));
    let result = inspect_supplied(&b, 2, |_| Err("unreadable"));
    assert!(matches!(result, Err(WalkError::Read("unreadable"))));
    rows.insert(a.clone(), vec![255]);
    assert!(matches!(
        walk(&b, 2, &rows),
        Err(WalkError::Read(DecodeError::Decode(_)))
    ));
    rows.insert(a.clone(), raw(&key(3, 0, 1), None));
    assert!(matches!(walk(&b,2,&rows),Err(WalkError::Misbound{requested,..}) if requested==a));
}

#[test]
fn cycles_and_truncation_return_no_partial_success_or_extra_reads() {
    let a = key(1, 0, 1);
    let b = key(2, 0, 1);
    let rows: BTreeMap<_, _> = [
        (a.clone(), raw(&a, Some(&b))),
        (b.clone(), raw(&b, Some(&a))),
    ]
    .into();
    let mut calls = 0;
    let result = inspect_supplied(&a, 3, |k| {
        calls += 1;
        rows.get(k).map(|r| Node::decode(r)).transpose()
    });
    assert!(matches!(result,Err(WalkError::Cycle(k)) if k==a));
    assert_eq!(calls, 2);
    calls = 0;
    let result = inspect_supplied(&a, 1, |k| {
        calls += 1;
        rows.get(k).map(|r| Node::decode(r)).transpose()
    });
    assert!(matches!(result, Err(WalkError::Limit)));
    assert_eq!(calls, 1);
}

#[test]
fn long_chain_is_iterative_and_exact_bound_includes_root() {
    let mut rows = BTreeMap::new();
    for n in 1..=300 {
        let k = key(n, 0, 1);
        let previous = key(n - 1, 0, 1);
        rows.insert(
            k.clone(),
            raw(&k, if n == 1 { None } else { Some(&previous) }),
        );
    }
    assert_eq!(
        walk(&key(300, 0, 1), 300, &rows).unwrap().nodes().len(),
        300
    );
    assert!(matches!(
        walk(&key(300, 0, 1), 299, &rows),
        Err(WalkError::Limit)
    ));
}

#[test]
fn unchanged_target_does_not_skip_revalidating_a_broken_predecessor() {
    let a = key(1, 0, 1);
    let b = key(2, 0, 1);
    let mut rows: BTreeMap<_, _> =
        [(a.clone(), raw(&a, None)), (b.clone(), raw(&b, Some(&a)))].into();
    let target = rows[&b].clone();
    assert!(walk(&b, 2, &rows).is_ok());
    rows.remove(&a);
    assert!(matches!(walk(&b, 2, &rows), Err(WalkError::Missing(_))));
    assert_eq!(rows[&b], target);
}
