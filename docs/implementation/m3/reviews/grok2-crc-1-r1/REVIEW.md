# GROK2 review: CRC-1 r1, core role closures

**Verdict: REQUIRED-FINDINGS.**

Subject manifest: `docs/implementation/m3/snapshot-plan-c/crc-1-subject.json`, 1433 bytes, sha256 `adfa0d97dd525e631c5893bb568b7ba249d36b1cb2d95bb62e0da5ea4bc8d73a`. Successor: `docs/implementation/m3/snapshot-plan-c/crc-1/successor.json`, 21459 bytes, sha256 `55b43151ec7d634fd42f14cc352658dfa6c848212428536db872403eafcd8477`. Single reviewer. Design-unit review. No cargo, tests, or crash-matrix binary. `crc-1-unit.json` is outside the subject and was not bound. `~/Library/Application Support/OpenSIP` was absent.

Thirty-four of the thirty-five `hashes.txt` pins matched, including the seven subject members, the six parents, M3-C r7 and r6, M3-E1 r3, M3-H r1 and r2, both Grok H reviews, EC1, I1-L, X12 r4, and the three product objects at `9c11c53` (`design-lock.json`, `tools/verify_design.py`, and `crates/security/tests/fixtures/core-inventory318.ndjson`). The unmatched pin is the unbound SYN-1F draft, which the pin line says may change (NBO-1).

## Evidence

Python was `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Git used a private `HOME` and `core.hooksPath=/dev/null`.

`evidence/build_crc_1.py --check` rebuilt the subject files to the bytes on disk. It differs only on `crc-1-unit.json` (NBO-2).

`evidence/check_crc_1.py` passed at `9c11c53` (79 successors) and at `cd5958b` (82). Parents match the arch bytes and the accepted lock set, every selector is unbound, every `after` only inserts, the IDS-L mask changes only the three strings, `byField` and the kind list are unchanged, the IE:285 paragraph contains item 9's field list, and the vector matches EC1 and all 53 accepted fixture cases. The five ids are:

- core `closure2:54322a2c18a7ed6d5a2c92ab7e1204884e7095cfc254d40d352f879761fa118d`
- evaluator `closure2:7da97b9a4686fe5dc6ff69d83ddde230ac6895afb699717f2ef07a05810b89e2`
- detector `closure2:be7bd6cc99990375edfc652b38f48fa5c51677970849b1dca3282245b0503c66`
- provider `closure2:df5e7cbab37c1ebccf867d343eaeb5d2739103492896e87d238a80efa1b8e662`
- adapter `closure2:670d260fd9956436fe1ef014d14ca18fb923e223f9a7f514a6fe4043fe36a0bf`

`evidence/verify_scratch.py --rev 9c11c53` selects CRC-1 as successor 80. `--rev cd5958b` and the checkout at `cd5958b3608f44a0035566c9d4500e5005c62e91` select it as successor 83. Each run has nine overrides, no supersession, six candidates, selected inventory `repository-file-inventory.v134.json`, and 55 inheritance rows. The second-override probe refuses with `conflicting contract passage overrides`. Checkout mode verified 40 generation sources and 48 admission sources (15 aliases) and executed no generator or runtime code.

## RF-1

`SELECTION_ADD` appends this to IDS-L `closureMembership.selectionLaw`:

> the core provider closure is a direct member exactly when the Plan selects a native.semantic-universe.syntax.v2 universe, and is never selected otherwise, explicitly included

The IE:1377 insertion in the same record says:

> and is never selected otherwise, not even explicitly

README row 5 says the pointer appends the same exception as row 2. The parent text says extra admissible retained closures may be selected explicitly. Item 9 (PROPOSAL-r7.md:443) and C2-T13 (PROPOSAL-r7.md:470) refuse the core provider in `semanticClosures` when no syntax universe is selected. The schema sentence, read after that parent grant, tells the reader to include the closure explicitly in the case the law refuses. The standing text and the IE:285 provider bullet state the clear rule. The defect is this one schema string. The replacement is in `review.json`.

## Rulings

**Exactness, other than RF-1.** The other eight insertions contain their `before` text and only insert. The IE:285 paragraph is item 9 with r6's X-C1: three projections of descriptor D, `manifestDigest` the raw SHA-256 of the TR-CORE-signed inventory body with the envelope excluded, the detector on bundled-pack `detectorClosure` and `finding.ruleClosure`, the adapter only as `import.adapterClosure` of `dependency` and `prepared` imports and never a `semanticClosures` member, and the provider's two uses. The syntax-universe fields match M3-E1 r3 item 14b (PROPOSAL-r3.md:568-593), the grammar stays kind `grammar`, and the stage-schema sentence applies the existing registration rule at IE:1303-1318. The detector's `semanticClosures` membership follows the unchanged direct rule for `finding.ruleClosure`, which the paragraph identifies with the core detector closure. The emission field is named in the paragraph and is the join site. COMP:9 states the Run-closure join: the seal's evaluator descriptor except for `kind`, `contributionId` in that pack row's `contributions`, and another core's detector cannot stand in.

**Form, LD-1 and LD-2.** EC1 already binds IE:273, IE:278, IE:455, and the original IDS artifact pointer (`core-evaluator-closure-ec1/successor.json`). A second override of those selectors refuses. CRC-1's selectors are free at `9c11c53` and at `cd5958b`. Overriding I1-L's selected copy, and extending the kind-`evaluator` wording by the later IE:285 paragraph, is the sound form. The artifact string on IDS-L is extended directly and names the same inventory body. The SYN-1F procedure, whichever unit binds second absorbs the other, is the right coordination. The live draft has moved (NBO-1).

**Recognition, LD-3, LD-4, and LD-5.** IE:285 recognizes a core role closure of a Plan exactly when its descriptor equals, except for `kind`, the descriptor of the core evaluator closure the Plan selects and its evaluation seal names. IE:1364-1366 requires the seal's evaluator to be that selected evaluator, so the test is one closure at admission and at Run closure. The `closureKinds` note's shorter "when the Plan selects" names that same closure on an admitted Plan. The admitted fields are a closed list, and `cache-key.producerClosure` is a real `byField` provider field and a direct member, so naming it is a real extra refusal. No new refusal code, class, exit, or route is introduced. Misuse stays on the existing closure-kind and membership refusals, and the detector join stays on X5's structural row.

**Consequential passages, LD-6.** WS:308, WSE:312, and the detector-manifest `/description` are the sentences that still said `closure.manifestDigest` identifies the component manifest body for the compatibility listing. Each insert says that for a core role closure the digest is the inventory body and the listing is the reserved file of the core platform tree. COMP:9 is the composition sentence that says what may stand in for a detector. IE:273 and IE:455 keep the component-manifest wording for other kinds and, by the IE:285 paragraph, hold equally for every core role closure. SL:28-70 is the component-manifest delivery path. Its receipt field `componentManifestDigest` is the admitted closure's `manifestDigest`, which is the inventory body for a core role closure, and CRC-1 leaves the field name to M5. NE, `enumeration-plan.schema.v1.json`, and `execution-inputs.schema.v1.json` do not say that every `manifestDigest` is a component manifest body and do not confine these three closures to a different field. ENS calls the enumerator a selected provider closure. EXS types `producerClosure` as `closure2`. The universe restriction stays the identity rule.

**X-H3, LD-8.** Leaving X-H3 out is required by the accepted law. Item 9 forbids the core provider on any TypeScript or Rust record (PROPOSAL-r7.md:443, :464, and :474). X-H3 is word for word between M3-H r1 and r2, and r2 is still REQUIRED-FINDINGS. Grok's R5 says the third use is lawful only as a successor and that H does not apply it before C r7 / CRC-1 (`reviews/grok-fact-admission-h-r1/REVIEW.md:42`). CRC-2 cannot rewrite these selectors: the second-override probe refuses. IE line 286 is blank, so a fresh paragraph there is a free selector. Pointers on whichever IDS copy is then selected are the right schema path.

**Law diff.** Item 7 and item 9 are the same text in r6 and r7. The byte diff is the round banner, the r7 change note, item 16 row 8, and R1. Row 8 selects the core evaluator and detector closures as inventory projections, outside R10a's component manifests. CRC-1's reading that the provider and adapter projections are the same kind of projection is item 9, and it agrees with that row.

**Vector and selection, LD-7 and LD-9.** The vector is reproducible from the `baseline-macos` fixture, matches EC1's core and evaluator closures, fits IDS-L's closed `closure` shape, and gives five pairwise-distinct ids in all 53 accepted cases. Product copies are untouched. Binding remains a later lock-only commit. The record is well-formed under `verify_design`'s contract-successor and successor-chain rules at 79 to 80 and at 82 to 83.

## Required finding

**RF-1.** Restore `not even explicitly` in `SELECTION_ADD` and regenerate. The full replacement sentence is in `review.json`.
