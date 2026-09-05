# Adversarial review — g29-fixture-corpus.v2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/g29-fixture-corpus.v2.json`
Expected sha256:
`22969243b638c01d1ea391eddb2b7006901f94d835319a7a7eb372da9493a0dd`
Mode 0444. If the subject moves, OBJECT.

Also freeze-check `docs/coop/artifacts/fixtures/g29.v2/` (four directories `macos-arm64`, `macos-x86_64`, `linux-x86_64`, `linux-arm64`; forty files). Each copy's sha256 must equal the corresponding `docs/coop/artifacts/fixtures/g29.v1/` payload digest. Frozen `fixtures/g29.v1/` stays unmoved, mode 0444, no platform subdirectory. If any copy digest diverges or `fixtures/g29.v1/` moved, OBJECT.

Frozen predecessor:
- `docs/coop/artifacts/g29-fixture-corpus.v1.json` `24fbbd2ddba0ca0a4e930cfabe83125768f8df38741abb867fc23c9b435b4fa1`
  Stage A Claude ACCEPT 0/0 (`c82007f84eca70daa19ddedde212c90bc85fa4fe225d74e0c201d6c064e5546b`); Codex ACCEPT 0/0 (`c582205d822872e95bb34f3a4c1f8a39ea4f0ca7d532121177eb6e7e125132e5`).
If the predecessor moved, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/g29-fixture-corpus.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/g29-fixture-corpus.v2.review-independent.codex.json`

Do not edit the subject. Do not mutate fixtures. Do not edit leftover-join.v6 of G29, occupancy v3, D-319 drafts, file 08, or COORD.
Do not commit. Do not SATISFY DR-117, DR-131, or DR-133. Do not close leftover-design of OBL-G29-FX-AUTHORING.
Do not remasure g29 leftover-join.v6. Do not remasure leftover-join.v4 of G29.
Do not claim leftover-design of these copies stale as an authoring claim.
Do not invent a D-002 platform list. Do not invent a section 7.1 recipe, a D9 code, or a PlanIntent schema.
Do not invent identifiers. Do not read the other reviewer's current-turn review.

HEAD is `8787d6ded31776a645b0a45f9f7a79b6c42513e2`. Last heading is D-341. Required-now is 28.
Live COORD sha256 is `2a61a842ec9a7dd3191bdd2589336aae6a96a2766525dc7c7c3427754b74e3e7`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-31.

This is leftover-design fixture authoring (D-056 Decision 5), not SATISFIED-GRADE.
Speaker is g29-fixture-corpus.v2. Candidate binds NOTHING. leftoverDesignClosedIfAcceptedAndRecorded is []. leftover-design of OBL-G29-FX-AUTHORING remains on leftover-join.v6 of G29. basedOn.d341.role is the sole last-heading claimant. Occupancy v3 stays unmoved. Frozen g29-fixture-corpus.v1 stays unmoved. Naming parent of DR-G29 is D-157, not D-086 and not leftover-join.v6 of G29.

OQ-G29-2 is answered by quoting G10 occupancy v2 `#$.platforms` ORDERED-EQUAL against G23 occupancy v2, recorded practice at g21-fixture-corpus.v8 (D-247). Occupancy v3 carries no platforms array. A D-002 platform list is not invented.

Attack:
- leftover-design of OBL-G29-FX-AUTHORING claimed closed
- leftover-design of the copies measured stale as an authoring claim by this corpus
- OQ-G29-2 unanswered while copies authored
- D-002 platform list invented rather than quoted from G10 occupancy v2
- G10 occupancy v2 unpinned while ORDERED-EQUAL is claimed
- platformsQuotedFromG10OccupancyV2 not ORDERED-EQUAL to G10 occupancy v2 `#$.platforms`
- g23OccupancyV2PlatformsOrderedEqual false
- a current-standing clause denies per-platform copies while copies are authored
- EV-1 collapsed into EV-2
- a live G29 retained-evidence member omitted
- EE-7a, EE-7b, or EE-7d treated as a G29 class
- section 7.1 recipe invented
- D9 code, exit number, or HostTermination invented
- EV-3 / v1SlicePin does not quote occupancy v3 section7Item8Standing.pin with path, digest, and verbatim
- DR-117 SATISFIED or Class A opened
- live required-now claimed other than 28
- leftover-join.v6 of G29 remasured
- leftover-join.v4 of G29 remasured
- parentReview treats leftover-join.v6 of G29 or D-086 as naming parent
- leftover-join.vN tokens in basedOn roles not lineage-qualified
- a deictic "This v2" / "This join" / "This leftover-join"
- QUALIFIED claimed or G29 executed
- G21, G23, or G30 taken over
- Windows copied
- a copy sha256 not equal to the corresponding fixtures/g29.v1/ payload
- fixtures/g29.v1/ mutated
- cited digests do not match live bytes
- subject or fixtures moved
- authorizes docs/v2/implementation/
- file 08 edited
- SATISFIES DR-117

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
