//! Selected Rust3 numeric policy and the Hello/OpenUniverse host builders.
//! The supplied descriptors, capability selection and native universe must
//! already be admitted by their owners. These builders check wire shape and
//! exact cross-frame joins; they grant no source or execution authority.
use super::super::super::{cbor::Value, ts2::carrier};
use opensip_identity::{JsonValue as J, digest_hex, parse_json, raw_sha256};
use std::collections::BTreeMap;

const HANDSHAKE: &[u8] =
    include_bytes!("../../../../../../schemas/sources/handshake-v1.schema.json");
const RPP: &[u8] = include_bytes!("../../../../data/rust-provider-protocol.v2.json");
const EXTRA: [(&str, u64); 8] = [
    ("maxDependencySourcePackages", 4096),
    ("maxDependencySourceEntries", 1_000_000),
    ("maxDependencySourceTotalBytes", 8_589_934_592),
    ("maxDependencySourceChunkBytes", 1_048_576),
    ("maxUnresolvedEdgesPerStage", 1_000_000),
    ("maxCfgSets", 4),
    ("maxExpansionRows", 1_000_000),
    ("maxGeneratedFileRows", 1_000_000),
];

#[derive(Debug, PartialEq, Eq)]
pub(super) enum Refusal {
    Law(String),
    Shape(String),
    Join(&'static str),
}
#[derive(Debug)]
pub(super) struct Policy {
    pub limits: BTreeMap<String, u64>,
}
fn object(j: &J) -> Result<&BTreeMap<String, J>, Refusal> {
    if let J::Object(v) = j {
        Ok(v)
    } else {
        Err(Refusal::Law("expected object".into()))
    }
}
fn at<'a>(v: &'a J, path: &[&str]) -> Result<&'a J, Refusal> {
    path.iter().try_fold(v, |v, k| {
        object(v)?
            .get(*k)
            .ok_or_else(|| Refusal::Law(format!("missing {k}")))
    })
}
fn number(v: &J) -> Result<u64, Refusal> {
    if let J::Integer(n) = v {
        u64::try_from(n.get()).map_err(|_| Refusal::Law("uint64".into()))
    } else {
        Err(Refusal::Law("uint64".into()))
    }
}
fn member<'a>(v: &'a Value, k: &str) -> Option<&'a Value> {
    if let Value::Map(v) = v {
        carrier::field(v, k)
    } else {
        None
    }
}
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn map(v: Vec<(&str, Value)>) -> Value {
    Value::Map(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}

impl Policy {
    pub(super) fn load() -> Result<Self, Refusal> {
        Self::from_sources(HANDSHAKE, RPP)
    }
    fn from_sources(handshake: &[u8], rpp: &[u8]) -> Result<Self, Refusal> {
        let h = parse_json(handshake).map_err(|e| Refusal::Law(format!("handshake: {e}")))?;
        let r = parse_json(rpp).map_err(|e| Refusal::Law(format!("RPP: {e}")))?;
        let definition = at(&h, &["$defs", "ProtocolLimitsV3"])?;
        if at(definition, &["additionalProperties"])? != &J::Bool(false) {
            return Err(Refusal::Law("limits closure".into()));
        }
        let J::Array(required) = at(definition, &["required"])? else {
            return Err(Refusal::Law("required array".into()));
        };
        let properties = object(at(definition, &["properties"])?)?;
        if required.len() != 32 || properties.len() != 32 {
            return Err(Refusal::Law("32 limits".into()));
        }
        let mut limits = BTreeMap::new();
        for key in required {
            let J::String(key) = key else {
                return Err(Refusal::Law("required name".into()));
            };
            let property = properties
                .get(key)
                .ok_or_else(|| Refusal::Law("required property".into()))?;
            let n = number(at(property, &["const"])?)?;
            if limits.insert(key.clone(), n).is_some() {
                return Err(Refusal::Law("duplicate limit".into()));
            }
        }
        let original = object(at(&r, &["limits"])?)?;
        if original.len() != 24 {
            return Err(Refusal::Law("24 retained limits".into()));
        }
        let mut expected = BTreeMap::new();
        for (k, v) in original {
            expected.insert(k.clone(), number(v)?);
        }
        for (k, v) in EXTRA {
            if expected.insert(k.into(), v).is_some() {
                return Err(Refusal::Law("successor overlap".into()));
            }
        }
        if limits != expected {
            return Err(Refusal::Law("retained/successor limit equality".into()));
        }
        Ok(Self { limits })
    }
    pub(super) fn limit(&self, key: &str) -> Result<u64, Refusal> {
        self.limits
            .get(key)
            .copied()
            .ok_or_else(|| Refusal::Law(format!("unselected limit {key}")))
    }
    pub(super) fn hello(
        &self,
        host_build_id: &str,
        identity: Value,
        capabilities: &[String],
    ) -> Result<Value, Refusal> {
        // Selection order is signed input. Never sort/deduplicate a bad row.
        if capabilities
            .windows(2)
            .any(|p| p[0].as_bytes() >= p[1].as_bytes())
        {
            return Err(Refusal::Join("capability selection order"));
        }
        let value = map(vec![
            ("protocolMajor", Value::Unsigned(3)),
            ("hostBuildId", t(host_build_id)),
            (
                "expectedProtocolContractSha256",
                t(&digest_hex(&raw_sha256(RPP))),
            ),
            ("expectedIdentity", identity),
            (
                "expectedCapabilities",
                Value::Array(capabilities.iter().map(|x| t(x)).collect()),
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
            (
                "limits",
                Value::Map(
                    self.limits
                        .iter()
                        .map(|(k, v)| (k.clone(), Value::Unsigned(*v)))
                        .collect(),
                ),
            ),
        ]);
        super::super::admit_extern(
            "opensip.product.provider-handshake.1#/$defs/HelloV3",
            &value,
        )
        .map_err(Refusal::Shape)?;
        Ok(value)
    }
    pub(super) fn open(&self, hello: &Value, input: Open) -> Result<Value, Refusal> {
        // The exact checked Hello is also checked on this boundary: a forged
        // expectedIdentity must not create a different lawful universe join.
        super::super::admit_extern("opensip.product.provider-handshake.1#/$defs/HelloV3", hello)
            .map_err(Refusal::Shape)?;
        if member(hello, "expectedProtocolContractSha256")
            != Some(&t(&digest_hex(&raw_sha256(RPP))))
        {
            return Err(Refusal::Join("protocol contract pin"));
        }
        let Some(Value::Map(identity)) = member(hello, "expectedIdentity") else {
            return Err(Refusal::Join("expected identity"));
        };
        for (k, v) in identity {
            if member(&input.universe, k) != Some(v) {
                return Err(Refusal::Join("Hello/universe identity"));
            }
        }
        let inputs =
            member(&input.universe, "resolvedInputs").ok_or(Refusal::Join("resolved inputs"))?;
        for key in ["dependencySourceSetId", "preparedOutputSetId"] {
            let a = member(inputs, key).ok_or(Refusal::Join("universe set id"))?;
            if member(&input.repository_resolution, key) != Some(a) {
                return Err(Refusal::Join("repository/universe set id"));
            }
        }
        let value = map(vec![
            ("executionId", t(&input.execution_id)),
            ("snapshotId", t(&input.snapshot_id)),
            ("planId", t(&input.plan_id)),
            ("planIntentCommitment", t(&input.plan_intent_commitment)),
            ("providerId", t("rust-semantic")),
            ("universe", input.universe),
            ("repositoryResolution", input.repository_resolution),
        ]);
        super::super::admit_extern(
            "opensip.product.provider-startup.1#/$defs/OpenUniverseV3",
            &value,
        )
        .map_err(Refusal::Shape)?;
        Ok(value)
    }
}
pub(super) struct Open {
    pub execution_id: String,
    pub snapshot_id: String,
    pub plan_id: String,
    pub plan_intent_commitment: String,
    pub universe: Value,
    pub repository_resolution: Value,
}

#[cfg(test)]
#[path = "policy_tests.rs"]
mod tests;
