//! Private lifecycle groundwork; no operational authority or public effect API.
#![forbid(unsafe_code)]
#[allow(dead_code)]
mod leases;

#[allow(dead_code)]
mod locations;

#[allow(dead_code)]
mod selection;

mod lineage;

pub use lineage::{
    CAP as LINEAGE_NODE_CAP, DecodeError as LineageDecodeError, Key as LineageKey,
    Node as DecodedLineageNodeV1, SuppliedChain as SuppliedLineageChain,
    WalkError as LineageWalkError, inspect_supplied as inspect_supplied_lineage,
};

// Syntax only; these values never grant custody, selection or initialization.
pub use selection::{
    CAP as SELECTION_PAIR_CAP, Error as SelectionDecodeError, LEAF as SELECTION_PAIR_LEAF,
    Selection as DecodedSelectionV1,
};
