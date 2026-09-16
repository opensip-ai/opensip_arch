# Independent review 03: native TS2/Rust3 wire owner, candidate 03

**Verdict: changes-required.** Four required findings and nine advisories follow.

**Standing.** This is an independent review only. It is not approval, source promotion, a production codec, admission or generator, or M2/M3/release qualification. Nothing was committed or pushed, no subagents were used, and no private sessions were read.

## Custody

**Subject.** `/tmp/opensip-implementation/m1-native-wire-owner-subject-03`, with outer manifest sha256 `2d68beaa22d69c4b4296f882db25072bd6e5088eb06bb0d73c6dfb038490cbf4`.

**Before the review: PASS.**
- **File set:** 64/64 hashes and lengths match; the walk finds 64 files with none extra or missing.
- **Inner manifest:** `subject-files.json` has sha256 `919202c8…cf0` and lists 35 inputs, 4 outputs and 24 evidence files. Together with itself that equals the outer 64, and `tools/filelist.py` INPUTS equals the inner input list.
- **Architecture pins:** 36/36 match. HEAD is `c3856824`; relative to it the pinned files show 12 modified and 11 untracked.
- **Node:** the pin matches (sha256 and bytes).
- **`prior/`:** all 24 evidence copies are byte-equal to the review-01 and review-02 scratch files and the subject-01/02 originals.

**After the review:** see the last section.

## Reproduction

I copied exactly the 35 declared inputs (without `subject-files.json`) to `scratch/copy` and ran them with `env -i PATH=/usr/bin:/bin`, the reference interpreter with `-I -B`, and my own `TMPDIR`.

- **check.py: 373 checks, 0 failed.** Ids, outcomes and details are identical to the frozen output. The closure shows 36 architecture reads, 0 unpinned, 0 bytecode, 0 hidden `/tmp` reads, 23 subject reads with 0 unlisted, and 4 executions, all of the pinned Node.
- **selftest.py: 78/78 caught**, with a clean baseline. Root's own selftest is separate and is not claimed here.

## Prior findings

| Finding | Disposition |
|---|---|
| Review-01 RF-1 hidden inputs | Resolved: the 35-input copy runs and no outside reads occur |
| Review-01 RF-2 pins/closure | Resolved: 36 pins are checked before and after the run; the registry is now pinned |
| Review-01 RF-3 PreparedOutput | Resolved, with residue: defaulted-mode application (new RF-3) |
| Review-01 RF-4 ProviderFault | Resolved and retained: `provider-fault-refusal-same-d9` passes. P3-29 is the only Cancel row and P3-22 the only Analyze row. The race model was not re-run |
| Review-01 RF-5 paths | Resolved for the listed members, with residue: other extern path members (new RF-1) |
| Review-01 RF-6 packageKey | Resolved: NFC is now refused at set admission |
| Review-02 RF-1 route join | Resolved, with residue: the owner functions derive the termination, envelope and exit, and the real schemas validate. The binding is self-consistent in places (new RF-3, A-2) |
| Review-02 RF-2 representability | Resolved, with residue: the arithmetic is independently reproduced. Open: the owner crash (new RF-2), sender binding (new RF-4), and A-4, A-5, A-6 |
| Review-02 RF-3 patterns | Resolved: my own closure gives 54 sites and 53 lowerings exactly. Integration residue: new RF-1 and RF-2 |
| Review-02 A-1…A-7 | All resolved. A-3 has residue (A-6); A-6's digest covers only the function body (A-9) |

## Independent assessments

### Boundary sizing: accepted

- **Prefix exclusion is owner law, not an author choice.** rust2 `limitPolicy.aggregateAccounting` says totals "include exact canonical-CBOR envelope payload bytes and exclude each 40-byte transport prefix", and `framing.lengthScope` is "payload bytes only".
- **Encoder agreement.** My own deterministic-CBOR length function agrees with the owner `wire_cbor` on 216 materialized chunk frames. They span the sequence, index, offset and byte-string head thresholds.
- **Recomputed boundaries.** From real small encodes plus closed form, with no multi-GiB allocation:

  | Quantity | Recomputed value |
  |---|---|
  | Dependency manifest, per 24-scalar entry | 204 bytes |
  | Dependency manifest, published groups | 67108864 at the limit, 67108865 one over |
  | Request | 9663676416 at the limit (9222 frames; the reserved Cancel is 151 bytes), 9663676417 one over |
  | Small request | 6834 bytes, 10 frames |
  | `maxRequestFrames` bound | 796198 (minimal dependency entry 116 bytes, minimal snapshot entry 135 bytes) |

### Chunk units: frame-minimal, not byte-minimal (RF-4)

- **Units and metadata.**
  - Chunks carry 1..max bytes.
  - Zero-length entries have no chunk.
  - The Seal carries `totalChunkCount`.
- **Frame count.** Greedy chunking minimizes the frame count. It is also byte-minimal on 10683 exhaustive compositions that stay below the CBOR head thresholds.
- **Across a threshold.** Greedy loses. The owner encoder gives `[6,24]` = 457 bytes and `[7,23]` = 456 bytes, against greedy `[24,6]` = 458.

### Cancel reservation: accepted, meaning to be stated (A-7)

- **Only one Cancel.** P3-29 allows exactly one Cancel, and its reason is const `user-interrupt`.
- **It counts toward totals.** Every host-to-worker envelope counts toward the request totals.
- **What the reserve buys.** Reserving it keeps an interrupt at D9 130 rather than a worker limit fault. The cost is that requests fitting only without the Cancel are refused.

### Two new public detail codes: necessary

- **Why a code is needed at all.** `failure_envelope_errors` (model 1130–1146) uses `route.envelopeDetail` whenever `domainDetail` is absent. The owner `envelopeErrorsComposition` law says such a route "still owes the envelope a detail". Root's earlier permission for detail-absent internal routes therefore still needs one registered envelope code per route. The owner precedent added four members for exactly this reason.
- **No existing member fits honestly:**
  - `PROJECT.SCOPE_LIMIT` covers selection arrays;
  - `native.prepare-bound-exceeded` is operational-failed with `HOST.IO_FAILURE`;
  - `EVALUATION.OUTPUT_BOUND_EXCEEDED` belongs to the identity evaluator;
  - `native.release-declaration-invalid` names a malformed declaration.
- **Registered, typed and scoped correctly:**
  - registered through successor rows (records, enum, remedies) and typed by real `StepTermination`/`DomainDetail` validation;
  - correctly not aliased;
  - correctly absent from `D9_MAP`, like the precedent `native.release-declaration-invalid`.
- **Weakness:** the condition-to-code and remedy binding is not executed (A-2).

### New origin `admitted-plan-input`: necessary

- **Why a value is needed.** `possibleOrigins` must be non-empty, and the derivation refuses any other origin.
- **No existing value fits.** None of the five existing values describes repository, lockfile, vendored or preparation input.
- **Law consistency.** Under `originatingBoundaryLaw`, external input maps to request-rejected, which is what these routes use.

### Consistency with the original routes

Class and exit (request-rejected, 2) are consistent. The errorCode of the two limit keys is not (A-1).

### Pattern closure and dialect

- **Closure.** My walker covers every subschema keyword, tracks negation across `$ref` and uses a separate lowering lexer. It yields exactly 54 sites: 13 distinct patterns, 22 extern roots and 66 refs.
- **Lowering list.** It gives the same 53 lowering sites. Only lookahead and `.` force lowering for these patterns, and none uses `\d`, `\w`, `\b`, `\p` or a bare `\s`.
- **Integration.** There are two consequences, covered by RF-1 and RF-2.

## Required findings

### RF-1: a newline-hidden `..` segment is admitted in extern path members on the Rust3 wire

**Evidence.**
- **The pattern admits it.** Under pinned Node with `/u`, the Native2 CanonicalPath pattern admits `x\n/..`, `x\n/../y`, `a /../b` and `a\n\n/../../etc/passwd`. The lookahead's `.*` stops at the line terminator.
- **The owner admits it.** `_LOGICAL_RE` and `prepared_output_set_admit` admit a generated `logicalPath` of `x\n/../../escape.rs`.
- **The carrier admits it.** `PreparedOutputManifest` admits that row, and `OpenUniverse` admits `crateRootPaths=["x\n/../y.rs"]`. The validator is live: `../y.rs` is refused in both.
- **Only one of six sites is covered.** Of the six sites for this pattern, only the dependency manifest path is in `CANONICAL-PATH-ADMISSION.externMembers`. The other five rely on the pattern alone:
  - `ExpansionSiteV1.path`
  - `GeneratedFileV1.logicalPath`
  - `crateRootPaths`
  - `jsRootFiles`
  - `programRootFiles`
- **The candidate codifies the defect.** The defect originates in the owner, but the candidate's closed, normative pattern closure and lowering law now require generators to reproduce it.

**Fix.**
- Apply a segment lexical rule to every path-valued extern member, recomputed from the carrier graph. Alternatively, publish a scoped successor that corrects the pattern and gives it a refusal route.
- Add vectors: `x\n/../y` refused; `a\nb` admitted.

### RF-2: dialect divergence makes owner set admission raise, with no route

**Evidence.**
- **The declared law admits these paths.** `a/..\n` and `..\n` are legal dependency file names. The ECMA pattern, `canonical-path-segments` and the `DependencySourceManifest` carrier all admit them.
- **The owner raises instead.** The owner `dependency_source_set_admit` raises `jsonschema.ValidationError` via `file_manifest_identity`, `native_identity` and `validate_native` (Python `re`).
- **The successor inherits it.** The successor calls the owner first, so it raises too. There is no set identity, no DS refusal and no route.
- **Prepared sets behave the same.** A generated `logicalPath` of `a/..\n` makes `prepared_output_set_admit` raise, while the carrier admits the manifest.
- **The existing check is too narrow.** `owner-model-uses-python-re` probes only `validate_native`. The "owner refusals keep precedence" selector contract fails for these inputs.

**Fix.**
- Select one final owner. Either:
  - (a) publish a successor that evaluates owner patterns under ECMA /u at set admission and identity; or
  - (b) refuse the strings on which the two dialects disagree, with a routed key, before owner identity.
- Add vectors that execute the owner set admission, so each input ends as admitted or a routed refusal, never an exception.

### RF-3: prepared route row says "explicitly selected", but defaulted mode is refused too, and nothing pins it

**Evidence.**
- **Defaulted mode is refused.** With 257 fresh inert rows and `explicit=False`, the owner returns `admitted` and the successor returns `rejected` (`…:entries`).
- **The owner's sibling rule does the opposite.** Its defaulted-mode law for PO-1 staleness is fallback with disclosure.
- **Nothing pins either behaviour.** Mutant `m_prepared_refuse_only_explicit` fails 0 of 373 checks.

**Fix.**
- Decide between refusal and non-prepared fallback with disclosure.
- Align the selector `applies` field and the row condition with that decision.
- Add a defaulted-mode vector.

### RF-4: planner acceptance does not bind the sender's chunking

**Evidence.**
- **No sending rule.** `REQUEST-WIRE-ACCOUNTING` plans greedy chunks, but nothing requires the host to send them. `CHUNK-CUSTODY` and rust2 only require contiguous chunks of 1..max bytes.
- **Acceptance side.** A host that sends smaller lawful chunks after acceptance can exceed the request bytes or frames. For example, one extra frame at the 9663676416 accept vector costs at least 100 bytes. The worker would then fault.
- **Refusal side.** Greedy is not byte-minimal (457 against 458 above), so a refusal at the exact boundary does not prove that no lawful encoding exists.

**Fix.**
- Make the planned sequence normative for the sender: every chunk except an entry's last is exactly max bytes.
- Qualify the refusal as "under the normative host chunking".
- Add a control where a non-greedy transcript is non-conforming.

## Advisories

- **A-1.** The limit keys copy `REQUEST.PRECONDITION_FAILED` from the release-declaration row, while the owner's bound-exceeded family (`PROJECT.SCOPE_LIMIT`, `native.too-many-units`) uses `REQUEST.UNSATISFIABLE`. Justify the choice or obtain a root decision.
- **A-2.** Route semantics are bound only as self-consistent copies. Each of these mutants fails 0 checks:
  - swapped envelope details between the two keys;
  - a wrong remedy text;
  - the dependency selector timing moved to `plan-time-no-spawn`;
  - the origin meaning rewritten as a host invariant.

  `remedyKeyingConstraint` is asserted, not executed.
- **A-3.** Plan-time refusal happens after PlanId. State the fate of `plan2` and that no `run3` or Coverage is minted. The line-2848 anchor gives timing only: that step's existing outcome is Coverage unknown, not a refusal.
- **A-4.** TS2 has no exact frame-boundary vector. A doubled TS2 frame limit fails 0 checks.
- **A-5.** Seal `totalChunkCount` is unpinned. Counting a zero-length entry as one chunk fails 0 checks.
- **A-6.** A set-admission vector for `a\n/../b` is missing. Skipping the lexical check for newline-bearing paths fails 0 checks.
- **A-7.** State the reserved-Cancel meaning: exactly one Cancel (P3-29), counted in the totals, keeping an interrupt at exit 130.
- **A-8.** Root binding must retain the 36 exact pinned bytes (12 modified, 11 untracked). The Node binary is pinned; its system libraries are trusted and unselected. The audit is closure evidence, not confinement.
- **A-9.** `ownerFunctionSourceSha256` covers only the function body. Callee changes are caught only by the whole-file pin.

## Reviewer mutants (`scratch/mutants.out.json`, each run through check.py)

**Caught:**

| Mutant | Checks failed |
|---|---|
| `reserveCancel` off | 10 |
| prefix included | 7 |
| chunk byteOffset head wrong | 4 |
| `maxRequestFrames` unenforced | 2 |

**Uncaught (0 checks fail):** swapped envelope details, dependency timing moved, wrong remedy text, origin meaning, prepared refused only when explicit, seal zero-length count, newline lexical skip, TS2 frame limit ×2.

## Untested limits

- **Not run or assessed:**
  - No generator, production codec or M2/M3 artifact was run.
  - The P3 race model, commitment classes, scope2, the TS2 digest and field coverage were not re-derived; I rely on author checks.
- **Rust regex:** the crate is not available offline. Lowering needs were judged from documented semantics, not executed.
- **Real-world reach:** newline-bearing file names in real crates or generated outputs were not measured, and the traversal was not executed in a real worker VFS.
- **Background process:**
  - One over-large foreground enumeration was auto-moved to the background by the tool harness at the timeout.
  - I terminated it (exit 144) and reran a bounded version in the foreground.
  - No background output is used.
- **Audit scope:** open and Popen events only.
- **Root's selftest:** not claimed.

## Custody after the review

**PASS, after I removed my own stray bytecode files.**

- **File set:** the outer manifest still has sha256 `2d68beaa…0cbf4`, and the walk finds 64 files with none extra, missing or mismatched. The directories are only `inputs`, `prior` (and its three subdirectories) and `tools`.
- **Pins:** all 36 match, with HEAD `c3856824` showing 12 modified and 11 untracked. The Node pin is unchanged. The evidence is in `scratch/custody-after.json`.

**Reviewer error, disclosed.**
- **What happened.** My first custody scripts imported `tools/filelist.py` and `tools/common.py` straight from the frozen subject with system `python3` without `-B`. That wrote `tools/__pycache__/filelist.cpython-314.pyc` (20:36:12) and `common.cpython-314.pyc` (20:36:25) into the subject.
- **Why the before-walk still saw 64 files.** It had already run earlier in the same script.
- **How it was found and fixed.** The first after-check saw 66 files. The mtimes match my scripts, so I removed exactly those two files and the empty `__pycache__` directory. A re-verification that imports nothing from the subject then passed 64/64.
- **Impact.** No byte listed in the manifest changed. All reproduction ran from `scratch/copy` with `-I -B` and forced pycache prefixes, so neither check.py nor selftest.py ever read the stray files. A similar stray `common.pyc` in my scratch copy, left by the closure probe, was also removed; it did not affect any run.
