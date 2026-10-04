CODEX2 review: two design units, **ENUM-1** and **SD-8**. Claude Opus 5.5 leads, and you are the single reviewer. Two verdicts are wanted, in two files, one per unit:
- **ENUM-1**, the enumeration contract successor that M3-C r8's cross-law finding X-8 owes: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**;
- **SD-8**, a passage supersession of SD-7's NE:3540 override that conforms NE's excluded-form row to RTC §7.4: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**. If you accept, its `review.json` must carry `supersededPassages` (below).

Write only under `/tmp/opensip-implementation/reviews/codex2-enum-1-sd-8-r1/`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- **No cargo.** Don't run any build, test or lead set: timing-sensitive lanes may be using this machine.
- You may re-run `evidence/verify_scratch.py` (this directory) only in your own throwaway detached worktree of product main `1799d3d`, with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, as the lead did. It is Python only. Never run it in the main product checkout: it rewrites the worktree's `design-lock.json`. Remove the worktree afterwards.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## The subjects

Paths are under `/Users/sb/code/opensip-ai/opensip_arch/`. Every pin is in `hashes.txt`. This request pins accepted snapshots only, apart from the two subjects. Both units' files are untracked until acceptance: read the working-tree bytes and check them against the pins.

| Subject | Path (`subjectManifestSha256`) | sha256 | Bytes |
|---|---|---|---|
| **ENUM-1** | `docs/implementation/m3/snapshot-plan-c/enum-1-subject.json` | `d6005ac5…` | 1,034 |
| **SD-8** | `docs/implementation/m3/supervisor-d/sd-8-subject.json` | `ea65c63a…` | 1,001 |

Each unit's members are its README, `PASSAGES.md`, `successor.json` and two evidence scripts (build and check). The lead's assent drafts, `enum-1-unit.json` and `sd-8-unit.json`, are not members. Read each README first; `PASSAGES.md` shows every `before` and `after` with word-level changes.

**Product:** main `1799d3d` (CRC-2's binding). Its lock has 99 contract successors and 4 contract passage supersessions.

## Background

- **X-8** (MC8:1266-1270; M3-C r8, `snapshot-plan-c/PROPOSAL-r8.md`, `578c186e…`, accepted in review by you). A required cell whose closure is not admitted has no lawful binding. ENC:53 refuses an unselected enumerator on a required cell, default discovery makes every cell required (NE:950-955), and no admitted closure can stand in. So E-3 (MJ5:464; MC8 item 7) and the durable golden "required provider closure not installed" (WS:1374; MJ5 row 27) have no Plan the contract admits. Your C r8 review confirmed the gap (its item 7).
- **The lead's decision for ENUM-1 (2026-10-04).** An enumeration contract successor admits the unselected enumerator in exactly that case, with the `provider-unavailable` pair. Nothing else changes. Rejected: dropping the cell; refusing the request; a synthetic enumerator (the producer principle at MC7:458); widening "required". ENUM-1's LD-1 records it.
- **The lead's ruling for SD-8 (2026-10-04).** RTC §7.4 governs, so an ephemeral attempt carries no detail (`reviews/grok-j2a-r1/REQUEST.md`, "Lead rulings", item 3). NE:3540, as SD-7 supersedes SD-5's override there, still gives the ephemeral no-trust form `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. SD-8, a VD2 supersession of SD-7's override, keeps every word except the ephemeral form's detail. J1 r6, accepted by Codex (`host-pipeline-j/PROPOSAL-r6.md`, `086e804a…`), records the conflict and the ruling (MJ6:822, :971-972). Rejected: reading the sentence as fixing only the class and code.

## ENUM-1

Eleven **plain overrides**, no supersession. No target key carries a bound override at `1799d3d`, so there was nothing to supersede.

| # | Parent | Selector |
|---|---|---|
| 1 | `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` (ENC, `b7858bc8…`) | line 53, the rule and its one exception |
| 2 | ENC | line 75, the restatement |
| 3 | ENC | line 145, the class table |
| 4 | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/enumeration-plan.schema.v1.json` (SYN-1F's copy, the selected schema, `cc29483f…`) | `/$defs/SelectedEnumeratorRef/description` |
| 5 | the same | `/$defs/UnselectedEnumeratorRef/description` |
| 6 | the same | `/$defs/EnumeratorRef/description` |
| 7 | `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` (EXC, `22ee2507…`) | line 103, the candidate-required refusal |
| 8 | EXC | line 110, its restatement of the enumeration owner's refusal |
| 9 | EXC | line 131, the meaning of an unselected binding |
| 10 | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/execution-inputs.schema.v1.json` (SYN-1F's copy, `0c196cba…`) | `/x-opensip-derived-carrier-law/candidateCarrier` |
| 11 | `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` (COMP, `30d4d9d2…`) | line 235, the proof bridge's restatement |

**The case** (ENC:53's new text): a required cell's binding may carry the existing `{status:"unselected", reason:"optional-unselected"}` only when no admitted closure can lawfully be its selected enumerator, because a closure the cell's mode needs is not admitted for the request. The pair is exactly `provider-unavailable` with `nativeCause` null. The cell stays required and holds the Run at `indeterminate`. An `inventory` cell never meets the case. The host establishes the case when it builds the Plan, and admission checks the shape (LD-4).

**A site X-8 does not name (LD-5).** Entries 7, 10 and 11 exist because the case would still refuse downstream. A required `clones-near` or `clones-cross-tsjs` cell in the case has no producer, so no envelope, and EXC:101-103, EXS's `candidateCarrier` and COMP:235 refuse such a cell as `EXECUTION_INPUTS_CANDIDATE_REQUIRED`. Default discovery requests `clones-near` with `required=true` in all six modes (NE:1081-1087; NCM marks every `clones-near` cell `SUPPORTED-DESIGN`), so every default Plan in the case would refuse at execution-input admission. The entries exempt only the case. The lead may split entries 7 to 11 into a separate execution-inputs successor; they are separable.

**Owed code, unchanged here.** The reference models and the product still refuse the case: `enumeration_model.v1.py:759-760` (the selected copy), `crates/evaluator/src/enumeration_join.rs:560-566`, `execution_inputs_model.v1.py:1198-1199` and `crates/evaluator/src/execution_inputs.rs:1170-1175`. The README assigns them to C4a and J2c, with reference successors.

**Its review lists `"supersededPassages": []`.** VD accepts the empty list for a record with no supersession (`:420-426` at `1799d3d`).

## SD-8

One **passage supersession** of SD-7's NE:3540 override (`docs/v2/contracts/product-v1/native-evidence.md`, `83b99783…`). Its `before` is SD-7's `after`: the raw release-declaration row, then the excluded-form row. The first row is unchanged. In the second, one sentence changes:
- **Before:** "… keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`."
- **After:** "… keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, with `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` on a durable request. On an ephemeral request, the no-trust form included, it is `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`, with no runId and no detail, because the run-termination contract's §7.4 admits no detail on an ephemeral attempt (contract successor SD-8)."

**One drafting choice to judge (LD-S8-2).** The ephemeral clause covers every ephemeral request, not only the no-trust form. The sentence's subject includes a closure that is not installed on any request, and §7.4 admits no detail on any ephemeral attempt. Dropping the detail for the no-trust form alone would leave the with-trust ephemeral form contradicting §7.4.

### SD-8's review must carry `supersededPassages`

VD refuses a contract passage supersession that its review does not list (`:420-426` at `1799d3d`). So if you accept SD-8, `sd-8/review.json` must contain `supersededPassages`, equal by value and in order to the record's `supersedes` list. The exact value:

```json
[{"record": {"path": "docs/implementation/m3/supervisor-d/sd-7/successor.json", "bytes": 14706, "sha256": "350a249afaa001fc97292c2837395d930cc7bdc0d6b62b594b04df55d9767c04"}, "parent": {"path": "docs/v2/contracts/product-v1/native-evidence.md", "bytes": 329013, "sha256": "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"}, "selector": {"line": 3540}}]
```

## The lead's local binding check

The output is pinned: `evidence/local-binding-check.json`.
- **Where.** A throwaway detached worktree of product main `1799d3d` (`/Users/sb/code/opensip-ai/opensip-enum1-check`, since removed), with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, also removed. Python only, with no cargo.
- **How.** The worktree's own `tools/verify_design.py` (43,946 bytes, `7b313de6…`, byte-equal to `1799d3d`'s) was loaded unchanged. Each unit's entry was appended to the worktree's `design-lock.json` with SCRATCH review and assent pins, served from memory by an overlay of `pinned_bytes`, as CRC-2's and SD-7's checks did. ENUM-1's scratch review lists `[]`, and SD-8's lists the value above.
- **Results:**

  | Configuration | With the worktree as implementation | Without | Contract successors | Contract passage supersessions |
  |---|---|---|---|---|
  | baseline (literal CLI and overlay) | PASS | PASS | 99 | 4 |
  | ENUM-1 alone | PASS | PASS | 100 | 4 |
  | SD-8 alone | PASS | PASS | 100 | 5 |
  | ENUM-1, then SD-8 | PASS | PASS | 101 | 5 |
  | SD-8, then ENUM-1 | PASS | PASS | 101 | 5 |

  In every configuration, the inventory chain, inheritance and supersessions, generation and admission sources, and verified inputs equal the baseline's.
- **Probes**, each on main's lock plus the named entries:

  | Probe | Result |
  |---|---|
  | ENUM-1 whose review lists SD-8's superseded passage | "contract review superseded passages differ from the record" |
  | after ENUM-1, a second plain override of ENC:53 | "conflicting contract passage overrides" |
  | ENUM-1 with ENC:53's `before` altered | "passage override before text differs from accepted parent" |
  | ENC:53 posed as a supersession naming SD-7's record | "superseded passage is not in the named record" |
  | after ENUM-1, a VD2 supersession of ENUM-1's ENC:53 | PASS (the passage stays editable) |
  | SD-8 whose review omits `supersededPassages` | "contract passage supersession is not listed by its review" |
  | SD-8 whose review lists `[]` | "contract review superseded passages differ from the record" |
  | SD-8 as a raw override of NE:3540 | "conflicting contract passage overrides" |
  | SD-8 superseding SD-5's override instead | "double supersession: the named passage is not the current meaning" |
  | after SD-8, a second supersession of SD-7's NE:3540 | "double supersession: the named passage is not the current meaning" |
  | after SD-8, a VD2 supersession of SD-8's NE:3540 | PASS (the chain stays linear) |

- **The literal CLI on the lock with both units appended** stops at "missing or escaping regular file: SCRATCH-ENUM-1/review.json". It fails closed, as for earlier units' SCRATCH pins. The overlay run is the binding result.
- `build_enum_1.py --check` and `build_sd8.py --check` report identical bytes, and `check_enum_1.py` and `check_sd8.py` pass, at `1799d3d`.

## Lead confirmations (Claude Opus 5.5, before sending)

- **ENUM-1 LD-5 is confirmed: the execution-inputs fix stays folded into ENUM-1.** Default discovery requests `clones-near` as required in all six modes. In the admitted case it has no producer, so without entries 7 to 11 every default Plan would refuse at `EXECUTION_INPUTS_CANDIDATE_REQUIRED`. It is one case with one cause, so it is one successor. **Rejected:** a separate execution-inputs successor, which would leave ENUM-1 unusable on its own.
- **SD-8 LD-S8-2 is confirmed:** no ephemeral request carries the detail, whether or not it has a trust view, because §7.4 admits no detail on any ephemeral attempt. **Rejected:** narrowing it to the no-trust form, which would leave the sentence contradicting §7.4 for an ephemeral request that has a trust view.
- **The drafter's three ENUM-1 decisions are confirmed as lead decisions:**
  - a null `nativeCause`, because `capability-missing` means no admitted closure bears the capability, which is not this case;
  - reusing the `optional-unselected` token rather than changing the schema's shape;
  - the host establishing the case at Plan build, with admission checking shape only.

  A disagreement with any of these is a finding.

## Decide

**For ENUM-1:**
1. **Faithfulness.** Is ENUM-1 exactly X-8's case and the lead's decision (LD-1), neither wider nor narrower? Are the rejected alternatives right?
2. **The case.** Is ENC:53's statement precise, including `syntax-only`'s grammar closure, the `inventory` exclusion and "A required unselected binding with any other pair still refuses"? Is the pair right (LD-2: `provider-unavailable` with `nativeCause` null, not `capability-missing`)? Is reusing the `optional-unselected` token (LD-3) acceptable? Is a host-established, shape-checked case (LD-4) acceptable?
3. **Downstream (LD-5).** Is the candidate-required site real, and are entries 7 to 11 within the one case? Does every other refusal stay, in particular `EXECUTION_INPUTS_CANDIDATE_REQUIRED` under a selected enumerator?
4. **Nothing else.** Does every sentence outside each rewritten fragment survive, and does each schema copy change only at its pointers? Are SYN-1F's copies the right schema targets, and are the product copies rightly left alone (CRC-1 LD-7)?
5. **Consumers.** Do the README's controls for C4a's Plan leg and J2c's ephemeral leg (C2-T18, E-3) follow, and is the owed code named correctly?
6. **Binding.** Does the record bind after main's chain, alone and with SD-8? Does any selected passage conflict?

**For SD-8:**
1. **Faithfulness.** Does SD-8 keep every word of SD-7's row and change only the ephemeral form's detail, as the ruling and RTC §7.4 require?
2. **Scope (LD-S8-2).** Is covering every ephemeral request right?
3. **Form and binding.** Is the supersession well formed under VD2 (`contract_successor` at `:186-276`, `successor_chain` at `:278-495`, the supersession checks at `:348-369` and `:415-426`), and does it bind, alone and with ENUM-1?

**For both:** anything else wrong.

## Output

Under `/tmp/opensip-implementation/reviews/codex2-enum-1-sd-8-r1/`. Do not commit, and run no cargo.
- **ENUM-1:** `enum-1/REVIEW.md` and `enum-1/review.json`, with:
  - `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
  - `"requiredFindings"`: a list, empty if you accept; each finding with an id, a location, the problem, the evidence and the fix;
  - `"nonBlockingObservations"`;
  - `"subjectManifestSha256"`: `d6005ac5a7a254c984010e581f4604af5d314a3550cb35c57baf59802e072f0b`, as one string;
  - `"supersededPassages"`: `[]`.
- **SD-8:** `sd-8/REVIEW.md` and `sd-8/review.json`, separate, with:
  - `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
  - `"requiredFindings"` and `"nonBlockingObservations"`, as above;
  - `"subjectManifestSha256"`: `ea65c63a0d30b060ee1ef0a8499f5a9edada1a0edb129cad22690023f7d9e1ed`, as one string;
  - `"supersededPassages"`: the list above, exactly, if you accept.

The two units are independent. An acceptance of one does not depend on the other.
