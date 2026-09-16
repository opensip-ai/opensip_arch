# Tooling file inventory v5

Proposes 77 additive files under existing package ownership: 36 generator/provisioning files, 37 boundary checker package and regression files, two package locks and two lane orchestration files. All 246 inherited rows, 20 package definitions, dependency edges and policy values remain equal. No product implementation is installed by this record.

The generator files correspond to frozen generator04 (actual Grok review and root assent in ../reviews/grok-combined-generation-04). The checker package corresponds to frozen packaging08, which is undergoing review. Its runtime remains accepted checker07. Owned first-party module and fixture paths are inventoried; materialized node_modules and Python wheel runtime members remain dependency closures pinned by their manifests. They are not a new forest of first-party modules.

The checker regression fixtures contain historical or synthetic approval data solely to exercise refusal and pin-binding behavior. The eventual product preflight must use the actual selected design lock. tools/check_typescript.py and tools/typescript-lanes.json reserve that orchestration boundary; their code and policy selection need separate review. This inventory does not approve unimplemented code.

Existing row descriptions remain unchanged under additive succession. The old root package-manager and report bundler descriptions therefore require scoped passage overrides when the concrete npm/bootstrap selection is reviewed; the existing accepted CLI bootstrap description must continue to inherit through v5. This record does not silently settle those deferred decisions.

Naming follows existing language conventions: Python maintenance entries use underscores; JavaScript/TypeScript modules use descriptive hyphenated names; tests use .test.mjs; explicit package/lock names remain standard. No new factory is introduced. Generator snapshot and build receipts describe inputs, not runtime semantic authority or release qualification.
