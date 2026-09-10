"""EDIT 5 (item 2, V20-ROOT-4): the default-construction duplicate guard names the REGISTERED key.

WHAT WAS MEASURED (probes/p2, results/p2-before.json):
  * `public_termination_for("DUPLICATE_REQUESTED_CAPABILITY")` and
    `failure_envelope_errors(...)` both refuse `native.public-route-key-unregistered:...`, so this
    refusal had no derivable public termination at all. The gap is REAL.
  * The condition is EXACTLY the registered `native.requested-capability-duplicate-ownership-tuple`
    condition. The route registry's own host-generated branch is written for it verbatim: "a host
    BUG minting its own invalid internal layer - DEFAULT CONSTRUCTION THAT EMITTED TWO ROWS FOR ONE
    CELL". The same rows meet that registered key at `admit_requested_capabilities`, measured.
  * The registry ALSO said "Exact whole-item duplicates never reach here - uniqueItems and the
    canonical-set order law refuse them first". On the DEFAULT-CONSTRUCTION path that was false:
    this guard runs BEFORE `admit_analysis_spec`, so uniqueItems is never reached. That sentence is
    corrected below rather than left to contradict the code.

WHAT IS NOT CHANGED, and why the guard is kept where it is:
  * It still refuses and still never dedupes; no requested analysis is lost.
  * It still runs BEFORE `admit_analysis_spec`, because `requestedCapabilities` is `uniqueItems`
    and the schema's answer for these rows is a generic ValidationError restating the whole
    instance (measured: results/p2-before.json `sameRowsAtWholeSpecBoundary`) - the same reason
    the cardinality guard precedes generic validation.
  * No origin is guessed here. `public_termination_for(key, origin)` is the HOST's derivation with
    the origin it holds; this helper emits the key alone, exactly as `helperDoesNotGuessOrigin`
    requires of every other guard.

WHAT IS NOT DONE: registering `DUPLICATE_REQUESTED_CAPABILITY` as a SECOND route row. That would be
a parallel vocabulary for one condition, and the alias map cannot carry it either - `aliasRule` /
`aliasMapIsContextFree` forbid a context-free alias for an origin-DEPENDENT key.
"""
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
applied = []


def sub(rel, old, new, count=1):
    p = ROOT / rel
    s = p.read_text()
    n = s.count(old)
    assert n == count, '%s: expected %d, found %d for %r' % (rel, count, n, old[:90])
    p.write_text(s.replace(old, new))
    applied.append({'file': rel, 'occurrences': n})


# --- (a) the guard --------------------------------------------------------------------------
sub('docs/coop/design-corrections/native/native_evidence_model.v2.py',
    """    # `analysis-spec.requestedCapabilities` is x-opensip-order: canonical-set, so the emitted array is in
    # canonical-byte order, not discovery order; a duplicate row refuses rather than silently deduping.
    requested = sorted(requested, key=C.canonical)
    if len({C.canonical(r) for r in requested}) != len(requested):
        raise AdmissionError("DUPLICATE_REQUESTED_CAPABILITY")
""",
    """    # `analysis-spec.requestedCapabilities` is x-opensip-order: canonical-set, so the emitted array is in
    # canonical-byte order, not discovery order; a duplicate row refuses rather than silently deduping.
    #
    # IT REFUSES UNDER THE REGISTERED KEY, which it did not always do. This guard used to raise a bespoke
    # `DUPLICATE_REQUESTED_CAPABILITY`, which had NO row in x-opensip-public-route-registry - so
    # `public_termination_for` and `failure_envelope_errors` both refused it
    # (`native.public-route-key-unregistered`) and a host holding this refusal could derive no public
    # termination for it at all. The condition is not a new one: it is exactly the registered
    # `native.requested-capability-duplicate-ownership-tuple`, whose host-generated route is written for
    # this very call site - "default construction that emitted two rows for one cell". Naming that key
    # here gives the refusal the origin-dependent route it always should have had, and adds no public
    # DomainDetailCode member.
    #
    # THE TUPLE IS THE NAME OF THE DEFECT, so it is the tuple that is reported. Every row this function
    # builds carries `required: True` literally, so for THESE rows a byte-identical duplicate and an
    # ownership-tuple duplicate are the same set; detecting on the tuple states the law that is actually
    # named and produces the same subject format `admit_requested_capabilities` produces, so the two
    # guards cannot drift in what they publish.
    #
    # THE POSITION IS UNCHANGED, and deliberately. `requestedCapabilities` is `uniqueItems`, so without
    # this guard these rows would refuse inside `admit_analysis_spec` as a generic schema ValidationError
    # restating the whole instance - the same reason the cardinality guard precedes generic validation.
    # NO ORIGIN IS GUESSED: this helper emits the internal key alone, and the host calls
    # `public_termination_for(key, origin)` with the origin it already holds.
    requested = sorted(requested, key=C.canonical)
    owners: dict[tuple[str, str, str], int] = {}
    for row in requested:
        tuple_key = (row["capabilityId"], row["languageMode"], row["workspaceRoot"])
        owners[tuple_key] = owners.get(tuple_key, 0) + 1
    for tuple_key in sorted(k for k, n in owners.items() if n > 1):
        raise AdmissionError("native.requested-capability-duplicate-ownership-tuple:" + ":".join(tuple_key))
""")

# --- (b) the route registry's own statement about reachability -------------------------------
SCHEMAS = ROOT / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
doc = json.loads(SCHEMAS.read_text())
row = doc['x-opensip-public-route-registry']['keys']['native.requested-capability-duplicate-ownership-tuple']
OLD_TAIL = (" Exact whole-item duplicates never reach here - uniqueItems and the canonical-set order law "
            "refuse them first - so this key always names DISTINCT rows.")
NEW_TAIL = (" WHICH ROWS REACH THIS KEY, stated exactly, because an earlier revision said `exact whole-item "
            "duplicates never reach here - uniqueItems and the canonical-set order law refuse them first` "
            "and that was true of only one of the two paths. On an EXPLICITLY SUPPLIED spec it holds: "
            "admit_analysis_spec runs validate_foundation before the vocabulary helper, so byte-identical "
            "rows refuse on uniqueItems and this key sees only DISTINCT rows disagreeing on `required`. On "
            "the DEFAULT-CONSTRUCTION path it does not: default_capability_selection guards its own freshly "
            "built rows BEFORE admit_analysis_spec - because the schema's answer there is a generic "
            "ValidationError restating the whole instance - and those rows all carry required=True, so the "
            "duplicate it catches IS byte-identical. That guard names THIS key rather than a bespoke one, so "
            "the host-generated route below is reachable from the call site it was written for instead of "
            "from nothing. Both paths report the same (capabilityId, languageMode, workspaceRoot) subject.")
assert row['why'].endswith(OLD_TAIL), row['why'][-200:]
row['why'] = row['why'][:-len(OLD_TAIL)] + NEW_TAIL
SCHEMAS.write_text(json.dumps(doc, indent=1) + '\n')
applied.append({'file': 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
                'occurrences': 1})

# --- (c) the owning normative prose ----------------------------------------------------------
sub('docs/v2/contracts/product-v1/native-evidence.md',
    """routes, and it adds **no** public `DomainDetailCode` member. Default construction
  is unaffected: the matrix-fixed default emits unique tuples, and two co-located
  units in one mode produce byte-identical rows that the existing
  `DUPLICATE_REQUESTED_CAPABILITY` guard already refuses rather than silently
  deduplicating, so no requested analysis is lost.
""",
    """routes, and it adds **no** public `DomainDetailCode` member. Default construction
  reports the **same** key. The matrix-fixed default emits unique tuples, and two
  co-located units in one mode produce byte-identical rows that
  `default_capability_selection` refuses rather than silently deduplicating, so no
  requested analysis is lost. That guard runs **before** the analysis-spec boundary
  — `uniqueItems` would otherwise answer with a generic schema error restating the
  whole instance, the same reason the §10 cardinality guard precedes generic
  validation — and it names this registered key, not a private one. An earlier
  revision raised a bespoke `DUPLICATE_REQUESTED_CAPABILITY` there, which had **no**
  row in the §10 route registry: `public_termination_for` refused it
  (`native.public-route-key-unregistered`), so the one refusal the default path can
  reach had no derivable public termination at all, even though this key's
  host-generated route was written for exactly that call site. The refusal, its
  position and its non-deduplicating behaviour are unchanged; only the key it names
  is, and no public `DomainDetailCode` member is added for it.
""")

# The byte-identical sentence one paragraph earlier is scoped to the path where it is true.
sub('docs/v2/contracts/product-v1/native-evidence.md',
    """different registered `languageMode` is a different cell and remains legal, and
  different capabilities on one unit remain legal. A **byte-identical** duplicate
  row is a different defect and keeps its own earlier answer — `uniqueItems` and
  the canonical-set order law — so this rule owns only distinct rows over one
  tuple.""",
    """different registered `languageMode` is a different cell and remains legal, and
  different capabilities on one unit remain legal. In an **explicitly supplied**
  spec a **byte-identical** duplicate row is a different defect and keeps its own
  earlier answer — `uniqueItems` and the canonical-set order law refuse it at
  `validate_foundation`, before this rule is reached — so on that path this rule
  owns only distinct rows over one tuple. On the **default-construction** path the
  guard described below runs first and reports byte-identical rows under this same
  key; both paths name the same tuple.""")

print(json.dumps({'applied': applied}, indent=1))
