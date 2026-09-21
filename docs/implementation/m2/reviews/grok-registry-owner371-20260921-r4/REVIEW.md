# Independent review — project-registry owner371 r4

**Verdict: `ACCEPT-UNIT`** (bounded OWNER/REFERENCE). **Not** selected-unit activation, **not** five-member `StoreGenerationBindingV1`, **not** S9.3, **not** native/OS qualification, **not** product runtime.

Archive `b658a9ee…dc1b` / **224780 B / 196 members**; every `subject.json` member rehashed (0 mismatches). Candidate `registry-draft.md` `14181ef7…9c8c` / 27933 B; schema `545e0006…6294` / 2858 B (kind required; not r2-identical). r3 NEEDS-CHANGES `8f37b64c…99b8` archived unchanged. No product/architecture edits.

Independent replay in fresh dirs: **274/274** cases, **274 unique caseIds**, results **byte-equal** author `reference-results.r4b.json` (`00293def…6fce`); **24/24** schema+extra-rule checks; capacity max **320555**; **8** faults after baseline (including `adoption-completed-as-ordinary` and `ordinary-inconsistent-prefix`). Extract not overwritten. No native suites.

---

## r3 required finding

**Closed.** Every entry is five-member `{projectId, namespaceId, root, status, allocationKind}` with `allocationKind` ∈ `{random, adopt}`, set at insertion and **immutable**. Missing/unknown kind refuses (no on-read migration; no deployed four-member row). Recovery takes the **full document + selected RESERVED N**.

| Trace | Result |
|---|---|
| adopt-kind + ordinary-recovery, all ns/marker pairs, **with and without** historical ProjectId (8 cases) | `ADOPTION_CONTEXT_REQUIRED` |
| adopt-kind + admitted-adoption + matching ProjectId + complete-initial/exact | `publish-ACTIVE` (reconfirm, not create-new) |
| adopt-kind + admitted-adoption + **wrong** ProjectId | `ADOPTION_PROJECT_MISMATCH` |
| random-kind + admitted-adoption | `CONTEXT_KIND_MISMATCH` |
| random-kind + absent-ns + exact marker + ordinary | `ORDINARY_PREFIX_REFUSED` |
| random-kind + complete-initial + exact + ordinary | `publish-ACTIVE` — **only** because kind is random (lawful first-use prefix) |
| kind rewrite on activate/move | REFUSE |

History-only inference is **not** used: first-local/cross-machine adopt-kind has no historical row and still cannot complete as ordinary. That was the r3 hole; persisted kind closes it without widening ordinary recovery.

`mode` / `adoption_project_id` remain **labels** for externally admitted context (draft §96). Native must not treat them as APIs. Registry activation still cannot complete bundle import/evidence/origin.

---

## Initial r4 fault (not a kill)

Author `reuse-retired-project` mutant **survived** the first r4 fault run: the old example row had become **adopt-kind**, so `reserve-random` refused on kind mismatch and never hit the history-reuse guard. Corrected example is **random-kind** reusing a retired ProjectId. Initial checker/logs retained. Final r4b detects the mutant. Do not treat the first run as a valid kill.

---

## Residuals (not requiredFindings)

Native must still AND `complete-initial` with `initial_namespace_footprint` (two empty 0600 files / 0700 dir); the completion function does not call the checker. Observation tokens are not custody proofs. 271 unique diagnostic names vs 274 caseIds (ids are the uniqueness contract).

No opaque-`projectKey` revival. T1–T4, T6–T8 r2 prose remains on these bytes.

---

## requiredFindings

None.

This **supports a subsequent formal selected-unit review** (wrapper, root assent, private validation). It does **not** itself select, install, or authorize writers.
