# B2-B0-REFERENCE-r2 review

**Verdict: REQUIRED-FINDINGS.** Both round-1 findings are resolved. Two further population defects require correction.

## Verification

Rehashed the 1,134-byte manifest, SHA-256 `b719004114567045dff9f6853397b49251b9ff4f12bc737e1c99d514a5cff63e`, and all five members. All pins match, including the 2,908-byte successor record at SHA-256 `183d67fda32aa2a8c32af8555c19ffcce71b16a67ee1651604320dd33df83f2c`.

Product HEAD is `94e5fdebd63a174694dadbb5e647063855614b77`; architecture HEAD is `3b2a55d48c442b66d188369a4d8a9307fdaeb14b`. Both tracked states are clean. All eight sorted parent pins match accepted bases, earlier contract candidates or selected inventory. Candidates cover the reviewed subject apart from its included record; no overrides exist. Successor 164 is the next position, conditional on corrected acceptance and assent.

The permitted checker passed and [checker-rerun.json](checker-rerun.json) is byte-identical to staged `checks.json`: 64 discovery replays and V3 validations, four classified boundary-model cases, 35 validated inventories and 26 controls. Its temporary negative-control output was confined beneath this review directory using TMPDIR and automatically removed by the checker. No repository or stage outputs were written.

## Prior findings resolved

**B2B0REF-1:** Upward evidence now comes from actual first-pass walked rows and explicit spellings, filtered to exclude paths below the selected root. The downward population is separate; pass two starts at the selected root, and upward provenance is restored from pass one. Both original reproductions and the depth overlap are covered by new controls. Independently repeated the hidden-cwd reproduction and tried accountHome/explicitResolved overlaps; they no longer leak hidden descendant paths.

**B2B0REF-2:** Unexpected replay or validation exceptions now add failures. Exact replay/validation counts are checked. The injected consistency fault runs the checker as a child process and must produce a nonzero exit, passed=false and the expected exception failure; that control passed in the permitted rerun.

## B2B0REF-3: unobserved VCS annotations survive pruning

`admit` copies the entire supplied entry before the pruning branch. A synthetic directory's `vcs` attribute summarizes evidence inside that directory; it is not no-follow metadata available from the parent's listing. SLM's separate nested-repository collection consumes that attribute even for a pruned anchor.

Independently supplied a custody-passing `/h/w/.opensip` directory with `vcs=True`, using explicit project and cwd `/h/w`. `current` accepts and reports both:

```json
{"nestedRepositories":["/h/w/.opensip"],"prunedTrees":[{"path":"/h/w/.opensip","reason":"opensip-custody-state","markerCount":null,"markerCountBasis":"not-enumerated"}]}
```

The same defect reproduces at `node_modules`, `.git` and Cargo `target` (with `/h/w/Cargo.toml`). Omitting child paths is insufficient when the retained entry itself carries a derived observation that the walker cannot make.

**Required:** project each entry to actually observed evidence. A pruned entry retains its kind/identity but no VCS or boundary annotation derived from hidden children. Preserve legitimate selected-root/upward VCS data separately. Add input-field and output assertions for all four reasons, with `vcs=True` and hidden Git evidence.

## B2B0REF-4: boundary detection precedes the depth stop

In `subtree`, `boundary(c)` is evaluated while processing the parent and can retain `c/opensip.json`. The depth check runs only when a directory reaches the queue. A boundary therefore bypasses it.

Independently supplied 257 `d` directory segments below `/h/w`, with `opensip.json` in the deepest directory. `current` retains that file in its downward population and reports the depth-257 directory as a nested project. The stated policy permits only four marker-name observations at depth 257, not config or derived VCS evidence.

**Required:** apply depth restrictions before consulting boundary children/annotations. Add config and VCS cases at depths 256, 257 and 258, checking exact population contents and reported boundaries. Retain the existing ordinary-marker depth controls.

## Other assessments and limits

SLM and the bound rule remain unedited and pinned; historical loading is separate. Parent-first chain handling, Cargo pruning and explicit/config source choice retain the prior fixes. The two-pass selection/provenance split is sound in itself. V3 projection, the pending reader field, shape-only fill and structurally complete boundary conversion remain sound; schema validity does not establish that a boundary was lawfully observed. Existing case differences are explained, but the checker lacks the controls above.

Inspected the supplied scratch verification report and reproduction support. They identify the exact subject/record and document synthetic binding compatibility; they are not actual acceptance or binding. No scratch builder or full design verification was run during this review. Product code, schema changes and qualification remain outside scope.

Used only permitted read-only inspection, hashing, JSON parsing, Git queries, the staged checker and reference imports over synthetic inputs. Ran no Cargo, tests, builds or lane; used no network, other panes or delegation; accessed no private fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md`, `review.json` and permitted checker output in this review directory.
