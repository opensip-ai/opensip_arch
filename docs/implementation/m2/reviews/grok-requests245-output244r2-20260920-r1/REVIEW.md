# Independent review — trust request slice 245 r1 and output follow-through 244 r2

**Standing:** bounded code review of frozen 245 r1 plus 244 r2. **Not** cumulative approval, 51-command completion, product installation, native dispatch, mutating API/MCP, or authenticated effects. Archived 244 r1 / 242 r2 / 243 reports were not edited.

Python 3.12.13 `-I -B`. Siblings reconstructed from verified 239 r2 (`822e3a9f…48c3`), 241 r1, and 242 r2 (`4b649237…6188`). Frozen variant output directories were not overwritten.

---

## Verification

| Archive | SHA256 | Bytes | Members |
|---|---|---|---|
| `trust-command-request-wip-245-r1` | `6c7b70fc…3647` | 19356 | 18 |
| `installation-output-wip-244-r2` | `ce13548b…996a` | 15048 | 43 |

Pin, tar, member count, and every `subject.json` hash matched before extract. Both extracts rehashed in full. 244 r2 and 245 `inputs.json` pins match the reconstructed 239/242 siblings (242 module `3ff84c3f…bc62`, map `af719206…c48e`).

244 r2 `before-r1/` is byte-identical to frozen 244 r1 schema and `output_reference.py`. r2 **schema** changed; the Python constructor is **unchanged** (`de40f007…30ce`).

---

## Part A — 244 r2: raw-schema GC fail-closed

The 244 r1 finding was: constructors refused `store-gc`, but `validate()` still admitted a project-shaped GC mutation envelope because installation-vs-project `if` enums omitted unowned-sweep.

r2 fix (schema only):

- `MutationReceiptProjection.operation` `$ref`s 242 `MutationOperation` and **`not: {enum: [store-gc]}`**, built from the map’s `unowned-sweep` operations (currently one token).
- Both installation-branch predicates (`projection.allOf[0].if.operation` and envelope `kind=mutation` then-branch) `$ref` `CurrentInstallationMutationReplayScopeV1.properties.operation` — **one owner**, no copied 15-token enum.
- Historical envelope URI is unchanged; a project-shaped GC document remains readable there.

### Reproduction

| Corpus | Result |
|---|---|
| `check_output.py` | **84/84** equal frozen `output-check-r4.json` |
| `check_variants.py` | **4/4** identity/key/request/exit controls (r2 dir) |
| `check_gc_schema_variant.py` | **1/1** omitting `operation.not` admits unowned GC; baseline `CONFIG.INVALID` |

New vs r1 (79→84): current schema refuses project-shaped and installation-shaped GC envelopes; historical GC readability; single-owner `$ref` assertion; well-shaped INDETERMINATE observation with recomputed `receiptId` under `operational-failed` / `HOST.IO_FAILURE` / exit 4, still `prepared-output-only` with three pending owners.

### Independent probes

| Probe | Result |
|---|---|
| Current URI + project-shaped `store-gc` | `CONFIG.INVALID` |
| Current URI + installation-shaped `store-gc` | `CONFIG.INVALID` |
| Historical URI + project-shaped `store-gc` | admitted (intentional) |
| INDETERMINATE full receipt, new identity | formats as prepared-only (r1 fixture failure was not general unrepresentability) |

**effectOutcome vs termination.class:** the formatter still joins **only** `termination.class` → `exitCode` (the r1 table). It does **not** pair `mutation.effectOutcome` with termination. Sources checked: envelope schema and workflows-and-surfaces do not state a closed (effect, class) matrix for this projection. Explicit selected cases: COMPLETED + `operational-failed` (failed delivery); INDETERMINATE + host-io as observation. Probe: **FAILED receipt + `success`/exit 0 still formats** (`prepared-output-only`). That is a **missing semantic output-registry join**, not a 244 r2 schema regression and not this module claiming command success. Do not treat it as a literal projection bug in the exit table.

No durable-uncertainty write permission: formatting is not retention.

---

## Part B — 245 r1 four trust request/inventory slice

Four exact CLI leaves: `trust ceremony begin|commit|abort`, `trust acknowledge-restore`. Closed body `{action}` only (`additionalProperties: false`). Transport JSON may have whitespace; retained intent is canonical. Duplicate keys, extra fields (`roles`, `store`, `projectId`, `authority`, `requestId`, `force`, `confirmation`, `path`), aliases, and `PATH` extras refuse. Host `RequestId` and S/G/K are arguments, not public fields. Installation key comes from 242.

Proposed inventory: **49 rows** = 45 existing rows JSON-equal + 4 security trust mutators. 242 `CommandName` enum is the same 49 names. Two evidence commands still absent — not 51-command completion. Distinct URI `urn:opensip:proposal245:command-inventory` adds the four names and authorization class **`trust-state-command`**.

### `trust-state-command` fit

The class is **prospective** and explicitly not a grant or network permission. Description: named action + admitted installation custody/selected store + trust-only active-transition barrier + installation fence; action-specific signed/state guards remain **mandatory**.

| Existing class | Relation |
|---|---|
| `user-consent` | interactive / `--yes-policy`. New class forbids confirmation substitution. Resolves 222 “no implicit confirmation” without reinterpreting user-consent. |
| `core-transition-leases` | S9.2 intent/journal + affected-namespace EXCLUSIVE. New rows `writesTrackedIntent: false`; `lockClass` fence-only. No contradiction if not used for executors. |
| `security-grant` | RepoExecutionGrantV2. New rows `authority: none`, `repositoryExecution: never`. |
| `exclusive-lease` | S7 EXCLUSIVE per namespace. Trust writes are fence-only / no project lock. |
| `recovery-authority-quorum` | S4.5 epoch. Ceremony signed guards stay a **separate** owner, as the description says. |

**No silent reuse of an old class.** The remaining work is implementing those guards/fence/barrier — the class name does not dispatch them. `observerSelector: observe` and `lockClass` are standing metadata, not executed here.

**222 vs agent-serve:** existing `agent-serve` is read-only (`steps: [query]`, `authorizationClass: none`) and **unchanged**. `current_agent_request` refuses all four bodies (`mutating-agent-transport-owner-unavailable`). Parsing intent is not an API/MCP grant. Do not treat this slice as satisfying 222 counterparts.

### Reproduction

| Corpus | Result |
|---|---|
| `check_requests.py` | **76/76** equal frozen `request-check-r1.json` (source `bee8e447…8982`) |
| `check_variants.py` | **3/3** closed-body / exact-CLI / ephemeral omission controls |

### Independent probes

| Probe | Result |
|---|---|
| CLI `['trust','ceremony','begin']` equals canonical body | admitted |
| Extra body field `authorizationClass` | `CONFIG.INVALID` (not a caller flag) |
| CI + `format=agent` | `prepared-invocation-only`, class `trust-state-command`; render format is not transport |
| `current_agent_request` | `mutating-agent-transport-owner-unavailable` |
| 49 inventory names vs 242 `CommandName` | equal; four new tokens only |

`prepare_invocation` builds required mutation step 0 (`retryPolicy: none`) and required render step 1 (`dependencyGate: terminal`, human/json/agent only). It validates 242 current invocation and **self-joins** `bind_step(wire, wire, ...)`. That is not retained custody. Ephemeral refuses. No `projectId` on the invocation.

---

## Concrete items before slice integration

1. **244 r2 GC schema fix is real** for current URI `validate()`. Historical GC envelopes stay readable. Do not add historical `not`.
2. **effectOutcome/termination pairing** is still a semantic output owner. The formatter’s only literal table is class→exitCode. FAILED+success currently formats as prepared-only.
3. **245 parity fields** `payload-digest` / `authorization-digest` / `batch-id` are declared on the four rows; typed projection, nullability, and refusal mapping are **not** implemented. Count them pending.
4. **Mutating transport** (API/MCP) remains owed. Agent format ≠ agent-serve mutation.
5. **Action-specific signed/state guards, fence, trust-only barrier, 241/243 outcome compose** remain pending. `trust-state-command` must not be treated as those owners.

Do not count those pending owners closed.

---

## Verdict

- [x] Both archives/pins/members verified. 244 r2: **84/4/1** reproduced. Raw current schema refuses unowned-sweep (`store-gc`) in both envelope shapes; installation branches `$ref` the 242 scope operation owner. Historical GC readability unchanged. INDETERMINATE observation is representable and not a write grant.
- [x] 245 r1: **76/3** reproduced. Closed `{action}` bodies, CLI/body parity, 49=45+4 with 242 name alignment, CI without invented consent, ephemeral refused, agent-serve read-only preserved. `trust-state-command` is an explicit new class, not a silent reinterpretation.
- [x] GC raw-schema bypass from 244 r1 is closed on the current URI. Constructor still does not prove effect/delivery/replay.
- [ ] **Not** 51-command completion, product installation, native/transport dispatch, or 222 API/MCP availability.
