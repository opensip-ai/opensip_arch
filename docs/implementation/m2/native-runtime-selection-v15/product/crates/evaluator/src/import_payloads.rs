//! Closed, two-key import payload registration and retained schema checks.
//! Returned data is inert: correspondence, traversal and replay are separate.
use crate::NativeUniverseError;
use crate::native_universe::{array, field, sha256_text, text};
use alloc::{format, string::String};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, RetainedInputError, RetainedInputs,
    SchemaAdmissionError, TraversalBudget, parse_json,
};

#[derive(Debug, PartialEq, Eq)]
pub enum ImportPayloadError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Refused(String),
    Limit,
    Law,
}
impl From<NativeUniverseError> for ImportPayloadError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
fn sha(v: &V) -> Result<[u8; 32], ImportPayloadError> {
    Ok(sha256_text(&format!("sha256:{}", text(v)?))?)
}
fn input(e: RetainedInputError) -> ImportPayloadError {
    match e {
        RetainedInputError::ClosureRole { field, expected } => {
            ImportPayloadError::Refused(format!("CLOSURE_FIELD_KIND:import.{field}:{expected}"))
        }
        e => ImportPayloadError::Record(GraphError::Input(e)),
    }
}
fn charge(budget: &mut TraversalBudget, cost: usize) -> Result<(), ImportPayloadError> {
    if budget.depth == 0 {
        return Err(ImportPayloadError::Limit);
    }
    budget.steps = budget
        .steps
        .checked_sub(cost)
        .ok_or(ImportPayloadError::Limit)?;
    Ok(())
}
fn select<'a>(rows: &'a V, kind: &V, domain: Option<&V>) -> Result<&'a V, ImportPayloadError> {
    for row in array(field(rows, "rows")?)? {
        if field(row, "kind")? == kind && Some(field(row, "payloadDomain")?) == domain {
            if field(row, "document")? != field(row, "ownerDocument")?
                || field(row, "selector")? != field(row, "ownerSelector")?
            {
                return Err(ImportPayloadError::Refused(
                    "PAYLOAD_IMPORT_REGISTRY_DRIFT".into(),
                ));
            }
            return Ok(row);
        }
    }
    Err(ImportPayloadError::Refused(
        "PAYLOAD_IMPORT_UNREGISTERED".into(),
    ))
}
/// Decode a retained import payload before selecting its exact kind/domain row.
/// The schema document's full digest and retained bytes are checked before its
/// selector. No imported claims are executed or promoted to findings. The two
/// registry refusals expose a named code without the reference's Python repr.
pub fn inspect_import_payload(
    inputs: &RetainedInputs<'_>,
    import_id: &str,
    mut budget: TraversalBudget,
) -> Result<V, ImportPayloadError> {
    charge(&mut budget, 1)?;
    let import = inputs
        .object(import_id, IdentityDomain::Import, budget.descriptor_work)
        .map_err(input)?;
    let descriptor = import.descriptor();
    let digest = sha(field(descriptor, "payloadDigest")?)?;
    let schema_digest = sha(field(descriptor, "payloadSchemaDigest")?)?;
    charge(&mut budget, 1)?;
    let blob = inputs.blob(digest).map_err(input)?;
    charge(&mut budget, blob.bytes().len())?;
    let value = blob.canonical_record().map_err(input)?;
    let registry = parse_json(include_bytes!("import-payload-registry.json"))
        .map_err(|_| ImportPayloadError::Law)?;
    let domain = match &value {
        V::Object(o) => o.get("payloadDomain"),
        _ => None,
    };
    let row = select(&registry, field(descriptor, "kind")?, domain)?;
    let document = text(field(row, "document")?)?;
    let selector = text(field(row, "selector")?)?;
    if schema_digest != sha(field(row, "sha256")?)? {
        return Err(ImportPayloadError::Refused(format!(
            "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT:{document}"
        )));
    }
    charge(&mut budget, 1)?;
    inputs
        .registered_record_shape(
            digest,
            schema_digest,
            document,
            selector,
            budget.descriptor_work,
        )
        .map_err(|e| match e {
            GraphError::Schema(SchemaAdmissionError::Schema(
                opensip_identity::SchemaError::Limit,
            ))
            | GraphError::Limit => ImportPayloadError::Limit,
            GraphError::Schema(SchemaAdmissionError::Mismatch) => {
                ImportPayloadError::Refused(format!("PAYLOAD_RECORD:{selector}"))
            }
            e => ImportPayloadError::Record(e),
        })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn two_key_registry_preserves_owner_agreement() {
        let mut rows = parse_json(include_bytes!("import-payload-registry.json")).unwrap();
        for row in array(field(&rows, "rows").unwrap()).unwrap() {
            assert!(
                select(
                    &rows,
                    field(row, "kind").unwrap(),
                    Some(field(row, "payloadDomain").unwrap())
                )
                .is_ok()
            );
        }
        let kind = V::String("runtime".into());
        let domain = V::String("workflow.import-payload.runtime.v1".into());
        let wrong = V::String("workflow.import-payload.history.v1".into());
        assert_eq!(
            select(&rows, &kind, Some(&wrong)),
            Err(ImportPayloadError::Refused(
                "PAYLOAD_IMPORT_UNREGISTERED".into()
            ))
        );
        if let V::Object(root) = &mut rows
            && let V::Array(list) = root.get_mut("rows").unwrap()
        {
            for row in list {
                if let V::Object(row) = row {
                    row.insert("ownerSelector".into(), V::String("#/$defs/wrong".into()));
                }
            }
        }
        assert_eq!(
            select(&rows, &kind, Some(&domain)),
            Err(ImportPayloadError::Refused(
                "PAYLOAD_IMPORT_REGISTRY_DRIFT".into()
            ))
        );
    }
}
