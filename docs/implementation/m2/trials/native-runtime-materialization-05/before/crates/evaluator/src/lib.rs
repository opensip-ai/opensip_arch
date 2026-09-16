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
mod native_retention;
mod native_universe;
mod unicode_case;
pub use native_universe::{NativeUniverseChecks, NativeUniverseError, inspect_syntax_universe};

pub use native_universe::inspect_typescript_universe;

pub use native_universe::inspect_rust_universe;

pub use native_retention::{NativeRetentionChecks, NativeRetentionError, inspect_native_retention};

mod plan_native;
pub use plan_native::{PlanNativeChecks, PlanNativeError, inspect_plan_native};
