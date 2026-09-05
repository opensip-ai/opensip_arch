# Independent review — leftover C2 design-contract candidates

Independent, refute not confirm. Did not author the subject.
Work in `/Users/sb/code/opensip-ai/opensip`.

Review **one subject at a time**. The coordinator names the subject
path, expected sha256, register row, and write path in the dispatch
message. Measure the digest at start AND end with Python hashlib.
If the subject moves, OBJECT.

Do not edit the subject. Do not commit.
Do not mark the register row SATISFIED.
Do not authorize `docs/v2/implementation/`.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not read the other current reviewer of the same subject.

## Subjects in this leftover set (dispatch names one)

| Row | Path | sha256 prefix |
|---|---|---|
| DR-101 | `distribution-core-inventory-contract.v1.json` | `43955ff4672fc0ab` |
| DR-105 | `permission-truth-tables.v5.json` | `dca5fcc768e29cef` |
| DR-107 | `lifecycle-generation-contract.v1.json` | `8d7f2d0c2438c275` |
| DR-111 | `compatibility-matrices-contract.v5.json` | `d0386cee26d8aafd` (D-103 recorded candidate; do not re-review as unrecorded) |
| DR-112 | `signed-index-trust-contract.v7.json` | `ce26f1621b4ff2a3` |
| DR-118 | `language-quality-matrix-contract.v1.json` | `500347c119e4ff9e` |
| DR-120 | `component-packaging-contract.v6.json` | `c1fe8cb788b7da1d` |
| DR-121 | `monorepo-ci-contract.v1.json` | `dce61c4ef9d641e0` |
| DR-122 | `sarif-projection-contract.v1.json` | `2002b3eca1385690` |
| DR-124 | `state-class-contract.v1.json` | `3d0466bbf43daba1` |
| DR-125 | `component-sdk-contract.v1.json` | `d937c1180492420b` |
| DR-126 | `platform-tcb-contract.v1.json` | `89913fd8a8f3c62c` |
| DR-127 | `anti-lockstep-contract.v1.json` | `4bc0b2815fde1562` |

Full sha256 must be re-measured; prefixes are orientation only.

## Attack (every leftover subject)

- Acceptance-evidence cell not answered obligation-by-obligation
- Row-verbatim mismatch against live file 08
- Inventing a closed surface owned by another row
- SATISFIED / QUALIFIED / implementation authorization
- Self-granted authority / silent fallback
- Treating an unaccepted sibling contract as settled
- Any lock claimed producible before DR-111 closes

ACCEPT only at 0 blockers and 0 SHOULD-FIX.

Final chat: short coordinator summary plus verdict word.
