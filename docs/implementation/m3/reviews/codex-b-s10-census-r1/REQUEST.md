# Review request: B-S10-CENSUS-r1 (operability census follow-on to B-S10)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b-s10-census-r1/`).

## Boundaries

Do not edit either repository, the worktree, the stage or control files. Do not run Cargo, tests, builds, generators or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only reading, hashing, JSON parsing, Git queries, and `tools/check_operability.py source --repository <tree>`, which only reads, against:
- the product `/Users/sb/code/opensip-ai/opensip` (clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`);
- the B-S10 candidate worktree `/Users/sb/code/opensip-ai/opensip-b-s10`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b-s10-census-r1-stage`
- **Subject file.** `docs/implementation/m3/config-discovery-b/b-s10-census-subject.json`: 916 bytes, SHA-256 `36dd58e86a9ab2a6cea4937618921eef3b45d3644ccdcf0c1be1de67b62dda95`, 4 members. Rehash every member.
- **Context.** B-S10, published at architecture `d8950a8d1a6f4fbefd49e98bbc8afe0ff272a90b` (your `codex-b-s10-r2` ACCEPT-DESIGN-UNIT).

## What to review

1. **The diff.** Is it exactly one `mintAudit` row count, 135 to 150, for the generated `invocation.rs` `into` calls?
2. **The count.** Does it equal the candidate tree's lexical census, `mint_inventory`, with no other row differing? Check that the base passes, and that the candidate passes with the update.
3. **The plan.** Is the product commit plan correct: the 14 B-S10 copies plus this record, then the separate lock commit?
4. **Design content.** Is it true that no B-S10 design content, exception class row or law changes?

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "36dd58e86a9ab2a6cea4937618921eef3b45d3644ccdcf0c1be1de67b62dda95",
  "singleRowCensusUpdate": true,
  "countMatchesCandidateTree": true,
  "basePassesCandidatePassesWithUpdate": true,
  "productCommitPlanCorrect": true,
  "designContentUnchanged": true,
  "pushed": false
}
```
