//! Law X3d r8 item 13 (unit X3d-3; X9 r5 and r7, item 6): the synthetic run
//! candidate, inputs only. It starts from the pinned corpus Run that
//! security's SEAL tests replay (`journal-seal-cases.json`, case
//! `packet-0-original`) and binds it to a real session:
//! - the snapshot's `projectId` becomes `CommitSession::project_id`;
//! - the evaluator closure becomes `CommitSession::core_evaluator_closure`
//!   (contract successor EC1), never `core_closure`. Its descriptor is
//!   retained as a closure object, with its manifest blob (the inventory
//!   body) and its tree blobs, from security's shared test-support accessor;
//! - every input content id and blob digest that depends on them is
//!   recomputed (a reference rewrite over the inputs, to a fixpoint);
//! - the outputs are re-derived with the evaluator's public
//!   `derive_evaluation`, and the evidence, seal and Run descriptors are
//!   built as `replay_run` checks them.
//!
//! It returns retained objects and blobs and the claimed RunId, never a
//! `ReplayedRun`: the evaluator's `replay_run` stays the only constructor of
//! the `ReplayedRun` that `prepare_commit` takes. Every run that uses it is
//! labelled `synthetic`. It lives in storage's `crash_matrix_support`, and
//! storage's own unit tests include this same file (X3d-3's positive tests).
use opensip_evaluator::{ReplayLimits, RetainedWalkLimits, derive_evaluation};
use opensip_identity::{
    IdentityDomain as D, JsonInteger, JsonValue as V, ObjectInput, RetainedInputs, TraversalBudget,
    canonical_bytes, digest_hex, hash_canonical_value, parse_json, raw_sha256,
};
use opensip_security::CommitSession;
use std::collections::{BTreeMap, BTreeSet};

/// The pinned corpus: security's SEAL replay fixture.
const CORPUS: &[u8] = include_bytes!("../../../security/tests/fixtures/journal-seal-cases.json");

/// The label every run that uses the candidate carries (X9 r1 item 6).
pub const SYNTHETIC_LABEL: &str = "synthetic";

/// The candidate: retained inputs and the claimed RunId. Inert values; it
/// grants nothing and is not a `ReplayedRun`.
pub struct SyntheticRunCandidate {
    run_id: String,
    objects: BTreeMap<String, ObjectInput>,
    blobs: BTreeMap<[u8; 32], Vec<u8>>,
}
impl std::fmt::Debug for SyntheticRunCandidate {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("SyntheticRunCandidate")
            .field("run_id", &self.run_id)
            .field("objects", &self.objects.len())
            .field("blobs", &self.blobs.len())
            .finish()
    }
}
impl SyntheticRunCandidate {
    /// The claimed RunId, for `replay_run`.
    pub fn run_id(&self) -> &str {
        &self.run_id
    }
    /// The retained typed objects, by identity.
    pub fn objects(&self) -> &BTreeMap<String, ObjectInput> {
        &self.objects
    }
    /// The retained raw blobs, by raw SHA-256.
    pub fn blobs(&self) -> &BTreeMap<[u8; 32], Vec<u8>> {
        &self.blobs
    }
    /// The retained inputs over storage's selected schema registry, for the
    /// caller's `replay_run`.
    pub fn retained_inputs(&self) -> RetainedInputs<'_> {
        RetainedInputs::new(registry(), &self.objects, &self.blobs)
    }
    /// The candidate's label.
    pub fn label(&self) -> &'static str {
        SYNTHETIC_LABEL
    }
}

/// The local replay bounds the candidate is built and replayed under.
pub fn synthetic_replay_limits() -> ReplayLimits {
    let bound = TraversalBudget {
        steps: 20_000_000,
        depth: 96,
        descriptor_work: 20_000_000,
    };
    ReplayLimits {
        retained: RetainedWalkLimits {
            walk: bound,
            owner: bound,
            owner_invocations: 100_000,
        },
        capture_entries: 100_000,
        retained_bytes: 32 * 1024 * 1024,
    }
}

fn registry() -> &'static opensip_identity::RegisteredSchemas {
    crate::schema_sources::registry().expect("storage's selected schema registry")
}
fn object(v: &V) -> &BTreeMap<String, V> {
    match v {
        V::Object(o) => o,
        _ => panic!("corpus: object"),
    }
}
fn string(v: &V) -> &str {
    match v {
        V::String(s) => s,
        _ => panic!("corpus: string"),
    }
}
fn array(v: &V) -> &[V] {
    match v {
        V::Array(a) => a,
        _ => panic!("corpus: array"),
    }
}
fn hex_bytes(s: &str) -> Vec<u8> {
    s.as_bytes()
        .chunks_exact(2)
        .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
        .collect()
}
fn digest(s: &str) -> [u8; 32] {
    hex_bytes(s).try_into().expect("a 32-byte digest")
}
/// `prefix:hex(H(domain, descriptor))`, the object identity recipe.
fn identity(domain: D, descriptor: &V) -> String {
    let h = hash_canonical_value(domain.name(), descriptor).expect("canonical descriptor");
    format!("{}:{}", domain.prefix(), digest_hex(&h))
}
fn hex_of(id: &str) -> &str {
    id.rsplit(':').next().unwrap()
}
fn int(n: i128) -> V {
    V::Integer(JsonInteger::new(n).unwrap())
}

/// One reference rewrite of a text: every mapped old text becomes its new
/// text.
fn substitute_text(text: &str, map: &[(String, String)]) -> String {
    let mut out = text.to_owned();
    for (old, new) in map {
        if out.contains(old.as_str()) {
            out = out.replace(old.as_str(), new);
        }
    }
    out
}
/// One reference rewrite of a value, in strings and member names. An array
/// that was in canonical byte order (a sorted id list, or refs ordered by
/// their leading `digest`) stays in that order.
fn substitute(value: &V, map: &[(String, String)]) -> V {
    match value {
        V::String(s) => V::String(substitute_text(s, map)),
        V::Array(a) => {
            let key = |v: &V| canonical_bytes(v).expect("canonical member");
            let sorted = a.windows(2).all(|w| key(&w[0]) <= key(&w[1]));
            let mut out: Vec<V> = a.iter().map(|v| substitute(v, map)).collect();
            if sorted {
                out.sort_by_key(key);
            }
            V::Array(out)
        }
        V::Object(o) => V::Object(
            o.iter()
                .map(|(k, v)| (substitute_text(k, map), substitute(v, map)))
                .collect(),
        ),
        other => other.clone(),
    }
}
/// A canonical JSON blob is rewritten as a value and re-encoded; any other
/// blob byte for byte, where every mapped text keeps its length (framed
/// binary blobs carry length prefixes).
fn substitute_blob(bytes: &[u8], map: &[(String, String)]) -> Vec<u8> {
    if let Ok(value) = parse_json(bytes)
        && canonical_bytes(&value).ok().as_deref() == Some(bytes)
    {
        return canonical_bytes(&substitute(&value, map)).expect("canonical blob");
    }
    let mut out = bytes.to_vec();
    for (old, new) in map {
        let (old, new) = (old.as_bytes(), new.as_bytes());
        let mut i = 0;
        while i + old.len() <= out.len() {
            if &out[i..i + old.len()] == old {
                assert_eq!(
                    old.len(),
                    new.len(),
                    "a framed blob's reference keeps its length"
                );
                out[i..i + old.len()].copy_from_slice(new);
                i += old.len();
            } else {
                i += 1;
            }
        }
    }
    out
}

/// Typed objects by identity, with their domains.
type Objects = BTreeMap<String, (D, V)>;
/// Raw blobs by raw SHA-256.
type Blobs = BTreeMap<[u8; 32], Vec<u8>>;

struct Corpus {
    run_id: String,
    objects: Objects,
    blobs: Blobs,
}
fn corpus() -> Corpus {
    let f = parse_json(CORPUS).expect("corpus");
    let f = object(&object(&f)["replay"]);
    let c = object(&f["case"]);
    assert_eq!(string(&c["label"]), "packet-0-original");
    let objects = array(&c["objects"])
        .iter()
        .map(|k| {
            let r = object(&object(&f["objectPool"])[string(k)]);
            (
                string(&r["id"]).to_owned(),
                (
                    D::parse(string(&r["domain"])).expect("domain"),
                    r["descriptor"].clone(),
                ),
            )
        })
        .collect();
    let blobs = array(&c["blobs"])
        .iter()
        .map(|k| {
            let r = object(&object(&f["blobPool"])[string(k)]);
            (digest(string(&r["digest"])), hex_bytes(string(&r["hex"])))
        })
        .collect();
    Corpus {
        run_id: string(&c["runId"]).to_owned(),
        objects,
        blobs,
    }
}
fn inputs_of(objects: &Objects) -> BTreeMap<String, ObjectInput> {
    objects
        .iter()
        .map(|(id, (domain, descriptor))| {
            (
                id.clone(),
                ObjectInput {
                    domain: *domain,
                    descriptor: descriptor.clone(),
                },
            )
        })
        .collect()
}

/// The session's core evaluator closure: its id, descriptor, manifest blob
/// (the inventory body) and tree blobs by logical path.
type Evaluator = (String, V, Vec<u8>, BTreeMap<String, Vec<u8>>);

/// Law X3d r8 item 13: the synthetic run candidate bound to `session`'s
/// project and core evaluator closure. Inputs only. Panics if the pinned
/// corpus cannot be rebound, as every fixture does.
pub fn synthetic_run_candidate(session: &CommitSession) -> SyntheticRunCandidate {
    bound_to(session, false)
}

/// Law X9 r12 (unit X9-3): the distinct variant of the candidate, for a
/// next writer whose project already committed the candidate's Run (F13,
/// F14, F15). It is built exactly as the candidate, for the same session's
/// `projectId` and core evaluator closure, except that the snapshot's
/// source file `extensionless` gets same-length salted bytes before the
/// fixpoint rewrite, so every dependent id and digest, the re-derived
/// outputs and the RunId differ. Inputs only; never a `ReplayedRun`.
#[cfg_attr(test, allow(dead_code))]
pub fn synthetic_run_candidate_distinct(session: &CommitSession) -> SyntheticRunCandidate {
    bound_to(session, true)
}

fn bound_to(session: &CommitSession, salted: bool) -> SyntheticRunCandidate {
    let evaluator = session.core_evaluator_closure().to_owned();
    let (descriptor, manifest, tree) = session.core_evaluator_closure_preimages();
    assert_eq!(identity(D::Closure, &descriptor), evaluator);
    assert_eq!(string(&object(&descriptor)["kind"]), "evaluator");
    assert_ne!(evaluator, session.core_closure());
    bind(
        session.project_id(),
        Some((evaluator, descriptor, manifest, tree)),
        salted,
    )
}

/// The distinct variant's salted source file and its same-length bytes.
const SALTED_PATH: &str = "extensionless";
const SALT: &[u8] = b"salted!\n";

/// The reference rewrite to a fixpoint: every item gets `map` applied, and
/// each item whose identity or digest changes adds its own old and new hex
/// to `map`, until nothing new is added.
fn rewrite(objects: &Objects, blobs: &Blobs, map: &mut Vec<(String, String)>) -> (Objects, Blobs) {
    loop {
        let mut added = Vec::new();
        let mut new_objects = BTreeMap::new();
        for (id, (domain, descriptor)) in objects {
            let rewritten = substitute(descriptor, map);
            let new_id = identity(*domain, &rewritten);
            if new_id != *id {
                added.push((hex_of(id).to_owned(), hex_of(&new_id).to_owned()));
            }
            new_objects.insert(new_id, (*domain, rewritten));
        }
        let mut new_blobs = BTreeMap::new();
        for (old, bytes) in blobs {
            let rewritten = substitute_blob(bytes, map);
            let new = raw_sha256(&rewritten);
            if new != *old {
                added.push((digest_hex(old), digest_hex(&new)));
            }
            new_blobs.insert(new, rewritten);
        }
        // An item may change again once a later pass maps one more of its
        // references, so an entry keeps the latest identity of its original.
        let before = map.clone();
        for (old, new) in added {
            match map.iter_mut().find(|(o, _)| *o == old) {
                Some(entry) => entry.1 = new,
                None => map.push((old, new)),
            }
        }
        if *map == before {
            return (new_objects, new_blobs);
        }
    }
}

/// The corpus Run rebound to `project`, and to `evaluator` when given (the
/// corpus's own evaluator closure is kept otherwise): the inputs rewritten,
/// then the outputs re-derived and the evidence, seal and Run built.
fn bind(project: &str, evaluator: Option<Evaluator>, salted: bool) -> SyntheticRunCandidate {
    let limits = synthetic_replay_limits().retained;
    let corpus = corpus();
    let get = |id: &str| &corpus.objects[id].1;
    let run = get(&corpus.run_id);
    let plan_id = string(&object(run)["planId"]);
    let seal = get(string(&object(run)["evaluationSealId"]));
    let proof_id = string(&object(seal)["proofBundleId"]);
    let proof = get(proof_id);
    let old_evaluator = string(&object(seal)["evaluatorClosure"]).to_owned();
    let old_project =
        string(&object(get(string(&object(get(plan_id))["snapshotId"])))["projectId"]).to_owned();

    // The outputs: what derive_evaluation derives over the corpus, and the
    // evidence, seal and Run that replay builds. Everything else is an input.
    let derived = {
        let objects = inputs_of(&corpus.objects);
        let inputs = RetainedInputs::new(registry(), &objects, &corpus.blobs);
        derive_evaluation(
            &inputs,
            plan_id,
            string(&object(seal)["executionPlanId"]),
            &old_evaluator,
            array(&object(proof)["evaluationInputRefs"]),
            limits,
        )
        .expect("the corpus derives")
    };
    let mut outputs: BTreeSet<String> = derived.objects().keys().cloned().collect();
    outputs.extend([
        corpus.run_id.clone(),
        string(&object(run)["evaluationSealId"]).to_owned(),
        string(&object(run)["evidenceId"]).to_owned(),
        proof_id.to_owned(),
    ]);
    let mut dropped: BTreeSet<[u8; 32]> = derived.blobs().keys().map(|k| digest(k)).collect();
    let mut map = vec![(old_project, project.to_owned())];

    // A replaced evaluator closure goes with its own manifest and tree blobs.
    if let Some((id, ..)) = &evaluator {
        let replaced = get(&old_evaluator);
        dropped.insert(digest(string(&object(replaced)["manifestDigest"])));
        for member in array(&object(replaced)["tree"]) {
            dropped.insert(digest(string(&object(member)["sha256"])));
        }
        outputs.insert(old_evaluator.clone());
        map.push((hex_of(&old_evaluator).to_owned(), hex_of(id).to_owned()));
    }
    let inputs: Objects = corpus
        .objects
        .iter()
        .filter(|(id, _)| !outputs.contains(*id))
        .map(|(id, v)| (id.clone(), v.clone()))
        .collect();
    let mut input_blobs: Blobs = corpus
        .blobs
        .iter()
        .filter(|(d, _)| !dropped.contains(*d))
        .map(|(d, b)| (*d, b.clone()))
        .collect();
    // X9 r12: the distinct variant's salt, before the rewrite, which then
    // carries the source file's new digest into every reference.
    if salted {
        let snapshot = get(string(&object(get(plan_id))["snapshotId"]));
        let entry = array(&object(snapshot)["sourceInventory"])
            .iter()
            .find(|e| string(&object(e)["path"]) == SALTED_PATH)
            .expect("the salted source file");
        let old = digest(string(&object(entry)["sha256"]));
        let bytes = input_blobs.remove(&old).expect("the salted file's bytes");
        assert_eq!(bytes.len(), SALT.len());
        assert_ne!(bytes, SALT);
        let new = raw_sha256(SALT);
        input_blobs.insert(new, SALT.to_vec());
        map.push((digest_hex(&old), digest_hex(&new)));
    }
    let (mut objects, mut blobs) = rewrite(&inputs, &input_blobs, &mut map);

    // The session's core evaluator closure, retained with its preimages.
    let evaluator = match evaluator {
        Some((id, descriptor, manifest, tree)) => {
            objects.insert(id.clone(), (D::Closure, descriptor));
            blobs.insert(raw_sha256(&manifest), manifest);
            for bytes in tree.into_values() {
                blobs.insert(raw_sha256(&bytes), bytes);
            }
            id
        }
        None => old_evaluator,
    };

    // The outputs, re-derived over the rewritten inputs.
    let plan_id = identity(D::Plan, &substitute(get(plan_id), &map));
    let execution_id = substitute_text(string(&object(seal)["executionPlanId"]), &map);
    let input_refs = substitute(&object(proof)["evaluationInputRefs"], &map);
    assert!(objects.contains_key(&plan_id) && objects.contains_key(&execution_id));
    let result = {
        let retained = inputs_of(&objects);
        let inputs = RetainedInputs::new(registry(), &retained, &blobs);
        derive_evaluation(
            &inputs,
            &plan_id,
            &execution_id,
            &evaluator,
            array(&input_refs),
            limits,
        )
        .expect("the rebound inputs derive")
    };
    for (key, pair) in result.objects() {
        let pair = array(pair);
        let domain = D::parse(string(&pair[0])).expect("domain");
        objects.insert(key.clone(), (domain, pair[1].clone()));
    }
    for (key, bytes) in result.blobs() {
        blobs.insert(digest(key), bytes.clone());
    }
    let proof = result.proof().clone();
    let proof_id = result.proof_bundle_id().to_owned();
    objects.insert(proof_id.clone(), (D::ProofBundle, proof.clone()));

    // The evidence, seal and Run, as `replay_run` checks them.
    let plan = objects[&plan_id].1.clone();
    let mut views = BTreeSet::new();
    let mut coverages = BTreeSet::new();
    for reference in array(&object(&proof)["evaluationInputRefs"]) {
        let r = object(reference);
        let digest = string(&r["digest"]);
        match string(&r["domain"]) {
            "view" => {
                views.insert(format!("view2:{digest}"));
            }
            "coverage" => {
                coverages.insert(format!("coverage2:{digest}"));
            }
            _ => {}
        }
    }
    for view in &views {
        for coverage in array(&object(&objects[view].1)["coverageIds"]) {
            coverages.insert(string(coverage).to_owned());
        }
    }
    let strings = |set: BTreeSet<String>| V::Array(set.into_iter().map(V::String).collect());
    let evidence = V::Object(BTreeMap::from([
        ("schemaVersion".into(), int(3)),
        ("planId".into(), V::String(plan_id.clone())),
        ("viewIds".into(), strings(views)),
        ("coverageIds".into(), strings(coverages)),
        ("importIds".into(), object(&plan)["importIds"].clone()),
        ("findingIds".into(), object(&proof)["findingIds"].clone()),
        ("proofBundleId".into(), V::String(proof_id.clone())),
    ]));
    let evidence_id = identity(D::SemanticEvidence, &evidence);
    let seal = V::Object(BTreeMap::from([
        ("schemaVersion".into(), int(3)),
        ("planId".into(), V::String(plan_id.clone())),
        ("executionPlanId".into(), V::String(execution_id)),
        ("evidenceId".into(), V::String(evidence_id.clone())),
        ("evaluatorClosure".into(), V::String(evaluator)),
        ("policyDigest".into(), object(&plan)["policyDigest"].clone()),
        ("proofBundleId".into(), V::String(proof_id)),
        ("verdict".into(), object(&proof)["verdict"].clone()),
    ]));
    let seal_id = identity(D::EvaluationSeal, &seal);
    let snapshot = &objects[string(&object(&plan)["snapshotId"])].1;
    assert_eq!(string(&object(snapshot)["projectId"]), project);
    let run = V::Object(BTreeMap::from([
        ("schemaVersion".into(), int(3)),
        ("projectId".into(), object(snapshot)["projectId"].clone()),
        ("snapshotId".into(), object(&plan)["snapshotId"].clone()),
        ("planId".into(), V::String(plan_id)),
        ("evidenceId".into(), V::String(evidence_id.clone())),
        ("evaluationSealId".into(), V::String(seal_id.clone())),
        (
            "capabilityManifestId".into(),
            object(&plan)["capabilityManifestId"].clone(),
        ),
    ]));
    let run_id = identity(D::Run, &run);
    objects.insert(evidence_id, (D::SemanticEvidence, evidence));
    objects.insert(seal_id, (D::EvaluationSeal, seal));
    objects.insert(run_id.clone(), (D::Run, run));
    SyntheticRunCandidate {
        run_id,
        objects: inputs_of(&objects),
        blobs,
    }
}

/// Unit X3d-3's mismatch test: the pinned corpus Run with only its
/// `projectId` rebound to `project` (its evaluator closure is the corpus's).
/// Storage's unit tests include this file; the feature's copy does not call it.
#[cfg(test)]
#[allow(dead_code)]
pub(crate) fn project_rebound_corpus(project: &str) -> SyntheticRunCandidate {
    bind(project, None, false)
}

/// Unit X3d-3's negative test: `candidate` with its evaluator closure
/// renamed to the closure `descriptor` names (for the session's core closure,
/// the same descriptor with `kind: "core"`), every dependent id and digest
/// recomputed, outputs included. Storage's unit tests include this file; the
/// feature's copy does not call it.
#[cfg(test)]
#[allow(dead_code)]
pub(crate) fn renaming_the_evaluator_closure(
    candidate: &SyntheticRunCandidate,
    descriptor: V,
) -> SyntheticRunCandidate {
    let seal = candidate
        .objects
        .values()
        .find(|o| o.domain == D::EvaluationSeal)
        .expect("a seal");
    let evaluator = string(&object(&seal.descriptor)["evaluatorClosure"]).to_owned();
    let renamed = identity(D::Closure, &descriptor);
    let objects: Objects = candidate
        .objects
        .iter()
        .filter(|(id, _)| **id != evaluator)
        .map(|(id, o)| (id.clone(), (o.domain, o.descriptor.clone())))
        .collect();
    let mut map = vec![(hex_of(&evaluator).to_owned(), hex_of(&renamed).to_owned())];
    let (mut objects, blobs) = rewrite(&objects, &candidate.blobs, &mut map);
    objects.insert(renamed, (D::Closure, descriptor));
    let run_id = substitute_text(&candidate.run_id, &map);
    assert!(objects.contains_key(&run_id));
    SyntheticRunCandidate {
        run_id,
        objects: inputs_of(&objects),
        blobs,
    }
}
