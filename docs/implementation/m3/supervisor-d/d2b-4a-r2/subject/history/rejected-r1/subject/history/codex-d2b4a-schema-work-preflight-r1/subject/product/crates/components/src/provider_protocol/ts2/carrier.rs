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
const ORDERS: [&str; 10] = [
    "utf8-strict",
    "path-utf8-strict",
    "cbor-bytes-strict",
    "candidateOrdinal-contiguous",
    "candidateOrdinal-increasing",
    "sequence",
    "request-order",
    "cve1-bytes-strict",
    "outputOrdinal-contiguous",
    "nested-loop-relation-rung-target",
];

/// The loaded carrier records and scalars of one protocol's namespace.
pub(crate) struct Carriers {
    rust3: bool,
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

// Additional complete-string forms in the Rust3 carrier grammar. This is
// not a general regular-expression engine or a product-schema policy.
const IDENTITY_PATTERN: &str = r"^[^\u0000-\u001f\u0080-\u009f]+(?![\s\S])";
const IDENTIFIER_PATTERN: &str = r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*(?![\s\S])";
const PREPARED_PATTERN: &str =
    r"^\.opensip/prepared/v3/(0|[1-9][0-9]*)-[0-9a-f]{64}\.blob(?![\s\S])";
const SUBJECT_PATTERN: &str = r"^rust-file:sha256:[0-9a-f]{64}(?![\s\S])";

fn known_pattern(pattern: &str) -> bool {
    hex_pattern(pattern).is_some()
        || [
            IDENTITY_PATTERN,
            IDENTIFIER_PATTERN,
            PREPARED_PATTERN,
            SUBJECT_PATTERN,
        ]
        .contains(&pattern)
}

fn pattern_ok(pattern: &str, value: &str) -> bool {
    let hex = |text: &str| {
        text.len() == 64
            && text
                .bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    };
    if let Some((prefix, count)) = hex_pattern(pattern) {
        return value.strip_prefix(prefix).is_some_and(|rest| {
            rest.len() == count
                && rest
                    .bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
        });
    }
    match pattern {
        IDENTITY_PATTERN => {
            !value.is_empty()
                && !value
                    .chars()
                    .any(|c| c <= '\u{1f}' || ('\u{80}'..='\u{9f}').contains(&c))
        }
        IDENTIFIER_PATTERN => {
            value.as_bytes().first().is_some_and(u8::is_ascii_lowercase)
                && value.split(['.', '_', ':', '-']).all(|part| {
                    !part.is_empty()
                        && part
                            .bytes()
                            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit())
                })
        }
        PREPARED_PATTERN => value
            .strip_prefix(".opensip/prepared/v3/")
            .and_then(|rest| rest.strip_suffix(".blob"))
            .and_then(|rest| rest.split_once('-'))
            .is_some_and(|(ordinal, digest)| {
                (ordinal == "0"
                    || (ordinal
                        .as_bytes()
                        .first()
                        .is_some_and(|b| (b'1'..=b'9').contains(b))
                        && ordinal.bytes().all(|b| b.is_ascii_digit())))
                    && hex(digest)
            }),
        SUBJECT_PATTERN => value.strip_prefix("rust-file:sha256:").is_some_and(hex),
        _ => false,
    }
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
            rust3: prefix == "Rust3",
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
            Some("alias") if self.rust3 => {
                self.validate_type(name, r.get("target").ok_or(name)?)?
            }
            Some("record") => {
                let J::Array(members) = r.get("members").ok_or(name)? else {
                    return Err(name.to_owned());
                };
                for m in members {
                    let m = obj(m).ok_or(name)?;
                    match m.get("presence").and_then(txt) {
                        Some("required") => {}
                        Some("optional") if self.rust3 => {}
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
            Some("uint64") if self.rust3 => &["t", "const", "min", "max"],
            Some("uint64") => &["t", "const", "max"],
            Some("text") if self.rust3 => &[
                "t",
                "const",
                "enum",
                "lexical",
                "maxScalars",
                "minScalars",
                "nfc",
                "pattern",
                "maxUtf8Bytes",
                "forbidC0C1",
            ],
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
            Some("bool") if self.rust3 => &["t"],
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
            && !(if self.rust3 {
                known_pattern(p)
            } else {
                hex_pattern(p).is_some()
            })
        {
            return Err(format!("{at}: unimplemented pattern {p}"));
        }
        if let Some(l) = t.get("lexical").and_then(txt) {
            let rule = self
                .lexical
                .get(l)
                .and_then(obj)
                .ok_or(format!("{at}: lexical {l}"))?;
            let package_key = self.rust3 && l == "package-key";
            let allowed: &[&str] = if package_key {
                &[
                    "kind",
                    "separator",
                    "nameVersionForbidAtOrBelow",
                    "owner",
                    "deliberate",
                    "text",
                ]
            } else if self.rust3 {
                &[
                    "kind",
                    "separator",
                    "forbiddenScalars",
                    "forbiddenSegments",
                    "maxSegmentScalars",
                    "owner",
                    "text",
                    "firstSegmentForbiddenPattern",
                ]
            } else {
                &[
                    "kind",
                    "separator",
                    "forbiddenScalars",
                    "forbiddenSegments",
                    "maxSegmentScalars",
                    "owner",
                    "text",
                ]
            };
            if rule.get("kind").and_then(txt)
                != Some(if package_key {
                    "package-key"
                } else {
                    "segments"
                })
                || rule.keys().any(|k| !allowed.contains(&k.as_str()))
            {
                return Err(format!("{at}: unimplemented lexical rule {l}"));
            }
            if let Some(pattern) = rule.get("firstSegmentForbiddenPattern")
                && txt(pattern) != Some("^[A-Za-z]:")
            {
                return Err(format!("{at}: unimplemented first-segment pattern"));
            }
            if package_key
                && (rule.get("separator").and_then(txt) != Some(" ")
                    || num(rule.get("nameVersionForbidAtOrBelow")) != Some(32))
            {
                return Err(format!("{at}: unimplemented package-key grammar"));
            }
        }
        if let Some(o) = t.get("order").and_then(txt)
            && !(if self.rust3 {
                &ORDERS[..]
            } else {
                &ORDERS[..7]
            })
            .contains(&o)
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
                if num(t.get("min")).is_some_and(|min| *n < min) {
                    return fail("below min");
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
                if num(t.get("maxUtf8Bytes")).is_some_and(|max| s.len() as u64 > max) {
                    return fail("UTF-8 byte length");
                }
                if t.get("forbidC0C1") == Some(&J::Bool(true))
                    && s.chars()
                        .any(|c| c <= '\u{1f}' || ('\u{80}'..='\u{9f}').contains(&c))
                {
                    return fail("C0/C1 control");
                }
                if let Some(pattern) = t.get("pattern").and_then(txt)
                    && !pattern_ok(pattern, s)
                {
                    return fail("pattern");
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
            Some("bool") => {
                let Value::Bool(_) = v else {
                    return fail("not a bool");
                };
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
                if record.get("kind").and_then(txt) == Some("alias") {
                    return self.check(record.get("target").ok_or(at)?, v, at);
                }
                let Value::Map(fields) = v else {
                    return fail("not a map");
                };
                match record.get("kind").and_then(txt) {
                    Some("record") => {
                        let members = self.members(name);
                        if fields
                            .iter()
                            .map(|(key, _)| key)
                            .collect::<std::collections::BTreeSet<_>>()
                            .len()
                            != fields.len()
                            || fields.iter().any(|(field, _)| {
                                !members.iter().any(|(member, _)| member == field)
                            })
                        {
                            return fail("member set");
                        }
                        let Some(J::Array(declarations)) = record.get("members") else {
                            return fail("members");
                        };
                        for (mname, mt) in &members {
                            if let Some(x) = field(fields, mname) {
                                self.check(mt, x, &format!("{at}.{mname}"))?;
                            } else {
                                let optional = declarations.iter().filter_map(obj).any(|member| {
                                    member.get("name").and_then(txt) == Some(mname)
                                        && member.get("presence").and_then(txt) == Some("optional")
                                });
                                if !optional {
                                    return Err(format!("{at}: missing {mname}"));
                                }
                            }
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
                if self.rust3 {
                    super::super::rust3::admit_extern(r, v)
                } else {
                    admit_extern(r, v)
                }
                .map_err(|e| format!("{at}: {e}"))?;
            }
            _ => return fail("form"),
        }
        Ok(())
    }

    fn lexical_ok(&self, rule: &str, s: &str) -> Result<(), String> {
        let r = self.lexical.get(rule).and_then(obj).ok_or("lexical rule")?;
        let sep = r.get("separator").and_then(txt).ok_or("separator")?;
        if rule == "package-key" {
            let mut parts = s.splitn(3, sep);
            let name = parts.next().ok_or("package name")?;
            let version = parts.next().ok_or("package version")?;
            let _source_id = parts.next().ok_or("package sourceId separator")?;
            return if [name, version]
                .iter()
                .all(|part| !part.is_empty() && part.chars().all(|c| c > '\u{20}'))
            {
                Ok(())
            } else {
                Err("package-key: name/version".to_owned())
            };
        }
        if r.contains_key("firstSegmentForbiddenPattern") {
            let first = s.split(sep).next().unwrap_or_default().as_bytes();
            if first.len() >= 2 && first[0].is_ascii_alphabetic() && first[1] == b':' {
                return Err(format!("{rule}: first segment drive prefix"));
            }
        }
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
        "cve1-bytes-strict" => strictly(
            items
                .iter()
                .map(|v| {
                    to_json(v)
                        .ok()
                        .and_then(|json| opensip_identity::encode_cve1(&json).ok())
                })
                .collect(),
        ),
        "outputOrdinal-contiguous" => {
            if items.iter().enumerate().all(|(index, value)| {
                matches!(value, Value::Map(fields)
                    if field(fields, "outputOrdinal") == Some(&Value::Unsigned(index as u64)))
            }) {
                Ok(())
            } else {
                Err("outputOrdinal-contiguous".to_owned())
            }
        }
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

#[cfg(test)]
mod rust3_grammar_tests {
    use super::*;

    fn text(value: &str) -> Value {
        Value::Text(value.to_owned())
    }
    fn scalar(c: &Carriers, name: &str, value: &str) -> bool {
        c.check_record(name, &text(value)).is_ok()
    }

    #[test]
    fn rust3_snapshot_variants_require_the_published_boolean_and_null_slots() {
        let c = Carriers::load("Rust3").unwrap();
        let file = vec![
            ("path".to_owned(), text("main.rs")),
            ("kind".to_owned(), text("file")),
            ("byteLength".to_owned(), Value::Unsigned(3)),
            ("contentSha256".to_owned(), text(&"a".repeat(64))),
            ("executable".to_owned(), Value::Bool(false)),
            ("targetBytes".to_owned(), Value::Null),
        ];
        assert!(
            c.check_record("Rust3SnapshotEntryV2", &Value::Map(file.clone()))
                .is_ok()
        );
        for (member, bad) in [
            ("executable", Value::Unsigned(0)),
            ("targetBytes", Value::Bytes(vec![1])),
        ] {
            let mut fields = file.clone();
            fields.iter_mut().find(|(key, _)| key == member).unwrap().1 = bad;
            assert!(
                c.check_record("Rust3SnapshotEntryV2", &Value::Map(fields))
                    .is_err(),
                "{member}"
            );
        }
        let mut link = file;
        for (key, value) in &mut link {
            *value = match key.as_str() {
                "kind" => text("symlink"),
                "byteLength" | "contentSha256" | "executable" => Value::Null,
                "targetBytes" => Value::Bytes(b"target".to_vec()),
                _ => value.clone(),
            };
        }
        assert!(
            c.check_record("Rust3SnapshotEntryV2", &Value::Map(link.clone()))
                .is_ok()
        );
        link.iter_mut()
            .find(|(key, _)| key == "executable")
            .unwrap()
            .1 = Value::Bool(false);
        assert!(
            c.check_record("Rust3SnapshotEntryV2", &Value::Map(link))
                .is_err()
        );
    }

    #[test]
    fn rust3_optional_stage_members_preserve_absence_without_accepting_null_or_duplicates() {
        let c = Carriers::load("Rust3").unwrap();
        let minimal = vec![
            ("kind".to_owned(), text("fact-derivation")),
            ("stageId".to_owned(), text("stage-one")),
            ("relations".to_owned(), Value::Array(vec![text("file")])),
            ("operator".to_owned(), text("semantic-provider")),
        ];
        assert!(
            c.check_record("Rust3C2PlanStageV3", &Value::Map(minimal.clone()))
                .is_ok()
        );
        for (member, valid) in [
            ("dependsOn", Value::Array(Vec::new())),
            (
                "budget",
                Value::Map(vec![
                    ("unit".to_owned(), text("items")),
                    ("limit".to_owned(), Value::Unsigned(1)),
                ]),
            ),
            ("capabilityGrants", Value::Array(vec![text("read-source")])),
            ("providerId", text("rust-semantic")),
        ] {
            let mut fields = minimal.clone();
            fields.push((member.to_owned(), valid));
            assert!(
                c.check_record("Rust3C2PlanStageV3", &Value::Map(fields))
                    .is_ok(),
                "{member}"
            );
            let mut fields = minimal.clone();
            fields.push((member.to_owned(), Value::Null));
            assert!(
                c.check_record("Rust3C2PlanStageV3", &Value::Map(fields))
                    .is_err(),
                "{member}"
            );
        }
        let mut duplicate = minimal.clone();
        duplicate.push(("stageId".to_owned(), text("stage-two")));
        assert!(
            c.check_record("Rust3C2PlanStageV3", &Value::Map(duplicate))
                .is_err()
        );
        let mut unknown = minimal.clone();
        unknown.push(("extra".to_owned(), Value::Null));
        assert!(
            c.check_record("Rust3C2PlanStageV3", &Value::Map(unknown))
                .is_err()
        );
        let mut missing = minimal;
        missing.retain(|(key, _)| key != "stageId");
        assert!(
            c.check_record("Rust3C2PlanStageV3", &Value::Map(missing))
                .is_err()
        );
    }

    #[test]
    fn rust3_grammar_loads_and_distinguishes_byte_and_scalar_path_bounds() {
        let c = Carriers::load("Rust3").unwrap();
        for (value, accepted) in [
            ("file.rs", true),
            ("dir/\n.rs", true),
            ("C:/file", false),
            ("c:relative", false),
            ("1:/file", true),
            ("dir/C:/file", true),
            ("dir/.\n/file", true),
            ("dir/..\n/file", true),
            ("dir/./file", false),
            ("dir/../file", false),
            ("dir//file", false),
            ("/file", false),
            ("file/", false),
            ("file\\name", false),
            ("file\0name", false),
        ] {
            assert_eq!(
                scalar(&c, "Rust3CanonicalPath", value),
                accepted,
                "{value:?}"
            );
            assert_eq!(
                scalar(&c, "Rust3DependencySourcePath", value),
                accepted,
                "{value:?}"
            );
        }
        assert!(scalar(&c, "Rust3CanonicalPath", &"x".repeat(4096)));
        assert!(!scalar(&c, "Rust3CanonicalPath", &"x".repeat(4097)));
        assert!(scalar(&c, "Rust3CanonicalPath", &"😀".repeat(1024)));
        assert!(!scalar(&c, "Rust3CanonicalPath", &"😀".repeat(1025)));
        assert!(scalar(&c, "Rust3DependencySourcePath", &"😀".repeat(4096)));
        assert!(!scalar(&c, "Rust3DependencySourcePath", &"😀".repeat(4097)));
        assert!(Carriers::load("Ts2").is_ok());
    }

    #[test]
    fn rust3_identity_identifier_and_package_key_follow_their_separate_owners() {
        let c = Carriers::load("Rust3").unwrap();
        for (value, accepted) in [
            ("id", true),
            ("\u{7f}", true),
            ("\n", false),
            ("\u{85}", false),
            ("", false),
        ] {
            assert_eq!(
                scalar(&c, "Rust3IdentityText", value),
                accepted,
                "{value:?}"
            );
        }
        assert!(scalar(&c, "Rust3IdentityText", &"😀".repeat(1024)));
        assert!(!scalar(&c, "Rust3IdentityText", &"😀".repeat(1025)));
        for (value, accepted) in [
            ("a0.b:c_d-e", true),
            ("a..b", false),
            ("A", false),
            ("a-", false),
            ("a\n", false),
        ] {
            assert_eq!(
                scalar(&c, "Rust3CanonicalIdentifier", value),
                accepted,
                "{value:?}"
            );
        }
        assert!(scalar(&c, "Rust3CanonicalIdentifier", &"a".repeat(128)));
        assert!(!scalar(&c, "Rust3CanonicalIdentifier", &"a".repeat(129)));
        for (value, accepted) in [
            ("name version ", true),
            ("name version source with spaces", true),
            ("name\u{7f} ver\u{85} source", true),
            ("name version", false),
            (" name source", false),
            ("name  source", false),
            ("na\tme version source", false),
        ] {
            assert_eq!(scalar(&c, "Rust3PackageKey", value), accepted, "{value:?}");
        }
        for (value, accepted) in [
            (".opensip/prepared/v3/0-", true),
            (".opensip/prepared/v3/123-", true),
            (".opensip/prepared/v3/00-", false),
            (".opensip/prepared/v3/-1-", false),
        ] {
            let path = format!("{value}{}.blob", "a".repeat(64));
            assert_eq!(pattern_ok(PREPARED_PATTERN, &path), accepted, "{path}");
            assert!(!pattern_ok(PREPARED_PATTERN, &format!("{path}\n")));
        }
        assert!(!known_pattern(".*"));
        assert!(!pattern_ok(".*", "anything"));
    }

    #[test]
    fn rust3_uint_minimum_alias_and_cve1_order_are_enforced() {
        let c = Carriers::load("Rust3").unwrap();
        let budget = |limit| {
            Value::Map(vec![
                ("unit".to_owned(), text("items")),
                ("limit".to_owned(), Value::Unsigned(limit)),
            ])
        };
        assert!(c.check_record("Rust3C2StageBudgetV1", &budget(1)).is_ok());
        assert!(c.check_record("Rust3C2StageBudgetV1", &budget(0)).is_err());
        assert!(
            c.check_record("Rust3C2StageBudgetV1", &budget(i64::MAX as u64 + 1))
                .is_err()
        );
        let seal = Value::Map(vec![
            (
                "dependencySourceSetId".to_owned(),
                text(&format!("sha256:{}", "a".repeat(64))),
            ),
            ("manifestSha256".to_owned(), text(&"b".repeat(64))),
            ("entryCount".to_owned(), Value::Unsigned(0)),
            ("totalBytes".to_owned(), Value::Unsigned(0)),
            ("totalChunkCount".to_owned(), Value::Unsigned(0)),
        ]);
        let reference =
            "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3";
        assert!(admit_extern(reference, &seal).is_ok());
        assert!(
            c.check_record("Rust3DependencySourceAcceptedV3", &seal)
                .is_ok()
        );
        assert!(
            c.check_record("Rust3DependencySourceAcceptedV3", &Value::Map(Vec::new()))
                .is_err()
        );
        // CVE1 text uses a fixed length field: one-byte z precedes two-byte aa.
        // This is intentionally the reverse of ordinary lexical text order.
        assert!(order_ok("cve1-bytes-strict", &[text("z"), text("aa")]).is_ok());
        assert!(order_ok("cve1-bytes-strict", &[text("aa"), text("z")]).is_err());
        assert!(order_ok("cve1-bytes-strict", &[text("z"), text("z")]).is_err());
        let anchor = |path: &str, end| {
            Value::Map(vec![
                ("kind".to_owned(), text("source-span")),
                (
                    "snapshotId".to_owned(),
                    text(&format!("snapshot2:{}", "a".repeat(64))),
                ),
                ("path".to_owned(), text(path)),
                ("contentSha256".to_owned(), text(&"b".repeat(64))),
                ("startByte".to_owned(), Value::Unsigned(0)),
                ("endByte".to_owned(), Value::Unsigned(end)),
                ("factId".to_owned(), Value::Null),
            ])
        };
        let a = anchor("z", 2);
        let b = anchor("aa", 1);
        assert!(c.check_record("Rust3AnchorRefV1", &a).is_ok());
        assert!(c.check_record("Rust3AnchorRefV1", &b).is_ok());
        assert!(cbor::encode(&a) < cbor::encode(&b));
        assert!(order_ok("cve1-bytes-strict", &[b.clone(), a.clone()]).is_ok());
        assert!(order_ok("cve1-bytes-strict", &[a, b]).is_err());
        let row = |n| Value::Map(vec![("outputOrdinal".to_owned(), Value::Unsigned(n))]);
        assert!(order_ok("outputOrdinal-contiguous", &[row(0), row(1)]).is_ok());
        assert!(order_ok("outputOrdinal-contiguous", &[row(1), row(2)]).is_err());
        assert!(order_ok("outputOrdinal-contiguous", &[row(0), row(0)]).is_err());
    }
}
