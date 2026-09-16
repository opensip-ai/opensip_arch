//! Retained predicate witness/address diagnostics. Evaluation and independent
//! reconstruction are separate; checked references do not establish truth.
use crate::NativeUniverseError;
use crate::native_universe::{array, field, sha256_text, text};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::String,
    vec::Vec,
};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, RetainedInputs, TraversalBudget, canonical_bytes,
    digest_hex, raw_sha256,
};
#[derive(Debug, PartialEq, Eq)]
pub enum PredicateError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Refused(&'static str),
    Limit,
}
impl From<NativeUniverseError> for PredicateError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
pub struct PredicateChecks {
    predicates: usize,
}
impl PredicateChecks {
    pub fn predicate_count(&self) -> usize {
        self.predicates
    }
}
struct Reader<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    budget: TraversalBudget,
}
impl Reader<'_, '_> {
    fn step(&mut self) -> Result<(), PredicateError> {
        if self.budget.depth == 0 {
            return Err(PredicateError::Limit);
        }
        self.budget.steps = self
            .budget
            .steps
            .checked_sub(1)
            .ok_or(PredicateError::Limit)?;
        Ok(())
    }
    fn object(&mut self, id: &str, domain: IdentityDomain) -> Result<V, PredicateError> {
        self.step()?;
        Ok(self
            .inputs
            .object(id, domain, self.budget.descriptor_work)
            .map_err(|e| PredicateError::Record(GraphError::Input(e)))?
            .descriptor()
            .clone())
    }
    fn record(&mut self, sha: &V, kind: &str) -> Result<V, PredicateError> {
        self.step()?;
        self.inputs
            .identity_record_shape(
                sha256_text(&format!("sha256:{}", text(sha)?))?,
                kind,
                self.budget.descriptor_work,
            )
            .map_err(PredicateError::Record)
    }
    fn strings(&mut self, value: &V) -> Result<BTreeSet<String>, PredicateError> {
        let mut set = BTreeSet::new();
        for v in array(value)? {
            self.step()?;
            set.insert(text(v)?.into());
        }
        Ok(set)
    }
    fn refs(&mut self, value: &V) -> Result<BTreeSet<Vec<u8>>, PredicateError> {
        let mut set = BTreeSet::new();
        for v in array(value)? {
            self.step()?;
            set.insert(canon(v)?);
        }
        Ok(set)
    }
}
fn canon(v: &V) -> Result<Vec<u8>, PredicateError> {
    canonical_bytes(v).map_err(|e| {
        PredicateError::Record(GraphError::Input(
            opensip_identity::RetainedInputError::Canonical(e),
        ))
    })
}
fn require(yes: bool, cause: &'static str) -> Result<(), PredicateError> {
    if yes {
        Ok(())
    } else {
        Err(PredicateError::Refused(cause))
    }
}
// Internal-only: the public entry derives root from a hash/schema-checked
// retained program. Canonical ASCII addresses are never normalized aliases.
fn node_at<'a>(
    mut node: &'a V,
    address: &str,
    reader: &mut Reader<'_, '_>,
) -> Result<&'a V, PredicateError> {
    let mut parts = address.split('.');
    require(parts.next() == Some("p"), "PREDICATE_ADDRESS")?;
    for part in parts {
        reader.step()?;
        require(
            !part.is_empty()
                && part.bytes().all(|c| c.is_ascii_digit())
                && !(part.len() > 1 && part.starts_with('0')),
            "PREDICATE_ADDRESS",
        )?;
        let children: Vec<&V> = match text(field(node, "op")?)? {
            "and" | "or" => array(field(node, "operands")?)?.iter().collect(),
            "not" => alloc::vec![field(node, "operand")?],
            _ => Vec::new(),
        };
        require(!children.is_empty(), "PREDICATE_ADDRESS_LEAF")?;
        // Registered operands have a tiny closed bound. Any otherwise valid
        // decimal too large for usize necessarily exceeds that bound, on every
        // supported target. Preserve the reference's LEAF-before-RANGE order.
        let index = part
            .parse::<usize>()
            .map_err(|_| PredicateError::Refused("PREDICATE_ADDRESS_RANGE"))?;
        node = children
            .get(index)
            .copied()
            .ok_or(PredicateError::Refused("PREDICATE_ADDRESS_RANGE"))?;
    }
    Ok(node)
}
fn child_addresses(node: &V, address: &str) -> Result<BTreeSet<String>, PredicateError> {
    Ok(match text(field(node, "op")?)? {
        "and" | "or" => (0..array(field(node, "operands")?)?.len())
            .map(|i| format!("{address}.{i}"))
            .collect(),
        "not" => BTreeSet::from([format!("{address}.0")]),
        _ => BTreeSet::new(),
    })
}
/// Check retained predicate inputs and exact program-node/witness joins from a
/// retained Run id. This does not run policy compilation, full graph admission,
/// atom evaluation or replay, and its private count is not proof authority.
pub fn inspect_predicate_witnesses(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    budget: TraversalBudget,
) -> Result<PredicateChecks, PredicateError> {
    let mut reader = Reader { inputs, budget };
    let run = reader.object(run_id, IdentityDomain::Run)?;
    let seal = reader.object(
        text(field(&run, "evaluationSealId")?)?,
        IdentityDomain::EvaluationSeal,
    )?;
    let proof = reader.object(
        text(field(&seal, "proofBundleId")?)?,
        IdentityDomain::ProofBundle,
    )?;
    reader.step()?;
    let program = inputs
        .current_record_shape(
            sha256_text(&format!(
                "sha256:{}",
                text(field(&proof, "ruleProgramDigest")?)?
            ))?,
            "workflows/schemas/policy-document.v2.schema.json",
            "#/$defs/RuleProgramV2",
            reader.budget.descriptor_work,
        )
        .map_err(PredicateError::Record)?;
    let rules: BTreeMap<&str, &V> = array(field(&program, "rules")?)?
        .iter()
        .map(|r| Ok((text(field(r, "ruleId")?)?, r)))
        .collect::<Result<_, NativeUniverseError>>()?;
    let evaluation_refs = reader.refs(field(&proof, "evaluationInputRefs")?)?;
    let predicates = array(field(&proof, "predicateProofs")?)?;
    let mut proven: BTreeMap<(String, String), BTreeSet<String>> = BTreeMap::new();
    for pred in predicates {
        reader.step()?;
        proven
            .entry((
                text(field(pred, "ruleId")?)?.into(),
                text(field(pred, "subjectId")?)?.into(),
            ))
            .or_default()
            .insert(text(field(pred, "predicateId")?)?.into());
    }
    for pred in predicates {
        reader.step()?;
        require(
            reader
                .refs(field(pred, "inputRefs")?)?
                .is_subset(&evaluation_refs),
            "HIDDEN_PREDICATE_INPUT",
        )?;
        let (mut scopes, mut facts, mut coverages) =
            (BTreeSet::new(), BTreeSet::new(), BTreeSet::new());
        for reference in array(field(pred, "inputRefs")?)? {
            reader.step()?;
            if text(field(reference, "domain")?)? == "view" {
                let view = reader.object(
                    &format!("view2:{}", text(field(reference, "digest")?)?),
                    IdentityDomain::View,
                )?;
                scopes.extend(reader.strings(field(&view, "scopeIds")?)?);
                facts.extend(reader.strings(field(&view, "facts")?)?);
                coverages.extend(reader.strings(field(&view, "coverageIds")?)?);
            }
        }
        require(
            reader.strings(field(pred, "scopeIds")?)?.is_subset(&scopes),
            "PREDICATE_SCOPE_ROOTS",
        )?;
        let witness = reader.record(field(pred, "witnessDigest")?, "predicate-witness")?;
        let mut cited_facts = reader.strings(field(&witness, "matchingFactIds")?)?;
        cited_facts.extend(reader.strings(field(&witness, "uncertainFactIds")?)?);
        require(cited_facts.is_subset(&facts), "WITNESS_FACT_ROOTS")?;
        require(
            reader
                .strings(field(&witness, "coverageIds")?)?
                .is_subset(&coverages),
            "WITNESS_COVERAGE_ROOTS",
        )?;
        let addressed = reader.record(
            field(&witness, "programPredicateDigest")?,
            "program-predicate",
        )?;
        require(
            field(&addressed, "ruleProgramDigest")? == field(&proof, "ruleProgramDigest")?,
            "PROGRAM_PREDICATE_PROGRAM_JOIN",
        )?;
        require(
            field(&addressed, "ruleId")? == field(pred, "ruleId")?
                && field(&addressed, "predicateId")? == field(pred, "predicateId")?,
            "PROGRAM_PREDICATE_ADDRESS_JOIN",
        )?;
        require(
            field(&addressed, "operation")? == field(pred, "operation")?,
            "PROGRAM_PREDICATE_OPERATION_JOIN",
        )?;
        let rule = rules
            .get(text(field(pred, "ruleId")?)?)
            .ok_or(PredicateError::Refused("PROGRAM_PREDICATE_RULE_UNKNOWN"))?;
        let address = text(field(&addressed, "predicateId")?)?;
        let node = node_at(field(rule, "emitWhen")?, address, &mut reader)?;
        require(
            field(node, "op")? == field(&addressed, "operation")?,
            "PROGRAM_PREDICATE_NODE_OPERATION",
        )?;
        // Full registered RuleProgramV2 admission already checks each exact
        // Predicate node with the same policy-v2 selector used by the reference.
        require(
            digest_hex(&raw_sha256(&canon(node)?)) == text(field(&addressed, "nodeDigest")?)?,
            "PROGRAM_PREDICATE_NODE_DIGEST",
        )?;
        let children = child_addresses(node, address)?;
        require(
            reader.strings(field(&witness, "childPredicateIds")?)? == children,
            "WITNESS_CHILD_ADDRESS_JOIN",
        )?;
        let key = (
            text(field(pred, "ruleId")?)?.into(),
            text(field(pred, "subjectId")?)?.into(),
        );
        require(
            proven.get(&key).is_some_and(|ids| children.is_subset(ids)),
            "WITNESS_CHILD_NOT_PROVEN",
        )?;
        let limit = if text(field(node, "op")?)? == "count-at-most" {
            field(node, "n")?
        } else {
            &V::Null
        };
        require(
            field(&witness, "countLimit")? == limit,
            "WITNESS_COUNT_LIMIT_JOIN",
        )?;
    }
    Ok(PredicateChecks {
        predicates: predicates.len(),
    })
}
