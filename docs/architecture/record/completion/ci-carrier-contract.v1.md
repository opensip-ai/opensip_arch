# CI carrier admission

Author: Codex lead. Proposed reference design evidence for G16; no qualification.

`ci-ownership-schema.v1.json` is the closed compiled selector-input carrier.
`check_ci_carrier_design.py` independently compares all ownership maps, complete
Git unit/component domains, manifest dependency maps, role/platform and consumer
maps, source record digests and retained corpus-basis digest with trusted host
observations. Its fixtures inject those independently acquired observations;
the model does not claim to read Git or verify release signatures itself.
Twenty-four admission/ambiguity cases precede the already retained qualification
design unit's 26 selector scenarios and complete matrix.

The repository source record is `.opensip-ci-ownership.json` at each compared
Git tree, a strict JSON object with exactly `schemaMajor:1` and `owners`, where
`owners` uses the compiled schema's `currentOwners` grammar. Every tracked path,
including this record and build files, has an explicit owner. Hash the exact
source blob bytes with SHA-256 to produce previous/currentRecordDigest. These
digests refer to source records, never recursively to the compiled carrier
containing them. Production reads the referenced Git blob and complete tree,
validates map equality/completeness and compiles the carrier; no caller-supplied
digest makes an unrelated ownership map authoritative. Dependency and shared
consumer observations are similarly acquired from the pinned manifest/contract
sources identified by the parent distribution contract.

A source-record change expands changed units to the complete previous/current
union. Missing or inconsistent data refuses before a complete ownership conflict
may select all. Correctly observed multiple owners are not an integrity error:
they select the complete universe. A caller inventing the same conflict without
corresponding source ownership refuses. Changed units, tree IDs and source
observations are trusted verifier output in this reference model, not user data.

The parent distribution §7 adopts the source path and exact encoding above.
Substitutions retain complete independent custody, refusal-before-conflict,
reverse dependency/shared-consumer closure, all six lane result slots and the
same G16 execution owner (CI + release engineering). Current reference cases
are design evidence; actual Git acquisition and CI execution remain gate work.
