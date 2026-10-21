//! M3-D r5 item 10 (unit D2b-3a; LD-D2B3-1): the carrier-typed closed check of
//! TS2's inherited frames, and the schema check of its extern payloads.
//!
//! The inherited payloads (SnapshotAccepted, FactBatch V1 and V3, Complete,
//! Cancelled, and their nested records) have no product-registered schema:
//! their closed schemas are DLV's `payloadSchemas`, and the carriers'
//! `records` are those schemas as data, each naming its DLV selector
//! (`schemas/wire/native-carriers-v1.json`). So the carrier-typed decode is
//! the closed check (LD-D2B3-1): this module interprets the records' type
//! grammar over the decoded tree. Loading refuses any grammar form, array
//! order, pattern or lexical rule it does not implement, so a carrier is
//! never interpreted loosely. An `extern` member, and every extern payload,
//! is admitted by the product schema it names, through the embedded registry
//! (OWNER-PATTERN-EVALUATION's consumer here: every pattern D2b's schema checks
//! reach is evaluated by the identity crate's selected pattern profile). A
//! `lexical` scalar is judged over its complete string by its bound rule
//! (PATH-SITE-SEGMENT-LAW; TS2-LOGICAL-PATH-ADMISSION for `Ts2ProjectPath`, so
//! for every worker-sent anchor path).
use super::super::cbor::{self, Value};
use opensip_identity::{JsonInteger, JsonValue as J, canonical_bytes, is_nfc, parse_json};
use std::collections::BTreeMap;

pub(crate) const CARRIERS: &[u8] =
    include_bytes!("../../../../../schemas/wire/native-carriers-v1.json");
/// The schema evaluator's work bound for one admitted document, B1's
/// configuration admission's (`crates/host/src/configuration.rs`
/// `SCHEMA_BUDGET`), as C1a3's sealing reuses it.
pub(crate) const SCHEMA_BUDGET: usize = 64 * 1024 * 1024;

/// The array orders the TS2 records name. `request-order` is a join with the
/// request (contextual admission), so it has no intrinsic check here.
const ORDERS: [&str; 7] = [
    "utf8-strict",
    "path-utf8-strict",
    "cbor-bytes-strict",
    "candidateOrdinal-contiguous",
    "candidateOrdinal-increasing",
    "sequence",
    "request-order",
];

/// The loaded carrier records and scalars of one protocol's namespace.
pub(crate) struct Carriers {
    records: BTreeMap<String, J>,
    scalars: BTreeMap<String, J>,
    lexical: BTreeMap<String, J>,
}

fn obj(v: &J) -> Option<&BTreeMap<String, J>> {
    match v {
        J::Object(o) => Some(o),
        _ => None,
    }
}
fn txt(v: &J) -> Option<&str> {
    match v {
        J::String(s) => Some(s),
        _ => None,
    }
}
fn num(v: Option<&J>) -> Option<u64> {
    v.and_then(txt).and_then(|s| s.parse().ok())
}

/// The one pattern form the TS2 scalars use: a literal prefix, then exactly
/// `n` lowercase hex digits, then the absolute end.
fn hex_pattern(pattern: &str) -> Option<(&str, usize)> {
    let rest = pattern.strip_prefix('^')?.strip_suffix("(?![\\s\\S])")?;
    let (prefix, tail) = rest.split_once("[0-9a-f]{")?;
    let n = tail.strip_suffix('}')?.parse().ok()?;
    prefix
        .chars()
        .all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == ':' || c == '_')
        .then_some((prefix, n))
}

impl Carriers {
    /// The records and scalars named `prefix*` (`Ts2`), with every form,
    /// order, pattern and lexical rule they use checked as implemented.
    pub(crate) fn load(prefix: &str) -> Result<Self, String> {
        let doc = parse_json(CARRIERS).map_err(|e| format!("carriers: {e}"))?;
        let doc = obj(&doc).ok_or("carriers")?;
        let pick = |key: &str| -> Result<BTreeMap<String, J>, String> {
            let all = obj(doc.get(key).ok_or(key)?).ok_or(key)?;
            Ok(all
                .iter()
                .filter(|(k, _)| k.starts_with(prefix))
                .map(|(k, v)| (k.clone(), v.clone()))
                .collect())
        };
        let lexical = doc
            .get("privateRepresentation")
            .and_then(obj)
            .and_then(|p| p.get("lexicalRules"))
            .and_then(obj)
            .ok_or("lexicalRules")?
            .clone();
        let carriers = Self {
            records: pick("records")?,
            scalars: pick("scalars")?,
            lexical,
        };
        for (name, record) in &carriers.records {
            carriers.validate_record(name, record)?;
        }
        for (name, scalar) in &carriers.scalars {
            carriers.validate_type(name, scalar.get_type().ok_or(name.as_str())?)?;
        }
        Ok(carriers)
    }

    fn validate_record(&self, name: &str, record: &J) -> Result<(), String> {
        let r = obj(record).ok_or(name)?;
        match r.get("kind").and_then(txt) {
            Some("record") => {
                let J::Array(members) = r.get("members").ok_or(name)? else {
                    return Err(name.to_owned());
                };
                for m in members {
                    let m = obj(m).ok_or(name)?;
                    match m.get("presence").and_then(txt) {
                        Some("required") => {}
                        other => return Err(format!("{name}: presence {other:?}")),
                    }
                    self.validate_type(name, m.get("type").ok_or(name)?)?;
                }
            }
            Some("variant-record") => {
                for variant in obj(r.get("variants").ok_or(name)?).ok_or(name)?.values() {
                    for t in obj(variant).ok_or(name)?.values() {
                        self.validate_type(name, t)?;
                    }
                }
            }
            other => return Err(format!("{name}: kind {other:?}")),
        }
        Ok(())
    }

    pub(crate) fn validate_type(&self, at: &str, t: &J) -> Result<(), String> {
        let t = obj(t).ok_or(at)?;
        let allowed: &[&str] = match t.get("t").and_then(txt) {
            Some("uint64") => &["t", "const", "max"],
            Some("text") => &[
                "t",
                "const",
                "enum",
                "lexical",
                "maxScalars",
                "minScalars",
                "nfc",
                "pattern",
            ],
            Some("bytes") => &["t", "maxBytes", "minBytes"],
            Some("null") => &["t"],
            Some("nullable") => &["t", "of"],
            Some("array") => &["t", "items", "maxItems", "minItems", "order"],
            Some("ref") => &["t", "ref"],
            Some("extern") => &["t", "generatedType", "schemaRef"],
            Some("frame-payload") => &["t", "protocol"],
            other => return Err(format!("{at}: form {other:?}")),
        };
        if let Some(k) = t.keys().find(|k| !allowed.contains(&k.as_str())) {
            return Err(format!("{at}: unimplemented keyword {k}"));
        }
        if let Some(p) = t.get("pattern").and_then(txt)
            && hex_pattern(p).is_none()
        {
            return Err(format!("{at}: unimplemented pattern {p}"));
        }
        if let Some(l) = t.get("lexical").and_then(txt) {
            let rule = self
                .lexical
                .get(l)
                .and_then(obj)
                .ok_or(format!("{at}: lexical {l}"))?;
            if rule.get("kind").and_then(txt) != Some("segments")
                || rule.keys().any(|k| {
                    ![
                        "kind",
                        "separator",
                        "forbiddenScalars",
                        "forbiddenSegments",
                        "maxSegmentScalars",
                        "owner",
                        "text",
                    ]
                    .contains(&k.as_str())
                })
            {
                return Err(format!("{at}: unimplemented lexical rule {l}"));
            }
        }
        if let Some(o) = t.get("order").and_then(txt)
            && !ORDERS.contains(&o)
        {
            return Err(format!("{at}: unimplemented order {o}"));
        }
        for k in ["of", "items"] {
            if let Some(inner) = t.get(k) {
                self.validate_type(at, inner)?;
            }
        }
        if let Some(r) = t.get("ref").and_then(txt)
            && !self.records.contains_key(r)
            && !self.scalars.contains_key(r)
        {
            return Err(format!("{at}: unknown ref {r}"));
        }
        Ok(())
    }

    /// The named record's members, in declared order (a `record`).
    pub(crate) fn members(&self, record: &str) -> Vec<(String, J)> {
        let Some(J::Array(members)) = self
            .records
            .get(record)
            .and_then(obj)
            .and_then(|r| r.get("members"))
        else {
            return Vec::new();
        };
        members
            .iter()
            .filter_map(obj)
            .filter_map(|m| Some((txt(m.get("name")?)?.to_owned(), m.get("type")?.clone())))
            .collect()
    }

    /// Check `v` against record `name`.
    pub(crate) fn check_record(&self, name: &str, v: &Value) -> Result<(), String> {
        self.check(
            &J::Object(BTreeMap::from_iter([
                ("t".to_owned(), J::String("ref".to_owned())),
                ("ref".to_owned(), J::String(name.to_owned())),
            ])),
            v,
            name,
        )
    }

    /// Check `v` against type expression `t`; `at` names the site.
    pub(crate) fn check(&self, t: &J, v: &Value, at: &str) -> Result<(), String> {
        let t = obj(t).ok_or(at)?;
        let fail = |what: &str| Err(format!("{at}: {what}"));
        match t.get("t").and_then(txt) {
            Some("uint64") => {
                let Value::Unsigned(n) = v else {
                    return fail("not a uint64");
                };
                if let Some(c) = num(t.get("const"))
                    && *n != c
                {
                    return fail("const");
                }
                if let Some(max) = num(t.get("max"))
                    && *n > max
                {
                    return fail("above max");
                }
            }
            Some("text") => {
                let Value::Text(s) = v else {
                    return fail("not text");
                };
                if t.get("nfc") == Some(&J::Bool(true)) && !is_nfc(s) {
                    return fail("not NFC");
                }
                if let Some(c) = t.get("const").and_then(txt)
                    && s != c
                {
                    return fail("const");
                }
                if let Some(J::Array(e)) = t.get("enum")
                    && !e.iter().any(|x| txt(x) == Some(s))
                {
                    return fail("not in enum");
                }
                let scalars = s.chars().count() as u64;
                if num(t.get("minScalars")).is_some_and(|m| scalars < m)
                    || num(t.get("maxScalars")).is_some_and(|m| scalars > m)
                {
                    return fail("scalar length");
                }
                if let Some((prefix, n)) = t.get("pattern").and_then(txt).and_then(hex_pattern) {
                    let ok = s.strip_prefix(prefix).is_some_and(|h| {
                        h.len() == n
                            && h.bytes()
                                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
                    });
                    if !ok {
                        return fail("pattern");
                    }
                }
                if let Some(l) = t.get("lexical").and_then(txt) {
                    self.lexical_ok(l, s).map_err(|e| format!("{at}: {e}"))?;
                }
            }
            Some("bytes") => {
                let Value::Bytes(b) = v else {
                    return fail("not a byte string");
                };
                if num(t.get("minBytes")).is_some_and(|m| (b.len() as u64) < m)
                    || num(t.get("maxBytes")).is_some_and(|m| b.len() as u64 > m)
                {
                    return fail("byte length");
                }
            }
            Some("null") => {
                if *v != Value::Null {
                    return fail("not null");
                }
            }
            Some("nullable") => {
                if *v != Value::Null {
                    self.check(t.get("of").ok_or(at)?, v, at)?;
                }
            }
            Some("array") => {
                let Value::Array(items) = v else {
                    return fail("not an array");
                };
                let n = items.len() as u64;
                if num(t.get("minItems")).is_some_and(|m| n < m)
                    || num(t.get("maxItems")).is_some_and(|m| n > m)
                {
                    return fail("item count");
                }
                let item = t.get("items").ok_or(at)?;
                for (i, x) in items.iter().enumerate() {
                    self.check(item, x, &format!("{at}[{i}]"))?;
                }
                if let Some(order) = t.get("order").and_then(txt) {
                    order_ok(order, items).map_err(|e| format!("{at}: {e}"))?;
                }
            }
            Some("ref") => {
                let name = t.get("ref").and_then(txt).ok_or(at)?;
                if let Some(scalar) = self.scalars.get(name) {
                    return self.check(scalar.get_type().ok_or(at)?, v, &format!("{at} ({name})"));
                }
                let record = self.records.get(name).and_then(obj).ok_or(at)?;
                let Value::Map(fields) = v else {
                    return fail("not a map");
                };
                match record.get("kind").and_then(txt) {
                    Some("record") => {
                        let members = self.members(name);
                        if fields.len() != members.len() {
                            return fail("member set");
                        }
                        for (mname, mt) in &members {
                            let x = field(fields, mname).ok_or(format!("{at}: missing {mname}"))?;
                            self.check(mt, x, &format!("{at}.{mname}"))?;
                        }
                    }
                    Some("variant-record") => {
                        let disc = record.get("discriminator").and_then(txt).ok_or(at)?;
                        let Some(J::Array(order)) = record.get("memberOrder") else {
                            return fail("memberOrder");
                        };
                        let Some(Value::Text(kind)) = field(fields, disc) else {
                            return fail("discriminator");
                        };
                        let variant = record
                            .get("variants")
                            .and_then(obj)
                            .and_then(|vs| vs.get(kind))
                            .and_then(obj)
                            .ok_or(format!("{at}: variant {kind}"))?;
                        if fields.len() != order.len() {
                            return fail("member set");
                        }
                        for m in order.iter().filter_map(txt) {
                            let x = field(fields, m).ok_or(format!("{at}: missing {m}"))?;
                            if m != disc {
                                self.check(variant.get(m).ok_or(at)?, x, &format!("{at}.{m}"))?;
                            }
                        }
                    }
                    _ => return fail("record kind"),
                }
            }
            Some("extern") => {
                let r = t.get("schemaRef").and_then(txt).ok_or(at)?;
                admit_extern(r, v).map_err(|e| format!("{at}: {e}"))?;
            }
            _ => return fail("form"),
        }
        Ok(())
    }

    fn lexical_ok(&self, rule: &str, s: &str) -> Result<(), String> {
        let r = self.lexical.get(rule).and_then(obj).ok_or("lexical rule")?;
        let sep = r.get("separator").and_then(txt).ok_or("separator")?;
        let strings = |k: &str| -> Vec<&str> {
            match r.get(k) {
                Some(J::Array(a)) => a.iter().filter_map(txt).collect(),
                _ => Vec::new(),
            }
        };
        let forbidden = strings("forbiddenScalars");
        if s.chars()
            .any(|c| forbidden.iter().any(|f| f.chars().eq(std::iter::once(c))))
        {
            return Err(format!("{rule}: forbidden scalar"));
        }
        let max = num(r.get("maxSegmentScalars"));
        for segment in s.split(sep) {
            if strings("forbiddenSegments").contains(&segment) {
                return Err(format!("{rule}: forbidden segment"));
            }
            if max.is_some_and(|m| segment.chars().count() as u64 > m) {
                return Err(format!("{rule}: segment length"));
            }
        }
        Ok(())
    }
}

trait TypeOf {
    fn get_type(&self) -> Option<&J>;
}
impl TypeOf for J {
    fn get_type(&self) -> Option<&J> {
        obj(self)?.get("type")
    }
}

/// A map member by name.
pub(crate) fn field<'v>(fields: &'v [(String, Value)], name: &str) -> Option<&'v Value> {
    fields.iter().find(|(k, _)| k == name).map(|(_, v)| v)
}

fn order_ok(order: &str, items: &[Value]) -> Result<(), String> {
    let ordinal = |v: &Value| match v {
        Value::Map(f) => match field(f, "candidateOrdinal") {
            Some(Value::Unsigned(n)) => Some(*n),
            _ => None,
        },
        _ => None,
    };
    let strictly = |keys: Vec<Option<Vec<u8>>>| -> Result<(), String> {
        let keys: Option<Vec<Vec<u8>>> = keys.into_iter().collect();
        let keys = keys.ok_or(format!("{order}: key"))?;
        if keys.windows(2).all(|w| w[0] < w[1]) {
            Ok(())
        } else {
            Err(format!("{order}: not strictly ascending"))
        }
    };
    match order {
        "utf8-strict" => strictly(
            items
                .iter()
                .map(|v| match v {
                    Value::Text(s) => Some(s.as_bytes().to_vec()),
                    _ => None,
                })
                .collect(),
        ),
        "path-utf8-strict" => strictly(
            items
                .iter()
                .map(|v| match v {
                    Value::Map(f) => match field(f, "path") {
                        Some(Value::Text(s)) => Some(s.as_bytes().to_vec()),
                        _ => None,
                    },
                    _ => None,
                })
                .collect(),
        ),
        "cbor-bytes-strict" => strictly(items.iter().map(|v| Some(cbor::encode(v))).collect()),
        "candidateOrdinal-contiguous" => {
            let ords: Option<Vec<u64>> = items.iter().map(ordinal).collect();
            let ords = ords.ok_or("candidateOrdinal")?;
            match ords.first() {
                Some(first)
                    if ords
                        .iter()
                        .enumerate()
                        .all(|(i, o)| first.checked_add(i as u64) == Some(*o)) =>
                {
                    Ok(())
                }
                None => Ok(()),
                _ => Err("candidateOrdinal-contiguous: not contiguous".to_owned()),
            }
        }
        "candidateOrdinal-increasing" => {
            let ords: Option<Vec<u64>> = items.iter().map(ordinal).collect();
            let ords = ords.ok_or("candidateOrdinal")?;
            if ords.windows(2).all(|w| w[0] < w[1]) {
                Ok(())
            } else {
                Err("candidateOrdinal-increasing".to_owned())
            }
        }
        _ => Ok(()),
    }
}

/// A decoded value as its JSON vector (the carriers' `privateRepresentation`:
/// integers stay exact; a byte string has no JSON form in an extern payload).
pub(crate) fn to_json(v: &Value) -> Result<J, String> {
    Ok(match v {
        Value::Null => J::Null,
        Value::Bool(b) => J::Bool(*b),
        Value::Unsigned(n) => J::Integer(JsonInteger::new(*n as i128).map_err(|_| "integer")?),
        Value::Negative(n) => J::Integer(JsonInteger::new(*n as i128).map_err(|_| "integer")?),
        Value::Text(s) => J::String(s.clone()),
        Value::Bytes(_) => return Err("a byte string in an extern payload".to_owned()),
        Value::Array(a) => J::Array(a.iter().map(to_json).collect::<Result<_, _>>()?),
        Value::Map(m) => J::Object(
            m.iter()
                .map(|(k, x)| Ok((k.clone(), to_json(x)?)))
                .collect::<Result<_, String>>()?,
        ),
    })
}

/// Admit `v` against the product schema `schema_ref` (`id#` or
/// `id#/$defs/Name`) through the embedded registry.
pub(crate) fn admit_extern(schema_ref: &str, v: &Value) -> Result<(), String> {
    let (id, pointer) = schema_ref.split_once('#').ok_or("schemaRef")?;
    let registry = crate::schema_sources::registry().ok_or("the embedded registry")?;
    let handle = registry
        .schema(id, pointer)
        .map_err(|e| format!("{schema_ref}: {e:?}"))?;
    let raw = canonical_bytes(&to_json(v)?).map_err(|e| format!("{schema_ref}: {e}"))?;
    handle
        .admit_json(&raw, SCHEMA_BUDGET)
        .map(|_| ())
        .map_err(|e| format!("{schema_ref}: {e:?}"))
}
