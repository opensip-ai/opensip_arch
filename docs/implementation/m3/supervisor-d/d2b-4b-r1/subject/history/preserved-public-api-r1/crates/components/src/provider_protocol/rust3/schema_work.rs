//! A conservative bound on the existing schema evaluator's meter credits.
//!
//! Let W be one credit per value node plus UTF-8 string/key bytes. For
//! strict byte-free deterministic CBOR, W <= encoded payload length. The
//! selected acyclic schema's coefficient C bounds evaluation by C*W:
//! branches/refs add; repeated items share the maximum child coefficient;
//! object patterns add. Fixed schema literals are amortized by W >= 1.
//! Full input precharge adds one coefficient. This changes no schema rule,
//! transport limit, JSON profile, CAN eligibility or semantic authority.
use super::super::{cbor, ts2::carrier};
use opensip_identity::{JsonValue as J, parse_json};
use std::collections::{BTreeMap, BTreeSet};
use std::sync::OnceLock;

type R<T> = Result<T, String>;
const ROOTS: &[&str] = &[
    "opensip.product.occupancy-companion.1#",
    "opensip.product.provider-handshake.1#/$defs/HelloAckV3",
    "opensip.product.provider-handshake.1#/$defs/HelloV3",
    "opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3",
    "opensip.product.provider-startup.1#/$defs/CoverageV3",
    "opensip.product.provider-startup.1#/$defs/NativeContextVerifiedV1",
    "opensip.product.provider-startup.1#/$defs/OpenUniverseV3",
    "opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1",
    "opensip.product.provider-startup.1#/$defs/UnavailableV3",
    "opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3",
    // LD-D2B-17's host builder (4b). These are the same selected registry
    // and evaluator; adding the two callers recomputes their bounded work
    // closure and grants no reference-response or worker admission (4c).
    "opensip.product.rust-subject-scope.1#/$defs/RustSubjectScopeV1",
    "opensip.product.rust-subject-scope.1#/$defs/StageRequestV3",
    "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3",
    "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3",
    "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3",
    "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/PreparedOutputRowV3",
    "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/Relation",
    "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/Rung",
];
fn add(total: &mut usize, value: usize) -> R<()> {
    *total = total.checked_add(value).ok_or("schema work overflow")?;
    Ok(())
}
fn object(v: &J) -> R<&BTreeMap<String, J>> {
    match v {
        J::Object(v) => Ok(v),
        _ => Err("schema object".to_owned()),
    }
}
fn array(v: &J) -> R<&[J]> {
    match v {
        J::Array(v) => Ok(v),
        _ => Err("schema array".to_owned()),
    }
}
fn text(v: &J) -> R<&str> {
    match v {
        J::String(v) => Ok(v),
        _ => Err("schema text".to_owned()),
    }
}
fn weight(v: &J) -> R<usize> {
    let mut n = 1;
    match v {
        J::String(s) => add(&mut n, s.len())?,
        J::Array(items) => {
            for v in items {
                add(&mut n, weight(v)?)?;
            }
        }
        J::Object(items) => {
            for (key, v) in items {
                add(&mut n, key.len())?;
                add(&mut n, weight(v)?)?;
            }
        }
        _ => {}
    }
    Ok(n)
}
struct Derivation {
    documents: BTreeMap<String, J>,
    memo: BTreeMap<String, usize>,
    active: BTreeSet<String>,
}
impl Derivation {
    fn reference(&mut self, reference: &str, owner: &str) -> R<usize> {
        let (base, pointer) = reference.split_once('#').ok_or("schema ref")?;
        let base = if base.is_empty() { owner } else { base };
        let key = format!("{base}#{pointer}");
        if let Some(n) = self.memo.get(&key) {
            return Ok(*n);
        }
        if !self.active.insert(key.clone()) {
            return Err("recursive schema work closure".to_owned());
        }
        let mut node = self.documents.get(base).ok_or("schema document")?;
        if !pointer.is_empty() && !pointer.starts_with('/') {
            return Err("schema pointer".to_owned());
        }
        for token in pointer.split('/').skip(1) {
            node = object(node)?
                .get(&token.replace("~1", "/").replace("~0", "~"))
                .ok_or("schema pointer member")?;
        }
        // Clone only the fixed public schema node, never the received value.
        let node = node.clone();
        let n = self.coefficient(&node, base)?;
        self.active.remove(&key);
        self.memo.insert(key, n);
        Ok(n)
    }
    fn coefficient(&mut self, schema: &J, owner: &str) -> R<usize> {
        if matches!(schema, J::Bool(_)) {
            return Ok(1);
        }
        let s = object(schema)?;
        let mut out = 1;
        if let Some(v) = s.get("$ref") {
            add(&mut out, self.reference(text(v)?, owner)?)?;
        }
        if let Some(v) = s.get("const") {
            add(&mut out, 1)?;
            add(&mut out, weight(v)?)?;
        }
        if let Some(v) = s.get("enum") {
            for v in array(v)? {
                add(&mut out, 1)?;
                add(&mut out, weight(v)?)?;
            }
        }
        for key in ["allOf", "anyOf", "oneOf"] {
            if let Some(v) = s.get(key) {
                for child in array(v)? {
                    add(&mut out, self.coefficient(child, owner)?)?;
                }
            }
        }
        for key in ["not", "if", "then", "else"] {
            if let Some(v) = s.get(key) {
                add(&mut out, self.coefficient(v, owner)?)?;
            }
        }
        let mut child_max = 0;
        if let Some(v) = s.get("prefixItems") {
            for v in array(v)? {
                child_max = child_max.max(self.coefficient(v, owner)?);
            }
        }
        if let Some(v) = s.get("items") {
            child_max = child_max.max(self.coefficient(v, owner)?);
        }
        let mut arr = 1;
        add(&mut arr, child_max)?;
        if let Some(v) = s.get("contains") {
            add(&mut arr, self.coefficient(v, owner)?)?;
        }
        // canonical JSON bytes <= 32*W: integers need <=21 bytes, escaped
        // string/key bytes <=6 each, and container punctuation is bounded
        // by the value nodes. The uniqueness scan additionally charges W.
        if s.get("uniqueItems") == Some(&J::Bool(true)) {
            add(&mut arr, 33)?;
        }
        if let Some(v) = s.get("x-opensip-order") {
            add(&mut arr, 1)?;
            add(&mut arr, weight(v)?)?;
        }
        let mut obj = 1;
        if let Some(v) = s.get("required") {
            for key in array(v)? {
                add(&mut obj, 1)?;
                add(&mut obj, text(key)?.len())?;
            }
        }
        if let Some(v) = s.get("propertyNames") {
            add(&mut obj, self.coefficient(v, owner)?)?;
        }
        let mut named_max = 0;
        if let Some(v) = s.get("properties") {
            for v in object(v)?.values() {
                named_max = named_max.max(self.coefficient(v, owner)?);
            }
        }
        add(&mut obj, named_max)?;
        if let Some(v) = s.get("patternProperties") {
            for v in object(v)?.values() {
                add(&mut obj, 1)?;
                add(&mut obj, self.coefficient(v, owner)?)?;
            }
        }
        if let Some(v) = s.get("additionalProperties") {
            add(&mut obj, self.coefficient(v, owner)?)?;
        }
        add(&mut out, arr.max(obj).max(1))?;
        Ok(out)
    }
}
fn factors() -> R<BTreeMap<String, usize>> {
    // The registry first checks all52 raw-document pins and selected aliases.
    crate::schema_sources::registry().ok_or("embedded registry")?;
    let mut documents = BTreeMap::new();
    for raw in crate::schema_sources::sources() {
        let doc = parse_json(raw).map_err(|e| format!("schema source: {e}"))?;
        let id = text(object(&doc)?.get("$id").ok_or("schema id")?)?.to_owned();
        if documents.insert(id, doc).is_some() {
            return Err("duplicate schema id".to_owned());
        }
    }
    let mut d = Derivation {
        documents,
        memo: BTreeMap::new(),
        active: BTreeSet::new(),
    };
    ROOTS
        .iter()
        .map(|reference| {
            let mut coefficient = d.reference(reference, "")?;
            add(&mut coefficient, 1)?; // complete input precharge
            Ok(((*reference).to_owned(), coefficient))
        })
        .collect()
}
pub(crate) fn admit_extern(reference: &str, value: &cbor::Value) -> R<()> {
    static FACTORS: OnceLock<R<BTreeMap<String, usize>>> = OnceLock::new();
    let factors = FACTORS
        .get_or_init(factors)
        .as_ref()
        .map_err(Clone::clone)?;
    let coefficient = factors.get(reference).ok_or("unselected Rust3 work root")?;
    let length = usize::try_from(cbor::encoded_length(value).ok_or("payload length overflow")?)
        .map_err(|_| "payload length range")?;
    let budget = length
        .checked_mul(*coefficient)
        .ok_or("schema work budget overflow")?;
    let (id, selector) = reference.split_once('#').ok_or("schema ref")?;
    crate::schema_sources::registry()
        .ok_or("embedded registry")?
        .schema(id, selector)
        .map_err(|e| format!("{reference}: {e:?}"))?
        .admit_value(&carrier::to_json(value)?, budget)
        .map(|_| ())
        .map_err(|e| format!("{reference}: {e:?}"))
}
