Of the four comparisons, one is a real reference defect, one is a gap in the law, and two are permitted freedom. The only blocker is the strong owner's handling of `partial` availability.

Frozen42 matched its manifest before and after (12913 members, 0 missing, mismatched or extra). The consumer vectors, root replay verification, root capture reports, both consumer exports and root's two readers all match their stated hashes. Every Run was fully admitted before any query, and all subprocesses have finished.

| # | Comparison | Classification | Blocker? |
|---|---|---|---|
| 1 | Page-1 cursor hash; owner refuses the consumer's page-2 tokens | Permitted choice | No |
| 2 | `path-both-direction` edge orientation | Normative gap | Needs an owner decision; neither implementation is wrong |
| 3 | `partial` availability: consumer `partial`, owner `retained` | Reference defect (owner) | Yes |
| 4 | Success termination, `note` text, refusal wording | Permitted choice | No |

## 1. Cursor
- **Preimages.** I reproduced both hashes exactly with the owner's canonicalisation. The two canonical records are identical except that the consumer adds an `"order": "query-projection-contract.v3 s3/s4"` member.
- **Law.** The contract (§5 `:136`) and the schema's `Page.cursor` description call the token an opaque host token. The `q3.…` form is only a reference form, and no source requires tokens to be portable between implementations.
- **Refusal.** The owner rejects the consumer's tokens with a complete envelope (`request-rejected` / `REQUEST.PRECONDITION_FAILED` / `QUERY.CURSOR_MISMATCH`, exit 2). That is the published route.
- **Owner's own tokens:** its page-1 token continues the same page-2 request correctly and does not re-resolve latest. The result is identical with a host cache present, and the page-2 items equal the consumer's.
- The two page-2 vectors therefore aren't a cross-implementation test. No cursor was translated.

## 2. Path edge orientation
- **Measurement.** For the stored fact `main→helper`, the owner reports a helper→main path under `both` or `incoming` with edges reversed to follow the walk, and each edge links consecutive nodes. Its neighbour rows keep the stored orientation. The consumer's path keeps the stored orientation. Both responses pass the schema.
- **Why it's a gap:** no contract text, schema description or maintained control fixes path-edge orientation, yet §4 requires every backend to "reproduce the same result".
- **Proposed fix:** one sentence in §4 pinning the reference's current walk orientation, plus two pinning controls. No reference code changes. Keeping the stored orientation instead is equally coherent, so this is an owner decision.

## 3. `partial` availability
- **Admission agrees.** Both implementations admit the same Run with identical items, consistent with §7: `partial` neither refuses nor grants.
- **Reported value.** Identity law treats current availability as a separate record, including `partial`, and says "A query reports both" (`identity-and-evidence.md:1721-1725`). The query contract calls availability a trusted current host observation, and the response field is required with `partial` allowed.
- **Defect.** The frozen owner returns `retained` for omitted, `retained` and `partial` observations alike: `observe_availability` maps `partial` to `retained`, and `execute_graph_query` hardcodes `"retained"`.

## 4. Termination, notes and refusal wording
- **Optional fields:** response `termination` and `resolutionLimitations[].note` are optional. Owner responses without them still pass the schema.
- **Refusal envelopes:** I regenerated the owner's actual failure envelopes (`QueryRefusal.envelope(host)`). For all 23 consumer failure vectors they match on every route field: kind, exit code, request id, project id, class, error code, fault cause, detail code, error codes and no `run`. Only `remedy`/`subject` wording differs, which §7 declares diagnostic.

## Proposed correction
The patch is `correction.patch` (sha256 `4c32d6c3…`); base and after hashes for the three files are in `delta-manifest.json`, and every base file is byte-identical to frozen42.
- **Model** (`query_projection_model.v3.py`): report an observed `retained` or `partial` as observed; an omitted observation still reports `retained`. No refusal route changes.
- **Contract** (`query-projection-contract.v3.md`): the §7 availability sentence and the §4 path sentence.
- **Checker** (`check-query-projection.v3.py`): five controls.
  - Availability discriminator: `partial` is reported.
  - Availability preserved positives: `partial` changes nothing else; `retained` and omitted report `retained`.
  - Path pins: `incoming` and `both` edges follow the walk.
- **Unchanged:** schema bytes, identity and native owners, and the product contract.

**Receipts:**

| Run | Checks | Failed |
|---|---|---|
| Unpatched copy | 204 | 0 |
| Patched copy | 209 | 0 |
| Patched checker on unpatched model | 209 | 1: `host-availability-partial-reported-in-response` (got `retained`) |

- All 204 existing checks are unchanged.
- Re-running every exact vector on the patched copy changes only the `partial` case's `context.availability`.
- The path pins pass on the unpatched model too, because they encode existing behaviour.

## Limits
- **Not inferred, left to root:** three uncaptured vectors — `syntax-mixed-disclosed`, and missing-bytes and corrupt-bytes (both on `cmp-code`). The `cmp-scope` wrapper failure is bookkeeping. I didn't use root's metadata with the trailing backslash-n.
- **Unstated but unchanged:** no source says what an omitted availability observation should report. Both implementations report `retained`, and the patch keeps that.
- **Standing:** owner results are reference executions, not product or renderer qualification. I didn't run consumer code; its behaviour comes from its recorded vectors and source.
- **Not run:** broad suites, pins or planning. Any repin of the three changed files belongs to root.
- **Hash index scope:** `hash-index.json` also hashed pre-existing harness files in the runtime (`launch.py`, `preparation.json`, `process.json`, `prompt.md`, `public-events.jsonl`). I didn't create or read them.

Files are in `/tmp/opensip-design-corrections/claude-query42-discrepancy-assessment.v1`:
- review.md
- review.json
- correction.patch
- delta-manifest.json
- hash-index.json
- receipts/
- tools/
