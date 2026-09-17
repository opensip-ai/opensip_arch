//! Producer stage output registration and structural schema checks. The selected
//! portable profile is not an executable schema compiler or instance validator.
use crate::NativeUniverseError;
use crate::native_universe::{array, field, sha256_text, text};
use alloc::{collections::BTreeSet, format, string::String};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, RetainedInputs, TraversalBudget, parse_json,
};
#[derive(Debug, PartialEq, Eq)]
pub enum StageOutputError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Refused(String),
    InvalidDocument,
    Limit,
}
impl From<NativeUniverseError> for StageOutputError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
fn require(ok: bool, cause: &str) -> Result<(), StageOutputError> {
    if ok {
        Ok(())
    } else {
        Err(StageOutputError::Refused(cause.into()))
    }
}
struct Work {
    remaining: usize,
    depth: usize,
}
impl Work {
    fn spend(&mut self, n: usize) -> Result<(), StageOutputError> {
        self.remaining = self
            .remaining
            .checked_sub(n)
            .ok_or(StageOutputError::Limit)?;
        Ok(())
    }
}
fn strings(v: &V, work: &mut Work) -> Result<bool, StageOutputError> {
    let V::Array(values) = v else {
        return Ok(false);
    };
    let mut seen = BTreeSet::new();
    for value in values {
        work.spend(1)?;
        let V::String(s) = value else {
            return Ok(false);
        };
        if !seen.insert(s) {
            return Ok(false);
        }
    }
    Ok(true)
}
fn anchor(s: &str) -> bool {
    let s = s.strip_suffix('\n').unwrap_or(s);
    let mut chars = s.bytes();
    chars
        .next()
        .is_some_and(|c| c.is_ascii_alphabetic() || c == b'_')
        && chars.all(|c| c.is_ascii_alphanumeric() || matches!(c, b'_' | b'-' | b'.'))
}
fn identifier(s: &str) -> bool {
    match s.find('#') {
        None => true,
        Some(i) => matches!(&s[i..], "#" | "#\n"),
    }
}
// Finite projection of the eight frozen default meta-schema resources. These
// are the meta-schema's own fixed keyword/type checks, not producer evaluation.
fn meta(v: &V, work: &mut Work, depth: usize) -> Result<bool, StageOutputError> {
    work.spend(1)?;
    if depth > work.depth {
        return Err(StageOutputError::Limit);
    }
    let V::Object(values) = v else {
        return Ok(matches!(v, V::Bool(_)));
    };
    for (key, value) in values {
        work.spend(1)?;
        let valid = match key.as_str() {
            "$id" => matches!(value, V::String(s) if identifier(s)),
            "$anchor" | "$dynamicAnchor" | "$recursiveAnchor" => {
                matches!(value, V::String(s) if anchor(s))
            }
            "$schema" | "$ref" | "$dynamicRef" | "$recursiveRef" | "$comment" | "title"
            | "description" | "format" | "contentEncoding" | "contentMediaType" | "pattern" => {
                matches!(value, V::String(_))
            }
            "$vocabulary" => {
                if let V::Object(o) = value {
                    work.spend(o.len())?;
                    o.values().all(|v| matches!(v, V::Bool(_)))
                } else {
                    false
                }
            }
            "$defs" | "definitions" | "properties" | "patternProperties" | "dependentSchemas" => {
                if let V::Object(o) = value {
                    let mut valid = true;
                    for v in o.values() {
                        if !meta(v, work, depth + 1)? {
                            valid = false;
                            break;
                        }
                    }
                    valid
                } else {
                    false
                }
            }
            "items"
            | "contains"
            | "additionalProperties"
            | "propertyNames"
            | "if"
            | "then"
            | "else"
            | "not"
            | "unevaluatedItems"
            | "unevaluatedProperties"
            | "contentSchema" => meta(value, work, depth + 1)?,
            "prefixItems" | "allOf" | "anyOf" | "oneOf" => {
                if let V::Array(a) = value {
                    let mut valid = !a.is_empty();
                    for v in a {
                        if !meta(v, work, depth + 1)? {
                            valid = false;
                            break;
                        }
                    }
                    valid
                } else {
                    false
                }
            }
            "dependencies" | "dependentRequired" => {
                if let V::Object(o) = value {
                    let mut valid = true;
                    for v in o.values() {
                        if !(key == "dependencies" && meta(v, work, depth + 1)?
                            || strings(v, work)?)
                        {
                            valid = false;
                            break;
                        }
                    }
                    valid
                } else {
                    false
                }
            }
            "type" => {
                let kind = |v: &V| matches!(v, V::String(s) if matches!(s.as_str(), "array" | "boolean" | "integer" | "null" | "number" | "object" | "string"));
                if let V::Array(a) = value {
                    !a.is_empty() && strings(value, work)? && a.iter().all(kind)
                } else {
                    kind(value)
                }
            }
            "enum" | "examples" => matches!(value, V::Array(_)),
            "maximum" | "exclusiveMaximum" | "minimum" | "exclusiveMinimum" => {
                matches!(value, V::Integer(_))
            }
            "multipleOf" => matches!(value, V::Integer(n) if n.get() > 0),
            "maxLength" | "minLength" | "maxItems" | "minItems" | "maxContains" | "minContains"
            | "maxProperties" | "minProperties" => matches!(value, V::Integer(n) if n.get() >= 0),
            "uniqueItems" | "deprecated" | "readOnly" | "writeOnly" => matches!(value, V::Bool(_)),
            "required" => strings(value, work)?,
            _ => true,
        };
        if !valid {
            return Ok(false);
        }
    }
    Ok(true)
}
fn parse_document(raw: &[u8], work: &mut Work) -> Result<V, StageOutputError> {
    work.spend(1)?;
    work.spend(raw.len())?;
    parse_json(raw).map_err(|e| match e {
        opensip_identity::CanonicalError::ByteLimit
        | opensip_identity::CanonicalError::DepthLimit => StageOutputError::Limit,
        _ => StageOutputError::InvalidDocument,
    })
}
fn parse_shape(raw: &[u8], work: &mut Work) -> Result<V, StageOutputError> {
    let v = parse_document(raw, work)?;
    if !meta(&v, work, 0)? {
        return Err(StageOutputError::InvalidDocument);
    }
    Ok(v)
}
/// Inspect only the structural producer-schema profile over supplied JSON bytes.
/// This returns inert data; it does not prove registration, compile regexes,
/// resolve producer references, validate instances, or establish Run authority.
pub fn inspect_stage_schema_shape(raw: &[u8], steps: usize) -> Result<V, StageOutputError> {
    parse_shape(
        raw,
        &mut Work {
            remaining: steps,
            depth: 96,
        },
    )
}
struct Reader<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    descriptor_work: usize,
    work: Work,
}
impl Reader<'_, '_> {
    fn object(&mut self, id: &str, domain: IdentityDomain) -> Result<V, StageOutputError> {
        self.work.spend(1)?;
        Ok(self
            .inputs
            .object(id, domain, self.descriptor_work)
            .map_err(|e| StageOutputError::Record(GraphError::Input(e)))?
            .descriptor()
            .clone())
    }
    fn record(&mut self, digest: [u8; 32], kind: &str) -> Result<V, StageOutputError> {
        self.work.spend(1)?;
        self.inputs
            .identity_record_shape(digest, kind, self.descriptor_work)
            .map_err(StageOutputError::Record)
    }
    fn spec(&mut self, digest: [u8; 32]) -> Result<(V, V), StageOutputError> {
        let spec = self.record(digest, "stage-spec")?;
        let producer = self.object(
            text(field(&spec, "producerClosure")?)?,
            IdentityDomain::Closure,
        )?;
        require(
            text(field(&producer, "kind")?)? == "provider",
            "CLOSURE_FIELD_KIND:stage-spec.producerClosure:provider",
        )?;
        Ok((spec, producer))
    }
}
fn sha(v: &V) -> Result<[u8; 32], StageOutputError> {
    Ok(sha256_text(&format!("sha256:{}", text(v)?))?)
}
fn output_schema(
    reader: &mut Reader<'_, '_>,
    spec: &V,
    producer: &V,
) -> Result<V, StageOutputError> {
    reader.work.spend(1)?;
    // The selected retained caller evaluates blob(outputSchemaDigest) before
    // entering the registration helper; retention faults precede its guards.
    let blob = reader
        .inputs
        .blob(sha(field(spec, "outputSchemaDigest")?)?)
        .map_err(|e| StageOutputError::Record(GraphError::Input(e)))?;
    let operation = text(field(spec, "operation")?)?;
    require(
        !operation.is_empty()
            && operation.len() <= 128
            && operation
                .bytes()
                .next()
                .is_some_and(|c| c.is_ascii_lowercase() || c.is_ascii_digit())
            && operation.bytes().all(|c| {
                c.is_ascii_lowercase() || c.is_ascii_digit() || matches!(c, b'.' | b'_' | b'-')
            }),
        "STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT",
    )?;
    let path = format!("opensip-interface/stage-output/{operation}.schema.json");
    let mut member = None;
    for row in array(field(producer, "tree")?)? {
        reader.work.spend(1)?;
        if text(field(row, "path")?)? == path {
            member = Some(row);
            break;
        }
    }
    let row = member.ok_or_else(|| {
        StageOutputError::Refused(format!("STAGE_OUTPUT_SCHEMA_UNREGISTERED:{path}"))
    })?;
    require(
        field(row, "sha256")? == field(spec, "outputSchemaDigest")?,
        &format!("STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH:{path}"),
    )?;
    reader.work.spend(1)?;
    let document = parse_document(blob.bytes(), &mut reader.work).map_err(|e| match e {
        StageOutputError::InvalidDocument => {
            StageOutputError::Refused(format!("STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:{path}"))
        }
        e => e,
    })?;
    let V::Object(fields) = &document else {
        return Err(StageOutputError::Refused(format!(
            "STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:{path}"
        )));
    };
    require(
        matches!(fields.get("$schema"),Some(V::String(s))if s=="https://json-schema.org/draft/2020-12/schema"),
        &format!("STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:{path}"),
    )?;
    require(
        meta(&document, &mut reader.work, 0)?,
        &format!("STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:{path}"),
    )?;
    let declaration = fields.get("x-opensip-stage-output");
    require(
        matches!(declaration,Some(V::Object(o))if o.len()==3
        && matches!(o.get("schemaVersion"),Some(V::Integer(n))if n.get()==1)
        && o.get("operation")==Some(field(spec,"operation")?)
        && o.get("outputDomains")==Some(field(spec,"outputDomains")?)),
        &format!("STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH:{path}"),
    )?;
    Ok(document)
}
/// Rehash a retained stage-spec, provider closure and exact registered raw schema
/// bytes. The returned document is inert structural metadata, not executable
/// schema authority or proof of Plan selection. It may contain invalid regexes.
pub fn inspect_stage_output_schema(
    inputs: &RetainedInputs<'_>,
    spec_digest: [u8; 32],
    budget: TraversalBudget,
) -> Result<V, StageOutputError> {
    if budget.depth == 0 {
        return Err(StageOutputError::Limit);
    }
    let mut reader = Reader {
        inputs,
        descriptor_work: budget.descriptor_work,
        work: Work {
            remaining: budget.steps,
            depth: budget.depth,
        },
    };
    let (spec, producer) = reader.spec(spec_digest)?;
    output_schema(&mut reader, &spec, &producer)
}
pub struct StageSpecChecks {
    stages: usize,
}
impl StageSpecChecks {
    pub fn stage_count(&self) -> usize {
        self.stages
    }
}
/// Check the post-policy derivation-stage joins in their retained Run context.
/// This does not walk the full graph, execute producers or replay the Run.
pub fn inspect_stage_specs(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    budget: TraversalBudget,
) -> Result<StageSpecChecks, StageOutputError> {
    if budget.depth == 0 {
        return Err(StageOutputError::Limit);
    }
    let mut reader = Reader {
        inputs,
        descriptor_work: budget.descriptor_work,
        work: Work {
            remaining: budget.steps,
            depth: budget.depth,
        },
    };
    let run = reader.object(run_id, IdentityDomain::Run)?;
    let plan = reader.object(text(field(&run, "planId")?)?, IdentityDomain::Plan)?;
    let seal = reader.object(
        text(field(&run, "evaluationSealId")?)?,
        IdentityDomain::EvaluationSeal,
    )?;
    let execution = reader.object(
        text(field(&seal, "executionPlanId")?)?,
        IdentityDomain::ExecutionPlan,
    )?;
    inspect_stage_context(reader, plan, execution, field(&run, "planId")?)
}

/// Recheck a retained execution Plan's derivation stages before any Run, seal
/// or proof exists. Producer execution and full capture admission are separate.
pub fn inspect_plan_stage_specs(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    execution_plan_id: &str,
    budget: TraversalBudget,
) -> Result<StageSpecChecks, StageOutputError> {
    if budget.depth == 0 {
        return Err(StageOutputError::Limit);
    }
    let mut reader = Reader {
        inputs,
        descriptor_work: budget.descriptor_work,
        work: Work {
            remaining: budget.steps,
            depth: budget.depth,
        },
    };
    let plan = reader.object(plan_id, IdentityDomain::Plan)?;
    let execution = reader.object(execution_plan_id, IdentityDomain::ExecutionPlan)?;
    let plan_value = V::String(plan_id.into());
    require(
        field(&execution, "planId")? == &plan_value,
        "EXECUTION_PLAN_JOIN",
    )?;
    inspect_stage_context(reader, plan, execution, &plan_value)
}

fn inspect_stage_context(
    mut reader: Reader<'_, '_>,
    plan: V,
    execution: V,
    plan_id: &V,
) -> Result<StageSpecChecks, StageOutputError> {
    let analysis = reader.record(sha(field(&plan, "analysisSpecDigest")?)?, "analysis-spec")?;
    let stages = array(field(&execution, "stages")?)?;
    for stage in stages {
        reader.work.spend(1)?;
        let (spec, producer) = reader.spec(sha(field(stage, "stageSpecDigest")?)?)?;
        require(field(&spec, "planId")? == plan_id, "STAGE_SPEC_PLAN_JOIN")?;
        require(
            array(field(&plan, "semanticClosures")?)?.contains(field(&spec, "producerClosure")?),
            "STAGE_SPEC_UNSELECTED_PRODUCER",
        )?;
        require(
            field(&spec, "outputDomains")? == field(stage, "outputDomains")?,
            "STAGE_SPEC_OUTPUT_DOMAIN_JOIN",
        )?;
        for parameter in array(field(&spec, "parameters")?)? {
            reader.work.spend(1)?;
            require(
                array(field(&analysis, "parameters")?)?.contains(parameter),
                "STAGE_SPEC_HIDDEN_PARAMETER",
            )?;
        }
        output_schema(&mut reader, &spec, &producer)?;
    }
    Ok(StageSpecChecks {
        stages: stages.len(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn structural_registration_does_not_execute_regexes_or_remote_refs() {
        for raw in [
            br#"{"pattern":"(","patternProperties":{"(":true}}"#.as_slice(),
            br#"{"$ref":"https://unreachable.invalid/schema","format":"custom"}"#,
        ] {
            assert!(inspect_stage_schema_shape(raw, 10000).is_ok());
        }
        assert!(matches!(
            inspect_stage_schema_shape(br#"{"pattern":false}"#, 10000),
            Err(StageOutputError::InvalidDocument)
        ));
    }
    #[test]
    fn fixed_meta_patterns_preserve_selected_trailing_lf_behavior() {
        for raw in [br#"{"$anchor":"a\n"}"#.as_slice(), br#"{"$id":"a#\n"}"#] {
            assert!(inspect_stage_schema_shape(raw, 10000).is_ok());
        }
        for raw in [
            br#"{"$anchor":"a\r"}"#.as_slice(),
            br#"{"$anchor":"a\n\n"}"#,
            br#"{"$id":"a#foo"}"#,
        ] {
            assert!(matches!(
                inspect_stage_schema_shape(raw, 10000),
                Err(StageOutputError::InvalidDocument)
            ));
        }
    }
    #[test]
    fn schema_shape_keeps_raw_integer_json_and_nested_keyword_constraints() {
        for raw in [
            br#"{"minimum":1.0}"#.as_slice(),
            br#"{"type":"object","type":"string"}"#,
            br#"{"minimum":18446744073709551616}"#,
            br#"{"properties":{"a":{"required":["x","x"]}}}"#,
            br#"{"prefixItems":[]}"#,
        ] {
            assert!(matches!(
                inspect_stage_schema_shape(raw, 10000),
                Err(StageOutputError::InvalidDocument)
            ));
        }
        assert!(
            inspect_stage_schema_shape(
                br#"{"enum":[],"properties":{"a":false},"required":[]}"#,
                10000
            )
            .is_ok()
        );
    }
    #[test]
    fn resource_exhaustion_is_distinct_from_invalid_schema() {
        assert!(matches!(
            inspect_stage_schema_shape(b"{}", 0),
            Err(StageOutputError::Limit)
        ));
        assert!(matches!(
            inspect_stage_schema_shape(b"{}", 3),
            Err(StageOutputError::Limit)
        ));
        assert!(inspect_stage_schema_shape(b"{}", 4).is_ok());
        assert!(matches!(
            inspect_stage_schema_shape(b"", 0),
            Err(StageOutputError::Limit)
        ));
        assert!(matches!(
            inspect_stage_schema_shape(b"", 1),
            Err(StageOutputError::InvalidDocument)
        ));
    }
}
