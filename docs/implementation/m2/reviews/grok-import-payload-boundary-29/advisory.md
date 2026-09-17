# Advisory: import-registry totality (`payloadDomain` type)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded reference-totality advisory for import payload-registry lookup. **Not ACCEPT-DESIGN-UNIT. Not source-27. Not runtime. Not full walk / correspondence / replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-import-payload-boundary-29/review`. No live/frozen/history edits.

Selected identity `7b6750a9…0da2` / 158739 (`stage-meta-reference-selection-v1/reference/identity_model.py`). Selected workflows `1d5212d5…9874` / 142828 (`predicate-matching-reference-selection-v1/reference/workflows_model.v1.py`; v2 candidate; `registry_row` region byte-identical to coop parent `be37023f…66dc` / 142811). Identity schema import class `a76c9e2f…db21` / 196987. Live lock independently **20 inventory / 28 contract** (inventory v22, runtime v13).

## Law (do not invert)

Identity-schemas.v3 `x-opensip-payload-registry.law`: a key with **no row refuses**; there is **no default row** and **no caller-selected schema**. `keyedBy` for import is `kind` (naming record) + `payload.payloadDomain` (parsed payload).

`registered_payload` (1102–1120) **decodes first**, then selects the row:

1. `canonical_bytes(digest, 'NONCANONICAL_REGISTERED_PAYLOAD')` — memoized parse only
2. Build `key` from `keyedBy` (`payload.*` via `value.get` if the payload is a dict, else `None`)
3. `registry_row` → for `payloadClass=='import'`, `W.registry_row(key[0], key[1])` then identity `rows.get(str(key[0])+'|'+str(key[1]))`
4. No row → `PAYLOAD_IMPORT_UNREGISTERED:+str(key)`
5. Owner vs declared document/selector differ → `PAYLOAD_IMPORT_REGISTRY_DRIFT:+str(key)`
6. Only then: registered schema digest, `validate_registered_record` on **that row's** selector

Payload-schema validation **cannot** precede row selection: that would guess a schema. Arrays/objects as `payloadDomain` are **well-formed** integer JSON (`C.parse` / `typed` allow list and dict). They must still be **unregistered keys**, not a Python crash.

## Gap (independently reproduced)

Selected `registry_row` (workflows 813–814):

```python
def registry_row(kind, payload_domain):
    return PAYLOAD_REGISTRY.get((kind, payload_domain))
```

`PAYLOAD_REGISTRY` has **exactly five** `(str, str)` keys. `dict.get` of a tuple containing a list or dict raises `TypeError: cannot use 'tuple' as a dict key (unhashable type: 'list'|'dict')` **before** the identity `owner is None` named refusal.

Identity import branch (1080–1084) is otherwise fail-closed: `declared` uses `str(key[…])`, which is hashable. The crash is only the workflows tuple lookup.

Exact probes (`review/probes/probe-results.json`):

| Probe | Current `W.registry_row` | Identity import branch after `type is str` guard |
| --- | --- | --- |
| five valid `(kind, domain)` strings | row | row (owners workflow/native unchanged) |
| unknown strings | `None` | `PAYLOAD_IMPORT_UNREGISTERED` |
| `payloadDomain` `[]` / `{}` / `[[]]` | **TypeError unhashable** | `PAYLOAD_IMPORT_UNREGISTERED` |
| `kind` `[]` / `{}` | **TypeError unhashable** | `PAYLOAD_IMPORT_UNREGISTERED` |
| `None` / `True` / `False` / `0` / `1` | `None` (hashable miss) | `PAYLOAD_IMPORT_UNREGISTERED` |

Reachable JSON types after selected integer parse: object, array, string, int, bool, null. Only **array and object** are unhashable. Null/bool/int already miss.

## bool/int equality cannot admit a row

All five keys are two strings. Independently: every pair of `{True, False, 0, 1, None}` as `(kind, domain)` admits **zero** rows. `True==1` does not help. Identity `str(True)+'|'+…` does not collide with `runtime|workflow.import-payload.runtime.v1` (0 collisions). Use `type(x) is str`, not `isinstance(x, int)` (bool is an `int` subclass).

## Is `W.registry_row` the only required site?

**Yes, for the identity `registered_payload` / Rust import-payloads owner.** That path’s only unhashable lookup is `PAYLOAD_REGISTRY.get((kind, payload_domain))`. Identity’s `declared` map is `str`-keyed. A type guard that returns `None` unless **both** elements are `str` preserves decode→key→row→named refusal and the five valid rows.

**Not sufficient for `build_import` (837–839).** After a `None` miss, ` '…' + payload_domain` still TypeErrors for list/dict/bool. That constructor is outside the retained import-payloads owner. Optional follow-up; do not block this successor on it.

Relation `key[0] not in RELATIONS` has a similar unhashable gap; it is **not** this import owner.

## Minimal explicit reference successor

Selected workflows `registry_row` only (keep the five-row table and `PAYLOAD_BINDINGS` unchanged):

```python
def registry_row(kind, payload_domain):
    if type(kind) is not str or type(payload_domain) is not str:
        return None
    return PAYLOAD_REGISTRY.get((kind, payload_domain))
```

No identity-schema change (law already refuses an unregistered key). No identity_model change required for this import path. Do **not** validate the payload against a guessed selector first.

Required review: **formal DESIGN-UNIT** of that workflows reference successor (parent = selected `1d5212d5…9874` candidate / predicate-matching-v2 record as live accepted set requires). Then the pure Rust `import_payloads` owner may fail-closed against the same five rows.

Rust: if `kind` or `payloadDomain` is not a string → `PAYLOAD_IMPORT_UNREGISTERED` (no Python list/`repr` suffix). Same for `PAYLOAD_IMPORT_REGISTRY_DRIFT`. Those are the two repr suffixes to normalize. Inert named codes only; not full walk, correspondence, or replay.

## requiredFindings (advisory)

1. `W.registry_row` / `PAYLOAD_REGISTRY.get((kind, payload_domain))` is not total over well-formed JSON: list/object keys raise `TypeError` instead of `PAYLOAD_IMPORT_UNREGISTERED`.
2. Successor must type-guard **both** tuple elements as exact `str` and return `None`; identity then raises the named code. Valid five-row behavior must stay.

## Limits / not claimed

Not source-27, inventory-v22 re-acceptance, runtime, `open_run_closure`, correspondence, or replay. Probes used extracted selected `PAYLOAD_REGISTRY`/`registry_row` AST plus the identity import branch; they did not execute full `open_run_closure`. `build_import` concat and relation-class `in` lookup are adjacent, not this owner.
