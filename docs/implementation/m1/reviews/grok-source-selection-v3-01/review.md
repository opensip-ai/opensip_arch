# Independent Grok correction review: source-selection v3

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/source-selection-v3-subject.json`
**Manifest SHA-256:** `ea4bb9bf97e68dc675c855798c647cfc6f784e5a6977839d560472ff79cc53ed`
**Members:** 140
**Verdict:** **ACCEPT-DESIGN-UNIT**

Binding-order correction of uninstalled source-selection-v2. Original Grok v2 `ACCEPT-DESIGN-UNIT` and historical root assent remain historical evidence. They did not install a source unit. This review does not relabel them as sufficient for the product lock.

## Missed prerequisite (SOURCE-BINDING-ORDER-01)

Root full product binding failed: `contract candidates paths must be sorted and unique` (`trials/source-selection-v2-integration-01/verify.stderr`). Product `pin_rows` compares `paths != sorted(set(paths))` on **full POSIX path strings**.

v2 candidates were ordered by `pathlib` component tuples. First divergence at index 7: Path order places `…/evidence/candidate-source-map.json` before `…/evidence-pins.json`; string order is the reverse (`'-' < '/'`). The earlier Grok v2 review compared candidate **sets** only and missed this. Independently reproduced: product `pin_rows` still refuses the frozen v2 successor and accepts the v3 list.

## Custody

| Check | Result |
| --- | --- |
| Manifest | `ea4bb9bf…53ed` matches declared |
| 140 pins | architecture bytes/length match |
| Inherited | 136 v2 non-record members byte-identical |
| New | four files under `source-selection-v3/`: README, `correction.json`, `check_binding.py`, `successor.json` |
| previousCandidate | frozen v2 successor `8bd78b83…2819`; not a v3 subject or candidate member |
| After | frozen 140 unchanged |

No schema, owner, dispatch, profile, or coverage change. Parents and passage overrides equal v2.

## Reproduction

Read-only `check_binding.py --architecture opensip_arch --product opensip`: exit 0, stdout byte-identical to frozen `source-selection-v3-01/check01.stdout`. Original source checker 40/14/323 still passes with `selectionApproved: false`. Original unsorted candidate list fails `sorted and unique`. Eight in-memory negatives refuse: reverse/duplicate/missing candidates, bad member pin, reverse/unaccepted parents, wrong before-image, duplicate override. `approvalFabricated: false`.

Independent probes **28/28**, including string-sorted subject and candidate arrays (139 candidates = subject minus this record, **order** not only set), live lock still inventory4 + two contracts and **no** source-selection record, all 11 parents still in the live accepted base, v3 member paths do not reuse accepted paths, live `verify_design` passes without this unit.

## Remaining verifier prerequisites (do not skip)

`contract_successor` still requires a review of **this** subject with `ACCEPT-DESIGN-UNIT` / empty `requiredFindings` / this manifest digest, and root `ACCEPTED-DESIGN-UNIT` assent naming this record. Historical v2 review+assent against a private candidate lock refuse (`contract review names a different manifest`). A wrong-subject review refuses (`independent contract acceptance missing or findings remain`). Those are installation steps after this review, not defects of the sorted record. No further structural refusal (parent set, path reuse, pin_rows order, passage before-images) was found against the actual accepted lock. This review does not fabricate assent or install the unit.

## Semantics

Original v2 source findings and open duties stand: report08 Q-FIT-1 remains CHANGES REQUIRED on that unit; selected fit/history/native/L02 composition is unchanged; R11 before M4; P01/X01 before M5; fresh blind consumer, generation/tool/bootstrap, and product qualification remain open.

## Must-fix / should-fix

None in this correction scope.

## Remaining

Fresh root assent and a candidate-lock `verify_design` run before installation. Not product, M1, or Claude agreement.
