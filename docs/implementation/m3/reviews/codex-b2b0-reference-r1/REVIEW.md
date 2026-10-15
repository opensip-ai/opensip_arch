# B2-B0-REFERENCE-r1 review

**Verdict: REQUIRED-FINDINGS.** Two required corrections: upward-population leakage and a checker exception path that permits success without completing a replay.

## Subject and verification

Rehashed the 1,133-byte subject manifest, SHA-256 `f1af9b4bbe8b88689190177ed7f3de883c22b61d013f205f39ae827ddc0ca876`, and all five members. Every size and digest matches. The 2,857-byte successor record matches `ebebd41959e5d0ecb079b5097f307971648bbdac74be4b7db216746ff35470c4`.

Verified product HEAD `94e5fdebd63a174694dadbb5e647063855614b77` and architecture HEAD `3b2a55d48c442b66d188369a4d8a9307fdaeb14b`, with clean tracked state. All eight sorted record parent pins match their bytes and accepted source/application manifests, selected inventory or earlier contract candidates. The four candidates exactly cover the subject apart from its included record. There are no overrides. With 163 existing contract successors, 164 is the correct next position, conditional on corrected acceptance and lead assent.

Ran the exact permitted checker, writing [checker-rerun.json](checker-rerun.json). It passed with 22 controls; its output is byte-identical to staged `evidence/checks.json`. Independently counted 64 schema-valid discovery results and 35 schema-valid inventories. The four supplied-provenance boundary-model cases are explicitly listed separately. Existing replay outcomes are unchanged; the two reported `vendor/lib` removals correspond to explicit/config population restrictions. These existing results agree with the staged claims but do not cover the defects below.

## B2B0REF-1: upward ancestors bypass downward restrictions

`walker_population` lines 104–109 insert every ancestor of all four possible starting paths and their `opensip.json` children into `keep`. The restricted downward traversal never removes them. This treats hypothetical upward observations as actual downward evidence. In particular, an explicit project selects its path directly; it does not walk the unrelated cwd chain.

Independently reproduced using permitted read-only imports of the staged reference and bound models, over synthetic custody-passing metadata only:

- With `explicitProject=/h/w`, `cwd=/h/w/.opensip/hidden-repo`, and a `vcs=True` directory at that cwd, `current` accepts and reports `/h/w/.opensip/hidden-repo` in `nestedRepositories`. A supplied `/h/w/.opensip/opensip.json` is also retained in the population. Both are beneath the pruned custody anchor.
- With `explicitProject=/h/w`, `explicitJoins=['a/u']`, `cwd=/h/w/b/repo`, a marker at `a/u/package.json` and `vcs=True` on `b/repo`, `current` accepts but retains `/h/w/b` and `/h/w/b/repo` and reports the unrelated repository.

The selected-root/source equality still holds. The checker population property also holds, because the forbidden output path was inserted into the population first. This defeats both SX-1 and exact-source confinement, and the same unconditional ancestor union bypasses the intended depth population bound when cwd is deeper.

**Required correction:** retain the upward evidence actually used by selection and keep it separate from the downward map supplied to `finish`. Preserve genuine upward provenance without exposing those observations to unrestricted nested-repository/project collection. An explicit project must not import unrelated cwd/account-home ancestor observations into discovery. Add direct population and result checks for the two reproductions and a depth-overlap case, then regenerate all evidence and pins.

## B2B0REF-2: unexpected replay exceptions can report success

The current replay exception handler at checker lines 119–121 appends an `EXCEPTION` row and continues without recording a failure. An exception in swapped discovery or `current`, including its explicit root/source consistency error, therefore skips schema and population checks while leaving `passed` eligible to be true. The discovery-case counter increments before this branch and cannot establish successful replay coverage.

**Required correction:** make unexpected discovery exceptions fail. Any intentional exception case needs an explicit case-specific expectation. Assert exact replay/validation coverage and the four designated boundary-model cases; add a negative checker control showing that a current-replay consistency exception produces failure and a nonzero exit. This is established by source inspection; no checker or reference bytes were mutated during review.

## Other assessments

Loading the accepted SLM and replacing only its DD global is correctly implemented and pinned. Historical mode remains separate; SLM, DD and the bound B2-a copy retain their bytes. Parent-first explicit chains retain ancestor Cargo evidence and correctly stop at boundaries/pruned prefixes. Downward pruning precedes boundary handling in the traversal itself; the failure is the separate unconditional union of upward paths.

`current` correctly preserves a pre-finish refusal and checks root/source equality on pass two. That mechanism does not establish lawful population geometry, and its error must be enforced by the checker. The two-pass mechanism itself need not change to fix the silent exception handling.

The V3 projection preserves the pending reader field explicitly. Shape filling occurs only in schema-validation inputs, not emitted results. Existing D9 values validate against the V3 subset. The boundary converter emits a structurally complete V3 inventory for accepted partial results; this structural completeness does not establish that its leaked paths were lawfully observed.

Inspected the scratch builder and report, which identify this exact subject/record and report base verification and successor-164 verification passing using synthetic review/assent. Did not run that builder or full design verification. Scratch binding compatibility is not independent acceptance or an actual binding. Product code, schemas and qualification remain outside this unit.

## Boundaries

Used permitted read-only reading, hashing, JSON parsing, Git queries, the exact staged checker and reference imports over synthetic inputs. Ran no Cargo, tests, builds or lane; used no network, other panes or delegation; accessed no private 413 fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md`, `review.json` and the permitted checker output in this review directory.
