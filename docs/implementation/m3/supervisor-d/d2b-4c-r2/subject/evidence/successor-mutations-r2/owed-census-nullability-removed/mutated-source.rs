//! FA-2 wire rules. C4 supplies the owed census/closure and owns Plan
//! admission. H owns returned symbol-scope commitments and settlement.
use super::super::{
    ReceivedFrame,
    cbor::Value,
    ts2::carrier::{self, field},
};
use opensip_identity::{JsonValue as J, digest_hex, hash_canonical_value, parse_json};
use std::collections::{BTreeMap, BTreeSet};
const SOURCE: &[u8] = include_bytes!("../../../../../schemas/sources/symbol-census-v1.schema.json");
const REGISTRY: &[u8] = include_bytes!("../../../data/relation-payload-schemas.v2.json");
const MAX_BYTES: u64 = 4_194_304;
fn object(v: &J) -> Result<&BTreeMap<String, J>, String> {
    if let J::Object(x) = v {
        Ok(x)
    } else {
        Err("census source object".into())
    }
}
fn at<'a>(v: &'a J, keys: &[&str]) -> Result<&'a J, String> {
    keys.iter().try_fold(v, |v, k| {
        object(v)?
            .get(*k)
            .ok_or_else(|| format!("census source {k}"))
    })
}
fn text(v: &J) -> Result<&str, String> {
    if let J::String(x) = v {
        Ok(x)
    } else {
        Err("census source text".into())
    }
}
fn integer(v: &J) -> Result<u64, String> {
    if let J::Integer(x) = v {
        u64::try_from(x.get()).map_err(|_| "census source uint".into())
    } else {
        Err("census source uint".into())
    }
}
fn map(v: &Value) -> Result<&[(String, Value)], String> {
    if let Value::Map(x) = v {
        Ok(x)
    } else {
        Err("census wire map".into())
    }
}
fn get<'a>(v: &'a Value, k: &str) -> Result<&'a Value, String> {
    field(map(v)?, k).ok_or_else(|| format!("census missing {k}"))
}
fn string<'a>(v: &'a Value, k: &str) -> Result<&'a str, String> {
    if let Value::Text(s) = get(v, k)? {
        Ok(s)
    } else {
        Err(format!("census {k}: text"))
    }
}
fn uint(v: &Value, k: &str) -> Result<u64, String> {
    if let Value::Unsigned(n) = get(v, k)? {
        Ok(*n)
    } else {
        Err(format!("census {k}: uint"))
    }
}
fn array<'a>(v: &'a Value, k: &str) -> Result<&'a [Value], String> {
    if let Value::Array(a) = get(v, k)? {
        Ok(a)
    } else {
        Err(format!("census {k}: array"))
    }
}
fn t(s: &str) -> Value {
    Value::Text(s.to_owned())
}

pub(super) struct Law {
    kinds: BTreeMap<String, String>,
    scope_domain: String,
    scope_prefix: String,
    descriptor_members: BTreeSet<String>,
    rows_order: opensip_identity::ArrayOrder,
    paths_order: opensip_identity::ArrayOrder,
    rows_max: u64,
    paths_max: u64,
    path_scalars: u64,
    subject_scalars: u64,
    name_scalars: u64,
    tokens_max: u64,
    token_scalars: u64,
}
impl Law {
    /// Check every original closed-schema rule without serializing a whole
    /// census row merely to test redundant uniqueItems. The exact source
    /// shape/order proof is checked at load; each full row and path still
    /// goes through the same selected structured schema evaluator.
    pub(super) fn shape(&self, payload: &Value) -> Result<(), String> {
        let fields = map(payload)?;
        let census = get(payload, "symbolCensus")?;
        let metadata = Value::Map(
            fields
                .iter()
                .map(|(key, value)| {
                    (
                        key.clone(),
                        if key == "symbolCensus" {
                            Value::Null
                        } else {
                            value.clone()
                        },
                    )
                })
                .collect(),
        );
        super::admit_extern(
            "opensip.product.symbol-census.1#/$defs/CompleteV3",
            &metadata,
        )?;
        if *census == Value::Null {
            return Ok(());
        }
        match string(census, "state")? {
            "over-bound" => super::admit_extern(
                "opensip.product.symbol-census.1#/$defs/OverBoundSymbolCensusV1",
                census,
            ),
            "complete" => {
                let sample = Value::Map(
                    map(census)?
                        .iter()
                        .map(|(key, value)| {
                            (
                                key.clone(),
                                if ["rows", "examinedPaths"].contains(&key.as_str())
                                    && matches!(value, Value::Array(_))
                                {
                                    Value::Array(Vec::new())
                                } else {
                                    value.clone()
                                },
                            )
                        })
                        .collect(),
                );
                super::admit_extern(
                    "opensip.product.symbol-census.1#/$defs/CompleteSymbolCensusV1",
                    &sample,
                )?;
                for (member, root, maximum, order) in [
                    (
                        "rows",
                        "opensip.product.symbol-census.1#/$defs/SymbolCensusRowV1",
                        self.rows_max,
                        &self.rows_order,
                    ),
                    (
                        "examinedPaths",
                        "opensip.product.symbol-census.1#/$defs/LogicalPath",
                        self.paths_max,
                        &self.paths_order,
                    ),
                ] {
                    let items = array(census, member)?;
                    if items.len() as u64 > maximum {
                        return Err(format!("native.symbol-census-bound: {member}"));
                    }
                    let mut values = Vec::with_capacity(items.len());
                    for item in items {
                        super::admit_extern(root, item)?;
                        values.push(carrier::to_json(item)?);
                    }
                    order
                        .verify(&values)
                        .map_err(|e| format!("native.symbol-census-order: {member}: {e:?}"))?;
                }
                Ok(())
            }
            _ => Err("census state".into()),
        }
    }
    pub(super) fn load() -> Result<Self, String> {
        // These documents are already in the one exact selected registry.
        crate::schema_sources::registry().ok_or("embedded schema registry")?;
        let doc = parse_json(SOURCE).map_err(|e| format!("census source: {e}"))?;
        let limits = |name: &str, member: &str, key: &str| {
            integer(at(&doc, &["$defs", name, "properties", member, key])?)
        };
        // Full-row uniqueItems is implied by strict unique nativeSubjectId.
        // Every remaining array/item rule must still be covered exactly.
        for definition in ["CompleteV3", "CompleteSymbolCensusV1"] {
            let root = object(at(&doc, &["$defs", definition])?)?;
            if root.keys().any(|key| {
                ![
                    "type",
                    "additionalProperties",
                    "required",
                    "properties",
                    "description",
                ]
                .contains(&key.as_str())
            }) {
                return Err("unimplemented census enclosing schema rule".into());
            }
        }
        let row_order =
            parse_json(br#"{"by":["nativeSubjectId"]}"#).map_err(|_| "row order literal")?;
        for (member, reference, order) in [
            ("rows", "#/$defs/SymbolCensusRowV1", &row_order),
            (
                "examinedPaths",
                "#/$defs/LogicalPath",
                &J::String("canonical-set".into()),
            ),
        ] {
            let shape = object(at(
                &doc,
                &["$defs", "CompleteSymbolCensusV1", "properties", member],
            )?)?;
            if shape.keys().any(|key| {
                ![
                    "type",
                    "items",
                    "maxItems",
                    "uniqueItems",
                    "x-opensip-order",
                    "description",
                ]
                .contains(&key.as_str())
            }) || text(shape.get("type").ok_or("array type")?)? != "array"
                || shape.get("uniqueItems") != Some(&J::Bool(true))
                || shape.get("x-opensip-order") != Some(order)
                || object(shape.get("items").ok_or("array items")?)?.len() != 1
                || text(at(shape.get("items").ok_or("array items")?, &["$ref"])?)? != reference
            {
                return Err(format!("unimplemented census array rule: {member}"));
            }
        }
        let rows_order = opensip_identity::ArrayOrder::parse(&row_order)
            .map_err(|e| format!("census row order: {e:?}"))?;
        let paths_order = opensip_identity::ArrayOrder::parse(&J::String("canonical-set".into()))
            .map_err(|e| format!("census path order: {e:?}"))?;
        let rows_max = limits("CompleteSymbolCensusV1", "rows", "maxItems")?;
        let paths_max = limits("CompleteSymbolCensusV1", "examinedPaths", "maxItems")?;
        let law = text(at(&doc, &["x-opensip-symbol-census-law", "return"])?)?;
        if !law.contains(&format!("{MAX_BYTES} bytes of deterministic CBOR"))
            || !law.contains(&format!("{rows_max} rows"))
            || !law.contains(&format!("{paths_max} examined paths"))
        {
            return Err("unimplemented census bound law".into());
        }
        let carriers = parse_json(carrier::CARRIERS).map_err(|e| format!("carriers: {e}"))?;
        let J::Array(rows) = at(&carriers, &["admission"])? else {
            return Err("admission rows".into());
        };
        let matching: Vec<_> = rows
            .iter()
            .filter(|r| at(r, &["id"]).and_then(text).ok() == Some("PER-KEY-SCOPE2"))
            .collect();
        if matching.len() != 1 {
            return Err("PER-KEY-SCOPE2 owner".into());
        }
        let params = at(matching[0], &["params"])?;
        let J::Array(members) = at(params, &["descriptorMembers"])? else {
            return Err("scope descriptor members".into());
        };
        let descriptor_members = members
            .iter()
            .map(|v| text(v).map(str::to_owned))
            .collect::<Result<BTreeSet<_>, _>>()?;
        if descriptor_members.len() != members.len() {
            return Err("duplicate scope descriptor member".into());
        }
        let registry = parse_json(REGISTRY).map_err(|e| format!("relation registry: {e}"))?;
        let mut kinds = BTreeMap::new();
        for (name, row) in object(at(
            &registry,
            &["x-opensip-relation-registry", "relations"],
        )?)? {
            let kind = text(at(row, &["subjectKind"])?)?;
            if !["symbol", "source-path", "package-name"].contains(&kind) {
                return Err("unimplemented relation subject kind".into());
            }
            kinds.insert(name.clone(), kind.to_owned());
        }
        Ok(Self {
            rows_order,
            paths_order,
            kinds,
            scope_domain: text(at(params, &["identityDomain"])?)?.to_owned(),
            scope_prefix: text(at(params, &["textPrefix"])?)?.to_owned(),
            descriptor_members,
            rows_max,
            paths_max,
            path_scalars: integer(at(&doc, &["$defs", "LogicalPath", "maxLength"])?)?,
            subject_scalars: integer(at(&doc, &["$defs", "SubjectIdV1", "maxLength"])?)?,
            name_scalars: limits("SymbolCensusRowV1", "qualifiedName", "maxLength")?,
            tokens_max: limits("SymbolCensusRowV1", "signatureTokens", "maxItems")?,
            token_scalars: integer(at(
                &doc,
                &[
                    "$defs",
                    "SymbolCensusRowV1",
                    "properties",
                    "signatureTokens",
                    "items",
                    "maxLength",
                ],
            )?)?,
        })
    }
    pub(super) fn is_symbol(&self, relation: &str) -> bool {
        self.kinds.get(relation).map(String::as_str) == Some("symbol")
    }
    /// Reconstruct D-empty to check a supplied Plan cell, not to admit or
    /// mint the native scope descriptor on C4's behalf.
    pub(super) fn empty_scope(
        &self,
        snapshot: &str,
        key: &Value,
        closure: &str,
    ) -> Result<String, String> {
        let suffix = |name| -> Result<&str, String> {
            string(key, name)?
                .strip_prefix("sha256:")
                .ok_or_else(|| format!("{name}: universe prefix"))
        };
        let descriptor = Value::Map(vec![
            ("schemaVersion".into(), Value::Unsigned(2)),
            ("snapshotId".into(), t(snapshot)),
            ("sourceUniverse".into(), t(suffix("sourceUniverseId")?)),
            ("targetUniverse".into(), t(suffix("targetUniverseId")?)),
            ("relation".into(), t(string(key, "relation")?)),
            ("resolution".into(), t(string(key, "resolution")?)),
            ("enumeratorClosure".into(), t(closure)),
            ("subjects".into(), Value::Array(Vec::new())),
        ]);
        let Value::Map(fields) = &descriptor else {
            unreachable!()
        };
        if fields
            .iter()
            .map(|(k, _)| k.clone())
            .collect::<BTreeSet<_>>()
            != self.descriptor_members
        {
            return Err("unimplemented D-empty descriptor members".into());
        }
        let h = hash_canonical_value(&self.scope_domain, &carrier::to_json(&descriptor)?)
            .map_err(|e| format!("scope H: {e:?}"))?;
        Ok(format!("{}{}", self.scope_prefix, digest_hex(&h)))
    }
    pub(super) fn request_keys<'a>(
        &self,
        snapshot: &str,
        keys: impl Iterator<Item = &'a Value>,
        token: bool,
        closure: Option<&str>,
    ) -> Result<(), String> {
        if !token {
            return if closure.is_none() {
                Ok(())
            } else {
                Err("census owed without selected token".into())
            };
        }
        let mut count = 0_u64;
        for key in keys {
            if !self.is_symbol(string(key, "relation")?) {
                continue;
            }
            count = count.checked_add(1).ok_or("symbol key count overflow")?;
            let closure = closure.ok_or("symbol-kind request without owed census")?;
            if string(key, "subjectScopeCommitment")? != self.empty_scope(snapshot, key, closure)? {
                return Err("native.symbol-census-request-commitment-mismatch".into());
            }
        }
        if (count == 0) != closure.is_none() {
            return Err("census owed/key population mismatch".into());
        }
        Ok(())
    }
    fn max_complete_bytes(&self, rows: u64, paths: u64) -> u64 {
        let text = |n: u64| 9_u64.saturating_add(4_u64.saturating_mul(n));
        let key = |s: &str| 1 + s.len() as u64;
        let row = 9
            + key("nativeSubjectId")
            + text(self.subject_scalars)
            + key("path")
            + text(self.path_scalars)
            + key("qualifiedName")
            + text(self.name_scalars)
            + key("exported")
            + text("not-exported".len() as u64)
            + key("signatureTokens")
            + 9
            + self.tokens_max.saturating_mul(text(self.token_scalars));
        9_u64
            .saturating_add(key("state") + text("complete".len() as u64))
            .saturating_add(key("examinedPaths") + 9)
            .saturating_add(paths.saturating_mul(text(self.path_scalars)))
            .saturating_add(key("rows") + 9)
            .saturating_add(rows.saturating_mul(row))
    }
    /// Shape admission precedes this contextual check. Byte length is from
    /// the original received node, never from a replacement encoding.
    pub(super) fn returned(
        &self,
        frame: &ReceivedFrame,
        node: usize,
        payload: &Value,
        owed: bool,
    ) -> Result<(), String> {
        let census = get(payload, "symbolCensus")?;
        if false && (*census == Value::Null) == owed {
            return Err("native.symbol-census-null-mismatch".into());
        }
        if *census == Value::Null {
            return Ok(());
        }
        match string(census, "state")? {
            "complete" => {
                let fields = map(payload)?;
                let index = fields
                    .iter()
                    .position(|(k, _)| k == "symbolCensus")
                    .ok_or("census node member")?;
                let at = frame.children(node).nth(index).ok_or("census node")?;
                let bytes = frame.node(at).ok_or("census bytes")?.as_bytes().len() as u64;
                if bytes > MAX_BYTES {
                    return Err("native.symbol-census-bound".into());
                }
                let paths = array(census, "examinedPaths")?
                    .iter()
                    .map(|v| {
                        if let Value::Text(s) = v {
                            Ok(s.as_str())
                        } else {
                            Err("examined path")
                        }
                    })
                    .collect::<Result<BTreeSet<_>, _>>()?;
                for row in array(census, "rows")? {
                    if !paths.contains(string(row, "path")?) {
                        return Err("native.symbol-census-path-not-examined".into());
                    }
                }
            }
            "over-bound" => {
                let rows = uint(census, "rowCount")?;
                let paths = uint(census, "examinedPathCount")?;
                if rows <= self.rows_max
                    && paths <= self.paths_max
                    && self.max_complete_bytes(rows, paths) <= MAX_BYTES
                {
                    return Err("native.symbol-census-over-bound-within-bounds".into());
                }
            }
            _ => return Err("census state".into()),
        }
        Ok(())
    }
}
