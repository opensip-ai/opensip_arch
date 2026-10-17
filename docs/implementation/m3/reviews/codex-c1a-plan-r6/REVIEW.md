# ACCEPT — C1a plan amendment, round 2 (r6)

Subject manifest SHA-256: `caa54dc6e80c7b8b9dd2f33965bca1309fc843e819d42a156423dc99cfb29c2c`. All three members match their declared bytes and hashes. Accepted r4 and reviewed r5 remain unchanged. r6 is 42,711 bytes, SHA-256 `3668221c025d2f678aa59e48c8cd25412c903eaf395d13f782f7915db50cd76e`. Product HEAD is clean at `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `5c92b4f7f2055a841347bcaf758844b7a50b6ba9`.

## Prior findings resolved

- **C1APLAN-R5-RF-1:** C1a4 cap selection and profile publication now require a separately accepted M3-C r9 law record. The former r5 formula is withdrawn as a plan rule and retained only as a recommendation to that law review. Derivation population, census role, rounding, over-item-5 classification, margin coverage and rejected alternatives are explicitly reserved to r9. C1a1–3 remain preparatory library/model work, with no production profile or caller claim.
- **C1APLAN-R5-RF-2:** Term (a) is explicitly a conservative componentwise bound rather than an impossible 100,000-row/4-MiB tree. The plan separates row/open counts, full-descriptor path budget, payload, per-file attempt envelopes, non-inventory/directory/ACL/copy work and C1a2 custody/capture/retention charges. Completion of the model and review of r9's formula precede cap adoption. This is an adequate plan-level prerequisite; numerical counts, coefficients and proof remain to be reviewed there, rather than inferred already sound.
- **C1APLAN-R5-RF-3:** Caps are chosen from the componentwise bound and lead-readable census before any held-out run. The constructor and closure re-pin freeze those bytes and make the old receipt stale. One pre-/post-reviewed blind validation run then measures against those frozen caps and writes both receipts. A failing/erroring in-scope result returns to the law and starts a new cap-choice cycle. The review/run counts and stale interval are now explicit and non-circular.

The full r5-to-r6 diff is confined to those resolutions, bases, the revised C1a4 section and the answered Q5. Earlier proposal language is superseded by the explicit r6 withdrawal and gate.

## Requested decisions

**Q5 / law authority:** The answer is now correctly recorded: r9 gates C1a4. Acceptance of this implementation plan does not accept r5's former formula as current M3-C law. The formal discovery-law precedent is respected rather than used to bypass a law revision.

**Rule and population:** A conservative componentwise envelope is a legitimate way to define a proposed derivation, provided the completed formula proves every stated count and charge at the proper stage. The full canonical descriptor must include framing, digests, lengths and escaping. Per-file ceilings must be summed conservatively, including short/Interrupted/EOF attempts; non-inventory work cannot be inferred from final row count. Those numerical obligations are explicitly pending C1a2/r9. Likewise, over-item-5 classification and the resulting margin coverage are proposals for r9, not a currently granted exemption. An unclassified error cannot be treated as proof of exclusion or a passing margin.

**Reordering:** Moving the constructor and its cap together to C1a4 preserves the original no-constructor-before-cap invariant. Discovery-profile testing in C1a1–3 is disclosed preparatory evidence and establishes no production snapshot-profile margin. With no earlier closure changes, the discovery receipt remains current until C1a4's re-pin. The final blind receipts must bind the final code, caps, model/tool inputs and other required pins under B2-b4-r6's closed protocol; changing them afterward would stale the receipts again. This plan acceptance neither executes nor independently approves a future blind mode.

**Model evidence:** The imported discovery census is byte-identical to product main. The model retains shared cost-closure checks and anchors, snapshot whole-file/shape pins and dearer-branch captures. The vector set has 28 accepted automatic discovery cases plus four generated cases; snapshot-module pins verify. This supports the stated walk-model purpose, while full C1a1 review and the later host-read/custody extension remain separate.

Independently ran only the permitted command in the C1a1 worktree:

`python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`

It passed and reproduced the vector bytes. Its checked path uses the public references and synthetic vector trees, with no T2-store access. No native tests were run: native <= predicted on the 32 trees, the 28-case oracle and the reported exact native equality remain implementation evidence for the separate C1a1 review, not results independently established by this Python check.

No required findings or non-blocking observations remain. This acceptance covers the revised sequencing and gates; it does not complete r9, cap derivation, corpus validation, C1a1, C1 or product qualification. No compiler, build, other test/generator, lane, network, delegation or prohibited private-data access occurred. Only the allowed model check and read-only file/hash/JSON/Git operations were used. Only this directory's `REVIEW.md` and `review.json` were written; neither repository nor worktree was edited.
