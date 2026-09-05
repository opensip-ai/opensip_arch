# Steering 00 — Overview

**Subject:** how the shipping opensip-cli could move toward the greenfield
architecture in `../architecture/`.

**This is a different question from the design.** The design asks *what is
right*. This asks *what is reachable, in what order, at what risk*. Conflating
them is the error that caused this split — see `../architecture/10-method.md`,
Error 4.

---

## The one-way rule

> **`architecture/` may constrain `steering/`. Migration *decisions* may never
> constrain `architecture/`.**

The rule governs decisions, not evidence. A measurement taken here may be
promoted into the design tree if it is **construct-valid** — if it measures a
property that is not an artifact of the current system's constraints. Runtime
startup behaviour is construct-valid; "what fraction of today's rules do X" is
not, because today's rules were written under today's constraints. Promote with
the construct-validity argument stated, or not at all.

Concretely, none of the following is a valid design argument:

- "The existing corpus only does X, so the design should treat X as rare."
- "That would require rewriting N checks."
- "The current package layout makes that awkward."
- "We would need a compatibility alias for that."

Each is a legitimate *migration* consideration and belongs here. Each silently
narrows the design space when it appears in the other tree.

---

## What is in this tree

| Doc | Covers |
|-----|--------|
| [01 — Current-state evidence](01-current-state-evidence.md) | Measurements of the shipping product; porting cost; the calibration asymmetry |
| [02 — Reachability and slices](02-reachability-and-slices.md) | Which target elements are incrementally reachable; reversible strangler slices; prototype gates |
| [03 — Compatibility and parity](03-compatibility-and-parity.md) | Feature coverage, aliases, dual identities, legacy bridges, deletion discipline |

---

## The standing conclusion

**No rewrite.** Not because the target is wrong, but because the value at risk is
not in the code:

- Tuned rules carrying real-world false-positive calibration
- Working language adapters
- Qualification and burn-in lanes
- Accumulated knowledge of which edge cases actually bite

Rule **mechanics** port cheaply — 91% of check bodies are already pure functions
of their inputs. Rule **calibration** does not port at all. That asymmetry is the
entire argument for strangling rather than rewriting, and it makes **fixture
parity** the acceptance test for every rule migration.

## What the design costs to reach

Most of the target is reachable without discontinuity. Two elements are not:

| Element | Reachable incrementally? |
|---------|--------------------------|
| Unified Run identity, always-write Run, projections over one record | **Yes** |
| Shared fact store beneath existing capabilities | **Yes** |
| Centralised semantic provider | **Yes** — the existing graph adapter is close to the target shape |
| Declarative tier for the text-pattern rules | **Yes** |
| Baselines and gates as queries; recipe versioning | **Yes** |
| Contract consolidation | **Yes**, mechanical |
| Narrow producer interfaces replacing the tool contract | **Partly** — needs the fact store first |
| Out-of-process contribution edge | **No — discontinuity** |
| Host language change | **No — discontinuity** |

The two discontinuities are exactly the two that were never authorised. Everything
else is available now.

> **Caveat added by the greenfield re-derivation:** the design's execution
> topology is now *reopened* (`../architecture/08-surfaces-and-topology.md`,
> R-1). If it lands on a resident engine as the primary lifetime, the migration
> picture changes materially — residency is a larger change than any single slice
> below, and it should not be assumed away. Do not sequence past slice 4 without
> settling it.

## Highest-value work that depends on nothing

Two items are pure wins regardless of which target is chosen, and neither
requires an architectural decision:

1. **Fix the eager composition root** so metadata commands do not load compilers
   and grammars. Largest measured latency defect, lowest risk, no design
   dependency.
2. **Consolidate exit classification** to one mapper and one write site. Eight
   decision records, three mappers, and nearly two hundred exit-capable call
   sites say this concern has never had an owner.

Neither is blocked by anything in either tree.
