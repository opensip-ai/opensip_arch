// M3-B r9 item 16 (unit B2-d1): the closed YAML subset reader against its
// cross-implementation vectors (tools/host/yaml_subset_vectors.py: the
// hand-written grammar table, checked against the bound B2-d0 reference, and
// a substitution sweep whose results are the reference's), plus a full
// byte-substitution sweep that must never panic.
use super::yaml_subset::{MAX_BYTES, OutsideSubset, parse_pnpm_packages};
use opensip_identity::{JsonValue as V, parse_json};

const VECTORS: &[u8] = include_bytes!("yaml_subset_vectors.json");

fn field<'v>(value: &'v V, key: &str) -> &'v V {
    let V::Object(fields) = value else {
        panic!("{value:?}")
    };
    fields.get(key).unwrap_or(&V::Null)
}
fn text(value: &V) -> &str {
    let V::String(s) = value else {
        panic!("{value:?}")
    };
    s
}
fn items(value: &V) -> &[V] {
    let V::Array(items) = value else {
        panic!("{value:?}")
    };
    items
}
fn bytes(hex: &str) -> Vec<u8> {
    (0..hex.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
        .collect()
}
/// One vector: its kind, its name, the document, and the expected globs
/// (`None` outside the subset).
type Case = (String, String, Vec<u8>, Option<Vec<String>>);
fn cases() -> Vec<Case> {
    let body = parse_json(VECTORS).unwrap();
    items(field(&body, "cases"))
        .iter()
        .map(|case| {
            let expected = match field(case, "packages") {
                V::Null => None,
                list => Some(items(list).iter().map(|v| text(v).to_owned()).collect()),
            };
            (
                text(field(case, "kind")).to_owned(),
                text(field(case, "name")).to_owned(),
                bytes(text(field(case, "hex"))),
                expected,
            )
        })
        .collect()
}

#[test]
fn every_vector_matches_the_reference() {
    let body = parse_json(VECTORS).unwrap();
    let V::Integer(bound) = field(&body, "maxBytes") else {
        panic!("maxBytes")
    };
    assert_eq!(usize::try_from(bound.get()).unwrap(), MAX_BYTES);
    let all = cases();
    let grammar = all.iter().filter(|c| c.0 == "grammar").count();
    let sweep = all.iter().filter(|c| c.0 == "sweep").count();
    assert!(grammar >= 100 && sweep >= 1000, "{grammar} {sweep}");
    for (kind, name, raw, expected) in &all {
        assert_eq!(parse_pnpm_packages(raw).ok(), *expected, "{kind} {name}");
    }
}

#[test]
fn each_refusal_names_its_reason() {
    let reason = |name: &str| {
        let (_, _, raw, _) = cases().into_iter().find(|c| c.1 == name).unwrap();
        parse_pnpm_packages(&raw).unwrap_err()
    };
    assert_eq!(reason("past-64-kib"), OutsideSubset::Bound);
    assert_eq!(reason("refuse-not-utf8"), OutsideSubset::NotUtf8);
    assert_eq!(reason("refuse-nul-double"), OutsideSubset::Character);
    assert_eq!(reason("refuse-eof-cr-block-item"), OutsideSubset::Character);
    assert_eq!(reason("refuse-bare-key"), OutsideSubset::Structure);
    assert_eq!(
        reason("refuse-unseparated-empty-flow"),
        OutsideSubset::Structure
    );
    assert_eq!(reason("refuse-terminal-colon"), OutsideSubset::Scalar);
    assert_eq!(reason("refuse-integer"), OutsideSubset::Scalar);
}

#[test]
fn every_single_byte_substitution_returns_a_result() {
    // Every accepted grammar document, every position, every byte value: the
    // reader returns (never panics), and the same input gives the same result.
    for (kind, name, raw, expected) in cases() {
        if kind != "grammar" || expected.is_none() {
            continue;
        }
        for i in 0..raw.len() {
            let mut flipped = raw.clone();
            for byte in 0..=u8::MAX {
                flipped[i] = byte;
                let first = parse_pnpm_packages(&flipped);
                assert_eq!(
                    first,
                    parse_pnpm_packages(&flipped),
                    "{name} at {i} = {byte}"
                );
            }
        }
    }
}
