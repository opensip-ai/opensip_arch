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

mod body_identity;
pub use body_identity::{BodyIdentityChecks, BodyIdentityError, inspect_body_identity};

mod capability_support;
pub use capability_support::{
    NativeSupportChecks, NativeSupportError, inspect_coverage_prerequisites, inspect_syntax_fact,
};

mod coverage;
pub use coverage::{
    CoverageProducerChecks, CoverageProducerError, CoverageProducerInput, CoverageUnresolvedEdge,
    inspect_coverage_producer,
};

mod view_joins;
pub use view_joins::{ViewJoinChecks, ViewJoinError, inspect_view_joins};

mod run_links;
pub use run_links::{
    EvidenceRootChecks, RunLinkChecks, RunLinkError, inspect_evidence_roots, inspect_run_links,
};

mod policy;
pub use policy::{GlobMatchError, portable_glob_match};

pub use policy::{EvaluatorParameterChecks, inspect_evaluator_parameters};
pub use policy::{PolicyAdmissionError, PolicyProgramChecks, inspect_policy_program};

mod proofs;
pub use proofs::{PredicateChecks, PredicateError, inspect_predicate_witnesses};

mod budgets;
pub use budgets::{
    EvaluationCensus, EvaluationWork, RuleWork, WorkError, estimate_evaluation_work,
};

mod stage_output;
pub use stage_output::{
    StageOutputError, StageSpecChecks, inspect_stage_output_schema, inspect_stage_schema_shape,
    inspect_stage_specs,
};

mod import_joins;
pub use import_joins::{
    ImportJoinChecks, ImportJoinError, inspect_import_joins, inspect_parameter_selection,
};

mod import_payloads;
pub use import_payloads::{ImportPayloadError, inspect_import_payload};

mod full_walk;
pub use full_walk::{
    RetainedWalkChecks, RetainedWalkError, RetainedWalkLimits, inspect_retained_walk,
};

mod enumeration;
pub use enumeration::{
    EnumerationExtent, EnumerationExtentError, EnumerationExtentInputs, EnumerationExtentKind,
    project_enumeration_extent,
};

pub use enumeration::{
    EnumerationMembershipChecks, EnumerationMembershipError, inspect_enumeration_membership,
};

pub use enumeration::{EnumerationPackages, project_enumeration_packages};

mod enumeration_join;

pub use enumeration_join::{EnumerationJoinChecks, EnumerationJoinError, inspect_enumeration_join};

pub use import_joins::inspect_plan_import_joins;
pub use stage_output::inspect_plan_stage_specs;
pub use view_joins::inspect_plan_view_joins;
