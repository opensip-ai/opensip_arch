# B2-B3D-r1 review

Verdict: **REQUIRED-FINDINGS**

Subject manifest: `docs/implementation/m3/config-discovery-b/b2-b3d-r1-subject.json`, 9,747 bytes, SHA-256 `c01a71932880f5c88e7d441b6faca4abb5af4c876da8ad72de862b5dbc72905b`. All 43 members independently rehashed successfully. All ten product-map rows match the candidate worktree and archived bytes; existing parent pins match product base `84caf3f58d8379c9386fda42a41e5513ac81ebbb`. The candidate has exactly the nine changed paths and one new path in the map. Product main is clean at that base; architecture is at `a1f14786e4ecb0c780d25b093c438821e6a5c3d8`. All nine source-authority pins match committed architecture bytes.

## Required finding

**B2B3D-R1-RF-1: Charge the parallel observation storage before reserving it**

Location: `crates/security/src/custody/discovery_walk.rs:779-788 (Walk::enter)`.

Vec::with_capacity(paths.len()) allocates the complete ChildObservation array before the loop charges any observation slot. The dedicated owned(size_of::<ChildObservation>()) charge happens only after observing each child. If the next observation or slot charge exhausts the ledger, the full array has already been allocated. At the listing ceiling, 131,072 slots at the pinned 88-byte size reserve 11,534,336 bytes before those slot charges. ListingConversion precharges its path and validator records, not this separately charged observation array. The earlier layout also reserved its observation vector eagerly; carrying that pattern into the redesigned parallel vector does not satisfy this unit's explicit charge-before-allocation obligation. Final used() totals and the current marginal-count/native soundness tests do not detect the ordering violation.

Required change: Remove the eager capacity reservation and charge before each allocation/growth, or precharge the entire observation-array allowance with checked arithmetic before reserving capacity, avoiding double charging afterwards. Keep the census consistent with the resulting charge sites and add a focused tight-budget or allocation-order control demonstrating that observation storage is not reserved before its allowance succeeds. Preserve the current behavioral vectors and records.

## Substantive assessment

The core consistently reads relative scope keys: custody, markers, unit chains, nested boundaries and automatic enumeration use the revised representation. The empty key represents the root; removing one common prefix preserves BTreeMap order. Resolved output fields and UnobservedAcl paths are reconstructed under the root with the `/` special case. Grammar refusals retain the raw specification. The scan-test adapter retains the root and slash-delimited descendants and drops previously unread outside entries. Existing expected records and vector files are unchanged.

The walker removes per-entry absolute spellings from frames, listed/verdict sets, transient child keys and the scope. It owns the root spelling once in production. Relative child paths are sorted before observations, and parallel observation indices stay aligned; paths move out on directory descent and names are borrowed as last segments. Scope-owned relative keys remain separately accounted. Terminal Changed/name refusal details stay absolute. Lazy trace and hook closures are ignored by the production stubs; test-only trace_child rebuilds downward relative paths while preserving absolute upward arguments. Descriptor-relative opens and gitdir evidence behavior are preserved.

ListingConversion charges visits, drops dot entries, precharges conversion temporaries, retains the first invalid name with an owned-record charge, and stops converting subsequent names. It continues listing, propagates listing/visitor/limit/native errors before materializing a saved name refusal, and observes no children from a failed listing. The new controls cover the ordering and unchanged escaped detail. Other charge sites retain precharges for keys, scope records, ACL entries, cached verdicts, listed/cargo records and frames. RF-1 concerns the eager observation-array allocation specifically.

The test changes preserve behavioral assertions, traces, hooks and record expectations. Relative-key/population adapters and the two marginal charge-count tests change for the new representation, with their new per-copy counts explained. Three ListingConversion controls are added. The structural check verifies lazy trace call shapes, unchanged empty production stubs and permitted spelling/join sites; its three planted negatives are meaningful for this concrete implementation. It is a structural regression check, not a general Rust program proof.

The census model matches the redesigned charge-site accounting: visits include dot entries, converted paths include validator copies, scope keys and observation slots use their actual sizes, frame paths move, markers use relative keys, and only the retained root contributes a root-length term. Captures retain the componentwise dearer bound, and the read envelope remains explicitly uninterrupted. Whole-file closure pins, anchors and the closed native size inventory are consistent with the successor. The old automatic probe cross-check is removed and disclosed; the new supporting probe's diff changes only throwaway limits and adds the ignored probe. All four successful probe rows exactly match the census's objects, edges and bytes at their actual 134-byte root.

Census maxima are 1,721,687 objects, 1,007,224 edges and 389,872,769 bytes at R=4,096. The smallest powers of two at least twice those values are 2^22, 2^21 and 2^30, respectively. Every censused lead-readable row has perRootByte=1. Only aws-sdk-rust fails the current provisional object margin. No overall margin, held-out margin or workspace full-ledger margin is claimed. Caps and law are unchanged; the lock is byte-identical to base, with inventory 197, 157 inventory successors and 164 contract successors. No caller or environment read is introduced. B2-b and the whole plan remain incomplete.

## Verification

Independently executed only the permitted checks in the candidate worktree:

- Operability source census: 114 rows, no findings.
- Environment exceptions: 10 tests passed.
- FW-01: 7 tests passed.
- Census controls: 18 tests passed.
- Walker storage structural checks: 4 tests passed.
- Full permitted census `--check`: both generated records verified. Held-out repositories and workspaces are skipped before store/overlay resolution.

Assessed supplied Rust/lane evidence without running Rust or the lane. All 17 recorded check rows report success, including warning-denied all-targets Clippy for host/security/platform and formatting of all five edited Rust files. The supplied security comparison preserves the same 14 failures with 1,124→1,127 passes; host preserves the same eight failures and 343 passes. These are equal failure sets, not whole-suite passes. The six focused census tests pass; all 56 supplied native cost comparisons are bounded in all three dimensions, with 46 exact. Each of the eight mutation logs contains precisely its listed runtime test failures, rather than a compilation failure; the five model mutations regenerate predictions. RF-1 is not exercised by those final-total comparisons or mutations.

## Non-blocking observation

**B2B3D-R1-NBO-1** (`SCOPE.md, The outcome; tools/security/discovery_census.py module documentation`): Tighten the descriptions: bytes still depend on root spelling through the single per-walk coefficient 1, so describe removal of the per-entry root term rather than saying bytes no longer depend on root spelling. The census module documentation still says the real-store probe is cross-checked, although the executable cross-check was retired and the replacement probe is separately archived supporting evidence. The generated record and scope otherwise disclose retirement correctly.

## Boundaries

No Cargo, rustc, Rust tests, builds, lane or network was run. No other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or held-out store/overlay was accessed. Neither repository, the candidate worktree, the stage nor control files was edited. Candidate mapped bytes were rechecked after the permitted checks. Only this `REVIEW.md` and `review.json` were written in the requested directory. Lead assent, publication, product commit and inventory successor remain subsequent actions.
