"""Static bypass checklist against inspect_rust_universe. Not product code."""
from pathlib import Path

src = Path(
    "/tmp/opensip-implementation/m2-rust-universe-subject-12/product/crates/evaluator/src/native_universe.rs"
).read_text()
fn = src.split("pub fn inspect_rust_universe", 1)[1]
checks = {
    "no_admission_parameter": "admission:" not in fn.split("{", 1)[0],
    "reruns_inspect_native_context": "inspect_native_context(inputs, context_digest, work)" in fn,
    "named_snapshot_object": 'object(snapshot_id, IdentityDomain::Snapshot, work)' in fn,
    "nested_h_frames": "NativeFrameSet::Nested" in fn,
    "expected_nested_domains": all(
        d in fn
        for d in (
            "native.dependency-source-set.v1",
            "native.unified-features.rust.v1",
            "native.prepared-output-set.v3",
            "native.source-unit-ownership.v1",
        )
    ),
    "config_projection_record_h": 'hash_canonical_value("native.cargo-config-projection.v2", projection)'
    in fn,
    "not_file_projectionSha256": "projectionSha256" not in fn,
    "unit_id_closed_h": 'hash_canonical_value(\n                "native.compilation-unit.v1"' in fn
    or 'hash_canonical_value(\n                "native.compilation-unit.v1",' in fn,
    "optional_ownership_null_skip": 'if field(u, "sourceUnitOwnershipId")? != &V::Null' in fn,
    "cfg_additions_subset": "base.is_subset(&cfg)" in fn,
    "no_plan_grant": "prepare-code" not in fn and "read-import" not in fn,
    "no_memo": "OnceLock" not in src and "lazy_static" not in src and "thread_local" not in src,
    "carries_context_refusals": "admission.refusals()" in fn,
}
print("\n".join(f"{k}={v}" for k, v in checks.items()))
assert all(checks.values()), checks
