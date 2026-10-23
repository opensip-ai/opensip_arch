//! M3-D r5 item 24 (unit D4-2; D4 plan r2, LD-D4-2 to LD-D4-4, LD-D4-13):
//! the host's adapter for R10a's and ER10a's excluded-form judge. It
//! projects the trust owner's `AdmissionView` into components' borrowed
//! `ManifestClaims`, builds the `AdmissionPolicy` (the reader's own reserved
//! list, the pinned provider-relation table, and the empty M3 explicit-trust
//! list), and runs `opensip_components::manifest::admit`. It parses nothing:
//! every value it reads is the security owner's validated manifest or the
//! catalog release row the ordinary reader joined. Every allocation, lookup
//! and comparison is charged on the caller's borrowed scope before it is
//! made; it selects no profile (LD-D4-SD9). Its production caller is R10a's
//! wiring (J3d, J2c, with C2a-4); none exists yet.
use opensip_components::manifest::{
    self, AdmissionPolicy, CapabilityClaim, Cleared, CommandClaim, ExcludedForm, InvariantFault,
    ManifestClaims, PolicyRefusal, PolicySlice, Refusal, ReleaseProvenance, Role, SourceClass,
};
use opensip_identity::JsonValue as V;
use opensip_platform::{WorkBudgetError, WorkCost, WorkFailure, WorkScope};
use opensip_security::{AdmissionView, AuthenticatedComponent};
use std::collections::BTreeMap;

/// The native capability matrix's provider relations (LD-D4-4): the
/// `(relation, rung)` pairs of every `capabilities[]` member of the embedded
/// `native_capability_matrix.v2.json` whose `authority` is neither `fact`
/// nor `candidate-only`, ascending. A test pins it to the embedded matrix
/// member by member, in order. It separates the matrix's authority classes
/// and authorizes nothing outside the manifest schema's closed branches.
pub(crate) static PROVIDER_RELATIONS: [(&str, &str); 9] = [
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

/// The explicit-trust list at M3: empty (LD-D4-3; `codex-d4-plan-r1` Q1).
pub(crate) static EXPLICITLY_TRUSTED: [&str; 0] = [];

/// Why the adapter did not clear the view.
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum AdmissionFailure {
    /// Every excluded form, as `manifest::admit` returns them (SD-5's order).
    Excluded(Vec<ExcludedForm>),
    /// A host-invariant fault: a repeated digest, an unordered policy
    /// slice, or a validated value without a field its schema requires.
    Invariant(Fault),
    Budget(WorkBudgetError),
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Fault {
    Judge(InvariantFault),
    Policy(PolicySlice),
    Projection,
}

type Step<T> = Result<T, AdmissionFailure>;

fn budget(failure: WorkFailure<()>) -> AdmissionFailure {
    match failure {
        WorkFailure::Budget(b) => AdmissionFailure::Budget(b),
        WorkFailure::Operation(()) => unreachable!("a charge has no operation failure"),
    }
}
fn edges(work: &mut WorkScope<'_>, n: usize) -> Step<()> {
    work.charge::<()>(WorkCost {
        objects: 0,
        edges: n,
        bytes: 0,
    })
    .map_err(budget)
}
/// One owned vector reserved for exactly `n` values of `T`, charged first.
fn reserve<T>(work: &mut WorkScope<'_>, n: usize) -> Step<Vec<T>> {
    work.charge::<()>(WorkCost {
        objects: 1,
        edges: 0,
        bytes: n.saturating_mul(size_of::<T>()),
    })
    .map_err(budget)?;
    Ok(Vec::with_capacity(n))
}
/// One member lookup in a validated object, charged before the search.
/// Rust 1.95 scans keys once within each visited B-tree node and descends
/// through disjoint nodes. It compares no more than the object's total
/// number of keys. This is a conservative bound, not an exact count; an
/// empty lookup retains one edge for its empty check. D4-1's logarithmic
/// sorted-slice probe price does not describe this map implementation.
fn member<'v>(
    object: &'v BTreeMap<String, V>,
    key: &str,
    work: &mut WorkScope<'_>,
) -> Step<Option<&'v V>> {
    edges(work, object.len().max(1))?;
    Ok(object.get(key))
}
fn object(v: &V) -> Step<&BTreeMap<String, V>> {
    match v {
        V::Object(o) => Ok(o),
        _ => Err(AdmissionFailure::Invariant(Fault::Projection)),
    }
}
fn text(v: &V) -> Step<&str> {
    match v {
        V::String(s) => Ok(s),
        _ => Err(AdmissionFailure::Invariant(Fault::Projection)),
    }
}
fn array(v: &V) -> Step<&[V]> {
    match v {
        V::Array(a) => Ok(a),
        _ => Err(AdmissionFailure::Invariant(Fault::Projection)),
    }
}
fn required<'v>(
    object: &'v BTreeMap<String, V>,
    key: &str,
    work: &mut WorkScope<'_>,
) -> Step<&'v V> {
    member(object, key, work)?.ok_or(AdmissionFailure::Invariant(Fault::Projection))
}
/// The optional string-array member `key` (absent is empty).
fn strings<'v>(
    object: &'v BTreeMap<String, V>,
    key: &str,
    work: &mut WorkScope<'_>,
) -> Step<&'v [V]> {
    match member(object, key, work)? {
        Some(v) => array(v),
        None => Ok(&[]),
    }
}

/// The role, by one charged comparison per candidate tried.
fn role(name: &str, work: &mut WorkScope<'_>) -> Step<Role> {
    for (spelling, role) in [
        ("analyzer", Role::Analyzer),
        ("toolchain", Role::Toolchain),
        ("stdlib", Role::Stdlib),
        ("rust-dev-llvm", Role::RustDevLlvm),
        ("grammar", Role::Grammar),
    ] {
        edges(work, 1)?;
        if name == spelling {
            return Ok(role);
        }
    }
    Err(AdmissionFailure::Invariant(Fault::Projection))
}
fn source_class(name: &str, work: &mut WorkScope<'_>) -> Step<SourceClass> {
    for (spelling, class) in [
        ("first-party", SourceClass::FirstParty),
        ("explicitly-trusted", SourceClass::ExplicitlyTrusted),
    ] {
        edges(work, 1)?;
        if name == spelling {
            return Ok(class);
        }
    }
    Err(AdmissionFailure::Invariant(Fault::Projection))
}
/// The release row's `manifestDigest`, 64 lowercase hex digits, decoded at
/// one charged edge per byte.
fn digest(hex: &str, work: &mut WorkScope<'_>) -> Step<[u8; 32]> {
    let raw = hex.as_bytes();
    if raw.len() != 64 {
        return Err(AdmissionFailure::Invariant(Fault::Projection));
    }
    let nibble = |b: u8| match b {
        b'0'..=b'9' => Some(b - b'0'),
        b'a'..=b'f' => Some(b - b'a' + 10),
        _ => None,
    };
    let mut out = [0u8; 32];
    for (i, pair) in raw.chunks_exact(2).enumerate() {
        edges(work, 1)?;
        let (Some(hi), Some(lo)) = (nibble(pair[0]), nibble(pair[1])) else {
            return Err(AdmissionFailure::Invariant(Fault::Projection));
        };
        out[i] = hi << 4 | lo;
    }
    Ok(out)
}

/// One component's fields as the claims need them, read from its validated
/// manifest and its release row; the string slices borrow those values.
struct Read<'a> {
    digest: [u8; 32],
    role: Role,
    name: &'a str,
    aliases: &'a [V],
    commands: Option<&'a [V]>,
    capabilities: &'a [V],
    publisher: &'a str,
    source_class: SourceClass,
}
fn read<'a>(component: &AuthenticatedComponent<'a>, work: &mut WorkScope<'_>) -> Step<Read<'a>> {
    let body = object(component.manifest())?;
    let release = object(component.release())?;
    let digest = digest(text(required(release, "manifestDigest", work)?)?, work)?;
    let publisher = text(required(release, "publisher", work)?)?;
    let source_class = source_class(text(required(release, "sourceClass", work)?)?, work)?;
    let role = role(text(required(body, "role", work)?)?, work)?;
    let name = text(required(body, "name", work)?)?;
    let aliases = strings(body, "aliases", work)?;
    let commands = match member(body, "commands", work)? {
        Some(v) => Some(array(v)?),
        None => None,
    };
    let capabilities = array(required(body, "capabilities", work)?)?;
    Ok(Read {
        digest,
        role,
        name,
        aliases,
        commands,
        capabilities,
        publisher,
        source_class,
    })
}

/// R10a's and ER10a's judge over the view (LD-C2A-1 step 2): the projection
/// in three charged passes, then the policy, then `manifest::admit`.
/// `Cleared` names the judged digests and authorizes nothing; the wiring
/// must compare it with the set it hands to C2a (X-D4P-4).
pub(crate) fn judge(view: &AdmissionView<'_>, work: &mut WorkScope<'_>) -> Step<Cleared> {
    let components = view.components();
    // The reserved list, borrowed in the reader's ascending order.
    let mut reserved: Vec<&str> = reserve(work, view.reserved_roots().len())?;
    for root in view.reserved_roots() {
        edges(work, 1)?;
        reserved.push(root);
    }
    // Pass 1: each component's fields, and the sizes the claims need.
    let mut reads: Vec<Read<'_>> = reserve(work, components.len())?;
    let (mut names, mut commands, mut capabilities) = (0usize, 0usize, 0usize);
    for component in components {
        let r = read(component, work)?;
        names = names.saturating_add(r.aliases.len());
        for command in r.commands.unwrap_or(&[]) {
            edges(work, 1)?;
            names = names.saturating_add(strings(object(command)?, "aliases", work)?.len());
        }
        commands = commands.saturating_add(r.commands.map_or(0, <[V]>::len));
        capabilities = capabilities.saturating_add(r.capabilities.len());
        edges(work, 1)?;
        reads.push(r);
    }
    // Pass 2: every alias spelling, manifest aliases then each command's,
    // into one exact list; and each capability's relation and rung.
    let mut spelled: Vec<&str> = reserve(work, names)?;
    let mut caps: Vec<CapabilityClaim<'_>> = reserve(work, capabilities)?;
    for r in &reads {
        for alias in r.aliases {
            edges(work, 1)?;
            spelled.push(text(alias)?);
        }
        for command in r.commands.unwrap_or(&[]) {
            for alias in strings(object(command)?, "aliases", work)? {
                edges(work, 1)?;
                spelled.push(text(alias)?);
            }
        }
        for capability in r.capabilities {
            let c = object(capability)?;
            let data = object(required(c, "declarationData", work)?)?;
            edges(work, 1)?;
            caps.push(CapabilityClaim {
                capability_id: text(required(c, "capabilityId", work)?)?,
                relation: text(required(data, "relation", work)?)?,
                rung: text(required(data, "rung", work)?)?,
            });
        }
    }
    // Pass 3: the commands, slicing the spelled aliases; then the claims.
    let mut tree: Vec<CommandClaim<'_>> = reserve(work, commands)?;
    let mut at = 0usize;
    for r in &reads {
        at += r.aliases.len();
        for command in r.commands.unwrap_or(&[]) {
            let c = object(command)?;
            let aliases = strings(c, "aliases", work)?.len();
            let parent = match member(c, "parent", work)? {
                Some(p) => Some(text(p)?),
                None => None,
            };
            edges(work, 1)?;
            tree.push(CommandClaim {
                name: text(required(c, "name", work)?)?,
                parent,
                aliases: &spelled[at..at + aliases],
            });
            at += aliases;
        }
    }
    let mut claims: Vec<ManifestClaims<'_>> = reserve(work, reads.len())?;
    let (mut name_at, mut command_at, mut capability_at) = (0usize, 0usize, 0usize);
    for r in &reads {
        let command_count = r.commands.map_or(0, <[V]>::len);
        let command_aliases: usize = tree[command_at..command_at + command_count]
            .iter()
            .map(|c| c.aliases.len())
            .sum();
        edges(work, 1)?;
        claims.push(ManifestClaims {
            manifest_digest: r.digest,
            role: r.role,
            name: r.name,
            aliases: &spelled[name_at..name_at + r.aliases.len()],
            commands: r
                .commands
                .map(|_| &tree[command_at..command_at + command_count]),
            capabilities: &caps[capability_at..capability_at + r.capabilities.len()],
            provenance: ReleaseProvenance {
                publisher: r.publisher,
                source_class: r.source_class,
            },
        });
        name_at += r.aliases.len() + command_aliases;
        command_at += command_count;
        capability_at += r.capabilities.len();
    }
    let policy = AdmissionPolicy::new(&reserved, &PROVIDER_RELATIONS, &EXPLICITLY_TRUSTED, work)
        .map_err(|e| match e {
            PolicyRefusal::Unordered(slice) => AdmissionFailure::Invariant(Fault::Policy(slice)),
            PolicyRefusal::Budget(b) => AdmissionFailure::Budget(b),
        })?;
    manifest::admit(&claims, &policy, work).map_err(|e| match e {
        Refusal::Excluded(forms) => AdmissionFailure::Excluded(forms),
        Refusal::Invariant(fault) => AdmissionFailure::Invariant(Fault::Judge(fault)),
        Refusal::Budget(b) => AdmissionFailure::Budget(b),
    })
}

#[cfg(test)]
#[path = "component_admission_tests.rs"]
mod tests;
