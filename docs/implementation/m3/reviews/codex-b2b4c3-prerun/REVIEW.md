# B2-b4c3 pre-run review

Verdict: **ACCEPT**. **runAuthorized: true**, for the single refresh described by the pinned RUN-PLAN.md at the verified product base and bindings. No run was performed by this reviewer.

Subject manifest: `docs/implementation/m3/config-discovery-b/b2-b4c3-prerun-subject.json`, 684 bytes, SHA-256 `3479eed14441a9c8e452891ae33ef2b11feac631ff0059140c84caebf1fd7ffa`. All three members match their pinned sizes and hashes:

- RUN-PLAN.md: 3,350 bytes, `64d6f6271093fb89fcfda7ae1cf818ff74702befd8fd67a9201b513e68d68a5a`.
- evidence/drift.json: 12,346 bytes, `e4cc7a99898c853364907414a6f6d8f58a6acefeaa06a2c187afaeddf78135fa`.
- evidence/run_b2b4c3_blind.py: 4,851 bytes, `d58d742bd6515c06ee7df897285a233e3e181a3431065de4e0ce8382db942cfc`.

Product main is clean at `15a8ac0a82bd81bd04d24190ba90539e2a5bd582`. Architecture HEAD is `2cd0bb7712b2c7d4663a2301ed70eaea27934001` plus the proposed files.

## Assessment

1. **The identified drift is inert to this computation.** All 23 file-binding comparisons in drift.json were independently recomputed from the public files and match exactly. Only tools/contracts/generator-closure.json differs from the receipt. Its old bytes match the parent of S10-TSC code commit 25d0f79; its current bytes match that commit and have not changed since. The file remains 68,468 bytes, changing from SHA-256 fe4bb4f4580706a556bb047c5a62ffc0a481b43dbc77984169a8fe8d2ea6fbd2 to 796701ea87e7ff7db1b029c8c0eea043e550e9cd5f0daf234637fae927291acb. The only changed rows are schemas/source-map.json and common-v1/v3/v4.schema.json. No rows are added or removed and all other top-level keys are equal.

   The reference loader filters that closure to tools/contracts/python-packages/ rows, verifies their bytes and adds that package directory to the Python import path. No changed schema row participates in that loading. All 128 current package files match their pins. The census tool is the unchanged reviewed 63,787-byte file with SHA-256 6ea8a1ab7ecad60220896790df6fb07aa53d2eac7efe7e6120a441b7b75c7dfd. All 15 cost-closure files, the manifest and remaining reference files match the existing receipt. The unchanged tool/closure preserve the size inventory, extracted caps and root lengths; their public recorded values agree as well.

2. **The proposed execution is scoped correctly.** RUN-PLAN step 1 prepares a clean detached worktree of this product main. The runner requires main/worktree HEAD equality and clean status, and checks the tool hash in both before removing only the worktree's stale receipt. It makes one blind-mode subprocess call, with no retry loop for that call. The lane lock encloses the work; nice 10 is set before children spawn; the temporary directory is private 0700 and supplied through TMPDIR. The Python interpreter, tool path, architecture/packages roots and cache argument are explicit.

   The wrapper reads only public control files, the closed receipt and census output; it contains no traversal or direct read of a held-out store. Held-out content access is confined to the unchanged accepted blind mode. That mode retains its exception redaction and closed receipt format, while ordinary --write/--check retain the reviewed prohibition on held-out store access. Its one-line stdout summary and redacted error channel remain the original reviewed disclosure surface.

   On a successful blind exit with a receipt, the wrapper runs ordinary --write and --check and records both exit codes. It compares receipt rows, state and standing, changed binding categories, changed reference rows and census byte identity, and records receipt size/hash and worktree changes. These are appropriate post-run evidence. The expected product difference is the receipt alone; this remains an expectation to verify after execution. The runner itself does not create the worktree or independently assert detached HEAD, and it checks main/worktree equality rather than a hardcoded base hash: the prepared detached worktree and this verified base are part of the pinned run procedure and this acceptance's scope.

3. **Authorization is sufficient.** The recorded owner decision authorizes the mechanical blind method with review before and after. This refresh changes no method, population, store-access boundary or disclosure allowlist. Accepted B2-b4 plan r6 section 2.5 already provides for a new reviewed run after binding drift. The prior mode acceptance and original run acceptance remain applicable to their exact unchanged code, while this review supplies the fresh pre-run gate for the current input binding. No fresh owner choice is needed. Post-run Codex review and lead assent are still required before a product commit; this pre-run acceptance does not close them.

4. **The failure path is correct.** The runner contains no commit or push operation. Exit codes, comparisons, stdout/stderr status and receipt identity are evidence, not automatic acceptance. Any unexpected row/state/binding/census change, nonempty stderr or execution error prevents the proposed receipt-only integration and must be reported for review. Pending that review, the current margin remains outstanding. A subsequently verified failing margin must follow item 12's return-to-law rule; it cannot be converted into a passing receipt or silently retried.

5. **The miss is accurately recorded.** Receipt bytes remained unchanged through S10's code and lock commits. The loader-binding hash therefore became stale with code 25d0f79, and was already stale at lock 1f70dba. From compose_held_out's unchanged logic, current ordinary composition substitutes exactly the ten stale held-out rows and sets heldOutMargin to outstanding. No altered package input or walker computation changes a lead-readable/workspace row. Thus the committed census's historical holds state and r101's every-repository margin statement lack a current receipt binding. The proposed record correctly acknowledges this and commits to correcting status independently of the refresh outcome. No census run was needed or performed to establish that control-flow consequence.

No required findings or non-blocking observations.

## Limits

Authorization is for this exact proposed one-time run, not for a B3-b cost-model change, a new held-out population or a completed margin claim. Fresh post-run evidence must establish the expected equality and current receipt bindings. Inventory is unaffected because the receipt path already exists.

Review used only file reading, hashing, JSON/AST parsing and Git queries. No census, blind-mode, Cargo, test, generator or build was run. Neither repository nor control files were edited. No T2 held-out store/overlay, installation, private fixture or signing key was accessed. No delegation was used. Only REVIEW.md and review.json were written in the requested directory.
