//! Dependency wire frames from C4's admitted set and retained file manifests.
//! Native H identities and raw wire manifest digests are different recipes.
//! This checks their joins, not acquisition, set admission or byte custody.
use super::super::super::{
    cbor::{self, Value},
    manifest_digest,
    ts2::carrier::Carriers,
};
use super::{policy::Policy, schedule};
use opensip_identity::{JsonValue as J, digest_hex, hash_canonical_value, parse_json};
use std::collections::BTreeMap;

#[derive(Debug, PartialEq, Eq)]
pub(super) enum Refusal {
    Policy(super::policy::Refusal),
    Shape(String),
    Join(&'static str),
    Bound(&'static str),
    Arithmetic,
}
impl From<super::policy::Refusal> for Refusal {
    fn from(v: super::policy::Refusal) -> Self {
        Self::Policy(v)
    }
}
pub(super) struct Input<'a> {
    pub set: &'a J,
    pub manifests: &'a BTreeMap<String, J>,
    /// Exact OpenUniverse.repositoryResolution.dependencySourceSetId.
    pub set_id: &'a str,
}
pub(super) struct Built {
    pub manifest: Value,
    pub seal: Value,
    pub bytes: u64,
    pub chunks: u64,
}
fn field<'a>(v: &'a J, k: &str) -> Result<&'a J, Refusal> {
    let J::Object(v) = v else {
        return Err(Refusal::Join("object"));
    };
    v.get(k).ok_or(Refusal::Join("missing member"))
}
fn text(v: &J) -> Result<&str, Refusal> {
    if let J::String(v) = v {
        Ok(v)
    } else {
        Err(Refusal::Join("text"))
    }
}
fn array(v: &J) -> Result<&[J], Refusal> {
    if let J::Array(v) = v {
        Ok(v)
    } else {
        Err(Refusal::Join("array"))
    }
}
fn number(v: &J) -> Result<u64, Refusal> {
    if let J::Integer(v) = v {
        u64::try_from(v.get()).map_err(|_| Refusal::Arithmetic)
    } else {
        Err(Refusal::Join("uint64"))
    }
}
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn map(v: Vec<(&str, Value)>) -> Value {
    Value::Map(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn head(n: u64) -> u64 {
    match n {
        0..=23 => 1,
        24..=255 => 2,
        256..=65_535 => 3,
        65_536..=4_294_967_295 => 5,
        _ => 9,
    }
}
fn native_hash(domain: &str, v: &J) -> Result<String, Refusal> {
    hash_canonical_value(domain, v)
        .map(|h| digest_hex(&h))
        .map_err(|e| Refusal::Shape(format!("native H: {e}")))
}
fn package_key(package: &J) -> Result<String, Refusal> {
    Ok(format!(
        "{} {} {}",
        text(field(package, "name")?)?,
        text(field(package, "version")?)?,
        text(field(package, "sourceId")?)?
    ))
}
fn wire_entry(key: &str, row: &J) -> Result<Value, Refusal> {
    Ok(map(vec![
        ("packageKey", t(key)),
        ("path", t(text(field(row, "path")?)?)),
        (
            "byteLength",
            Value::Unsigned(number(field(row, "byteLength")?)?),
        ),
        ("contentSha256", t(text(field(row, "contentSha256")?)?)),
    ]))
}
fn selected_manifest<'a>(input: &'a Input<'_>, package: &J) -> Result<&'a J, Refusal> {
    input
        .manifests
        .get(text(field(package, "fileManifestSha256")?)?)
        .ok_or(Refusal::Join("missing retained file manifest"))
}

pub(super) fn build(policy: &Policy, input: &Input<'_>, sequence: u64) -> Result<Built, Refusal> {
    let packages = array(field(input.set, "packages")?)?;
    if u64::try_from(packages.len()).map_err(|_| Refusal::Arithmetic)?
        > policy.limit("maxDependencySourcePackages")?
    {
        return Err(Refusal::Bound("dependency packages"));
    }
    if input.set_id
        != format!(
            "sha256:{}",
            native_hash("native.dependency-source-set.v1", input.set)?
        )
    {
        return Err(Refusal::Join("dependency set identity"));
    }
    let carriers = Carriers::load("Rust3").map_err(Refusal::Shape)?;
    let key_shape = parse_json(br#"{"t":"ref","ref":"Rust3PackageKey"}"#)
        .map_err(|e| Refusal::Shape(e.to_string()))?;
    let path_shape = parse_json(br#"{"t":"ref","ref":"Rust3DependencySourcePath"}"#)
        .map_err(|e| Refusal::Shape(e.to_string()))?;
    let digest_shape = parse_json(br#"{"t":"ref","ref":"Rust3DigestHex"}"#)
        .map_err(|e| Refusal::Shape(e.to_string()))?;
    let maximum = policy.limit("maxDependencySourceChunkBytes")?;
    let frame_max = policy.limit("maxFramePayloadBytes")?;
    let probe = map(vec![
        ("dependencySourceSetId", t(input.set_id)),
        ("manifestSha256", t(&"0".repeat(64))),
        ("entries", Value::Null),
    ]);
    let wrapper = cbor::encoded_length(&probe)
        .and_then(|n| n.checked_sub(1))
        .ok_or(Refusal::Arithmetic)?;
    let mut count = 0_u64;
    let mut bytes = 0_u64;
    let mut chunks = 0_u64;
    let mut entries_length = 0_u64;
    let mut previous = None;
    for package in packages {
        let tuple = (
            text(field(package, "name")?)?,
            text(field(package, "version")?)?,
            text(field(package, "sourceId")?)?,
        );
        if previous.is_some_and(|p| p >= tuple) {
            return Err(Refusal::Join("dependency package order"));
        }
        previous = Some(tuple);
        let key = package_key(package)?;
        carriers
            .check(&key_shape, &t(&key), "packageKey")
            .map_err(Refusal::Shape)?;
        let manifest = selected_manifest(input, package)?;
        let rows = array(manifest)?;
        let file_count = u64::try_from(rows.len()).map_err(|_| Refusal::Arithmetic)?;
        if number(field(package, "fileCount")?)? != file_count {
            return Err(Refusal::Join("dependency file count"));
        }
        count = count.checked_add(file_count).ok_or(Refusal::Arithmetic)?;
        if count > policy.limit("maxDependencySourceEntries")? {
            return Err(Refusal::Bound("dependency entries"));
        }
        let mut package_bytes = 0_u64;
        let mut previous_path = None;
        for row in rows {
            let J::Object(fields) = row else {
                return Err(Refusal::Join("file manifest row"));
            };
            if fields.len() != 3 {
                return Err(Refusal::Join("file manifest row closure"));
            }
            let path = text(field(row, "path")?)?;
            if previous_path.is_some_and(|p| p >= path) {
                return Err(Refusal::Join("dependency path order"));
            }
            previous_path = Some(path);
            carriers
                .check(&path_shape, &t(path), "path")
                .map_err(Refusal::Shape)?;
            carriers
                .check(
                    &digest_shape,
                    &t(text(field(row, "contentSha256")?)?),
                    "contentSha256",
                )
                .map_err(Refusal::Shape)?;
            let length = number(field(row, "byteLength")?)?;
            package_bytes = package_bytes
                .checked_add(length)
                .ok_or(Refusal::Arithmetic)?;
            bytes = bytes.checked_add(length).ok_or(Refusal::Arithmetic)?;
            if bytes > policy.limit("maxDependencySourceTotalBytes")? {
                return Err(Refusal::Bound("dependency bytes"));
            }
            chunks = chunks
                .checked_add(
                    schedule::chunk_count(length, maximum).map_err(|_| Refusal::Arithmetic)?,
                )
                .ok_or(Refusal::Arithmetic)?;
            // One small row probe at a time, never an allocated wire array
            // proportional to a count whose envelope has not yet fitted.
            entries_length = entries_length
                .checked_add(
                    cbor::encoded_length(&wire_entry(&key, row)?).ok_or(Refusal::Arithmetic)?,
                )
                .ok_or(Refusal::Arithmetic)?;
            let partial = wrapper
                .checked_add(head(count))
                .and_then(|n| n.checked_add(entries_length))
                .ok_or(Refusal::Arithmetic)?;
            if schedule::envelope_length_for_payload(sequence, "DependencySourceManifest", partial)
                .map_err(|_| Refusal::Arithmetic)?
                > frame_max
            {
                return Err(Refusal::Bound("dependency manifest envelope"));
            }
        }
        if package_bytes != number(field(package, "totalBytes")?)? {
            return Err(Refusal::Join("dependency package bytes"));
        }
        if native_hash("native.dependency-file-manifest.v1", manifest)?
            != text(field(package, "fileManifestSha256")?)?
        {
            return Err(Refusal::Join("dependency file manifest H"));
        }
    }
    let length = wrapper
        .checked_add(head(count))
        .and_then(|n| n.checked_add(entries_length))
        .ok_or(Refusal::Arithmetic)?;
    if schedule::envelope_length_for_payload(sequence, "DependencySourceManifest", length)
        .map_err(|_| Refusal::Arithmetic)?
        > frame_max
    {
        return Err(Refusal::Bound("dependency manifest envelope"));
    }
    let mut values = Vec::new();
    for package in packages {
        let key = package_key(package)?;
        for row in array(selected_manifest(input, package)?)? {
            values.push(wire_entry(&key, row)?);
        }
    }
    let values = Value::Array(values);
    let digest = manifest_digest(&values);
    let manifest = map(vec![
        ("dependencySourceSetId", t(input.set_id)),
        ("entries", values),
        ("manifestSha256", t(&digest)),
    ]);
    let seal = map(vec![
        ("dependencySourceSetId", t(input.set_id)),
        ("entryCount", Value::Unsigned(count)),
        ("manifestSha256", t(&digest)),
        ("totalBytes", Value::Unsigned(bytes)),
        ("totalChunkCount", Value::Unsigned(chunks)),
    ]);
    for (root, value) in [
        ("DependencySourceManifestV3", &manifest),
        ("DependencySourceSealV3", &seal),
    ] {
        super::super::admit_extern(
            &format!("urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/{root}"),
            value,
        )
        .map_err(Refusal::Shape)?;
    }
    Ok(Built {
        manifest,
        seal,
        bytes,
        chunks,
    })
}

/// The parent sender selects this exact entry from its freshly reconstructed
/// immutable manifest, then compares the realized envelope to its frozen slot.
pub(super) fn chunk(
    policy: &Policy,
    set_id: &str,
    entry: &Value,
    index: u64,
    offset: u64,
    bytes: Vec<u8>,
) -> Result<Value, Refusal> {
    let Value::Map(fields) = entry else {
        return Err(Refusal::Join("dependency entry"));
    };
    let get = |k| {
        super::super::super::ts2::carrier::field(fields, k)
            .ok_or(Refusal::Join("dependency entry field"))
    };
    let Value::Unsigned(length) = get("byteLength")? else {
        return Err(Refusal::Join("dependency length"));
    };
    let maximum = policy.limit("maxDependencySourceChunkBytes")?;
    let start = index.checked_mul(maximum).ok_or(Refusal::Arithmetic)?;
    if start != offset || start >= *length {
        return Err(Refusal::Join("dependency chunk coordinates"));
    }
    if u64::try_from(bytes.len()).map_err(|_| Refusal::Arithmetic)?
        != (*length - start).min(maximum)
    {
        return Err(Refusal::Join("dependency greedy chunk length"));
    }
    let value = map(vec![
        ("dependencySourceSetId", t(set_id)),
        ("packageKey", get("packageKey")?.clone()),
        ("path", get("path")?.clone()),
        ("chunkIndex", Value::Unsigned(index)),
        ("byteOffset", Value::Unsigned(offset)),
        ("bytes", Value::Bytes(bytes)),
    ]);
    Carriers::load("Rust3")
        .map_err(Refusal::Shape)?
        .check_record("Rust3DependencySourceChunkV3", &value)
        .map_err(Refusal::Shape)?;
    Ok(value)
}

#[cfg(test)]
#[path = "dependency_tests.rs"]
mod tests;
