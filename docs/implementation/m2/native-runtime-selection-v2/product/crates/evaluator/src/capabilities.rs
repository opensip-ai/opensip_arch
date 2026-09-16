//! The closed current CAP-MANIFEST-ID-V1 scalar/record/order gates. Encoding
//! admission grants no release custody, supported-platform or provider authority.
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::{String, ToString},
    vec::Vec,
};
use opensip_identity::{
    Cve1Error, JsonValue as V, decode_cve1, encode_cve1, parse_json, raw_sha256,
};
const REGISTRY: &[u8] = include_bytes!("capability-registry.json");
const DOMAIN: &[u8] = b"opensip.capability-manifest.v1\0";
/// An admitted capability encoding. Its fields cannot be constructed or
/// deserialized independently of the closed gates. This is not a replay token.
/// ```compile_fail
/// use opensip_evaluator::CapabilityManifest;
/// let forged = CapabilityManifest {
///     identity: [0; 32], value: opensip_identity::JsonValue::Null,
///     relations: Vec::new(),
/// };
/// ```
pub struct CapabilityManifest {
    identity: [u8; 32],
    value: V,
    relations: Vec<String>,
}
impl CapabilityManifest {
    pub fn identity(&self) -> [u8; 32] {
        self.identity
    }
    pub fn value(&self) -> &V {
        &self.value
    }
    pub fn relations(&self) -> &[String] {
        &self.relations
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CapabilityRefusal {
    causes: Vec<String>,
    relations: Vec<String>,
}
impl CapabilityRefusal {
    pub fn causes(&self) -> &[String] {
        &self.causes
    }
    pub fn relations(&self) -> &[String] {
        &self.relations
    }
}
fn refusal(cause: String) -> CapabilityRefusal {
    CapabilityRefusal {
        causes: alloc::vec![cause],
        relations: Vec::new(),
    }
}
fn codec_name(e: Cve1Error) -> &'static str {
    match e {
        Cve1Error::Truncated => "CVE1_TRUNCATED",
        Cve1Error::TrailingBytes => "CVE1_TRAILING_BYTES",
        Cve1Error::Tag => "CVE1_TAG",
        Cve1Error::NegativeRange => "CVE1_NEGATIVE_RANGE",
        Cve1Error::Utf8 => "CVE1_UTF8",
        Cve1Error::NotNfc => "CVE1_NOT_NFC",
        Cve1Error::MapKey => "CVE1_MAP_KEY",
        Cve1Error::MapOrder => "CVE1_MAP_ORDER",
        Cve1Error::CountBound => "CVE1_COUNT_BOUND",
        Cve1Error::DepthBound => "CVE1_DEPTH_BOUND",
        Cve1Error::LengthBound => "CVE1_LENGTH_BOUND",
    }
}
fn object(v: &V) -> Option<&BTreeMap<String, V>> {
    if let V::Object(o) = v { Some(o) } else { None }
}
fn array(v: &V) -> Option<&[V]> {
    if let V::Array(a) = v { Some(a) } else { None }
}
fn text(v: &V) -> Option<&str> {
    if let V::String(s) = v { Some(s) } else { None }
}
// Accessors here operate only on this immutable, source-pinned registry. No
// caller chooses its rows, key sets, vocabularies or ladders.
fn field<'a>(v: &'a V, k: &str) -> &'a V {
    object(v)
        .and_then(|o| o.get(k))
        .expect("embedded capability registry field")
}
fn registry_array(v: &V) -> &[V] {
    array(v).expect("embedded capability registry array")
}
fn registry_text(v: &V) -> &str {
    text(v).expect("embedded capability registry string")
}
struct Gates {
    registry: V,
    causes: BTreeSet<String>,
    relations: BTreeSet<String>,
}
impl Gates {
    fn cause(&mut self, s: String) {
        self.causes.insert(s);
    }
    fn scalar_type(&mut self, name: &str, field: &str) {
        self.cause(format!("capability.adm-type:{name}.{field}"))
    }
    fn closed<'a>(&mut self, record: &'a V, name: &str) -> Option<&'a BTreeMap<String, V>> {
        let want = registry_array(field(
            field(field(&self.registry, "recordShape"), name),
            "requiredKeys",
        ));
        let Some(record) = object(record) else {
            self.cause(format!("capability.adm-closed:{name}"));
            return None;
        };
        if record.len() != want.len() || want.iter().any(|v| !record.contains_key(registry_text(v)))
        {
            self.cause(format!("capability.adm-closed:{name}"));
            return None;
        }
        let strings: &[&str] = match name {
            "ProviderCapability" => &[
                "providerId",
                "language",
                "providerVersionSource",
                "toolchainIdentitySource",
            ],
            "AbsentCapability" => &["providerId", "language", "deficiency", "coverageState"],
            _ => &[],
        };
        let mut valid = true;
        for key in strings {
            if record.get(*key).and_then(text).is_none() {
                self.scalar_type(name, key);
                valid = false
            }
        }
        for key in ["platformIds", "relationIds"] {
            if record.get(key).is_some_and(|v| array(v).is_none()) {
                self.scalar_type(name, key);
                valid = false
            }
        }
        if name == "ProviderCapability" && record.get("relations").and_then(object).is_none() {
            self.scalar_type(name, "relations");
            valid = false
        }
        valid.then_some(record)
    }
    fn member(&self, registry: &str, value: &str) -> bool {
        registry_array(field(
            field(field(&self.registry, "registries"), registry),
            "members",
        ))
        .iter()
        .any(|v| text(v) == Some(value))
    }
    fn order(&mut self, values: &[V], label: &str) {
        let Some(strings) = values.iter().map(text).collect::<Option<Vec<_>>>() else {
            return;
        };
        if strings
            .windows(2)
            .any(|w| w[0].as_bytes() >= w[1].as_bytes())
        {
            self.cause(format!("capability.adm-order:{label}"))
        }
    }
    fn finish(self, value: V, raw: &[u8]) -> Result<CapabilityManifest, CapabilityRefusal> {
        let relations = self.relations.into_iter().collect();
        if !self.causes.is_empty() {
            return Err(CapabilityRefusal {
                causes: self.causes.into_iter().collect(),
                relations,
            });
        }
        let mut preimage = Vec::with_capacity(DOMAIN.len() + raw.len());
        preimage.extend_from_slice(DOMAIN);
        preimage.extend_from_slice(raw);
        Ok(CapabilityManifest {
            identity: raw_sha256(&preimage),
            value,
            relations,
        })
    }
}
/// Current manifest admission over the exact retained CVE1 bytes. No sorting,
/// normalization, platform support inference or release-profile join is applied.
pub fn admit_capability_manifest(raw: &[u8]) -> Result<CapabilityManifest, CapabilityRefusal> {
    let value = decode_cve1(raw)
        .map_err(|e| refusal(format!("capability.cve1-decode:{}", codec_name(e))))?;
    let registry = parse_json(REGISTRY).expect("embedded capability registry JSON");
    let mut gates = Gates {
        registry,
        causes: BTreeSet::new(),
        relations: BTreeSet::new(),
    };
    let Some(root) = object(&value) else {
        gates.closed(&value, "CapabilityManifestV1");
        return gates.finish(value, raw);
    };
    if !matches!(root.get("schemaVersion"), Some(V::Integer(_))) {
        gates.scalar_type("CapabilityManifestV1", "schemaVersion")
    }
    if root.get("profile").and_then(text).is_none() {
        gates.scalar_type("CapabilityManifestV1", "profile")
    }
    for key in ["providers", "coverageForAbsent"] {
        if root.get(key).and_then(array).is_none() {
            gates.scalar_type("CapabilityManifestV1", key)
        }
    }
    if gates.closed(&value, "CapabilityManifestV1").is_none() || !gates.causes.is_empty() {
        return gates.finish(value, raw);
    }
    let providers = array(&root["providers"]).expect("typed providers");
    let absent = array(&root["coverageForAbsent"]).expect("typed absent collection");
    for value in providers {
        let Some(provider) = gates.closed(value, "ProviderCapability") else {
            continue;
        };
        for (relation, rung) in object(&provider["relations"]).expect("typed relation map") {
            gates.relations.insert(relation.clone());
            if !gates.member("RELATION-DOMAIN-V2", relation) {
                gates.cause(format!("capability.adm-domain:relation:{relation}"));
                continue;
            }
            let Some(rung) = text(rung) else {
                gates.scalar_type("ProviderCapability", "relations.value");
                continue;
            };
            let ladder = field(
                field(
                    field(
                        field(&gates.registry, "registries"),
                        "RELATION-LADDER-DOMAIN-V2",
                    ),
                    "ladders",
                ),
                relation,
            );
            if !registry_array(ladder).iter().any(|v| text(v) == Some(rung)) {
                gates.cause(format!("capability.adm-domain:rung:{relation}@{rung}"))
            }
        }
        let platforms = array(&provider["platformIds"]).expect("typed platform array");
        for platform in platforms {
            let Some(platform) = text(platform) else {
                gates.scalar_type("ProviderCapability", "platformIds[]");
                continue;
            };
            if !gates.member("PLATFORM-ID-DOMAIN-V1", platform) {
                gates.cause(format!("capability.adm-domain:platformId:{platform}"))
            }
        }
        gates.order(platforms, "platformIds");
    }
    for value in absent {
        let Some(record) = gates.closed(value, "AbsentCapability") else {
            continue;
        };
        let relations = array(&record["relationIds"]).expect("typed relation array");
        for relation in relations {
            let Some(relation) = text(relation) else {
                gates.scalar_type("AbsentCapability", "relationIds[]");
                continue;
            };
            gates.relations.insert(relation.into());
            if !gates.member("RELATION-DOMAIN-V2", relation) {
                gates.cause(format!("capability.adm-domain:relation:{relation}"))
            }
        }
        gates.order(relations, "relationIds");
        for (key, domain) in [
            ("deficiency", "DEFICIENCY-DOMAIN-V1"),
            ("coverageState", "COVERAGE-STATE-DOMAIN-V1"),
        ] {
            let s = text(&record[key]).expect("typed scalar");
            if !gates.member(domain, s) {
                gates.cause(format!("capability.adm-domain:{key}:{s}"))
            }
        }
    }
    let provider_ids = providers
        .iter()
        .filter_map(|v| object(v).and_then(|o| o.get("providerId")).and_then(text))
        .map(|s| V::String(s.to_string()))
        .collect::<Vec<_>>();
    gates.order(&provider_ids, "providers");
    let mut absent_keys = Vec::new();
    for row in absent {
        if object(row).is_some() {
            let encoded = encode_cve1(row).expect("subset of decoded CVE1 value");
            let key = encoded
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            absent_keys.push(V::String(key));
        }
    }
    gates.order(&absent_keys, "coverageForAbsent");
    if encode_cve1(&value).expect("decoded CVE1 value") != raw {
        gates.cause("capability.adm-order:not-canonical-cve1".into())
    }
    gates.finish(value, raw)
}

#[cfg(test)]
mod tests {
    use super::*;
    const GOLDEN: &[u8] = include_bytes!("../tests/fixtures/capability-manifest.golden.cve1");
    fn map(v: &mut V) -> &mut BTreeMap<String, V> {
        let V::Object(o) = v else {
            panic!("fixture object")
        };
        o
    }
    fn provider(v: &mut V) -> &mut BTreeMap<String, V> {
        let V::Array(a) = map(v).get_mut("providers").unwrap() else {
            panic!("fixture providers")
        };
        map(&mut a[0])
    }
    fn causes(value: &V) -> Vec<String> {
        match admit_capability_manifest(&encode_cve1(value).unwrap()) {
            Err(e) => e.causes,
            Ok(_) => panic!("must refuse"),
        }
    }
    #[test]
    fn inherited_golden_has_exact_published_identity() {
        let manifest = admit_capability_manifest(GOLDEN).unwrap();
        assert_eq!(
            opensip_identity::digest_hex(&manifest.identity()),
            "508f24c718a0564c52fe18a1e6a5308d53bdd6012a50ad186ffbc208bb18881b"
        );
        assert_eq!(manifest.value(), &decode_cve1(GOLDEN).unwrap());
        assert!(manifest.relations().iter().any(|r| r == "clones"));
    }
    #[test]
    fn malformed_roots_and_mixed_scalar_collections_are_structured_refusals() {
        for value in [V::Null, V::Bool(true), V::Array(Vec::new())] {
            assert_eq!(
                causes(&value),
                alloc::vec!["capability.adm-closed:CapabilityManifestV1".to_string()]
            );
        }
        for wrong in [
            V::Null,
            V::Bool(true),
            V::Array(Vec::new()),
            V::Object(BTreeMap::new()),
        ] {
            let mut value = decode_cve1(GOLDEN).unwrap();
            provider(&mut value).insert(
                "platformIds".into(),
                V::Array(alloc::vec![V::String("all-supported".into()), wrong]),
            );
            assert_eq!(
                causes(&value),
                alloc::vec!["capability.adm-type:ProviderCapability.platformIds[]".to_string()]
            );
        }
    }
    #[test]
    fn open_values_and_inherited_platform_domain_are_not_product_promises() {
        let mut value = decode_cve1(GOLDEN).unwrap();
        map(&mut value).insert(
            "schemaVersion".into(),
            V::Integer(opensip_identity::JsonInteger::new(2).unwrap()),
        );
        map(&mut value).insert("profile".into(), V::String("custody-is-separate".into()));
        provider(&mut value).insert("language".into(), V::String("cobol".into()));
        provider(&mut value).insert(
            "platformIds".into(),
            V::Array(alloc::vec![V::String("windows-x86_64-msvc".into())]),
        );
        assert!(admit_capability_manifest(&encode_cve1(&value).unwrap()).is_ok());
        map(&mut value).insert("schemaVersion".into(), V::Bool(true));
        assert!(
            causes(&value)
                .contains(&"capability.adm-type:CapabilityManifestV1.schemaVersion".into())
        );
    }
    #[test]
    fn relation_specific_ladder_and_string_collection_order_are_enforced() {
        let mut value = decode_cve1(GOLDEN).unwrap();
        provider(&mut value).insert(
            "relations".into(),
            V::Object(BTreeMap::from([(
                "declares".into(),
                V::String("resolved-callee".into()),
            )])),
        );
        assert!(
            causes(&value).contains(&"capability.adm-domain:rung:declares@resolved-callee".into())
        );
        let mut value = decode_cve1(GOLDEN).unwrap();
        provider(&mut value).insert(
            "platformIds".into(),
            V::Array(alloc::vec![
                V::String("all-supported".into()),
                V::String("all-supported".into())
            ]),
        );
        assert!(causes(&value).contains(&"capability.adm-order:platformIds".into()));
    }
}
