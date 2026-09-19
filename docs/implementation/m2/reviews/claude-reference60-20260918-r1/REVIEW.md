# Independent review: security reference correction 60 (root-policy) — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope: bounded review of unaccepted reference60 only. Not a review of later drafts, signature59,
real signatures, current trust, native custody or release qualification. Not formal selection.

## Verdict (bounded)

**CHANGES REQUIRED before formal selection.**

Split plainly, because the two halves have different standing:

- **The root-admission gate logic itself — no blocking finding.** `_preserved_root_policy` /
  `admit_root_document` and the inherited clock / calendar / ROOT-revocation corrections preserve the
  retained v8 semantics, refusal precedence, D9 branch, namespace / chain-origin / standing / threshold rules
  and cross-role key disjointness under every independent probe I ran (details below).
- **The candidate tree as a selectable subject — blocked by B1** (a concrete, reproduced cross-unit
  regression that the README does not disclose: the candidate makes `check-integration.py` abort where the
  archived parent passes 412/0), and by B2 (disclosed stale cross-unit pins). M1/M2 must be reconciled in the
  same correction or explicitly carried as named, owned items; L-items are nonblocking.

This verdict is not authority for any unreviewed downstream implementation.

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `docs/implementation/m2/trials/root-admission-reference-60/subject.tar.xz` (3,626,916 B) | `e8b4d2c2d9bfcdfdfaa5458a1fbf723eec7e032fdafc3a2788d3807a3a46e6cd` | matches `archive-pin.json` |
| `…/subject.json` (manifest, 2,552 entries) | `e3a5b45c2fedae60494edcc8e05c96c2bcd58d2f0d344221a477b168557e5d68` | byte-identical to review copy |
| `…/archive-pin.json` | `266108af22f49ff16d5729a211021b18a695504cf468f4563587db8d59b50334` | byte-identical to review copy |
| `…/README.md` | `301d866c043d0557446466666b4cea98dd308f25c399a439ec190fb1924d7f4e` | matches manifest |

`claude-out/verify_pins.py`: every one of the 2,552 manifest members was re-hashed from the tar **and**
byte-compared to the extracted `subject/`; 0 missing, 0 mismatched, 0 extra tar members, 0 extra extracted
files, no non-regular members. Re-run after all probes: still `bad 0` (subject bytes untouched; no
`__pycache__` written — probes ran with bytecode writing disabled).

Changed owners (candidate vs selected45; selected45 hashes confirmed equal to `selected45-before/` and, for
four of five, to the live repo):

| Path | selected45 | archived parent (58/56/53) | candidate60 |
|---|---|---|---|
| `security/security_lifecycle_model_v1.py` | `d0ef9814…d18bb9` | `2ed7729c…310b50` | `f71aceff…5e2d8` |
| `product-v1/security-and-lifecycle.md` | `a319da39…bad9d6` | `e46982ba…bc8bb` | `99df85e0…dd98` |
| `security/root-schema-cases.v1.json` | `7eb66f5d…2641ad` | same | `3898904d…dde6` |
| `public-detail-registry.v1.json` | `2702e6ca…70e68` | same | `5945378a…48e8` |
| `security/source-pins.v1.json` | `de2e53d2…d29e66` | same | `1943d91c…cce3d` |

Notes: (1) the archived parent is **not** selected45 (I found this from hashes before the owner's
clarification; the inherited model/contract diffs were reviewed against `selected45-before/`). (2) The
source-pin rebinding is exactly four hash lines plus `status`/`purpose` text — no other pin byte changed.
(3) The live repo's `security/source-pins.v1.json` is `f7c3e11a…`, i.e. live ≠ selected45 for that one file;
not caused by this subject, recorded only so nobody assumes live == selected45. (4) `git status` shows
`docs/implementation/ACTIVE-WORK.md` modified during my session; I did not touch it.

## Findings

### B1 (blocking, reproduced) — generated `DomainDetail` enum not regenerated; candidate breaks `check-integration.py`

- Evidence: `workflows/schemas/common.schema.json` (`b7b25d5e…`) and
  `workflows/schemas/evaluator3/common.schema.json` (`ce45b9ff…`) carry the closed `DomainDetail.code` enum
  "Generated/drift-checked from public-detail-registry.v1.json". Neither contains
  `ROOT.RETAINED_SEMANTIC_POLICY`; the registry now does.
- Reproduction: `check-integration.py --report claude-out/integration/report.json` on the **candidate** tree
  exits 1 with an uncaught `integration_workflow.Refusal: CONFIG.INVALID` raised from
  `check-integration.py:413` (`validate_import_record(... '#/$defs/DomainDetail', example)`,
  "exact enum type/value mismatch"); **no report is written**. The same command on the archived **parent**
  tree: `passed: 412, failed: []`.
- Consequence beyond the checker: the new public refusal is unrepresentable in a workflow result — a consumer
  that receives it refuses `CONFIG.INVALID / IMPORT.ARTIFACT_CORRUPT`, i.e. a root-policy refusal would
  surface as artifact corruption. That contradicts the closed-registry law the unit itself sweeps.
- Why the reported evidence missed it: the 470-case security checker's sweep
  `public-domain-details-are-a-closed-fully-registered-set` joins model ↔ registry only; nothing in the
  security unit joins registry ↔ generated workflow enum. README says cross-unit reconciliation "remains" but
  reports only passes; this is a regression relative to the parent, not merely pending work.
- Required: regenerate both enums from the registry by their owning generator (not by hand), re-pin, and
  retain a passing integration report for the candidate.

### B2 (blocking for selection, disclosed; not executed by me) — three other pin owners still bind the old bytes

`native/source-pins.v2.json`, `foundation/source-pins.v1.json` and
`foundation/evaluator3-source-pins.v1.json` each still pin all four pre-60 hashes (`2702e6ca…`, `7eb66f5d…`,
`d0ef9814…`, `a319da39…`). By the same stale-pin law the security checker correctly enforced, those units
must refuse the candidate tree. I verified the pin bytes; I did not run those units' checkers. B1's
regenerated schemas will add further rebinding. Required: exact, whitelisted rebinding per owner with
retained before-images, as was done for the security unit.

### M1 (medium) — retained regressions do not pin the schema-2 branch or any inherited correction

- All six new `retained-root-policy-*` cases are `rootSchema: 1`. No retained case expects
  `ROOT.RETAINED_SEMANTIC_POLICY` on a schema-2 root. The twelve schema-2 standing controls exist only inside
  the one-shot `scripts/check_root_reference60.py` (hard-coded paths, `assert not O.exists()`), so after
  selection nothing re-executes them. Deleting the whole `if root['rootSchema'] == 2:` tail of
  `_preserved_root_policy` would survive the retained 470-case checker.
- Inherited malformed-continuity fix: the only fixture (`monotonic-went-backwards-in-same-boot-is-a-finding`)
  asserts neither `anchorWrite` nor `writes`. `claude-out/anchor-results.json`: selected45 writes a fresh
  anchor (`writes: [evalHighWater, anchor]`), candidate writes none — **both satisfy the fixture**. The
  correction is mutation-survivable.
- Inherited timestamp fix: no case file contains an invalid calendar date or a non-ASCII digit
  (scanned every `*-cases.v1.json`). `claude-out/inherited-results.json`: under selected45,
  `ts('٢٠٢٦-01-01T00:00:00Z')` (Arabic-Indic digits) **returns 1767225600**, and Feb 31 / year 0000 /
  second 60 escape as untyped `ValueError`; the candidate rejects all typed. A real gap was closed and is
  unpinned.
- Required: retain schema-2 standing/absence negatives (both roles), a schema-2 retained-rule negative
  (e.g. duplicate public key on a TR-PROFILE key), a malformed-continuity case asserting
  `anchorWrite: null` with floor still advancing, and timestamp negatives (invalid date, non-ASCII digit) at
  `ts()`-consuming boundaries.

### M2 (medium) — the "sole root boundary" is not composed on two admission paths, and unmigrated fixtures depend on that

- `claude-out/chain-results.json`: a version-2 root with a duplicate public key, unbound keyId, TR-CORE
  threshold 1 and TR-INDEX without standing is refused by `admit_root_document`
  (`ROOT.RETAINED_SEMANTIC_POLICY:…`) yet `verify_root_chain` returns **ACCEPT, acceptedVersion 2**
  (it calls only the reduced `_admit_root_semantic`, model l.1301). `admit_profile_set_envelope` likewise
  returns **ACCEPT** over the same defective `acceptedRoot`.
- `admit_root_chain` (l.3284) is the correct composition and the contract (S9.1) names it, but
  `run_case('root-chain')` routes to the primitive, and the only test of the composition lives in
  `check-integration.py:147-149` — which currently produces no report (B1). There is **no** composed
  counterpart for profile-set admission: nothing requires its `acceptedRoot` to have passed the document
  boundary, and the v8 idea of an immutable `AdmittedRoot` carrier re-checked at use (SEC3-M1) has no
  successor analogue.
- Fixture dependence: all 8 roots in `root-chain-cases.v1.json` are `ROOT.SHAPE` at the document boundary;
  `public-detail-cases.v1.json` `root1`/`root2` were **not** migrated (16–19× `KEY_ID_MISMATCH`, every core
  role without standing/threshold, TR-BUNDLE without namespace) and are used as `acceptedRoot`. The new
  contract sentence "Synthetic role fixtures must satisfy these rules to claim document admission" is
  therefore only true of `root-schema-cases.v1.json`.
- Standing: README's last sentence discloses that full root-chain authority is not supplied, so this does
  not falsify the reference's claim; but the new contract sentence "The projected chain/signers assumptions
  never waive this document boundary" is currently asserted, not enforced or tested, for profile-set.
  Required before selection: either enforce (an admitted-root carrier or a composed
  `admit_profile_set` boundary + routed cases) or narrow the contract sentence and name the owner.

### L1 (low) — circular oracle in the 2,386-row comparison; mitigated by my independent oracle

`check_root_reference60.py` sets `V=N._RV8` — the very module object the candidate calls — so
`want = old ACCEPT and not V.admit_root(root)` proves wiring, not rule correctness, and cannot exercise the
schema-2 projection (v8 refuses any schema-2 role set). Mitigation performed: `claude-out/probe_root60.py`
restates v8 §3.1 + S9.1 without importing the v8 library; 40,000 seeded structural mutations of root1/root2:
0 oracle disagreements in either direction (2,975 accepts, 1,456 newly refused).

### L2 (low, architecture) — one rule now has three statements

Extension-role threshold policy is stated at model l.3075 (early gate, emits
`ROOT.TR_*_THRESHOLD_POLICY`), again at l.3002 (unreachable for that input class — the early gate always
returns first; confirmed by probes `s2-ext-threshold1-*`), and a third reduced copy in
`_admit_root_semantic` l.1328-1336 with *different* codes (`ROOT.TR_REPAIR_STANDING`) and no TR-PROFILE rule.
Dead duplicate branches drift silently. Prefer a single owner for the extension-role rule that the early
gate, the retained policy and the chain path all call.

### L3 (low) — detail string shape vs contract and sweep invariant (c)

Contract says `ROOT.RETAINED_SEMANTIC_POLICY:<retained reasons>`; emitted is
`…:ruleFailures=<r1;r2;…>`. The subject embeds strings that are themselves registered public codes
(`ROOT.ROLE_THRESHOLD_POLICY`, `ROOT.CHAIN_ORIGIN_INCONSISTENT`, `ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY`,
`ROOT.TR_REPAIR_MUST_BE_TYPED_ABSENCE`). Sweep invariant (c) tests only `subject.partition(':')[0]`, so the
literal `ruleFailures=` prefix is what keeps it green — a syntactic, not semantic, separation. The subject is
also unbounded by the gate (up to 64 `KEY_ID_MISMATCH:<8 hex>` entries ≈ 1.8 KB). I did not verify a
`DomainDetail.subject` length bound (unresolved). Suggest: align contract text with the emitted grammar,
bound/truncate the list deterministically, and make (c) scan the whole subject.

### L4 (low, defence in depth) — retained rules run outside an exception boundary; import-time coupling

v8's own boundary wrapped `admit_root` in `try/except → refusal` ("exceptions inside the boundary are
refusals"); the successor calls `_RV8.admit_root` bare. Post-schema this is unreachable today
(`publicKey` is `Hex64`, so `bytes.fromhex` cannot raise; 0 exceptions in 40k mutations + 106 cases), but the
safety now depends on schema/gate ordering staying put. Separately, importing the model now executes the
entire v8 unit library (incl. its `openssl` subprocess helper) by path; it is pinned in
`source-pins.v1.json` (l.4256) but the hash is checked by the checker, not at import.

### L5 (assumption to confirm) — malformed same-boot continuity is now sticky until reboot

With the anchor preserved, every later evaluation in that boot with `mono < anchor.mono` stays
`CLOCK-CONTINUITY-MALFORMED` (non-refusing), so the in-session 24 h excursion check is unavailable for the
rest of the boot; forward excursions remain bounded by the 90 d horizon. selected45's behaviour (re-baseline
once) was the worse laundering primitive, and the contract text now states the new behaviour deliberately, so
I treat this as intended — but it is a design choice the owner should confirm, not something a test proved.

### Observations (not regressions; identical in v8)

An unreferenced entry in `keys` is admitted; cross-role namespace overlap (e.g. TR-INDEX claiming TR-CORE's
namespace) is admitted — v8 §3.1 requires only "at least one namespace". Ed25519 point validity of
`publicKey` is not checked. All three are outside this reference's claim; listed so they are not mistaken
for covered.

## What I checked and found sound

- **Rule preservation:** v8 §3.1 (`security-completion.v8.md` l.160-163, `security_unit_lib_v8.py`
  `admit_root` l.217-266) vs the successor gate. Rules shadowed by earlier successor checks keep the earlier,
  already-registered detail; the newly reachable retained rules are exactly: public-key uniqueness, keyId
  binding, chain origin, core-role standing / threshold≥2 / keys≥t+1 / namespace, and exact schema-1
  TR-REPAIR typed absence (incl. missing `standing` and non-empty `namespaces`, both admitted by selected45).
- **Schema-2 projection does not weaken disjointness:** the projection blanks TR-REPAIR/TR-PROFILE/kernel
  keys only for the v8 call; `keys` stays whole, so duplicate-public-key and keyId binding still cover
  extension and kernel keys (probes `s2-ext-pubkey-duplicates-root-pubkey-*`, `s2-kernel-key-keyid-unbound`,
  `s2-kernel-key-duplicate-pubkey`), and the successor `seen` loop refuses every cross-list reuse I tried
  (ext↔core, ext↔recovery, ext↔root, profile↔repair, kernel↔profile/core/root). Input is not mutated.
- **Refusal precedence / monotonicity:** over 40,000 mutations, whenever the parent refuses the candidate
  returns the **identical** outcome object (0 violations); every new refusal is
  `PAYLOAD-NOT-ADMISSIBLE` + `ROOT.RETAINED_SEMANTIC_POLICY:ruleFailures=` with the unchanged D9 parent.
  Reader-set typing (`ROOT.SCHEMA_UNSUPPORTED` for schema 2 under `{1}`) unchanged.
- **ROOT revocation:** matches the retained owner — v8 §2.1 domain table ("revocation list | yes, ROOT") and
  `security_unit_lib_v8.py` l.40; selected45's "TR-INDEX" was the drift.
- **Timestamp grammar:** ASCII-only `TS_RE` + typed `Reject` on calendar failure is correct and consistent
  with the schema `Timestamp` pattern; root gate maps it to `ROOT.TIMESTAMP_GRAMMAR` / `ROOT.SCHEMA_SHAPE`.
- **Reported results reproduce:** full security checker on the candidate, fresh output dir: 470/470, 11/11
  sweeps, `sourcePinsValid` true (`claude-out/regression/`).

## Commands and outcomes (all output under `claude-out/`; interpreter `native-case15-reference-env` unless noted)

| Command | Outcome |
|---|---|
| `verify_pins.py` (metadata env; run 3×, incl. after all probes) | 2,552/2,552 tar + extracted match; 0 extra |
| `probe_root60.py` | 106 targeted cases, 0 failures; fuzz n=40,000: 0 exceptions, 0 monotone violations, 0 oracle disagreements |
| `probe_inherited.py` | selected45: 3 untyped `ValueError`, non-ASCII digits accepted; candidate: all typed rejects; revocation authority ROOT |
| `probe_anchor.py` | selected45 rewrites anchor on malformed continuity; candidate does not; fixture cannot tell them apart |
| `probe_chain.py` | chain + profile-set ACCEPT over document-refused root; 8/8 chain-fixture roots and public-detail `root1`/`root2` not document-admissible |
| `check-security-lifecycle.v1.py --report claude-out/regression/report.json` (candidate) | exit 0, 470 pass, 11 sweeps |
| `check-integration.py --report …` (candidate) | **exit 1, uncaught Refusal at l.413, no report** |
| `check-integration.py --report …` (parent) | exit 0, 412 passed, 0 failed |

Not run: one-shot preparers; native / foundation / evaluator3 / workflows unit checkers (B2 inferred from pin
bytes); any signature verification.

## Unresolved assumptions

1. `selected45-before/` is authentic selected45: I confirmed its five files against the hashes in
   `selected45-security-comparison.json` and four against the live repo, but did not independently obtain
   manifest45 (`8b4efbb0…`) or verify the "34 owners" count. The two preserved failed comparisons mean no
   complete selected45 ↔ candidate tree comparison exists; outside the five changed files I relied on
   candidate == archived parent (`diff -rq`, verified) and parent pins == selected45 pins (verified for the
   security pin file only).
2. Whether the v8 rule set is itself the *intended complete* policy (orphan keys, namespace overlap) is an
   owner decision; I judged preservation, not sufficiency.
3. `DomainDetail.subject` length limits and downstream rendering of the `ruleFailures=` list (L3).
4. L5 intent.
5. Signer sets remain asserted TCB; additional schema-2 role keys are synthetic. Nothing here is evidence of
   cryptographic admission.
