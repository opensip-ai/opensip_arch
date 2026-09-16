# Comments on `root-F00-F37-proposed.json` (awareness only)

**Standing.** Root owns these edits. This file is comment only: root's input
(`root-F00-F37-proposed.json`, sha256 `aa75d20d1f26eef019349066ae5f083df6926597703a950991387174652857b8`,
27358 bytes) is **not modified**. Nothing here is a change request; it is what I noticed while
checking the proposal against the laws this correction selects.

## What the proposal settles

It resolves the item I previously carried as a remaining gap. The internal `indeterminate` spelling
is gone from F00–F37 and replaced with the separated standings — `unknown-custody`,
`unknown-attempt-open`, `durability-undetermined`, `binding-unusable` and `snapshot-dependent` —
and `conclusionStanding` states directly that `durability-undetermined` projects
operational-failed / exit 4 and "never the policy indeterminate class/exit3". That closes the
overload. It also carries the negative-conclusion rule verbatim: `settled`+`refused` plus both rows
confirmed absent in one coherent snapshot.

F32 keeps root's typed route unchanged, and F36's substance is preserved.

## Three consistency observations

1. **`snapshot-dependent` has no projection row in my §1 table.** It appears on F29 and is a
   reasonable standing, but `commit-recovery-readonly.v3.md` §1 does not map it to a class,
   `errorCode` and `faultCause`. Either it should get a row there, or F29 should resolve into the
   existing standings it decomposes into (`committed-historically`, `unknown-attempt-open` or
   `unavailable-busy`, depending on what the one snapshot held). I did **not** add a row for it,
   because the vocabulary is root's to settle and C12 validates only what §1 declares.

2. **F36's `unknown-attempt-open` is a pre-sweep standing, and reads as permanent.** The text is
   right that an orphan SEAL "must never become a committed Run". But under the two-outcome custody
   model, that attempt does not stay `unknown-attempt-open` forever: once the authorized sweep
   observes a free lease and a readable ledger with neither row present, it settles `refused`, and
   the attempt then reads `terminal-not-committed`. Both answers are correct at their own time. If
   F36 is meant to describe the pre-sweep observation it is exact; if it is read as the terminal
   standing it understates what the sweep establishes. A clause naming the post-sweep standing
   would remove the ambiguity.

3. **F14 does not mention pending settlement.** "All commit barriers completed, acknowledgement
   lost" is precisely the lawful interval of §2.1: the receipt exists while the custody row may
   still be `admitted`. `committed` is the correct conclusion, and no change is needed to it — but
   the operational `pendingSettlement` disclosure is unstated, so an implementer could read F14 as
   requiring a settled row before answering committed. One clause would settle it.

## Nothing else conflicts

I checked F12, F23, F29, F34, F36 and F32 against the selected pre-settle interval law, the
two-outcome custody model, the negative-conclusion rule and the sweep's permitted writes. F12's
"Leave unresolved custody admitted for the authorized sweep" matches §4 exactly. F23 and F34 match
`unknown-custody`. No case asserts a third custody outcome, none infers absence from a phase alone,
and none treats a receipt present before settlement as a defect.
