# Independent review — command/policy composition 258 r1 (with 256/257)

**Standing:** one bounded review of frozen `command-policy-composition-reference-wip-258-r1` plus derivation of its 256/257 components. **Not** three separate approval ceremonies, full metadata admission, private-policy adoption, effective merge, claimed COMPLETED effects, staging, current trust, or native publication. Archived 255 (`edc45b4a…147d`), 254 review (`133979ba…1905`), and 254 owner notes were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Nested 255/256/257 archives pin-verified; remaining fixture siblings reused from already-verified extracts. Frozen fixture/key/result directories were not overwritten. Hardcoded `/tmp/opensip-implementation` test-driver paths were redirected in the review copy only.

---

## Verification

| Archive | Bytes | Members | SHA256 |
|---|---:|---:|---|
| 258 r1 | 18830192 | 1586 | `b36518ef3e96a911c77f5ab7eb818e98011d47e3f5f7679501b2d00efc90f622` |
| 256 r1 | 17368 | 132 | `4806dc299f73f4d0ed1354ae9def3f258a578b267d10fb341a797a556e56b793` |
| 257 r1 | 13992 | 93 | `d1e3122ec792bd79c00cbd04492d2bf745d82a66c2b2a2695c0792978b80c57a` |

Pin, tar, member count, and every `subject.json` hash matched before extract; extracts rehashed 1586/132/93. Nested copies of 255 (`335b7b47…06a5`), 256, and 257 inside 258 match those pins. Standing: Incomplete WIP.

258 candidate: **1373** files, **12** SHA deltas vs 255 (4 new, 8 changed), **39** pin updates (after hashes 39/39). New: `trust_policy_reference.py`, v8 `permission-policy.schema.json`, `command_metadata_reference.py`, composition note. Changed: `trust_operation_reference.py` plus inventories.

Keys are **TEST ONLY**.

---

## 256 — original COMPLETED BEGIN/COMMIT → authenticated metadata

`command_metadata_reference.py` uses 255 delivery’s **same** `Operation`. Closed delivery input first; closure is derived only from BEGIN `operation.input` or COMMIT retained `BeginBatch.closure`. No caller `closure_ref`. Then `op.recovery_metadata` on that closure; batch payload/auth/closure and authority/replacement RootBindings must equal the signed authorization; `selected` ⊆ signed `recoveries`; output context digests join. Role subset is not batch completeness. ABORT/FAILED stay on `D.prepare`; this helper refuses those scopes.

**r1 harness, not production:** extra-field `DocRef` was correctly refused as `shape:DocRef`, but r1 `check_command_metadata.py` omitted `M.A.I.Refusal` / `M.MD.I.Refusal`. Beforeimage + `check-r1.stderr` retained. r2 adds those classes and asserts `shape:DocRef`. Production SHA `0544b9b5…2f21` is unchanged.

**Reproduction class:** *adapted, not a second 256 ceremony.* 258’s 43 command cases keep the original 36 labels and add a valid signed raw-policy fixture. Frozen 256 r2 counters **18 / 65 / 26866**; 258 live **18 / 67 / 26944** (policy member). Frozen 256 six omission controls were **inspected** (skip actual metadata, roots, roles, closed input, outer guard, reset budget), not rerun, to avoid a third key-generation pass.

---

## 257 — packaged raw policy structure

After 255 metadata auth on one Operation, every `permissionPolicies` member is read (no first-file preference). Exact existing v8 raw schema (`3d7153d9…6d5b`, byte-identical to the 257 copy and to v2), integer `policySchema`, `admit_policy_paths`, duplicate `(stableId,token)` grant/deny. Raw blob SHA vs `opensip.metadata.policy.1` preimage are distinct. No policy envelope, merge, consent, or write. Empty list is not private-policy absence. Same bytes at two declared paths are both represented.

**Reproduction class:** *exact.* Live relocated 36 cases and counters **14 / 42 / 21548** equal frozen 257 and frozen 258. Helper AST (minus unwrapped public `prepare`) equals 257. Frozen 257 six omission controls were **inspected**, not rerun.

Standalone 257 still has a public `prepare` + `budget.guard`; 258 moves that wrapper to `Operation.recovery_policy_bodies` so command/policy share class identity.

---

## 258 — composition

Lower `trust_policy_reference` is 257 `_prepare` with local metadata/schema load; no Operation/workflow import. `Operation.recovery_policy_bodies` is the outer `budget.guard`. Workflow `command_metadata_reference` is 256 after **three** explicit body deltas: call `recovery_policy_bodies` on the actual derived closure and take nested `metadata`; return inert `policyBodies`; pending owner `native-private-policy-adoption-and-effective-merge` (packaged policy structure removed from remaining full-metadata wording). No security→workflow import, no `/tmp`/`m2-` in the command helper, no production monkeypatch. Public envelope/schema/49-row inventory unchanged.

### Reproduction

Fresh `policy-check-live` and `integration-fixtures-live`. Frozen generated dirs were not overwritten.

| Kind | Corpus | Result |
|---|---|---|
| Exact | Relocated 257 policy | **36/36**, counters **14 / 42 / 21548** |
| Adapted | Relocated 256 command + policy fixture + 7 linked | **43/43**, counters **18 / 67 / 26944** |
| Exact | 247 delivery + isolated import/schema/inventory | **38 + 5**, counters 9 / 17 / 6723 |
| Exact | Helper AST / three command deltas / no tmp | **3/3** |
| Exact | Composition controls | **2/2** (skip required policy body; omit outer command guard) |
| Observed | Helpers while minting TEST-ONLY keys | **42 / 32 / 35 / 48** |

Linked 7: legacy `D.prepare` still insufficient; BEGIN/COMMIT refuse own malformed policy and latch fail-stop; returned bodies confer no effective grant. Mutant incorrectly returns bounded command standing; exceptions are not counted. Real crypto stays enabled.

Root suites **inspected, not rerun**: foundation 231, native 477, workflows 2193, security 580, carrier 479, integration 1787; envelope 168 / 147 / 1803 / 47 payload-dispatch deltas / 55 actual replay-crypto / 6000 fuzz. Those receipts do not qualify native effects.

---

## Independent probes

| Probe | Result |
|---|---|
| Unrelated valid closure vs command’s bad payload | refuses (BEGIN and COMMIT) |
| Wrong batch authority/replacement; selected outside recoveries | `authenticated-batch-root-bindings` / `batch-outside-signed-role-scope` |
| Caller `closure_ref` | `closed-delivery-input` |
| Extra DocRef field | `shape:DocRef` |
| ABORT / FAILED | old `D.prepare` still works; helper refuses |
| COMPLETED + later delivery failure | still representable as a **claim** |
| Invalid packaged policy required on BEGIN/COMMIT | `packaged-policy-shape`; fail-stop latches |
| Empty list / two-path duplicate bytes / project grants | no adoption, no effective-grant inference |
| `merge_policy` / file write in policy helper | absent |
| Isolated import + pin tamper | pass / refuse |
| 255/254/253 reports | hashes unchanged |

Returned `policyBodies` are a private reference result, not a public wire field and not a native grant.

---

## Remaining (do not count closed)

Native private-policy source adoption and v8 effective merge; artifact/repair and other-root contexts; retained revocation population and non-key subjects; held authority, ancestry, floors, S4; claimed COMPLETED role/batch/whole-image effects; native invocation/attempt/store/fence/slot; live census, durability, replay, delivery. GC, evidence commands, mutating transport, native writers, source selection, M3–M6. 258 is not installed runtime source.

---

## Verdict

- [x] 258/256/257 archives verified. Nested 255/256/257 pins match.
- [x] **Exact:** 36 policy cases/counters identical to 257; 38+5 delivery; helper AST; 2 composition controls. **Adapted:** 43 command cases (256’s 36 labels + signed policy + 7 linked). **Inspected:** 256/257 six-control reports, 256 r1 harness stderr, 7-suite receipts.
- [x] 256 r1 failure was harness exception-class omission; production unchanged. 257 schema is the existing v8/v2 raw policy schema. 258 does not adopt or merge policy.
- [ ] **Not** full member admission, private-policy authority, claimed-effect proof, staging, current trust, or native publication.
