//! Pure portable glob predicate. Policy schema/domain admission and program
//! compilation are separate owners; a match supplies no evidence authority.
use alloc::{vec, vec::Vec};
#[derive(Debug, PartialEq, Eq)]
pub enum GlobMatchError {
    Limit,
}
fn charge(work: &mut usize, n: usize) -> Result<(), GlobMatchError> {
    *work = work.checked_sub(n).ok_or(GlobMatchError::Limit)?;
    Ok(())
}
fn segment(pattern: &[char], candidate: &[char], work: &mut usize) -> Result<bool, GlobMatchError> {
    let (mut i, mut j, mut star, mut mark) = (0, 0, None, 0);
    while j < candidate.len() {
        charge(work, 1)?;
        if i < pattern.len()
            && (pattern[i] == '?' || (pattern[i] != '*' && pattern[i] == candidate[j]))
        {
            i += 1;
            j += 1;
        } else if i < pattern.len() && pattern[i] == '*' {
            star = Some(i);
            i += 1;
            mark = j;
        } else if let Some(s) = star {
            i = s + 1;
            mark += 1;
            j = mark;
        } else {
            return Ok(false);
        }
    }
    while i < pattern.len() && pattern[i] == '*' {
        charge(work, 1)?;
        i += 1;
    }
    Ok(i == pattern.len())
}
/// Match whole strings using the portable glob-v1 law. Inputs remain subject to
/// their owning schema: this function neither admits LogicalPath/GlobPattern
/// nor normalizes them. Empty slash segments, literal brackets/braces and exact
/// Unicode scalars are preserved. `**` alone spans whole segments including the
/// final filename; ordinary `*`/`?` never cross `/`. No I/O or ambient locale.
///
/// Work is explicitly bounded; exhaustion is distinct from a negative match.
/// Dynamic programming avoids recursive/exponential `**` exploration.
pub fn portable_glob_match(
    pattern: &str,
    candidate: &str,
    mut work: usize,
) -> Result<bool, GlobMatchError> {
    charge(&mut work, 1)?;
    charge(&mut work, pattern.len())?;
    charge(&mut work, candidate.len())?;
    let patterns: Vec<Vec<char>> = pattern.split('/').map(|s| s.chars().collect()).collect();
    let candidates: Vec<Vec<char>> = candidate.split('/').map(|s| s.chars().collect()).collect();
    let mut next = vec![false; candidates.len() + 1];
    next[candidates.len()] = true;
    for p in patterns.iter().rev() {
        let mut current = vec![false; candidates.len() + 1];
        for j in (0..=candidates.len()).rev() {
            charge(&mut work, 1)?;
            current[j] = if p.as_slice() == ['*', '*'] {
                next[j] || (j < candidates.len() && current[j + 1])
            } else {
                j < candidates.len() && next[j + 1] && segment(p, &candidates[j], &mut work)?
            };
        }
        next = current;
    }
    Ok(next[0])
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn portable_glob_preserves_segments_scalars_and_literal_syntax() {
        for (pattern, candidate, expected) in [
            ("*a", "*ba", true),
            ("a*b", "a*xb", true),
            ("**a", "**ba", true),
            ("*?", "*ab", true),
            ("*?", "*", true),
            ("a*", "a*a", true),
            ("**/*.ts", "a.ts", true),
            ("**/*.ts", "src/nested/a.ts", true),
            ("*.ts", "src/a.ts", false),
            ("src/**", "src", true),
            ("src/**", "src/nested/legacy.js", true),
            ("src/**/*", "src", false),
            ("a/**/b", "a/b", true),
            ("a/**/b", "a/x/y/b", true),
            ("a/*/b", "a/b", false),
            ("a**b", "a/x/b", false),
            ("a**b", "axxb", true),
            ("*", ".hidden", true),
            ("a.ts", "A.ts", false),
            ("a.ts", "a.ts.extra", false),
            ("?.ts", "é.ts", true),
            ("?.ts", "e\u{301}.ts", false),
            ("?", "💠", true),
            ("[ab].ts", "a.ts", false),
            ("[ab].ts", "[ab].ts", true),
            ("{a,b}.ts", "a.ts", false),
            ("{a,b}.ts", "{a,b}.ts", true),
            ("src/", "src", false),
            ("a/*/b", "a//b", true),
            ("a/../b", "a/b", false),
        ] {
            assert_eq!(
                portable_glob_match(pattern, candidate, 10000),
                Ok(expected),
                "{pattern:?} {candidate:?}"
            );
            assert_eq!(
                portable_glob_match(pattern, candidate, 0),
                Err(GlobMatchError::Limit)
            );
        }
    }
}

// Retained policy/program admission is separate from matching and evaluation.
use crate::NativeUniverseError;
use crate::native_universe::{array, field, sha256_text, text};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::String,
};
use opensip_identity::{
    GraphError, IdentityDomain, JsonInteger, JsonValue as V, RetainedInputs, TraversalBudget,
    canonical_bytes, digest_hex, parse_json, raw_sha256,
};
const POLICY_DOCUMENT: &str = "workflows/schemas/policy-document.v2.schema.json";
#[derive(Debug, PartialEq, Eq)]
pub enum PolicyAdmissionError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Refused(String),
    RegistryLaw,
    Limit,
}
impl From<NativeUniverseError> for PolicyAdmissionError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
pub struct PolicyProgramChecks {
    rules: usize,
}
impl PolicyProgramChecks {
    pub fn rule_count(&self) -> usize {
        self.rules
    }
}
struct PolicyReader<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    budget: TraversalBudget,
}
impl PolicyReader<'_, '_> {
    fn step(&mut self) -> Result<(), PolicyAdmissionError> {
        if self.budget.depth == 0 {
            return Err(PolicyAdmissionError::Limit);
        }
        self.budget.steps = self
            .budget
            .steps
            .checked_sub(1)
            .ok_or(PolicyAdmissionError::Limit)?;
        Ok(())
    }
    fn object(&mut self, id: &str, domain: IdentityDomain) -> Result<V, PolicyAdmissionError> {
        self.step()?;
        Ok(self
            .inputs
            .object(id, domain, self.budget.descriptor_work)
            .map_err(|e| PolicyAdmissionError::Record(GraphError::Input(e)))?
            .descriptor()
            .clone())
    }
    fn record(&mut self, sha: &V, document: &str, kind: &str) -> Result<V, PolicyAdmissionError> {
        self.step()?;
        let sha = sha256_text(&format!("sha256:{}", text(sha)?))?;
        self.inputs
            .current_record_shape(
                sha,
                document,
                &format!("#/$defs/{kind}"),
                self.budget.descriptor_work,
            )
            .map_err(PolicyAdmissionError::Record)
    }
}
fn optional<'a>(v: &'a V, k: &str) -> Option<&'a V> {
    if let V::Object(o) = v { o.get(k) } else { None }
}
fn member_is(v: &V, k: &str, s: &str) -> bool {
    optional(v, k) == Some(&V::String(s.into()))
}
fn policy_require(yes: bool, cause: &str) -> Result<(), PolicyAdmissionError> {
    if yes {
        Ok(())
    } else {
        Err(PolicyAdmissionError::Refused(cause.into()))
    }
}
fn has_string(v: &V, s: &str) -> bool {
    if let V::Array(a) = v {
        a.iter().any(|x| x == &V::String(s.into()))
    } else {
        false
    }
}
// Inputs below are internal: both complete documents have passed the registered
// schema before these checks. In particular no caller can bypass FieldFilter
// shape admission or add an atom.subjectKind field forbidden by that schema.
fn atom_law(
    atom: &V,
    subject_kind: Option<&str>,
    registry: &V,
    reader: &mut PolicyReader<'_, '_>,
) -> Result<bool, PolicyAdmissionError> {
    reader.step()?;
    let rel = text(field(atom, "relation")?)?;
    let Some(spec) = optional(field(registry, "relations")?, rel) else {
        return Ok(false);
    };
    let rung = text(field(atom, "minResolution")?)?;
    if !has_string(field(spec, "ladder")?, rung) {
        return Ok(false);
    }
    let target = member_is(atom, "endpoint", "target");
    if target
        && (member_is(spec, "endpointTarget", "forbidden")
            || optional(spec, "endpointTargetRungs")
                .is_some_and(|r| matches!(r,V::Array(a)if !a.is_empty()) && !has_string(r, rung)))
    {
        return Ok(false);
    }
    let evidence = optional(atom, "evidence");
    if member_is(spec, "plane", "native") {
        if evidence.is_some_and(|v| v != &V::Null) {
            return Ok(false);
        }
    } else if evidence != optional(spec, "evidenceKind") {
        return Ok(false);
    }
    let kinds: Vec<&V> = if target {
        array(field(spec, "targetKinds")?)?.iter().collect()
    } else if let Some(kinds) = optional(spec, "sourceSubjectKinds") {
        array(kinds)?.iter().collect()
    } else {
        optional(spec, "sourceSubjectKind").into_iter().collect()
    };
    // The program path's first registry kind is deterministic selected behavior.
    // It must not be replaced with a different policy-enumeration requirement.
    let kind = match subject_kind {
        Some("export") => Some("symbol"),
        Some(k) => Some(k),
        None => kinds.iter().find_map(|v| {
            if let V::String(s) = v {
                if !s.is_empty() {
                    Some(s.as_str())
                } else {
                    None
                }
            } else {
                None
            }
        }),
    };
    if !kinds
        .iter()
        .any(|v| matches!(v,V::String(s)if Some(s.as_str())==kind))
    {
        return Ok(false);
    }
    for filter in array(field(atom, "filters")?)? {
        reader.step()?;
        let name = text(field(filter, "field")?)?;
        let cmp = text(field(filter, "cmp")?)?;
        let value = field(filter, "value")?;
        let projection = field(field(spec, "filters")?, name)?;
        let selected_projection = optional(projection, rung).unwrap_or(projection);
        if selected_projection == &V::String("forbidden".into()) {
            return Ok(false);
        }
        let table = field(field(registry, "comparatorTable")?, name)?;
        if !optional(table, cmp).is_some_and(|v| v != &V::Bool(false) && v != &V::Null) {
            return Ok(false);
        }
        let enumeration = match name {
            "resolution" => Some(field(spec, "ladder")?),
            "universe" => Some(field(registry, "portableUniverseDomains")?),
            "testResult" => optional(table, "enumByRelation").and_then(|v| optional(v, rel)),
            _ => optional(table, "enum"),
        };
        if let Some(values) = enumeration {
            let allowed = array(values)?;
            if (cmp == "eq" || cmp == "neq") && !allowed.contains(value) {
                return Ok(false);
            }
            if cmp == "in" {
                for item in array(value)? {
                    reader.step()?;
                    if !allowed.contains(item) {
                        return Ok(false);
                    }
                }
            }
        }
        if (cmp == "prefix" || cmp == "glob")
            && text(value)?.chars().any(|c| c == '\\' || c == '\0')
        {
            return Ok(false);
        }
    }
    Ok(true)
}
fn rule_law(
    rule: &V,
    registry: &V,
    reader: &mut PolicyReader<'_, '_>,
) -> Result<Option<&'static str>, PolicyAdmissionError> {
    let mut declared = BTreeSet::new();
    for row in array(field(rule, "evidenceUse")?)? {
        reader.step()?;
        if !declared.insert(text(field(row, "kind")?)?) {
            return Ok(Some("POLICY.UNKNOWN_RULE"));
        }
    }
    let kind = text(field(field(rule, "subjectEnumeration")?, "subjectKind")?)?;
    let mut stack = vec![(field(rule, "emitWhen")?, 1usize)];
    let mut count = 0;
    while let Some((node, depth)) = stack.pop() {
        reader.step()?;
        count += 1;
        if count > 64 || depth > 8 {
            return Ok(Some("POLICY.UNKNOWN_RULE"));
        }
        match text(field(node, "op")?)? {
            "and" | "or" => {
                for child in array(field(node, "operands")?)?.iter().rev() {
                    stack.push((child, depth + 1))
                }
            }
            "not" => stack.push((field(node, "operand")?, depth + 1)),
            _ => {
                if !atom_law(node, Some(kind), registry, reader)? {
                    return Ok(Some("POLICY.UNKNOWN_RULE"));
                }
                if let Some(evidence) = optional(node, "evidence")
                    && !declared.contains(text(evidence)?)
                {
                    return Ok(Some("IMPORT.ABSENT_FOR_PREDICATE"));
                }
            }
        }
    }
    Ok(None)
}
/// Rehash the Run-selected policy, waiver and compiled program; validate full
/// record shapes, exact compilation and bounded rule/atom admission. Private
/// counts are diagnostics, not a closed Run or evaluator proof. Earlier Run
/// links/native census and later stages/predicates/imports/replay remain owed.
pub fn inspect_policy_program(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    budget: TraversalBudget,
) -> Result<PolicyProgramChecks, PolicyAdmissionError> {
    let mut reader = PolicyReader { inputs, budget };
    let run = reader.object(run_id, IdentityDomain::Run)?;
    let plan = reader.object(text(field(&run, "planId")?)?, IdentityDomain::Plan)?;
    let seal = reader.object(
        text(field(&run, "evaluationSealId")?)?,
        IdentityDomain::EvaluationSeal,
    )?;
    let proof = reader.object(
        text(field(&seal, "proofBundleId")?)?,
        IdentityDomain::ProofBundle,
    )?;
    let policy = reader.record(
        field(&plan, "policyDigest")?,
        POLICY_DOCUMENT,
        "PolicyDocumentV2",
    )?;
    reader.record(
        field(&plan, "waiverDigest")?,
        "workflows/schemas/policy-document.schema.json",
        "WaiverSetV1",
    )?;
    let program = reader.record(
        field(&proof, "ruleProgramDigest")?,
        POLICY_DOCUMENT,
        "RuleProgramV2",
    )?;
    policy_require(
        field(&program, "policyDigest")? == field(&plan, "policyDigest")?,
        "RULE_PROGRAM_POLICY_JOIN",
    )?;
    let mut rules = Vec::new();
    for rule in array(field(&policy, "rules")?)? {
        reader.step()?;
        let mut row = BTreeMap::new();
        for k in ["ruleId", "ruleProgramRef", "emitWhen"] {
            row.insert(k.into(), field(rule, k)?.clone());
        }
        rules.push(V::Object(row));
    }
    let compiled = V::Object(BTreeMap::from([
        (
            "schemaVersion".into(),
            V::Integer(JsonInteger::new(2).map_err(|_| PolicyAdmissionError::RegistryLaw)?),
        ),
        ("policyDigest".into(), field(&plan, "policyDigest")?.clone()),
        ("rules".into(), V::Array(rules)),
    ]));
    let bytes = canonical_bytes(&compiled).map_err(|_| PolicyAdmissionError::RegistryLaw)?;
    policy_require(
        digest_hex(&raw_sha256(&bytes)) == text(field(&proof, "ruleProgramDigest")?)?,
        "RULE_PROGRAM_COMPILATION_JOIN",
    )?;
    let registry = parse_json(include_bytes!("atom-registry.json"))
        .map_err(|_| PolicyAdmissionError::RegistryLaw)?;
    for rule in array(field(&policy, "rules")?)? {
        if let Some(detail) = rule_law(rule, &registry, &mut reader)? {
            return Err(PolicyAdmissionError::Refused(format!(
                "POLICY_RULE_NOT_ADMISSIBLE:policy:{}:{detail}",
                text(field(rule, "ruleId")?)?
            )));
        }
    }
    for rule in array(field(&program, "rules")?)? {
        let mut stack = vec![field(rule, "emitWhen")?];
        while let Some(node) = stack.pop() {
            reader.step()?;
            match text(field(node, "op")?)? {
                "and" | "or" => stack.extend(array(field(node, "operands")?)?.iter().rev()),
                "not" => stack.push(field(node, "operand")?),
                _ => {
                    if !atom_law(node, None, &registry, &mut reader)? {
                        return Err(PolicyAdmissionError::Refused(format!(
                            "POLICY_ATOM_NOT_ADMISSIBLE:program:{}:POLICY.UNKNOWN_RULE",
                            text(field(rule, "ruleId")?)?
                        )));
                    }
                }
            }
        }
    }
    Ok(PolicyProgramChecks {
        rules: array(field(&policy, "rules")?)?.len(),
    })
}
