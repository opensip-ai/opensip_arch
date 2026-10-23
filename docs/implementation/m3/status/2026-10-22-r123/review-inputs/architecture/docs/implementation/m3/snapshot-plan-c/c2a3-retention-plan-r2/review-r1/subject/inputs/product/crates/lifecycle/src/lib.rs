//! Lifecycle groundwork. The component store, its installer and the
//! retained-tree capability (law CI r5 items 4 to 7; units CI-2 and CI-3)
//! are the public effect API; every other module is private groundwork with
//! no operational authority.
#![forbid(unsafe_code)]
// Law X9 r1 item 2, guard 1: the forwarded crash-matrix feature (plan r3
// LD-CIP-3) never reaches a build without debug assertions.
#[cfg(all(feature = "scenario-fixtures", not(debug_assertions)))]
compile_error!("scenario-fixtures is test-only and refuses builds without debug assertions");
#[cfg(all(feature = "crash-matrix", not(debug_assertions)))]
compile_error!(
    "the crash-matrix feature is test-only (law X9 r1 item 2) and refuses every build without debug assertions"
);
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
    relative_path as lineage_relative_path,
};

// Syntax only; these values never grant custody, selection or initialization.
pub use selection::{
    CAP as SELECTION_PAIR_CAP, Error as SelectionDecodeError, LEAF as SELECTION_PAIR_LEAF,
    Selection as DecodedSelectionV1,
};

// Law CI r5 items 4 and 5 (unit CI-2): the component store and its
// installer. Library only, with no production caller until CI-4.
#[cfg(target_os = "macos")]
pub mod installation;

// Law CI r5 items 6 and 7 (unit CI-3): the pinned retained-tree capability
// C2a-3 binds, and its verified transfer.
#[cfg(target_os = "macos")]
pub mod retained_tree;
