//! M3-D unit D4-1 tests (D4 plan r2, section 5): D4-T4 at D4's interface,
//! D4-T1's interface half, RF-1's independent accounting with one-unit-short
//! refusals at every charge site, and the closed-world pins.
use super::*;
use opensip_identity::{JsonValue as V, parse_json};
use opensip_platform::WorkLedger;

const CMS: &[u8] = include_bytes!("../../../tools/security/inputs/manifest-schema.json");

// The pinned matrix projection's nine pairs (the D4 plan r2's Q3 ruling), in
// order; D4-2 pins the host's table to the embedded matrix itself.
const RELATIONS: &[(&str, &str)] = &[
    ("calls", "resolved-callee"),
    ("control-flow", "syntactic"),
    ("declares", "syntactic"),
    ("imports", "resolved-target"),
    ("literal", "syntactic"),
    ("reachability", "from-resolved-calls"),
    ("references", "resolved-binding"),
    ("types", "checked"),
    ("unresolved-edge", "observed"),
];
const RESERVED: &[&str] = &["analyze", "doctor", "help", "version"];

fn d(b: u8) -> [u8; 32] {
    [b; 32]
}

const ROOT: &[CommandClaim<'static>] = &[
    CommandClaim {
        name: "tsa",
        parent: None,
        aliases: &["ts-analyzer"],
    },
    CommandClaim {
        name: "check",
        parent: Some("tsa"),
        aliases: &[],
    },
];
const IMPORTS: &[CapabilityClaim<'static>] = &[CapabilityClaim {
    capability_id: "typescript.imports",
    relation: "imports",
    rung: "resolved-target",
}];

fn analyzer(digest: u8) -> ManifestClaims<'static> {
    ManifestClaims {
        manifest_digest: d(digest),
        role: Role::Analyzer,
        name: "tsa",
        aliases: &["typescript-analyzer"],
        commands: Some(ROOT),
        capabilities: IMPORTS,
        provenance: ReleaseProvenance {
            publisher: "opensip",
            source_class: SourceClass::FirstParty,
        },
    }
}
fn closure(digest: u8, role: Role) -> ManifestClaims<'static> {
    ManifestClaims {
        manifest_digest: d(digest),
        role,
        name: "node-runtime",
        aliases: &[],
        commands: None,
        capabilities: &[],
        provenance: ReleaseProvenance {
            publisher: "opensip",
            source_class: SourceClass::FirstParty,
        },
    }
}

/// Run `admit` on a fresh ledger at the global caps.
fn run(claims: &[ManifestClaims<'_>], trusted: &[&str]) -> Result<Cleared, Refusal> {
    let mut ledger = WorkLedger::new();
    ledger
        .scope::<_, ()>(|w| {
            let policy = AdmissionPolicy::new(RESERVED, RELATIONS, trusted, w).unwrap();
            Ok(admit(claims, &policy, w))
        })
        .unwrap()
}
fn forms(r: Result<Cleared, Refusal>) -> Vec<(ExcludedFormClass, Arm, [u8; 32])> {
    match r {
        Err(Refusal::Excluded(v)) => v
            .iter()
            .map(|f| (f.class, f.arm, f.manifest_digest))
            .collect(),
        other => panic!("not an excluded-form refusal: {other:?}"),
    }
}

// ------------------------------------------------------------------ D4-T4

#[test]
fn d4t4_positive_mounted_root_and_closure_only_roles_pass() {
    let mut claims = vec![analyzer(1)];
    for (i, role) in [
        Role::Toolchain,
        Role::Stdlib,
        Role::RustDevLlvm,
        Role::Grammar,
    ]
    .into_iter()
    .enumerate()
    {
        claims.push(closure(2 + i as u8, role));
    }
    let cleared = run(&claims, &[]).unwrap();
    assert_eq!(cleared.digests(), &[d(1), d(2), d(3), d(4), d(5)]);
}

#[test]
fn d4t4_a_closure_only_role_declaring_commands_refuses() {
    for commands in [ROOT, &[][..]] {
        let mut c = closure(7, Role::Grammar);
        c.commands = Some(commands);
        assert_eq!(
            forms(run(&[c], &[])),
            vec![(ExcludedFormClass::Ee5a, Arm::ClosureOnlyCommands, d(7))]
        );
    }
}

#[test]
fn d4t4_b_a_root_outside_the_mounted_root_model_refuses() {
    const TWO: &[CommandClaim<'static>] = &[
        CommandClaim {
            name: "tsa",
            parent: None,
            aliases: &[],
        },
        CommandClaim {
            name: "other",
            parent: None,
            aliases: &[],
        },
    ];
    const MISNAMED: &[CommandClaim<'static>] = &[CommandClaim {
        name: "other",
        parent: None,
        aliases: &[],
    }];
    const NONE: &[CommandClaim<'static>] = &[CommandClaim {
        name: "check",
        parent: Some("tsa"),
        aliases: &[],
    }];
    for commands in [Some(TWO), Some(MISNAMED), Some(NONE), None] {
        let mut c = analyzer(3);
        c.commands = commands;
        assert_eq!(
            forms(run(&[c], &[])),
            vec![(ExcludedFormClass::Ee5a, Arm::RootModel, d(3))]
        );
    }
}

#[test]
fn d4t4_c_each_reserved_root_key_refuses() {
    const RESERVED_ROOT_ALIAS: &[CommandClaim<'static>] = &[CommandClaim {
        name: "tsa",
        parent: None,
        aliases: &["help"],
    }];
    let mut by_name = closure(4, Role::Stdlib);
    by_name.name = "doctor";
    let mut by_alias = analyzer(5);
    by_alias.aliases = &["version"];
    let mut by_root_alias = analyzer(6);
    by_root_alias.commands = Some(RESERVED_ROOT_ALIAS);
    for c in [by_name, by_alias, by_root_alias] {
        let digest = c.manifest_digest;
        assert_eq!(
            forms(run(&[c], &[])),
            vec![(ExcludedFormClass::Ee5a, Arm::ReservedRoot, digest)]
        );
    }
}

// ------------------------------------------------------------------ D4-T1's interface half

#[test]
fn d4t1_ee1_an_unlisted_explicitly_trusted_publisher_refuses() {
    let mut c = analyzer(8);
    c.provenance = ReleaseProvenance {
        publisher: "acme",
        source_class: SourceClass::ExplicitlyTrusted,
    };
    // At M3 the list is empty (LD-D4-3).
    assert_eq!(
        forms(run(&[c], &[])),
        vec![(ExcludedFormClass::Ee1, Arm::UnlistedPublisher, d(8))]
    );
    assert_eq!(
        forms(run(&[c], &["acme-other", "zeta"])),
        vec![(ExcludedFormClass::Ee1, Arm::UnlistedPublisher, d(8))]
    );
    assert_eq!(run(&[c], &["acme", "zeta"]).unwrap().digests(), &[d(8)]);
    // A first-party publisher passes whatever the list holds.
    assert_eq!(run(&[analyzer(9)], &["acme"]).unwrap().digests(), &[d(9)]);
}

#[test]
fn d4t1_ee3b_a_relation_outside_the_provider_projection_refuses() {
    // The matrix's fact and candidate-only members are not provider
    // capabilities: inventory and clones-fact relations refuse.
    for (relation, rung) in [
        ("file", "enumerated"),
        ("package", "manifest-declared"),
        ("vcs-change", "vcs-reported"),
        ("clones", "normalized-body-hash"),
        ("imports", "resolved-binding"),
    ] {
        let capabilities = [
            IMPORTS[0],
            CapabilityClaim {
                capability_id: "typescript.imports",
                relation,
                rung,
            },
        ];
        let mut c = analyzer(10);
        c.capabilities = &capabilities;
        assert_eq!(
            forms(run(&[c], &[])),
            vec![(ExcludedFormClass::Ee3b, Arm::UnmatchedCapability, d(10))]
        );
    }
    // Each provider pair passes.
    for &(relation, rung) in RELATIONS {
        let capabilities = [CapabilityClaim {
            capability_id: "x",
            relation,
            rung,
        }];
        let mut c = analyzer(11);
        c.capabilities = &capabilities;
        assert!(run(&[c], &[]).is_ok(), "{relation} {rung}");
    }
}

#[test]
fn d4t1_every_form_in_digest_then_class_order_whatever_the_input_order() {
    let caps = [CapabilityClaim {
        capability_id: "x",
        relation: "file",
        rung: "enumerated",
    }];
    let mut three = analyzer(0x30);
    three.provenance.source_class = SourceClass::ExplicitlyTrusted;
    three.capabilities = &caps;
    three.aliases = &["help"];
    let mut one = closure(0x10, Role::Toolchain);
    one.commands = Some(ROOT);
    let clean = analyzer(0x20);
    let expected = vec![
        (ExcludedFormClass::Ee5a, Arm::ClosureOnlyCommands, d(0x10)),
        (ExcludedFormClass::Ee1, Arm::UnlistedPublisher, d(0x30)),
        (ExcludedFormClass::Ee3b, Arm::UnmatchedCapability, d(0x30)),
        (ExcludedFormClass::Ee5a, Arm::ReservedRoot, d(0x30)),
    ];
    for order in [
        [one, clean, three],
        [three, clean, one],
        [clean, three, one],
        [three, one, clean],
    ] {
        assert_eq!(forms(run(&order, &[])), expected);
    }
    // The projected pair is the least refused digest and its first class.
    assert_eq!(expected[0].2, d(0x10));
}

#[test]
fn d4t1_sorted_cleared_whatever_the_input_order_and_the_empty_set() {
    let want = [d(1), d(2), d(3), d(4), d(5), d(6), d(7)];
    for order in [
        [1u8, 2, 3, 4, 5, 6, 7],
        [7, 6, 5, 4, 3, 2, 1],
        [4, 1, 7, 2, 6, 3, 5],
    ] {
        let claims: Vec<_> = order.iter().map(|&b| analyzer(b)).collect();
        assert_eq!(run(&claims, &[]).unwrap().digests(), &want);
    }
    assert_eq!(run(&[], &[]).unwrap().digests(), &[] as &[[u8; 32]]);
}

#[test]
fn d4t1_a_repeated_digest_is_a_host_invariant_refusal() {
    assert_eq!(
        run(&[analyzer(1), closure(2, Role::Stdlib), analyzer(1)], &[]).unwrap_err(),
        Refusal::Invariant(InvariantFault::DuplicateDigest)
    );
}

#[test]
fn policy_slices_must_be_strictly_ascending() {
    let mut ledger = WorkLedger::new();
    ledger
        .scope::<_, ()>(|w| {
            assert_eq!(
                AdmissionPolicy::new(&["b", "a"], RELATIONS, &[], w).unwrap_err(),
                PolicyRefusal::Unordered(PolicySlice::ReservedRoots)
            );
            assert_eq!(
                AdmissionPolicy::new(RESERVED, &[("a", "x"), ("a", "x")], &[], w).unwrap_err(),
                PolicyRefusal::Unordered(PolicySlice::ProviderRelations)
            );
            assert_eq!(
                AdmissionPolicy::new(RESERVED, RELATIONS, &["z", "a"], w).unwrap_err(),
                PolicyRefusal::Unordered(PolicySlice::ExplicitlyTrusted)
            );
            // Empty slices are lawful: nothing reserved, nothing provided.
            let empty = AdmissionPolicy::new(&[], &[], &[], w).unwrap();
            assert!(matches!(
                admit(&[analyzer(1)], &empty, w),
                Err(Refusal::Excluded(ref v)) if v.len() == 1 && v[0].class == ExcludedFormClass::Ee3b
            ));
            assert_eq!(
                admit(&[closure(2, Role::Grammar)], &empty, w)
                    .unwrap()
                    .digests(),
                &[d(2)]
            );
            Ok(())
        })
        .unwrap();
}

// ------------------------------------------------------------------ RF-1: independent accounting

/// The test's own model of every charge `admit` must make, in order,
/// computed from the input: its own merge sort and binary search count the
/// comparisons, and the sizes come from the types (LD-D4-8, LD-D4-10).
fn model(claims: &[ManifestClaims<'_>], trusted: &[&str]) -> Vec<WorkCost> {
    let edge = WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    };
    let mut log = Vec::new();
    let n = claims.len();
    log.push(WorkCost {
        objects: 2,
        edges: 0,
        bytes: n * 2 * 4,
    });
    // Bottom-up merge sort, counting comparisons.
    let mut idx: Vec<usize> = (0..n).collect();
    let mut width = 1;
    while width < n {
        let mut next = Vec::with_capacity(n);
        let mut low = 0;
        while low < n {
            let mid = (low + width).min(n);
            let high = (low + 2 * width).min(n);
            let (mut i, mut j) = (low, mid);
            while i < mid && j < high {
                log.push(edge);
                if claims[idx[j]].manifest_digest < claims[idx[i]].manifest_digest {
                    next.push(idx[j]);
                    j += 1;
                } else {
                    next.push(idx[i]);
                    i += 1;
                }
            }
            next.extend_from_slice(&idx[i..mid]);
            next.extend_from_slice(&idx[j..high]);
            low = high;
        }
        idx = next;
        width *= 2;
    }
    for _ in 1..n.max(1) {
        log.push(edge);
    }
    fn search<T: Ord>(slice: &[T], key: &T, log: &mut Vec<WorkCost>) -> bool {
        let edge = WorkCost {
            objects: 0,
            edges: 1,
            bytes: 0,
        };
        if slice.is_empty() {
            log.push(edge);
            return false;
        }
        let (mut lo, mut hi) = (0, slice.len());
        while lo < hi {
            let mid = (lo + hi) / 2;
            log.push(edge);
            match slice[mid].cmp(key) {
                std::cmp::Ordering::Less => lo = mid + 1,
                std::cmp::Ordering::Greater => hi = mid,
                std::cmp::Ordering::Equal => return true,
            }
        }
        false
    }
    let pass = |log: &mut Vec<WorkCost>| -> usize {
        let mut k = 0;
        for &i in &idx {
            let c = &claims[i];
            log.push(edge);
            if c.provenance.source_class == SourceClass::ExplicitlyTrusted
                && !search(trusted, &c.provenance.publisher, log)
            {
                k += 1;
            }
            for cap in c.capabilities {
                if !search(RELATIONS, &(cap.relation, cap.rung), log) {
                    k += 1;
                    break;
                }
            }
            log.push(edge);
            if c.role != Role::Analyzer && c.commands.is_some() {
                k += 1;
                continue;
            }
            let mut root = None;
            if c.role == Role::Analyzer {
                let mut roots = 0;
                for cmd in c.commands.unwrap_or(&[]) {
                    log.push(edge);
                    if cmd.parent.is_none() {
                        roots += 1;
                        root = Some(cmd);
                    }
                }
                if roots != 1 {
                    k += 1;
                    continue;
                }
                log.push(edge);
                if root.unwrap().name != c.name {
                    k += 1;
                    continue;
                }
            }
            let mut keys = vec![c.name];
            keys.extend_from_slice(c.aliases);
            keys.extend_from_slice(root.map_or(&[][..], |r| r.aliases));
            for key in keys {
                if search(RESERVED, &key, log) {
                    k += 1;
                    break;
                }
            }
        }
        k
    };
    let k = pass(&mut log);
    if k > 0 {
        log.push(WorkCost {
            objects: 1,
            edges: 0,
            bytes: k * size_of::<ExcludedForm>(),
        });
        pass(&mut log);
    } else {
        log.push(WorkCost {
            objects: 1,
            edges: 0,
            bytes: n * 32,
        });
        for _ in 0..n {
            log.push(edge);
        }
    }
    log
}

fn sum(costs: &[WorkCost]) -> WorkCost {
    costs
        .iter()
        .fold(WorkCost::default(), |a, &c| a.checked_add(c).unwrap())
}

fn policy_cost(trusted: &[&str]) -> WorkCost {
    WorkCost {
        objects: 0,
        edges: (RESERVED.len() - 1) + (RELATIONS.len() - 1) + trusted.len().saturating_sub(1),
        bytes: 0,
    }
}

// ------------------------------------------------------------------ RF-1 r2: the operation-order oracle

/// Arm the oracle, run `f`, and return what it recorded.
fn recorded<T>(f: impl FnOnce() -> T) -> (T, Vec<Operation>) {
    OPERATIONS.with(|log| *log.borrow_mut() = Some(Vec::new()));
    let out = f();
    let log = OPERATIONS.with(|log| log.borrow_mut().take()).unwrap();
    (out, log)
}

/// The oracle's grammar (`codex-d4-1-r1` RF-1): the log is a sequence of
/// blocks, each a charge followed by exactly the work it funds, with no work
/// outside a block. A two-object charge funds two allocations (the index
/// buffers), a one-object charge one allocation (the result), and a
/// one-edge charge one comparison or one push. So every comparison,
/// allocation and fill push is preceded by its own charge, and a refused
/// charge (which is not recorded) has no work after it. Returns the charges.
fn blocks(log: &[Operation]) -> Vec<WorkCost> {
    let mut charges = Vec::new();
    let mut i = 0;
    while i < log.len() {
        let Operation::Charged(cost) = log[i] else {
            panic!(
                "work at {i} with no charge before it: {:?}",
                &log[i.saturating_sub(3)..(i + 1).min(log.len())]
            )
        };
        let funded: &[&[Operation]] = match (cost.objects, cost.edges) {
            (2, 0) => &[&[Operation::Allocated], &[Operation::Allocated]],
            (1, 0) => &[&[Operation::Allocated]],
            (0, 1) => &[&[Operation::Compared, Operation::Pushed]],
            _ => panic!("an unknown charge {cost:?}"),
        };
        for (k, allowed) in funded.iter().enumerate() {
            let at = log
                .get(i + 1 + k)
                .unwrap_or_else(|| panic!("charge at {i} without its work"));
            assert!(
                allowed.contains(at),
                "charge at {i} funds {allowed:?}, then {at:?}"
            );
        }
        charges.push(cost);
        i += 1 + funded.len();
    }
    charges
}

/// Every charge site: the exact total; the oracle's charges equal the
/// model's, in order, and every work site follows its own charge; then, for
/// a scope one unit short of each site, `Budget`, with the ledger's prefix
/// and the oracle's blocks both stopping exactly before that site, so no
/// work at or past it occurred (not merely no further debit).
fn accounting(claims: &[ManifestClaims<'_>], trusted: &[&str]) {
    let log = model(claims, trusted);
    let pre = policy_cost(trusted);
    let mut ledger = WorkLedger::new();
    let (used, ops) = ledger
        .scope::<_, ()>(|w| {
            let policy = AdmissionPolicy::new(RESERVED, RELATIONS, trusted, w).unwrap();
            let before = w.used();
            let (result, ops) = recorded(|| admit(claims, &policy, w));
            match &result {
                Err(Refusal::Excluded(v)) => {
                    assert_eq!(v.capacity(), v.len(), "the vector is exact")
                }
                Ok(c) => assert_eq!(c.digests.capacity(), c.digests.len(), "the list is exact"),
                other => panic!("{other:?}"),
            }
            Ok(((before, w.used()), ops))
        })
        .unwrap();
    assert_eq!(used.0, pre);
    assert_eq!(used.1, pre.checked_add(sum(&log)).unwrap(), "exact total");
    assert_eq!(
        blocks(&ops),
        log,
        "the charges, in order, each before its work"
    );
    let filler = WorkCost {
        objects: 1,
        edges: 1,
        bytes: 1,
    };
    for site in 0..log.len() {
        let before = pre
            .checked_add(sum(&log[..site]))
            .unwrap()
            .checked_add(filler)
            .unwrap();
        let at = log[site];
        // The global caps (`work_ledger.rs`:12-14): `with_limits` may only lower them.
        let caps = (65_536, 131_072, 268_435_456);
        let limits = if at.objects > 0 {
            WorkCost {
                objects: before.objects + at.objects - 1,
                edges: caps.1,
                bytes: caps.2,
            }
        } else if at.edges > 0 {
            WorkCost {
                objects: caps.0,
                edges: before.edges + at.edges - 1,
                bytes: caps.2,
            }
        } else {
            WorkCost {
                objects: caps.0,
                edges: caps.1,
                bytes: before.bytes + at.bytes - 1,
            }
        };
        let mut tight = WorkLedger::with_limits(limits).unwrap();
        tight.charge::<()>(filler).unwrap();
        let mut ops = Vec::new();
        let outcome = tight.scope::<_, ()>(|w| {
            let policy = AdmissionPolicy::new(RESERVED, RELATIONS, trusted, w).unwrap();
            let (result, recorded_ops) = recorded(|| admit(claims, &policy, w));
            ops = recorded_ops;
            Ok(result)
        });
        assert!(
            matches!(
                outcome,
                Ok(Err(Refusal::Budget(_))) | Err(WorkFailure::Budget(_))
            ),
            "site {site}: {outcome:?}"
        );
        assert_eq!(
            tight.used(),
            before,
            "site {site}: nothing charged at or past it"
        );
        assert_eq!(
            blocks(&ops),
            log[..site],
            "site {site}: no work at or past it"
        );
    }
}

#[test]
fn rf1_policy_order_checks_charge_before_each_comparison() {
    let trusted: &[&str] = &["alpha", "beta", "gamma"];
    let mut ledger = WorkLedger::new();
    let ops = ledger
        .scope::<_, ()>(|w| {
            let (policy, ops) = recorded(|| AdmissionPolicy::new(RESERVED, RELATIONS, trusted, w));
            policy.unwrap();
            Ok(ops)
        })
        .unwrap();
    let edge = WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    };
    let sites = policy_cost(trusted).edges;
    assert_eq!(blocks(&ops), vec![edge; sites]);
    for site in 0..sites {
        let mut tight = WorkLedger::with_limits(WorkCost {
            objects: 65_536,
            edges: site + 1,
            bytes: 268_435_456,
        })
        .unwrap();
        tight.charge::<()>(edge).unwrap();
        let mut ops = Vec::new();
        let outcome = tight.scope::<_, ()>(|w| {
            let (policy, recorded_ops) =
                recorded(|| AdmissionPolicy::new(RESERVED, RELATIONS, trusted, w));
            ops = recorded_ops;
            Ok(policy.map(drop))
        });
        assert!(
            matches!(
                outcome,
                Ok(Err(PolicyRefusal::Budget(_))) | Err(WorkFailure::Budget(_))
            ),
            "site {site}: {outcome:?}"
        );
        assert_eq!(
            blocks(&ops),
            vec![edge; site],
            "site {site}: no comparison at or past it"
        );
    }
}

/// The source-order guard beside the oracle: every charge, comparison and
/// allocation of the module goes through its one recording wrapper, so the
/// oracle sees every site.
#[test]
fn rf1_every_site_goes_through_its_recording_wrapper() {
    let source = include_str!("manifest.rs");
    let production = &source[..source.find("#[cfg(test)]\n#[path").unwrap()];
    assert_eq!(
        production.matches("work.charge::<()>(").count(),
        1,
        "one raw charge, inside charge()"
    );
    assert_eq!(
        production.matches("Vec::with_capacity(").count(),
        1,
        "one raw allocation, inside reserve()"
    );
    assert_eq!(
        production.matches(".cmp(").count(),
        1,
        "one raw comparison, inside ordered()"
    );
    assert_eq!(
        production.matches(".push(").count(),
        3,
        "the oracle's own, the refusal vector's fill and the Cleared fill"
    );
    assert_eq!(
        production.matches("forms.push(f)").count(),
        1,
        "the refusal vector's fill, within its exact capacity"
    );
}

#[test]
fn rf1_accounting_on_cleared_sets_in_every_order() {
    let a: Vec<_> = [5u8, 1, 4, 2, 3].iter().map(|&b| analyzer(b)).collect();
    accounting(&a, &[]);
    let mut r = a.clone();
    r.reverse();
    accounting(&r, &[]);
    accounting(&[], &[]);
    accounting(&[closure(9, Role::Grammar)], &[]);
}

#[test]
fn rf1_accounting_on_refused_sets_with_several_classes_and_a_trust_list() {
    let caps = [
        IMPORTS[0],
        CapabilityClaim {
            capability_id: "x",
            relation: "clones",
            rung: "normalized-body-hash",
        },
    ];
    let mut multi = analyzer(0x40);
    multi.provenance.source_class = SourceClass::ExplicitlyTrusted;
    multi.provenance.publisher = "acme";
    multi.capabilities = &caps;
    multi.aliases = &["version"];
    let mut listed = analyzer(0x41);
    listed.provenance = ReleaseProvenance {
        publisher: "beta",
        source_class: SourceClass::ExplicitlyTrusted,
    };
    let mut bad = closure(0x11, Role::Stdlib);
    bad.commands = Some(&[]);
    let set = [multi, analyzer(0x22), listed, bad];
    accounting(&set, &["beta", "gamma"]);
    accounting(&[bad, listed, multi], &["alpha", "beta", "gamma", "zeta"]);
    accounting(&set, &[]);
}

#[test]
fn rf1_reference_bounds_dominate_the_model() {
    // The bottom-up merge sort's comparison count, on reversed, sorted and
    // interleaved inputs of every size up to 64.
    fn comparisons(keys: &[u32]) -> usize {
        let n = keys.len();
        let mut idx: Vec<usize> = (0..n).collect();
        let mut count = 0;
        let mut width = 1;
        while width < n {
            let mut next = Vec::with_capacity(n);
            let mut low = 0;
            while low < n {
                let mid = (low + width).min(n);
                let high = (low + 2 * width).min(n);
                let (mut i, mut j) = (low, mid);
                while i < mid && j < high {
                    count += 1;
                    if keys[idx[j]] < keys[idx[i]] {
                        next.push(idx[j]);
                        j += 1;
                    } else {
                        next.push(idx[i]);
                        i += 1;
                    }
                }
                next.extend_from_slice(&idx[i..mid]);
                next.extend_from_slice(&idx[j..high]);
                low = high;
            }
            idx = next;
            width *= 2;
        }
        count
    }
    for n in 0..65u32 {
        for keys in [
            (0..n).rev().collect::<Vec<_>>(),
            (0..n).collect(),
            (0..n).map(|x| (x * 7919) % (n + 1)).collect(),
        ] {
            assert!(
                comparisons(&keys) <= sort_reference_comparisons(n as usize),
                "n {n}"
            );
        }
    }
    for m in 0..20usize {
        let slice: Vec<u32> = (0..m as u32).map(|x| 2 * x).collect();
        for key in 0..(2 * m as u32 + 2) {
            let mut log = Vec::new();
            let mut lo = 0;
            let mut hi = slice.len();
            if slice.is_empty() {
                log.push(());
            }
            while lo < hi {
                let mid = (lo + hi) / 2;
                log.push(());
                match slice[mid].cmp(&key) {
                    std::cmp::Ordering::Less => lo = mid + 1,
                    std::cmp::Ordering::Greater => hi = mid,
                    std::cmp::Ordering::Equal => break,
                }
            }
            assert!(
                log.len() <= probe_reference_comparisons(m),
                "m {m} key {key}"
            );
        }
    }
}

// ------------------------------------------------------------------ closed-world pins (LD-D4-5)

fn object(v: &V) -> &std::collections::BTreeMap<String, V> {
    match v {
        V::Object(o) => o,
        _ => panic!("not an object"),
    }
}
fn keys(v: &V) -> Vec<&str> {
    object(&object(v)["properties"])
        .keys()
        .map(String::as_str)
        .collect()
}

#[test]
fn closed_world_cms_property_sets_are_pinned() {
    let cms = parse_json(CMS).unwrap();
    let defs = object(&object(&cms)["$defs"]);
    // Any change here must be judged against EE-4's manifest part (and
    // EE-1, EE-3b, EE-5a) before it lands: re-review the D4 plan.
    assert_eq!(
        keys(&cms),
        [
            "aliases",
            "capabilities",
            "closureProtocolMajor",
            "commands",
            "compatibility",
            "configuration",
            "declarations",
            "dependencies",
            "displayName",
            "kind",
            "manifestSchemaVersion",
            "name",
            "permissions",
            "platforms",
            "prerequisites",
            "provenance",
            "role",
            "stableId",
            "stateMigration",
            "updateData",
            "version"
        ]
    );
    assert_eq!(
        keys(&object(&object(&cms)["properties"])["provenance"]),
        ["publisher", "sourceClass"]
    );
    let V::Array(capability) = &object(&defs["capability"])["oneOf"] else {
        panic!("capability is a oneOf")
    };
    assert_eq!(capability.len(), 5);
    for branch in capability {
        assert_eq!(
            keys(branch),
            [
                "capabilityId",
                "declarationData",
                "roleSubprotocol",
                "subprotocolVersion"
            ]
        );
        assert_eq!(
            keys(&object(&object(branch)["properties"])["declarationData"]),
            ["relation", "rung"]
        );
    }
    assert_eq!(
        keys(&defs["platform"]),
        ["arch", "entrypoint", "os", "tree"]
    );
    let V::Array(entry) = &object(&defs["entry"])["oneOf"] else {
        panic!("entry is a oneOf")
    };
    let entry: Vec<_> = entry.iter().map(keys).collect();
    assert_eq!(
        entry,
        [
            vec!["length", "mode", "path", "sha256", "type"],
            vec!["mode", "path", "type"],
            vec!["mode", "path", "target", "type"]
        ]
    );
    assert_eq!(
        keys(&defs["command"]),
        [
            "aliases",
            "args",
            "description",
            "name",
            "options",
            "outputModes",
            "parent",
            "scope",
            "visibility"
        ]
    );
    assert_eq!(
        keys(&defs["dependency"]),
        ["reason", "stableId", "versionConstraint"]
    );
}

#[test]
fn closed_world_claim_types_and_classes_are_pinned() {
    // Exhaustive patterns: a new field or member fails to compile here,
    // which forces its review against item 24 before it lands.
    let ManifestClaims {
        manifest_digest: _,
        role: _,
        name: _,
        aliases: _,
        commands: _,
        capabilities: _,
        provenance:
            ReleaseProvenance {
                publisher: _,
                source_class: _,
            },
    } = analyzer(1);
    let CommandClaim {
        name: _,
        parent: _,
        aliases: _,
    } = ROOT[0];
    let CapabilityClaim {
        capability_id: _,
        relation: _,
        rung: _,
    } = IMPORTS[0];
    let all = [
        ExcludedFormClass::Ee1,
        ExcludedFormClass::Ee2,
        ExcludedFormClass::Ee3b,
        ExcludedFormClass::Ee4,
        ExcludedFormClass::Ee5a,
        ExcludedFormClass::Ee6a,
    ];
    for c in all {
        match c {
            ExcludedFormClass::Ee1
            | ExcludedFormClass::Ee2
            | ExcludedFormClass::Ee3b
            | ExcludedFormClass::Ee4
            | ExcludedFormClass::Ee5a
            | ExcludedFormClass::Ee6a => {}
        }
    }
    assert!(all.windows(2).all(|p| p[0] < p[1]), "the documented order");
}
