# Native retention and Plan owner modules

Add native_retention.rs for the native-frame byte traversal and plan_native.rs for Plan-level selection/capability/grant/read-set joins, plus native-plan-registry.json for their exact embedded metadata. All are within evaluator; no new crate, dependency direction or runtime dependency. Rust snake_case and JSON kebab-case match the existing native_context/native_universe and plan_capability family.

The next source candidate will extract retention logic from the growing native_universe.rs into native_retention.rs, leaving binders in the former. It will preserve behavior and public exports, with private crate-level sharing of the existing validated-value helpers. Plan joins then orchestrate those owners; identity remains lower-level and cannot call evaluator. This layout does not approve the extraction or new Plan behavior: exact frozen source review follows.

All370parent rows and20package/DAG records remain unchanged. Metadata registry is selected-source data, not a dynamic extension point. No compiler execution or Plan/native/fullRun/replay authority is implied by this layout. Reproject all selected description overrides by stable filepath at activation. Live11/16 already selects inventory13 and native-runtimev3; universe/retention/Plan source candidates are separate.
