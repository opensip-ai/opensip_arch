//! Exact selected keyword semantics. Shape validation never mints semantic trust.
use crate::{ArrayOrder, JsonValue as V, canonical_bytes, parse_json};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    string::{String, ToString},
    vec::Vec,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Error {
    Schema,
    Reference,
    UnselectedEntry,
    Pattern,
    Limit,
    Json,
}
const DIALECT: &str = "https://json-schema.org/draft/2020-12/schema";
const DEPTH: usize = 128;
struct Meter {
    remaining: usize,
}
impl Meter {
    fn spend(&mut self, cost: usize) -> Result<(), Error> {
        self.remaining = self.remaining.checked_sub(cost).ok_or(Error::Limit)?;
        Ok(())
    }
    // Charge a structural walk before repeated equality/canonical operations.
    fn value(&mut self, v: &V, depth: usize) -> Result<(), Error> {
        if depth > DEPTH {
            return Err(Error::Limit);
        }
        self.spend(1)?;
        match v {
            V::String(s) => self.spend(s.len())?,
            V::Array(a) => {
                for v in a {
                    self.value(v, depth + 1)?
                }
            }
            V::Object(o) => {
                for (k, v) in o {
                    self.spend(k.len())?;
                    self.value(v, depth + 1)?
                }
            }
            _ => {}
        }
        Ok(())
    }
}
fn obj(v: &V) -> Result<&BTreeMap<String, V>, Error> {
    if let V::Object(o) = v {
        Ok(o)
    } else {
        Err(Error::Schema)
    }
}
fn text(v: &V) -> Result<&str, Error> {
    if let V::String(s) = v {
        Ok(s)
    } else {
        Err(Error::Schema)
    }
}
fn array(v: &V) -> Result<&[V], Error> {
    if let V::Array(a) = v {
        Ok(a)
    } else {
        Err(Error::Schema)
    }
}
fn int(v: &V) -> Result<i128, Error> {
    if let V::Integer(n) = v {
        Ok(n.get())
    } else {
        Err(Error::Schema)
    }
}
fn count(v: &V) -> Result<i128, Error> {
    let n = int(v)?;
    if n < 0 { Err(Error::Schema) } else { Ok(n) }
}
fn kind(v: &V) -> &'static str {
    match v {
        V::Null => "null",
        V::Bool(_) => "boolean",
        V::Integer(_) => "integer",
        V::String(_) => "string",
        V::Array(_) => "array",
        V::Object(_) => "object",
    }
}
fn named_type(s: &str) -> bool {
    matches!(
        s,
        "null" | "boolean" | "integer" | "string" | "array" | "object"
    )
}
fn annotation(k: &str) -> bool {
    matches!(
        k,
        "x-maxUtf8Bytes"
            | "x-opensip-admission-precedence"
            | "x-opensip-config-node-kind-law"
            | "x-opensip-deficiency-cause-registry"
            | "x-opensip-digest"
            | "x-opensip-digest-domains"
            | "x-opensip-digest-law"
            | "x-opensip-evaluator-deficiency-registry"
            | "x-opensip-evaluator-profile"
            | "x-opensip-evaluator-registry"
            | "x-opensip-evaluator3-repair-target-law"
            | "x-opensip-evidence-relation-registry"
            | "x-opensip-fixture-representation"
            | "x-opensip-grammar-capability-registry"
            | "x-opensip-imported-requirement-law"
            | "x-opensip-mirror"
            | "x-opensip-mutation-operation-map"
            | "x-opensip-negotiation"
            | "x-opensip-order-vocabulary"
            | "x-opensip-output-profile"
            | "x-opensip-ownership-attribute"
            | "x-opensip-parameter-registry-extension"
            | "x-opensip-path-law"
            | "x-opensip-payload-registry"
            | "x-opensip-profile-major-law"
            | "x-opensip-public-route-registry"
            | "x-opensip-startup-law"
            | "x-opensip-uniqueness"
            | "x-opensip-vocabulary"
            | "x-opensip-wire"
            | "x-opensip-wire-law"
            | "x-opensip-kind-derivation"
            | "x-opensip-file-membership-extent-law"
            | "x-opensip-new-internal-faults"
            | "x-opensip-derived-carrier-law"
            | "x-opensip-external-joins"
            | "x-opensip-applicability-precedence"
            | "x-opensip-identity"
            | "x-opensip-law"
            | "x-opensip-relation-registry"
            | "x-opensip-subject-language-table"
            | "x-opensip-join-law"
    )
}

/// Owned immutable inert program, not a selected schema registry authority.
/// Every entry and its reference closure is checked before evaluating instances.
/// Pure references can only resolve supplied documents: no resolver or I/O port.
pub struct Program {
    documents: BTreeMap<String, V>,
    entries: BTreeSet<String>,
}
impl Program {
    pub(crate) fn matches_node(
        &self,
        owner: &str,
        schema: &V,
        value: &V,
        budget: usize,
    ) -> Result<bool, Error> {
        if !self.documents.contains_key(owner) {
            return Err(Error::Reference);
        }
        let mut meter = Meter { remaining: budget };
        meter.value(value, 0)?;
        self.evaluate(schema, value, owner, &mut meter, 0)
    }

    pub(crate) fn document(&self, id: &str) -> Option<&V> {
        self.documents.get(id)
    }

    pub fn compile(documents: Vec<V>, entries: &[&str], budget: usize) -> Result<Self, Error> {
        let mut meter = Meter { remaining: budget };
        let mut docs = BTreeMap::new();
        for d in documents {
            meter.value(&d, 0)?;
            let o = obj(&d)?;
            let id = text(o.get("$id").ok_or(Error::Schema)?)?;
            if id.is_empty()
                || id.contains('#')
                || text(o.get("$schema").ok_or(Error::Schema)?)? != DIALECT
                || docs.insert(id.to_string(), d).is_some()
            {
                return Err(Error::Schema);
            }
        }
        let mut selected = BTreeSet::new();
        for entry in entries {
            meter.spend(1 + entry.len())?;
            selected.insert(entry.to_string());
        }
        let p = Self {
            documents: docs,
            entries: selected,
        };
        let mut seen = BTreeSet::new();
        for entry in entries {
            p.check_ref(entry, "", &mut seen, &mut meter, 0)?;
        }
        Ok(p)
    }
    fn resolve(&self, reference: &str, owner: &str) -> Result<(&V, &str), Error> {
        let (id, fragment) = reference.split_once('#').unwrap_or((reference, ""));
        let id = if id.is_empty() { owner } else { id };
        let (id, v) = self.documents.get_key_value(id).ok_or(Error::Reference)?;
        let id = id.as_str();
        let mut v = v;
        if !fragment.is_empty() {
            if !fragment.starts_with('/') || fragment.contains('%') {
                return Err(Error::Reference);
            }
            for part in fragment[1..].split('/') {
                let mut chars = part.chars();
                let mut key = String::new();
                while let Some(c) = chars.next() {
                    key.push(if c == '~' {
                        match chars.next() {
                            Some('0') => '~',
                            Some('1') => '/',
                            _ => return Err(Error::Reference),
                        }
                    } else {
                        c
                    });
                }
                v = obj(v)?.get(&key).ok_or(Error::Reference)?;
            }
        }
        if !matches!(v, V::Bool(_) | V::Object(_)) {
            return Err(Error::Schema);
        }
        Ok((v, id))
    }
    fn check_ref(
        &self,
        r: &str,
        owner: &str,
        seen: &mut BTreeSet<(String, String)>,
        meter: &mut Meter,
        depth: usize,
    ) -> Result<(), Error> {
        meter.spend(1 + r.len())?;
        let (s, id) = self.resolve(r, owner)?;
        let fragment = r.split_once('#').map_or("", |(_, f)| f);
        if seen.insert((id.to_string(), fragment.to_string())) {
            self.check_schema(s, id, seen, meter, depth + 1)?
        }
        Ok(())
    }
    fn check_schema(
        &self,
        s: &V,
        owner: &str,
        seen: &mut BTreeSet<(String, String)>,
        meter: &mut Meter,
        depth: usize,
    ) -> Result<(), Error> {
        if depth > DEPTH {
            return Err(Error::Limit);
        }
        meter.spend(1)?;
        if matches!(s, V::Bool(_)) {
            return Ok(());
        }
        let o = obj(s)?;
        for (k, v) in o {
            meter.spend(1 + k.len())?;
            match k.as_str() {
                "$id" => {
                    if text(v)? != owner {
                        return Err(Error::Schema);
                    }
                }
                "$schema" => {
                    if text(v)? != DIALECT {
                        return Err(Error::Schema);
                    }
                }
                "$ref" => self.check_ref(text(v)?, owner, seen, meter, depth)?,
                "title" | "description" => {
                    text(v)?;
                }
                "$defs" | "definitions" => {
                    obj(v)?;
                }
                "default" | "const" => {}
                "type" => {
                    if let V::String(s) = v {
                        if !named_type(s) {
                            return Err(Error::Schema);
                        }
                    } else {
                        let a = array(v)?;
                        if a.is_empty() {
                            return Err(Error::Schema);
                        }
                        let mut unique = BTreeSet::new();
                        for t in a {
                            let t = text(t)?;
                            if !named_type(t) || !unique.insert(t) {
                                return Err(Error::Schema);
                            }
                        }
                    }
                }
                "enum" => {
                    let a = array(v)?;
                    if a.is_empty() {
                        return Err(Error::Schema);
                    }
                    let mut keys = BTreeSet::new();
                    for v in a {
                        meter.value(v, 0)?;
                        if !keys.insert(canonical_bytes(v).map_err(|_| Error::Schema)?) {
                            return Err(Error::Schema);
                        }
                    }
                }
                "required" => {
                    let mut keys = BTreeSet::new();
                    for x in array(v)? {
                        if !keys.insert(text(x)?) {
                            return Err(Error::Schema);
                        }
                    }
                }
                "minimum" | "maximum" => {
                    int(v)?;
                }
                "minProperties" | "maxProperties" | "minItems" | "maxItems" | "minLength"
                | "maxLength" => {
                    count(v)?;
                }
                "uniqueItems" => {
                    if !matches!(v, V::Bool(_)) {
                        return Err(Error::Schema);
                    }
                }
                "pattern" => {
                    crate::schema_patterns::matches(text(v)?, "").map_err(|_| Error::Pattern)?;
                }
                "x-opensip-order" => {
                    ArrayOrder::parse(v).map_err(|_| Error::Schema)?;
                }
                "properties" | "patternProperties" => {
                    for (key, rule) in obj(v)? {
                        if k == "patternProperties" {
                            crate::schema_patterns::matches(key, "").map_err(|_| Error::Pattern)?;
                        }
                        self.check_schema(rule, owner, seen, meter, depth + 1)?;
                    }
                }
                "additionalProperties"
                | "propertyNames"
                | "items"
                | "not"
                | "if"
                | "then"
                | "else"
                | "contains" => self.check_schema(v, owner, seen, meter, depth + 1)?,
                "allOf" | "anyOf" | "oneOf" | "prefixItems" => {
                    let a = array(v)?;
                    if a.is_empty() {
                        return Err(Error::Schema);
                    }
                    for rule in a {
                        self.check_schema(rule, owner, seen, meter, depth + 1)?;
                    }
                }
                k if annotation(k) => {}
                _ => return Err(Error::Schema),
            }
        }
        Ok(())
    }
    /// Limit exhaustion, invalid input and schema faults propagate separately from
    /// a completed mismatch. They can never make `not`, `if`, or `anyOf` succeed.
    #[cfg(test)]
    pub fn matches_json(&self, entry: &str, raw: &[u8], budget: usize) -> Result<bool, Error> {
        Ok(self.admit_json(entry, raw, budget)?.is_some())
    }
    pub(crate) fn has_entry(&self, entry: &str) -> bool {
        self.entries.contains(entry)
    }
    pub(crate) fn admit_json(
        &self,
        entry: &str,
        raw: &[u8],
        budget: usize,
    ) -> Result<Option<V>, Error> {
        if !self.entries.contains(entry) {
            return Err(Error::UnselectedEntry);
        }
        let value = parse_json(raw).map_err(|_| Error::Json)?;
        let mut m = Meter { remaining: budget };
        m.value(&value, 0)?;
        let (schema, owner) = self.resolve(entry, "")?;
        if self.evaluate(schema, &value, owner, &mut m, 0)? {
            Ok(Some(value))
        } else {
            Ok(None)
        }
    }
    fn evaluate(
        &self,
        s: &V,
        v: &V,
        owner: &str,
        m: &mut Meter,
        depth: usize,
    ) -> Result<bool, Error> {
        if depth > DEPTH {
            return Err(Error::Limit);
        }
        m.spend(1)?;
        if let V::Bool(b) = s {
            return Ok(*b);
        }
        let o = obj(s)?;
        if let Some(r) = o.get("$ref") {
            let (target, id) = self.resolve(text(r)?, owner)?;
            if !self.evaluate(target, v, id, m, depth + 1)? {
                return Ok(false);
            }
        }
        if let Some(c) = o.get("const") {
            m.value(v, 0)?;
            m.value(c, 0)?;
            if v != c {
                return Ok(false);
            }
        }
        if let Some(e) = o.get("enum") {
            let mut found = false;
            for c in array(e)? {
                m.value(v, 0)?;
                m.value(c, 0)?;
                if v == c {
                    found = true;
                    break;
                }
            }
            if !found {
                return Ok(false);
            }
        }
        if let Some(t) = o.get("type") {
            let k = kind(v);
            let yes = if let V::String(t) = t {
                t == k
            } else {
                array(t)?.iter().any(|t| matches!(t,V::String(s) if s==k))
            };
            if !yes {
                return Ok(false);
            }
        }
        for name in ["allOf", "anyOf", "oneOf"] {
            if let Some(a) = o.get(name) {
                let rules = array(a)?;
                let mut yes = 0;
                for rule in rules {
                    if self.evaluate(rule, v, owner, m, depth + 1)? {
                        yes += 1;
                        if name == "anyOf" {
                            break;
                        }
                    } else if name == "allOf" {
                        return Ok(false);
                    }
                }
                if (name == "anyOf" && yes == 0) || (name == "oneOf" && yes != 1) {
                    return Ok(false);
                }
            }
        }
        if let Some(rule) = o.get("not")
            && self.evaluate(rule, v, owner, m, depth + 1)?
        {
            return Ok(false);
        }
        if let Some(rule) = o.get("if") {
            let branch = if self.evaluate(rule, v, owner, m, depth + 1)? {
                "then"
            } else {
                "else"
            };
            if let Some(rule) = o.get(branch)
                && !self.evaluate(rule, v, owner, m, depth + 1)?
            {
                return Ok(false);
            }
        }
        match v {
            V::Integer(n) if !bounds(n.get(), o, "minimum", "maximum")? => {
                return Ok(false);
            }
            V::String(text) => {
                m.spend(text.len())?;
                if !bounds(text.chars().count() as i128, o, "minLength", "maxLength")? {
                    return Ok(false);
                }
                if let Some(p) = o.get("pattern")
                    && !crate::schema_patterns::matches(crate_text(p)?, text)
                        .map_err(|_| Error::Pattern)?
                {
                    return Ok(false);
                }
            }
            V::Array(items) => {
                if !bounds(items.len() as i128, o, "minItems", "maxItems")? {
                    return Ok(false);
                }
                let prefix = o.get("prefixItems").map(array).transpose()?.unwrap_or(&[]);
                for (i, item) in items.iter().enumerate() {
                    m.spend(1)?;
                    let rule = prefix.get(i).or_else(|| o.get("items"));
                    if let Some(rule) = rule
                        && !self.evaluate(rule, item, owner, m, depth + 1)?
                    {
                        return Ok(false);
                    }
                }
                if let Some(rule) = o.get("contains") {
                    let mut yes = false;
                    for item in items {
                        if self.evaluate(rule, item, owner, m, depth + 1)? {
                            yes = true;
                            break;
                        }
                    }
                    if !yes {
                        return Ok(false);
                    }
                }
                if matches!(o.get("uniqueItems"), Some(V::Bool(true))) {
                    let mut seen = BTreeSet::new();
                    for item in items {
                        m.value(item, 0)?;
                        let raw = canonical_bytes(item).map_err(|_| Error::Json)?;
                        m.spend(raw.len())?;
                        if !seen.insert(raw) {
                            return Ok(false);
                        }
                    }
                }
                if let Some(order) = o.get("x-opensip-order") {
                    m.value(v, 0)?;
                    m.value(order, 0)?;
                    let order = ArrayOrder::parse(order).map_err(|_| Error::Schema)?;
                    if order.verify(items).is_err() {
                        return Ok(false);
                    }
                }
            }
            V::Object(items) => {
                if !bounds(items.len() as i128, o, "minProperties", "maxProperties")? {
                    return Ok(false);
                }
                if let Some(r) = o.get("required") {
                    for key in array(r)? {
                        m.spend(1 + text(key)?.len())?;
                        if !items.contains_key(text(key)?) {
                            return Ok(false);
                        }
                    }
                }
                let props = o.get("properties").map(obj).transpose()?;
                let patterns = o.get("patternProperties").map(obj).transpose()?;
                for (key, item) in items {
                    m.spend(1 + key.len())?;
                    let mut matched = false;
                    if let Some(rule) = o.get("propertyNames")
                        && !self.evaluate(rule, &V::String(key.clone()), owner, m, depth + 1)?
                    {
                        return Ok(false);
                    }
                    if let Some(rule) = props.and_then(|p| p.get(key)) {
                        matched = true;
                        if !self.evaluate(rule, item, owner, m, depth + 1)? {
                            return Ok(false);
                        }
                    }
                    if let Some(patterns) = patterns {
                        for (pattern, rule) in patterns {
                            m.spend(1 + key.len())?;
                            if crate::schema_patterns::matches(pattern, key)
                                .map_err(|_| Error::Pattern)?
                            {
                                matched = true;
                                if !self.evaluate(rule, item, owner, m, depth + 1)? {
                                    return Ok(false);
                                }
                            }
                        }
                    }
                    if !matched
                        && let Some(rule) = o.get("additionalProperties")
                        && !self.evaluate(rule, item, owner, m, depth + 1)?
                    {
                        return Ok(false);
                    }
                }
            }
            _ => {}
        }
        Ok(true)
    }
}
fn crate_text(v: &V) -> Result<&str, Error> {
    text(v)
}
fn bounds(n: i128, o: &BTreeMap<String, V>, low: &str, high: &str) -> Result<bool, Error> {
    Ok(o.get(low).map(int).transpose()?.is_none_or(|v| n >= v)
        && o.get(high).map(int).transpose()?.is_none_or(|v| n <= v))
}
