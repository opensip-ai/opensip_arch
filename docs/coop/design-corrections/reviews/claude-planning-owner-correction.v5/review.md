# PS-01 final-boundary corrections — v5

I ran root's `early-abort.py` unchanged against root's exact copy of the v4 law; it reproduces the supplied JSON byte-for-byte (`d706adcc…` both files). Both counterexamples are correct and accepted. v4 immutable (103/103 verified), frozen25 intact (12869 members, 0 mismatches), nine planning inputs unmodified, **PS-04 unchanged** (`ae82ca6a…`).

---

## RC-6 — phase-sensitive marker availability

At LEASED the owner returns `ABORT`; that phase precedes materialisation, so the target marker cannot exist. v4 demanded it in every branch and turned the lawful early abort into corruption.

The requirement is now bound to the owner's own decision, and the observation is a closed three-way outcome:

| journal state | owner | target observation | v4 | v5 |
|---|---|---|---|---|
| LEASED | `ABORT` | `absent` | **QUARANTINE** | `none`, no refusal |
| PREPARING | `ABORT` | `absent` | — | `none`, no refusal |
| ABORTED (reclaimed) | `RELEASE-ONLY` | `absent` | — | `none`, no refusal |
| LEASED, target observable | `ABORT` | `readable` | — | `none`, premature check at the full triple |
| LEASED, malformed marker | `ABORT` | `unreadable` | — | **QUARANTINE** |
| LEASED, premature node at the full triple | `ABORT` | `readable` | — | **QUARANTINE** |
| LEASED, retained branch at an equal pair | `ABORT` | `absent` | — | `none`, no refusal |

An **unreadable** target is never read as absence, and an absence must be *stated* — never inferred from a missing key. A settled transition still requires a readable target; an absent one there is corruption. `BUSY` / `REFUSE` / `QUARANTINE` consult no marker at all.

Section C now uses this timing rather than synthesising markers everywhere, so the defect cannot be masked again:

```
store-migrate  LEASED     ABORT         target absent    none
               PREPARING  ABORT         target absent    none
               PREPARED   RESUME-COMMIT target readable  reconstructed-and-written
               COMMITTED  RESUME-COMMIT target readable  reconstructed-and-written
               DONE       RELEASE-ONLY  target readable  reconstructed-and-written
               ABORTED    RELEASE-ONLY  target absent    none
```

## RC-7 — idempotent path bypassed ancestry

`admit_node` returned `idempotent` before `ancestry()`. Chain and uniqueness checks now run on that path too, over the set that will stand, still writing nothing and rewriting no origin:

```
existing exact target whose predecessor chain is broken -> QUARANTINE, 0 written
existing exact target on a clean chain                  -> validated, 0 written, origin intact
existing target on a cyclic chain                       -> QUARANTINE
ancestor reselect onto a node with a dangling chain     -> QUARANTINE
```

## Two direct consequences

**One-root is a component invariant.** Several lineages may coexist — an authorized restore or adoption starts its own — so the rule is that the chain from the node under consideration reaches exactly one root. The auditor takes an explicit expected component count. Section J confirms two declared components are clean, declaring one over two is reported, and a restored lineage does not block a lawful forward selection.

**Real schema admission boundary.** `controls/node_schema.py` builds a validator from the companion's own closed schema using the frozen `foundation/canonical.py` `ExactValidator`, whose integer checker refuses a JSON boolean. The law assumes no member set, type or version constant; a caller that already admitted its inputs must say so via `ASSUME_SCHEMA_ADMITTED`, recorded as a labelled assumption — otherwise the law refuses rather than guessing. A node with `stateSchema: true` is now refused at the boundary.

---

## Deliverables

| File | v4 | v5 | Patch |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 88249 B | 89310 B | 2 hunks, +25/−7 |
| `store-instance-lineage.v1.json` | 59050 B | 67088 B | 7 hunks, +57/−21 |
| `report-asset-binding.v1.json` | 27714 B | **unchanged** | — |
| `security-and-lifecycle.md` (frozen25) | `12dcebea…` 94428 B | `3cce913c…` 102205 B | **2 hunks, +112/−0** |
| `lineage_law.py` · `check_lineage_recovery.py` · `check_store_instance_lineage.py` | | | 13 · 16 · 3 hunks |
| `controls/node_schema.py` | — | 2106 B | new |

Node schema unchanged at six members; no new public schema, member or operation. Eight of nine planning inputs byte-identical to frozen; both generated plan blocks byte-identical; JSON valid with no duplicate keys; no trailing whitespace or tabs; links resolve. All six root counterexample files plus root's v4 law copy and my re-run output retained in `root-counterexamples/`; exact digests in `manifest.json`.

**All six controls PASS** (`control-evidence.json`). `check_lineage_recovery` sections A–J, each recording its `inputAssumptions`; shape admission is reported separately from current-state/footprint admission. Unrelated suites not rerun.

## Limitations

Proposed, unaccepted, unfrozen; no readiness — independent final review is root's next step and I do not accept my own corrections. No product code; the law is a design reference, deliberately not a product parser. Whether a target root is *absent* or merely *unreadable* is an observation the implementation must make honestly at the existing S9 footprint boundaries — this design states the three outcomes and their consequences and measures no filesystem. `StateSchema` is `{1,2}`, so no owner-admitted example exercises multiple distinct ancestors at one schema, though the ancestor branch already refuses ambiguous and off-chain matches. Whole-install-root substitution and a readable-but-wrong marker stay in frozen25's stated undetected class. The CORE release catalog/manifest shape remains not provided by candidate25 and unassigned; COV-03 and the separately active carrier work remain open.
