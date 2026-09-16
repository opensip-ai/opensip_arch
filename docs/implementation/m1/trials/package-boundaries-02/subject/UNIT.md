# Cargo internal package boundary check candidate

Read-only developer tool against the separately selected inventory. Checks all
local package names/source roots, declared normal/build/dev/target/optional
internal dependencies, aliases, resolved internal edges, host/provider workspace
membership, explicit manifest values and Cargo target source locations. Current
raw manifests are cross-checked against metadata so stale metadata cannot hide
an added inactive internal dependency. External packages cannot shadow internal
owners or import a local product owner. No new package edge is selected here.

Fourteen test groups pass, including actual Cargo metadata negative controls for
an inactive forwarding feature, Windows-only dependency and build/dev edges.
The accepted CLI candidate's six local packages pass. The separate provider
trial builds the two unchanged pure libraries from an immutable source export
with no root Cargo manifest, host app, Node or generator files. Provider and root
select identical versions/features for all14 shared packages; the exact contracts
dependency check passes11 registry dependencies. Its disposable executable is a
build probe, not a provider implementation or compiler-integration qualification.

Inputs are explicit repository, freshly captured Cargo metadata, selected
inventory and lane. The caller runs design verification and Cargo --locked
--offline metadata first. This tool checks internal boundaries only; external
closure/features, target matrices, package scripts, macro expansion, #[path] and
include! imports, purity and runtime effects need their own checks/reviews. An
attacker-supplied metadata document is not a Cargo attestation. No approval,
product integration, M1 completion, commit, push or new compiler choice implied.

Candidate02 addresses the independent real-Cargo counterexample: legacy
build_dependencies/dev_dependencies tables accepted by editions before2024 are
also read, including target tables. Fresh metadata already exposed them; now
stale metadata cannot conceal the manifest change. Two new regression groups
include a real edition2021 metadata-before/manifest-after control. Earlier
candidate01 and the reviewer evidence remain unchanged.
