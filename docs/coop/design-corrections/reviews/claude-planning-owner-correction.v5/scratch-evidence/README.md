# claude-planning-owner-correction.v5 — PS-01 final-boundary corrections

Authored, not self-accepted. v4 and all earlier work are immutable and retained;
v4 is copied here as `v4-baseline/` with `hashes.v4-baseline.json`. All six of
root's supplied counterexample files, plus root's exact copy of the v4 law, are
retained unchanged in `root-counterexamples/`, together with
`early-abort.observed.json` recording my re-run.

Frozen candidate25 unmodified. **PS-04 bytes unchanged** (`ae82ca6a…`).

## Root's v4 counterexamples: both accepted

I ran `early-abort.py` unchanged against root's exact copy of the v4 law; it
reproduces the supplied JSON byte-for-byte.

**RC-6 — phase-sensitive marker availability.** For the owner-admitted
`intentStoreMigrate` at LEASED the owner returns `ABORT`. That phase precedes
materialisation of the new store, so its marker cannot exist — yet v4 required
`selectedStoreRoot` in every branch and turned the lawful early abort into
`QUARANTINE`. ABORTED is the same class: an unpublished target may already have
been reclaimed by the GC census.

**RC-7 — idempotent path bypassed ancestry.** `admit_node` returned `idempotent`
on an exact target match *before* running `ancestry()`. An existing target whose
immediate predecessor existed but whose chain was broken returned `validated`
with `refusal: None`, while the whole-set auditor reported the broken chain.

## Corrections

1. **Marker requirement bound to the owner's phase.** A settled transition
   (`RESUME-COMMIT` / `RELEASE-ONLY` → `DONE`) needs both markers. An unsettled one
   (`ABORT`, `RELEASE-ONLY` → `ABORTED`) accepts a stated absent target: no target
   triple can be formed, no premature node is possible, and the owner's abort
   stands. `BUSY` / `REFUSE` / `QUARANTINE` still read no marker at all.
2. **Three-way target observation**: `readable`, `absent` (not materialised yet, or
   reclaimed) and `unreadable` (observed but malformed). An unreadable target never
   becomes an absent one; an absence must be *stated*, never inferred from a
   missing key. Where a target *is* observable, its marker is validated before any
   dereference and a premature node is refused at that **full triple** only — never
   by scanning numeric pairs or digests.
3. **Idempotent path validates.** Chain and uniqueness checks now run on the exact-
   match path too, over the set that will stand. It still writes nothing and
   rewrites no origin. The same validation was added to the non-forward path.
4. **One-root is a component invariant.** Several lineages may coexist — an
   authorized restore or adoption starts its own — so the rule is that the chain
   from the node under consideration reaches exactly one root. The auditor takes an
   explicit expected component count instead of assuming one.
5. **Real schema admission boundary.** `controls/node_schema.py` builds a validator
   from the companion's own closed schema using the frozen
   `foundation/canonical.py` `ExactValidator`, whose integer type checker refuses a
   JSON boolean. The law no longer guesses member sets, types or version constants;
   a caller that has already admitted its inputs must say so with the explicit
   `ASSUME_SCHEMA_ADMITTED` sentinel, which controls record as a labelled
   assumption. Otherwise the law refuses rather than assuming.

## Files

| File | v4 | v5 | Patch |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 88249 B | 89310 B | 2 hunks, +25/−7 |
| `store-instance-lineage.v1.json` | 59050 B | 67088 B | 7 hunks, +57/−21 |
| `report-asset-binding.v1.json` | 27714 B | **unchanged** | — |
| `security-and-lifecycle.md` (frozen25) | `12dcebea…` 94428 B | `3cce913c…` 102205 B | **2 hunks, +112/−0** |
| `controls/lineage_law.py` | | | 13 hunks |
| `controls/check_lineage_recovery.py` | | | 16 hunks |
| `controls/check_store_instance_lineage.py` | | | 3 hunks |
| `controls/node_schema.py` | — | 2106 B | new |

Node schema unchanged at six members; no new public schema, member or operation.
Eight of nine planning inputs byte-identical to frozen; both generated plan blocks
byte-identical. Exact digests in `manifest.json`.

## Controls

    python docs/operations/check_repository_file_inventory.py --check
    python docs/operations/check_implementation_planning.py --source <c25> --check
    python controls/check_store_instance_lineage.py work <c25>
    python controls/check_lineage_recovery.py work <c25>
    python controls/check_report_asset_binding.py work <c25>
    python controls/check_report_asset_fixture.py

All six PASS. `check_lineage_recovery` sections: **A** root v2 regressions, **B**
owner pair law, **C** 7 operation cases × 6 journal states *with real lifecycle
timing*, **D** root v3 regressions, **E** composed migrate → rollback → second
forward selection, **F** damaged / duplicate / unreadable / off-chain, **G** owner
actions that decide nothing, **H** root v5 phase-sensitive markers, **I** root v5
idempotent-path validation (broken, clean, cyclic, non-forward dangling), **J**
lineage components beside a restored store.

Section C no longer synthesises a target marker in every phase: a forward
selection's target is stated **absent** at LEASED, PREPARING and ABORTED, so the
defect RC-6 exposed cannot be masked again. Every section records its input
assumptions under `inputAssumptions`, and node shape is admitted by the real schema
rather than assumed.

## Limitations

- Proposed, unaccepted, unfrozen; no readiness. Independent final review is root's
  next step — I do not accept my own corrections.
- No product code. Named owning modules already exist in the inventory, so no
  inventory row and no generated-section change.
- Owner results are the frozen model's own returns. The companion law is a design
  reference, not a carrier implementation, crash test or native lifecycle
  qualification, and it is deliberately not a product parser.
- Whether a target store root is absent or merely unreadable is an observation the
  implementation must make honestly at the existing S9 footprint boundaries. This
  design states the three outcomes and their consequences; it measures no
  filesystem.
- `StateSchema` is `{1, 2}`, so no owner-admitted example exercises multiple
  distinct ancestors at one schema; the ancestor branch already refuses ambiguous
  and off-chain matches.
- Whole-install-root substitution and a readable-but-wrong marker remain in
  frozen25's stated undetected class.
- The CORE release catalog/manifest shape remains not provided by candidate25 and
  unassigned. COV-03 and the separately active carrier work remain open.
