# Addendum: trailing-slash `under_prefix` finding

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Standing:** Addendum to the completed pinned atom-kernel50 advisory. Original `report.md` / `report.json` are retained byte-for-byte and are not rewritten. Rust five-corpus checks were not re-run. Root native-completeness 4896 remains outside this pin.

**Original reports (unmodified):**

| File | Bytes | sha256 |
| --- | ---: | --- |
| `report.md` | 9521 | `c8999ebd2941f0823504e1360ba09606baec4117b5665f833f2c42ee04a2f579` |
| `report.json` | 6241 | `80f772055090c16be3f654fafce75f929c9cc76c75e2b04c457974c19ba18df3` |

## Finding (for root disposition)

**ATOM-HELPER-UNDER-PREFIX-TRAILING-SLASH.** Pinned `under_prefix` is not `N._under_unit`. At the pure helper boundary this is an actionable semantic difference, even if a later public retained spelling excludes the trailing slash.

Selected `atom_model._under_prefix` maps `"."`/`""` to the empty root and then calls `N._under_unit`, which treats a non-empty root as a directory prefix via `root.rstrip("/") + "/"`. Pinned rust maps only `"."` to empty and then requires `path.strip_prefix(root)` to yield a remainder that **starts with `/`**. A root that already ends in `/` therefore matches only the exact root string, not its children.

Demonstrated with `/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B -X int_max_str_digits=0` loading actual `atom_model.v1.py` and `N._under_unit` (jsonschema not stubbed). Artifact: `trailing-slash-counterexample.json` **1713** / `63a50096…`.

| Input | Selected `_path_in_scope` / `N._under_unit` | Pinned rust `under_prefix` |
| --- | --- | --- |
| `workspaceRoots: ["src/"]`, path `src/foo` | **true** | **false** |
| `pathPrefixes: ["src/"]`, roots `["."]` | **true** | **false** |
| `excludedPathPrefixes: ["src/"]`, roots `["."]` | **false** (excluded) | **true** (exclusion missed) |
| `workspaceRoots: ["src"]`, path `src/foo` | true | true |

Root is aligning `under_prefix` to exact selected N behavior and adding regression cases.

## Can admitted import scope contain such roots?

**Yes at the import-scope schema and atom-helper boundary. No as an identity-model local `scope-descriptor` payload.**

- `atom_model.SCOPE_SCHEMA`, `identity-schemas.v2.json#/$defs/scope-descriptor` (`Text` items), and `imported-evidence.schema.json#/$defs/ImportScopeDescriptor` all **accept** `"src/"`. Reference `Draft202012Validator` accepted the counterexample record on all three.
- Atom `_import_scope` validates only `SCOPE_SCHEMA`. Workflow `validate_import_record` checks the identity `scope-descriptor` **schema**, not identity-model `payload()`'s extra `SCOPE_LOGICAL_PATH` loop.
- identity-model.v3 `payload(..., "scope-descriptor")` **would refuse** `"src/"` as `SCOPE_LOGICAL_PATH` because `split("/")` is `["src", ""]`. That extra check applies to local identity bundle scope-descriptor records (plan scope), not to the atom helper and not to import schema admission.
- Native `CanonicalRelativeDirV1` **rejects** `"src/"` (no trailing slash). That grammar is internal unit roots, not ImportScopeDescriptor members.

The helper is the import-scope membership law. A schema-admitted import scope may carry the trailing-slash spelling, so the divergence is live at this pin even if plan-retained scope-descriptor identity later excludes it.

## `noCallerTruthOrFlags`

That limit means **no public API** may take caller-provided truth or flags. The private test kernel **does** consume synthetic map flags: `flags()` / `_require_wrapper_flags` read reconstructed `importFlagsAdapter` (and wrapper `consumable`/`staleness`). That is retained-input machinery for the private scanner, not a public callback.

## requiredFindings

One finding, recorded above for root disposition. Original advisory verdict otherwise unchanged; this addendum does not re-accept SOURCE48/runtime24, public API, global admission, native scanning, or M2.
