# Review request: D4-2-inventory-v232 (the additive inventory successor for D4-2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d4-2-inventory-v232-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** D4-2's code is closed: you accepted it in `docs/implementation/m3/reviews/codex-d4-2-r2/`, and it is integrated at `a7839a14aa755495592a4063657e78959be97f43`.

## Subject

- **Stage:** `/tmp/opensip-implementation/d4-2-inventory/architecture`
- **Subject manifest:** `docs/implementation/m3/supervisor-d/d4-2-inventory-v232-subject.json`, 683 bytes, SHA-256 `4c8bf623c07f150d3a388e7807065fe4e133c56bf823b8e0708dadae32dc1207`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v231.json`, 760618 bytes, `f93e6e821788f81dcefcffebeb715f18e096b154d16287c3e2d5ff44a78cfcd3`. It is the lock's last inventory successor (191 successors, 177 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v232.json`, 762267 bytes, `c36f25247e6b6ef1c92bf61eb26fbc47a5c0217cb943a1f3da5eeeb58bd620c4`. Check that its path is the successor's (v232), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d4-2-inventory-v232/successor.json`, 6051 bytes, `b338c6f801cff6c9309096d91dbd3c47ad5e92314d28e6a943dfec2fbd78b6bb`.
- **Product:** clean product main `a7839a14aa755495592a4063657e78959be97f43`, holding D4-2's code commit `a7839a14aa755495592a4063657e78959be97f43`. The architecture is at `f43fb7713c8b44c7e1c1bd732a8004622a7ce043`.

## What to review

1. **Two added rows,** one for each new path of the accepted unit. Neither had a planned row.
   - `crates/host/src/component_admission.rs` (opensip-host, composition, generated false)
   - `crates/host/src/component_admission_tests.rs` (opensip-host, test, generated false)

   Check each row's package, role, `generated` flag and description, with no claim beyond the accepted unit.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's changed path, whose inherited description the lead judges still true:
     - `Cargo.lock`: "Pin the host workspace dependency resolution for reproducible executable builds."
     - `crates/host/Cargo.toml`: "Declare this package, explicit dependencies and build targets."
     - `crates/host/src/lib.rs`: "Expose the intentionally public API; keep internal modules private."
     - `crates/security/src/crash_matrix_sites.rs`: "X9-1's pin of every source site that names a test-only feature (law X9 r1 item 6, law X8 r3 item 4b), in every security test build: it scans every cfg and cfg! in crates/*/src and crates/*/tests and requires exactly the pinned table, the shared fixture gates under the one joint predicate any(test, feature = crash-matrix, feature = scenario-fixtures) (Image::Injected with the injected image and synthetic V2 profile set, HomeSource::Fixture with the creator path on a scratch H and the gate's test constructor, X4T-0 and its accessor, and the fenced state.v1 publisher, each with the closure it needs), the crash-matrix-only carrier fixtures, each crate's guard and support module, the census tests and X9-0's and X9 r2's platform sites; with a scanner self-test, a no-sleep pin over X9-1's sources, and tests of the shared producers (accepted trust installed, the fenced publisher advancing the revocation version and refusing without writing while another holder has the fence, a writer admitted) and of the inherited carrier fixture."
     - `crates/security/src/lib.rs`: "Expose admitted security services and opaque authority-session types with private constructors; never expose an unchecked operational grant or journal checkpoint."
     - `crates/security/src/trust.rs`: "Admit signed trust metadata, root chains and closure associations."
     - `crates/security/src/trust/component_fixtures.rs`: "M3-C r8 item 8 (unit C2a-2; C2a plan r4, LD-C2A-6): the shared synthetic signed component fixtures, included in core_authentication's tests module under its joint test-and-fixture predicate (no new predicate site). Role-valid bodies of every CR-1 role with C2PM-1's closureProtocolMajor and trees from supplied bytes, every value encoded by the canonical encoder (any lawful path escaped exactly), and release rows labelled synthetic, signed only through the existing sign with the public test-only TR-COMPONENT signer under the existing synthetic root. No root, key source or feature; no authority."
     - `crates/security/src/trust/root_payload.rs`: "Compose the existing private root, recovery, profile, revocation and retained-input owners; keep their logical module ancestry and guarded public reexports unchanged. Extract the existing module body without changing its logical ancestry or visibility."
     - `crates/security/src/trust/trust_bootstrap_tests.rs`: "Check X4B-a (law X4B r5 item 10) on ACL-scratch installations holding 467's P0 publication under a supplied fence, with test-signed releases (public quorum62 seeds) produced into an InitialCore through 463's injected-image constructor: P0 is accepted with TR-BUNDLE, TR-COMPONENT, TR-CORE and TR-INDEX trusted from one EV-PRESENT-PAYLOAD each and the one confirming admission admits the store without writing; X4T-a's native reread and every record's canonical content address accept it; the fresh-install time rules (tEval = max(W, A), payload-future, beyond-horizon and its boundary) write nothing on refusal; an expired catalog, an expired root, a stale list, a revoked signer whose quorum survives and expired-and-revoked give their event sequences, accepted.by and revokedBy, and X4T's continuation row or ExistingOnly; inactive and rejected entries record no event; a revoked counted signer that leaves a catalog or component manifest below threshold writes nothing; a missing catalog or a document signed outside its role writes nothing; no component manifest leaves TR-COMPONENT unbootstrapped; a crash before the pointer and a rerun; a changed state.v1; a short ledger; a non-P0 predecessor and a foreign root binding; and a two-root chain recorded in full, with the reader's current FirstIdentity refusal pinned as a stated gap."
     - `crates/security/src/trust_admitted_components.rs`: "M3-C r8 item 7 (unit C2a-1): the trust owner's read-only bridge to the components the ordinary reader verified. Each AuthenticatedComponent lends its authenticated body bytes, verified envelope, validated manifest, CR-1 kind and catalog release row by reference; only the trust owner constructs one, and it authorizes nothing. A test holder runs real body validation with test release and envelope stand-ins."
     - `crates/security/src/trust_ordinary_metadata.rs`: "Bind catalog, manifest and revocation metadata to the admitted root chain and host context with calendar and namespace constraints."

     Judge each against D4-2's change: security `lib.rs` and `trust.rs` re-export the admission view (and, under the joint fixture predicate, its fixture components); `trust_admitted_components.rs` gains the view; the ordinary reader keeps its reserved set; `root_payload.rs` gains the fixture bodies (an append); `component_fixtures.rs`'s release rows take their identity from the body; `trust_bootstrap_tests.rs` gains two controls; `crash_matrix_sites.rs` names fixture gate 9 and its five sites; host `lib.rs` declares the module, host `Cargo.toml` the components edge, and `Cargo.lock` its line.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 91 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** D4-2 changed no census-bound file (its lane's `census-closure-unchanged` check). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 447 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 192 and re-points every inherited passage row to v232. The contract successors stay at 177. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "4c8bf623c07f150d3a388e7807065fe4e133c56bf823b8e0708dadae32dc1207",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v232.json",
    "bytes": 762267,
    "sha256": "c36f25247e6b6ef1c92bf61eb26fbc47a5c0217cb943a1f3da5eeeb58bd620c4",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v231.json",
      "bytes": 760618,
      "sha256": "f93e6e821788f81dcefcffebeb715f18e096b154d16287c3e2d5ff44a78cfcd3"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d4-2-inventory-v232/successor.json",
      "bytes": 6051,
      "sha256": "b338c6f801cff6c9309096d91dbd3c47ad5e92314d28e6a943dfec2fbd78b6bb"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
