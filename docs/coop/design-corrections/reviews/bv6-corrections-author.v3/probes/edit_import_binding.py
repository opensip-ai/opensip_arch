"""BV6-V3-IMPORT-BINDING: publish the deterministic fingerprint -> imported-subject projection and
correct the non-existent recipe window-demand field."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work')
P = W / 'docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-imported-requirement-law']

proj = collections.OrderedDict()
proj['standing'] = (
    "Normative and CLOSED, and a SELECTED CLARIFICATION rather than a restatement: nothing before "
    "this published how a repair target reaches an imported payload subject. It introduces no new "
    "record and no new field; it names the retained records that already carry the join."
)
proj['theProblemItSolves'] = (
    "RepairPlanDescriptor.targets are FINGERPRINTS - `finding-key2:<64 hex>` - while RuntimeSubject "
    "is keyed by {path, symbol?} and HistorySubject by {path}. They are different vocabularies, and "
    "an earlier revision read the payload maps DIRECTLY by the target string and called the targets "
    "the payload subjects. That silently equated a finding-key identity with a LogicalPath and "
    "skipped a real join."
)
proj['deterministicProjection'] = [
    "1. TARGET -> FINDING. Every target must be a finding of the evidence Run named by "
    "RepairPlanDescriptor.evidenceRunId; repair preview already refuses a target that is not "
    "(REQUEST.PRECONDITION_FAILED, `target fingerprint not in the evidence Run`). This is the "
    "binding to the ORIGINAL evidence Run and it is not weakened here.",
    "2. FINDING -> FINGERPRINT DESCRIPTOR. The `finding-key2` identity is the H identity of the "
    "retained foundation `finding-fingerprint` descriptor, whose retention mode is `preimage`, so "
    "its exact bytes are retained under that digest and are re-hashed at Run closure. The "
    "projection therefore reads a RETAINED record, never a caller assertion.",
    "3. DESCRIPTOR -> SUBJECT KEY. That descriptor carries "
    "`subjectKey = {language, kind, logicalPath, qualifiedName, discriminator}`. `logicalPath` is "
    "the FILE granularity; `kind` together with `qualifiedName` is the SYMBOL granularity.",
    "4a. RUNTIME MATCH. A RuntimeSubject row matches the target when its `path` equals "
    "`subjectKey.logicalPath` AND, when that row carries `symbol`, its `symbol` equals "
    "`subjectKey.qualifiedName`. A symbol-granularity target is therefore served by a symbol-keyed "
    "row; a path-only row serves a file-granularity target. Granularity is preserved, not flattened.",
    "4b. HISTORY MATCH. HistorySubject has NO symbol field, so a row matches when its `path` equals "
    "`subjectKey.logicalPath`. A symbol-granularity target consequently projects to its FILE. That "
    "is a real WIDENING and is DISCLOSED on the outcome (`granularityWidenedToFile`) rather than "
    "silently accepted, because file-level history is coarser than the target the recipe named.",
    "5. AMBIGUITY REFUSES. If more than one payload subject matches one target, the projection is "
    "not deterministic and the host REFUSES rather than choosing; no silent first-match.",
    "6. UNMATCHED IS UNSUPPORTED. A target with no matching subject is unsupported. It never "
    "becomes satisfied, and it is never read as evidence of non-use.",
]
proj['whatItDoesNotDo'] = (
    "It derives no fact, mints no identity, and admits no payload. It is a READ over records the "
    "authenticated importer and the retained Run closure have already admitted, and its result is "
    "the already-admitted projection the reference outcome function consumes."
)
proj['referenceProjection'] = (
    "workflows_model.project_targets_to_imported_subjects implements steps 1-6 over the retained "
    "records and returns the per-target projection that imported_requirement_outcome consumes, so "
    "the join is EXERCISED and joined to its caller rather than only described. It refuses "
    "`native.imported-projection-ambiguous-target` and "
    "`native.imported-projection-target-not-in-evidence-run`."
)
law['targetSubjectProjection'] = proj

ib = law['inputBinding']
ib['targets'] = (
    "RepairPlanDescriptor.targets - the plan's own FINGERPRINTS. They are not a field of "
    "EvidenceRequirement and none is added. They are not payload subject keys either: see "
    "targetSubjectProjection for the deterministic join through the evidence Run's retained finding "
    "and its finding-fingerprint subjectKey, including symbol-versus-file granularity, the disclosed "
    "history widening, ambiguity refusal and unmatched handling."
)
ib['windowDemand'] = (
    "The bounded observation demand is owned by the ADMITTED RECIPE CLOSURE named by "
    "RepairPlanDescriptor.recipe.closureId - a content-addressed, signed contribution closure whose "
    "current-trust disposition repair preview already resolves and whose revocation already "
    "invalidates apply. It is NOT a wire field: RecipeRef carries only contributionId, recipeId, "
    "recipeVersion and closureId, and an earlier revision wrongly spoke of `the admitted repair "
    "recipe's declared observation demand` as though such a field existed. The host projects the "
    "closure-owned deterministic demand into the typed input this reference consumes; the reference "
    "does not re-derive it and does not invent one when it is absent."
)
ib['requiredVersusOptional'] = (
    "the owning rule/recipe evidenceUse declaration (workflows section 5), projected by the host "
    "into a TYPED BOOLEAN input. The reference REFUSES a non-boolean rather than treating a falsy "
    "value as optional, so there is no `unknown` state at this boundary and no default is applied "
    "to one. An earlier revision claimed unknown declarations are read as required while accepting "
    "None and 0 as optional; the claim is withdrawn and the boundary is typed instead. A repair "
    "requirement is NOT automatically identical to policy predicate truth: the policy evaluator's "
    "optional-absence route is its own, under its own stated conditions, and this projection is "
    "related to the owning declaration rather than equated with that route."
)
ib['allVersusAny'] = (
    "RepairPlanDescriptor.evidenceRequirements[].completeness. SELECTED CLARIFICATION, and its "
    "provenance is recorded accurately: the enum `complete | partial-acceptable` already existed, "
    "but its meaning FOR AN IMPORTED REQUIREMENT OVER PLAN TARGETS is chosen here and was not "
    "previously published. `complete` requires EVERY target supported; `partial-acceptable` requires "
    "at least one. An earlier revision said the enum `already means exactly this`, which was a "
    "historical overclaim."
)
law['inputBinding'] = ib
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok')
