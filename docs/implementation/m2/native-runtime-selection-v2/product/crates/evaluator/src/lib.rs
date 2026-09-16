//! Pure evaluator owners over supplied immutable evidence.
//! This prototype contains capability and bounded native context owner checks;
//! complete evaluator reconstruction and ReplayedRun remain unimplemented.
#![no_std]
#![forbid(unsafe_code)]
extern crate alloc;
mod capabilities;
pub use capabilities::{CapabilityManifest, CapabilityRefusal, admit_capability_manifest};
mod native_context;
pub use native_context::{NativeContextChecks, NativeContextError, inspect_native_context};
mod plan_capability;
pub use plan_capability::{PlanCapabilityError, admit_plan_capability};
mod unicode_case;
