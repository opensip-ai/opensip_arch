Author candidate 04 is ready to freeze in `/tmp/opensip-implementation/m1-native-wire-owner-author-04`. It still needs your fresh independent review; I haven't approved it.

**Final run:** 478 checks, 0 failed. All 108 mutation controls were caught (14 reviewer-01, 13 reviewer-02 and all 8 reviewer-03 mutants), with a clean baseline. The isolated copy of the 39 inputs passed with the same check IDs and outcomes. `outcome.json` reports RF-1..RF-4 and A-1..A-9 as resolved by their named checks. `subject-files.json` (sha256 `a2293654…44ee`) lists 39 inputs, 4 outputs and 36 evidence files; every hash matches and there is no bytecode outside `tmp/`. The subject-03 results (373/78), its manifest and the review-03 probe outputs are kept under `prior/`.

**RF-1: path sites.**
- **Site set:** `pathSites` is a closed set of 10 sites, recomputed from the pinned schemas. It covers the three wire path scalars, occupancy `LogicalPath`, and six evidence path fields: `ExpansionSite.path`, `GeneratedFile.logicalPath`, `crateRootPaths`, `jsRootFiles`, `programRootFiles` and the dependency manifest path.
- **Complete-string checks:** each site is bound to a lexical rule run over the whole string, splitting only on `/`. A segment `..`+LF is legitimate; a bare `..` is not.
- **Pattern fix:** the owner pattern's lookahead stopped at line terminators. It is corrected at all 34 places it appears in the owner schema.
- **Result:** `x\n/../../escape.rs` is now refused at every site and `a/..\n` is admitted. This is checked against pinned Node for every site and binding.

**RF-2: one final owner for pattern evaluation.**
- **Choice:** the declared ECMA-262 `/u` dialect wins, not Python `re`. It is installed in memory on every loaded `canonical.ExactValidator` and on the model regexes that copy schema patterns (`_LOGICAL_RE`, `_UNIT_ROOT_RE`, `_MEMBER_ROOT_RE`), not in the source files.
- **Pinning:** changed owner functions and everything they call carry source digests.
- **Legitimate names:** the owner now admits `a/..\n`, `..\n` and `a/.\n` with identities.
- **Bad paths:** they get a routed refusal before the owner runs, never an untyped `ValidationError`. A new key, `native.prepared-output-not-wire-representable`, covers prepared paths.
- **Evidence:** the pinned owner's two defects are reproduced as evidence, and a differential test over all 28 owner patterns shows 0 disagreements with Node.

**RF-3: prepared modes and route semantics.**
- **Mode rule:** an over-limit set is refused when prepared mode was explicit. When defaulted, it falls back to non-prepared analysis with a disclosure, following the owner's stale-row law. The rule, selector and route row now say the same thing, and both modes are tested.
- **Error codes (A-1):** the two limit keys moved to `REQUEST.UNSATISFIABLE`, matching the owner's bound-exceeded family (`PROJECT.SCOPE_LIMIT`). The two representability keys keep `REQUEST.PRECONDITION_FAILED`.
- **Route semantics (A-2):** remedy wording is now checked for all 17 (key, fault) pairs the vectors produce. Timing is tied to each owner function and its owner text, and the new origin must derive request-rejected under the owner's origin rule.
- **Mutants:** swapped details, wrong remedy text, moved timing, and a host-invariant origin are all caught.

**RF-4: sender bound to the plan.**
- **Minimality claim removed:** greedy chunking is deterministic but not byte-minimal. Under the owner encoder, `[7,23]` costs 572 bytes against greedy's 574.
- **Send plan:** the planner produces a fixed plan (frame slots, one reserved Cancel, seal chunk counts). Refusals are stated only as "does not fit under the canonical host send schedule".
- **Reference sender:** `tools/sender_ref.py` consumes the plan and refuses any divergence, including the byte-smaller lawful chunking. It re-checks the frame, request-byte and request-frame limits after every frame. An independent realization agrees with 12 accepted plans.
- **Kept:** the 40-byte prefix exclusion and the single-Cancel rule are unchanged.

**Other advisories.**
- **A-3:** `plan2` is computed but not published, with no run, Coverage or worker; the line-2848 anchor is timing only.
- **A-4:** exact TS2 manifest-frame vectors at 67,108,864 bytes and one byte over.
- **A-5:** seal chunk counts are pinned.
- **A-6:** newline-hidden `..` dependency vectors.
- **A-7:** the Cancel rule is stated and checked against P3-29.
- **A-9:** callee-closure digests.
- **A-8:** the 36 pins still match. 23 of them differ from HEAD `c3856824`, and other work is still changing the tree, so I make no clean-git claim.

**Limits:**
- **Node:** only the binary is pinned; its system libraries are a trusted, unpinned boundary.
- **Audit:** it only sees file opens and process launches, so it is not a confinement proof.
- **Owner fix:** it applies only in memory; no owner source file was edited.
- **Not claimed:** production codec, admission, sender, generator, platform or M2/M3.

**Mistakes I made and fixed along the way:**
- One control was vacuous (it set a binding to its own value).
- Another expected the wrong check.
- A length cache returned stale values.
- Some hand-written frame counts were wrong.

Nothing was committed or pushed, and I read no private sessions.
