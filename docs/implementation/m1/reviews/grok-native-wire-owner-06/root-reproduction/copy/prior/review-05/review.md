# Review 05: resumed independent review of native wire owner, author candidate 05

**Verdict: changes-required.** Two narrow required findings remain; there are four advisories.

**Standing.** This review resumes my review-03 and review-04 context; it is not a fresh session. It covers this unit and the source-bridge coherence the unit requires. It does not qualify the product, a full provider sender or admission, the generator, M2/M3, the platform or system libraries, and it promotes no source.

## Custody

**Subject:** `m1-native-wire-owner-subject-05`, sibling manifest `7b9d94c3…6f1d`.

| Check | Before | After |
|---|---|---|
| Files | 102/102, no extra, missing or mismatched files | 102/102, unchanged |
| Bytecode | none | none in subjects 03, 04 or 05 |
| Architecture pins | 44/44 match (8 new registry-closure documents) | 44/44; HEAD `c3856824` shows 12 modified and 18 untracked |
| Node pin | matches | unchanged |

- **Inner manifest.** `40a79ffe…6735` lists 40 inputs, 4 outputs and 57 evidence files; together with the manifest itself that equals the outer 102.
- **Retained evidence.** `prior/review-04/*` is byte-equal to my review-04 files. `prior/root-validation-04/*` is byte-equal to root's directory. `prior/subject-04*` is byte-equal to the frozen subject-04. All 38 files of subject-04's `prior/` tree reappear unchanged in subject-05.
- **Method.** Pins were parsed as text and nothing was imported from any frozen subject. All execution ran from my own copies with `-I -B` and a private pycache.

## Reproduction (only the 40 inputs, `scratch/copy`)

- **check.py:** 567 checks, 0 failed. Ids, outcomes and details are identical to the frozen result. Closure: 44 architecture reads, 0 unpinned, 0 bytecode, 28 subject reads with 0 unlisted, 13 pinned Node executions.
- **selftest.py:** 132/132 controls caught, with a clean baseline.
- **Root validation-05:** I saw only check output (567/0 in `stdout.txt` and `result.json`). I claim no root selftest or isolation result. The receipt confirms root04 ran only 478 checks.

## Review-04 dispositions

### RF-1 prepared limit bypass: resolved

These cases ran through the actual owner with the successor installed:

| Case | Owner | Successor |
|---|---|---|
| Defaulted, 257 rows, 1 stale | fallback, 256 usable | fallback, 0 usable, disclosure `257>256`, stale row kept |
| Defaulted, 256 rows, 1 stale | fallback, 255 usable | unchanged: fallback, 255 usable |
| Defaulted, 300 rows, all stale | fallback | fallback, 0 usable, 300 stale kept |
| Explicit, 257 rows, 1 failed | admitted | refused |
| Defaulted, 257 rows, 1 failed | admitted | fallback |
| Defaulted, stale row with over-limit blob | fallback | fallback |
| Explicit, stale row with over-limit blob | stale refusal | stale refusal keeps precedence |

- **Carried rows versus usable rows.** Counting carried rows rather than usable rows is justified by the real owner: `prepared_output_set_identity` hashes every row, and dropping one row changes the identity.
- **Planner.** It now refuses 257- and 299-entry manifests.
- **Mutants caught:** admitted-only outcome filter, usable-only count, entry bound off, fallback dropping stale evidence.

### RF-2 dialect scope: resolved

- **Scoped instances.** Only `NE_S`, `ST_S`, `WI_S` and `IM3_S` hold a `ScopedCanonical`. `NE_S.IM`, `NE_S.STARTUP` and `NE_S.WIRE` do not.
- **Marks.** They exist only in the scoped evidence copies (129 in each), the occupancy companion (2) and the IM3 relation-registry copy.
- **Validation logic.** `ScopedCanonical.validate` replicates pinned `canonical.validate` exactly.
- **Real consumers.** Each gives the same result pinned and scoped on `a/b`, `a/..<LF>`, `x<LF>/../y` and a 64-hex value followed by LF:
  - `IM3.validate_registered_record` for identity v3 and v2 `LogicalPath`;
  - `NE.validate_workflow` for workflows common;
  - `NE.validate_foundation` and `NE.IM.validate_registered_record` for identity v2.
- **c2v3 and rust2.** They have no consumer in the loaded models.
- **Mutants caught:** NE-only scope, and a view that makes every node ECMA.

### RF-3 relation-payload CanonicalPath: resolved for the terminator defect

Through IM3, pinned vs scoped:
- `x<LF>/../y.rs` goes from admitted to refused;
- `a/..<LF>` goes from refused to admitted.

The no-relation-row mutant is caught. The remaining relation path law is covered in A-1.

### RF-4 Cancel law: partly resolved

- **Position.** A Cancel at position 0 is refused as `cancel-before-hello`, and the expected echo is accepted at positions 1–9.
- **Wrong fields.** Wrong execution, ordinal or reason are refused.
- **Mutants caught:** the payload-bytes and request-limit survivors from review 04, echo checked by size only, and an ordinal allowed before Analyze.
- **Still open:** new RF-1.

### Advisories A-1…A-5: resolved or retained

- **A-1:** the remedy phrase is now bound, and the review-04 survivor is caught.
- **A-2:** defensive branches are labelled and exercised.
- **A-3:** precedence is stated, and my probes confirm it.
- **A-4:** integration duties are declared.
- **A-5:** pins are retained.

## Required findings

### RF-1: Cancel echo is bound to the plan, not to what was actually sent, and the comparison is type-lax

**Evidence** (`probe_05.out.json`, section S).
- **The owner law.** CANCEL-NULLABILITY requires the executionId to be the exact value of the OpenUniverse that was **sent**. Slots bind sequence, type, coordinates, seal counts and byte length only.
- **Planned echo accepted.** Send an OpenUniverse whose `executionId` is a same-length substitute (`…0000` instead of `…0001`), then a Cancel echoing the planned `…0001`. The sender **accepts** it, although that Cancel does not echo what was sent.
- **True echo refused.** The same transcript with the true echo of the sent value is **refused** (`cancel-echo`).
- **Content not bound.** A SnapshotManifest whose `manifestSha256` is substituted with a same-length digest is consumed as complete.
- **Type-lax equality.** `analysisOrdinal: False` against a planned `0` is **accepted**, because Python treats `False == 0`. The carrier refuses it with `TYPE_UINT64`.

**Fix.**
- Bind each slot to its planned payload identity (a digest of the planned deterministic-CBOR payload), or at minimum to the OpenUniverse `executionId` and Analyze `analysisOrdinal`.
- Derive or check the Cancel echo against what was actually consumed.
- Compare Cancel payloads by deterministic-CBOR bytes, not Python equality.
- Add vectors for both counterexamples.

### RF-2: Provenance and authority wording

- **Root attribution.** `contract.md:7` says root reproduced 478 checks and 108 mutants. The receipt `docs/implementation/m1/trials/native-wire-owner-04/root-validation/receipt.json` records `rootSelftestExecuted: false`, and root's stdout contains only 478/0. Correct the attribution and cite the receipt.
- **Owner claim.** The `OWNER-PATTERN-EVALUATION` rule states that `owner-pattern-successor.v1.json` is "the selected final owner". Its own standing, however, says it is an author candidate applied in memory and is not approval, and source-bridge promotion is still owed. Reword it as the proposed reference owner correction within its closed scope, effective only after root acceptance and promotion. Add a check against authority claims for unpromoted successors.

## Advisories

### A-1: `_is_path` in fact-plane

**Assessment:** not a live fact2 contradiction, but the author's framing is inaccurate and a relation-registry duty remains.

- **What the fact-plane v1 normative text says.** `sharedTypes.CanonicalPath` forbids only empty, `.` and `..` segments, a leading slash and backslash. The no-C0/C1 rule belongs to `CanonicalText`.
- **Why the checker is stricter.** `check-fact-plane.py` `_is_path` reuses `_is_nfc_text`, so it is stricter than its own type. It is the historical v1 CBOR-profile checker.
- **What fact2 admission actually does.** Retained fact2 admission (identity-model.v3 `registered_payload`) validates the relation v2 schema and scans for NFC and negative integers only; it never calls `_is_path`. A legitimate `a<LF>b` file, which the wire admits, is therefore not refused by fact2 payload validation. The contract's claim that such names "would still be refused at fact-plane admission" conflates two different admissions and should be corrected.
- **The real remaining gap** (`probe_05b.out.json`). Relation v2 `CanonicalPath` admits `a//b.rs`, `a/` and `a<BEL>b.rs`, both pinned and scoped. This happens even though the inherited type forbids empty segments and v2 claims every inherited restriction survives.
  - `FilePayloadV1.path` is guarded only by its snapshot-inventory join, which was not executed here (no `admit_frame` run).
  - The join laws for `PackagePayloadV1.manifestPath` and `VcsChangePayloadV1.previousPath` still need checking.
  - Record this as a relation-registry/fact-plane duty; it does not block this unit.

### A-2: Worker read authority for partial-stale fallback

The manifest carries stale and failed rows but no designation of which rows are usable. Specify one of two approaches:
- the worker recomputes PO-1 from `inputBinding` against its own admitted context and skips `status=failed`; or
- the host sends the owner partition.

### A-3: Carried-row counting is stricter than owner usability

A defaulted set of 257 rows with one stale row loses all 256 usable rows. This is accepted as the wire consequence of set identity; keep the vector.

### A-4: Pins and trust boundary

- Root binding must retain all 44 exact bytes: 12 modified and 18 untracked, including the 8 new documents.
- The Node system libraries are trusted and unpinned.
- The audit is not confinement.

## Reviewer mutants (`scratch/mutants.out.json`)

All 12 are caught.

**Review-04 survivors, re-seeded:**

| Mutant | Checks failed |
|---|---|
| NE-only scope | 37 |
| sender payload-bytes check removed | 3 |
| sender request-limit re-check removed | 3 |
| generated-file phrase dropped from the remedy | 1 |

**New:**

| Mutant | Checks failed |
|---|---|
| Cancel echo checked by size only | 10 |
| ordinal echoed before Analyze | 3 |
| limit applied to admitted outcome only | 11 |
| usable rows counted instead of carried | 5 |
| entry bound off | 6 |
| every node evaluated as ECMA | 5 |
| relation row removed | 2 |
| fallback drops stale evidence | 3 |

RF-1 has no mutant because the current code already accepts its counterexamples.

## Preserved and corrected evidence

- **Author disclosures, preserved:** the `succ.py` parse break, a first full run of 567/1, and a wording mismatch.
- **Review-04 evidence, preserved:** its failed controls and survivors, byte-equal.
- **Root attribution:** corrected by root's receipt, not by rewriting history; RF-2 asks the contract to follow the receipt.

## Remaining integration duties

- source-bridge promotion of the pattern rows and scope (after RF-2);
- production Rust/TS matchers;
- an M3 sender with a content-bound Cancel echo (RF-1);
- M3 worker prepared read authority (A-2);
- the relation-registry path law and a full `admit_frame` run (A-1);
- generator work, the renderer rebase and the D9 exit-contract successor.

## Untested limits

- **No retained admission run:** `admit_frame` over a retained Run bundle was not driven.
- **Not qualified:** production sender, admission, codec, generator and platform.
- **Rust regex lowering:** not executed.
- **Author checks relied on:** the TS2 Cancel position cross-check and the plan realizations came from author checks, not my own code.
- **Root's run:** selftest and isolation not observed.
