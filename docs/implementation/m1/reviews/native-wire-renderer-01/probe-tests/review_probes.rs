//! Reviewer scratch probes. Observational: prints accept/refuse for each case.
use opensip_native_wire_carrier_trial::wire::*;
use serde::Deserialize;
use serde::de::value::{Error, MapDeserializer, SeqDeserializer};
use serde::de::{IntoDeserializer, Visitor};

#[derive(Clone, Debug)]
enum V { T(&'static str), N, B(Vec<u8>), U(u64), S(Vec<V>) }

/// D(value, strict): strict honours type hints like a schema-directed codec.
#[derive(Clone, Debug)]
struct D(V, bool);

impl<'de> IntoDeserializer<'de, Error> for D {
    type Deserializer = Self;
    fn into_deserializer(self) -> Self { self }
}

fn refuse<T>(what: &str) -> Result<T, Error> { Err(serde::de::Error::custom(format!("strict refused {what}"))) }

impl D {
    fn hinted<'de, Vi: Visitor<'de>>(self, ok: fn(&V) -> bool, what: &str, visitor: Vi) -> Result<Vi::Value, Error> {
        if self.1 && !ok(&self.0) { return refuse(what); }
        serde::Deserializer::deserialize_any(self, visitor)
    }
}

impl<'de> serde::Deserializer<'de> for D {
    type Error = Error;
    fn deserialize_any<Vi: Visitor<'de>>(self, visitor: Vi) -> Result<Vi::Value, Error> {
        let strict = self.1;
        match self.0 {
            V::T(s) => visitor.visit_str(s),
            V::N => visitor.visit_unit(),
            V::B(b) => visitor.visit_byte_buf(b),
            V::U(u) => visitor.visit_u64(u),
            V::S(items) => visitor.visit_seq(SeqDeserializer::new(items.into_iter().map(move |x| D(x, strict)))),
        }
    }
    fn deserialize_str<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> { self.hinted(|x| matches!(x, V::T(_)), "str", v) }
    fn deserialize_string<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> { self.hinted(|x| matches!(x, V::T(_)), "string", v) }
    fn deserialize_identifier<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> { self.hinted(|x| matches!(x, V::T(_)), "identifier", v) }
    fn deserialize_bytes<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> { self.hinted(|x| matches!(x, V::B(_)), "bytes", v) }
    fn deserialize_byte_buf<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> { self.hinted(|x| matches!(x, V::B(_)), "byte_buf", v) }
    fn deserialize_u64<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> { self.hinted(|x| matches!(x, V::U(_)), "u64", v) }
    fn deserialize_unit<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> { self.hinted(|x| matches!(x, V::N), "unit", v) }
    fn deserialize_option<Vi: Visitor<'de>>(self, v: Vi) -> Result<Vi::Value, Error> {
        match self.0 { V::N => v.visit_none(), _ => v.visit_some(self) }
    }
    fn deserialize_enum<Vi: Visitor<'de>>(self, _n: &'static str, _vs: &'static [&'static str], v: Vi) -> Result<Vi::Value, Error> {
        match self.0 { V::T(s) => v.visit_enum(IntoDeserializer::<Error>::into_deserializer(s)), _ => refuse("enum") }
    }
    serde::forward_to_deserialize_any! {
        bool i8 i16 i32 i64 i128 u8 u16 u32 u128 f32 f64 char unit_struct newtype_struct seq tuple
        tuple_struct map struct ignored_any
    }
}

fn map<'de>(strict: bool, fields: Vec<(V, V)>) -> MapDeserializer<'de, std::vec::IntoIter<(D, D)>, Error> {
    MapDeserializer::new(fields.into_iter().map(|(k, v)| (D(k, strict), D(v, strict))).collect::<Vec<_>>().into_iter())
}

fn accepted() -> Vec<(V, V)> {
    vec![(V::T("snapshotId"), V::T("s")), (V::T("manifestSha256"), V::T("a")), (V::T("entryCount"), V::U(1)),
         (V::T("totalFileBytes"), V::U(0)), (V::T("totalChunkCount"), V::U(0))]
}
fn symlink() -> Vec<(V, V)> {
    vec![(V::T("path"), V::T("link")), (V::T("kind"), V::T("symlink")), (V::T("byteLength"), V::N),
         (V::T("contentSha256"), V::N), (V::T("executable"), V::N), (V::T("targetBytes"), V::B(vec![0xff]))]
}
fn with(mut base: Vec<(V, V)>, i: usize, k: Option<V>, v: Option<V>) -> Vec<(V, V)> {
    if let Some(k) = k { base[i].0 = k; }
    if let Some(v) = v { base[i].1 = v; }
    base
}
fn show<T, E: std::fmt::Display>(label: &str, r: Result<T, E>) {
    match r { Ok(_) => println!("ACCEPT  {label}"), Err(e) => println!("refuse  {label}: {e}") }
}

#[test]
fn observe_kind_preservation() {
    for strict in [false, true] {
        let m = if strict { "strict" } else { "loose " };
        show(&format!("{m} baseline flat"), Ts2SnapshotAcceptedV1::deserialize(map(strict, accepted())));
        show(&format!("{m} baseline tagged"), Rust3SnapshotEntryV2::deserialize(map(strict, symlink())));
        show(&format!("{m} flat String <- bstr"), Ts2SnapshotAcceptedV1::deserialize(map(strict, with(accepted(), 0, None, Some(V::B(b"s".to_vec()))))));
        show(&format!("{m} flat key u64 index 0"), Ts2SnapshotAcceptedV1::deserialize(map(strict, with(accepted(), 0, Some(V::U(0)), None))));
        show(&format!("{m} flat key bstr"), Ts2SnapshotAcceptedV1::deserialize(map(strict, with(accepted(), 0, Some(V::B(b"snapshotId".to_vec())), None))));
        show(&format!("{m} tagged String <- bstr"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 0, None, Some(V::B(b"link".to_vec()))))));
        show(&format!("{m} tagged tag <- bstr"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 1, None, Some(V::B(b"symlink".to_vec()))))));
        show(&format!("{m} tagged tag <- u64 1"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 1, None, Some(V::U(1))))));
        show(&format!("{m} tagged tag key <- bstr"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 1, Some(V::B(b"kind".to_vec())), None))));
        show(&format!("{m} tagged key u64 index 0"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 0, Some(V::U(0)), None))));
        show(&format!("{m} tagged key bstr"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 0, Some(V::B(b"path".to_vec())), None))));
        show(&format!("{m} tagged bytes <- text"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 5, None, Some(V::T("ff"))))));
        show(&format!("{m} tagged bytes <- array"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 5, None, Some(V::S(vec![V::U(255)]))))));
        show(&format!("{m} tagged unit <- u64"), Rust3SnapshotEntryV2::deserialize(map(strict, with(symlink(), 2, None, Some(V::U(0))))));
        show(&format!("{m} flat ByteString <- array"), ByteString::deserialize(D(V::S(vec![V::U(1)]), strict)));
    }
}

#[test]
fn observe_json_edges() {
    let dup = r#"{"snapshotId":"s","snapshotId":"t","manifestSha256":"a","entryCount":0,"totalFileBytes":0,"totalChunkCount":0}"#;
    show("json flat duplicate key", serde_json::from_str::<Ts2SnapshotAcceptedV1>(dup));
    let base = r#""path":"a","byteLength":1,"contentSha256":"b","linkTarget":null"#;
    show("json tagged baseline", serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":"file",{base}}}"#)));
    show("json tagged duplicate member", serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":"file",{base},"path":"z"}}"#)));
    show("json tagged duplicate tag", serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":"file",{base},"kind":"file"}}"#)));
    show("json tagged tag as 0", serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":0,{base}}}"#)));
    for bad in ["1.0", "-1", "1e0", "18446744073709551616"] {
        show(&format!("json tagged byteLength {bad}"), serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":"file","path":"a","byteLength":{bad},"contentSha256":"b","linkTarget":null}}"#)));
    }
    for bad in ["false", "0", "\"\"", "{}", "[]"] {
        show(&format!("json tagged unit linkTarget {bad}"), serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":"file","path":"a","byteLength":1,"contentSha256":"b","linkTarget":{bad}}}"#)));
    }
    show("json const analysisOrdinal 5 (inert)", serde_json::from_str::<Ts2CancelledV1>(r#"{"executionId":null,"analysisOrdinal":5,"observedPhase":"snapshot"}"#));
    show("json enum variant index", serde_json::from_str::<Ts2CancelledV1>(r#"{"executionId":null,"analysisOrdinal":null,"observedPhase":0}"#));
    let bytes = ByteString::from_vec(vec![0, 255]);
    let text = serde_json::to_string(&bytes).unwrap();
    println!("json ByteString serialize -> {text}");
    show("json ByteString roundtrip", serde_json::from_str::<ByteString>(&text));
}
