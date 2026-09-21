//! Private, read-only lineage syntax and supplied-chain inspection.
//! A decoded node or complete supplied chain is not an admitted native binding,
//! transition proof, custody capability, authorization, or permission to create.
use crate::locations::StoreComponent;
use opensip_identity::{CanonicalError, JsonValue as V, canonical_bytes, parse_json};
use std::collections::{BTreeMap, BTreeSet};
use std::path::PathBuf;

pub const CAP: usize = 4096;

#[derive(Debug, PartialEq, Eq)]
pub enum DecodeError {
    Bound,
    Decode(CanonicalError),
    Shape,
    Version,
    Store,
    Generation,
    StateSchema,
    Digest,
    RootPair,
    SelfPredecessor,
    NonCanonical,
}

/// A syntactically valid triple, not a selected or admitted store.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Key {
    store: String,
    generation: i64,
    schema: u8,
}
impl Key {
    pub fn parse(store: &str, generation: i64, schema: u8) -> Result<Self, DecodeError> {
        StoreComponent::parse(store).map_err(|_| DecodeError::Store)?;
        if generation < 0 {
            return Err(DecodeError::Generation);
        }
        if !matches!(schema, 1 | 2) {
            return Err(DecodeError::StateSchema);
        }
        Ok(Self {
            store: store.into(),
            generation,
            schema,
        })
    }
    pub fn store_instance(&self) -> &str {
        &self.store
    }
    pub fn store_generation(&self) -> i64 {
        self.generation
    }
    pub fn state_schema(&self) -> u8 {
        self.schema
    }
    /// Exact relative spelling only. Resolving this path requires retained native
    /// directory handles, custody checks and the installation fence elsewhere.
    pub fn relative_path(&self) -> PathBuf {
        PathBuf::from("transitions")
            .join("lineage")
            .join(&self.store)
            .join(self.generation.to_string())
            .join(format!("{}.node", self.schema))
    }
    fn from_fields(fields: &BTreeMap<String, V>) -> Result<Self, DecodeError> {
        let V::String(store) = &fields["storeInstanceId"] else {
            return Err(DecodeError::Store);
        };
        let V::Integer(generation) = &fields["storeGeneration"] else {
            return Err(DecodeError::Generation);
        };
        let generation = i64::try_from(generation.get()).map_err(|_| DecodeError::Generation)?;
        let schema = match &fields["stateSchema"] {
            V::Integer(n) if n.get() == 1 => 1,
            V::Integer(n) if n.get() == 2 => 2,
            _ => return Err(DecodeError::StateSchema),
        };
        Self::parse(store, generation, schema)
    }
}
fn exact(fields: &BTreeMap<String, V>, names: &[&str]) -> bool {
    fields.len() == names.len() && names.iter().all(|name| fields.contains_key(*name))
}

#[derive(Debug)]
pub struct Node {
    raw: Vec<u8>,
    key: Key,
    predecessor: Option<Key>,
    intent_digest: Option<String>,
}
impl Node {
    pub fn decode(raw: &[u8]) -> Result<Self, DecodeError> {
        if raw.len() > CAP {
            return Err(DecodeError::Bound);
        }
        let value = parse_json(raw).map_err(DecodeError::Decode)?;
        let V::Object(fields) = &value else {
            return Err(DecodeError::Shape);
        };
        if !exact(
            fields,
            &[
                "schemaVersion",
                "storeInstanceId",
                "storeGeneration",
                "stateSchema",
                "predecessor",
                "selectedByIntentDigest",
            ],
        ) {
            return Err(DecodeError::Shape);
        }
        if !matches!(&fields["schemaVersion"], V::Integer(n) if n.get() == 1) {
            return Err(DecodeError::Version);
        }
        let key = Key::from_fields(fields)?;
        let predecessor = match &fields["predecessor"] {
            V::Null => None,
            V::Object(p) if exact(p, &["storeInstanceId", "storeGeneration", "stateSchema"]) => {
                Some(Key::from_fields(p)?)
            }
            _ => return Err(DecodeError::Shape),
        };
        let intent_digest = match &fields["selectedByIntentDigest"] {
            V::Null => None,
            V::String(s)
                if s.len() == 64
                    && s.bytes()
                        .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)) =>
            {
                Some(s.clone())
            }
            _ => return Err(DecodeError::Digest),
        };
        if predecessor.is_none() != intent_digest.is_none() {
            return Err(DecodeError::RootPair);
        }
        if predecessor.as_ref() == Some(&key) {
            return Err(DecodeError::SelfPredecessor);
        }
        if canonical_bytes(&value).map_err(DecodeError::Decode)? != raw {
            return Err(DecodeError::NonCanonical);
        }
        Ok(Self {
            raw: raw.to_vec(),
            key,
            predecessor,
            intent_digest,
        })
    }
    pub fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub fn key(&self) -> &Key {
        &self.key
    }
    pub fn predecessor(&self) -> Option<&Key> {
        self.predecessor.as_ref()
    }
    pub fn selected_by_intent_digest(&self) -> Option<&str> {
        self.intent_digest.as_deref()
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum WalkError<E> {
    Limit,
    Read(E),
    Missing(Key),
    Misbound { requested: Key, observed: Key },
    Cycle(Key),
}

/// Owns only decoded supplied bytes, in selected-to-root order. It cannot prove
/// native existence, uniqueness of physical files, immutable publication, intent
/// authorization, marker equality or the full five-member namespace binding.
#[derive(Debug)]
pub struct SuppliedChain {
    nodes: Vec<Node>,
}
impl SuppliedChain {
    pub fn nodes(&self) -> &[Node] {
        &self.nodes
    }
}

/// Inspect one component, iteratively, without scanning unrelated lineages.
/// `max_nodes` is an explicit caller work bound, not a new architectural chain
/// limit. Missing, unreadable, misbound, cyclic and truncated chains return no
/// partial success. The future native caller must retain and recheck every file
/// and share its operation budget; this supplied reader does neither itself.
pub fn inspect_supplied<E>(
    start: &Key,
    max_nodes: usize,
    mut read: impl FnMut(&Key) -> Result<Option<Node>, E>,
) -> Result<SuppliedChain, WalkError<E>> {
    let mut next = start.clone();
    let mut seen = BTreeSet::new();
    let mut nodes = Vec::new();
    loop {
        if seen.contains(&next) {
            return Err(WalkError::Cycle(next));
        }
        if nodes.len() >= max_nodes {
            return Err(WalkError::Limit);
        }
        seen.insert(next.clone());
        let node = read(&next)
            .map_err(WalkError::Read)?
            .ok_or_else(|| WalkError::Missing(next.clone()))?;
        if node.key != next {
            return Err(WalkError::Misbound {
                requested: next,
                observed: node.key,
            });
        }
        let predecessor = node.predecessor.clone();
        nodes.push(node);
        match predecessor {
            Some(key) => next = key,
            None => return Ok(SuppliedChain { nodes }),
        }
    }
}

#[cfg(test)]
mod tests;
