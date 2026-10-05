# S-OP-2-R review

**Verdict: ACCEPT-DESIGN-UNIT.** Required findings: none. `supersededPassages: []`.

Subject manifest: `docs/implementation/m3/operability/s-op-2/s-op-2-r-subject.json`, **1,245 bytes**, SHA-256 `1d8e41be18a53dfd273cab0bb799bd95b07905caa8fddbb2e481bbe639425e4e`. All six members match their exact byte/hash pins and were stable through final verification. The accepted SOP2 r6 member is 130,001 bytes / `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`. The assent draft is not a subject member.

## Faithfulness and scope

Both overrides reproduce accepted SOP2 item 24, lines 921–926, character for character. Each removes back to its original parent passage without changing punctuation:

- SDK4 `/standardizedFamilies/1/rule` keeps the complete original sentence sequence, then adds the one sentence restricting host operational records to SOP2 registry events and SafeField kinds. It explicitly keeps the doctor report's DR-114 redaction tiers.
- DRC line 576 inserts the one host byte-count/truncation sentence between **meaning.** and **The SDK owns framing,**. Removing it restores the exact original line.

The manual pointer/line comparison, insertion-only reconstruction and accepted-proposal comparison pass; see [design-unit-checks.json](../design-unit-checks.json). F02 is neither a parent nor overridden. The five candidates plus successor record cover the six reviewed members, including the actual accepted law bytes.

Neither passage has an existing selected override or supersession at b7b87b7. These are plain passage overrides, and the empty supersededPassages list is correct. R needs P first because its parents are not otherwise selected. I agree with the lead's two-unit selection decision. Acceptance records existing SOP2 meaning; it introduces no new code, schema, class or product qualification.

## Independent binding evidence

The pinned helper ran in this review's own detached worktree of `b7b87b740b4332597ef9d609b1e96d7b420f8885`, at nice 19, with an isolated home and private 0700 Darwin-user TMPDIR:

- Baseline: PASS, 101 contracts / 5 passage supersessions / v138.
- R alone: REFUSED for unselected parents, with and without implementation checking.
- P→R: PASS, 103 contracts / 5 supersessions, with and without implementation checking. Other chains and verified inputs stay equal to baseline.
- All nine probes match expectations: wrong subject/review passage list, altered before-text, JSON line selector, duplicate override, duplicate selection and missing accepted-law member refuse; a properly formed later VD2 supersession passes.

See [local-binding-check.json](../local-binding-check.json) and [pin-verification.json](../pin-verification.json). The literal appended-lock CLI fails closed on missing SCRATCH review files; the overlay result establishes local binding, not actual integration. Actual root assent and sequential P→R integration remain necessary. Builder/checker source was inspected; their reported 37-check run was not independently repeated.

## Nonblocking observation

**S-OP-2-R-NB-01:** REQUEST.md's context self-pin is stale: expected 14,923 bytes / `516611d2cd1c914552bfc1299fb1256dc4703c269fe64006c6605e22220d7d82`; observed 15,899 bytes / `5351a04e88ff2cca0626293a2dae2e5afe9dea05830418fdef2edf0b2cbc7abb`. I followed the current request including lead answers. All 49 other pins match, including this subject and all members; all observed files remained stable. Refresh the context pin for a later request.

The O1 law's separate unit-dependency finding does not affect R. No Cargo, build/test lane, crash matrix, repository source edit, commit, delegation, real-home or private-fixture access. The private verification worktree and TMPDIR are removed; see [cleanup.json](../cleanup.json). This is acceptance of these exact design bytes.

