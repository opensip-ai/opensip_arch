//! Pure descriptor validation helpers over explicitly supplied values.
//! Lexical paths, exact collection order and shape-checked candidate identities.
//! Candidate identities do not establish retained closure or replay authority.
use alloc::string::String;
use core::fmt;

/// A string admitted by the selected identity schema's LogicalPath definition.
///
/// This is a lexical value, never filesystem custody or authorization. No
/// normalization, filesystem access or snapshot join occurs. Use it for the
/// direct Blob.path / import-blob.path profile, not scope paths (where `.` can
/// mean root) or the differently constrained fingerprint logicalPath member.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct LogicalPath(String);

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum LogicalPathError {
    Empty,
    PathLength,
    InvalidComponent,
    ComponentLength,
}
impl fmt::Display for LogicalPathError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}
impl core::error::Error for LogicalPathError {}

impl LogicalPath {
    pub fn parse(value: &str) -> Result<Self, LogicalPathError> {
        if value.is_empty() {
            return Err(LogicalPathError::Empty);
        }
        // Schema character limits count Unicode scalars, not UTF-8 bytes or
        // UTF-16 code units. Stop counting once the admitted bound is exceeded.
        if value.chars().take(4097).count() > 4096 {
            return Err(LogicalPathError::PathLength);
        }
        if value.contains(['\\', '\0']) {
            return Err(LogicalPathError::InvalidComponent);
        }
        for part in value.split('/') {
            if matches!(part, "" | "." | "..") {
                return Err(LogicalPathError::InvalidComponent);
            }
            if part.chars().take(256).count() > 255 {
                return Err(LogicalPathError::ComponentLength);
            }
        }
        // Preserve the selected pattern's Python-compatible `$` behavior in
        // `not: (^|/)\.\.?(/|$)`: it also matches before one final LF.
        // Do not silently widen that schema while enforcing semantic segments.
        if value
            .strip_suffix('\n')
            .is_some_and(|prefix| matches!(prefix.rsplit('/').next(), Some("." | "..")))
        {
            return Err(LogicalPathError::InvalidComponent);
        }
        Ok(Self(String::from(value)))
    }
    pub fn as_str(&self) -> &str {
        &self.0
    }
    pub fn into_string(self) -> String {
        self.0
    }
}
impl core::str::FromStr for LogicalPath {
    type Err = LogicalPathError;
    fn from_str(value: &str) -> Result<Self, Self::Err> {
        Self::parse(value)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use alloc::{vec, vec::Vec};

    #[test]
    fn refuses_noncanonical_segments_without_normalizing() {
        for path in [
            "",
            "/a",
            "a/",
            "a//b",
            ".",
            "..",
            "a/./b",
            "a/../b",
            "a\\b",
            "a\0b",
            "a\n/../../b",
        ] {
            assert!(LogicalPath::parse(path).is_err(), "{path:?}");
        }
        for path in ["src/lib.rs", "...", " a ", "a:b", "a\nb/c"] {
            let admitted = LogicalPath::parse(path).unwrap();
            assert_eq!(admitted.as_str(), path);
            assert_eq!(admitted.into_string(), path);
        }
    }

    #[test]
    fn unicode_scalar_limits_are_not_byte_or_utf16_limits() {
        assert!(LogicalPath::parse(&"😀".repeat(255)).is_ok());
        assert_eq!(
            LogicalPath::parse(&"😀".repeat(256)),
            Err(LogicalPathError::ComponentLength)
        );
        let mut parts: Vec<String> = vec!["a".repeat(255); 15];
        parts.push("b".repeat(254));
        parts.push(String::from("c"));
        let boundary = parts.join("/");
        assert_eq!(boundary.chars().count(), 4096);
        assert!(LogicalPath::parse(&boundary).is_ok());
        assert_eq!(
            LogicalPath::parse(&(boundary + "x")),
            Err(LogicalPathError::PathLength)
        );
    }

    #[test]
    fn preserves_distinct_unicode_spellings_and_order() {
        let nfc = LogicalPath::parse("é/file").unwrap();
        let nfd = LogicalPath::parse("e\u{301}/file").unwrap();
        assert_ne!(nfc, nfd);
        assert_eq!(nfc.as_str(), "é/file");
        assert_eq!(nfd.as_str(), "e\u{301}/file");
        assert!(nfd < nfc);
    }

    #[test]
    fn preserves_selected_final_lf_not_pattern_edge() {
        for path in [".\n", "..\n", "a/.\n", "a/..\n"] {
            assert_eq!(
                LogicalPath::parse(path),
                Err(LogicalPathError::InvalidComponent)
            );
        }
        for path in ["a\n", ".\n\n", "a/.\r\n", ".\u{2028}", ".\u{2029}"] {
            assert!(LogicalPath::parse(path).is_ok(), "{path:?}");
        }
    }
}

/// A selected `x-opensip-order` annotation, parsed without guessing a default.
///
/// This value checks only the order law supplied by the caller. Choosing the
/// registered schema, admitting item shapes and completing cross-object joins
/// are separate obligations. Success creates no evidence authority. Arrays are
/// never sorted or deduplicated: sequences and observed multiplicities survive.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ArrayOrder(OrderKind);

#[derive(Clone, Debug, PartialEq, Eq)]
enum OrderKind {
    Sequence,
    Utf8,
    CanonicalSet,
    CanonicalOrder,
    Fields(alloc::vec::Vec<String>),
    Numeric,
    Ordinal,
    CandidateOrdinal,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ArrayOrderError {
    InvalidAnnotation,
    ExpectedString,
    ExpectedObject,
    MissingField,
    ExpectedInteger,
    NonIncreasing,
    NonContiguousOrdinal,
    Canonical(crate::CanonicalError),
}
impl fmt::Display for ArrayOrderError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}
impl core::error::Error for ArrayOrderError {}

impl ArrayOrder {
    /// Parse the exact selected annotation vocabulary. Unknown names, malformed
    /// field tuples, duplicate fields and extra annotation members refuse even
    /// when a later value would be an empty array.
    pub fn parse(annotation: &crate::JsonValue) -> Result<Self, ArrayOrderError> {
        use crate::JsonValue as V;
        let kind = match annotation {
            V::String(name) => match name.as_str() {
                "sequence" => OrderKind::Sequence,
                "utf8" => OrderKind::Utf8,
                "canonical-set" => OrderKind::CanonicalSet,
                "canonical-order" => OrderKind::CanonicalOrder,
                "numeric" => OrderKind::Numeric,
                "ordinal" => OrderKind::Ordinal,
                "candidateOrdinal" => OrderKind::CandidateOrdinal,
                "path" | "ruleId" | "waiverId" => OrderKind::Fields(alloc::vec![name.clone()]),
                "predicate" => OrderKind::Fields(
                    ["ruleId", "subjectId", "predicateId"]
                        .into_iter()
                        .map(String::from)
                        .collect(),
                ),
                _ => return Err(ArrayOrderError::InvalidAnnotation),
            },
            V::Object(object) if object.len() == 1 => {
                let Some(V::Array(fields)) = object.get("by") else {
                    return Err(ArrayOrderError::InvalidAnnotation);
                };
                if fields.is_empty() {
                    return Err(ArrayOrderError::InvalidAnnotation);
                }
                let mut names = alloc::vec::Vec::with_capacity(fields.len());
                let mut seen = alloc::collections::BTreeSet::new();
                for field in fields {
                    let V::String(name) = field else {
                        return Err(ArrayOrderError::InvalidAnnotation);
                    };
                    if name.is_empty() || !seen.insert(name) {
                        return Err(ArrayOrderError::InvalidAnnotation);
                    }
                    names.push(name.clone());
                }
                OrderKind::Fields(names)
            }
            _ => return Err(ArrayOrderError::InvalidAnnotation),
        };
        Ok(Self(kind))
    }

    /// Check exact order without changing supplied values. Numeric keys compare
    /// exact signed/unsigned profile integers, not text or floating point. Tuple
    /// keys compare fields in declared order using raw UTF-8. Canonical keys use
    /// complete canonical JSON bytes; these can order differently from raw text.
    ///
    /// The surrounding descriptor's bounded JSON and item schema admission must
    /// still run. In particular, sequence imposes no item-shape or ordering law.
    pub fn verify(&self, values: &[crate::JsonValue]) -> Result<(), ArrayOrderError> {
        use crate::JsonValue as V;
        if self.0 == OrderKind::Sequence {
            return Ok(());
        }
        // Hold at most the previous and current keys; never build a sorted copy
        // of the document merely to verify the caller-supplied order.
        #[derive(PartialEq, Eq, PartialOrd, Ord)]
        enum Key<'a> {
            Text(&'a str),
            Tuple(alloc::vec::Vec<&'a str>),
            Canonical(alloc::vec::Vec<u8>),
            Number(i128),
        }
        fn field<'a>(value: &'a V, name: &str) -> Result<&'a V, ArrayOrderError> {
            let V::Object(object) = value else {
                return Err(ArrayOrderError::ExpectedObject);
            };
            object.get(name).ok_or(ArrayOrderError::MissingField)
        }
        fn text(value: &V) -> Result<&str, ArrayOrderError> {
            match value {
                V::String(s) => Ok(s),
                _ => Err(ArrayOrderError::ExpectedString),
            }
        }
        fn integer(value: &V) -> Result<i128, ArrayOrderError> {
            match value {
                V::Integer(n) => Ok(n.get()),
                _ => Err(ArrayOrderError::ExpectedInteger),
            }
        }
        let mut previous = None;
        for (index, value) in values.iter().enumerate() {
            let key = match &self.0 {
                OrderKind::Sequence => unreachable!("sequence returned before iteration"),
                OrderKind::Utf8 => Key::Text(text(value)?),
                OrderKind::Fields(fields) => Key::Tuple(
                    fields
                        .iter()
                        .map(|name| text(field(value, name)?))
                        .collect::<Result<_, _>>()?,
                ),
                OrderKind::CanonicalSet | OrderKind::CanonicalOrder => Key::Canonical(
                    crate::canonical_bytes(value).map_err(ArrayOrderError::Canonical)?,
                ),
                OrderKind::Numeric => Key::Number(integer(value)?),
                OrderKind::CandidateOrdinal => {
                    Key::Number(integer(field(value, "candidateOrdinal")?)?)
                }
                OrderKind::Ordinal => {
                    let ordinal = integer(field(value, "ordinal")?)?;
                    if ordinal != index as i128 {
                        return Err(ArrayOrderError::NonContiguousOrdinal);
                    }
                    Key::Number(ordinal)
                }
            };
            if let Some(prior) = previous.as_ref() {
                let invalid = if self.0 == OrderKind::CanonicalOrder {
                    prior > &key
                } else {
                    prior >= &key
                };
                if invalid {
                    return Err(ArrayOrderError::NonIncreasing);
                }
            }
            previous = Some(key);
        }
        Ok(())
    }
}

#[cfg(test)]
mod order_tests {
    use super::*;
    use crate::{JsonValue, canonical_bytes, parse_json};

    fn check(annotation: &str, input: &str) -> Result<(), ArrayOrderError> {
        let order = ArrayOrder::parse(&parse_json(annotation.as_bytes()).unwrap())?;
        let JsonValue::Array(values) = parse_json(input.as_bytes()).unwrap() else {
            panic!("test fixture must be an array");
        };
        order.verify(&values)
    }
    #[test]
    fn raw_text_and_canonical_json_have_distinct_orders() {
        assert!(check(r#""utf8""#, r#"["\n","!"]"#).is_ok());
        assert!(check(r#""utf8""#, r#"["!","\n"]"#).is_err());
        assert!(check(r#""canonical-set""#, r#"["!","\n"]"#).is_ok());
        assert!(check(r#""canonical-set""#, r#"["\n","!"]"#).is_err());
    }
    #[test]
    fn multiplicity_is_specific_to_the_selected_law() {
        for annotation in [r#""utf8""#, r#""canonical-set""#] {
            assert_eq!(
                check(annotation, r#"["a","a"]"#),
                Err(ArrayOrderError::NonIncreasing)
            );
        }
        assert!(check(r#""canonical-order""#, r#"["a","a","b"]"#).is_ok());
        assert!(check(r#""canonical-order""#, r#"["b","a","a"]"#).is_err());
        let input = parse_json(br#"["x","(",")","x"]"#).unwrap();
        let before = canonical_bytes(&input).unwrap();
        let JsonValue::Array(ref values) = input else {
            unreachable!()
        };
        ArrayOrder::parse(&JsonValue::String(String::from("sequence")))
            .unwrap()
            .verify(values)
            .unwrap();
        assert_eq!(canonical_bytes(&input).unwrap(), before);
    }
    #[test]
    fn field_tuples_compare_only_declared_keys_in_declared_order() {
        assert!(
            check(
                r#"{"by":["name"]}"#,
                r#"[{"a":"z","name":"a"},{"a":"a","name":"z"}]"#
            )
            .is_ok()
        );
        assert!(
            check(
                r#"{"by":["name"]}"#,
                r#"[{"name":"a","payload":1},{"name":"a","payload":2}]"#
            )
            .is_err()
        );
        assert!(
            check(
                r#"{"by":["name","version"]}"#,
                r#"[{"name":"a","version":"1"},{"name":"a","version":"2"}]"#
            )
            .is_ok()
        );
        assert!(
            check(
                r#"{"by":["name","version"]}"#,
                r#"[{"name":"a","version":"2"},{"name":"a","version":"1"}]"#
            )
            .is_err()
        );
        assert!(check(r#""predicate""#, r#"[{"ruleId":"r","subjectId":"s","predicateId":"a"},{"ruleId":"r","subjectId":"s","predicateId":"b"}]"#).is_ok());
        for name in ["path", "ruleId", "waiverId"] {
            let annotation = alloc::format!("\"{name}\"");
            let values = alloc::format!("[{{\"{name}\":\"a\"}},{{\"{name}\":\"b\"}}]");
            assert!(check(&annotation, &values).is_ok());
        }
    }
    #[test]
    fn integer_order_is_exact_and_candidate_ordinal_can_have_gaps() {
        assert!(check(r#""numeric""#, "[-9223372036854775808,-1,0,2,10,9007199254740992,9007199254740993,18446744073709551615]").is_ok());
        assert!(check(r#""numeric""#, "[10,2]").is_err());
        assert!(check(r#""numeric""#, "[true]").is_err());
        assert!(check(r#""ordinal""#, r#"[{"ordinal":0},{"ordinal":1}]"#).is_ok());
        assert_eq!(
            check(r#""ordinal""#, r#"[{"ordinal":0},{"ordinal":2}]"#),
            Err(ArrayOrderError::NonContiguousOrdinal)
        );
        assert!(
            check(
                r#""candidateOrdinal""#,
                r#"[{"candidateOrdinal":4},{"candidateOrdinal":7}]"#
            )
            .is_ok()
        );
        assert!(
            check(
                r#""candidateOrdinal""#,
                r#"[{"candidateOrdinal":4},{"candidateOrdinal":4}]"#
            )
            .is_err()
        );
        // Sign bounds belong to item schema, not this order annotation.
        assert!(
            check(
                r#""candidateOrdinal""#,
                r#"[{"candidateOrdinal":-2},{"candidateOrdinal":-1}]"#
            )
            .is_ok()
        );
    }
    #[test]
    fn malformed_annotations_refuse_even_for_empty_arrays() {
        for annotation in [
            "null",
            "true",
            "1",
            "[]",
            r#""unknown""#,
            r#"{"by":[]}"#,
            r#"{"by":[""]}"#,
            r#"{"by":["n","n"]}"#,
            r#"{"by":["n"],"descending":true}"#,
            r#"{"by":"n"}"#,
            r#"{"by":[1]}"#,
        ] {
            assert_eq!(
                check(annotation, "[]"),
                Err(ArrayOrderError::InvalidAnnotation),
                "{annotation}"
            );
        }
    }
    #[test]
    fn ordered_keys_must_have_the_exact_required_type() {
        assert_eq!(
            check(r#""utf8""#, "[1]"),
            Err(ArrayOrderError::ExpectedString)
        );
        assert_eq!(
            check(r#"{"by":["n"]}"#, "[1]"),
            Err(ArrayOrderError::ExpectedObject)
        );
        assert_eq!(
            check(r#"{"by":["n"]}"#, "[{}]"),
            Err(ArrayOrderError::MissingField)
        );
        assert_eq!(
            check(r#"{"by":["n"]}"#, r#"[{"n":1}]"#),
            Err(ArrayOrderError::ExpectedString)
        );
        assert_eq!(
            check(r#""candidateOrdinal""#, r#"[{"candidateOrdinal":"0"}]"#),
            Err(ArrayOrderError::ExpectedInteger)
        );
        assert_eq!(
            check(r#""ordinal""#, r#"[{"ordinal":false}]"#),
            Err(ArrayOrderError::ExpectedInteger)
        );
    }
}

use crate::schema_registry::{AdmissionError, RegisteredSchemas, ShapeValue};
use crate::{DigestError, JsonValue as V, digest_hex, hash_canonical_value};
use alloc::{collections::BTreeMap, format, string::ToString};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IdentityDomain {
    Fact,
    Snapshot,
    Closure,
    Import,
    Plan,
    SubjectScope,
    Coverage,
    View,
    ExecutionPlan,
    FindingFingerprint,
    Finding,
    ProofBundle,
    SemanticEvidence,
    EvaluationSeal,
    Run,
    CacheKey,
    RegenerationKey,
    PolicyDerivation,
    EvaluationSubject,
}
impl IdentityDomain {
    pub fn parse(s: &str) -> Result<Self, CandidateError> {
        Ok(match s {
            "fact" => Self::Fact,
            "snapshot" => Self::Snapshot,
            "closure" => Self::Closure,
            "import" => Self::Import,
            "plan" => Self::Plan,
            "subject-scope" => Self::SubjectScope,
            "coverage" => Self::Coverage,
            "view" => Self::View,
            "execution-plan" => Self::ExecutionPlan,
            "finding-fingerprint" => Self::FindingFingerprint,
            "finding" => Self::Finding,
            "proof-bundle" => Self::ProofBundle,
            "semantic-evidence" => Self::SemanticEvidence,
            "evaluation-seal" => Self::EvaluationSeal,
            "run" => Self::Run,
            "cache-key" => Self::CacheKey,
            "regeneration-key" => Self::RegenerationKey,
            "policy-derivation" => Self::PolicyDerivation,
            "evaluation-subject" => Self::EvaluationSubject,
            _ => return Err(CandidateError::Domain),
        })
    }
    pub fn name(self) -> &'static str {
        self.parts().0
    }
    pub fn prefix(self) -> &'static str {
        self.parts().1
    }
    fn parts(self) -> (&'static str, &'static str) {
        match self {
            Self::Fact => ("fact", "fact2"),
            Self::Snapshot => ("snapshot", "snapshot2"),
            Self::Closure => ("closure", "closure2"),
            Self::Import => ("import", "import2"),
            Self::Plan => ("plan", "plan2"),
            Self::SubjectScope => ("subject-scope", "scope2"),
            Self::Coverage => ("coverage", "coverage2"),
            Self::View => ("view", "view2"),
            Self::ExecutionPlan => ("execution-plan", "exec-plan2"),
            Self::FindingFingerprint => ("finding-fingerprint", "finding-key2"),
            Self::Finding => ("finding", "finding3"),
            Self::ProofBundle => ("proof-bundle", "proof3"),
            Self::SemanticEvidence => ("semantic-evidence", "evidence3"),
            Self::EvaluationSeal => ("evaluation-seal", "seal3"),
            Self::Run => ("run", "run3"),
            Self::CacheKey => ("cache-key", "cache2"),
            Self::RegenerationKey => ("regeneration-key", "regen2"),
            Self::PolicyDerivation => ("policy-derivation", "policy-derivation3"),
            Self::EvaluationSubject => ("evaluation-subject", "subject3"),
        }
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CandidateError {
    Domain,
    Schema(AdmissionError),
    Order(ArrayOrderError),
    LogicalPath,
    StageDag,
    Digest(DigestError),
}
impl From<AdmissionError> for CandidateError {
    fn from(e: AdmissionError) -> Self {
        Self::Schema(e)
    }
}
impl From<ArrayOrderError> for CandidateError {
    fn from(e: ArrayOrderError) -> Self {
        Self::Order(e)
    }
}
/// A reproducible candidate ID, not proof that referenced objects exist or that
/// an evaluator/security/storage boundary admitted the complete graph.
pub struct IdentityCandidate<'a> {
    domain: IdentityDomain,
    shape: ShapeValue<'a>,
    identifier: String,
}
impl<'a> IdentityCandidate<'a> {
    pub fn from_json(
        registry: &'a RegisteredSchemas,
        domain: IdentityDomain,
        raw: &[u8],
        budget: usize,
    ) -> Result<Self, CandidateError> {
        let shape = registry
            .schema(
                "urn:opensip:product-v1:identity:v3",
                &format!("/$defs/{}", domain.name()),
            )?
            .admit_json(raw, budget)?;
        ordered(shape.value(), "")?;
        let digest =
            hash_canonical_value(domain.name(), shape.value()).map_err(CandidateError::Digest)?;
        let identifier = format!("{}:{}", domain.prefix(), digest_hex(&digest));
        Ok(Self {
            domain,
            shape,
            identifier,
        })
    }
    pub fn identifier(&self) -> &str {
        &self.identifier
    }
    pub fn domain(&self) -> IdentityDomain {
        self.domain
    }
    pub fn descriptor(&self) -> &V {
        self.shape.value()
    }
    pub fn schema_document_sha256(&self) -> [u8; 32] {
        self.shape.schema().document_sha256()
    }
}
fn path(s: &str) -> bool {
    !s.contains(['\0', '\\']) && s.split('/').all(|part| !matches!(part, "" | "." | ".."))
}
fn named_order(name: &str) -> Result<ArrayOrder, CandidateError> {
    Ok(ArrayOrder::parse(&V::String(name.to_string()))?)
}
fn fields_order(fields: &[&str]) -> Result<ArrayOrder, CandidateError> {
    let mut o = BTreeMap::new();
    o.insert(
        "by".to_string(),
        V::Array(fields.iter().map(|s| V::String((*s).to_string())).collect()),
    );
    Ok(ArrayOrder::parse(&V::Object(o))?)
}
fn object(v: &V) -> Result<&BTreeMap<String, V>, CandidateError> {
    if let V::Object(o) = v {
        Ok(o)
    } else {
        Err(ArrayOrderError::ExpectedObject.into())
    }
}
fn field<'a>(v: &'a V, key: &str) -> Result<&'a V, CandidateError> {
    object(v)?
        .get(key)
        .ok_or(ArrayOrderError::MissingField.into())
}
fn integer(v: &V) -> Result<i128, CandidateError> {
    if let V::Integer(i) = v {
        Ok(i.get())
    } else {
        Err(ArrayOrderError::ExpectedInteger.into())
    }
}
fn ordered(value: &V, name: &str) -> Result<(), CandidateError> {
    match value {
        V::Object(o) => {
            for (key, value) in o {
                if matches!(key.as_str(), "path" | "logicalPath")
                    && let V::String(s) = value
                    && !path(s)
                {
                    return Err(CandidateError::LogicalPath);
                }
                ordered(value, key)?;
            }
        }
        V::Array(a) => {
            let order = match name {
                "allowedScopes" => named_order("sequence")?,
                "sourceInventory" | "tree" | "blobs" => {
                    for v in a {
                        let V::String(s) = field(v, "path")? else {
                            return Err(ArrayOrderError::ExpectedString.into());
                        };
                        if !path(s) {
                            return Err(CandidateError::LogicalPath);
                        }
                    }
                    named_order("path")?
                }
                "requires" => named_order("numeric")?,
                "owner-source-set" => fields_order(&["ownerKey"])?,
                "stages" => {
                    let order = named_order("ordinal")?;
                    order.verify(a)?;
                    for stage in a {
                        let ordinal = integer(field(stage, "ordinal")?)?;
                        let V::Array(requires) = field(stage, "requires")? else {
                            return Err(CandidateError::StageDag);
                        };
                        for dependency in requires {
                            if integer(dependency)? >= ordinal {
                                return Err(CandidateError::StageDag);
                            }
                        }
                    }
                    order
                }
                "predicateProofs" => named_order("predicate")?,
                "ruleResults" => named_order("ruleId")?,
                _ => named_order("canonical-set")?,
            };
            order.verify(a)?;
            for v in a {
                ordered(v, "")?;
            }
        }
        _ => {}
    }
    Ok(())
}
#[cfg(test)]
mod candidate_tests {
    use super::*;
    use crate::parse_json;
    fn check(s: &str, name: &str) -> Result<(), CandidateError> {
        ordered(&parse_json(s.as_bytes()).unwrap(), name)
    }
    #[test]
    fn imperative_paths_are_not_generic_blob_component_limits() {
        for s in ["a", "a/é", "a/.\n", &"x".repeat(256)] {
            assert!(path(s));
        }
        for s in ["", "/a", "a/", "a//b", ".", "a/../b", "a\\b", "a\0b"] {
            assert!(!path(s));
        }
    }
    #[test]
    fn array_order_is_specific_and_never_rewrites() {
        assert!(check("[2,1,1]", "allowedScopes").is_ok());
        assert!(check("[1,2]", "requires").is_ok());
        assert!(check("[1,true]", "requires").is_err());
        assert!(check("[2,1]", "").is_err());
        assert!(check("[1,1]", "").is_err());
        assert!(check(r#"[{"a":"x","b":2},{"a":"y","b":1}]"#, "").is_ok());
    }
    #[test]
    fn stage_order_and_backward_dependencies_are_separate() {
        assert!(
            check(
                r#"[{"ordinal":0,"requires":[]},{"ordinal":1,"requires":[0]}]"#,
                "stages"
            )
            .is_ok()
        );
        assert_eq!(
            check(r#"[{"ordinal":0,"requires":[0]}]"#, "stages"),
            Err(CandidateError::StageDag)
        );
        assert!(check(r#"[{"ordinal":1,"requires":[]}]"#, "stages").is_err());
    }
    #[test]
    fn arbitrary_digest_domains_are_not_registered_candidates() {
        for v in ["", "Fact", "native.context.rust.v2", "fact2", "fact\n"] {
            assert!(IdentityDomain::parse(v).is_err());
        }
        assert_eq!(
            IdentityDomain::parse("finding").unwrap().prefix(),
            "finding3"
        );
    }
}
