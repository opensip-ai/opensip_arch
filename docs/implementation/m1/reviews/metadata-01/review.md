# Review: RF-01 metadata design/reference correction (m1-metadata-subject-01)

**Verdict: CHANGES-REQUIRED**

- Subject manifest: `/tmp/opensip-implementation/m1-metadata-subject-01.json`
- Subject manifest SHA-256: `bccfda510cfe8cb5ff690922e9e729569900e8884a0d8adc82805e557b50c93b`
- Candidate folder: `docs/implementation/m1/metadata-v1/` (10 files)
- Architecture checkout (read-only): `/Users/sb/code/opensip-ai/opensip_arch`
- Environment: `/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B` (jsonschema 4.25.1, referencing 0.37.0)

## Summary

The schema core is sound:

- **Envelope4.** It adds only the metadata branch and one narrow parser-refusal rule. Once those additions are stripped, every envelope3 constraint is byte-for-byte unchanged. I confirmed this with the checker's compatibility function and my own normalized diff.
- **Metadata schema1.** It has closed, mutually exclusive help/version variants and a private `BuildMetadataV1`.
- **Inventory4.** It pins the fixed selectors as constants.

My 102 independent probes found no schema-behaviour defect.

The unit still cannot be accepted, for three scoped reasons:

1. **Stale coverage routing.** The coverage successor still routes help/version verification to envelope major 3 and to the uncorrected "release descriptor" wording. Neither the new parser-refusal rule nor the build-metadata record has an owner.
2. **Incomplete successor binding.** `successor.json` does not bind the README. The README is the only place the semantic contract is stated: catalogue admission, M1 development-only builds, no-effects bootstrap, and signing direction. The accepted passages whose wording the candidate claims to correct are also not listed.
3. **A second build-channel constant.** `BuildMetadataV1.buildChannel` sits beside the accepted `HostAssetPinV1.buildChannel`, and nothing says the two are derived from one selection. The accepted plan says "No second untrusted self-declaration is introduced".

All three are small corrections that stay inside RF-01. None of them requires redesigning the envelope or metadata schemas.

## Subject integrity

- **Before review:** all 10 manifest files matched on SHA-256 and byte length, and there were no unlisted files under the frozen root.
- **After review:** the manifest SHA-256 was unchanged, all 10 files still matched, and no unlisted files had appeared. My probes imported `check_metadata.py` with `-B`, so no bytecode was written.
- **Architecture copies:** the checkout holds byte-identical copies of the candidate folder, which is where the checker's `arch/` pins resolve. All 10 hashes are equal to the frozen subject.

## Checker execution

I ran `check_metadata.py --architecture /Users/sb/code/opensip-ai/opensip_arch` from the frozen folder. It exited 0 with `passed: true`, 28 schemas verified, 43 cases (each outcome matching its expectation), 5 lexical negatives and `productQualification: false`. The output is saved in `checker-output.json`.

## Source pins (sources.json)

- **Overlay manifests:** I checked `candidate-subject.v45.json` (sha `8b4efbb0…`, 3190907 bytes) and `application-subject.v46.json` (sha `dab6e00f…`, 126405 bytes) against the design-lock approvals. Both match.
- **Non-candidate pins:** all 25 match the overlay-selected entry (v46 `files` first, then v45 `files`) and the live bytes. That is 24 accepted schemas plus `canonical.py`; three of the schemas come from v45.
  - Four paths also appear in v46 `beforeImages`. For each, I confirmed the pin is the after-image, not the before-image.
- **Candidate pins:** the three candidate schema pins are exempt, as the scope allows, and match the frozen bytes.
- **Scope caveat:** `sources.json` is an input list, not a generation recipe. I did not treat it as one.

## Topic assessment

### Schema exclusivity and compatibility

- **`kind=meta` requires `meta`.** It fixes `termination` to exactly `{"class":"success"}` (so no `runId`) and `exitCode` to 0. It excludes all 16 other top-level carriers, and the checker confirms that list equals the envelope's properties minus the allowed set.
- **`meta` is forbidden on every other kind.** A metadata payload on a failure is refused (probe `meta-on-failure-kind`), and so is a mixed help+version payload (`meta-both-variants-mixed`).
- **Major versions are separated.** The major3 reader rejects every accepted major4 case, and the major4 reader rejects a major3 failure. Evaluator, Run, finding, query and mutation identities are unchanged.
- **Inventory4 differs from inventory3 only in:**
  - `metaDispatch` on help and version;
  - the added `build-channel` parity field;
  - the JSON renderer version and parity rule;
  - `schemaMajor` and `standing`.

  The checker proves this by restoration. My probes confirm that the inventory schema refuses: an altered selector, `metaDispatch` on `completion`, a missing `metaDispatch` on version, and swapped dispatches.

### Integer, Unicode and ordering semantics

- **Integers are exact.** `exitCode:false`, `schemaMajor:true`, `4.0`, `4e0`, `-0` and 2^64 are all refused.
- **Parsing is strict.** Duplicate keys, lone surrogates, NaN, a BOM and overlong UTF-8 are all refused.
- **`maxLength` counts Unicode scalars.** 2048 astral characters are accepted and 2049 are refused; lone surrogates are refused before validation.
- **SemVer is enforced.** The limit of 128 is exact, and leading zeros, empty identifiers, non-ASCII digits, surrounding whitespace, a trailing newline and a `v` prefix are all refused. `closure2` grammar is enforced (case, prefix, trailing newline).
- **Arrays are strictly ordered.** 256 closure IDs are accepted and 257 refused. Help rows are strictly unique in UTF-8 order by name.
- **Command names match the inventory.** The metadata `CommandName` enum equals the 45 inventory4 command names exactly.

### Fixed human/JSON parity selectors

- **Selectors are pinned constants.** Each resolves against the fixture envelopes, and the checker confirms the selector keys equal `parityFields`.
- **They are declarative.** No JSONPath engine is required, and JSON Pointer `queryDispatch` is unchanged.
- See advisories A-03 and A-04.

### Command catalogue scope

- **The semantics are sound.** Admission compares the entire rows to the trusted catalogue:
  - `topic=null` must return the full catalogue;
  - a named topic must return exactly its row;
  - unknown or known-but-unimplemented topics are refused.

  During M1 the catalogue lists implemented commands only; full completion requires all 45.
- **Where the rules live.** These rules exist only in README prose and the reference `admit()` function, which is why RF-B matters.

### Development versus release identity admission

- **Shape rules hold.** Development must have an empty `closureIds`, and the schema enforces this. Release shape validity is explicitly not admission.
- **M1 has no release switch.** There is no environment or caller way to select the release channel.
- **Semantic admission compares against a trusted build selection.**
- **Gaps:** the single-source rule for the build channel is missing (RF-C), and the schema admits a release with no closures (advisory A-02).

### Signing and self-hash direction

The direction is correct and acyclic:

1. The private record excludes the host digest/closure, its own digest, archives and signing outputs.
2. Non-host closures are admitted first and compiled into the host.
3. The existing signing owners then bind the finished host bytes.

No new signature envelope, `signatureVerified` field or trust path is introduced; probes confirm those fields are refused. This answers RF-01(b)'s question about signature verification at M1 versus later: version describes the shipped selection and performs no fresh verification.

The wording correction is not bound where the old wording lives (RF-B).

### No-effects bootstrap contract

- **The contract is stated adequately for design:** arguments and compiled constants only, with no project, config, provider, store, registry, network or asset access.
- **It is prose only.** Nothing here executes it, and I did not accept it as product execution. The coverage method still carries that obligation to `apps/cli/tests/startup_tests.rs`.

### Coverage routing

Deficient; see RF-A.

## Judgment: parser-refusal empty-errors rule

**Sound and D9-compatible. Complete for its purpose, apart from the advisory hardening below.**

Evidence for the premise:

- **No general argument detail exists.** I scanned all 319 `DomainDetailCode` entries for argument, option, usage, topic, parse, CLI and flag detail. The only matches are context-specific (`GRANT.ARGV_MISMATCH`, `TEST.ARGV_NOT_IN_CLOSURE`, `AUTHZ.CI_FLAG_MISMATCH`, …). None is a general malformed-invocation detail.
- **The registry states "existing D9 class/code/exit remains unchanged".**
- **D9 already owns the code.** The d9-joins OC-4 row `invocationRefused` (request-rejected, exit 2) maps malformed invocation to `REQUEST.UNKNOWN_OPTION`. So the one relaxed code covers every ordinary parser refusal (unknown option or topic, missing or invalid argument). Other OC-4 sub-causes keep their existing detail-bearing forms.
- **No prose law conflicts.** I found no accepted product-v1 contract requiring a registered detail on every failure. The `minItems:1` on `errors` was the only such law.
- **The D9 golden agrees.** In `d9-exit-contract.v1.14.json` (L1702–1723), golden `pre-admission-unknown-option` ("unknown CLI option before project resolution") has `expectedTermination` exactly `{"class":"request-rejected","errorCode":"REQUEST.UNKNOWN_OPTION"}`, with no `domainDetail`. That is the termination the candidate fixes for its empty-errors rule.

Probe results:

- **Narrowness holds.**
  - Empty `errors` is refused with a `domainDetail`, a `runId`, `SCHEMA_MAJOR_UNSUPPORTED`, `PRECONDITION_FAILED`, `CONFIG.INVALID`, `kind=query`, `kind=meta`, exit 3 or 4, or missing or empty `diagnostics`.
  - Envelope3 cannot carry it.
  - The nonempty-detail form and the `OUTPUT.FORMAT_NOT_APPLICABLE` completion refusal are preserved in both majors.
- **Mutation coverage.** Widening the rule's termination constraint is caught by the fixtures, but not by `compatibility()`, which strips the last two `allOf` entries by position.

Residual hardening (advisory A-01, not blocking):

- `diagnostics:[""]` is admitted.
- Diagnostics can reflect raw argv bytes, including ESC and NUL, because `BoundedText` has no control-character law.
- `projectId` and `agentHints` are not forbidden on a pre-admission parser refusal.

I see no need for a different scoped correction. Minting a detail would widen the public vocabulary, and adding a fixed detail would falsely represent a parser failure as another class.

## Required findings

### RF-A — Coverage successor still routes help/version verification to envelope major 3 and the uncorrected descriptor wording; the new obligations are unrouted

**Evidence:**

- `implementation-coverage.v2.json` L1177 (help) and L1209 (version) say: "Produce human and CommandEnvelope-major-3 JSON … version closure IDs are the build-embedded release descriptor values".
- A normalized diff against v1 shows only three `valueSha256` changes, the added `build-channel` parity field, the inventory pointer and `standing`. No method text changed and no row was added.
- No coverage text mentions `metadata:1`, `BuildMetadataV1`, the envelope4 empty-errors parser-refusal rule, the development-only / no-release-switch negative, or HostAssetPin agreement.

**Why it blocks:** the coverage successor is the implementation routing selected as part of this unit. As written, it directs the startup tests to verify the superseded carrier and wording. The new obligations have no owner or test.

**Correction:**

- Update the help/version verification methods to CommandEnvelope major 4 with `metadata:1`, the `metaDispatch` selectors and the corrected wording.
- Route the parser-refusal rule (owner such as `arguments.rs`/`outcomes.rs`; tests covering empty errors only for UNKNOWN_OPTION, exit 2 and nonempty diagnostics).
- Route the `BuildMetadataV1` build-time producer and its negatives (M1 development only, no environment or caller release switch, rejection of invented closures).
- Refresh any hashes and the checker.

### RF-B — successor.json does not bind the normative contract or the corrected accepted passages

**Evidence:**

- `successor.json.candidates` lists the three schemas, inventory4 and coverage v2 only. `README.md`, `fixtures.json`, `check_metadata.py` and `sources.json` are unbound.
- The README is the only statement of:
  - catalogue admission (full rows, null topic means everything, a known but unimplemented topic is refused, aliases canonicalized);
  - trusted-build semantic admission;
  - the M1 development-only / no-switch rule;
  - the no-effects bootstrap;
  - the signing direction;
  - the rationale for the parser-refusal rule.
- The README says the planning wording "build-embedded signed release descriptor" is corrected "within this scope". That wording persists in accepted text the successor does not list as parents:
  - `docs/v2/architecture/implementation-boundaries-and-build-plan.md` L885;
  - `docs/v2/architecture/14-repository-and-module-layout.md` L325;
  - `docs/v2/architecture/repository-file-inventory.v1.json` L279;
  - the M1 successor `docs/implementation/m1/repository-file-inventory.v3.json` L279, pinned by the current design-lock.

**Why it blocks:** a product implementation that binds `successor.json` (the declared overlay) receives schemas without their semantic contract. It would also still read the old wording in bound parents. RF-01's closure evidence is "the accepted successor, pinned in design-lock.json", so the pinnable record must be complete.

**Correction:**

- Add the README (contract), fixtures, checker and sources as bound members, or move the normative clauses into a bound record.
- List each corrected accepted passage (path, sha256, bytes, line or selector) with its replacement wording as a scoped supersession.

### RF-C — BuildMetadataV1.buildChannel is not single-sourced with the accepted HostAssetPinV1.buildChannel

**Evidence:**

- The accepted build plan L813–815 says the build "compiles the manifest's exact length and raw SHA-256 into the host binary as `HostAssetPinV1` with its `buildChannel`. No second untrusted self-declaration is introduced".
- `docs/v2/architecture/report-asset-binding.v1.json` (HostAssetPinV1 `buildChannel`) says: "A development build must state its channel in version output and can never present itself as a signed product release."
- Plan-01 advisory A-11 asked the successor to "mirror `HostAssetPinV1.buildChannel`".
- The candidate adds a separate compiled `BuildMetadataV1.buildChannel`. Neither the README, the schema nor the checker states that it derives from, or must equal, the HostAssetPin channel. HostAssetPinV1 is never mentioned, and no case covers a disagreement.

**Why it blocks:** two independently compiled channel constants could disagree. For example, the assets could be pinned as development fixtures while version reports `release`. That is exactly the masquerade the accepted parents forbid, and it is the development-disclosure question RF-01(b) asked this successor to settle.

**Correction:**

- State that version's `buildChannel` and `HostAssetPinV1.buildChannel` are projections of one trusted build selection, or that version reads the HostAssetPin channel.
- Add a reference negative in which they disagree and admission or build refuses.
- Route the matching build-time test (see RF-A).

## Advisories

- **A-01 — parser-refusal hardening.** Consider:
  - `minLength:1` on the required diagnostic;
  - an explicit renderer escaping or sanitization law for reflected argv (ESC and NUL are currently admitted);
  - forbidding `projectId`/`projectRoot` on the empty-errors branch.
- **A-02 — release with no closures.** The schema admits `buildChannel=release` with `closureIds:[]`; only trusted-build comparison refuses it. State whether a release must have at least one admitted closure, or leave that to M6 explicitly.
- **A-03 — help parity covers names only.** Parity covers only `command-names`. The human rendering of topic, usage and summary is prose, not parity-bound. Also, the inventory schema does not bind `parityFields` to the selector keys; only the checker's set equality does.
- **A-04 — selector syntax.** The selectors use JSONPath-like syntax (`$.meta.commands[*].name`) next to the JSON Pointer `parityPaths`. They are fixed constants, which is acceptable, but give each an equivalent pointer or projection definition so implementers don't need a JSONPath dialect. Separately, the inherited `(?![\s\S])` end anchor has no Rust `regex` crate equivalent; generated validators must use `\z` or equivalent.
- **A-05 — fixtures mask schema laws.** Semantic `admit()` hides schema-level laws. If the development empty-closure rule or the help order annotation is removed from the schema, the envelope fixtures still pass through catalogue/build comparison (my mutation probes). Add schema-only cases for the payload `$defs`, and select the new `allOf` entries in `compatibility()` by content rather than position.
- **A-06 — length units.** Length limits count Unicode scalar values. Product validators must count `char`s, not bytes or UTF-16 units.
- **A-07 — editorial.**
  - The README says the parser-refusal correction is "below"; it is above.
  - The README's opening line ("Candidate for actual Claude review") and `successor.json` `standing` must be replaced by the eventual acceptance record, not edited in place after review.
- **A-08 — checker input location.** The checker loads candidate schemas from the `--architecture` checkout, not from its own folder. They are hash-pinned and identical today, but a frozen-folder run against a checkout without those copies would fail rather than validate the frozen bytes.

## Executed checks

1. Pre-review and post-review SHA-256/byte verification of the manifest and all 10 subject files, including an unlisted-file scan.
2. Frozen-folder checker run (exit 0; 28 schemas; 43 cases; 5 lexical negatives).
3. `sources.json`: 25 non-candidate pins checked against the v45/v46 `files` overlay (after-image, not `beforeImages`) and live bytes; overlay manifest hashes checked against the design-lock approvals; 3 candidate schemas matched to the frozen bytes.
4. Byte comparison of the architecture checkout's `docs/implementation/m1/metadata-v1` copies with the frozen subject.
5. Normalized JSON diffs of envelope3→4, inventory schema 3→4, inventory v3→v4 and coverage v1→v2.
6. Registry and D9 inspection: all 319 `DomainDetailCode` entries, registry record for `OUTPUT.FORMAT_NOT_APPLICABLE`, `StepTermination` `allOf`, D9ErrorCode request members, d9-joins v8 OC-4, the d9-exit-contract v1.14 `pre-admission-unknown-option` golden (termination has no detail), workflows-and-surfaces L1141–1142, and a product-v1 prose search for a detail-required law (no match).
7. Plan-01 review RF-01 and A-11 text; build plan L800–845 and L885; ch14 L325; repository-file-inventory v1 and M1 v3 L279; report-asset-binding HostAssetPinV1 `buildChannel`.
8. 102 independent probes (`probes.py`, results in `probe-results.json`). 93 matched expectations with no schema defect. The 9 misses are the coverage and successor-binding expectations behind RF-A and RF-B. The probes covered meta exclusivity, the parser-refusal boundaries, SemVer, closures, Unicode length, lexical rules, inventory mutations, selector resolution and 6 schema/checker mutations.

## Limitations

- No product code exists or was run. Renderer parity, startup no-effects, release assembly and signing are unexecuted prose obligations.
- Entry-point closure of the whole corpus was not evaluated. The known historical RF-03 dangling policy Atom definition is unrelated and is not counted as metadata success.
- Only one jsonschema/referencing version was used, and only the Python reference validator.
- `d9-exit-contract.v1.14.json` was not read in full. I read its `pre-admission-unknown-option` golden and otherwise relied on the evaluator3 common D9 definitions and the d9-joins v8 OC-4 row.
- The golden search listed only the first 10 matching files, all d9-exit-contract versions. I did not look for envelope-level (errors/diagnostics) fixtures for that golden beyond the v1.12–v1.14 termination entries.
- The review is limited to the frozen subject and the parents cited here; the full 12,920-file accepted set was not read.

## Standing

This review does not accept the unit. When RF-A to RF-C are corrected and accepted, only that scoped design/reference correction would be accepted. Product implementation, design-lock successor binding, and the M1, runtime and release gates would all remain required.
