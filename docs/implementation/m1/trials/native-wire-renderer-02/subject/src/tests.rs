use crate::wire::*;
use opensip_contracts::generated::evidence::FieldPresence;
use serde::Deserialize;
use serde_json::{Value, json};

// Test-only self-describing values. These do not implement a wire format.
enum TypedValue { Text(&'static str), Null, Bytes(Vec<u8>), Unsigned(u64), EmptyMap }
impl<'de> serde::de::IntoDeserializer<'de, serde::de::value::Error> for TypedValue {
    type Deserializer = Self;
    fn into_deserializer(self) -> Self { self }
}
impl<'de> serde::Deserializer<'de> for TypedValue {
    type Error = serde::de::value::Error;
    fn deserialize_any<V: serde::de::Visitor<'de>>(self, visitor: V) -> Result<V::Value, Self::Error> {
        match self {
            Self::Text(v) => visitor.visit_str(v),
            Self::Null => visitor.visit_unit(),
            Self::Bytes(v) => visitor.visit_byte_buf(v),
            Self::Unsigned(v) => visitor.visit_u64(v),
            Self::EmptyMap => visitor.visit_map(serde::de::value::MapDeserializer::<_, Self::Error>::new(std::iter::empty::<(TypedValue, TypedValue)>())),
        }
    }
    serde::forward_to_deserialize_any! {
        bool i8 i16 i32 i64 u8 u16 u32 u64 f32 f64 char str string bytes byte_buf
        option unit unit_struct newtype_struct seq tuple tuple_struct map struct enum
        identifier ignored_any
    }
}

#[test]
fn internally_tagged_record_retains_binary_value_kind() {
    let fields = vec![
        ("path", TypedValue::Text("link")), ("kind", TypedValue::Text("symlink")),
        ("byteLength", TypedValue::Null), ("contentSha256", TypedValue::Null),
        ("executable", TypedValue::Null), ("targetBytes", TypedValue::Bytes(vec![0xff, 0xfe])),
    ];
    let de = serde::de::value::MapDeserializer::<_, serde::de::value::Error>::new(fields.into_iter());
    let value = Rust3SnapshotEntryV2::deserialize(de).unwrap();
    match value {
        Rust3SnapshotEntryV2::Symlink { target_bytes, .. } => assert_eq!(target_bytes.as_slice(), [0xff, 0xfe]),
        _ => panic!("discriminator lost"),
    }
}

#[test]
fn tagged_record_preserves_key_text_tag_and_null_kinds() {
    fn fields() -> Vec<(TypedValue, TypedValue)> {
        vec![
            (TypedValue::Text("path"), TypedValue::Text("link")),
            (TypedValue::Text("kind"), TypedValue::Text("symlink")),
            (TypedValue::Text("byteLength"), TypedValue::Null),
            (TypedValue::Text("contentSha256"), TypedValue::Null),
            (TypedValue::Text("executable"), TypedValue::Null),
            (TypedValue::Text("targetBytes"), TypedValue::Bytes(vec![0xff])),
        ]
    }
    let decode = |values: Vec<(TypedValue, TypedValue)>| Rust3SnapshotEntryV2::deserialize(
        serde::de::value::MapDeserializer::<_, serde::de::value::Error>::new(values.into_iter()));
    assert!(decode(fields()).is_ok());
    for index in [0, 1] {
        let mut values = fields();
        values[index].0 = TypedValue::Bytes(if index == 0 { b"path".to_vec() } else { b"kind".to_vec() });
        assert!(decode(values).is_err(), "byte-string key at {index}");
        let mut values = fields();
        values[index].0 = TypedValue::Unsigned(index as u64);
        assert!(decode(values).is_err(), "integer key at {index}");
        let mut values = fields();
        values[index].1 = TypedValue::Bytes(if index == 0 { b"link".to_vec() } else { b"symlink".to_vec() });
        assert!(decode(values).is_err(), "byte-string text/tag at {index}");
    }
    for index in [2, 3, 4] {
        let mut values = fields();
        values[index].1 = TypedValue::EmptyMap;
        assert!(decode(values).is_err(), "empty map for null at {index}");
    }
    let mut reversed = fields();
    reversed.reverse();
    assert!(decode(reversed).is_ok(), "decoder must not require tag-first order");
}

#[test]
fn every_json_representable_required_null_rejects_empty_map() {
    fn probe<T: serde::de::DeserializeOwned>(base: Value) {
        assert!(serde_json::from_value::<T>(base.clone()).is_ok());
        for (key, value) in base.as_object().unwrap() {
            if value.is_null() {
                for replacement in [json!({}), json!([]), json!(""), json!(0), json!(false)] {
                    let mut changed = base.clone();
                    changed[key] = replacement;
                    assert!(serde_json::from_value::<T>(changed).is_err(), "{key}");
                }
            }
        }
    }
    probe::<Ts2SnapshotEntryV1>(json!({"kind":"file","path":"a","byteLength":0,"contentSha256":"a","linkTarget":null}));
    probe::<Ts2SnapshotEntryV1>(json!({"kind":"symlink","path":"a","byteLength":0,"contentSha256":null,"linkTarget":"b"}));
    probe::<Rust3SnapshotEntryV2>(json!({"kind":"file","path":"a","byteLength":0,"contentSha256":"a","executable":true,"targetBytes":null}));
    for base in [
        json!({"kind":"source-span","snapshotId":"s","path":"a","contentSha256":"a","startByte":0,"endByte":1,"factId":null}),
        json!({"kind":"fact-ref","snapshotId":null,"path":null,"contentSha256":null,"startByte":null,"endByte":null,"factId":"f"}),
    ] {
        probe::<Ts2AnchorRefV1>(base.clone());
        probe::<Rust3AnchorRefV1>(base);
    }
}

#[test]
fn owned_bytes_are_not_json_sequences_or_text() {
    for raw in ["[0,1,255]", "\"0001ff\"", "\"AAH/\"", "null", "{}"] {
        assert!(serde_json::from_str::<ByteString>(raw).is_err(), "{raw}");
    }
    let raw = vec![0, 1, 255];
    let deserializer = serde::de::value::BorrowedBytesDeserializer::<serde::de::value::Error>::new(&raw);
    let owned = ByteString::deserialize(deserializer).unwrap();
    drop(raw);
    assert_eq!(owned.as_slice(), [0, 1, 255]);
    assert_eq!(owned.into_vec(), vec![0, 1, 255]);
}

#[test]
fn null_is_present_and_required_and_extra_keys_are_rejected() {
    let base = json!({"executionId":null,"analysisOrdinal":null,"observedPhase":"snapshot"});
    let parsed: Ts2CancelledV1 = serde_json::from_value(base.clone()).unwrap();
    assert_eq!(serde_json::to_value(parsed).unwrap(), base);
    for name in ["executionId", "analysisOrdinal", "observedPhase"] {
        let mut missing = base.clone();
        missing.as_object_mut().unwrap().remove(name);
        assert!(serde_json::from_value::<Ts2CancelledV1>(missing).is_err(), "{name}");
    }
    for wrong in [json!("SNAPSHOT"), json!(4), json!(null)] {
        let mut changed = base.clone();
        changed["observedPhase"] = wrong;
        assert!(serde_json::from_value::<Ts2CancelledV1>(changed).is_err());
    }
    let mut extra = base;
    extra["extra"] = json!(0);
    assert!(serde_json::from_value::<Ts2CancelledV1>(extra).is_err());
}

#[test]
fn optional_fields_preserve_absence_and_empty_values() {
    let base = json!({"kind":"fact-derivation","stageId":"stage1","relations":["calls"],"operator":"semantic-provider"});
    let absent: Rust3C2PlanStageV3 = serde_json::from_value(base.clone()).unwrap();
    assert!(matches!(absent.depends_on, FieldPresence::Missing));
    assert_eq!(serde_json::to_value(absent).unwrap(), base);
    for name in ["dependsOn", "budget", "capabilityGrants", "providerId"] {
        let mut invalid = base.clone();
        invalid[name] = Value::Null;
        assert!(serde_json::from_value::<Rust3C2PlanStageV3>(invalid).is_err(), "{name}");
    }
    let mut present = base;
    present["dependsOn"] = json!([]);
    present["capabilityGrants"] = json!([]);
    present["providerId"] = json!("rust-semantic");
    let value: Rust3C2PlanStageV3 = serde_json::from_value(present.clone()).unwrap();
    assert!(matches!(value.depends_on, FieldPresence::Present(ref v) if v.is_empty()));
    assert_eq!(serde_json::to_value(value).unwrap(), present);
}

#[test]
fn tagged_records_preserve_required_null_and_reject_other_shape() {
    let base = json!({"path":"a.ts","kind":"file","byteLength":u64::MAX,"contentSha256":"a".repeat(64),"linkTarget":null});
    let value: Ts2SnapshotEntryV1 = serde_json::from_value(base.clone()).unwrap();
    assert_eq!(serde_json::to_value(value).unwrap(), base);
    for name in ["path", "byteLength", "contentSha256", "linkTarget"] {
        let mut missing = base.clone();
        missing.as_object_mut().unwrap().remove(name);
        assert!(serde_json::from_value::<Ts2SnapshotEntryV1>(missing).is_err(), "{name}");
    }
    let mut other = base.clone();
    other["kind"] = json!("symlink");
    assert!(serde_json::from_value::<Ts2SnapshotEntryV1>(other).is_err());
    let mut extra = base;
    extra["surprise"] = json!(1);
    assert!(serde_json::from_value::<Ts2SnapshotEntryV1>(extra).is_err());
}

#[test]
fn integers_do_not_round_or_accept_float_or_negative() {
    let wrap = |raw: &str| format!(r#"{{"snapshotId":"s","manifestSha256":"a","entryCount":{raw},"totalFileBytes":0,"totalChunkCount":0}}"#);
    for raw in ["0", "9007199254740993", "18446744073709551615"] {
        let v: Ts2SnapshotAcceptedV1 = serde_json::from_str(&wrap(raw)).unwrap();
        assert_eq!(v.entry_count.to_string(), raw);
    }
    for raw in ["-1", "1.0", "1e0", "18446744073709551616"] {
        assert!(serde_json::from_str::<Ts2SnapshotAcceptedV1>(&wrap(raw)).is_err());
    }
}
