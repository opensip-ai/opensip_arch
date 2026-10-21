//! Pure store marker syntax and supplied expected-ID comparison. No native authority.
use crate::store_identity::StoreInstance;
use crate::{CanonicalError, JsonValue as V, canonical_bytes, parse_json};
use alloc::vec::Vec;
pub const MARKER_LIMIT: usize = 128;
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Error {
    Bound,
    Decode(CanonicalError),
    Shape,
    Instance,
    NonCanonical,
    Binding,
}
#[derive(Debug)]
pub struct Marker {
    instance: StoreInstance,
    bytes: Vec<u8>,
}
impl Marker {
    pub fn decode(raw: Vec<u8>, expected: &StoreInstance) -> Result<Self, Error> {
        if raw.len() > MARKER_LIMIT {
            return Err(Error::Bound);
        }
        let value = parse_json(&raw).map_err(Error::Decode)?;
        let V::Object(ref fields) = value else {
            return Err(Error::Shape);
        };
        if fields.len() != 2
            || !matches!(fields.get("schemaVersion"),Some(V::Integer(n))if n.get()==1)
        {
            return Err(Error::Shape);
        }
        let Some(V::String(id)) = fields.get("storeInstanceId") else {
            return Err(Error::Shape);
        };
        let instance = StoreInstance::parse(id).map_err(|_| Error::Instance)?;
        if canonical_bytes(&value).map_err(Error::Decode)? != raw {
            return Err(Error::NonCanonical);
        }
        if &instance != expected {
            return Err(Error::Binding);
        }
        Ok(Self {
            instance,
            bytes: raw,
        })
    }
    pub fn instance(&self) -> &StoreInstance {
        &self.instance
    }
    pub fn raw(&self) -> &[u8] {
        &self.bytes
    }
}
