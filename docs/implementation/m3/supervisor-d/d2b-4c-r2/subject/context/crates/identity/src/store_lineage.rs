//! Private, read-only lineage syntax and supplied-chain inspection.
//! A decoded node or complete supplied chain is not an admitted native binding,
//! transition proof, custody capability, authorization, or permission to create.
use crate::store_identity::StoreInstance as StoreComponent;
use crate::{CanonicalError, JsonValue as V, canonical_bytes, parse_json};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::{String, ToString},
    vec::Vec,
};

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
    /// The node's exact relative components, `transitions/lineage/S/G/K.node`:
    /// the one spelling every crate joins. Not resolution, custody or selection.
    pub fn relative_components(&self) -> [String; 5] {
        [
            "transitions".into(),
            "lineage".into(),
            self.store.clone(),
            self.generation.to_string(),
            format!("{}.node", self.schema),
        ]
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
    /// The admitted chain, from the requested key back to its one root.
    pub fn into_nodes(self) -> Vec<Node> {
        self.nodes
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
mod tests {
    use super::Key;

    #[test]
    fn the_relative_components_pin_the_node_spelling() {
        let store = "0123456789abcdef0123456789abcdef";
        for (generation, schema, g, k) in [
            (0, 1, "0", "1.node"),
            (i64::MAX, 2, "9223372036854775807", "2.node"),
        ] {
            let key = Key::parse(store, generation, schema).unwrap();
            assert_eq!(
                key.relative_components(),
                ["transitions", "lineage", store, g, k]
            );
        }
        assert_eq!(
            Key::parse(store, 17, 2)
                .unwrap()
                .relative_components()
                .join("/"),
            "transitions/lineage/0123456789abcdef0123456789abcdef/17/2.node"
        );
    }
}
