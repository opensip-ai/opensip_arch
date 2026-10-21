//! Inert prepared-output frames for the complete set selected by C4.
//! C4 owns selection, freshness and read authority. No row is filtered here:
//! failed rows still bind the selected set and are transferred as declared;
//! they grant no worker read/consumption authority.
use super::super::super::{
    cbor::{self, Value},
    manifest_digest,
    ts2::carrier::Carriers,
};
use super::{policy::Policy, schedule};
use opensip_identity::{JsonValue as J, digest_hex, hash_canonical_value, parse_json};

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
    pub set_id: &'a str,
    pub plan_id: &'a str,
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
fn size(n: usize) -> Result<u64, Refusal> {
    u64::try_from(n).map_err(|_| Refusal::Arithmetic)
}
fn string_length(v: &str) -> Result<u64, Refusal> {
    let n = size(v.len())?;
    head(n).checked_add(n).ok_or(Refusal::Arithmetic)
}
/// Exact size over the borrowed native descriptor, without cloning its trees
/// or encoding strings. The admitted native JSON domain has no bytes/floats.
fn wire_length(v: &J) -> Result<u64, Refusal> {
    match v {
        J::Null | J::Bool(_) => Ok(1),
        J::Integer(_) => Ok(head(number(v)?)),
        J::String(v) => string_length(v),
        J::Array(v) => v.iter().try_fold(head(size(v.len())?), |n, v| {
            n.checked_add(wire_length(v)?).ok_or(Refusal::Arithmetic)
        }),
        J::Object(v) => v.iter().try_fold(head(size(v.len())?), |n, (k, v)| {
            n.checked_add(string_length(k)?)
                .and_then(|n| n.checked_add(wire_length(v).ok()?))
                .ok_or(Refusal::Arithmetic)
        }),
    }
}
fn wire(v: &J) -> Result<Value, Refusal> {
    Ok(match v {
        J::Null => Value::Null,
        J::Bool(v) => Value::Bool(*v),
        J::Integer(_) => Value::Unsigned(number(v)?),
        J::String(v) => t(v),
        J::Array(v) => Value::Array(v.iter().map(wire).collect::<Result<_, _>>()?),
        J::Object(v) => Value::Map(
            v.iter()
                .map(|(k, v)| Ok((k.clone(), wire(v)?)))
                .collect::<Result<_, Refusal>>()?,
        ),
    })
}
fn entry(row: &J, ordinal: u64, plan_row: Value) -> Result<Value, Refusal> {
    let blob = field(row, "blob")?;
    let sha = text(field(blob, "sha256")?)?;
    let length = number(field(blob, "byteLength")?)?;
    Ok(map(vec![
        ("outputOrdinal", Value::Unsigned(ordinal)),
        ("kind", t(text(field(row, "kind")?)?)),
        ("planRow", plan_row),
        (
            "logicalPath",
            t(&format!(".opensip/prepared/v3/{ordinal}-{sha}.blob")),
        ),
        ("blobByteLength", Value::Unsigned(length)),
        ("blobSha256", t(sha)),
        ("contentByteLength", Value::Unsigned(length)),
        ("contentSha256", t(sha)),
    ]))
}

pub(super) fn build(policy: &Policy, input: &Input<'_>, sequence: u64) -> Result<Built, Refusal> {
    let J::Array(rows) = field(input.set, "rows")? else {
        return Err(Refusal::Join("prepared rows"));
    };
    let count = size(rows.len())?;
    if !policy.entries_fit("maxPreparedOutputEntries", count)? {
        return Err(Refusal::Bound("prepared entries"));
    }
    let identity = hash_canonical_value("native.prepared-output-set.v3", input.set)
        .map_err(|e| Refusal::Shape(format!("prepared H: {e}")))?;
    if input.set_id != format!("sha256:{}", digest_hex(&identity)) {
        return Err(Refusal::Join("prepared set identity"));
    }
    let carriers = Carriers::load("Rust3").map_err(Refusal::Shape)?;
    carriers
        .check(
            &parse_json(br#"{"t":"ref","ref":"Rust3PlanId2"}"#)
                .map_err(|e| Refusal::Shape(e.to_string()))?,
            &t(input.plan_id),
            "planId",
        )
        .map_err(Refusal::Shape)?;
    let mut bytes = 0_u64;
    let mut chunks = 0_u64;
    let mut entries_length = head(count);
    for (ordinal, row) in rows.iter().enumerate() {
        let kind = text(field(row, "kind")?)?;
        if ![
            "build-script-directives",
            "macro-expansion",
            "generated-file",
        ]
        .contains(&kind)
        {
            return Err(Refusal::Join("non-inert prepared row"));
        }
        let blob = field(row, "blob")?;
        if kind == "generated-file" && field(field(row, "generated")?, "blob")? != blob {
            return Err(Refusal::Join("generated blob equality"));
        }
        let length = number(field(blob, "byteLength")?)?;
        bytes = bytes.checked_add(length).ok_or(Refusal::Arithmetic)?;
        if bytes > policy.limit("maxPreparedOutputTotalBlobBytes")? {
            return Err(Refusal::Bound("prepared blob bytes"));
        }
        chunks = chunks
            .checked_add(
                schedule::chunk_count(length, policy.limit("maxPreparedOutputChunkBytes")?)
                    .map_err(|_| Refusal::Arithmetic)?,
            )
            .ok_or(Refusal::Arithmetic)?;
        let probe = entry(row, size(ordinal)?, Value::Null)?;
        let length = cbor::encoded_length(&probe)
            .and_then(|n| n.checked_sub(1))
            .and_then(|n| n.checked_add(wire_length(row).ok()?))
            .ok_or(Refusal::Arithmetic)?;
        entries_length = entries_length
            .checked_add(length)
            .ok_or(Refusal::Arithmetic)?;
    }
    let probe = map(vec![
        ("planId", t(input.plan_id)),
        ("manifestSha256", t(&"0".repeat(64))),
        ("entries", Value::Null),
    ]);
    let payload = cbor::encoded_length(&probe)
        .and_then(|n| n.checked_sub(1))
        .and_then(|n| n.checked_add(entries_length))
        .ok_or(Refusal::Arithmetic)?;
    let full = schedule::envelope_length_for_payload(sequence, "PreparedOutputManifest", payload)
        .map_err(|_| Refusal::Arithmetic)?;
    if full > policy.limit("maxFramePayloadBytes")? {
        return Err(Refusal::Bound("prepared manifest envelope"));
    }
    let values = Value::Array(
        rows.iter()
            .enumerate()
            .map(|(ordinal, row)| entry(row, size(ordinal)?, wire(row)?))
            .collect::<Result<_, _>>()?,
    );
    let digest = manifest_digest(&values);
    let manifest = map(vec![
        ("planId", t(input.plan_id)),
        ("manifestSha256", t(&digest)),
        ("entries", values),
    ]);
    carriers
        .check_record("Rust3PreparedOutputManifestV3", &manifest)
        .map_err(Refusal::Shape)?;
    let seal = map(vec![
        ("planId", t(input.plan_id)),
        ("manifestSha256", t(&digest)),
        ("entryCount", Value::Unsigned(count)),
        ("totalBlobBytes", Value::Unsigned(bytes)),
        ("totalChunkCount", Value::Unsigned(chunks)),
    ]);
    carriers
        .check_record("Rust3PreparedOutputSealV3", &seal)
        .map_err(Refusal::Shape)?;
    Ok(Built {
        manifest,
        seal,
        bytes,
        chunks,
    })
}

pub(super) fn chunk(
    policy: &Policy,
    plan_id: &str,
    entry: &Value,
    index: u64,
    offset: u64,
    bytes: Vec<u8>,
) -> Result<Value, Refusal> {
    let Value::Map(fields) = entry else {
        return Err(Refusal::Join("prepared entry"));
    };
    let get = |key| {
        super::super::super::ts2::carrier::field(fields, key)
            .ok_or(Refusal::Join("prepared entry field"))
    };
    let Value::Unsigned(length) = get("blobByteLength")? else {
        return Err(Refusal::Join("prepared length"));
    };
    let maximum = policy.limit("maxPreparedOutputChunkBytes")?;
    let start = index.checked_mul(maximum).ok_or(Refusal::Arithmetic)?;
    if start != offset || start >= *length {
        return Err(Refusal::Join("prepared chunk coordinates"));
    }
    if size(bytes.len())? != (*length - start).min(maximum) {
        return Err(Refusal::Join("prepared greedy chunk length"));
    }
    let value = map(vec![
        ("planId", t(plan_id)),
        ("outputOrdinal", get("outputOrdinal")?.clone()),
        ("chunkIndex", Value::Unsigned(index)),
        ("byteOffset", Value::Unsigned(offset)),
        ("bytes", Value::Bytes(bytes)),
    ]);
    Carriers::load("Rust3")
        .map_err(Refusal::Shape)?
        .check_record("Rust3PreparedOutputChunkV3", &value)
        .map_err(Refusal::Shape)?;
    Ok(value)
}

#[cfg(test)]
#[path = "prepared_tests.rs"]
mod tests;
