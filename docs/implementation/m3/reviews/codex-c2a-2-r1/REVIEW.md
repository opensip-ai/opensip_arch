# C2A-2-r1 review

**Verdict: REQUIRED-FINDINGS — one required finding, no non-blocking observations.**

The predicate, existing signing seam and staged signed-path controls are sound for the supplied default fixtures. The shared generator needs to encode valid escapable path strings correctly before this unit is accepted. Both open questions are answered below and are not findings.

## Subject and verification

Manifest: `docs/implementation/m3/snapshot-plan-c/c2a-2-r1-subject.json`, 8,558 bytes, SHA-256 `1e64f3800a4a47259969e8fde95562c9877d460ef78563efb5a17c8ee8182f44`.

Rehashed all 37 members successfully. All four candidate/archive map pins, the two existing-file parent pins, source.json authority pins and the candidate product-lock pin match. The worktree is detached at `e770404a8e6e1f5a604c54e7b0626c6309d76381`; its dirty/untracked scope is exactly the four mapped files. There are two new files. No lib.rs change or new predicate-census site is present.

Read the scope, implementation/tests, lane runner/results, relevant component-manifest shape/path validation, existing public test-only signing code and the accepted C2a plan/item-8 authorities. Independently ran only the permitted operability source check: passed, 114 rows, no findings. No Cargo, compiler, build, test, signing operation or lane was run during this review.

## Required finding

### C2A2-R1-RF-1 — JSON-escape supplied tree paths and entrypoints

**P2; `crates/security/src/trust/component_fixtures.rs:90`**, also directory prefixes at line 84 and entrypoint at lines 98–100.

`body()` inserts supplied paths directly into JSON string literals with format!, then parses the assembled platform with unwrap(). The manifest's generated path shape accepts a nonempty string, and `component_manifest::path_ok` does not exclude a quote or non-NUL controls. These are not malformed path inputs merely because JSON requires escaping them.

For example, keep both default files and add the lawful file **`lib/a"b.js`**, with any supplied bytes. The emitted file entry contains:

```text
"path":"lib/a"b.js"
```

This is invalid JSON, so the platform parse panics before the real body validator or signed reader can run. A quote in a proper directory prefix also breaks its directory row. A quote in the first supplied filename independently breaks the entrypoint encoding. Newline/general-control path characters have the same JSON-escaping issue. Parsing the literal fragments implied by the source confirms the syntax error; no product code was executed.

This violates the shared generator's supplied-tree/role-valid-body duty and prevents lawful adversarial fixtures from exercising the ordinary reader and C2a-1. The current role-validity test uses only the fixed FILES paths (`bin/entry`, `lib/provider.js`), which cannot expose the issue.

**Required change:** encode path strings with the existing JSON/canonical machinery, or correctly escape every affected interpolation, including directory prefixes and entrypoint. Add controls with quoted names, non-NUL controls and non-ASCII names, including an escapable first-file entrypoint and directory prefix. Assert exact decoded paths, supplied lengths/digests, real body validation and the signed-reader/candidate path. Preserve the existing p1 output and empty-components behavior. Do not repair this by narrowing fixtures to ASCII-only names.

## Other requested assessments

**Predicate and signers.** The include is lexically inside the existing tests module under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. The source pin and unchanged crash-matrix site census cover that placement; the predicate-widening mutation is caught by both. The shared module uses the existing sign function and caller-supplied existing signer/root seam, with normal component/catalog construction using COMPONENT_SIGNER and INDEX_SIGNER. No new seed, root, key source or feature is introduced. Reading the existing public test signing implementation was explicitly in scope; no key file was read.

**Existing bytes.** The component_release refactor preserves its p1 literal layout, digest associations and deterministic envelope for the pre-existing component_body inputs. The compatibility control compares it with the prior literal and sign operation. The empty-components branch retains the old bodies and wrapper. Full-suite equal failure sets support that preservation. The new default release path carries LABEL on its artifact rows. RF-1 concerns additional valid supplied names, not the existing default-byte comparison.

**Role validity and tree projection.** On the default supplied tree, each of the five roles passes real full body validation with declaration 1. Non-analyzers drop commands and clear capabilities/permissions; the analyzer keeps its existing provider protocol and command duties. File lengths/digests come from supplied slices and directory prefixes are included. RF-1 prevents this claim extending to lawful escapable names. Nothing here verifies retained artifact bytes or grants component closure admission.

**C2-T6's staged leg.** The new bootstrap control builds the signed release, obtains the InitialCore, accepts onto the private synthetic P0 site, reads the accepted store with the full ordinary reader and host contexts, and uses C2a-1's authenticated bridge/candidate for all roles. The analyzer uses the explicitly test-selected seam. It checks component kinds, candidate identifiers, body digest and Blob count. This is the appropriate staged leg; C2a-3's retained-tree verifier/admission remains outstanding.

## Open-question dispositions

- **Q-C2A2-1 — not a finding.** Keeping historical p1 rows unchanged while new fixture release rows carry LABEL is consistent with the simultaneous byte-preservation and fixture-label duties. This accepts C2-T8's stated label half only; it does not establish the later synthetic-labelled Run/authoritative-surface refusal or qualification.
- **Q-C2A2-2 — not a finding.** Including the module inside the already gated tests module inherits exactly the required joint predicate without introducing a new independently pinned feature site. Actual lexical placement, the source pin and the unchanged census support that approach.

## Lane, rules and inventory

Raw archived test logs agree with the summary: security 1,212 to 1,218 passes with the same 14 failures; host 412 to 412 passes with the same 8 failures. Focused tests pass all 22, including the predicate-site census. Archived warning-denied all-targets Clippy, workspace/feature checks, release build, environment checks, operability and verify_design pass. New/base-clean files are formatted; core_authentication.rs remains base-dirty and hand-edited, and lib.rs is unchanged.

All nine mutation logs match the recorded failing tests, with no compilation failure substituting for detection. These cover labels, old bytes, declarations, role rules, supplied-content digests, selected bodies, signer use and the predicate, but not JSON escaping of supplied paths.

All 19 census-closure pins match and no candidate file intersects that closure. The operability exception file is unchanged with 439 mint-audit rows. No new mint authority/call, runtime environment read, let-discard, key/root/role/feature or production caller was found. The std::env/env! mentions in the new source-pin test are forbidden-token strings, not calls. Signing uses the existing public fixture seam only. Two new inventory rows are owed after acceptance, numbered from the then-current lock after the combined v223 bind (v224 or later).

No repository, worktree or control file was edited, and the lane lock was not taken. No network, private 413 fixture, installation, signing/private test key file, held tree, T2 store or cache was accessed. No other pane or delegation was used. Only REVIEW.md and review.json were written in the requested directory.
