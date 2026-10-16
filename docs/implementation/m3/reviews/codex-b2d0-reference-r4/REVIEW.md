# B2-D0-REFERENCE-r4 review

**Verdict: ACCEPT-DESIGN-UNIT.** The binding-record correction is exactly as described. Round 3's substantive acceptance carries forward, with its existing nonblocking observation.

## Verified subject and delta

Manifest: 1,952 bytes, SHA-256 `3bd9f9ece2f48c0da63837021e82d0f9a634ceb294534337d77fed224553fc8a`.

Rehashed all seven manifest members. The six non-record members match the accepted r3 successor's candidate pins exactly, including README, reference, checker/mutant scripts and recorded outputs. Only successor.json differs. The r3 record retained in the prior reviewer-owned temporary copy establishes the comparison without relying on regenerated checker output bytes.

The revised successor is 3,902 bytes, SHA-256 `a2a37d2dfe7bead07822348f1ef68049ce5e802af5f0b20cef996db61e98b01a`. Verified programmatically:

- The seven parents, six candidates and two authorities are each sorted by unique path.
- The union of new parents and authorities equals the old nine parent pins, including every byte count and hash.
- The new candidates equal the old candidates sorted by path.
- Exactly the archived JSONC reading and accepted plan moved to authorities.
- All other record fields are unchanged, including standing and empty passageOverrides.
- Every parent, authority and candidate pin matches its current file bytes.

Live product HEAD remains `a50ae9646c9cf6b6c3600c2c28c816f7a77ab609`, clean; architecture HEAD remains `1e938a466923ca2c7d1c45c6ddb7761c9019ed25`. The product lock still has 170 contract successors.

## Contract-record assessment

The correction matches tools/verify_design.py's actual rules. pin_rows requires sorted unique lists. contract_successor requires candidates to cover exactly the reviewed subject other than the record, and requires each parent to match an accepted base or selected successor pin. All seven retained parents were independently matched against the lock-pinned source/application manifests or contract successor 81's candidates. The candidate set covers exactly the other six reviewed members.

Separating authorities is appropriate. The plan and archived JSONC helper are supporting authorities/dependencies, not accepted parent contracts being superseded. Moving them does not promote either archive to accepted-base status, alter a passage, change the reference or remove a pin. The reference still verifies the JSONC archive's fixed bytes before loading it.

The current verifier does not interpret the additional authorities field. Its bytes are nevertheless authenticated by the reviewed successor record and subject manifest; both authority files were independently rehashed in this review. Thus no new verifier behavior or authority is being claimed.

My r3 statement that no binding defect existed was too broad: that review missed the sorting and parent-eligibility restrictions. This round checks those restrictions directly and accepts their correction. I did not recreate scratch assent/review files or independently replay the reported full verify_design dry run.

## Acceptance carried forward

The six executable/documentary/evidence members are byte-identical to those accepted in r3. The five-change oracle, YAML repairs, TOML profile, FR-4/FR-2 behavior and identity/provenance conclusions carry forward. Round 3 freshly ran 143 checks with zero failures and caught all 17 mutants; those executions were not repeated in this binding-only round.

**B2D0REF-R4-NBO-1:** carry forward r3's nonblocking matrix observation. The single-result overflow loop omits explicit-nonempty while the description advertises it. Existing overlapping controls cover the mechanism; add the combination for B2-d2 or narrow the description. No required finding remains.

This accepts the reviewed design-unit subject. Root assent, actual binding, implementation and qualification are separate; none is claimed complete here.

## Boundaries

Only reading, hashing, JSON parsing and Git queries were used. No repository edits, commits, builds, checker/mutant runs, network, other panes or delegation. No prohibited fixture, key, installation directory, held tree or T2 store was accessed. Only REVIEW.md and review.json in the requested review directory were written.
