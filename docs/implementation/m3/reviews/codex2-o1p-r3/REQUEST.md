CODEX2 review: unit **O1-p** r3, the subject join for inventory v141. Grok leads. Round 2 is ACCEPT-UNIT on the product diff and inventory v141, with no findings. That review cannot bind: `verify_design` joins the assent's subject pin to `subjectManifestSha256`, and round 2 has `subjectSha256` only. Verdict wanted: **ACCEPT-UNIT**, with the same inventory assessment and with `subjectManifestSha256`. No product change is in this round.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only `REVIEW.md` and `review.json` under `/tmp/opensip-implementation/reviews/codex2-o1p-r3`.
- Never touch `~/Library/Application Support/OpenSIP`. It must stay absent.
- Never read the private 413 UUID fixture.
- Do not touch other worktrees. No cargo is required. If you run cargo, take `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"` and `rmdir` only a lock your own `mkdir` created.

## Unchanged from the accepted round 2

- Product commit `e6e2b847535fa1af29886a832886ac83d8cb82ee` on product main. Parent `e01efff`. The diff `git diff e01efff e6e2b84` is 16661 bytes, sha256 `3d1d7bf418175bc0bf4e1bc45f6f9df56abb63491e152c5bf0e862f39214da7f`. Five platform files, +374 −1. `design-lock.json` is not in that commit.
- Inventory v141 is unchanged: 585083 bytes, `6f9cddbc0531ff3128e783d8446d05462281b227a116ec84456ba28af642e750`. Parent v140: 584066 bytes, `9eebf35bd89cb76a631f416200d7f2ca654a8d6e6e5cfc8cf2ab81fcc30961de`. Successor: `docs/implementation/m2/platform-mechanisms-o1p-inventory-v141/successor.json`, 307821 bytes, `5a939e59b7ca01e4a19d1aad40c6f7f8774211cad0ab706d92295119050d6306`.
- Round 2 closed `RF-O1P-1` and `RF-O1P-2`. Do not reopen them. This round does not accept S-OP-2b.

## The new subject

`docs/implementation/m2/platform-mechanisms-o1p-inventory-v141-subject.json`, 655 bytes, sha256 `7acd481df640d38f74f684fb6ec87229ce49e78c73db1e958248cdb3f0a4206d`.

Its three files, sorted, are the successor README, `successor.json`, and inventory v141. The README states why this manifest exists. The product sources are not members. The assent unit file is not written yet and is not a member.

## review.json

- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`.
- `"requiredFindings"`: an array, empty on acceptance.
- `"subjectSha256"`: `3d1d7bf418175bc0bf4e1bc45f6f9df56abb63491e152c5bf0e862f39214da7f`.
- `"subjectManifestSha256"`: `7acd481df640d38f74f684fb6ec87229ce49e78c73db1e958248cdb3f0a4206d`.
- `"inventoryCandidateAssessment"`: verdict `ACCEPT` or `REQUIRED-FINDINGS`, `requiredFindings`, candidate path `docs/implementation/m2/repository-file-inventory.v141.json` with bytes 585083 and sha256 `6f9cddbc0531ff3128e783d8446d05462281b227a116ec84456ba28af642e750`, `parent` pinning v140 (path, bytes 584066, sha256 `9eebf35bd89cb76a631f416200d7f2ca654a8d6e6e5cfc8cf2ab81fcc30961de`), and `successorRecord` pinning the successor (path `docs/implementation/m2/platform-mechanisms-o1p-inventory-v141/successor.json`, bytes 307821, sha256 `5a939e59b7ca01e4a19d1aad40c6f7f8774211cad0ab706d92295119050d6306`).

The binder compares path, sha256, and bytes on the candidate and the parent, and path and sha256 on the successor record. Extra assessment fields are ignored by that comparison.
