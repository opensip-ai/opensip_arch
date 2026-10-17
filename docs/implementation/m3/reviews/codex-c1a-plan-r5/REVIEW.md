# REQUIRED-FINDINGS — C1a plan r5 amendment

Subject manifest SHA-256: `3e9d3a96b75ace40662d03a8a90a34e8e2784770b1eb6ef1b9a7e4140ad22517`. Both members match their declared bytes and hashes. Accepted r4 is unchanged (36,209 bytes, `73ce52b14a84a8a51a74225ac08ea3f7171fe45d15e7b23ab7a4b17281e9cafe`). r5 is 40,241 bytes, SHA-256 `d5fa30f86abaa653bd91f586bf6e94cef2b4f7c1f0063476681286e791424df2`. Product HEAD is clean at `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `5c92b4f7f2055a841347bcaf758844b7a50b6ba9`.

**Q5: an explicit M3-C law record is needed before C1a4 adopts the new rule.** The discovery precedent selected its changed caps through M3-B r6 after measured alternatives. It does not make a plan amendment a substitute for the return-to-law step. The conservative supremum can remain informational under a new law decision; it need not remain the selected cap merely because r4 used it.

## Required findings

### C1APLAN-R5-RF-1 — The replacement cap and margin rule needs an explicit law gate

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r5.md:13`. r4's stated return-to-law trigger has fired. r5 now adopts a different population/corpus cap rule, adds power-of-two rounding and exempts over-item-5 entries from the margin obligation. M3-C item 2 asks for a maximum-population recipe derivation and extends the T2 margin test; it does not explicitly select this new empirical formula or qualification exception. M3-B r6 is a precedent for a separately reviewed law amendment selecting caps after measured options, not for silently adopting a replacement rule in an implementation plan.

Required change: Gate C1a4's cap selection/profile publication on an accepted M3-C r9 law record (or equivalent explicit law revision). Have it settle the derivation population, empirical T2 role, rounding rule, over-item-5 classification and margin coverage, and the rejected alternatives. C1a1–3 may remain scoped preparatory library/model work without a production snapshot-profile claim.

### C1APLAN-R5-RF-2 — The item-5 reference population and its full charge are not defined

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r5.md:14`. Term (a) is described as 100,000 rows whose canonical inventory is at most 4 MiB. No such inventory exists: the 64-character digest values alone take 6,400,000 bytes before paths, keys and framing. It could instead be a conservative componentwise envelope, but the plan must say so and define its formula. Row count and total payload also do not determine directory/listing, excluded-name, ACL, repeated-copy, read-attempt and custody work. The current C1a1 model predicts the walk only; read, retention and custody terms are explicitly still to be added.

Required change: Define (a) as either a feasible admissible-population optimization or an explicitly conservative componentwise bound, with the full descriptor envelope distinguished from inventory bytes. Specify all operation counts and worst-branch charges, including directory/non-inventory work, bounded short-read/Interrupted/EOF attempts and C1a2's custody/capture/row costs. Do not substitute a typical or impossible tree for the normative population. Make completion and review of this formula a prerequisite to the cap calculation.

### C1APLAN-R5-RF-3 — One blind run cannot both choose an unknown cap and bind its later closure change as ordered

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r5.md:239`. C1a4 evaluates held-out maximum (c), uses it to choose the cap, then changes snapshot_profile/work_ledger.rs and re-pins the census. It nevertheless promises one gated blind run that both supplies (c) and refreshes the discovery receipt against those final bytes. Under B2-b4 plan r6 section 2.5 the receipt binds current caps, tool bytes and every closure pin, including work_ledger.rs. A measurement before the final cap is written is stale after that change; a final receipt run after the change cannot be the earlier run that first supplied the unknown maximum.

Required change: Specify a non-circular, pre-reviewed protocol. For example, use a separately reviewed blind derivation phase with an explicitly allowed closed output, then freeze the law-approved caps and closure pins, followed by the reviewed final receipt run; or choose caps entirely before a single final validation run and return failures to the law. Name all reviews, outputs, staleness transitions and run counts. Do not expose raw held-out counts or imply a changed-pin receipt remains current.

## Other requested decisions

**Reordering:** Moving the constructor, its final cap and the work_ledger.rs re-pin together into C1a4 preserves r1 RF-4's key invariant: no constructor precedes its reviewed cap. C1a1–3 can test borrowed WorkScopes on the discovery profile as expressly partial, no-caller support. Those tests do not establish the eventual snapshot profile's bounds or margins. If no closure file changes earlier, the discovery receipt remains current earlier. RF-3 is needed to make the later transition executable as specified.

**Over-item-5 entries:** Reporting a genuine semantic-bound failure separately from successful snapshot populations is sensible, without inventing a successful seal or margin. The law must state how that classification affects its all-entry margin obligation. Until then, dropping those entries from the gate is not an established consequence of item 5. Such entries still exercise walk-phase work before semantic bounds, so their budget/failure classification cannot be assumed from final inventory admissibility alone.

**Model evidence:** Inspected the contextual model and its native soundness/oracle controls. The imported discovery_census.py is byte-identical to product main. Its shared cost closure is checked whole and by anchors; the snapshot modules have whole-file pins and shape anchors. The model charges all listed entries before extent classification and uses dearer capture branches. This is a useful construction for the snapshot-walk portion, with 28 accepted automatic discovery cases and four generated cases. It does not yet model host content reads, capture retention, blob custody or sealing, which r5 leaves to the later extension.

Independently ran only the specifically permitted command in the C1a1 worktree:

`python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`

It passed and reproduced the 32-case vector bytes; the two snapshot whole-file pins also match. This path loads the public reference and synthetic vector trees, not T2 stores. The native soundness test asserts used <= predicted for all 32 cases; the oracle test requires 28 exact file-set matches. Neither native test was run in this review. Equality of every native charge, universal model coverage and C1a1 acceptance are not inferred from the Python replay. The candidate's full review remains separate.

The full r4-to-r5 diff was inspected. The new derivation rule and constructor/receipt sequencing are the substantive changes; inherited capture, source-read ownership, retained-parent opening, VCS/read-set limits, carrier join and final semantic-bound order remain in place. No product caller, corpus result, law acceptance or qualification follows from this amendment review.

No non-blocking observations. No compiler, product build, other test/generator, lane, network, delegation or prohibited private-data access occurred. Only the allowed model check and read-only file/hash/JSON/Git operations were used. Only this directory's `REVIEW.md` and `review.json` were written; neither repository nor worktree was edited.
