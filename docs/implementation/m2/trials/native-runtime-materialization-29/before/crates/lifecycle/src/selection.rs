//! Private lifecycle selection.pair codec. Exact bytes and syntactic identifiers
//! do not select/admit a core or store, acquire custody, or authorize first use.
use crate::locations::StoreComponent;
use opensip_identity::{CanonicalError, JsonValue as V, canonical_bytes, parse_json};
pub const CAP: usize = 4096;
pub const LEAF: &str = "selection.pair";
#[derive(Debug, PartialEq, Eq)]
pub enum Error {
    Bound,
    Decode(CanonicalError),
    Shape,
    Schema,
    Closure,
    Store,
    Generation,
    StateSchema,
    NonCanonical,
}
pub struct Selection {
    raw: Vec<u8>,
    core_closure: String,
    store_instance: StoreComponent,
    store_generation: i64,
    state_schema: u8,
}
impl Selection {
    pub fn decode(raw: &[u8]) -> Result<Self, Error> {
        if raw.len() > CAP {
            return Err(Error::Bound);
        }
        let value = parse_json(raw).map_err(Error::Decode)?;
        let V::Object(fields) = &value else {
            return Err(Error::Shape);
        };
        let names = [
            "selectionSchema",
            "coreClosure",
            "storeInstanceId",
            "storeGeneration",
            "stateSchema",
        ];
        if fields.len() != names.len() || !names.iter().all(|k| fields.contains_key(*k)) {
            return Err(Error::Shape);
        }
        if !matches!(&fields["selectionSchema"],V::Integer(n)if n.get()==1) {
            return Err(Error::Schema);
        }
        let V::String(closure) = &fields["coreClosure"] else {
            return Err(Error::Closure);
        };
        if !closure.strip_prefix("closure2:").is_some_and(|h| {
            h.len() == 64
                && h.bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
        }) {
            return Err(Error::Closure);
        }
        let V::String(instance) = &fields["storeInstanceId"] else {
            return Err(Error::Store);
        };
        let instance = StoreComponent::parse(instance).map_err(|_| Error::Store)?;
        let V::Integer(generation) = &fields["storeGeneration"] else {
            return Err(Error::Generation);
        };
        let generation = i64::try_from(generation.get()).map_err(|_| Error::Generation)?;
        if generation < 0 {
            return Err(Error::Generation);
        }
        let schema = match &fields["stateSchema"] {
            V::Integer(n) if n.get() == 1 => 1,
            V::Integer(n) if n.get() == 2 => 2,
            _ => return Err(Error::StateSchema),
        };
        if canonical_bytes(&value).map_err(Error::Decode)? != raw {
            return Err(Error::NonCanonical);
        }
        Ok(Self {
            raw: raw.to_vec(),
            core_closure: closure.clone(),
            store_instance: instance,
            store_generation: generation,
            state_schema: schema,
        })
    }
    pub fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub fn core_closure(&self) -> &str {
        &self.core_closure
    }
    pub fn store_instance(&self) -> &str {
        self.store_instance.as_str()
    }
    pub fn store_generation(&self) -> i64 {
        self.store_generation
    }
    pub fn state_schema(&self) -> u8 {
        self.state_schema
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use opensip_identity::JsonInteger;
    fn integer(n: i128) -> V {
        V::Integer(JsonInteger::new(n).unwrap())
    }
    fn sample(g: i128, k: i128) -> V {
        V::Object(
            [
                ("selectionSchema".into(), integer(1)),
                (
                    "coreClosure".into(),
                    V::String(format!("closure2:{}", "a".repeat(64))),
                ),
                ("storeInstanceId".into(), V::String("b".repeat(32))),
                ("storeGeneration".into(), integer(g)),
                ("stateSchema".into(), integer(k)),
            ]
            .into(),
        )
    }
    fn with(field: &str, value: V) -> Vec<u8> {
        let V::Object(mut o) = sample(0, 1) else {
            unreachable!()
        };
        o.insert(field.into(), value);
        canonical_bytes(&V::Object(o)).unwrap()
    }
    #[test]
    fn selection_roundtrip_owns_exact_bytes_and_preserves_zero_max_and_both_schemas() {
        for g in [0, 1, i64::MAX as i128] {
            for k in [1, 2] {
                let mut raw = canonical_bytes(&sample(g, k)).unwrap();
                let selected = Selection::decode(&raw).unwrap();
                let saved = raw.clone();
                raw.clear();
                assert_eq!(selected.raw(), saved);
                assert_eq!(
                    selected.core_closure(),
                    format!("closure2:{}", "a".repeat(64))
                );
                assert_eq!(selected.store_instance(), "b".repeat(32));
                assert_eq!(selected.store_generation(), g as i64);
                assert_eq!(selected.state_schema(), k as u8);
            }
        }
    }
    #[test]
    fn selection_closed_members_duplicates_and_types_are_not_coerced() {
        let V::Object(base) = sample(0, 1) else {
            unreachable!()
        };
        for key in base.keys() {
            let mut o = base.clone();
            o.remove(key);
            assert!(matches!(
                Selection::decode(&canonical_bytes(&V::Object(o)).unwrap()),
                Err(Error::Shape)
            ));
        }
        assert!(matches!(
            Selection::decode(&with("extra", V::Null)),
            Err(Error::Shape)
        ));
        let mut renamed = base.clone();
        renamed.remove("coreClosure");
        renamed.insert(
            "coreclosure".into(),
            V::String(format!("closure2:{}", "a".repeat(64))),
        );
        assert!(matches!(
            Selection::decode(&canonical_bytes(&V::Object(renamed)).unwrap()),
            Err(Error::Shape)
        ));
        let raw = String::from_utf8(canonical_bytes(&sample(0, 1)).unwrap()).unwrap();
        let duplicate = raw.replace(
            "\"selectionSchema\":1",
            "\"selectionSchema\":1,\"selectionSchema\":1",
        );
        assert!(matches!(
            Selection::decode(duplicate.as_bytes()),
            Err(Error::Decode(_))
        ));
        for value in [
            V::Null,
            V::Bool(true),
            V::String("1".into()),
            integer(0),
            integer(2),
        ] {
            assert!(matches!(
                Selection::decode(&with("selectionSchema", value)),
                Err(Error::Schema)
            ));
        }
        for raw in [b"[]" as &[u8], b"null", b"1"] {
            assert!(matches!(Selection::decode(raw), Err(Error::Shape)));
        }
        assert!(matches!(
            Selection::decode(&with("coreClosure", integer(1))),
            Err(Error::Closure)
        ));
        assert!(matches!(
            Selection::decode(&with("storeInstanceId", V::Null)),
            Err(Error::Store)
        ));
    }
    #[test]
    fn selection_identifiers_are_complete_lowercase_and_exactly_sized() {
        for id in [
            "a".repeat(64),
            format!("closure1:{}", "a".repeat(64)),
            format!("closure2:{}", "A".repeat(64)),
            format!("closure2:{}\n", "a".repeat(64)),
            format!("closure2:{}", "a".repeat(63)),
            format!("closure2:{}", "a".repeat(65)),
            format!("closure2:{}", "g".repeat(64)),
        ] {
            assert!(matches!(
                Selection::decode(&with("coreClosure", V::String(id))),
                Err(Error::Closure)
            ));
        }
        for id in [
            "b".repeat(31),
            "b".repeat(33),
            "B".repeat(32),
            "g".repeat(32),
            format!("{}\n", "b".repeat(32)),
            "../store".into(),
        ] {
            assert!(matches!(
                Selection::decode(&with("storeInstanceId", V::String(id))),
                Err(Error::Store)
            ));
        }
    }
    #[test]
    fn selection_generation_and_state_schema_keep_exact_integer_domains() {
        for value in [
            integer(-1),
            integer(i64::MAX as i128 + 1),
            integer(u64::MAX as i128),
            V::Bool(false),
            V::String("0".into()),
            V::Null,
        ] {
            assert!(matches!(
                Selection::decode(&with("storeGeneration", value)),
                Err(Error::Generation)
            ));
        }
        for value in [
            integer(0),
            integer(3),
            integer(-1),
            V::Bool(true),
            V::String("1".into()),
            V::Null,
        ] {
            assert!(matches!(
                Selection::decode(&with("stateSchema", value)),
                Err(Error::StateSchema)
            ));
        }
        let raw = String::from_utf8(canonical_bytes(&sample(0, 1)).unwrap()).unwrap();
        for number in ["0.0", "0e0", "-1.0"] {
            assert!(matches!(
                Selection::decode(
                    raw.replace(
                        "\"storeGeneration\":0",
                        &format!("\"storeGeneration\":{number}")
                    )
                    .as_bytes()
                ),
                Err(Error::Decode(_))
            ));
        }
    }
    #[test]
    fn selection_cap_precedes_decode_and_noncanonical_records_stay_unavailable() {
        assert!(matches!(
            Selection::decode(&vec![0xff; 4097]),
            Err(Error::Bound)
        ));
        assert!(matches!(
            Selection::decode(&vec![0xff; 4096]),
            Err(Error::Decode(_))
        ));
        let raw = canonical_bytes(&sample(0, 1)).unwrap();
        let mut newline = raw.clone();
        newline.push(b'\n');
        assert!(matches!(
            Selection::decode(&newline),
            Err(Error::NonCanonical)
        ));
        let text = String::from_utf8(raw).unwrap();
        for changed in [
            format!(" {text}"),
            text.replace("\":", "\": "),
            text.replace("\"a", "\"\\u0061"),
        ] {
            if changed != text {
                assert!(Selection::decode(changed.as_bytes()).is_err());
            }
        }
        let reordered = format!(
            "{{\"selectionSchema\":1,\"coreClosure\":\"closure2:{}\",\"storeInstanceId\":\"{}\",\"storeGeneration\":0,\"stateSchema\":1}}",
            "a".repeat(64),
            "b".repeat(32)
        );
        assert!(matches!(
            Selection::decode(reordered.as_bytes()),
            Err(Error::NonCanonical)
        ));
    }
}
