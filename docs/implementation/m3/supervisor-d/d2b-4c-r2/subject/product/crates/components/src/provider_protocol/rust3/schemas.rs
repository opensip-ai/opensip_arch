//! Rust3's closed envelope and payload shapes, from the selected carrier
//! document and registered product schemas. These checks do not perform
//! contextual admission or publish a table event. Immutable token selection
//! chooses the FA-2 and subject-scope-reference variants.
use super::super::cbor::Value;
#[cfg(test)]
use super::super::ts2::carrier::SCHEMA_BUDGET;
use super::super::ts2::carrier::{self, Carriers, field};
use opensip_identity::{JsonValue as J, parse_json};
use std::collections::BTreeMap;

const STARTUP: &[u8] = include_bytes!("../../../../../schemas/sources/startup-v1.schema.json");
const STARTUP_ID: &str = "opensip.product.provider-startup.1";

// Rust3's strict reader already bounds and validates its CBOR value. The
// registered evaluator checks the same selected schema directly, preserving
// its native-owner profile without adding an intermediate JSON byte bound.
// Other protocols' existing JSON admission paths remain unchanged.
fn admit_extern(schema_ref: &str, value: &Value) -> Result<(), String> {
    super::schema_work::admit_extern(schema_ref, value)
}

fn obj(value: &J) -> Option<&BTreeMap<String, J>> {
    if let J::Object(fields) = value {
        Some(fields)
    } else {
        None
    }
}
fn text(value: &J) -> Option<&str> {
    if let J::String(s) = value {
        Some(s)
    } else {
        None
    }
}
fn at<'v>(value: &'v J, path: &[&str]) -> Option<&'v J> {
    path.iter()
        .try_fold(value, |value, key| obj(value)?.get(*key))
}
fn number(value: Option<&J>) -> Result<Option<u64>, String> {
    match value {
        None => Ok(None),
        Some(J::Integer(n)) => u64::try_from(n.get())
            .map(Some)
            .map_err(|_| "negative count".to_owned()),
        _ => Err("noninteger count".to_owned()),
    }
}
#[derive(Debug)]
enum Payload {
    Record(String),
    Extern(String),
}
#[derive(Debug)]
struct FrameShape {
    direction: String,
    selector: Option<String>,
    alternatives: BTreeMap<String, Payload>,
}
#[derive(Debug)]
struct Piecewise {
    member: String,
    item_ref: String,
    min: Option<u64>,
    max: Option<u64>,
}

/// The original Rust3 frame-shape checks. This is a codec mechanism, not
/// full protocol admission. The session must independently bind the signed
/// token selection, check contextual joins and commitments, and step P3T.
/// In particular, shape success never authorizes publication or disclosure.
pub struct Rust3PayloadSchemas {
    carriers: Carriers,
    frames: BTreeMap<String, FrameShape>,
    piecewise: BTreeMap<String, Piecewise>,
}
impl Rust3PayloadSchemas {
    pub fn load() -> Result<Self, String> {
        // Registry construction verifies all selected raw-source pins and
        // aliases before any extern entry point is obtained.
        let registry = crate::schema_sources::registry().ok_or("embedded schema registry")?;
        let carriers = Carriers::load("Rust3")?;
        let doc = parse_json(carrier::CARRIERS).map_err(|e| format!("carriers: {e}"))?;
        let protocol = at(&doc, &["protocols", "rust-semantic"]).ok_or("Rust3 protocol")?;
        if at(protocol, &["major"]).and_then(text) != Some("3")
            || at(protocol, &["profile"]).and_then(text) != Some("rust3-cbor")
            || at(protocol, &["envelope"]).and_then(text) != Some("Rust3ProviderFrameV3")
        {
            return Err("unimplemented Rust3 protocol profile".to_owned());
        }
        let Some(J::Array(list)) = at(protocol, &["frames"]) else {
            return Err("Rust3 frames".to_owned());
        };
        let mut frames = BTreeMap::new();
        for frame in list {
            let name = at(frame, &["frameType"])
                .and_then(text)
                .ok_or("frameType")?;
            let direction = at(frame, &["direction"])
                .and_then(text)
                .ok_or("direction")?;
            if !["host-to-worker", "worker-to-host"].contains(&direction) {
                return Err("unknown direction".to_owned());
            }
            let payload = at(frame, &["payload"]).ok_or("payload")?;
            let selector = at(payload, &["select"]).and_then(text);
            let alternatives = if let Some(selector) = selector {
                let expected: &[&str] = match selector {
                    "negotiated-target-attribution-v2" => &["false", "true"],
                    "host-phase" => &["ANALYZING", "WAIT_NATIVE_CONTEXT_VERIFIED"],
                    _ => return Err(format!("unimplemented Rust3 selector {selector}")),
                };
                let alternatives = at(payload, &["alternatives"])
                    .and_then(obj)
                    .ok_or("alternatives")?;
                if alternatives.len() != expected.len()
                    || expected.iter().any(|key| !alternatives.contains_key(*key))
                {
                    return Err(format!("{name}: unexpected selector alternatives"));
                }
                alternatives
                    .iter()
                    .map(|(key, value)| Ok((key.clone(), Self::payload(&carriers, value)?)))
                    .collect::<Result<_, String>>()?
            } else {
                BTreeMap::from([(String::new(), Self::payload(&carriers, payload)?)])
            };
            for value in alternatives.values() {
                if let Payload::Extern(schema) = value {
                    let (id, pointer) = schema.split_once('#').ok_or("extern schemaRef")?;
                    registry
                        .schema(id, pointer)
                        .map_err(|e| format!("{schema}: {e:?}"))?;
                }
            }
            if frames
                .insert(
                    name.to_owned(),
                    FrameShape {
                        direction: direction.to_owned(),
                        selector: selector.map(str::to_owned),
                        alternatives,
                    },
                )
                .is_some()
            {
                return Err(format!("duplicate frame {name}"));
            }
        }
        // A metadata-preserving sample is sufficient for these original
        // plain item arrays, then every actual item and count is checked.
        // Unknown keywords or any different item shape refuse at load.
        let startup = parse_json(STARTUP).map_err(|e| format!("startup: {e}"))?;
        let mut piecewise = BTreeMap::new();
        for (definition, member) in [
            ("CoverageV3", "entries"),
            ("UnavailableV3", "coverage"),
            ("BudgetExhaustedV3", "coverage"),
        ] {
            let shape = at(&startup, &["$defs", definition, "properties", member])
                .and_then(obj)
                .ok_or("piecewise array")?;
            if shape.get("type").and_then(text) != Some("array")
                || shape.keys().any(|key| {
                    ![
                        "type",
                        "items",
                        "minItems",
                        "maxItems",
                        "x-opensip-order",
                        "description",
                    ]
                    .contains(&key.as_str())
                })
                || shape.get("x-opensip-order").and_then(text) != Some("sequence")
            {
                return Err(format!("{definition}.{member}: unimplemented array shape"));
            }
            let item = shape.get("items").and_then(obj).ok_or("items")?;
            if item.len() != 1 {
                return Err("nonreference item shape".to_owned());
            }
            let item_ref = item
                .get("$ref")
                .and_then(text)
                .ok_or("item $ref")?
                .to_owned();
            let (id, pointer) = item_ref.split_once('#').ok_or("absolute item ref")?;
            registry
                .schema(id, pointer)
                .map_err(|e| format!("{item_ref}: {e:?}"))?;
            piecewise.insert(
                format!("{STARTUP_ID}#/$defs/{definition}"),
                Piecewise {
                    member: member.to_owned(),
                    item_ref,
                    min: number(shape.get("minItems"))?,
                    max: number(shape.get("maxItems"))?,
                },
            );
        }
        Ok(Self {
            carriers,
            frames,
            piecewise,
        })
    }
    fn payload(carriers: &Carriers, value: &J) -> Result<Payload, String> {
        match at(value, &["t"]).and_then(text) {
            Some("ref") => {
                // Validate the selected reference against the exact loaded
                // namespace, rather than treating an unknown record loosely.
                carriers.validate_type("payload", value)?;
                Ok(Payload::Record(
                    at(value, &["ref"])
                        .and_then(text)
                        .ok_or("payload ref")?
                        .to_owned(),
                ))
            }
            Some("extern") => {
                carriers.validate_type("payload", value)?;
                Ok(Payload::Extern(
                    at(value, &["schemaRef"])
                        .and_then(text)
                        .ok_or("schemaRef")?
                        .to_owned(),
                ))
            }
            _ => Err("unimplemented payload shape".to_owned()),
        }
    }
    /// Check only the envelope's closed members, direction and known frame.
    /// Sequence equality/overflow belongs to the session's direction counter.
    pub fn check_envelope(&self, value: &Value, direction: &str) -> Result<(String, u64), String> {
        let Value::Map(fields) = value else {
            return Err("envelope is not a map".to_owned());
        };
        let members = self.carriers.members("Rust3ProviderFrameV3");
        if fields.len() != members.len()
            || members
                .iter()
                .any(|(name, _)| field(fields, name).is_none())
        {
            return Err("envelope member set".to_owned());
        }
        for (name, shape) in &members {
            if name != "payload" {
                self.carriers
                    .check(shape, field(fields, name).ok_or("member")?, name)?;
            }
        }
        let Some(Value::Text(name)) = field(fields, "frameType") else {
            return Err("frameType".to_owned());
        };
        let shape = self.frames.get(name).ok_or("unknown frame")?;
        if shape.direction != direction
            || field(fields, "direction") != Some(&Value::Text(direction.to_owned()))
        {
            return Err("wrong frame direction".to_owned());
        }
        let Some(Value::Unsigned(sequence)) = field(fields, "sequence") else {
            return Err("sequence".to_owned());
        };
        Ok((name.clone(), *sequence))
    }
    /// Apply the original closed payload selected by the host's current
    /// phase and exact negotiated target-attribution token. This method does
    /// not negotiate tokens, check the table or establish contextual truth.
    pub fn check_payload(
        &self,
        name: &str,
        value: &Value,
        host_phase: &str,
        target_attribution: bool,
    ) -> Result<(), String> {
        let frame = self.frames.get(name).ok_or("unknown frame")?;
        let key = match frame.selector.as_deref() {
            None => String::new(),
            Some("host-phase") => host_phase.to_owned(),
            Some("negotiated-target-attribution-v2") => target_attribution.to_string(),
            _ => return Err("unimplemented selector".to_owned()),
        };
        match frame
            .alternatives
            .get(&key)
            .ok_or("no payload for host selector")?
        {
            Payload::Record(record) => self.carriers.check_record(record, value),
            Payload::Extern(schema) => match self.piecewise.get(schema) {
                Some(shape) => Self::check_piecewise(schema, value, shape),
                None => admit_extern(schema, value),
            },
        }
    }
    /// Census selection is immutable signed-session context. A selected
    /// CompleteV3 uses the existing structured schema owner with the
    /// source-checked metadata/item decomposition in census::Law. No field
    /// is dropped to turn the selected value into an inherited payload.
    pub(super) fn check_selected_payload(
        &self,
        name: &str,
        value: &Value,
        host_phase: &str,
        target_attribution: bool,
        census: bool,
    ) -> Result<(), String> {
        if census && name == "Complete" {
            super::census::Law::load()?.shape(value)
        } else {
            self.check_payload(name, value, host_phase, target_attribution)
        }
    }
    fn check_piecewise(schema: &str, value: &Value, shape: &Piecewise) -> Result<(), String> {
        let Value::Map(fields) = value else {
            return Err("payload map".to_owned());
        };
        let Some(Value::Array(items)) = field(fields, &shape.member) else {
            return Err("payload array".to_owned());
        };
        let count = items.len() as u64;
        if shape.min.is_some_and(|min| count < min) || shape.max.is_some_and(|max| count > max) {
            return Err("payload array count".to_owned());
        }
        let sample = Value::Map(
            fields
                .iter()
                .map(|(key, value)| {
                    (
                        key.clone(),
                        if key == &shape.member {
                            Value::Array(items.iter().take(1).cloned().collect())
                        } else {
                            value.clone()
                        },
                    )
                })
                .collect(),
        );
        admit_extern(schema, &sample)?;
        for item in items {
            admit_extern(&shape.item_ref, item)?;
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn wire(value: &J) -> Value {
        match value {
            J::Null => Value::Null,
            J::Bool(value) => Value::Bool(*value),
            J::Integer(value) => Value::Unsigned(u64::try_from(value.get()).unwrap()),
            J::String(value) => Value::Text(value.clone()),
            J::Array(values) => Value::Array(values.iter().map(wire).collect()),
            J::Object(values) => Value::Map(
                values
                    .iter()
                    .map(|(key, value)| (key.clone(), wire(value)))
                    .collect(),
            ),
        }
    }
    fn universe_accepted() -> Value {
        let fixture = parse_json(include_bytes!(
            "../../../tests/data/rust3-startup-shape.v1.json"
        ))
        .unwrap();
        wire(at(&fixture, &["universeAccepted"]).unwrap())
    }
    #[test]
    fn rust3_universe_accepted_shape_preserves_the_original_recursive_value() {
        let schemas = Rust3PayloadSchemas::load().unwrap();
        let value = universe_accepted();
        assert!(
            schemas
                .check_payload("UniverseAccepted", &value, "WAIT_UNIVERSE_ACCEPTED", false)
                .is_ok()
        );
    }
    #[test]
    fn wide_rust3_universe_shape_uses_the_wire_bound_without_an_extra_json_byte_cap() {
        let schemas = Rust3PayloadSchemas::load().unwrap();
        let value = universe_accepted();
        let Value::Map(fields) = &value else {
            unreachable!()
        };
        let universe = field(fields, "universe").unwrap();
        // The original selected schema admits arbitrary NFC component-name
        // keys, with DigestHex values. No semantic toolchain admission is
        // claimed by this shape-only wire control.
        let components = Value::Map(vec![("\0".repeat(700000), t(&"a".repeat(64)))]);
        let wide = with(
            &value,
            "universe",
            with(universe, "standardLibraryComponentDigests", components),
        );
        assert_eq!(
            opensip_identity::canonical_bytes(&carrier::to_json(&wide).unwrap()),
            Err(opensip_identity::CanonicalError::ByteLimit)
        );
        let raw = super::super::super::cbor::encode(&wide);
        assert!((raw.len() as u64) < super::super::super::MAX_FRAME_PAYLOAD_BYTES);
        let decoded =
            super::super::super::cbor::decode(&raw, super::super::super::cbor::Profile::Rust3, 32)
                .unwrap();
        let got = schemas.check_payload(
            "UniverseAccepted",
            &decoded,
            "WAIT_UNIVERSE_ACCEPTED",
            false,
        );
        assert!(
            got.is_ok(),
            "legal Rust3 CBOR shape exceeds only intermediate JSON bytes: {got:?}"
        );
        let bad_components = Value::Map(vec![("\0".repeat(700000), t(&"a".repeat(63)))]);
        let bad = with(
            &value,
            "universe",
            with(universe, "standardLibraryComponentDigests", bad_components),
        );
        assert!(
            schemas
                .check_payload("UniverseAccepted", &bad, "WAIT_UNIVERSE_ACCEPTED", false)
                .is_err(),
            "the full original schema must still reject the bad large-map value"
        );
        assert!(
            schemas
                .check_payload(
                    "UniverseAccepted",
                    &with(&wide, "extra", Value::Null),
                    "WAIT_UNIVERSE_ACCEPTED",
                    false
                )
                .is_err(),
            "the full original closed member set remains enforced"
        );
    }

    #[test]
    fn large_legal_rust3_wire_shape_is_not_capped_by_borrowed_schema_work_budget() {
        let schemas = Rust3PayloadSchemas::load().unwrap();
        let value = universe_accepted();
        let Value::Map(fields) = &value else {
            unreachable!()
        };
        let universe = field(fields, "universe").unwrap();
        // The old 64Mi-credit configuration budget cannot cover even two
        // structural scans of this legal key. The derived budget must cover
        // the selected schema over its full admitted wire-size range.
        let components = Value::Map(vec![("\0".repeat(33_554_433), t(&"a".repeat(64)))]);
        let value = with(
            &value,
            "universe",
            with(universe, "standardLibraryComponentDigests", components),
        );
        let raw = super::super::super::cbor::encode(&value);
        assert!((raw.len() as u64) < super::super::super::MAX_FRAME_PAYLOAD_BYTES);
        drop(value);
        let decoded =
            super::super::super::cbor::decode(&raw, super::super::super::cbor::Profile::Rust3, 7)
                .unwrap();
        let got = schemas.check_payload(
            "UniverseAccepted",
            &decoded,
            "WAIT_UNIVERSE_ACCEPTED",
            false,
        );
        assert!(
            got.is_ok(),
            "legal wire must not hit an unrelated schema work cap: {got:?}"
        );
    }

    #[test]
    fn structured_registry_admission_preserves_selected_owner_patterns_and_handles() {
        let registry = crate::schema_sources::registry().unwrap();
        for (id, selector) in [
            (
                "urn:opensip:product-v1:native:evidence-schemas:v2",
                "/$defs/CanonicalPath",
            ),
            ("opensip.product.symbol-census.1", "/$defs/LogicalPath"),
        ] {
            for path in [
                "src/main.rs",
                "src/../main.rs\n",
                "src/.\n/main.rs",
                "src/..\n/main.rs",
            ] {
                let value = J::String(path.to_owned());
                let raw = opensip_identity::canonical_bytes(&value).unwrap();
                let json_ok = registry
                    .schema(id, selector)
                    .unwrap()
                    .admit_json(&raw, SCHEMA_BUDGET)
                    .is_ok();
                let shape = registry
                    .schema(id, selector)
                    .unwrap()
                    .admit_value(&value, SCHEMA_BUDGET);
                assert_eq!(shape.is_ok(), json_ok, "{id} {path:?}");
                if let Ok(shape) = shape {
                    assert_eq!(shape.schema().schema_id(), id);
                    assert_eq!(shape.schema().selector(), selector);
                    assert_eq!(shape.value(), &value);
                }
            }
        }
        assert!(registry.schema(STARTUP_ID, "/$defs/NOT-SELECTED").is_err());
        let value = universe_accepted();
        let model = carrier::to_json(&value).unwrap();
        let shape = registry
            .schema(STARTUP_ID, "/$defs/UniverseAcceptedV3")
            .unwrap()
            .admit_value(&model, SCHEMA_BUDGET)
            .unwrap();
        assert_eq!(
            shape.schema().document_sha256(),
            opensip_identity::raw_sha256(STARTUP)
        );
        assert_eq!(shape.value(), &model);
    }
    fn t(s: &str) -> Value {
        Value::Text(s.to_owned())
    }
    fn map(fields: Vec<(&str, Value)>) -> Value {
        Value::Map(fields.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
    }
    fn with(value: &Value, key: &str, replacement: Value) -> Value {
        let Value::Map(fields) = value else {
            panic!("map");
        };
        let mut fields = fields.clone();
        match fields.iter_mut().find(|(k, _)| k == key) {
            Some((_, value)) => *value = replacement,
            None => fields.push((key.to_owned(), replacement)),
        };
        Value::Map(fields)
    }
    fn ack() -> Value {
        map(vec![
            ("protocolMajor", Value::Unsigned(3)),
            ("providerBuildId", t("provider")),
            ("rustCommitHash", t(&"a".repeat(40))),
            ("hostTriple", t("aarch64-apple-darwin")),
            ("targetTriple", t("aarch64-apple-darwin")),
            ("sysrootDigest", t(&"b".repeat(64))),
            (
                "capabilities",
                Value::Array(
                    [
                        "coverage-v3",
                        "fact-identity-fact2",
                        "plan-identity-plan2",
                        "source-identity-snapshot2",
                    ]
                    .map(t)
                    .to_vec(),
                ),
            ),
            (
                "identityVersions",
                map(vec![
                    ("snapshot", Value::Unsigned(2)),
                    ("plan", Value::Unsigned(2)),
                    ("fact", Value::Unsigned(2)),
                    ("coverage", Value::Unsigned(3)),
                ]),
            ),
        ])
    }
    fn candidate() -> Value {
        map(vec![
            ("candidateOrdinal", Value::Unsigned(0)),
            ("relation", t("file")),
            ("resolution", t("enumerated")),
            ("layer", t("inventory")),
            ("producer", t("rust-semantic")),
            ("producerVersion", t("provider")),
            ("schemaVersion", Value::Unsigned(1)),
            ("language", t("rust")),
            ("sourceUniverseId", t(&format!("sha256:{}", "a".repeat(64)))),
            ("targetUniverseId", t(&format!("sha256:{}", "b".repeat(64)))),
            ("confidenceMillionths", Value::Unsigned(1000000)),
            ("relationSchemaId", t("file-schema")),
            ("canonicalRelationPayload", Value::Bytes(vec![0xa0])),
            (
                "anchors",
                Value::Array(vec![map(vec![
                    ("kind", t("source-span")),
                    ("snapshotId", t(&format!("snapshot2:{}", "c".repeat(64)))),
                    ("path", t("main.rs")),
                    ("contentSha256", t(&"d".repeat(64))),
                    ("startByte", Value::Unsigned(0)),
                    ("endByte", Value::Unsigned(1)),
                    ("factId", Value::Null),
                ])]),
            ),
        ])
    }
    #[test]
    fn rust3_closed_envelope_preserves_protocol_direction_and_sequence_shape() {
        let schemas = Rust3PayloadSchemas::load().unwrap();
        assert_eq!(schemas.frames.len(), 26);
        let envelope = map(vec![
            ("protocolMajor", Value::Unsigned(3)),
            ("direction", t("worker-to-host")),
            ("sequence", Value::Unsigned(0)),
            ("frameType", t("HelloAck")),
            ("payload", ack()),
        ]);
        assert_eq!(
            schemas.check_envelope(&envelope, "worker-to-host"),
            Ok(("HelloAck".to_owned(), 0))
        );
        for (key, value) in [
            ("protocolMajor", Value::Unsigned(2)),
            ("direction", t("host-to-worker")),
            ("sequence", Value::Bool(false)),
            ("frameType", t("Hello")),
            ("frameType", t("unknown")),
            ("extra", Value::Null),
        ] {
            assert!(
                schemas
                    .check_envelope(&with(&envelope, key, value), "worker-to-host")
                    .is_err(),
                "{key}"
            );
        }
    }
    #[test]
    fn rust3_hello_ack_uses_the_selected_rust_identity_and_token_shapes() {
        let schemas = Rust3PayloadSchemas::load().unwrap();
        assert!(
            schemas
                .check_payload("HelloAck", &ack(), "WAIT_HELLO_ACK", false)
                .is_ok()
        );
        for (key, value) in [
            ("rustCommitHash", t(&"a".repeat(64))),
            ("protocolMajor", Value::Unsigned(2)),
            ("capabilities", Value::Array(vec![t("coverage-v3")])),
            ("extra", Value::Null),
        ] {
            assert!(
                schemas
                    .check_payload(
                        "HelloAck",
                        &with(&ack(), key, value),
                        "WAIT_HELLO_ACK",
                        false
                    )
                    .is_err(),
                "{key}"
            );
        }
    }
    #[test]
    fn rust3_fact_batch_variant_is_exact_and_each_count_bound_stays_closed() {
        let schemas = Rust3PayloadSchemas::load().unwrap();
        let base = map(vec![
            ("analysisOrdinal", Value::Unsigned(0)),
            ("stageId", t("stage")),
            ("batchIndex", Value::Unsigned(0)),
            ("candidates", Value::Array(vec![candidate()])),
        ]);
        assert!(
            schemas
                .check_payload("FactBatch", &base, "ANALYZING", false)
                .is_ok()
        );
        assert!(
            schemas
                .check_payload("FactBatch", &base, "ANALYZING", true)
                .is_err()
        );
        let v3 = with(
            &with(&base, "schemaVersion", Value::Unsigned(3)),
            "occupancyCompanions",
            Value::Array(Vec::new()),
        );
        assert!(
            schemas
                .check_payload("FactBatch", &v3, "ANALYZING", true)
                .is_ok()
        );
        assert!(
            schemas
                .check_payload("FactBatch", &v3, "ANALYZING", false)
                .is_err()
        );
        for count in [0, 4097] {
            let candidates = Value::Array(
                (0..count)
                    .map(|n| with(&candidate(), "candidateOrdinal", Value::Unsigned(n)))
                    .collect(),
            );
            assert!(
                schemas
                    .check_payload(
                        "FactBatch",
                        &with(&base, "candidates", candidates),
                        "ANALYZING",
                        false
                    )
                    .is_err(),
                "{count}"
            );
        }
        let bad = with(&candidate(), "anchors", Value::Array(Vec::new()));
        assert!(
            schemas
                .check_payload(
                    "FactBatch",
                    &with(&base, "candidates", Value::Array(vec![bad])),
                    "ANALYZING",
                    false
                )
                .is_err()
        );
    }
    #[test]
    fn rust3_phase_selected_unavailable_and_terminal_array_shapes_do_not_fall_back() {
        let schemas = Rust3PayloadSchemas::load().unwrap();
        let spent = map(vec![
            ("analysisOrdinal", Value::Unsigned(0)),
            ("triggerStageId", t("stage")),
            ("unit", t("items")),
            ("limit", Value::Unsigned(1)),
            ("observed", Value::Unsigned(2)),
            ("coverage", Value::Array(Vec::new())),
            (
                "coverageCommitment",
                t(&format!("sha256:{}", "a".repeat(64))),
            ),
        ]);
        assert!(
            schemas
                .check_payload("BudgetExhausted", &spent, "ANALYZING", false)
                .is_ok()
        );
        assert!(
            schemas
                .check_payload(
                    "BudgetExhausted",
                    &with(&spent, "coverage", Value::Null),
                    "ANALYZING",
                    false
                )
                .is_err()
        );
        let pre = map(vec![
            ("executionId", t("execution")),
            ("snapshotId", t(&format!("snapshot2:{}", "a".repeat(64)))),
            ("planId", t(&format!("plan2:{}", "b".repeat(64)))),
            ("reason", t("native-context-mismatch")),
            ("nativeContextId", t(&format!("sha256:{}", "c".repeat(64)))),
            (
                "recomputedNativeContextId",
                t(&format!("sha256:{}", "d".repeat(64))),
            ),
        ]);
        assert!(
            schemas
                .check_payload("Unavailable", &pre, "WAIT_NATIVE_CONTEXT_VERIFIED", false)
                .is_ok()
        );
        for phase in ["ANALYZING", "READY_ANALYZE", "START"] {
            assert!(
                schemas
                    .check_payload("Unavailable", &pre, phase, false)
                    .is_err(),
                "{phase}"
            );
        }
    }
}
