# Combined generation01 checkpoint

One explicit runner generates all eight schema/native/report-codec files from40 source schemas and857 entry points. A second run from a different workspace root produces the same eight files and input-closure digest. Seven files equal native04 exactly; report.ts differs only in two provenance comments. Strict TypeScript with exactOptionalPropertyTypes passes. Prior unchanged-runtime tests are not claimed as rerun.

This is an observed development recipe, not a confined production build. Python/jsonschema dependency closure and native runtime remain unqualified. Tool executables are supplied explicitly and byte-pinned; no hardcoded generation roots in the runner. Source approval, product registry/bootstrap/inventory and confinement still require integration. Candidate01 is checkpointed; use a successor for further edits.
