import json,hashlib
from pathlib import Path
W=Path('/tmp/opensip-design-corrections/post-reset-review.v19')
def sh(n): return hashlib.sha256((W/'results'/n).read_bytes()).hexdigest()
def ev(n): return {"path":"post-reset-review.v19/results/"+n,"sha256":sh(n)}
r=json.load(open(W/'review.json'))
SRC="docs/coop/design-corrections/reviews/codex-post-reset.v1/successor-source-assessment.v19.json"
SRCH="a055cef9d2b9b5ed08ba10c8bffdeed6693f80fa13c5ee76ef305a0572c05cbc"
def src(sel): return {"path":SRC,"sha256":SRCH,"selector":sel}

d={}
d["CB7-MUST-1"]={"id":"CB7-MUST-1","severity":"MUST","origin":"blind consumer-B v7; reaffirmed STANDS in its own clarification",
 "disposition":"RESOLVED-IN-THESE-BYTES","independentlyVerified":True,
 "sourceBinding":src("/findingDispositions/0"),
 "basis":("47 controls I authored. The law is READ from its owning registry "
  "(identity-schemas.v2.json#/x-opensip-digest-domains/scopeCapabilityLaw and each universe's languageVersionBinding.dialect.table): "
  "the module value EQUALS the registry law, and no suffix->sourceVariant pair is restated anywhere in either executable model, so the "
  "vocabulary has exactly one authority. Longest-match selection is correct including the declaration suffix (.d.ts -> ts-declaration, "
  "never ts). The counterexample that opened the finding - a clones scope over package.json under the TypeScript universe - now yields the "
  "EXISTING language-tier-unsupported / capability-missing pair, with no new deficiency, cause or public detail code. Empty source-path "
  "scopes are unsupported rather than vacuously complete; mixed scopes disclose in both orders; supported .ts/.tsx/.mts/.cts/.js/.jsx/.mjs/.cjs "
  "and .d.ts scopes stay eligible for complete; all three inventory capabilities are ungated even on unlisted suffixes and on empty scopes. "
  "Rust's ownership form has no suffix table, so this law does not own it and BODY_LANGUAGE_OWNER_NOT_COMPILED is untouched; the syntax "
  "universe keeps its own grammar guard, ordered ahead of this backstop."),
 "optionalContextCannotBypassFinalAuthority":("The producer-boundary application is conditional on the caller supplying universe_dialect, "
  "which is disclosed in both the code and the published guardOrder. The final authority is NOT conditional: "
  "coverage_source_variant_prerequisite is called unconditionally at identity-model.py:1560 inside close_run, and the dialect it reads comes "
  "from the RETAINED universe record (identity-model.py:1545-1546), never from the coverage payload. So a provider cannot switch its own "
  "capability on by asserting a flag, and a caller that supplies nothing still meets the closure guard."),
 "actualFirstRefusalAndPrecedence":("Run closure runs the producer admission (line 1547) BEFORE its own prerequisites, so a false complete for "
  "an unsupported source-path clones scope refuses there as native.coverage-source-variant-unsupported-complete. Among closure's own "
  "prerequisites the order is ownership, then syntax grammar capability, then this backstop, so a syntax violation keeps its own name. This is "
  "an INTENTIONAL and published precedence (CX-V19-PRECEDENCE-PUBLICATION); the earlier grammar-first wording that contradicted producer "
  "admission is corrected, and the grammar law is neither weakened nor reordered."),
 "scopeOfMyClaim":("I verified the reference model's admission logic and its Run-closure wiring by execution. I did NOT execute a compiler, "
  "parser, provider or host, and I make no claim of host/compiler enforcement or of a fully admitted product Run."),
 "evidence":[ev("ctrl-a.json"),ev("ctrl-c.json")]}

d["CB7-SHOULD-2"]={"id":"CB7-SHOULD-2","severity":"SHOULD","origin":"blind consumer-B v7; STANDS with two self-corrections in its clarification",
 "disposition":"RESOLVED-IN-THESE-BYTES","independentlyVerified":True,
 "sourceBinding":src("/findingDispositions/1"),
 "basis":("56 direct plus 14 ACTUAL-INVOCATION controls. The three bounds are READ from the schema (128/128/256) and PLAN_SELECTION_FIELDS "
  "equals the $defs/plan declaration order. At limit+1 each field reaches PROJECT.SCOPE_LIMIT with subject {field,count,limit}, d9 "
  "request-rejected / REQUEST.UNSATISFIABLE / exit 2, and its OWN narrowing remedy (three distinct remedy sentences). Exactly-at-limit, "
  "below-limit and empty arrays are admitted."),
 "actualArrayOnlyCardinality":("Only an actual list over its bound refuses. A 500-char string, a 500-key dict, null, bool, int, float and a "
  "tuple all pass through as the SAME OBJECT, so length-of-a-string is never reported as a member count; a missing field and an in-bound array "
  "of wrong element types are the schema's. An OVER-bound array of wrong element types still refuses on cardinality."),
 "multiFieldPrecedence":("With all three oversized the subject is semanticClosures; with closures in bound it is nativeContextDigests; Python "
  "insertion order does not change it; an earlier field of the WRONG TYPE does not mask a later breach; five repetitions yield one subject."),
 "actualInvocationWiringNotAnOrphan":("admit_plan_selection_cardinality is called INLINE in the prospective Plan construction at "
  "integration-fixtures.py:725 and check-identity.py:770, immediately before add('plan',...), so a refusal structurally precedes minting. "
  "Driving the owning checker's real build() with 257 importIds refuses with importIds:257>256, exit 2, and returns NO planId and NO objects; "
  "256 importIds still closes a Run. It is additionally accounted at the earlier PRODUCER boundary: plan_native_context_digests refuses 129 "
  "DISTINCT contexts before any prospective Plan exists, admits exactly 128, and collapses 129 identical descriptors to one."),
 "earlierCommittedOutcomesPreserved":("An ordinary invocation before and after the refusal is byte-identical (same canonical Run hash, same "
  "planId), and the at-limit positive is repeatable after a refusal."),
 "retainedOversizedPlanIsCorruption":("An externally retained Plan over its bound refuses on the SCHEMA route, NOT as a prospective request "
  "rejection, and admit_plan_selection_cardinality appears nowhere in identity-model.py, so retained Run closure cannot take the request route."),
 "evidence":[ev("ctrl-b.json"),ev("ctrl-c.json")]}

d["CB7-SHOULD-1"]={"id":"CB7-SHOULD-1","severity":"SHOULD","status":"WITHDRAWN","disposition":"WITHDRAWN-BY-ORIGINAL-REVIEWER-AND-INDEPENDENTLY-CONFIRMED-UNFOUNDED",
 "sourceBinding":src("/withdrawnFinding"),
 "withdrawalEvidence":{"path":"docs/coop/design-corrections/reviews/consumer-b.v7-clarification.v1/output/clarification.json",
   "sha256":"a409b4a01e598e21aae032059f0875c4897df617ca82a03e522715200d8aea00","selector":"/item2_repairCauseCarrierReassessment",
   "verified":"I rehashed this file in the frozen snapshot; it matches."},
 "rootAssessment":{"path":"docs/coop/design-corrections/reviews/codex-post-reset.v1/blind-assessment.v7-clarification.v1.json",
   "sha256":"6b46dbbef63ade7ac9151ad98973168991c8a72c33c689a707db1be742ba4ca3","verified":"rehashed, matches"},
 "basis":("The original premise imposed unmetPreconditions[].code == the deficiency token, which no contract states. The original reviewer "
  "retracted it IN FULL in its own clarification ('RETRACTED IN FULL'). I confirmed the premise is unfounded against the bytes: the deficiency "
  "is admitted SEPARATELY (plane, deficiency = admit_evidence_requirement(req)) and is projected into the REMEDY text, and no member of the "
  "native deficiency vocabulary is ever minted as a detail code - every emitted code stays in the pre-existing REPAIR namespace."),
 "notRepresentedAs":("This is NOT original blind acceptance of v19, and NOT a revival of the 11-new-code premise. The clarification states it "
  "cannot accept a future source fix, which needs a newly frozen candidate and a fresh independent blind."),
 "evidence":[ev("ctrl-e.json")]}

d["CX-V19-REPAIR-PROJECTION-MAPPING"]={"id":"CX-V19-REPAIR-PROJECTION-MAPPING","severity":"SHOULD","origin":"root/code-owner repair projection clarification",
 "disposition":"RESOLVED-IN-THESE-BYTES","independentlyVerified":True,"sourceBinding":src("/findingDispositions/5"),
 "basis":("22 controls. The decisive fact is that the repair preview emission body is BYTE-IDENTICAL to pre-v19: the ONLY v19 change to "
  "workflows_model.v1.py is the five-line subject copy. The S6 paragraph therefore BROADENS PUBLISHED MEANING TO MATCH UNCHANGED MODEL "
  "BEHAVIOUR and asserts no new behaviour."),
 "perRequirementEmissionIsMandatory":("if not req['satisfied'] emits unconditionally - no flag and no option - so schema-only permissiveness "
  "is NOT normative optionality: an unsatisfied requirement with empty unmetPreconditions is decided non-conforming at ADMISSION, exactly as the "
  "paragraph states."),
 "existingCodeOnly":("Exactly two routes inside preview reach the ONE existing REPAIR.EVIDENCE_RUN_UNAVAILABLE code, and the emitted code set is "
  "identical to pre-v19. No per-deficiency detail code is minted; EvidenceRequirement.deficiency remains the typed cause carrier."),
 "causeFieldsOnlyOnThatEntry":("The RETENTION entry's remedy names Run-level restoration and carries NO relation, minResolution, plane or "
  "deficiency. The PER-REQUIREMENT entry's remedy names all four. So per-requirement cause fields are required only on that entry, never on the "
  "retention remedy - the exact distinction the clarification draws."),
 "authorityPreserved":("Authoritative applicability is unchanged (applicable == not unmet; a non-authoritative or ephemeral Run still refuses "
  "REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE), and the exact authorization binding is preserved because any edit to the descriptor mints a different "
  "repairPlanId that no authorization names."),
 "evidence":[ev("ctrl-e.json")]}

d["CX-V19-PROTOCOL-INITIALIZATION-PUBLICATION"]={"id":"CX-V19-PROTOCOL-INITIALIZATION-PUBLICATION","severity":"SHOULD",
 "disposition":"RESOLVED-IN-THESE-BYTES","independentlyVerified":True,"sourceBinding":src("/findingDispositions/4"),
 "basis":("21 controls, 423 behavioural cases, 25 permutation sweeps. The decisive control is that I wrote an INDEPENDENT interpreter from the "
  "PUBLISHED DOCUMENT ALONE - its initializationAndUpdateOrder, matchLaw, preMatchLaw, noMatchLaw, guardLaw, stateUpdates, "
  "stageDependentTransitions and terminalLaw - and it reproduces protocol3_run EXACTLY on all 423 cases: four mode combinations, multi-stage "
  "CoverageV3 resolution and one-stage-short, all five terminal kinds, every process fault, FAULT absorption, post-terminal frames, unknown and "
  "out-of-order frames, and 400 seeded fuzz sequences over the published frame vocabulary. That is what 'directly consumable' means operationally."),
 "structure":"34 ordered rows P3-01..P3-34, 22 phases, the exact nine-field initialState, *PRE_COMPLETE equal to its published derivation phases[1:17], and the *PROCESS_FAULT frame set.",
 "consumedNotCopied":"The model READS the artifact: PROTOCOL3_RULES and PROTOCOL3_PHASES equal the published values and no P3-xx row literal remains in the model source.",
 "noSilentlyAlteredBehaviour":("I exec'd the PRE-v19 inline table segment out of source-before-v19 and compared: the published rows, phases, "
  "phases[1:17] derivation, process-fault set and the now-DERIVED _SOURCE_FRAMES are all byte-equal to the pre-v19 values. The table adds no "
  "frame, phase or terminal."),
 "matchLawAndDisjointness":("I proved pairwise disjointness myself over the non-*ANY rows (accounting for *PRE_COMPLETE membership and mutually "
  "exclusive guards): zero overlapping pairs. 25 random permutations of the rows preserve every outcome on 60 cases, confirming that first-match "
  "position resolves no ambiguity today while remaining the declared normative rule."),
 "honestLimit":("My interpreter takes IDENTITY_TOKENS from the model, because the document declares the identity token set PROSE-OWNED "
  "(section 9.1). That is a declared division, not a gap - but a kit reader needs the contract prose as well as the table."),
 "evidence":[ev("ctrl-d.json")]}

d["CX-V19-PRECEDENCE-PUBLICATION"]={"id":"CX-V19-PRECEDENCE-PUBLICATION","severity":"SHOULD","disposition":"RESOLVED-IN-THESE-BYTES",
 "independentlyVerified":True,"sourceBinding":src("/findingDispositions/2"),
 "basis":("I read the actual control flow rather than the prose. close_run runs the producer admission at identity-model.py:1547, then "
  "coverage_dialect_prerequisite (1551), syntax_capability_prerequisite (1552) and coverage_source_variant_prerequisite (1560). The corrected "
  "native contract and the registry's guardOrder now state exactly that: producer first, then ownership/grammar/suffix. An honestly disclosed "
  "unsupported scope is ADMITTED at both boundaries and closes its Run carrying onUnsupportedScope; only a false or mismatched claim refuses."),
 "evidence":[ev("ctrl-a.json"),ev("ctrl-c.json")]}

d["CX-V19-CONTEXT-AND-PLAN-ORDER"]={"id":"CX-V19-CONTEXT-AND-PLAN-ORDER","severity":"SHOULD","disposition":"RESOLVED-IN-THESE-BYTES",
 "independentlyVerified":True,"sourceBinding":src("/findingDispositions/3"),
 "basis":("Two corrections, both checked. (1) Context identity: the contract now states that two units collapse EXACTLY WHEN their entire "
  "admitted context descriptor is identical, naming configProjection (including configGraphPaths), moduleResolutionMode, packageModuleType, "
  "nodeModulesLayoutDigest and lockfileIdentity, and says sharing a compiler closure and stdlib is necessary and NOT sufficient. This is the "
  "correction of the overbroad retained-config-graph claim. (2) The 'generic exception' wording: the earlier text claimed a jsonschema maxItems "
  "error 'names no field, no count and no limit'. I ran jsonschema myself - the error DOES carry json_path '$.a', validator 'maxItems' and "
  "validator_value 3 - so the retracted wording was factually wrong and the corrected wording ('carries no typed scope projection ... even though "
  "its own structured fields do identify the failing path and the bound') is accurate. The declaration-order claim is now correctly scoped to the "
  "prospective-Plan boundary."),
 "evidence":[ev("ctrl-b.json"),ev("ctrl-e.json")]}

d["CX-V19-WORKFLOW-SUBJECT-PROJECTION"]={"id":"CX-V19-WORKFLOW-SUBJECT-PROJECTION","severity":"SHOULD","disposition":"RESOLVED-IN-THESE-BYTES",
 "independentlyVerified":True,"sourceBinding":src("/findingDispositions/6"),
 "basis":("The projection copies an explicitly supplied subject by PRESENCE, not truthiness. An absent subject yields byte-identical output to "
  "pre-v19 (strictly additive); a detail-less observation still carries no domainDetail at all; an explicit EMPTY string is preserved, which the "
  "published BoundedText admits. I also confirmed the root's correction of the coauthor's narrower claim: False, 0, [] and {} are preserved too, "
  "not just None/empty. The subject is COPIED, never ADMITTED - a 2000-char subject and each falsey shape are refused by the SCHEMA. End to end, "
  "a real native ScopeRefusal's importIds:257>256 survives into the workflow envelope with class request-rejected and exit 2."),
 "evidence":[ev("ctrl-e.json")]}

ADVS={"CB7-ADV-1":("D9 successor faultCause obligation","I measured both enums at their owning locations: the inherited "
  "docs/coop/artifacts/d9-exit-contract.v1.14.json carries 11 members and the successor common.schema.json#/$defs/D9FaultCause carries 12. "
  "Exactly one member is added - host-invariant - with no removals, and the inherited artifact remains historical and still omits it. This "
  "confirms the 11->12 comparison the blind itself corrected to in its clarification; the original review's '10->12' mixed a non-none count "
  "with a total. Substance unaffected."),
 "CB7-ADV-2":("Matrix-fixed default cannot express 94..1024-unit TypeScript repositories","Arithmetic confirmed against the published bound of "
  "1024: 93x11 = 1023 (one row UNDER the bound, not at it) and 94x11 = 1034. The typed refusal it names is real - an over-bound capability "
  "selection refuses with subject requestedCapabilities:1025>1024."),
 "CB7-ADV-3":("PLATFORM-ID-DOMAIN-V1 is broader than the four-platform promise","Measured at native/capability-manifest-domains.v2.json#"
  "/registries/PLATFORM-ID-DOMAIN-V1: memberCount 8 and 8 listed members, of which four are the selected macOS/Linux machine platform ids. The "
  "registry itself discloses that the inherited delivery vocabulary is deliberately broader, and it is bound only at "
  "ProviderCapability.platformIds[]."),
 "CB7-ADV-4":("PROTOCOL3_RULES is named, not published","This is the advisory v19 ACTS ON. The 34-row table is now a published artifact that the "
  "contract cites by path and the model consumes; the standalone 'the table is PROTOCOL3_RULES in the model' wording is gone. Substantively "
  "addressed - see CX-V19-PROTOCOL-INITIALIZATION-PUBLICATION. I raise CX-CL19-ADV-1 because kit INCLUSION is still a future assembly act."),
 "CB7-ADV-5":("UNICODE_CASE_DATA_VERSION is a prose constant","Confirmed: the pinned constant is 15.0.0 and the contract states the portability "
  "limitation itself. The advisory's own reasoning stands - current lib names are ASCII, where the candidate fold operations coincide, so no "
  "vector discriminates U+0130, Final_Sigma or U+00DF.")}
for k,(t,b) in ADVS.items():
    d[k]={"id":k,"severity":"ADVISORY","title":t,"disposition":"CARRIED-INDEPENDENTLY-REMEASURED" if k!="CB7-ADV-4" else "SUBSTANTIVELY-ADDRESSED-IN-THESE-BYTES",
     "independentlyVerified":True,"sourceBinding":src("/findingDispositions"),
     "originalSeverityPreserved":True,"basis":b,"evidence":[ev("ctrl-f.json")]}
r["priorFindingDispositions"]=d
r["priorFindingAccounting"]={"total":len(d),"must":1,"should":6,"withdrawn":1,"advisories":5,
 "unresolvedMust":0,"unresolvedShould":0,
 "note":("Every v19 source finding is accounted individually, plus the withdrawn CB7-SHOULD-1 as withdrawn and all five CB7-ADV. "
  "Prior reviews are historical: the v18 ACCEPT and every earlier verdict bind their own frozen bytes, not these.")}
json.dump(r,open(W/'review.json','w'),indent=1)
print('findings',len(d),'total keys',len(r))
