# Advisory: canonical map domain vs Python `dict.items` walk order

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded **reference/API** question only. **Not source-32. Not ACCEPT-DESIGN-UNIT. Not runtime. Not first-fault product identity.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-canonical-walk-order-33/review`. No live/frozen/history edits. No install.

Selected identity `7b6750a9…0da2` / 158739 (`stage-meta-reference-selection-v1/reference/identity_model.py`). `open_run_closure.walk` (950–983) iterates `value.items()` on dicts. Product Rust `JsonValue` is `BTreeMap<String, Value>` (`crates/identity/src/canonical.rs`). This assignment does **not** review composed `full_walk` owner behavior (source-32 / wN).

## Decision

**The narrow oracle projection is sufficient and legal for a fixed Rust structural API.** An explicit identity-model successor that sorts walk keys (or freezes first-refusal) is **not required** now and must **not** be slipped in as an implicit hash or validity change.

## Normative / byte boundary

Identity-and-evidence §3: **C(X)** is canonical JSON with **UTF-8 byte-ordered object keys**; arrays keep admitted order (`x-opensip-order`). **H(D,X)** hashes `C(X)`, not walk-visit order.

- `C.canonical` already `sort_keys=True`. Two insertion permutations of one object have **equal** C bytes and **equal** H.
- `C.parse(C.canonical(v))` rebuilds a Python dict whose `.items()` order **is** that UTF-8 key order (probe: `zzz` then `aaa` vs reverse → both parse to `aaa`, `zzz`).
- Rust `parse` inserts into `BTreeMap`; iteration is the same UTF-8/lexicographic order. The representable request domain is **decoded C(X)**, never an arbitrary CPython insertion-order dict.

`canonical_bytes` in the selected model already refuses `C.canonical(value)!=raw` and then walks the **parsed** value. Feeding the oracle `C.parse(C.canonical(v))` is the same domain the product parser exposes.

## What differs (and what must not be claimed)

Preserved insertion-order oracle (`m2-full-walk-trial-32/initial-insertion-order-oracle`): **2/8** shared class mismatches (`shared-payload-shift-start` invalid vs unavailable; `ladder-before-universe` unavailable vs relation-rung). Current `check_full_walk_shared32.py` with canonical decode: **8/8** agree; valid shared payload **checked**; body/anchor refusals are real named causes.

Independent permutation probe (`probes/probe-results.json`):

| Input | C(X) / H | `value.items()` first undeclared key |
| --- | --- | --- |
| `{"zzz":1,"aaa":2}` raw | equal | `zzz` |
| `{"aaa":2,"zzz":1}` raw | equal | `aaa` |
| either after `C.parse(C.canonical)` | equal | `aaa` (UTF-8 order, matches BTreeMap) |

So:

- **Final accept** of a fully-good canonical object is permutation-stable (every property must pass).
- **First-fault cause** (and sometimes **invalid vs unavailable**) among several independent faults is **not** a C(X)/H property. It follows map iteration. Insertion-order Python dicts are **outside** the Rust representable domain.
- Resource/Limit vs named refusal remains a **class** comparison on that canonical domain; do not treat first-fault strings on raw fixtures as product law.

## Successor?

**Do not write one now.** Sorting `walk` to `sorted(value.items(), key=lambda kv: kv[0].encode("utf-8"))` would only make the Python helper total over non-canonical in-memory dicts. It is optional later hygiene, not a product-hash fix. It must not touch `C.canonical`, array `x-opensip-order`, or identifier recipes.

A first-refusal successor (which of several faults wins as a published rule) is a **larger** semantic claim. Not required for the Rust structural API if comparison is restricted to the canonical map domain.

## requiredFindings (advisory; not a live unit)

1. Source-32 / Rust comparison must use the **canonical map domain** (`C.parse(C.canonical(v))` or parse of retained C bytes). Insertion-order first-fault parity is extra-product and is **not** claimed.
2. Do **not** change selected `C.canonical` or array order to “fix” walk. Preserve the insertion-order oracle as negative evidence; do not rewrite it into old REFUSE.

## Limits / not claimed

Not source-32 acceptance, not full_walk implementation, not runtime, not first-fault as H identity. wN reviews composed owner behavior separately on this canonical domain.
