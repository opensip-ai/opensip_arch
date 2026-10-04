CODEX2 review: **CR-1**, the security and DR-103 host-vocabulary contract successor that carries out item 7 of law M3-C (CODEX2 accepted r6 and r7). It adds the closed role-to-kind table and widens the component-manifest `role` vocabulary to five roles. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-cr-1-r1`.

(Lead note: this request was first written for Codex. CODEX2 reviews it, because it was free. Product main is now `cd5958b` (82 contract successors); the unit binds there, 82 → 83, per its `verify_scratch`. Don't run cargo; P0's lanes are using the machine.)


**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests, no generator and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** The lead ran the real `tools/verify_design.py` in the scratch harness (`evidence/verify_scratch.py`). The harness writes nothing; it holds a synthetic review and assent in memory. You may rerun it. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**
- **Product main is `9c11c53`**, read only: B-S1's binding, with 79 contract successors. The record is built on it.
  - The checkout has since advanced to `cd5958b`, which binds B-S2, B-S9 and I1-P (82 successors) and X4-F1.
  - The README records that CR-1 also binds there.

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/snapshot-plan-c/cr-1-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 9 members** are:
  - `cr-1/successor.json`;
  - `README.md`;
  - `PASSAGES.md`;
  - `completion/manifest-schema.completed.v1.json`, the successor copy;
  - `materialization-map.json`;
  - `evidence/copies-report.json`;
  - `evidence/build_cr_1.py`, `check_cr_1.py` and `verify_scratch.py`.
- **Not part of the subject:** `cr-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Law.**
- `snapshot-plan-c/PROPOSAL-r7.md` (`a1ee9386…`) is your r7 acceptance:
  - item 7 is r7:360-396, and its table r7:370-376;
  - the CR-1 row is r7:1053, and R2 r7:1211.
- r6 (`8274bca1…`) has the same item 7.
- Consumers:
  - M3-E1 r3's CR-1 row (`syntax-e/PROPOSAL-r3.md:697`);
  - M3-D r3 item 24, D4 at R10a (`supervisor-d/PROPOSAL-r3.md:718`).

## What it does

The README has the full tables. In brief:
1. **SL:70** (`docs/v2/contracts/product-v1/security-and-lifecycle.md`). After S1's closure-association paragraph (SL:21-70), a new block, **Component roles and closure kinds**:
   - **the table, word for word MC item 7's:** `analyzer` to `provider`, and `toolchain`, `stdlib`, `rust-dev-llvm` and `grammar` to the kind of the same name;
   - **where the kind comes from:** only from `role`, never from a caller, path or other field. A role/field kind mismatch refuses.
   - **roles that do not exist:** `evaluator`, `detector`, `adapter` and `core` are never roles;
   - **the closure-only roles.** The four non-`analyzer` roles are closure-only: never launched through the manifest, and read only as closure bytes. Their manifests declare `capabilities: []` and `permissions: []`. The `entrypoint` is a committed regular file under RJ-3 that need not be executable and is never executed. Commands are never mounted or dispatched.
2. **DR103** (`docs/coop/artifacts/component-manifest-schemas.v11.json`), two JSON Pointer strings on the `role` field:
   - `/manifestSchema/fields/7/type` gets the M3 vocabulary;
   - `/manifestSchema/fields/7/semantics` gets the closure-only sentence.
3. **A complete successor copy of the completed manifest schema** (`docs/coop/completion/manifest-schema.completed.v1.json`, `a5140714…`).
   - **Why a copy.** That schema is not a `verify_design` input. The architecture application pins it in clause `M.SCHEMA`, and it is the product's `tools/security/inputs/manifest-schema.json`. So it cannot be a parent, and the copy is a new candidate.
   - **The one edit:** `/properties/role` changes from `{"const": "analyzer"}` to the five-role enum, in the parent's own serialization.
   - **Selection** is declared in the record's `standing`, B-S9's form.
   - **C2a** materializes it (`materialization-map.json`).
4. **A role-case audit.** No existing negative role case uses a new role:
   - the arch cases' `builder`;
   - the product shape fixture's 55 role cases;
   - the semantic fixture's `REQUIRED/role` and `TYPE/role`.

## Lead decisions for you to rule on

The README records seven, each with the alternatives it rejects:
- **LD-1.** The table goes in SL S1 and the vocabulary in the DR-103 role field.
- **LD-2.** A complete copy widens the enum, with `$id` and `manifestSchemaVersion` unchanged.
  - **Why:** the change is additive and old hosts fail closed.
  - **Rejected:** a major bump; per-role `oneOf` branches; overriding the application's pins.
- **LD-3, the substantive one.** The four non-`analyzer` roles are **closure-only**, with four field rules.
  - **Why:** without them, a `stdlib` or `grammar` component would need a dummy executable entrypoint, because the completed checker and `crates/security/src/component_manifest.rs:337` refuse `ENTRYPOINT_NOT_EXECUTABLE_FILE`. E1's closed grammar tree cannot carry one at all.
  - **Rejected:** no per-role rule; dropping `entrypoint` or `commands`; a second manifest `kind`; executable entrypoints for `toolchain` only.
- **LD-4.** `evaluator`, `detector`, `adapter` and `core` never become roles.
- **LD-5.** The selection is declared in the record. The completion contract's "initial role vocabulary remains exactly `analyzer`" becomes historical.
- **LD-6.** No new refusal code.
- **LD-7.** C2a materializes the copy; binding-only product commit first.

## Decide

1. **Exactness.**
   - Is every `before` the exact parent text?
   - Does every `after` only insert?
   - Is SL's table exactly MC r7:370-376, and are its rules exactly MC:368-385?
2. **LD-3.**
   - Are the closure-only rules right and minimal: the role-scoped executable entrypoint, empty capabilities and permissions, and commands never mounted?
   - Does a closure-only manifest need any other field rule? Look at `compatibility.providerProtocol`, which the README notes, and at `dependencies` and `declarations`.
   - Do the rules conflict with M3-D r3 item 24's R10a exclusions EE-1 to EE-5a, or with E1's grammar closure?
3. **The copy (LD-2, LD-5).**
   - Is it exactly the completed schema with one edit, in its own serialization?
   - Is declaring its selection in the record, for a schema `verify_design` does not track, a sound successor?
   - Is the role-case audit complete?
4. **Consequential passages.** Does any other accepted passage still enumerate the role vocabulary as `analyzer` only, or derive a kind any other way? Look in SL, BP:699-720, DR103, IE, NE and the D law.
5. **Selection.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules, alone and after CRC-1? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/snapshot-plan-c/cr-1/`:
1. `evidence/build_cr_1.py --check` rebuilds every generated file in memory and compares it with the files on disk. It reads the product lock, the schema input and the fixtures at `9c11c53` with `git show`. The product shape fixture is 55 MB.
2. `evidence/check_cr_1.py` runs the independent checks: pins, `before`s, inserts, the DR103 mask, the table against MC r7, the copy against its parent, the application pin and the product input, the report, the map, the audit, and the README's passage list. `--rev cd5958b` also passes.
3. `evidence/verify_scratch.py --rev 9c11c53` binds 79 to 80. `--after-crc-1` binds CRC-1 first, giving 81. With no `--rev`, it uses the checkout (now `cd5958b`, 82 to 83) and also checks generation and admission sources.

The lead ran each twice, with byte-identical generated files.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `cr-1-subject.json`. The lead's value is `f0a5c22231a4a6c942817ce8fd311f1edf0ad58f298e8c8d9eff3cbbaa46a3d9`.
- `"successor"`: `{path, bytes, sha256}` of `cr-1/successor.json`. The lead's value is 7822 bytes, `a0e23ed18868b888f9f6c8b464fb6f2efc8bb2d423146048b9370b42122fb471`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement text. CRC-1 (`codex-crc-1-r1`) is the sibling unit. The two share no parent and can be reviewed in either order. Do not commit.
