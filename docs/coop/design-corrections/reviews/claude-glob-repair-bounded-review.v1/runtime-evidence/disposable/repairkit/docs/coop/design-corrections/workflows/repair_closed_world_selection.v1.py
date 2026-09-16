"""AUTHOR_PENDING_REVIEW. Repair closed-world SELECTION law: which retained native
ClosedWorldV2 records the delete/replace prerequisite reads, and the deterministic display
summary the descriptor carries.

WHY THIS EXISTS. workflows-and-surfaces section 6 and both repair.schema.json documents
previously said the prerequisite is decided against "the evidence Run's own native
ClosedWorldV2", as though a Run held one. It does not. `ClosedWorldV2` is a REQUIRED member
of `ViewEntryV3` (native-evidence.md section 4.3), so a Run holds ONE PER COVERAGE ENTRY,
keyed by `CoverageKeyV2` (relation, resolution, sourceUniverse, targetUniverse,
subjectScopeCommitment). identity-and-evidence.md section 3 makes several differing entries
lawful in one Run in as many words: "A differing tuple is a different claim, not an overlap,
which is why the same subject may lawfully appear under two relations, two rungs or two
universes." With N retained records, "that Run's own ClosedWorldV2" does not denote. This
module states which records are read and in what order.

WHAT THIS MODULE IS NOT.
  * It is NOT native producer qualification. Every ClosedWorldV2 it reads is a trusted
    producer observation already admitted by the native owner; this module re-admits nothing
    and validates no native record. A malformed native record is refused at the native
    producer boundary (`admit_coverage_result_v3`) and again at retained Run closure, which
    are the actual admission sites; this module is downstream of both and is not a second
    validator.
  * It is NOT a full product repair, and it is NOT authorization. `repair-preview` is a
    Query-class step. Trust, consent, current-snapshot equality and an authorization bound
    to the exact `repairPlanId` remain separately required at apply, unchanged.
  * It does not qualify a compiler, a provider, an enumerator or a repository read.

ROLE SPLIT, kept strict:
  * The GATE reads FULL retained native `ClosedWorldV2` records (RS-4).
  * The DESCRIPTOR carries a five-field DISPLAY SUMMARY (RS-5). The summary is a
    deterministic reduction for display and for the `repairPlanId` preimage. It is NOT a
    native producer record, does not claim to be one, and is never an input to the gate.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------- published law

#: Unchanged and unqualified: every `delete` and every `replace` in a plan is unsafe.
UNSAFE_ACTIONS = frozenset({"delete", "replace"})

_REGISTRY = json.loads(
    (HERE.parent / "foundation" / "relation-payload-schemas.v2.json").read_text()
)["x-opensip-relation-registry"]

#: The relations whose subject-scope `subjects` ARE snapshot paths, read from the single
#: published registry rather than restated. `subjectKindLaw` says of `source-path`: "each
#: subject is a path in the snapshot this scope names, so the scope's own extent is exactly
#: those paths". It says of `symbol`: the enumerator's attribution of symbols to files "is
#: NOT re-derivable from the retained Run ... inventing symbol-to-path parsing would be
#: fabricated evidence." So a symbol-kind or package-name-kind scope NEVER contributes a path
#: owner here, and no prefix, display string, sidecar or unreferenced host observation does.
SOURCE_PATH_RELATIONS = frozenset(
    name for name, row in _REGISTRY["relations"].items() if row.get("subjectKind") == "source-path"
)

#: Every source-path relation is `universeRule: same-only`, so for this join
#: sourceUniverse == targetUniverse and there is no cross-universe join left implicit.
SOURCE_PATH_UNIVERSE_RULES = {
    name: _REGISTRY["relations"][name]["universeRule"] for name in sorted(SOURCE_PATH_RELATIONS)
}

#: Per-field CLOSED-to-OPEN order for the display reduction (RS-5). Index 0 is the most
#: closed member; the reduction takes the greatest index present. `exportsClosed` reuses the
#: same closed/open/unknown order the existing foundation fold already applies, so this
#: introduces no second ordering for that field; it is reused, not claimed as normative there.
DISPLAY_ORDER = {
    "exportsClosed": ("closed", "open", "unknown"),
    "entryPointsRecognized": ("all", "partial", "none"),
    "nonliteralLoading": ("none", "present"),
    "externalConsumers": ("none-declared", "possible", "unknown"),
}

#: The five descriptor members, in the descriptor's own order. Shape unchanged.
DISPLAY_FIELDS = (
    "deadCodeRepairEligible",
    "exportsClosed",
    "entryPointsRecognized",
    "nonliteralLoading",
    "externalConsumers",
)

#: RS-5 empty case. `deadCodeRepairEligible=false` is the authoritative part. The four enum
#: members take the LEAST-CLOSED member of their own enum, which is the same rule the
#: non-empty case applies, so the empty case is not a special case with its own vocabulary.
#: DISCLOSED LIMIT: `nonliteralLoading` has no `unknown` member in the current owner enum
#: (`none|present`), so its least-closed pole is `present`. That is a DISPLAY CONVENTION
#: under one uniform rule, not an observation that nonliteral loading was seen. Adding an
#: `unknown` member would be a native `ClosedWorldV2` field-shape change, which this unit
#: does not own and does not make.
EMPTY_DISPLAY_SUMMARY = {
    "deadCodeRepairEligible": False,
    "exportsClosed": "unknown",
    "entryPointsRecognized": "none",
    "nonliteralLoading": "present",
    "externalConsumers": "unknown",
}

CLOSED_WORLD_NOT_ESTABLISHED = "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"


class RetainedEvidenceUnavailable(Exception):
    """A retained record this law must read is not resolvable in the supplied closure.

    Raised rather than guessed. The caller maps it to the existing typed repair outcome; this
    module mints no public detail code and asks for none.
    """


# ------------------------------------------------------------------- retained-graph adapter

class RetainedRunView:
    """A read-only view over the retained objects/blobs of ONE admitted Run.

    `objects` and `blobs` are exactly the mapping shape the identity owner's `close_run`
    consumes: `objects[id] = (domain, record)` and `blobs[digest] = bytes`. Nothing is
    re-admitted here. Construction does not assert that the Run was admitted; the caller
    supplies a closure it has already had admitted, and the controls in this unit do exactly
    that through the foundation replay fixtures.
    """

    def __init__(self, run, objects, blobs):
        self.run = run
        self.objects = objects
        self.blobs = blobs
        self.snapshot_id = run["snapshotId"]
        self._evidence = self._get(run["evidenceId"], "semantic-evidence")

    def _get(self, key, domain):
        entry = self.objects.get(key)
        if entry is None or entry[0] != domain:
            raise RetainedEvidenceUnavailable(domain + ":" + str(key))
        return entry[1]

    # -- findings -----------------------------------------------------------------
    def matched_findings(self):
        """Every retained finding of this Run whose correspondence state is `matched`.

        Unmatched findings are already not lawful repair targets
        (`REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE`), so they are not universe sources either.
        """
        out = []
        for fid in self._evidence["findingIds"]:
            finding = self._get(fid, "finding")
            if finding.get("correspondence", {}).get("state") == "matched":
                out.append((fid, finding))
        return out

    def subject(self, subject_id):
        return self._get(subject_id, "evaluation-subject")

    # -- scopes and coverage ------------------------------------------------------
    def subject_scopes(self):
        """Every subject-scope the Run's views reference, including scopes with no Coverage.

        identity-and-evidence.md section 3 states the partition rule covers "every scope the
        view references, including scopes with no Coverage entry", so enumerating through the
        views is the retained enumeration, not a convenience.
        """
        out = {}
        for vid in self._evidence["viewIds"]:
            view = self._get(vid, "view")
            for sid in view["scopeIds"]:
                out[sid] = self._get(sid, "subject-scope")
        return out

    def coverage_records(self):
        """Every retained coverage2 of this Run, joined to its own scope and payload."""
        out = []
        for cid in self._evidence["coverageIds"]:
            coverage = self._get(cid, "coverage")
            scope = self._get(coverage["scopeId"], "subject-scope")
            raw = self.blobs.get(coverage["payloadDigest"])
            if raw is None:
                raise RetainedEvidenceUnavailable("coverage-payload:" + coverage["payloadDigest"])
            out.append((cid, coverage, scope, json.loads(raw)))
        return out


# ------------------------------------------------------------------------------ the law

def unsafe_edit_paths(edits):
    """RS-1. Every `delete` and every `replace` path in the plan, sorted by exact bytes.

    The unsafe SET is those two actions without qualification. No target-to-edit pointer is
    used or invented: `targets` and `edits` are separate descriptor arrays with no published
    correspondence between them, and this law reads each on its own terms.
    """
    return sorted({e["path"] for e in edits if e["action"] in UNSAFE_ACTIONS},
                  key=lambda p: p.encode())


def target_universes(view, targets):
    """RS-2a. Universes reached through ALL matching occurrences of EVERY target fingerprint.

    finding3 -> subject3 -> universe, a join the Run closure guarantees: dropping the
    `evaluation-subject` records makes `close_run` refuse with EVIDENCE_UNAVAILABLE. A
    representative occurrence is deliberately NOT used, because one fingerprint may be matched
    in two universes and the projection law that groups them compares ruleId, subjectPath,
    kind, qualifiedName and detector closure but NOT universe.
    """
    wanted = set(targets)
    found = {}
    for fid, finding in view.matched_findings():
        if finding.get("fingerprint") in wanted:
            universe = view.subject(finding["subjectId"])["universe"]
            found.setdefault(universe, []).append(
                {"via": "target", "fingerprint": finding["fingerprint"], "findingId": fid}
            )
    return found


def path_owner_universes(view, paths):
    """RS-2b. The analysis universes that OWN each unsafe edited path.

    Ownership is read from retained subject-scopes of source-path-kind relations only, whose
    `subjects` ARE snapshot paths by the published `subjectKindLaw`. Legitimate MULTIPLE
    ownership is preserved rather than collapsed: one physical path analysed under two Rust
    targets or editions is two different `sourceUniverse` values, and both are returned, so
    both must be eligible.

    Returns (universeSources, unownedPaths). An unowned path is NOT silently dropped and is
    NOT treated as vacuously satisfied; the caller turns it into a typed refusal.
    """
    found = {}
    owned = set()
    for sid, scope in sorted(view.subject_scopes().items()):
        if scope["relation"] not in SOURCE_PATH_RELATIONS:
            continue
        if scope["snapshotId"] != view.snapshot_id:
            continue
        subjects = set(scope["subjects"])
        for path in paths:
            if path in subjects:
                owned.add(path)
                found.setdefault(scope["sourceUniverse"], []).append(
                    {"via": "unsafe-edit-path", "path": path,
                     "relation": scope["relation"], "resolution": scope["resolution"],
                     "scopeId": sid}
                )
    return found, [p for p in paths if p not in owned]


def relevant_universes(view, targets, edits):
    """RS-2. U* = universes of all target occurrences UNION universes owning any unsafe path.

    A universe in neither set is TRULY UNRELATED and does not veto. That scoping is the whole
    reason an unrelated closed finding cannot justify deleting a path analysed in an open
    universe, and equally the reason an unrelated open universe cannot block a plan.
    """
    paths = unsafe_edit_paths(edits)
    by_path, unowned = path_owner_universes(view, paths)
    sources = {}
    for bucket in (target_universes(view, targets), by_path):
        for universe, why in bucket.items():
            sources.setdefault(universe, []).extend(why)
    # Provenance rows are sorted by their own canonical spelling so the derivation is
    # reproducible whatever order the caller enumerated findings, scopes or edits in.
    sources = {u: sorted(v, key=lambda d: json.dumps(d, sort_keys=True).encode())
               for u, v in sources.items()}
    return sorted(sources, key=lambda u: u.encode()), sources, unowned, paths


def select_coverage(view, universes):
    """RS-3. Every retained native coverage2 whose scope's SOURCE universe is relevant.

    SOURCE-VS-TARGET, stated rather than left implicit: `ClosedWorldV2` characterises the
    universe whose subjects were examined. The published `coverageTotality.matchLaw` calls
    totality "a claim about what THIS universe examined", and that extent is the scope's
    SOURCE side. So relevance is decided on `sourceUniverse` ALONE. An entry with
    sourceUniverse=w outside U* and targetUniverse inside U* is an observation MADE IN w about
    edges into U*; its closed world describes w, so joining it would import exactly the
    unrelated evidence this scoping exists to exclude. For the three source-path relations the
    question cannot even arise: they are all `universeRule: same-only`.

    Selection is INDEPENDENT of the plan's `evidenceRequirements`. A recipe cannot narrow this
    set to a favourable relation or rung, and cannot remove a conflicting record from it.

    Dedupe is by retained `coverage2` IDENTITY, never by relation. Order is the full published
    partition key plus that identity as the final tie-break, so the result is total and does
    not depend on input enumeration order.
    """
    wanted = set(universes)
    rows = {}
    for cid, _coverage, scope, payload in view.coverage_records():
        if scope["snapshotId"] != view.snapshot_id:
            continue
        if scope["sourceUniverse"] not in wanted:
            continue
        key = payload["key"]
        rows[cid] = {
            "coverageId": cid,
            "relation": key["relation"],
            "resolution": key["resolution"],
            "sourceUniverse": key["sourceUniverse"],
            "targetUniverse": key["targetUniverse"],
            "subjectScopeCommitment": key["subjectScopeCommitment"],
            "closedWorld": payload["entry"]["closedWorld"],
        }
    return sorted(
        rows.values(),
        key=lambda r: (r["relation"].encode(), r["resolution"].encode(),
                       r["sourceUniverse"].encode(), r["targetUniverse"].encode(),
                       r["subjectScopeCommitment"].encode(), r["coverageId"].encode()),
    )


def display_summary(selected):
    """RS-5. The deterministic five-field DISPLAY SUMMARY.

    Not a native producer record, and it does not pretend to be one: a fieldwise reduction may
    combine members that no single producer emitted together. That is acceptable precisely
    because this record carries no authority. `deadCodeRepairEligible` is the conjunction; each
    enum member is the LEAST-CLOSED value present. With no selected record the same rule gives
    the fixed EMPTY_DISPLAY_SUMMARY, so the descriptor is deterministic even with zero native
    coverage, which is what keeps `repairPlanId` deterministic for a create-only plan.
    """
    if not selected:
        return dict(EMPTY_DISPLAY_SUMMARY)
    summary = {"deadCodeRepairEligible": all(
        bool(r["closedWorld"]["deadCodeRepairEligible"]) for r in selected)}
    for field, order in DISPLAY_ORDER.items():
        summary[field] = max((r["closedWorld"][field] for r in selected),
                             key=lambda value: order.index(value))
    return {field: summary[field] for field in DISPLAY_FIELDS}


def derive(view, targets, edits):
    """The whole law. Returns the selection, the gate outcome and the display summary.

    `gateActivated` is RS-1. `eligible` is RS-4 and is None when the gate is not activated,
    because a create-only plan asks no eligibility question: lack of closed-world eligibility
    ALONE must never add an unsafe-edit failure to a plan that makes no unsafe edit.
    """
    universes, sources, unowned, paths = relevant_universes(view, targets, edits)
    selected = select_coverage(view, universes)
    by_universe = {u: [r for r in selected if r["sourceUniverse"] == u] for u in universes}
    uncovered = sorted((u for u, rows in by_universe.items() if not rows),
                       key=lambda u: u.encode())

    gate_activated = bool(paths)
    unmet = []
    eligible = None
    if gate_activated:
        if unowned:
            unmet.append({
                "code": CLOSED_WORLD_NOT_ESTABLISHED,
                "remedy": "no retained source-path subject scope of this Run owns "
                          + ",".join(unowned)
                          + "; the analysing universe cannot be reconstructed from retained "
                            "evidence, and it is not guessed. Re-run analysis over a "
                            "configuration that enumerates this path.",
            })
        if not universes:
            unmet.append({
                "code": CLOSED_WORLD_NOT_ESTABLISHED,
                "remedy": "no relevant analysis universe could be derived for this plan; an "
                          "empty relevant set is not eligibility.",
            })
        for universe in uncovered:
            unmet.append({
                "code": CLOSED_WORLD_NOT_ESTABLISHED,
                "remedy": "relevant universe " + universe + " retains no native Coverage "
                          "record in this Run, so it establishes no closed world; an empty "
                          "evidence subset is not true.",
            })
        defeaters = [r for r in selected if not r["closedWorld"]["deadCodeRepairEligible"]]
        for row in defeaters:
            unmet.append({
                "code": CLOSED_WORLD_NOT_ESTABLISHED,
                "remedy": "native deadCodeRepairEligible is false for "
                          + row["relation"] + "@" + row["resolution"]
                          + " in universe " + row["sourceUniverse"]
                          + " (" + ",".join(row["closedWorld"].get("reasons", [])) + "); "
                          + "declare entry points/consumers explicitly and re-run analysis",
            })
        eligible = not unmet

    return {
        "gateActivated": gate_activated,
        "unsafePaths": paths,
        "relevantUniverses": universes,
        "universeSources": sources,
        "unownedUnsafePaths": unowned,
        "universesWithoutCoverage": uncovered,
        "selectedCoverage": selected,
        "eligible": eligible,
        "unmetPreconditions": unmet,
        "closedWorld": display_summary(selected),
    }
