# Independent scoped reviews — frozen trust-codecs-wip-227-r8 and core-distribution-wip-229-r1

Two bounded reviews of root-corrected frozen bytes. **Not approval of my earlier author proposals,
not cumulative, not readiness.** No product/arch/candidate edit, commit or push; output only here.

## Verification and reproduction (both subjects)

- 227 r8 `9cedf041…8cde` (153196 B, 207 members) and 229 r1 `10d83d6a…57f6` (67440 B, 31 members):
  archive pin and EVERY `subject.json` member (path, sha256, bytes) verified from the tar before
  extraction; no unsafe/non-regular member; both re-verified at the end (`pin-verification.json`).
- Runs used output-local copies only. 227: copy without `proof-mutants-r3/` and
  `empty-event-mutants-r2/` (runners use `exist_ok=False`), exact `canonical.py` staged at the
  relative path the script resolves; `shape_join_model.py` now asserts the live file's hash itself.
  229: copy without `distribution-mutants-r1/`; `m2-trust-layout-reference-201` is a symlink to my
  previously verified reference-201 extraction (the model hash-asserts `canonical.py` d47f25db… and
  the kernel df45c9c5…; the kernel's sibling imports come from that verified tree). **No script
  was edited; there is no redirect diff.**
- 227: 59 proof cases, 17 variants, 69 capsule cases, 9 empty-event variants and the schema
  inventory all regenerate **byte-identical** to the frozen outputs.
- 229: 39 cases, 9 variants and `author-gaps.json` regenerate **byte-identical**. The six omissions
  root reproduced in MY author draft are real: my `admit_anchor` never compared `binding`, never
  joined the root envelope, validated `tcbProfiles` only as `[]`; and my "NFD alias" case normalised
  an ASCII string and tested nothing. Root's dispositions on those points are correct.

---

# Part 1 — 227 r8: corrections to my r7 findings

| r7 item | r8 state | evidence |
|---|---|---|
| F-1 typed edges contradict schemas | **closed in claimed scope** | `EDGES` is now derived from every NodeRef/EventRef/PublicationRef field reachable from the owned codec roots (168 field rows); my four r7 refusals now admit (adv227 P4); closure still references nothing, history still cannot reach time/closure/image (P5, P6); unknown field names hit an `assert` (fail-closed) |
| F-2 unexercised empty-event guards | **closed** | 9 variants (store, revision, previous, phase, L, anchor, serial, challenge, T) each die on the exact intended assertion; `bad()` now checks the label; the KeyError of a pure phase-guard deletion is disclosed as not a kill and replaced by an unsafe-early-success variant |
| F-3 no single-path rule | **closed for exact logical paths** | one global inventory over direct bodies, all slots, artifacts, repair, authorization body; 5 collision classes tested; duplicate root member refuses (P8). Case/normalisation aliases still admit (P7) — explicitly left to native alias admission in PROOF-NODE-JOINS, so not a finding |
| L-2 | closed | reachability sentence added (no L/T advance due; F write-ahead in an earlier revision; operation descriptor is the audit evidence) |
| L-3 / L-4 | closed | `empty-required-graph`; validator hash asserted |

Pending codecs (creation, transition intent, absence, restore, restriction, trust-admission input)
refuse `dependency-codec-unimplemented` both as targets and as a start node (P1); I treat these as
the stated boundary.

**227 observations (low, no blocker):**

- **O-1 the edge table is per KIND, the inventory is per FIELD.** `time → root/history` is now
  allowed for every time input because S4.5 needs it, so an `S4EvaluationInputV1` naming a root is
  type-legal although its schema has no such field. Cycles are still caught, and README says the
  inventory is "schema possibility extraction, NOT runtime value edge extractor"; the residue is
  only that the 168 precise rows are collapsed before use. When the runtime extractor exists it
  should check `(definition, pointer) → kind`, not `kind → kind`.
- **O-2 kinds are caller-supplied.** A pending object labelled `time` admits (P3). Inherent to the
  toy graph and disclosed ("Fixture IDs are deliberately not hash claims").
- **O-3 dead guard.** After the path inventory, a same-slot duplicate is refused
  `member-path-collision` before `signed-duplicate` can fire; the case was relabelled accordingly.
  Harmless; either delete the old guard or note it as defence in depth.

---

# Part 2 — 229 r1: core distribution, embedded bootstrap, anchor, payload frame

## Confirmed (by reading and by probe)

- The preimage/`rootDigest` recipe is NOT a second recipe: it equals the pinned kernel's
  `metadata_sha(domain, body)` on the pinned root1 and on a non-ASCII value (adv229 Q1a/b).
- Root documents go through the real `admit_root_document`; it RETURNS `REFUSE` (never raises) for
  bool/missing version, schema 3, extra member, non-object, empty object (`root-policy229.json`),
  so the model's mapping to `root-document-policy` is total.
- "EVERY platform tree" is real: a second platform with a different `root.json`, a different
  envelope length, or no bootstrap manifest refuses with the right label (Q3–Q5); two identical
  platforms admit (Q2).
- Tree law: symlink parent, file-under-file, symlink entrypoint, a REAL case-fold alias
  (`straße`/`strasse`), a compatibility-fold alias (`ﬁle`/`file`) and an NFD path all refuse
  (Q6a, Q6c, Q7a–d); a nested `inventory.json` leaf is ordinary (Q7f).
- A root body that is not `rootChain[0]` refuses (Q8). Envelope subject substitution refuses; a
  different signature set over the same subject changes nothing. Result is `bytes-bound-only`.
- All `$ref`s in the inlined TCB template resolve (Q9a). Three retained pairs / six blobs, each
  individually required (owner cases).
- Scope statements are honest: synthetic signatures, opaque unused catalog/list, no native
  custody/launch/quorum/profile-set matching, equivalence of inventory and core release manifest
  stated as a proposed owner decision.

## Findings

### G-1 (medium, cross-owner semantics) — "anchor = index 0" + 215's pre-acceptance authority selects the OLDEST embedded recovery authority

229 C.1 fixes the anchor as embedded `rootChain[0]` and makes later embedded roots ordinary in-order
edges. 215 r14 l.9 says "Before any accepted root, the authority root must be the embedded anchor of
the admitted immutable core closure" and l.24 "the replacement must exceed the embedded authority
anchor". With 229's definition, "embedded anchor" now names index 0 exactly. If a core ships an
embedded chain `[v1, v2, v3]` because v1's keys or recovery authority were rotated out, a
never-established installation would accept a `RootRecoveryAuthorizationV1` signed by **v1's**
`recoveryAuthority` — the very authority the rotation retired — and only needs a replacement
version above v1. Neither text is wrong alone; the composition is. **Action (one sentence in each
owner):** the pre-acceptance authority is the HEAD of the embedded chain after in-order
authentication from the index-0 anchor (and the replacement must exceed that head), or 229 requires
a single-root embedded chain. I did not find either statement in 229 r1. Not a model bug; the model
has no recovery path.

### G-2 (medium, test adequacy) — 15 refusal reasons have no case that depends on them

Guard-off survey (wrap `M.require` to ignore ONE reason, run the owner's 39 cases, no source edit;
`guard-survey229.json`). **SURVIVES** = all 39 cases still pass with the guard disabled:

`anchor-index-zero`, `anchor-tree-length`, `bootstrap-frame`, `bootstrap-kind`,
`bootstrap-member-tree`, `bootstrap-reference`, `bootstrap-tree`, `root-document-policy`,
`retained-bytes`, `retained-budget`, `tree-alias`, `tree-parent-type`, `logical-nfc`,
`payload-path-alias`, `layer-order`, `requires-order`.

(16 listed; `retained-budget` is a limit no small fixture reaches, so 15 are the meaningful ones.)
Five more (`anchor-envelope-membership`, `platform-unavailable`, `requires-node`,
`retained-unavailable`, `tree-order`) end in an unrelated exception when disabled — reported as
ERROR-not-a-kill, not as kills; each does have a positive label hit in the baseline.

These are the proposal's headline claims — index-zero anchor (root's own requirement), every-platform
bootstrap joins, the real 201 root policy, RJ-3 alias/NFC, retained-byte rehash — and deleting any of
them leaves the corpus green. My probes show the guards themselves WORK; the corpus just never
exercises them, and all fixtures are single-platform, single-root. The 9 owner mutants cover other
guards. **Action:** a two-platform and a two-root fixture plus one exact-label negative per reason
above, and extend the mutant list to them. Same pattern as 227 r7 F-2.

### G-3 (low) — symlink targets are grammar-checked only

DR-103 pathRule (quoted in OWNER B.2 as applying "incl. pathRule"): "Symlink targets must resolve
inside the tree." A symlink whose target is no tree entry admits (Q6b). Since identity ignores
symlink rows and bootstrap/entrypoint cannot sit behind one, impact is small, but the claim
"existing TreeCommitment shape incl. pathRule" is not fully implemented.

### G-4 (low) — `logical()` refuses `:` anywhere

DR-103 forbids drive letters; identity `LogicalPath` (the `Blob.path` grammar the projection must
satisfy) allows `:`. The model refuses any path containing `:` (Q7e), which is stricter than both
owners and would refuse a lawful tree. Either narrow to a drive-letter prefix or state the stricter
rule in OWNER as a proposal.

### G-5 (low) — TCB template: resolved, but never positively instantiated

Root's correction is real (`{'bad':'profile'}` refuses; the `actual-tcb-shape` mutant dies), and
every internal `$ref` resolves. But every positive fixture still has `tcbProfiles: []`, so no case
shows that a conforming non-empty entry is ADMITTED. A schema that refused every instance would pass
this corpus. One positive instance built from the template closes it. (Native qualification stays
out of scope, as stated.)

### G-6 (low, prose) — A.3's second half has no mechanism

"a non-core closure whose `manifestDigest` names an inventory, refuses" cannot be decided from a
digest. The enforceable form is by route: a non-core closure is admitted only with an envelope of
kind `manifest` whose `storedSha256` equals `manifestDigest`; a core only with kind `inventory`.
This sentence came from my draft; it should be rewritten, not kept.

### G-7 (editorial) — author first person inside a root-owned OWNER.md

D.4 ("Correction to my anchor227 report. I wrote …") and C.5 ("my anchor227 retention correction")
are my words in a document now headed ROOT-CORRECTED. Harmless technically, confusing for
attribution when this text is cited later.

## Boundaries I did NOT treat as findings

Synthetic signatures; unused catalog/list; no envelope-index producer or ambiguity policy; payload2
and the nine-kind envelope successor not integrated; no install/launch/first-channel evidence; no
profile-set match; primary schema/reference/runtime selection. All are stated by README/OWNER.

## Limitations

Probes call the owners' unmodified functions with the owners' fixture builders re-parameterised;
"ADMITS" is the toy model's verdict. The 229 guard survey disables a reason label, not a source
line — two guards sharing one label are disabled together (`logical-path`, `metadata-cap`,
`protocol-membership-order` each cover several conditions, so a "killed" there does not prove every
sub-condition is tested). G-1 is a reading of 215 r14 l.9/l.24 against 229 C.1; I did not re-review
215. I did not re-run 227's 67 event / 35 time checks. No harness failure occurred in this task
other than the ERROR-not-a-kill rows above, which are preserved in the outputs.

## Pins

227 r8: `check_proof_joins.py` 7fb2dd0e10ebf6b85a659248f8993632ec0fead7af106bcbeaf23123ce17f359 ·
`schema_dependency_inventory.py` 079d84e6fc35627d55316ea1e89e1f853dc7d315699a51d877eaadff08cf3236 ·
`shape_join_model.py` 781061b62f37954b071765104b934702d1a59d88437e42962f7c8f8b6d7bcdf2 ·
`PROOF-NODE-JOINS.md` fd687e4e08e88e053385a35c5d234fda6107e9b87285f6e214adf5efc4e83e10
229 r1: `distribution_model.py` 13e4d10aa4654f7e5460d64e5d74aa2aa17e4b5feb347aa02e1f74a3b192413c ·
`check_distribution.py` d04fa3a5efc6f9f1d17384fd752f45a4cf8a1e12ca1a1bacdb2c542c3c9449bd ·
`core-distribution.v1.json` 57de5b0c6169a4ea66030d88c9f6291f5d26b4556d8cfc27b1181b30bf30039d ·
`OWNER.md` 948bf9a2173d061f55e27812e1f0c3586f747528a57573b0d36dfae1b9b6ad1e ·
`ROOT-DISPOSITION.md` 349f86bd3c0e0ea1321a6f3dc9b1de7985a1d0149851111858651431b7d6945a
Reference: `canonical.py` d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442 ·
kernel df45c9c5444790b5f89b458efbee5cb068781d5fc1e82483c2678d2f10712299 · 215 r14 `OWNER.md`
d8165f14a161d4fd7453afd0bc4af5a9c2f2a0f73be5eee35976b99cc9ef19fa
