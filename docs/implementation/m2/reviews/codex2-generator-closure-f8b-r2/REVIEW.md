# CODEX2 review: F8b proposal r2

**Verdict: ACCEPT (proposal).** F8B-RF-1 and F8B-NBO-1 are resolved. No required finding remains. Two minor clarifications below do not block proposal acceptance.

Subject: `docs/implementation/m2/generator-closure-f8b/PROPOSAL.md`, 25864 bytes, SHA-256 `cf7e118358fa4831f1ff3b4ade7ab9f7efed0d7100b811ed631336d76e4feb49`. Product examined: `3e64266aa8729160cd22509dcfff95a3bb09fcea`. This does not grant ACCEPT-DESIGN-UNIT; that review follows the actual rebuild and frozen subject manifest.

## Requested judgments

1. **F8B-RF-1 is resolved, and the probe can be implemented as specified.** Step 5 keeps the selected public drift check on rebuild-02, preserving the toolchain, closure and observed-receipt joins. Step 6 never calls that entry point, `pipeline.run` or the receipt validator. Its comparison therefore does not encounter the old-binary admission conflict.

   The rebuild-01 pin exactly matches the current selected generator: 7202304 bytes, SHA-256 `4388e707035e0ea4b0c3dcd9206e55fd7045e58658a443fb13e04a12847a6959`. Rebuild-02 must use its actual observed receipt pin. The planned copies, shared input bytes and before/after checks are sufficient for this trusted-host comparison.

   `src/main.rs:6–20` accepts both specified command forms. Ordinary generation reads owners and the Rust projection and emits the six named modules (`:66–85`); format reads the supplied Rust file and writes the named output (`:9–11`). The six-file prepared directory and unformatted protocol input match `pipeline.py:124–132,158–160`. Using rebuild-02's unformatted input is valid after ordinary output equality establishes that rebuild-01 would supply the same Rust bytes.

   The confinement grants and explicit environment follow `pipeline.py:85–95`. `admission.child_profile` accepts these executable/read/write arguments (`admission.py:83–95`), and `confine.capture_child` supplies bounded status and logs (`confine.py:14–61`). The implementation must create the private output roots before constructing profiles, refuse capture failures or unsuccessful children, and collect exactly the declared regular files. These are ordinary implementation requirements, not changes to the design.

2. **The probe stays apart from admission.** Lines 102–107 and 130 distinguish the public drift gate from comparison evidence. The probe selects nothing, never substitutes for step 5, and cannot lead to changing a receipt or relaxing a check. A mismatch between either binary or the admitted run stops the unit. The clean integration checks still require no synthetic assent.

3. **The planned frozen evidence supports the later review.** The script, exact inputs, both output sets, logs, sandbox profiles, result and archive-member manifest preserve what was compared. The reviewer can verify exact membership and bytes, rerun both command forms with the pinned binaries, and judge the recorded equality. Rerunning step 5 before step 6, as line 167 requires, recreates the intermediate and final reference outputs for the determinism checks. The archive does not independently preserve those original reference trees; the specified replay order supplies them.

   The binaries remain host-local, explicitly. Replay consequently depends on the exact recorded binaries remaining available. That is consistent with the stated development-host scope and is not a portability or reproducible-build claim. The later review must verify the actual frozen script, pins and materialized LFS bytes; none exists as observed probe evidence yet.

4. **F8B-NBO-1 is addressed.** Lines 70 and 100 now limit the comparison to rebuild-01 versus rebuild-02 and preserve the unverified rebuild403 limitation. Line 178 limits the functional comparison to this one input set.

5. **No new blocking problem was introduced.** The r1/r2 diff preserves the file scope and underlying lead decisions. Static Git reads confirm that all nine proposed materialization files, verify_design.py, all three locks and the relevant generator sources/profile are byte-identical between `30c5db1` and `3e64266`; the only integration changes are F8a's two policy files. The preserved r1 proposal and copied r1 review also match their earlier bytes. The r1 scope, successor-vehicle and lead-decision conclusions therefore stand.

## Non-blocking observations

### F8B-NBO-2 — Distinguish raw protocol output from final product output

**Location:** PROPOSAL.md:129.

The sentence saying step 5's drift gate equated “those outputs” with product is too broad for ordinary `protocol.rs`. That file is an intermediate: the pipeline appends native carriers and formats it before final drift comparison (`pipeline.py:158–160`). The actual probe references are correct. Clarify that ordinary outputs are tied to the generation run's base tree, while formatted protocol output is tied directly to the final output.

### F8B-NBO-3 — Make the confinement-profile source explicit

**Location:** PROPOSAL.md:107,122.

Step 6 permits only two repository helper reads, but `verify_confinement` needs the profile value. Load `confinement-profile.json` from the retained `gen-candidate/snapshot/tools/contracts/` tree and assert its closure pin, rather than adding a third worktree-file read. Step 5 already creates that authenticated snapshot (`pipeline.py:65–76`) and retains it; later replay recreates it. This is an implementation clarification with an available source, not a blocker.

## Review boundaries

The subject and preserved r1 hashes were checked using standard-library code and read-only Git/file reads. Product sources were inspected at the exact requested commit; no repository module was imported.

No cargo, Node, generator, product code or tests were run. No installed tool, generator binary, cached archive or provisioned dependency tree was read. No real application home or 413 fixture was accessed. Writes are confined to this review directory. No repository edits or commits were made.

