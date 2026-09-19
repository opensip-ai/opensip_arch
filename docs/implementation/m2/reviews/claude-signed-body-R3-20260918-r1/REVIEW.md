# Independent bounded probe review — signed-body R-3 (re-signed near-valid stored bodies)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. This carries out the concrete probes I named in platform123 F-2. **Bounded evidence
only**: not a universal fuzz result, not whole-security approval, and actual external signatures, OS and
root custody remain conditional. No frozen/selected/product edit; the probe is inserted into a scratch copy
only; no commit, push or delegation.

## 1. Subject and inputs (exact)

| Item | Value |
|---|---|
| Product under test | my verified extraction of frozen **124** (`linked-capture-checkpoint-124`, archive `9e07e634…62c3`); its `crates/security/src/trust.rs` is **byte-identical to 123's** (`cmp`), SHA-256 `8f3b37357d8bb85d173281b68bf3078e6d13453b29ac03bfc8442d985f13d8a1` |
| Composed reference | `envelope_reference.py` + model from my verified **125** tree (the primary model is unchanged since 122) |
| Signing keys | the **public TEST-ONLY** quorum62 seeds, `SHA256("opensip-public-test-only-quorum62-seed-" ‖ byte(i))`; `keys.py` derives the public keys with real OpenSSL and confirms that **every** key of `quorum-roots`, `profile-roots`, `recovery-root` and the chain anchors (27 / 27 / 27 / 33) comes from them. They confer no authority. |
| Signing | real OpenSSL 3 `pkeyutl -sign -rawin` over the v8 `envelope_message_hex`, after recomputing `storedSha256` and the domain-framed `preimageSha256` for each mutated body |
| Pins | `claude-out/hashes.txt`: generator, key script, probe source, run notes, all three input corpora (35 MB, each line = stored bytes + complete signed envelope + context), all three Rust outputs, both comparisons |

**Framing self-check.** Ed25519 is deterministic, so a correct re-signer must reproduce the fixtures. It
does: the unmodified **revocation** and **root-chain-link** controls come out **byte-identical to the
fixture envelopes, signatures included**. The recovery control differs only because the fixture's stored
epoch is not in canonical key order and I re-encode canonically; it still verifies at the carrier and the
reference applies it.

## 2. Method
From one valid, admitted body per kind: a control, every single-member **deletion**, every single-member
**replacement** from a 20-value pool (null, booleans, 0, 1, −1, 2⁵³, 2⁶³−1, 2⁶³, empty/short/hex/upper-hex
strings, an impossible calendar date, a valid date, an offset date, empty and non-empty arrays and
objects) at every path (first two elements of each array), plus one unknown top-level member. Each mutated
body is canonically encoded and **genuinely re-signed by the same signers**, so the carrier verifies and
payload admission is actually reached. The Rust boundary is called with shape-valid roots and the
fixture's own context, under `catch_unwind`. Nothing mutates evidence after its constructor.

## 3. Results

| Boundary | Inputs | Raw quorum at the reference carrier | Panics | Rust outcome | Against the reference |
|---|---|---|---|---|---|
| `verify_revocation` | 302 | **302 / 302 VERIFIED** | **0** | 24 admitted, 276 `Shape`, 2 `RootVersion` | no composed revocation admit exists in the reference, so I compared with the retained `revocation.schema.json` + calendar rules + root-version equality: **302 / 302 identical** |
| `propose_recovery` (epoch body) | 242 | **242 / 242 VERIFIED** | **0** | 5 proposed, 237 refused | `Verifier.admit_signed_recovery_epoch`: **0 admission disagreements, and the refusal detail is identical in all 237** (`SHAPE:counters` 70, `SHAPE:challenge` 57, `SHAPE:kind` 19, `SHAPE:installBinding` 19, `SHAPE:recoverySchema` 18, `SHAPE:issuedAt` 18, `SHAPE:epochSerial` 16, `SHAPE` 8, three `COUNTER_MISMATCH:*` ×3 each, `TIME_BEFORE_LAST_ACCEPTED`, `CHALLENGE_MISMATCH`) |
| `verify_root_chain` (one link) | 1,302 | reference reaches `root-chain` for 38; 1,264 stop at `root-document` | **0** | 35 accepted, 1,264 `Payload(0)`, 2 `Gap(0)`, 1 `FinalExpired` | `Verifier.admit_signed_root_chain`: **0 disagreements**; `ROOT.CHAIN_GAP` ↔ `Gap(0)`, `ROOT.FINAL_EXPIRED` ↔ `FinalExpired` |

**1,846 genuinely signed near-valid bodies, plus 9 targeted possession cases: 0 panics, 0 admission differences.**

Everything admitted is a *value-valid* substitution, which is what a near-valid generator should also
produce: the same value re-inserted (`1` for a schema member that is 1), a different valid timestamp,
another valid integer (`2⁵³`, `2⁶³−1` for a version; `2⁶³` is refused), a deleted array element, free-text
members (`label`, namespaces), an empty `entries`. Deleting any required member, any wrong type, the
impossible date, the offset date, upper-case hex where hex is required, and the unknown member are refused
at every path.

What the chain rows cover, as asked: link **schema** (`rootSchema` replaced/deleted → `Payload(0)`; the
value-equal replacement accepted), **continuity** (`previousRootVersion` / `rootVersion` → `Gap(0)`) and
**expiry** (`expiresAt` → `FinalExpired`). **Key possession was *not* reached by the single-member
mutations**: all 60 `rootKeys` and 20 `rootThreshold` mutations (and 100 `recoveryAuthority`, 166 of 180
`keys`) are refused at *document* admission by both sides, before any quorum logic. So I added nine
targeted cases with a **valid** mutated root document (`gen_possession.py` → `root-chain-possession.*`):

| Case (new-root keys that signed / rootKeys, threshold) | Reference | Rust |
|---|---|---|
| control (2/3, 2) | ACCEPT | ACCEPT |
| new root lists only one signer among its rootKeys (1/3, 2) | `ROOT.CHAIN_NEW_THRESHOLD` | `NewThreshold(0)` |
| new root's rootKeys are all non-signers (0/3, 2) | refused at the carrier, "no valid signature from authorized key" | `NewThreshold(0)` |
| new threshold raised to 3 (2/3, 3) | `ROOT.CHAIN_NEW_THRESHOLD` | `NewThreshold(0)` |
| one new-root signature removed | `ROOT.CHAIN_NEW_THRESHOLD` | `NewThreshold(0)` |
| one old-root signature removed | `ROOT.CHAIN_OLD_THRESHOLD` | `OldThreshold(0)` |
| only old-root signatures | carrier, no valid signature | `NewThreshold(0)` |
| only new-root signatures | carrier, no valid signature | `OldThreshold(0)` |
| no signatures | carrier, malformed envelope | `Envelope(0)` |

**9 / 9 agree on admission**: a rotation is accepted only with a genuine quorum under the old root *and*
genuine possession under the new one. The only difference is class: with zero valid signatures under one
of the two roots the reference stops at the carrier, Rust names the unmet threshold. My first version of
these cases was **mislabelled** — I chose "non-signing" keys from the new root's key table without
excluding the old root's keys it still lists, two of which are signers, so both sides correctly ACCEPTED
what I had labelled a possession failure. That run is preserved
(`root-chain-possession.failed-r1.*`, `gen_possession.failed-r1.py`) with a note; it was never a finding.

## 4. Findings

**None against the Rust boundaries.** Two observations, neither a new defect:

- **O-1 (schema-level, shared)** — a revocation entry's `subject` is any 1–256-character string whatever
  its `subjectKind`. `{subjectKind: "keyId", subject: "x"}` is admitted by the retained schema and by Rust
  alike. It cannot match a real key id, so it revokes nothing — but a publisher's typo in a key revocation
  is accepted silently. If `keyId` subjects should be 64 lower-hex (and `catalogSnapshot` subjects
  canonical decimals, cf. 116 N-1), that is a schema-owner decision, not a Rust fix.
- **O-2 (scope reminder)** — the separately adjudicated recovery **record** defect (unsigned caller input,
  my 123 F-3 and the recovery-record r1/r2 adjudications) is not re-counted here: in this corpus the record
  is the fixture's valid one and only the **signed epoch body** varies.

## 5. Limits
One base document per kind; one mutation at a time; arrays sampled to their first two elements; roots and
context valid; one link per chain; no revoked-signer interplay; no oversize or deeply nested bodies (the
metadata limits are covered elsewhere); macOS arm64 only. This narrows R-3 for the three signed-body
paths I had named as unprobed; it does not close R-3, and the owner's regression and fuzz gates remain
necessary. The corpus is retained and runnable (`claude-out/RUN.md`) so the 127/128 successors can be
checked against exactly the same 1,846 inputs.

## 6. Bounded verdict
**Signed-body R-3 probes: 0 panics and 0 admission disagreements with the composed reference (or, for
revocation, with the retained schema) over 1,846 near-valid stored bodies that genuinely reach payload
admission, plus nine valid-document key-possession cases.** No new finding; R-3 remains open as a general obligation. Not approval of the signed-security
group, of evidence encapsulation (128), or any cumulative, OS, custody or release standing.

Evidence: `claude-out/gen_corpus.py`, `keys.py`, `rust_probe.rs.txt`, `RUN.md`, `gen_possession.py`, `corpus/*` (inputs,
`*.rust` outputs, `generation-stats.json`, `comparison.json`, `revocation-vs-schema.json`), `hashes.txt`.
