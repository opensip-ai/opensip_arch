//! Retained normalized-body frame checks for one owning clone fact.
//! These diagnostics do not admit a Plan, provider semantics, or complete Run.
use crate::native_retention::inspect_native_frame_inputs;
use crate::native_universe::{array, field, sha256_text, text};
use crate::{NativeRetentionError, NativeUniverseError};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::String,
    vec::Vec,
};
use opensip_identity::{
    GraphError, IdentityDomain, JsonInteger, JsonValue as V, NativeFrameSet, RetainedInputs,
    TraversalBudget, canonical_bytes, parse_json, raw_sha256,
};
#[derive(Debug, PartialEq, Eq)]
pub enum BodyIdentityError {
    Owner(NativeUniverseError),
    Retention(NativeRetentionError),
    Record(GraphError),
    Refused(String),
    Limit,
}
impl From<NativeUniverseError> for BodyIdentityError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
impl From<NativeRetentionError> for BodyIdentityError {
    fn from(e: NativeRetentionError) -> Self {
        Self::Retention(e)
    }
}
fn no<T>(cause: impl Into<String>) -> Result<T, BodyIdentityError> {
    Err(BodyIdentityError::Refused(cause.into()))
}
fn get<'a>(v: &'a V, k: &str) -> Option<&'a V> {
    if let V::Object(o) = v { o.get(k) } else { None }
}
fn map(v: &V) -> Result<&BTreeMap<String, V>, NativeUniverseError> {
    if let V::Object(o) = v {
        Ok(o)
    } else {
        Err(NativeUniverseError::RegistryLaw)
    }
}
fn path<'a>(mut v: &'a V, p: &V) -> Result<&'a V, NativeUniverseError> {
    for k in array(p)? {
        v = field(v, text(k)?)?;
    }
    Ok(v)
}
fn bare(v: &V) -> Result<[u8; 32], NativeUniverseError> {
    sha256_text(&format!("sha256:{}", text(v)?))
}
fn number(v: &V) -> Result<usize, NativeUniverseError> {
    if let V::Integer(n) = v {
        usize::try_from(n.get()).map_err(|_| NativeUniverseError::RegistryLaw)
    } else {
        Err(NativeUniverseError::RegistryLaw)
    }
}
fn take<'a>(
    raw: &'a [u8],
    p: &mut usize,
    n: usize,
    cause: &str,
) -> Result<&'a [u8], BodyIdentityError> {
    let end = p
        .checked_add(n)
        .ok_or_else(|| BodyIdentityError::Refused(cause.into()))?;
    let value = raw
        .get(*p..end)
        .ok_or_else(|| BodyIdentityError::Refused(cause.into()))?;
    *p = end;
    Ok(value)
}
fn be(raw: &[u8]) -> usize {
    raw.iter().fold(0usize, |n, b| (n << 8) | usize::from(*b))
}
fn body_frame(raw: &[u8]) -> Result<[&[u8]; 6], BodyIdentityError> {
    let mut fields: [&[u8]; 6] = [&[]; 6];
    let mut p = 0;
    for field in fields.iter_mut().take(5) {
        let n = be(take(raw, &mut p, 1, "BODY_FRAME_TRUNCATED")?);
        *field = take(raw, &mut p, n, "BODY_FRAME_TRUNCATED")?;
    }
    let n = be(take(raw, &mut p, 4, "BODY_FRAME_TRUNCATED")?);
    fields[5] = take(raw, &mut p, n, "BODY_FRAME_TRAILING")?;
    if p != raw.len() {
        return no("BODY_FRAME_TRAILING");
    }
    Ok(fields)
}
fn token_stream(raw: &[u8], steps: usize) -> Result<usize, BodyIdentityError> {
    let mut p = 0;
    let count = be(take(raw, &mut p, 4, "BODY_TOKEN_STREAM_TRUNCATED")?);
    if count > steps {
        return Err(BodyIdentityError::Limit);
    }
    for _ in 0..count {
        let n = be(take(raw, &mut p, 2, "BODY_TOKEN_STREAM_TRUNCATED")?);
        take(raw, &mut p, n, "BODY_TOKEN_STREAM_TRUNCATED")?;
        let n = be(take(raw, &mut p, 4, "BODY_TOKEN_STREAM_TRUNCATED")?);
        take(raw, &mut p, n, "BODY_TOKEN_STREAM_TRUNCATED")?;
    }
    if p != raw.len() {
        return no("BODY_TOKEN_STREAM_TRAILING");
    }
    Ok(count)
}
/// Private diagnostic fields preserve the distinction between L0 recomputation
/// and L1-L3 framed custody. Neither case qualifies a provider or normalizer.
pub struct BodyIdentityChecks {
    digest: [u8; 32],
    language_version: [u8; 32],
    recomputed: bool,
    tokens: usize,
}
impl BodyIdentityChecks {
    pub fn digest(&self) -> [u8; 32] {
        self.digest
    }
    pub fn language_version(&self) -> [u8; 32] {
        self.language_version
    }
    pub fn source_recomputed(&self) -> bool {
        self.recomputed
    }
    pub fn token_count(&self) -> usize {
        self.tokens
    }
}
fn projection(
    inputs: &RetainedInputs<'_>,
    universe: &V,
    context: &V,
    row: &V,
    anchor: &V,
    budget: TraversalBudget,
) -> Result<V, BodyIdentityError> {
    let Some(binding) = get(row, "languageVersionBinding") else {
        return no(format!(
            "BODY_LANGUAGE_UNIVERSE_UNBOUND:{}",
            text(field(row, "language")?)?
        ));
    };
    let mut record = BTreeMap::from([(
        String::from("schemaVersion"),
        V::Integer(JsonInteger::new(1).map_err(|_| NativeUniverseError::RegistryLaw)?),
    )]);
    for (name, source) in map(field(binding, "fields")?)? {
        let value = if let Some(c) = get(source, "const") {
            c
        } else {
            path(
                if text(field(source, "source")?)? == "native-context" {
                    context
                } else {
                    universe
                },
                field(source, "path")?,
            )?
        };
        record.insert(name.clone(), value.clone());
    }
    let dialect = field(binding, "dialect")?;
    let anchor_path = text(field(anchor, "path")?)?;
    let variant = match text(field(dialect, "form")?)? {
        "closed-suffix-table" => {
            let table = map(field(dialect, "table")?)?;
            let selected = table
                .iter()
                .filter(|(k, _)| anchor_path.ends_with(k.as_str()))
                .max_by_key(|(k, _)| k.len());
            let Some((_, variant)) = selected else {
                return no(format!(
                    "{}:{anchor_path}",
                    text(field(dialect, "onUnknown")?)?
                ));
            };
            record.insert(
                "languageId".into(),
                field(field(binding, "bodyLanguageByVariant")?, text(variant)?)?.clone(),
            );
            variant.clone()
        }
        "selected-compilation-target-edition" => {
            let language = field(binding, "bodyLanguage")?;
            record.insert("languageId".into(), language.clone());
            let editions = map(path(universe, field(dialect, "path")?)?)?;
            if editions.is_empty() {
                return no(format!(
                    "{}:{}",
                    text(field(dialect, "onEmpty")?)?,
                    text(language)?
                ));
            }
            let spec = field(dialect, "ownership")?;
            let retained_as = text(field(spec, "retainedAs")?)?;
            let mut ownership = None;
            for join in array(field(row, "nestedIdentities")?)? {
                if get(join, "retainedAs").map(text).transpose()? != Some(retained_as) {
                    continue;
                }
                let reference = path(universe, field(join, "path")?)?;
                if reference == &V::Null {
                    continue;
                }
                let d = match text(field(join, "form")?)? {
                    "sha256-text" => sha256_text(text(reference)?)?,
                    "bare-hex" => bare(reference)?,
                    _ => return Err(NativeUniverseError::RegistryLaw.into()),
                };
                ownership = Some(
                    inputs
                        .frame_candidate(d, NativeFrameSet::Nested, budget.descriptor_work)
                        .map_err(BodyIdentityError::Record)?
                        .descriptor()
                        .clone(),
                );
            }
            let Some(ownership) = ownership else {
                return no(format!(
                    "{}:{}",
                    text(field(dialect, "onOwnershipMissing")?)?,
                    editions.len()
                ));
            };
            if text(field(&ownership, text(field(spec, "enumerationField")?)?)?)? != "complete" {
                return no(format!(
                    "{}:{anchor_path}",
                    text(field(dialect, "onOwnerUnenumerated")?)?
                ));
            }
            let unit_field = text(field(spec, "unitField")?)?;
            let units = array(field(&ownership, text(field(spec, "unitsField")?)?)?)?
                .iter()
                .map(|u| Ok((text(field(u, unit_field)?)?, u)))
                .collect::<Result<BTreeMap<_, _>, NativeUniverseError>>()?;
            let mut rows = Vec::new();
            for r in array(field(&ownership, "ownership")?)? {
                if text(field(r, text(field(spec, "pathField")?)?)?)? == anchor_path {
                    rows.push(r);
                }
            }
            if rows.is_empty() {
                return no(format!(
                    "{}:{anchor_path}",
                    text(field(dialect, "onOwnerNotCompiled")?)?
                ));
            }
            let selected = array(field(&ownership, text(field(spec, "selectionField")?)?)?)?;
            let chosen: Vec<_> = rows
                .into_iter()
                .filter(|r| get(r, unit_field).is_some_and(|v| selected.contains(v)))
                .collect();
            if chosen.is_empty() {
                return no(format!(
                    "{}:{anchor_path}",
                    text(field(dialect, "onOwnerNotSelected")?)?
                ));
            }
            let mut unknown = BTreeSet::new();
            for r in &chosen {
                let id = text(field(r, unit_field)?)?;
                if !units.contains_key(id) {
                    unknown.insert(id);
                }
            }
            if !unknown.is_empty() {
                return no(format!(
                    "{}:unknown-unit:{}",
                    text(field(dialect, "onOwnerAmbiguous")?)?,
                    unknown.into_iter().collect::<Vec<_>>().join(",")
                ));
            }
            let mut effective = BTreeSet::new();
            for r in chosen {
                let unit = units[text(field(r, unit_field)?)?];
                let target = field(unit, text(field(spec, "targetEditionField")?)?)?;
                if target != &V::Null {
                    effective.insert(number(target)?);
                } else {
                    let name = text(field(unit, text(field(spec, "crateField")?)?)?)?;
                    let Some(edition) = editions.get(name) else {
                        return no(format!(
                            "{}:unknown-crate:{name}",
                            text(field(dialect, "onOwnerAmbiguous")?)?
                        ));
                    };
                    effective.insert(number(edition)?);
                }
            }
            if effective.len() > 1 {
                return no(format!(
                    "{}:{anchor_path}:{}",
                    text(field(dialect, "onOwnerAmbiguous")?)?,
                    effective.len()
                ));
            }
            V::Integer(
                JsonInteger::new(
                    effective
                        .into_iter()
                        .next()
                        .ok_or(NativeUniverseError::RegistryLaw)? as i128,
                )
                .map_err(|_| NativeUniverseError::RegistryLaw)?,
            )
        }
        form => return no(format!("BODY_LANGUAGE_DIALECT_FORM:{form}")),
    };
    record.insert(
        "dialect".into(),
        V::Object(BTreeMap::from([(
            text(field(dialect, "key")?)?.into(),
            variant,
        )])),
    );
    let value = V::Object(record);
    inputs
        .check_identity_value_shape(&value, "body-language-version", budget.descriptor_work)
        .map_err(BodyIdentityError::Record)?;
    Ok(value)
}
fn specification(
    inputs: &RetainedInputs<'_>,
    level: &str,
    version: [u8; 32],
    closure: &V,
    law: &V,
    work: usize,
) -> Result<(), BodyIdentityError> {
    let tree = array(field(closure, "tree")?)?;
    let location = text(field(law, "closureTreePath")?)?;
    let entry = tree
        .iter()
        .find(|r| get(r, "path").and_then(|v| text(v).ok()) == Some(location));
    let Some(entry) = entry else {
        return no(format!("BODY_NORMALIZATION_MAP_MISSING:{location}"));
    };
    let digest = bare(field(entry, "sha256")?)?;
    // Missing/corrupt retained bytes remain input errors, rather than being
    // relabeled as malformed metadata. Schema/canonical/order faults are maps.
    inputs
        .blob(digest)
        .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
    let record = inputs
        .identity_record_shape(digest, "normalization-specification-map", work)
        .map_err(|e| match e {
            GraphError::Schema(opensip_identity::SchemaAdmissionError::Schema(
                opensip_identity::SchemaError::Limit,
            )) => BodyIdentityError::Limit,
            _ => BodyIdentityError::Refused("BODY_NORMALIZATION_MAP_INVALID".into()),
        })?;
    let rows = array(field(&record, "levels")?)?;
    let mut previous = None;
    let mut selected = None;
    for r in rows {
        let current = text(field(r, "level")?)?;
        if previous.is_some_and(|p| p >= current) {
            return no("BODY_NORMALIZATION_MAP_INVALID");
        }
        previous = Some(current);
        if current == level {
            selected = Some(r);
        }
    }
    let Some(selected) = selected else {
        return no(format!("BODY_NORMALIZATION_LEVEL_UNMAPPED:{level}"));
    };
    if bare(field(selected, "specificationDigest")?)? != version {
        return no(format!("BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:{level}"));
    }
    if !tree
        .iter()
        .any(|r| get(r, "sha256").and_then(|v| bare(v).ok()) == Some(version))
    {
        return no(format!(
            "BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:{level}"
        ));
    }
    inputs
        .blob(version)
        .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
    Ok(())
}
/// Check one clone fact's retained body identity. Local payload/snapshot laws,
/// native frame retention and context admission run afresh; universe/Plan
/// selection, capability/coverage and global Run joins remain separate. No
/// caller-supplied ADMIT or normalization result is trusted as proof. The
/// normalized token stream is checked for framing/custody only, not semantics.
pub fn inspect_body_identity(
    inputs: &RetainedInputs<'_>,
    fact_id: &str,
    budget: TraversalBudget,
) -> Result<BodyIdentityChecks, BodyIdentityError> {
    if budget.steps == 0 || budget.depth == 0 {
        return Err(BodyIdentityError::Limit);
    }
    let fact = inputs
        .object(fact_id, IdentityDomain::Fact, budget.descriptor_work)
        .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
    let f = fact.descriptor();
    if text(field(f, "relation")?)? != "clones" {
        return no("BODY_RELATION_NOT_SELECTED");
    }
    let sha = bare(field(f, "payloadDigest")?)?;
    let schema = bare(field(f, "payloadSchemaDigest")?)?;
    inputs
        .inspect_relation_snapshot(sha, schema, f, budget)
        .map_err(BodyIdentityError::Record)?;
    let payload = inputs
        .blob(sha)
        .and_then(|b| b.canonical_record())
        .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
    let law = parse_json(include_bytes!("body-registry.json"))
        .map_err(|_| NativeUniverseError::RegistryLaw)?;
    let relation = field(&law, "clones")?;
    let join = field(relation, "bodyIdentityJoin")?;
    let d = sha256_text(text(field(&payload, text(field(join, "field")?)?)?)?)?;
    let raw = inputs
        .blob(d)
        .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
    let level = text(field(&payload, text(field(join, "levelField")?)?)?)?;
    let version = bare(field(&payload, text(field(join, "levelVersionField")?)?)?)?;
    inputs
        .blob(version)
        .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
    let [
        tag,
        level_id,
        version_bytes,
        language,
        language_version,
        body,
    ] = body_frame(raw.bytes())?;
    if tag != text(field(join, "domainTag")?)?.as_bytes() {
        return no("BODY_IDENTITY_DOMAIN");
    }
    if level_id != level.as_bytes() {
        return no("BODY_IDENTITY_LEVEL_JOIN");
    }
    if version_bytes != version {
        return no("BODY_IDENTITY_LEVEL_VERSION_JOIN");
    }
    let uid = bare(field(f, "sourceUniverse")?)?;
    let sid = text(field(f, "snapshotId")?)?;
    inspect_native_frame_inputs(inputs, uid, NativeFrameSet::SemanticUniverse, sid, budget)?;
    let u = inputs
        .frame_candidate(
            uid,
            NativeFrameSet::SemanticUniverse,
            budget.descriptor_work,
        )
        .map_err(BodyIdentityError::Record)?;
    let row = u.registry_row();
    let value = u.descriptor();
    let binding = field(row, "languageVersionBinding")?;
    let lang = core::str::from_utf8(language)
        .map_err(|_| BodyIdentityError::Refused("BODY_IDENTITY_LANGUAGE_UTF8".into()))?;
    if !array(field(binding, "bodyLanguages")?)?
        .iter()
        .any(|v| matches!(v,V::String(s) if s==lang))
    {
        return no(format!("BODY_IDENTITY_LANGUAGE_JOIN:{lang}"));
    }
    if text(field(row, "contextForm")?)? != "sha256-text" {
        return no("BODY_LANGUAGE_CONTEXT_FORM");
    }
    let cid = sha256_text(text(path(value, field(row, "contextField")?)?)?)?;
    inspect_native_frame_inputs(inputs, cid, NativeFrameSet::Context, sid, budget)?;
    let c = inputs
        .frame_candidate(cid, NativeFrameSet::Context, budget.descriptor_work)
        .map_err(BodyIdentityError::Record)?;
    if c.domain() != text(field(row, "contextDomain")?)? {
        return no(format!(
            "BODY_LANGUAGE_UNIVERSE_CONTEXT_DOMAIN:{}",
            c.domain()
        ));
    }
    let interpreter = text(path(
        c.descriptor(),
        field(field(binding, "normalizationClosure")?, "path")?,
    )?)?;
    let closure = inputs
        .object(interpreter, IdentityDomain::Closure, budget.descriptor_work)
        .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
    specification(
        inputs,
        level,
        version,
        closure.descriptor(),
        field(&law, "normalizationSpecificationLaw")?,
        budget.descriptor_work,
    )?;
    if field(field(relation, "anchorLaw")?, "cardinality")? != field(join, "anchorCardinality")? {
        return no("RELATION_ANCHOR_LAW_DRIFT:clones");
    }
    let anchor = array(field(f, "anchors")?)?
        .first()
        .ok_or(NativeUniverseError::RegistryLaw)?;
    let projected = projection(inputs, value, c.descriptor(), row, anchor, budget)?;
    if text(field(&projected, "languageId")?)? != lang {
        return no(format!("BODY_IDENTITY_LANGUAGE_JOIN:{lang}"));
    }
    let projection_bytes =
        canonical_bytes(&projected).map_err(|_| NativeUniverseError::RegistryLaw)?;
    let derived = raw_sha256(&projection_bytes);
    if language_version != derived {
        return no("BODY_IDENTITY_LANGUAGE_VERSION_JOIN");
    }
    let recomputed = array(field(join, "recomputableAt")?)?
        .iter()
        .any(|v| matches!(v,V::String(s)if s==level));
    let tokens = if recomputed {
        let source = inputs
            .blob(bare(field(anchor, "blobDigest")?)?)
            .map_err(|e| BodyIdentityError::Record(GraphError::Input(e)))?;
        let start = number(field(anchor, "startByte")?)?.min(source.bytes().len());
        let end = number(field(anchor, "endByte")?)?.min(source.bytes().len());
        // This local recipe matches Python slicing; full anchor custody/range
        // admission is a separate graph obligation and is not claimed here.
        let span = if start <= end {
            &source.bytes()[start..end]
        } else {
            &[]
        };
        if body.len() != span.len() + 4
            || body.get(..4) != Some(&(span.len() as u32).to_be_bytes())
            || body.get(4..) != Some(span)
        {
            return no("BODY_IDENTITY_BODY_SPAN");
        }
        0
    } else {
        token_stream(body, budget.steps)?
    };
    Ok(BodyIdentityChecks {
        digest: d,
        language_version: derived,
        recomputed,
        tokens,
    })
}
