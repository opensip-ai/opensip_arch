//! Pure private selection.pair codec. Exact bytes and syntactic identifiers
//! do not select/admit a core or store, acquire custody, or authorize first use.
use crate::store_identity::StoreInstance as StoreComponent;
use crate::{CanonicalError, JsonValue as V, canonical_bytes, parse_json};
use alloc::{string::String, vec::Vec};
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
