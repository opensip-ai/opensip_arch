# Proposed opaque slot carrier: C2A3-LIBSRC-R1-RF-1 correction

Unaccepted additive interface clarification of the accepted C2a3 plan r2.
It changes no public/serialized code, cap, ledger owner, retention step or M fee.

## Selected shape

Add two root-public opaque lifecycle types under the existing macOS gate:
PreparedCandidateSlots and CandidateSlotClaim. Both have private fields and no
Clone, Default, Deserialize, public field constructor, raw slice conversion,
DerefMut, resize/push/extraction or mutable candidate accessor. The operation
frame owns prepared storage outside the admitted result, exactly as before.

PreparedCandidateSlots borrows the ordinary-reader component slice and owns the
Vec<Option<ClosureCandidate>> privately. Its sole constructor is
AdmittedSet::prepare_slots(components, work). It derives count from that actual
slice, charges the candidate-array fee, then allocates and initializes exactly
count None slots. It stores the matching slice privately. External callers can
neither choose a mismatched count nor populate slots outside the constructor.
Zero components allocate and charge nothing; authenticated core evidence still
comes from its own receipt handoff.

prepare_slots keeps its exact selected half of shared accounting:
R(n*Sc) + (0,4n,4n*Sc), when n>0. The result array is charged and allocated once
inside admit: R(n*Sr) + (0,4n,2n*Sr). Their aggregate equals the accepted shared
fee R(n*Sc)+R(n*Sr)+(0,8n,4n*Sc+2n*Sr). Concrete carrier metadata/moves must remain
within this source-audited allowance; if not, stop for a reviewed price change.
This adds no claim that ABI, allocation behavior or actual charges are proved.

## One-shot claim without an operational slot failure

PreparedCandidateSlots::claim(&mut self) returns Option<CandidateSlotClaim>.
The first call flips its private availability flag before lending its private
slot slice; subsequent calls return None without allocating or minting a claim.
The claim privately contains that slice and the constructor's matching component
slice. It cannot outlive/move/grow its owning storage. Its only consumer is
AdmittedSet::admit, which takes the claim **by value**, not a raw slice or a
prepared carrier that can be admitted repeatedly. No claim is Clone or Copy.
None is a closed, spent capability observation, not a component failure route
or permission to return an empty/partial admitted set. Native wiring must obtain
one fresh owner/claim on its original admission ledger and preserve its source
controls; this library does not claim a new production caller.

admit derives count/order from the claim. The component and slot lengths match
by private construction. Consume the mutable slot slice's IntoIterator so each
candidate reference retains the full owner borrow. For each slot, construct its
candidate through C2a-1, insert via Option::insert and immediately perform full
retention before advancing. There is no public-reachable prepopulated or wrong-
length state, no private Fault::Slots and no slot-to-Invariant conversion.
The claim stays spent even if candidate or retention fails; completed payloads
and pins drop, partial candidates remain unadmitted private storage, and the
original failed ledger cannot be reopened. No retry on fresh slots is licensed.

The existing public unit Invariant and its collector-only fixed record key are
unchanged. No new slot operational-record key, public detail or invariant basis
is selected. Core/sink/production owner gates remain exactly as accepted.

## Lifetimes and validation owed

The proposed owner is PreparedCandidateSlots<'input,'manifest>, borrowing the
component slice for 'input. claim(&'borrow mut self) yields
CandidateSlotClaim<'borrow,'input,'manifest>, with 'manifest:'input:'borrow.
The admitted set borrows the slots for 'borrow. No self-referential owning
return, unsafe code or lifetime extension is permitted. Compiler pass/fail
controls must establish expressibility before source implementation acceptance.

Required controls: external raw None vectors cannot satisfy admit; no public
constructor, mutable extraction, resizing, prepopulation, Clone/Copy or second
claim; exact candidate fee before allocation; result fee charged once; equal
aggregate shared price; zero-component case; original-ledger propagation in
owning composition; serial refusal order; failure pin release and no partial
admitted set; moving/dropping/growing owner while a claim or admitted set lives
fails compilation; independent source/ABI/move/allocation controls. Plan/source
acceptance cannot substitute for executing those controls under the native gate.

All broader C2a3, signed ordinary-reader fixture, source/native/recipe/unit,
inventory/production/census/fit and project qualification gates remain open.
