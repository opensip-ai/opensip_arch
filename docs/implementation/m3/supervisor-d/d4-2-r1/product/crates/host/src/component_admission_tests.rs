//! M3-D unit D4-2 tests (D4 plan r2, section 5's D4-2 controls): the pinned
//! provider table against the embedded matrix, the adapter over the trust
//! owner's view for every role and for an explicitly-trusted analyzer,
//! provenance read from the release row, the reader's reserved list passed
//! through, the no-trust-view case, exhaustion, and the source-order guards.
use super::*;
use opensip_components::manifest::{Arm, ExcludedFormClass};
use opensip_platform::WorkLedger;
use opensip_security::{TestComponent, admission_fixture_components};
use std::collections::BTreeSet;

const MATRIX: &[u8] = include_bytes!("native_capability_matrix.v2.json");

fn run(view: &AdmissionView<'_>) -> Step<Cleared> {
    let mut ledger = WorkLedger::new();
    ledger.scope::<_, ()>(|work| Ok(judge(view, work))).unwrap()
}
fn digest_of(c: &TestComponent) -> [u8; 32] {
    opensip_identity::raw_sha256(c.authenticated().body())
}

#[test]
fn d4_2_the_provider_table_is_the_embedded_matrix_projection_member_by_member() {
    let matrix: serde_json::Value = serde_json::from_slice(MATRIX).unwrap();
    let mut want: Vec<(String, String)> = Vec::new();
    let mut excluded: Vec<(String, String)> = Vec::new();
    for c in matrix["capabilities"].as_array().unwrap() {
        let authority = c.get("authority").and_then(|a| a.as_str());
        for pair in c["relations"].as_array().unwrap() {
            let pair = (
                pair[0].as_str().unwrap().to_owned(),
                pair[1].as_str().unwrap().to_owned(),
            );
            if matches!(authority, Some("fact") | Some("candidate-only")) {
                excluded.push(pair);
            } else {
                want.push(pair);
            }
        }
    }
    want.sort();
    let table: Vec<(String, String)> = PROVIDER_RELATIONS
        .iter()
        .map(|(r, g)| ((*r).to_owned(), (*g).to_owned()))
        .collect();
    // Order-aware and member by member: a same-size substitution or a
    // source-side addition fails here.
    assert_eq!(table, want);
    // The host-produced facts are excluded: inventory's three pairs and
    // clones-fact's; the candidate-only members have no pairs at all.
    assert_eq!(excluded.len(), 4);
    for pair in &excluded {
        assert!(!table.contains(pair), "{pair:?}");
    }
    assert!(EXPLICITLY_TRUSTED.is_empty());
}

#[test]
fn d4_2_every_role_passes_and_the_set_is_cleared_in_digest_order() {
    let fixtures = admission_fixture_components();
    assert_eq!(fixtures.len(), 6);
    let five: Vec<_> = fixtures[..5]
        .iter()
        .map(TestComponent::authenticated)
        .collect();
    let reserved = BTreeSet::new();
    let view = AdmissionView::fixture(five, &reserved);
    let cleared = run(&view).unwrap();
    let mut want: Vec<[u8; 32]> = fixtures[..5].iter().map(digest_of).collect();
    want.sort();
    assert_eq!(cleared.digests(), &want[..]);
}

/// A lawful analyzer command tree has one mounted root and a child.
/// Dropping the child's parent would manufacture a second root and refuse
/// an otherwise admissible component.
#[test]
fn d4_2_a_child_command_keeps_its_parent_and_does_not_become_a_root() {
    let fixtures = admission_fixture_components();
    let analyzer = fixtures[0].authenticated();
    let mut value = opensip_identity::parse_json(analyzer.body()).unwrap();
    let V::Object(body) = &mut value else {
        unreachable!()
    };
    let V::Array(commands) = body.get_mut("commands").unwrap() else {
        unreachable!()
    };
    commands.push(V::Object(
        [
            ("name".to_owned(), V::String("inspect".to_owned())),
            (
                "parent".to_owned(),
                V::String("typescript-analyzer".to_owned()),
            ),
            (
                "description".to_owned(),
                V::String("synthetic child command".to_owned()),
            ),
        ]
        .into_iter()
        .collect(),
    ));
    let raw = opensip_identity::canonical_bytes(&value).unwrap();
    let mut release = match analyzer.release() {
        V::Object(row) => row.clone(),
        _ => unreachable!(),
    };
    let digest = opensip_identity::raw_sha256(&raw);
    release.insert(
        "manifestDigest".to_owned(),
        V::String(opensip_identity::digest_hex(&digest).to_owned()),
    );
    let component = TestComponent::new(raw, Vec::new(), V::Object(release)).unwrap();
    // A child uses its parent's namespace: only the mounted root is
    // checked against the reserved root-command set.
    let reserved = ["inspect".to_owned()].into_iter().collect();
    let view = AdmissionView::fixture(vec![component.authenticated()], &reserved);
    assert_eq!(run(&view).unwrap().digests(), &[digest]);
}

#[test]
fn d4_2_the_explicitly_trusted_analyzer_refuses_ee1() {
    let fixtures = admission_fixture_components();
    let all: Vec<_> = fixtures.iter().map(TestComponent::authenticated).collect();
    let reserved = BTreeSet::new();
    let view = AdmissionView::fixture(all, &reserved);
    let Err(AdmissionFailure::Excluded(forms)) = run(&view) else {
        panic!("not refused")
    };
    assert_eq!(forms.len(), 1);
    assert_eq!(forms[0].class, ExcludedFormClass::Ee1);
    assert_eq!(forms[0].arm, Arm::UnlistedPublisher);
    assert_eq!(forms[0].manifest_digest, digest_of(&fixtures[5]));
}

#[test]
fn d4_2_provenance_is_the_release_rows_not_the_bodys() {
    // A first-party body joined to a release row saying explicitly-trusted:
    // the adapter reads the release association, so it refuses EE-1.
    let fixtures = admission_fixture_components();
    let first = fixtures[0].authenticated();
    let mut release = match first.release() {
        V::Object(o) => o.clone(),
        _ => unreachable!(),
    };
    release.insert(
        "sourceClass".to_owned(),
        V::String("explicitly-trusted".to_owned()),
    );
    let joined = TestComponent::new(first.body().to_vec(), Vec::new(), V::Object(release)).unwrap();
    let reserved = BTreeSet::new();
    let view = AdmissionView::fixture(vec![joined.authenticated()], &reserved);
    let Err(AdmissionFailure::Excluded(forms)) = run(&view) else {
        panic!("not refused")
    };
    assert_eq!(forms[0].class, ExcludedFormClass::Ee1);
}

#[test]
fn d4_2_the_readers_reserved_list_is_the_one_judged() {
    // The fixture manifests' name, `typescript-analyzer`, reserved: EE-5a (c),
    // so the adapter passed the view's list through.
    let fixtures = admission_fixture_components();
    let five: Vec<_> = fixtures[..5]
        .iter()
        .map(TestComponent::authenticated)
        .collect();
    let reserved: BTreeSet<String> = ["doctor", "typescript-analyzer"]
        .into_iter()
        .map(str::to_owned)
        .collect();
    let view = AdmissionView::fixture(five, &reserved);
    let Err(AdmissionFailure::Excluded(forms)) = run(&view) else {
        panic!("not refused")
    };
    // Every synthetic role shares the fixture manifest's name, so each of
    // the five is refused by (c), and only because the list was passed.
    assert_eq!(forms.len(), 5);
    for form in &forms {
        assert_eq!(
            (form.class, form.arm),
            (ExcludedFormClass::Ee5a, Arm::ReservedRoot)
        );
    }
    let empty = BTreeSet::new();
    let five: Vec<_> = fixtures[..5]
        .iter()
        .map(TestComponent::authenticated)
        .collect();
    assert!(run(&AdmissionView::fixture(five, &empty)).is_ok());
}

#[test]
fn d4_2_no_trust_view_admits_nothing_and_refuses_nothing() {
    let reserved = BTreeSet::new();
    let view = AdmissionView::fixture(Vec::new(), &reserved);
    assert_eq!(run(&view).unwrap().digests(), &[] as &[[u8; 32]]);
}

/// Exhaustion: with every allowance below the run's actual use, the judge
/// refuses `Budget`, never a partial clearing or a refusal it could not
/// fund; at the actual use it clears.
#[test]
fn d4_2_every_short_allowance_refuses_budget() {
    let fixtures = admission_fixture_components();
    let five = || {
        fixtures[..5]
            .iter()
            .map(TestComponent::authenticated)
            .collect::<Vec<_>>()
    };
    let reserved = BTreeSet::new();
    let view = AdmissionView::fixture(five(), &reserved);
    let mut ledger = WorkLedger::new();
    let used = ledger
        .scope::<_, ()>(|work| {
            judge(&view, work).unwrap();
            Ok(work.used())
        })
        .unwrap();
    for (which, limits) in [
        (
            "edges",
            (1..used.edges)
                .step_by((used.edges / 97).max(1))
                .map(|e| WorkCost {
                    objects: 65_536,
                    edges: e,
                    bytes: 268_435_456,
                })
                .collect::<Vec<_>>(),
        ),
        (
            "objects",
            (1..used.objects)
                .map(|o| WorkCost {
                    objects: o,
                    edges: 131_072,
                    bytes: 268_435_456,
                })
                .collect(),
        ),
    ] {
        for limit in limits {
            let mut tight = WorkLedger::with_limits(limit).unwrap();
            let outcome = tight.scope::<_, ()>(|work| Ok(judge(&view, work)));
            assert!(
                matches!(
                    outcome,
                    Ok(Err(AdmissionFailure::Budget(_))) | Err(WorkFailure::Budget(_))
                ),
                "{which} {limit:?}: {outcome:?}"
            );
        }
    }
    let mut exact = WorkLedger::with_limits(used).unwrap();
    assert!(
        exact
            .scope::<_, ()>(|work| Ok(judge(&view, work)))
            .unwrap()
            .is_ok()
    );
}

/// The source-order guards (checklist item 1): every allocation goes
/// through `reserve`, its charge on the line before; every member lookup
/// through `member`, its charge on the line before; every push and every
/// spelling comparison after its own one-edge charge; and each digest byte
/// after its charge.
#[test]
fn d4_2_every_work_site_follows_its_charge() {
    let source = include_str!("component_admission.rs");
    let production = &source[..source.find("#[cfg(test)]\n#[path").unwrap()];
    let lines: Vec<&str> = production.lines().map(str::trim).collect();
    let before = |i: usize| -> &str {
        let mut j = i;
        loop {
            j -= 1;
            if !lines[j].is_empty() && !lines[j].starts_with("//") {
                return lines[j];
            }
        }
    };
    let sites = |needle: &str| -> Vec<usize> {
        lines
            .iter()
            .enumerate()
            .filter(|(_, l)| l.contains(needle))
            .map(|(i, _)| i)
            .collect()
    };
    let alloc = sites("::with_capacity(");
    assert_eq!(alloc.len(), 1);
    assert_eq!(before(alloc[0]), ".map_err(budget)?;");
    assert!(lines[alloc[0] - 6].starts_with("work.charge::<()>(WorkCost {"));
    let get = sites(".get(");
    assert_eq!(get.len(), 1);
    assert!(
        before(get[0])
            .starts_with("edges(work, manifest::probe_reference_comparisons(object.len()))?;")
    );
    let pushes = sites(".push(");
    assert_eq!(pushes.len(), 7);
    for p in pushes {
        assert_eq!(before(p), "edges(work, 1)?;", "the push at line {}", p + 1);
    }
    let spellings = sites("if name == spelling {");
    assert_eq!(spellings.len(), 2);
    for s in spellings {
        assert_eq!(before(s), "edges(work, 1)?;");
    }
    let nibbles = sites("let (Some(hi), Some(lo)) = (nibble(pair[0]), nibble(pair[1])) else {");
    assert_eq!(nibbles.len(), 1);
    assert_eq!(before(nibbles[0]), "edges(work, 1)?;");
}
