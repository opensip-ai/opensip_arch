"""Static bypass checklist against inspect_syntax_universe. Not product code."""
from pathlib import Path
src = Path(
    "/tmp/opensip-implementation/m2-syntax-universe-subject-10/product/crates/evaluator/src/native_universe.rs"
).read_text()
checks = {
    "no_admission_parameter": "admission:" not in src.split("pub fn inspect_syntax_universe", 1)[1][:800],
    "reruns_inspect_native_context": "inspect_native_context(inputs, context_digest, work)" in src,
    "no_memo_cache": "OnceLock" not in src and "lazy_static" not in src and "thread_local" not in src,
    "compiler_unsupported": '"compiler universe retained-input owners"' in src,
    "row_dispatch_entry_point": 'bind_syntax_universe' in src,
    "context_form_sha256_text": 'sha256-text' in src,
    "carries_admission_refusals": "admission.refusals()" in src,
    "grammar_subset": "native.syntax-grammar-not-in-bundle" in src,
    "no_snapshot_param": "snapshot_inventory" not in src and "snapshotInventory" not in src,
    "no_nested_retained_map": "configGraph" not in src and "nodeModulesLayout" not in src,
}
print("\n".join(f"{k}={v}" for k, v in checks.items()))
assert all(checks.values())
