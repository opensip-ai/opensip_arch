"""source39.v2 helper corrections of this origin's own ported helpers (continuing HC-1..HC-32, which remain history:
HC-1..HC-13 consumer-b.v24, HC-14..HC-32 source39.v1 in preserved/source39-v1/tools/hc_source39.py and still present in the ported code).

Each entry: the original failure and where its bytes/results are retained, the kit selector that answers it, and the correction.
Path/label rebinding of ported tools to this runtime (phase0 runtime label and origin text, checkpoint log labels) is port bookkeeping,
not a helper correction, and is recorded in notes/11-v2-self-audit.md.
"""
HC = {
    "HC-33": ("ref/closure.py close_run + consumers (tools/from_scratch.py, replay_all.py, replay_export.py, tamper_outputs.py, phase5_vectors.py, "
              "phase8_envelopes.py, phase9_graph_query.py, phase9_admission_log.py): output construction and closure validation were not separated. "
              "admit_graph resolved run/plan/seal/evidence/proof and inputs, but no typed-prefix OUTPUT reference (proof.findingIds, "
              "predicateProofs[].subjectId, rule enumerations, finding.subjectId/fingerprint/ruleClosure, evidence typed arrays) was resolved and "
              "admitted before replay; replay compared only out['objects'], the subset its own emitter produced. Original failure: "
              "selfcheck/pre-summary.json - the unchanged v1 code ADMITs all 27 claimed positives (equal to v1's recorded results) while the "
              "independent schema/registry walker refuses every one RETENTION PREIMAGE_MISSING typed-prefix:evaluation-subject "
              "(selfcheck/pre/<run>.walk.json). Selectors: evaluator-composition-contract.v3.md s7 line 74 ('A field declared as a typed-prefix "
              "identity resolves and admits the retained descriptor in its prefix-selected identity domain; checking only bare fields carrying "
              "x-opensip-digest does not close typed-prefix references ... cannot establish complete retention by comparing only an output subset "
              "selected by its own emitter'); identity-and-evidence.md lines 616-617 and 435-439; identity-schemas.v3.json "
              "#/x-opensip-digest-domains/scope/typedPrefixIdentities. Correction: ref/retained_graph.py (independent of builders/evaluator/"
              "closure/digestlaw; derives the required graph from owning schemas, the s3 prefix table, byDomain, domainSets joins, closureMembership, "
              "closureKinds, payload registry and the native/relation retention vocabularies) runs as its own stage after owner graph admission; "
              "replay only when both admit; stage-ordered faults, first refusal and masked stages are reported."),
    "HC-34": ("ref/closure.py replay: no exact reachable output-set equality; extra reachable semantic outputs or unrecomputed references were "
              "invisible when the proof bytes happened to agree. Selectors: evaluator-composition-contract.v3.md s7 line 76 ('Check exact reachable "
              "output-set equality so extra unreferenced semantic outputs cannot masquerade as evaluated findings') and line 328 ('Additional retained "
              "unreachable objects do not become authoritative findings'). Correction: the walker's reachable run3/seal3/evidence3/proof3/finding3/"
              "finding-key2/subject3 set must equal the recomputed set in both directions (SEMANTIC_REPLAY_REACHABLE_OUTPUT_NOT_RECOMPUTED / "
              "SEMANTIC_REPLAY_RECOMPUTED_OUTPUT_NOT_REACHABLE); unreachable retained frames are listed, never counted."),
    "HC-35": ("ref/evaluator.py: subject3 descriptors were emitted only inside mint_finding, so every subject referenced solely by a rule enumeration, "
              "a predicate proof or a deficiency had no retained descriptor in any exported store (all 63 v1 stores; selfcheck/pre-summary.json). "
              "Selector: evaluator-composition-contract.v3.md s7 line 72 ('The retained output set includes every evaluation-subject descriptor "
              "referenced by a rule's selected or unresolved subject enumeration, a predicate proof, a deficiency, or a finding. Retention is "
              "independent of predicate truth and finding emission'). Correction: rule_enumeration keeps the descriptor of every selected and "
              "unresolved subject; evaluate emits the descriptor of every referenced subject3 (cb24.SUBJECT_DESCRIPTOR_UNRESOLVED if one cannot be "
              "resolved). Run/proof/evidence/seal identities are unchanged by this correction (descriptors are referenced, not embedded); stores gain "
              "the missing frames."),
    "HC-36": ("ref/retained_graph.py (introduced by HC-33) resolved every schema-declared typed-prefix value it walked, including values inside "
              "workflow-owned Plan input documents. Original failure: logs/v2-build.4.from_scratch.log - cmp-empty and cmp-budget refused "
              "RETAINED_CLOSURE.RETENTION.PREIMAGE_MISSING at $run.planId.waiverDigest.waivers[0].target.fingerprint (finding-key2): the Plan-selected "
              "WaiverSetV1 targets a fingerprint no finding of that Run produced (all rules disabled; work budget exhausted). Selectors: "
              "evaluator-composition-contract.v3.md s7 line 74 ('Closing these outputs traverses their reference fields'), s5 line 54 (a waiver "
              "target is compared for equality with an occurrence's fingerprint), identity-and-evidence.md lines 597-600 and 627-631 (policy "
              "document and resolved waiver set are admitted by their owning workflow unit's schema admission). Correction: typed-prefix values in "
              "workflows/* documents are recorded as owner-scoped keys (exemptions, class typed-prefix/workflow-owner-scoped-key), never demanded as "
              "retained descriptors; identity, native and foundation record positions are still resolved. The kit does not state this boundary "
              "explicitly (advisory A-v2-1)."),
}
PHASE = {5: ["HC-33", "HC-35", "HC-36"], 9: ["HC-33", "HC-34", "HC-35", "HC-36"]}
CARRIED = ("HC-14..HC-32 (source39.v1) remain in the ported code as prior corrections; their records are preserved at "
           "preserved/source39-v1/tools/hc_source39.py and were re-exercised, not re-made, by this runtime's re-execution.")


def for_phase(n):
    return [f"{k}: {HC[k]}" for k in PHASE.get(n, [])]


def all_entries():
    return [f"{k}: {v}" for k, v in HC.items()]
