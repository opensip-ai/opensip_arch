# ERRATUM E-3 r2 to SEC-PREDRAW-1 r7 (§1.8, §5.2): where C-NC-20 and C-NC-21 can run, and the measured reach

**Author:** claude-sec-predraw-1 (w35:p1), Claude Opus 5.5 / high, R3-FRONTIER, long-horizon lead.

**Authority:** LD-Q-240 (`coordinator/msg-ldq240.txt`, `8d43aaa9…`), option A, and LD-Q-242 (`coordinator/msg-ldq242.txt`, `76498ceb…`), on REVIEW-E3's alternative. **Scope: the execution form of two controls, and
a stated limit. Text only.**

E-3 is a standalone erratum to the adopted record `SUCCESSOR-SEC-PREDRAW-1-r7.md` (`f8bbd0fb…`), read with E-1 and E-2. **The
bytes of r7, FB-1 r4, E-1 and E-2 are not edited.** If E-3 is adopted, it controls on the two control forms named below.

**Pins:**
- product `fe379d218358d3193073db3f037b062713a258f2`;
- the SP branch `claude/sec-predraw-1-sp4` at `778fbf5d6810c61d82b1136e6921b33f266f136a`, holding both controls;
- architecture `5f328f32`.

## 1. The defect

r7:529 runs C-NC-21 "on both the durable path and the read `Some` path", and r7:1066-1068 define C-NC-21 and C-NC-20 over signed
catalogs of 21 and 20 components. **On the durable path, neither can run as written:** on the measured fixture, a signed catalog of 20 or 21
components is stopped before P-1, because the attempt ledger's edge limit (`EDGE_LIMIT = 131_072`, `work_ledger.rs:13`) is exhausted first.
At 18 and 19, P-1 runs and returns, and the wrapper's receipt recheck then refuses. The basis is the trace in §2.

The read `Some` path runs exactly as written.

## 2. The measured reach

Real signed chains on the fixture, with first-use registration and a scripted guard seam:

| Components | Read `Some`: P-1 | `durable_pre_draw` result | Durable P-1 | Durable + `hand_off` | `begin` |
|---|---|---|---|---|---|
| 5 | passes | completes | ran, returned a hold | passes (107,962 edges) | passes (102,316) |
| 9 | not run | completes (`hand_off` ran) | ran, returned a hold | passes (127,544) | passes (120,810) |
| 10 | passes | completes | ran, returned a hold | **refused** | passes (125,433) |
| 11 | passes | completes | ran, returned a hold | refused | passes (130,056) |
| 12 | passes | completes | ran, returned a hold | refused | **refused** |
| 14 | passes | completes | ran, returned a hold | refused | not run |
| 16, 17 | passes | completes | **traced:** entered, returned ok | refused | not run |
| 18, 19 | passes | **refused** | **traced:** entered, returned ok; the wrapper's receipt recheck then refused | not reached | not run |
| 20 | **passes** | refused | **traced: not entered** | not reached | not run |
| 21 | **the cap refuses** | refused | **traced: not entered** | not reached | not run |

**The trace is the basis for the "Durable P-1" column at n = 16 to 21** (`nc-reach-v4`). It logs entry to `project`, its return, and a wrapper refusal after the step, in the real
`durable_pre_draw`. r1 inferred the location from the call's result, which could not tell these apart: all four refusals at 18 to 21 report the same `Project(Receipt(BudgetExhausted))`. From 5 to 14 the
column follows from `durable_pre_draw` returning a hold, which only P-1's step produces.

**The limit, stated plainly.** "At most 20" binds only on the read path. On the durable path, on this first-use fixture, the effective limit through `hand_off`
is **9 components** today, and in the traced runs P-1's cap never decides, because 21 does not reach it. At M3's five components, 23,110 edges remain after `hand_off`. The coordinator
files this as backlog CP-DURABLE-EDGE-REACH.

**A composition constraint (REVIEW-E3 §2.3).** A valid P-1 view-fit calculation does not guarantee that a whole durable acquisition or handoff fits. The rechecks that r7:1047 places outside the view's fit are not free: they
stay on their ledgers. The 23,110-edge remainder does not itself show that C2a-4d or R10a fits.

**How far these numbers hold.** They are measurements on this fixture at these heads. They are not law, and no control pins them:
- A minimal tree gives the same outcomes at every row (`nc-reach-v1`), so the tree's size is not the driver at these sizes.
- First-use registration is the path measured; later acquisitions on one fixture were not tabulated.
- Refusals fail closed. The durable refusal is `Project(Installation(BudgetExhausted))`; the read path's cap terminates `BudgetExhausted`.

Evidence (`sec-predraw-1/evidence/`, each with its exact uncommitted experiment patch): `nc-reach-v1` (the read and durable results),
`nc-reach-v2` (the edge figures, and n = 9; `begin` against durable, n = 1 to 11), `nc-reach-v3` (`begin` at 11, 12, 13), `nc-reach-v4` (the trace of P-1's entry and return, n = 16 to 21).

## 3. The per-step rechecks, counted

r7:1047-1049 declares the wrappers' per-step rechecks and places them outside the view's fit. As LD-Q-240 requires, these are counted,
not inferred: each call was logged with its attempt-ledger delta and its caller (`nc-rechecks-v1`).

**Count, from the admitted subject to the end of `hand_off` or `begin`:**

| Path | `WritePlatformReceipt::recheck` (attempt ledger) | `DurableWriteGate::recheck` (gate ledger) |
|---|---|---|
| `begin` | 9 | 9 |
| durable | **10** | **10** |

**Which, in order, by caller** (each is the gate recheck, then the receipt recheck):

| # | `begin` | durable |
|---|---|---|
| 1 | `join_store_endpoint` | `join_store_endpoint` |
| 2 | `namespace_lease::admit` | `namespace_lease::admit` |
| 3 | `gate_step` (the first read) | `gate_step` (the first read) |
| 4 | `lease_free` | `lease_free` |
| 5 | `attempt_step` | `attempt_step` |
| 6 | — | **`gate_step` (P-1's step, r7:1048)** |
| 7 | `NamespaceTarget::lease` | `NamespaceTarget::lease` |
| 8 | `handoff` | `handoff` |
| 9 | `attempt_step` | `attempt_step` |
| 10 | `handoff` | `handoff` |

**The extra cost is exactly that one recheck, to the unit:**

| n | One receipt recheck (objects, edges, bytes) | Durable less `begin`, total attempt use |
|---|---|---|
| 1 | 458, 4,558, 477,198 | 458, 4,558, 477,198 |
| 5 | 498, 5,646, 554,566 | 498, 5,646, 554,566 |
| 9 | 538, 6,734, 631,934 | 538, 6,734, 631,934 |

Non-recheck edges are identical on the two paths at each n (42,802, 51,502, 60,204). So this is r7:1048's declared recheck, and nothing else on the
attempt ledger differs. `hand_off`'s comparison charge runs no recheck.

**Growth, `begin`, n = 1 to 9:** 4,623.25 edges per component. Of that, 2,448 is the nine rechecks at 272 each, and 2,175.25 is other work on the
attempt ledger, which E-3 does not itemise.

## 4. The two controls, as they run

**On the read `Some` path: unchanged from r7.** A real signed chain, a real retaining report read, and the real `read_pre_draw`:
- 20 components admit, within E-2's success bound (at most 10 objects, at most 185,700 B), with zero edges, the bare step's recheck subtracted;
- 21 refuse on `TrustRow::Budget`, terminating `BudgetExhausted`, with no `ReadPreDraw` and the fence free;
- on a twin live session, the real `charged_step` over the same refusal leaves the session ledger unchanged: no P-1 allocation, the mark included.

**On the durable path: E-3's form, replacing r7:529's durable clause for these two controls.** The real `gate_step` wrapper, on a writer from a one-component
installation, over the real signed N-component inventory and revocation list that a real first read retained on a separate N-component installation:
- 20 admit, under the same bound, the bare step's recheck subtracted;
- 21 refuse at the premise, with the gate ledger unchanged (the mark included), and the gate spent.

**What this form does and does not exercise:**
- It runs the same `project`, the same wrapper, and a real signed inventory. **It bypasses the production acquisition prefix and also uses the small writer's post-step rechecks,** not an N-component writer's.
- Its evidence is P-1's cap and boundary behaviour, and the real wrapper's success, refusal and latch behaviour, under that context. **It does not establish N-component durable composition, or that the N-component post-step recheck is affordable.** The trace shows it is not, at 18 and 19, on this fixture.
- It does not run `durable_pre_draw`'s own closure (`pre_draw.rs:244`) on `Cap`. That closure is exercised through C-A3i's revocation, and `Cap`'s route to
  `TrustRow::Budget` by the unit tests (`trust_pre_draw_tests.rs:415-425`), but not together.
- Inventory and writer come from different installations, which production cannot do. No claim is made about such a pairing; it exists only to reach the premise.

**The counting allocator (r7:1066, :1135-1136) is unchanged and stays owed** on both forms, at SP-7. The executed observations above are ledger observations.

**Mutations (SP branch, evidence `sp7c-controls-v1`, `sp7c-m26-v2`):** each is killed by both forms.
- the cap refusing at 20;
- the cap admitting 21;
- a charge before the premise.

## 5. What does not change

No constant, order, row or bound:
- `MAX_CATALOG_COMPONENTS_M3 = 20`, P-1's order, route (a);
- `EDGE_LIMIT` and the other ledger limits;
- E-2's bounds; FB-1's fit, which concerns the view's ledger and places these rechecks outside it (r7:1047);
- C-NC-site, C-NC-fit, C-SORT-0, C-A1i′.

E-3 adds no product code. It is not a finding against r7's funding, which never claimed the durable path could carry 20.

## 6. Out of scope

- Any change to `EDGE_LIMIT` or to the receipt's recheck cost: CP-DURABLE-EDGE-REACH.
- Whether C2a-4d's own spending on this attempt ledger fits the remaining margin. The coordinator has told C2a-4 the figure. This unit has not assessed it.

## 7. Changes from r1 (`b1c2e547…`, REVIEW-E3 `5f588870…`)

- **E3-RF-1, answered by a trace rather than by narrowing.** r1's "18 or more never reaches P-1" was **false at 18 and 19**. §1 and §2 now state the located boundary, with `nc-reach-v4` as the basis. The same false sentence stands in the commit message of `ac87730`, kept as history; the comment
  was corrected in `778fbf5`, which is otherwise unchanged. The 9/10 boundary is now scoped to the measured first-use fixture.
- **E3-RF-2.** §4 no longer says the form removes "only" the prefix, and states what it does not establish.
- **Added from REVIEW-E3 §2.3:** the composition constraint in §2.

Unchanged from r1: §3's count, §5 and §6, the controls and their mutations, and every constant.
