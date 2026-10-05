# S-OP-2-P review

**Verdict: ACCEPT-DESIGN-UNIT.** Required findings: none. `supersededPassages: []`.

Subject manifest: `docs/implementation/m3/operability/s-op-2/s-op-2-p-subject.json`, **622 bytes**, SHA-256 `65af7fd35c9f5439d50d46e1b7769f7acee43c62c3436c6122c3b36f379f456f`. All three manifest members match their exact byte/hash pins and were stable through final verification. The assent draft is context, not a reviewed member.

## Assessment

The parent-selection defect is real. At product `b7b87b740b4332597ef9d609b1e96d7b420f8885`, SDK4 and DRC are neither source/application-manifest members nor candidates of the 101 selected contract successors. APP pins them without selecting their bytes. The independently repeated binding check rejects R alone with **contract parent is not an accepted base or selected inventory**.

P lawfully selects exactly those two existing files, with APP as its only parent and no override, following the bound control-source-v1 selection form:

- SDK4: 17,867 bytes / `c53d541f12258eb96e86f0f5dbd3924a5f2e189d19c8f8672bae9037532461c3`; APP `/rows/12/inheritedContract`.
- DRC: 49,989 bytes / `9ab2874edafa6e37ce9c552db50f985135ca311ab7be7570cfc41558e46ce0d1`; APP `/evidenceTargets/D.SDK/sources/0`.

SDK4 retains its CANDIDATE-NOT-APPLIED header and its stated absence of application authority. P binds the byte provenance and existing DR-125 inheritance; it does not apply the candidate SDK or grant new component authority. Selecting the whole DRC file likewise does not expand APP's D.SDK section-8 inheritance. The carriedLimits and acceptanceDoesNotQualifyProduct fields make this scope explicit. I agree with the lead's two-unit decision and answer Q5.

There is no existing override or supersession for either target passage. P itself has no overrides, so an empty supersededPassages list is correct.

## Independent verification

The permitted pinned verify_scratch.py ran in this review's own detached worktree of b7b87b7, at nice 19, with an isolated home and a private 0700 Darwin-user TMPDIR. P alone passes with and without the implementation check: 102 contract successors, 5 passage supersessions, unchanged inventory and other non-contract chains. P→R passes at 103/5. The duplicate-selection probe refuses; the other eight probes have their specified results.

Evidence: [local-binding-check.json](../local-binding-check.json), [design-unit-checks.json](../design-unit-checks.json), [pin-verification.json](../pin-verification.json). The literal appended-lock CLI correctly refuses missing SCRATCH review files; the overlay supplies local binding evidence. Actual root assent and integration remain separate. Builder/checker source was inspected, without independently repeating their reported 37-check run.

## Nonblocking observation

**S-OP-2-P-NB-01:** REQUEST.md's context self-pin is stale: expected 14,923 bytes / `516611d2cd1c914552bfc1299fb1256dc4703c269fe64006c6605e22220d7d82`; observed 15,899 bytes / `5351a04e88ff2cca0626293a2dae2e5afe9dea05830418fdef2edf0b2cbc7abb`. The current request including lead answers was followed. All 49 other pins match, including this subject and every member; all observed files remained stable. Refresh the request pin for a later request.

The O1 law's separate unit-dependency finding does not affect this selection. No Cargo, build/test lane, crash matrix, repository source edit, commit, delegation, real-home or private-fixture access. The private verification worktree and TMPDIR are removed; see [cleanup.json](../cleanup.json). This verdict qualifies the exact design unit, not product implementation.

