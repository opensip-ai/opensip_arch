# Two bounded prose corrections — source coauthor

Source coauthorship only; no independent, blind or readiness claim. Inputs are read-only
captures of in-progress work; the main author's workspace was not read or modified. No
test, suite or environment was run.

## 1. Precedence paragraph — SOUND, exact bytes emitted

Root's diagnosis is right on both phrases, and the second was the worse error. Saying the
published pair is carried "at whichever boundary saw the defect" implied a *refused*
record still carries a disclosure pair. It cannot: a producer-admission refusal yields no
admitted Coverage entry at all. And "a `clones` scope … is refused" dropped the
false-claim condition, implying the scope itself is refused when an honestly disclosed one
is admitted.

Verified against the captured sources:

- **Honest disclosure is admitted.** `check-identity.py:2491-2498` — the mixed Markdown
  clone Run closes as `run2:` with `coverage=unknown`, `language-tier-unsupported`,
  `capability-missing`.
- **The refusal is conditioned on the false claim.**
  `native_evidence_model.v2.py:1380-1382` appends
  `native.coverage-source-variant-unsupported-complete` only under
  `if entry["coverage"] == "complete"`; `identity-model.py:1549` wraps it as
  `COVERAGE_PRODUCER_ADMISSION`.
- **"before the grammar guard"** is better than my absolute "and not by the grammar
  guard": it states which boundary arrives first without claiming the grammar guard could
  never have decided the case.

`precedence-final.md` is byte-identical to `precedence-proposed.md`.

Two non-blocking notes. The producer branch also refuses deficiency- and cause-mismatch
(`:1383-1388`), so false-complete is an *example* there, not the closed set — no change
needed, since S1.2 already enumerates all three earlier and this sentence is about
boundary order. And purely cosmetically, line 21 is 109 columns against the paragraph's
80-column wrap; I did not rewrap because exact bytes were requested, and root can rewrap
it at integration with no semantic change.

## 2. `SCOPE_LIMIT_REMEDY["nativeContextDigests"]` — AGREE

The removed clause was false **as a sufficiency claim**.
`typescript_native_context` (`native-model.observed.py:2082-2086`) mints identity over the
whole descriptor: `schemaVersion`, `languageMode`, `toolchain`, `toolClosure`,
`configProjection`, `moduleResolutionMode`, `packageModuleType`,
`nodeModulesLayoutDigest`, `lockfileIdentity`. `configGraphPaths` sits under
`configProjection` (`:2290`, `:2688`). So two units sharing compiler closure, standard
library and effective options can still differ in `configGraphPaths`, `lockfileIdentity`,
`nodeModulesLayoutDigest` or `moduleResolutionMode` and **not** collapse — the dedup key
is the whole-descriptor `planNativeContextDigest` set (`:3076`).

Root's replacement is the right shape: it omits the inaccurate explanation rather than
inventing a rule, preserves the shared remedy class the neighbouring comment states
(`:3731-3732`, "nothing was truncated") via "no context was truncated", and reuses the
lever wording already published for `requestedCapabilities` (`:3740`). Bound and field
naming unchanged; diagnostic string only, no behaviour change.

Emitted as a two-line parenthesised literal to match its neighbours; the concatenated
value is byte-exactly root's sentence, verified by `exec` of both blocks, each defining
only the `nativeContextDigests` key.

**Flagged, not altered:** the docstring at `:3070-3071` has a similar parenthetical but is
defensible — it says identical *contexts* collapse and calls it "deduplication of an
identical descriptor, never of two different ones", asserting no sufficiency. Left
untouched as instructed; root may review separately.

## Hashes

| artifact | sha256 |
|---|---|
| `precedence-final.md` (= root's proposal) | `9c5ec70337e44d7ea05450b87c120fd99ca0f9a5e3270ce383e948607d09bf51` |
| `scope-remedy-before.py` (occurs once in model) | `a73521de0eb459c0a933797dcc90029529a76f2a968bc9610e29a9abce461dcc` |
| `scope-remedy-after.py` | `483c9ddbe01db3335004836cfa482a920f19e8ecb01e9262e6a633212893e588` |
| `native-model.observed.py` (unmodified) | `9663ef2bccece114c740f2f09c86cddbbb558f9cc82086effee432ef0c2f2add` |
| spliced model — **rebase arithmetic only, not written** | `44e056b03e4e752c7dd0ad5773f5d972397069e3d1d8429f3dcc0d8fe2f28d20` |

**Rebase:** correction 1's citations are from the prior capture — re-locate by selector
(`if entry["coverage"] == "complete"`, `native.coverage-source-variant-*`,
`COVERAGE_PRODUCER_ADMISSION`) if lines moved. Correction 2 is anchored to a 3-line
literal occurring exactly once; if it no longer matches, the surrounding code changed and
it should not be blind-applied.

Wrote only `/tmp/opensip-design-corrections/v19-prose-final-coauthor.v1`. Prior outputs
preserved.
