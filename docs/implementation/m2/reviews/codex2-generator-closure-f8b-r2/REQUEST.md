CODEX2 review: F8b, the generator-closure and TypeScript-lane-registry contract successor, **proposal r2**. Claude Opus 5.5 leads. Verdict wanted: **ACCEPT** (proposal) or **REQUIRED-FINDINGS**. The unit's ACCEPT-DESIGN-UNIT review comes later, on the frozen subject manifest, after the observed rebuild.

Write only under `/tmp/opensip-implementation/reviews/codex2-generator-closure-f8b-r2`.

**Rules:**
- Read-only. Run no cargo, Node or generator; the crash-matrix evidence run is still active on this machine.
- Never touch the real home. Never read the 413 fixture. Do not commit.

**Subject:** `docs/implementation/m2/generator-closure-f8b/PROPOSAL.md`, 25864 bytes, sha256 `cf7e118358fa4831f1ff3b4ade7ab9f7efed0d7100b811ed631336d76e4feb49`.

**Previous round:**
- r1 is kept byte-identical as `PROPOSAL-r1.md`: 16874 bytes, sha256 `f3162181aa65aeb63266df162147d6e6e366862a76c011610becf9126fba9833`, the subject you reviewed.
- Your r1 review is copied to `docs/implementation/m2/reviews/codex2-generator-closure-f8b-r1/`, byte-identical to your `/tmp` output. It found F8B-RF-1 (required) and F8B-NBO-1 (non-blocking).
- `diff -u PROPOSAL-r1.md PROPOSAL.md` shows every change.

**Product:** `/Users/sb/code/opensip-ai/opensip`, main `3e64266`, which is F8a integrated on `30c5db1`. F8a changes only `tools/contracts/dependency-policy.json` and `tools/identity/dependency-policy.json`. The lead rechecked every exact value in the scope table against `3e64266`, and all of them are unchanged from r1.

## What r2 changes

The "r2 changes" section at the top of the proposal lists them. In short:

1. **F8B-RF-1.**
   - **Step 5** keeps the admitted public drift gate on rebuild-02 only. It also retains the generation run's work directory as the probe's input source. It states that rebuild-01 is never passed to the selected path, which `pipeline.py:40–44` refuses after step 4, correctly.
   - **New step 6** is the executable-equivalence probe, labelled comparison evidence and not admitted F8b drift:
     - **Script:** `evidence/equivalence/probe_f8b.py`. It never calls `generate_contracts.py`, `pipeline.run` or the receipt validator.
     - **Binaries:** rebuild-01 at 7202304 B, `4388e707…`; rebuild-02 at the step 2 receipt's executable pin. Both are checked before and after, and run from 0700 copies.
     - **Inputs:** step 5's whole `prepared/` directory and its `protocol-unformatted.rs`, pinned before and after.
     - **Invocations:** both, mirroring `pipeline.py:132` (ordinary) and `:160` (`--format-rust`). Each runs under the pipeline's own confinement helpers and environment.
     - **Comparison:** exit status, stdout, stderr, the output file set, and every output byte.
     - **Determinism check:** rebuild-02's probe outputs must equal step 5's own outputs.
     - **Outcome rule:** any difference stops the unit, and never leads to editing a receipt, re-pinning rebuild-01 or relaxing a check.
     - **Frozen evidence:** `probe_f8b.py`, `probe-result.json`, `probe-manifest.json` and `probe.tar.xz` (LFS; inputs, both output trees, logs and profiles; binaries pinned, not frozen).
   - **Your alternative, a coherent comparison snapshot,** is rejected with a reason: base cannot run the public path either, because its closure pins the pre-VD1 `verify_design.py`. A snapshot would therefore need an invented second selection.
   - Old steps 6–9 become 7–10. The review and freeze lists, and decision 3's step reference, follow.
2. **F8B-NBO-1.** Decision 2 and step 3 now claim only a rebuild-01 versus rebuild-02 result. They preserve native re-pin's unverified rebuild403 limitation. A new limit says the probe covers one input set, not general equivalence.

Nothing else in the scope table, decisions 1 and 3–5, the parents or the integration steps changes in substance.

## Decide

1. Does r2 resolve F8B-RF-1? Is the probe specified in a form that can actually run once the machine is free? Check the binaries, inputs, both invocations, confinement, comparison and outcome rule against `tools/contracts/pipeline.py`, `admission.py`, `confine.py` and `src/main.rs` at `3e64266`.
2. Is the probe correctly kept apart from admission? It must be labelled comparison evidence, must not substitute for step 5, must have no hand-edited receipt, and must not weaken or bypass any selected check.
3. Is the frozen evidence set sufficient for the later ACCEPT-DESIGN-UNIT reviewer to rerun and judge the probe?
4. Is F8B-NBO-1 addressed?
5. Did r2 introduce any new problem?

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`;
- `"requiredFindings"`;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: `cf7e118358fa4831f1ff3b4ade7ab9f7efed0d7100b811ed631336d76e4feb49`, as a single string.
