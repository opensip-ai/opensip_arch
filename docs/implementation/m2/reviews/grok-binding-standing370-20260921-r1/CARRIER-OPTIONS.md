# Native ProjectId registry carrier — options (recommendation only)

**Standing:** bounded physical-carrier recommendation while root drafts the logical binding/S9 owner. **Not** acceptance, **not** a frozen owner, **not** implementation authorization. Do not revive historical opaque-`projectKey` DDL. Preserve every closed public record. Root will author/freeze the actual owner for independent review before implementation.

REVIEW.md (`304f4430…6b9a`) and findings.json (`b2a3d1e2…49cd`) are unchanged. ADDENDUM §1–3 (`a07f5dc4…ff03`) plus §4 lineage-root append remain the scope clarifications.

---

## Does any selected owner require `lifecycle.sqlite` for ProjectId registry?

**No.**

| Source | What it says | Lock input? |
|---|---|---|
| Identity §2 (`c82404f3…`) | “private host registry” must agree with `.opensip/project-id.v1`; no file format, no SQLite | yes |
| `resolved-inputs.v2.json#/projectIdContract` (`0114205a…`) | unique reservation in the host ProjectId registry; markerBytes ASCII; eight-candidate protocol; **no** `lifecycle.sqlite` | **no** |
| S9.2 | `registry` is `NamespaceList` of strings | yes |
| PSL 201 (historical copy `a5f6797c…`) | locates `lifecycle.sqlite` as “existing lifecycle owner” for registry/**carrier**; adopts **locator only** and does **not** revive historical registry identity/lease protocol | **no** |
| `lifecycle-carrier.contract.v2` / `.schema.v2.sql` | nine-field `project_registry` with opaque `projectKey`; `lifecycle.sqlite` | **no** (PROPOSED) |

Selected current owners therefore **do not** mandate SQLite for the revised ProjectId registry. An explicit successor **may** choose `I/project-registry.v1` (product-canonical bounded file under the installation fence) without contradicting lock text. PSL’s `lifecycle.sqlite` cell is an unselected locator for a **different**, superseded carrier, not a selected ProjectId store.

The revised native registry carrier remains a **prerequisite for actual native registry/root admission** (ADDENDUM §2). It is optional only for a purely logical five-field **view** under an already-admitted handle.

---

## Option A — `I/project-registry.v1` canonical bounded file (recommended default)

One regular file at a closed path relative to the admitted installation root `I`, opened through the **installation fence** (no path-string identity). Product-canonical JSON, cap bounded (recommend a hard byte cap before parse, same family as selection 4096 / marker 128 — exact cap is an owner choice). `additionalProperties: false`. Members should include at least:

- `schemaVersion` const 1
- `projectId` (`^prj1-[0-9a-f]{64}$`)
- `namespaceId` (lowercase UUIDv4, locator only; not interpolated from ProjectId)
- root-handle incarnation (device/inode/birth or the selected native identity the owner already uses)
- `status`: `RESERVED` | `ACTIVE` | `RETIRED` (tombstone)
- no opaque `projectKey`, no four-field epoch, no `newRoot` callback fields

**Uniqueness:** at most one `ACTIVE` row per ProjectId and per namespace `N`; at most one `ACTIVE` row per live root incarnation. Historical `RETIRED` rows retain ProjectId/`N`/root identity for correlation and **do not** grant admission. Duplicate live roots refuse. Source or target absence must be **positively observed** under custody, not inferred from a missing caller value.

**Crash ordering (mirror `projectIdContract`, not invent a new protocol):** reserve (`RESERVED` published atomically) → publish exact 92-byte ASCII marker (create-new, fsync marker and parent) → mark `ACTIVE`. Crash: drop uncommitted `RESERVED` **or** complete an exact matching marker; any other pre-existing marker bytes refuse. Callers never supply ProjectId.

**No pre-admission sidecar/data writes:** a single canonical file updated by exclusive no-replace / sibling-temp + durable rename under the fence produces no WAL/SHM. First-use (missing marker **and** missing registry) writes nothing until the authorized allocation act.

**Native descriptor binding:** all reads/writes use the retained installation-root handle; directory name is not identity; reconstruction of JSON fields outside the fence/lease does not reproduce current authority.

**Recovery:** explicit adopt/fork/move as identity §2; no silent import of a marker without registry; restore/adoption of a **store** remains a lineage **root outside any transition** (ADDENDUM §4) and must not invent an intent.

**Limits:** one-file uniqueness is installation-local. Concurrent writers serialize on the fence. Large historical tombstone sets need an explicit bound or a successor that splits history without changing V1 public records.

---

## Option B — SQLite carrier (allowed only with stricter constraints)

SQLite is **not** required. If chosen, it must **not** be a revival of `lifecycle-carrier.schema.v2.sql`. Forbidden: opaque `projectKey` PK, nine-field historical DDL, `lifecycle_project_root_verified` taking identity from `.opensip` (it already forbade that) **as a reason to ignore the project marker**, four-field epoch tickets as ProjectId authority.

Required if SQLite is used:

- **No pre-admission sidecar/data writes.** Opening `lifecycle.sqlite` with WAL creates `-wal`/`-shm` before any admission. That is incompatible with identity’s first-use (missing marker and registry) and with S9’s no-write pre-initialization. A SQLite option must use a connection mode that creates **no** sidecar and **no** data page until the authorized allocation act (or keep the DB off the admission path entirely until after fence+first-write). Default WAL `lifecycle.sqlite` as in the historical carrier **fails** this test.
- Native descriptor binding of the DB file and its parent under the installation fence; not a path string.
- Same reservation → marker fsync → ACTIVE ordering; crash recovery explicit.
- `ACTIVE` vs `RETIRED` uniqueness/tombstones as in Option A; historical rows never admit.
- Bundled SQLite remains TCB (already true of runtime25 security), which is extra trusted C, not a reason to pick SQLite.

---

## Comparison (for the owner draft)

| Requirement | `I/project-registry.v1` file | SQLite (new schema) |
|---|---|---|
| Selected owner currently requires this form | no | no |
| Pre-admission zero sidecar/data writes | yes, if unpublished until allocation | only if WAL/create-on-open is forbidden |
| Native handle / fence | yes | yes, plus DB file identity |
| Eight-candidate + marker fsync + ACTIVE | yes (file atomic publish) | yes (txn) **if** no sidecar before ACTIVE |
| Active vs historical uniqueness | encode in one bounded document | UNIQUE indexes on ACTIVE subset |
| Tombstones without granting admission | `RETIRED` rows | `RETIRED` rows; never revive opaque-key retired semantics |
| Revive historical DDL | must not | must not |
| Extra TCB | none beyond existing fence | bundled SQLite C + `cc` |

**Recommendation:** prefer **Option A** as the default for a first successor. It matches other product-canonical private records, avoids WAL-before-admission, and does not pretend PSL’s `lifecycle.sqlite` cell selected a ProjectId store. SQLite remains a later successor if cardinality/tombstones demand it, under the no-sidecar constraint.

This does not accept S9.3, does not invent a `stores/S` G/K header, and does not implement code.
