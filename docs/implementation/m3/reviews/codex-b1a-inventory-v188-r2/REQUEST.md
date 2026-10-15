# Review request: B1-A-inventory-v188, round 2 (record shape only)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1a-inventory-v188-r2/`).

## Boundaries

The same as round 1: read-only. Do not edit either repository, the stage or the control files. No compiler, Cargo, tests, lane or network. No private fixture, installation, keys or held trees. No other panes and no delegation.

## Why round 2

Your round-1 review (`/tmp/opensip-implementation/reviews/codex-b1a-inventory-v188-r1/`) accepted the inventory successor with no findings. Do not modify it. Its `inventoryCandidateAssessment` carried the candidate pin as a nested `candidate` object, because the lead's request asked for that shape.

The product's `tools/verify_design.py` (lines 108-113) requires a different shape. The candidate's `path`, `bytes` and `sha256` must be members of `inventoryCandidateAssessment` itself, beside `parent` and `successorRecord`, as every earlier inventory review carried them. The pre-commit verification therefore refused with "review candidate names a different subject". **Nothing was committed;** the architecture working tree was restored clean.

## What to do

Re-confirm your judgment on the **unchanged** subject, the same stage and the same pins:
- **Stage.** `/tmp/opensip-implementation/b1a-inventory-v188/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b1-a-inventory-v188-subject.json`: 695 bytes, SHA-256 `6117c369e94c27c2cf29bea6319d9ef933770aab998e2f647a83dbda7458c837`. Rehash its three members.
- **Product.** Product main is still `50cefc64173b6e5daa8f1d2d9d410045544d1f9c` and architecture `7ff769c9e1626967f4fe9ece0fa78b8621891a15`.

Then re-issue it in the verifier's shape. This is not a new review of content. Do say if anything has changed since round 1.

## Output

`review.json` must carry exactly these fields, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "6117c369e94c27c2cf29bea6319d9ef933770aab998e2f647a83dbda7458c837",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v188.json",
    "bytes": 668214,
    "sha256": "6ce62d32b66598aabb5ded732ea1f0f806111c5708db63f428e88e91c2c4492a",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v187.json",
      "bytes": 663806,
      "sha256": "a35614a8d0c4b8a36664d6680bf5955055f43da20781412afd5f3b8d5a5f4977"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b1-a-inventory-v188/successor.json",
      "bytes": 6964,
      "sha256": "418408947f862413ca412a580990301ba9002087cd8b12c99376d2d65ef8ad3c"
    }
  }
}
```
