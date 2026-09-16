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
    native producer record, does not claim to be one, NO MEMBER OF IT IS AUTHORITATIVE
    (the boolean included), and it is never an input to the gate.

WHERE OWNERSHIP COMES FROM. A first revision of this module derived path ownership from
retained source-path Coverage scopes alone. That was a real omission: those scopes prove only
that they NAME paths, not that they ENUMERATE every selected program that owns one. The
retained `EnumerationPlanV1` -- a REQUIRED evaluator3 analysis-spec parameter, refused as
`EVALUATOR_REQUIRED_PARAMETER_MISSING` when absent and re-admitted by full replay -- publishes
the program-to-path relation directly, through each selected binding's own `extents[]` and
`candidateSourcePaths`. `selected_program_owners` reads that census; source-path scopes are
unioned in as an additional witness only.

That omission is REACHABLE, not hypothetical: driving the enumeration owner's own
`admit_enumeration`, a Plan in which one universe binds ONLY on a symbol-kind cell -- owning a
path through its retained symbol extent, with no file inventory and therefore no lawful
`file@enumerated` scope -- is ADMITTED. So is an UNAVAILABLE selected binding retaining a host
extent that contains the path, and so is a candidate-only cell's `candidateSourcePaths`. Those
are enumeration-owner admissions, not full Runs, and this module says so where it matters.

SEPARATE AND UNTOUCHED: native `dynamicDispatch` keeps its target-relative role through
`affected_targets` and per-requirement `sufficiency_v2`; recipe trust, policy consent,
current-snapshot equality and the apply-time authorization bound to the exact `repairPlanId`
all remain separately required. Preview is a Query-class step and authorizes nothing.
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
#: those paths."
#:
#: THESE ARE AN ADDITIONAL RETAINED WITNESS, NOT THE OWNER CENSUS. An earlier revision of this
#: module derived path ownership from these scopes ALONE. That was wrong, and the reason is
#: worth stating precisely because the wrong argument is seductive: the `subjectKindLaw` proves
#: those scopes NAME paths; it does not prove they ENUMERATE every selected program that owns a
#: path. The companion observation -- that a symbol's path is not re-derivable from an opaque
#: native symbol ID -- is true and answers a DIFFERENT question, because the retained program's
#: path EXTENT is published directly by the EnumerationPlan and needs no symbol parsing at all.
#: The owner census is `selected_program_owners` below; these scopes are unioned in as a
#: redundant-or-additional witness and never as a completeness certificate.
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

#: RS-5 empty case: the five-field LEAST-CLOSED DISPLAY SENTINEL. It is NOT an "all-unknown"
#: record and must never be described as one. Exactly two members are `unknown`; the other
#: three are a false boolean, `entryPointsRecognized="none"` and `nonliteralLoading="present"`,
#: each the least-closed member of its own enum under the same rule the non-empty case applies.
#: NO MEMBER OF THIS RECORD IS AUTHORITATIVE, including the boolean: the authority is the full
#: native selection in `derive`, and this sentinel states only that nothing was selected to
#: display. DISCLOSED LIMIT: `ClosedWorldV2` has no `unknown` member for
#: `entryPointsRecognized` (`all|partial|none`) or `nonliteralLoading` (`none|present`), so
#: neither can spell "not observed"; their least-closed poles stand in. Root resolved this:
#: keep the existing enum and label the value a display sentinel. Widening the enum would be a
#: native field-shape change this unit does not own and does not make.
EMPTY_DISPLAY_SUMMARY = {
    "deadCodeRepairEligible": False,
    "exportsClosed": "unknown",
    "entryPointsRecognized": "none",
    "nonliteralLoading": "present",
    "externalConsumers": "unknown",
}

#: The published selection order (RS-3). Comparison is on the **UTF-8 encoded bytes** of each
#: member in this exact sequence: the five `CoverageKeyV2` coordinates, then the retained
#: `coverage2` identity as the final tie-break. Two lawfully distinct records that agree on the
#: five coordinates are still separated by the sixth, so the order is total.
SELECTION_ORDER_KEY = (
    "relation",
    "resolution",
    "sourceUniverse",
    "targetUniverse",
    "subjectScopeCommitment",
    "coverageId",
)

#: The registered analysis-spec parameter row that carries the retained EnumerationPlanV1.
ENUMERATION_PARAMETER_ROW = "foundation/enumeration-plan.schema.v1.json"

CLOSED_WORLD_NOT_ESTABLISHED = "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"


class RetainedEvidenceUnavailable(Exception):
    """A retained record this law must read is not resolvable in the supplied closure.

    Raised rather than guessed. The caller maps it to the existing typed repair outcome; this
    module mints no public detail code and asks for none.
    """


_PARAMETER_ROW_OF = None


def _default_parameter_row_of():
    """The identity owner's own registry resolution, loaded lazily by file.

    `identity-model.v3.parameter_row_of` is the SAME resolution the Run closure performs; it is
    imported rather than restated so a registry row added there is covered here with no edit.
    """
    global _PARAMETER_ROW_OF
    if _PARAMETER_ROW_OF is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "repair_selection_identity3", HERE.parent / "foundation" / "identity-model.v3.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _PARAMETER_ROW_OF = module.parameter_row_of
    return _PARAMETER_ROW_OF


# ------------------------------------------------------------------- retained-graph adapter

class RetainedRunView:
    """A read-only view over the retained objects/blobs of ONE admitted Run.

    `objects` and `blobs` are exactly the mapping shape the identity owner's `close_run`
    consumes: `objects[id] = (domain, record)` and `blobs[digest] = bytes`. Nothing is
    re-admitted here. Construction does not assert that the Run was admitted; the caller
    supplies a closure it has already had admitted, and the controls in this unit do exactly
    that through the foundation replay fixtures.
    """

    def __init__(self, run, objects, blobs, parameter_row_of=None):
        self.run = run
        self.objects = objects
        self.blobs = blobs
        self.snapshot_id = run["snapshotId"]
        self._evidence = self._get(run["evidenceId"], "semantic-evidence")
        # The identity owner's OWN registry resolution, injected rather than reimplemented, so
        # this module never restates which schema document a parameter row is.
        self._parameter_row_of = parameter_row_of or _default_parameter_row_of()

    def _get(self, key, domain):
        entry = self.objects.get(key)
        if entry is None or entry[0] != domain:
            raise RetainedEvidenceUnavailable(domain + ":" + str(key))
        return entry[1]

    def _blob(self, digest, what):
        raw = self.blobs.get(digest)
        if raw is None:
            raise RetainedEvidenceUnavailable(what + ":" + str(digest))
        return json.loads(raw)

    # -- the retained selected-program census ---------------------------------------
    def enumeration_plan(self):
        """The retained `EnumerationPlanV1`, reached only through guaranteed retained joins.

        run3 -> plan2 -> `analysisSpecDigest` -> the analysis spec -> its `parameters`, then the
        entry whose `schemaDigest` resolves, through the identity owner's own
        `parameter_row_of`, to the registered `foundation/enumeration-plan.schema.v1.json` row.

        This parameter is REQUIRED for evaluator3, not optional and not caller-supplied:
        `evaluator_input_model.v3.required_parameters` refuses
        `EVALUATOR_REQUIRED_PARAMETER_MISSING` without it, and full replay re-admits it. There
        is no optional unsigned map here, no sidecar and no filename parsing.
        """
        plan = self._get(self.run["planId"], "plan")
        spec = self._blob(plan["analysisSpecDigest"], "analysis-spec")
        rows = [item for item in spec.get("parameters", [])
                if self._parameter_row_of(item["schemaDigest"]) == ENUMERATION_PARAMETER_ROW]
        if len(rows) != 1:
            # `admit_parameter_selection` already refuses two entries resolving to one row, so
            # this is a typed unavailability, never a silent pick between candidates.
            raise RetainedEvidenceUnavailable(
                "enumeration-plan-parameter:" + str(len(rows)) + "-rows")
        return self._blob(rows[0]["payloadDigest"], "enumeration-plan")

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


def binding_applicable_paths(binding):
    """The APPLICABLE PATH CENSUS of one retained program binding, per extent kind.

    This is the binding's own declared census and nothing wider. Each `KindExtentV1` is read as
    itself, so file/package HOST extents and the semantic SYMBOL program extent stay distinct
    and are reported separately:

      * `file`    -- the scoped inventoried first-party membership extent of that cell/binding.
      * `package` -- first-party manifests only.
      * `symbol`  -- the SELECTED PROGRAM's code scope: owner-admitted `programRootFiles`,
                     syntax code suffixes, or Rust `sourceUnitOwnership` selected paths when the
                     universe is available; the membership-fallback code extent when it is not.

    All snapshot files are therefore NOT treated as every compiler's `programRootFiles`: a
    binding contributes only the paths its own extents declare. `candidateSourcePaths` is the
    Plan-selected census of a candidate-only cell and counts the same way.
    """
    out = {}
    for extent in binding.get("extents") or []:
        for path in extent.get("paths") or []:
            out.setdefault(path, set()).add(extent.get("kind"))
    for path in binding.get("candidateSourcePaths") or []:
        out.setdefault(path, set()).add("candidateSourcePaths")
    return out


def selected_program_owners(view, paths):
    """RS-2b. The SELECTED-PROGRAM path owner census, from the retained EnumerationPlan.

    WHY THE ENUMERATION PLAN AND NOT COVERAGE SCOPES. `enumeration-contract.v1.md` publishes the
    program-to-path relation directly: an AVAILABLE binding carries a non-null `universe` and
    `extents[]` (§1); a candidate-only cell's available binding must carry
    `candidateSourcePaths`, "the Plan-selected source-path census for THAT program" (§1); an
    UNAVAILABLE binding has `universe=null` yet "`extents` still populated from host membership
    so expected file/package paths are not lost" (§1); and the symbol extent is the selected
    program's code scope (§5, §8). A source-path Coverage scope can only witness ownership that
    this census already carries, and only when such a scope happens to exist in this Run.

    Returns (available, unresolved, owned):
      * `available`  -- {universe: [provenance rows]} for bindings with a non-null universe.
      * `unresolved` -- rows for SELECTED but UNAVAILABLE bindings (`universe=null`) whose
        retained extent contains an unsafe path. These hold a real retained EXPECTED ownership
        claim with no universe to make eligible and no Coverage to establish a closed world, so
        the caller must turn them into a typed not-established outcome. They must NOT vanish
        because some other owner of the same path is closed.
      * `owned`      -- the set of paths any selected binding claimed at all.

    DO NOT INFER UNSELECTED PROGRAMS. A binding whose `enumerator.status` is `unselected`
    (lawful only for an optional unavailable cell, §1) is not a selected program and never
    contributes here, in either bucket.

    Legitimate MULTIPLE ownership is preserved: one physical path analysed under two Rust
    targets or editions is two different selected bindings with two universes, and both are
    returned, so both must be eligible.
    """
    plan = view.enumeration_plan()
    wanted = set(paths)
    available, unresolved, owned = {}, [], set()
    for cell_ordinal, cell in enumerate(plan.get("cells") or []):
        for binding in cell.get("programBindings") or []:
            if (binding.get("enumerator") or {}).get("status") != "selected":
                continue
            census = binding_applicable_paths(binding)
            for path in sorted(wanted & set(census), key=lambda p: p.encode()):
                owned.add(path)
                row = {"via": "unsafe-edit-path", "path": path,
                       "capabilityId": cell.get("capabilityId"),
                       "cellOrdinal": cell_ordinal,
                       "programOrdinal": binding.get("ordinal"),
                       "extentKinds": sorted(census[path]),
                       "provenance": binding.get("provenance")}
                universe = binding.get("universe")
                if universe is None:
                    unresolved.append(dict(row, via="unsafe-edit-path-unavailable-binding",
                                           deficiency=binding.get("deficiency"),
                                           nativeCause=binding.get("nativeCause")))
                else:
                    available.setdefault(universe, []).append(row)
    return available, unresolved, owned


def source_path_scope_witnesses(view, paths):
    """ADDITIONAL retained witness only. Never an owner-completeness certificate.

    Retained source-path subject scopes do name paths, so a universe they witness is a real
    retained ownership observation and is unioned in. It cannot certify completeness: a selected
    program with no source-path scope in this Run owns its extent just the same, which is
    exactly the case `selected_program_owners` exists to cover. Whether these witnesses are
    redundant with the census in a given Run is reported, never assumed.
    """
    found = {}
    for sid, scope in sorted(view.subject_scopes().items()):
        if scope["relation"] not in SOURCE_PATH_RELATIONS:
            continue
        if scope["snapshotId"] != view.snapshot_id:
            continue
        subjects = set(scope["subjects"])
        for path in paths:
            if path in subjects:
                found.setdefault(scope["sourceUniverse"], []).append(
                    {"via": "source-path-scope-witness", "path": path,
                     "relation": scope["relation"], "resolution": scope["resolution"],
                     "scopeId": sid}
                )
    return found


def relevant_universes(view, targets, edits):
    """RS-2. U* = universes of all target occurrences UNION universes owning any unsafe path.

    A universe in neither set is TRULY UNRELATED and does not veto. That scoping is the whole
    reason an unrelated closed finding cannot justify deleting a path analysed in an open
    universe, and equally the reason an unrelated open universe cannot block a plan. A selected
    program whose own applicable path census does not include the edit stays unrelated.

    Ownership comes from the retained selected-program census; source-path scopes are unioned
    in as an additional witness. Whether the witnesses added anything beyond the census is
    reported in `witnessOnlyUniverses`, so their redundancy is measured rather than assumed.
    """
    paths = unsafe_edit_paths(edits)
    census, unresolved, owned = selected_program_owners(view, paths)
    witnesses = source_path_scope_witnesses(view, paths)
    sources = {}
    for bucket in (target_universes(view, targets), census, witnesses):
        for universe, why in bucket.items():
            sources.setdefault(universe, []).extend(why)
    # Provenance rows are sorted by their own canonical spelling so the derivation is
    # reproducible whatever order the caller enumerated findings, scopes or edits in.
    sources = {u: sorted(v, key=lambda d: json.dumps(d, sort_keys=True).encode())
               for u, v in sources.items()}
    unowned = [p for p in paths if p not in owned and not any(
        row["path"] == p for rows in witnesses.values() for row in rows)]
    detail = {
        "censusUniverses": sorted(census, key=lambda u: u.encode()),
        "witnessUniverses": sorted(witnesses, key=lambda u: u.encode()),
        "witnessOnlyUniverses": sorted(set(witnesses) - set(census), key=lambda u: u.encode()),
        "unresolvedOwnership": sorted(
            unresolved, key=lambda d: json.dumps(d, sort_keys=True).encode()),
    }
    return sorted(sources, key=lambda u: u.encode()), sources, unowned, paths, detail


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

    Dedupe is by retained `coverage2` IDENTITY, never by relation. ORDER is `SELECTION_ORDER_KEY`
    compared on **UTF-8 encoded bytes**: `relation`, `resolution`, `sourceUniverse`,
    `targetUniverse`, `subjectScopeCommitment`, then the retained `coverage2` identity. The
    sixth member makes the order total even for two records that agree on all five coordinates,
    so it does not depend on input enumeration order.
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
    return sorted(rows.values(),
                  key=lambda r: tuple(r[m].encode("utf-8") for m in SELECTION_ORDER_KEY))


def record_coordinates(row):
    """The exact retained record a remedy names: all five coordinates plus the identity.

    A remedy that named only relation, rung and sourceUniverse could not tell two lawfully
    distinct retained records apart -- they may differ only in `targetUniverse`, in
    `subjectScopeCommitment`, or in nothing but the `coverage2` identity itself. Every member of
    `SELECTION_ORDER_KEY` is therefore spelled out, in that order, and no value is abbreviated.
    """
    return " ".join(m + "=" + str(row[m]) for m in SELECTION_ORDER_KEY)


def display_summary(selected, absent=False):
    """RS-5. The deterministic five-field DISPLAY SUMMARY.

    NOT a native producer record and it does not pretend to be one: a fieldwise reduction may
    combine members no single producer emitted together. NO MEMBER OF IT IS AUTHORITATIVE,
    the boolean included. The authority is the full native selection in `derive`.

    `deadCodeRepairEligible` is the conjunction over the selected records; each enum member is
    the LEAST-CLOSED value present.

    ABSENCE IS INCORPORATED, so the summary cannot read as closed while eligibility is refused
    for a missing relevant universe. When `absent` is set -- some relevant universe retains no
    native Coverage -- the reduction additionally folds in `EMPTY_DISPLAY_SUMMARY`, whose members
    are each the least-closed pole. The boolean therefore becomes false and each enum member
    becomes at least as open as the sentinel's. The summary is still not the gate: it is a
    display that now states the absence instead of hiding it behind the records that do exist.

    With nothing selected at all the same rule yields exactly `EMPTY_DISPLAY_SUMMARY`, so the
    descriptor -- and therefore `repairPlanId` -- is deterministic even with zero native
    Coverage, which is what a create-only plan needs.
    """
    worlds = [r["closedWorld"] for r in selected]
    if absent:
        worlds = worlds + [EMPTY_DISPLAY_SUMMARY]
    if not worlds:
        return dict(EMPTY_DISPLAY_SUMMARY)
    summary = {"deadCodeRepairEligible": all(bool(w["deadCodeRepairEligible"]) for w in worlds)}
    for field, order in DISPLAY_ORDER.items():
        summary[field] = max((w[field] for w in worlds), key=lambda value: order.index(value))
    return {field: summary[field] for field in DISPLAY_FIELDS}


def derive(view, targets, edits):
    """The whole law. Returns the selection, the gate outcome and the display summary.

    `gateActivated` is RS-1. `eligible` is RS-4 and is None when the gate is not activated,
    because a create-only plan asks no eligibility question: lack of closed-world eligibility
    ALONE must never add an unsafe-edit failure to a plan that makes no unsafe edit.
    """
    universes, sources, unowned, paths, ownership = relevant_universes(view, targets, edits)
    selected = select_coverage(view, universes)
    by_universe = {u: [r for r in selected if r["sourceUniverse"] == u] for u in universes}
    uncovered = sorted((u for u, rows in by_universe.items() if not rows),
                       key=lambda u: u.encode())
    unresolved = ownership["unresolvedOwnership"]

    gate_activated = bool(paths)
    unmet = []
    eligible = None
    if gate_activated:
        if unowned:
            unmet.append({
                "code": CLOSED_WORLD_NOT_ESTABLISHED,
                "remedy": "no selected program binding of this Run's retained EnumerationPlan, "
                          "and no retained source-path subject scope, claims "
                          + ",".join(unowned)
                          + "; the analysing universe cannot be reconstructed from retained "
                            "evidence, and it is not guessed. Re-run analysis over a "
                            "configuration that enumerates this path.",
            })
        for row in unresolved:
            unmet.append({
                "code": CLOSED_WORLD_NOT_ESTABLISHED,
                "remedy": "selected program binding cell=" + str(row["cellOrdinal"])
                          + " (" + str(row["capabilityId"]) + ") ordinal="
                          + str(row["programOrdinal"]) + " retains " + row["path"]
                          + " in its " + "/".join(row["extentKinds"])
                          + " extent but is UNAVAILABLE (universe=null, deficiency="
                          + str(row["deficiency"]) + "), so its ownership of this unsafe path "
                          + "is unresolved and no closed world is established for it. Another "
                          + "owner being closed does not discharge it.",
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
                "remedy": "relevant universe sourceUniverse=" + universe + " retains no native "
                          "Coverage record in this Run, so it establishes no closed world; an "
                          "empty evidence subset is not true.",
            })
        defeaters = [r for r in selected if not r["closedWorld"]["deadCodeRepairEligible"]]
        for row in defeaters:
            unmet.append({
                "code": CLOSED_WORLD_NOT_ESTABLISHED,
                "remedy": "native deadCodeRepairEligible is false for the retained record "
                          + record_coordinates(row)
                          + " (reasons: " + ",".join(row["closedWorld"].get("reasons", [])) + "); "
                          + "declare entry points/consumers explicitly and re-run analysis",
            })
        eligible = not unmet

    return {
        "gateActivated": gate_activated,
        "unsafePaths": paths,
        "relevantUniverses": universes,
        "universeSources": sources,
        "ownership": ownership,
        "unresolvedOwnership": unresolved,
        "unownedUnsafePaths": unowned,
        "universesWithoutCoverage": uncovered,
        "selectedCoverage": selected,
        "eligible": eligible,
        "unmetPreconditions": unmet,
        "closedWorld": display_summary(selected, absent=bool(uncovered or unresolved or unowned)),
    }
