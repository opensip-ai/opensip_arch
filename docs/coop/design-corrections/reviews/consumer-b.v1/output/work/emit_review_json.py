"""Emit blind-review.json from the retained vector results."""
import hashlib
import json
import os

OUT = "/tmp/opensip-design-corrections/consumer-b.v1/output"
SUBJ = "/tmp/opensip-design-corrections/consumer-b.v1/subject"
res = json.load(open(os.path.join(OUT, "vectors", "vector-results.json")))
g = json.load(open(os.path.join(OUT, "vectors", "run-descriptor-graph.json")))
man = json.load(open(os.path.join(SUBJ, "consumer-input-manifest.json")))


def by(i):
    return next(r for r in res["results"] if r["id"] == i)


doc = {
 "artifact": "opensip.dr-011-r10.blind-consumer-review",
 "subjectKit": "consumer-b.v1",
 "reviewer": "actual Claude, fresh blind session (no author model/fixture/"
             "golden/report/prior review consulted)",
 "date": "2026-09-06",
 "verdict": "CHANGES_REQUIRED",
 "verdictBasis": "Five MUST-level gaps each change a committed identity or a "
                 "public termination, so two conforming implementations would "
                 "disagree on run2 for identical source. All are narrow "
                 "completions of otherwise fully specified machinery, not "
                 "design rework.",
 "standing": {
  "grantsReadiness": False, "qualifiesPlatform": False,
  "authorizesImplementation": False, "isIndependentAcceptance": False,
  "note": "Design-reference reconstruction only. Every OS/crypto/SQLite/"
          "provider observation used is a synthetic assumption, never native "
          "enforcement proof."},
 "inputCustody": {
  "manifest": "subject/consumer-input-manifest.json",
  "manifestSha256": hashlib.sha256(open(os.path.join(
      SUBJ, "consumer-input-manifest.json"), "rb").read()).hexdigest(),
  "parentSubjectSha256": man["parentSubjectSha256"],
  "filesDeclared": len(man["files"]), "filesVerifiedExact": 42,
  "hashMismatches": 0, "byteLengthMismatches": 0, "missingFiles": 0,
  "undeclaredFilesPresent": 0, "totalVerifiedBytes": 1951574,
  "consumerSubsetDigestSha256":
      "11a21bb701b00434e97647504c144445de7a3c0355cbf9ba08611e888b27e90a",
  "consumerSubsetDigestRecipe":
      "SHA256 over path||0x00||sha256bytes||0x00 for each declared file, "
      "sorted by path",
  "citedButAbsent": [
   "docs/coop/design-corrections/README.md (correction record / "
   "successor-selector crosswalk, cited by docs/v2/contracts/product-v1/"
   "README.md)",
   "docs/v2/architecture/08-decision-and-readiness-register.md (readiness "
   "register, cited as sole completion checklist)"],
  "absenceAssessment": "Correct for a blind design read; neither may be "
   "consumed for acceptance. Recorded as scoped input custody (S-5b) because "
   "successor-vs-inherited disposition disputes are not adjudicable from these "
   "bytes alone. Did not block reconstruction."},
 "vectors": {
  "total": res["total"], "passed": res["passed"], "bySeries": res["series"],
  "seriesMeaning": {
   "A": "exact admission, canonical encoding, H framing, retained "
        "CAP-MANIFEST-ID-V1",
   "B": "complete minimal positive Run descriptor graph; semantic vs "
        "operational change",
   "C": "refused hidden / mismatched / tampered inputs",
   "D": "public terminations, positive plus negative branch controls",
   "E": "baseline audit, comparison, authorization, registry and inventory "
        "joins",
   "F": "reproducible probes of gaps that force invention"},
  "resultsFile": "vectors/vector-results.json",
  "runGraphFile": "vectors/run-descriptor-graph.json"},
 "positiveRunGraph": {
  "note": "Computed by cb_canonical.py written from prose only. Conditional on "
          "inventions M-1 and M-2 and assumption CB-A1 (M-4). Not an oracle.",
  "schemaErrors": 0, "closureRefusals": 0,
  "identities": {k: g[k] for k in [
      "projectId", "snapshotId", "planId", "scopeId", "factId", "coverageId",
      "viewId", "executionPlanId", "fingerprintId", "findingId", "proofId",
      "evidenceId", "sealId", "runId"]},
  "typescriptUniverseKey": g["universe"],
  "capabilityManifestId": g["plan"]["capabilityManifestId"]},
 "findings": [
  {"id": "M-1", "severity": "MUST", "vector": "F3",
   "title": "subjectScopeCommitment has no producing recipe",
   "selectors": [
    "native-evidence.schemas.v2.json#/$defs/CoverageKeyV2 (required "
    "subjectScopeCommitment)",
    "native-evidence.schemas.v2.json#/$defs/ExaminedUniverseV1 (required "
    "subjectScopeCommitment)",
    "native-evidence.md §0 retains c2-plan-stage-schema.v4.json "
    "$.coverageKey.key[subjectScopeCommitment]",
    "c2-plan-stage-schema.v4.json $.coverageKey.key[4].boundHere = 'SHAPE "
    "ONLY; computation and verification stay deferred (R1-C2-03).'",
    "c2-plan-stage-schema.v4.json $.coverageKey."
    "subjectScopeCommitmentExamples.rule ('EXAMPLE ENCODING for the fixtures "
    "only ... NOT a claim about how a product computes a real subject-scope "
    "commitment')",
    "identity-and-evidence.md §3 auxiliary-digest paragraph (does not include "
    "it)",
    "native-evidence.md §11 identity domains (no member for it)"],
   "impact": "Value enters the Coverage payload digest -> coverage2 -> view2 "
             "-> evidence2 -> seal2 -> run2.",
   "inventionRequired": True,
   "evidence": {"twoPlausibleRecipesDiverge": True,
                "coverage2": by("F3")["observed"]["resultingCoverage2"]},
   "requiredChange": "State the producing recipe in identity §3's "
    "auxiliary-digest list or as a native H domain, and state its relation to "
    "scope2."},

  {"id": "M-2", "severity": "MUST", "vector": "F4",
   "title": "the TypeScript native context is required and identity-bearing "
            "but never defined",
   "selectors": [
    "native-evidence.schemas.v2.json#/$defs/"
    "TypeScriptUniverseV2ResolvedInputs.required[nativeContextId]",
    "native-evidence.schemas.v2.json#/$defs/NativeContextV2 (Rust-only "
    "required fields)",
    "native-evidence.md §2.3 title 'NativeContextV2 (Rust)'",
    "native-evidence.md §11 (only native.context.rust.v2)",
    "identity-and-evidence.md §3 ('typescriptStdlibMerkleRoot and "
    "rustcDevLlvmDigest in native-context schema 2')",
    "native-evidence.md §14 (same claim)"],
   "impact": "Universe key keys fact2/subject-scope/CoverageKeyV2 and "
             "populates plan.nativeContextDigests; typescriptStdlibMerkleRoot "
             "appears in no closed native schema at all.",
   "inventionRequired": True, "evidence": by("F4")["observed"],
   "requiredChange": "Add the closed TypeScript native-context descriptor and "
    "its H domain carrying typescriptStdlibMerkleRoot; correct identity §3 and "
    "native §14."},

  {"id": "M-3", "severity": "MUST", "vector": "F2, F2b",
   "title": "the canonical encoder cannot decide which arrays are sets",
   "selectors": [
    "identity-and-evidence.md §3 'Arrays whose semantics are sets are sorted "
    "and unique by canonical item bytes' (names four exceptions and one "
    "priority array)",
    "policy-document.schema.json#/$defs/PolicyDocumentV1/properties/rules "
    "description 'sorted ascending by ruleId UTF-8 bytes'",
    "policy-document.schema.json#/$defs/RuleProgramV1/properties/rules",
    "workflows-and-surfaces.md §5 'ordered rule programs'",
    "identity-schemas.v2.json#/$defs/execution-plan/properties/stages "
    "(uniqueItems:true yet ordinal-ordered)",
    "identity-schemas.v2.json#/$defs/closure/properties/tree "
    "(uniqueItems:true yet path-ordered)"],
   "impact": "policyDigest -> plan2 and seal2 -> run2 diverges for the same "
             "policy file.",
   "inventionRequired": True, "evidence": by("F2")["observed"],
   "requiredChange": "Either add a per-field ordering table covering every "
    "array in every digest-bearing document, or state one closing default and "
    "mark declared orders machine-readably."},

  {"id": "M-4", "severity": "MUST", "vector": "F1, F1b",
   "title": "resolvedConfigDigest has two admissible spellings",
   "selectors": [
    "admission-and-qualification.md §1.1 'Resolved semantic configuration "
    "contains analysis, components, discovery, policy and evidence values.'",
    "identity-schemas.v2.json#/$defs/semantic-configuration "
    "required=['analysis'], every section required=[]",
    "admission-and-qualification.md §4 'A missing profile is "
    "CONFIG_PROFILE_MISSING'"],
   "impact": "resolvedConfigDigest -> snapshot2, plan2, run2 diverges. Lands "
             "on the zero-config path: is `discovery` absent or {} for a "
             "repository with no config file?",
   "inventionRequired": True,
   "assumptionTaken": "CB-A1: all five sections present.",
   "evidence": by("F1")["observed"],
   "requiredChange": "Make the resolver output shape exact (require all five "
    "sections, or state that empty sections are omitted) and tighten "
    "`analysis` to its post-resolution required set."},

  {"id": "M-5", "severity": "MUST", "vector": "E21",
   "title": "security names public typed details the closed registry cannot "
            "express",
   "selectors": [
    "security-and-lifecycle.md S9.1 ('detail PROFILE_SET.NO_TR_PROFILE_ROLE'; "
    "'refuses PROFILE_SET.CORE_PIN_MISMATCH')",
    "security-and-lifecycle.md S8 ('refuses PROFILE_SET_KEY_NOT_MACHINE_ID')",
    "security-and-lifecycle.md S12 ('PAYLOAD-NOT-ADMISSIBLE (incl. ROOT.*, "
    "ENVELOPE.*, PROFILE_SET.* details)')",
    "public-detail-registry.v1.json $.records",
    "common.schema.json#/$defs/DomainDetailCode",
    "workflows-and-surfaces.md §12 'Owners register stable details before "
    "emitting them; an unknown detail refuses admission.'"],
   "impact": "A host implementing S9.1 literally cannot emit the refusal S9.1 "
             "mandates: the termination is schema-refused.",
   "inventionRequired": False,
   "evidence": {"registeredByFamily": {"ROOT.": 38, "TRANSITION.": 39,
                                       "PROFILE_SET.": 0, "ENVELOPE.": 0},
                "securityOwnedRecords": 180, "totalRecords": 270,
                "schemaRefusesNamedDetail":
                    by("E21")["observed"]["schemaRefusesNamedDetail"]},
   "requiredChange": "Register the PROFILE_SET.* and ENVELOPE.* details, or "
    "state in S12 that they travel as `subject` data under "
    "PAYLOAD-NOT-ADMISSIBLE (which contradicts S9.1's word 'detail')."},

  {"id": "S-1", "severity": "SHOULD", "vector": "F7",
   "title": "the D9 hostTerminationUnion field closure and nullability are "
            "never dispositioned",
   "selectors": [
    "workflows-and-surfaces.md §0 (retains d9-exit-contract.v1.14.json "
    "'class/code/exit table' only)",
    "d9-exit-contract.v1.14.json $.hostTerminationUnion.unknownFieldPolicy = "
    "'reject'",
    "d9-exit-contract.v1.14.json $.hostTerminationUnion.nullabilityPolicy",
    "common.schema.json#/$defs/StepTermination (adds authority, domainDetail, "
    "faultCause)",
    "workflows-and-surfaces.md §8 ('run-id is explicitly null in the "
    "projection's non-authoritative case')"],
   "evidence": by("F7")["observed"],
   "requiredChange": "Add a §0 disposition row naming $.hostTerminationUnion "
    "and stating whether its field closure and nullability rule are retained, "
    "extended or superseded."},

  {"id": "S-2", "severity": "SHOULD", "vector": "F6",
   "title": "two schema-1 root documents disagree on admission",
   "selectors": [
    "security-and-lifecycle.md S9.1 ('the v8 root.schema.json rule set, "
    "preserved with its exact closed schema and semantic rules (RootV1 in the "
    "schema bundle...)')",
    "docs/coop/completion/security-schemas.v8/root.schema.json (bare $ end "
    "anchors)",
    "security/security-lifecycle.schemas.v1.json $.schemas.RootV1 (strict "
    "(?![\\s\\S]))",
    "admission-and-qualification.md §1 end-anchor rule"],
   "evidence": {
    "reachableDivergence": "indexOrigin.url with a trailing newline: v8 "
                           "admits, bundle RootV1 refuses",
    "productSchemaDiscipline": "12 product-successor documents, 335 patterns, "
                               "0 bare $; 3 retained v8 documents, 52 "
                               "patterns, all bare $",
    "probe": by("F6")["observed"]},
   "requiredChange": "Name one document as the admission boundary for schema-1 "
                     "roots."},

  {"id": "S-3", "severity": "SHOULD", "vector": "F5",
   "title": "inventory ordering has no tie-break",
   "selectors": [
    "identity-and-evidence.md §3 'Inventories instead sort by UTF-8 logical "
    "path'",
    "identity-schemas.v2.json#/$defs/snapshot/properties/sourceInventory "
    "(uniqueItems on the Blob object, not on `path`)"],
   "evidence": by("F5")["observed"],
   "requiredChange": "Enforce path uniqueness in the schema or declare a "
                     "tie-break."},

  {"id": "S-4", "severity": "SHOULD", "vector": None,
   "title": "`regeneration-mismatch` is an unregistered detail spelling",
   "selectors": [
    "identity-and-evidence.md §4 'A mismatch is `regeneration-mismatch`'",
    "public-detail-registry.v1.json (identity owns 4 of 270 records; no such "
    "code)"],
   "requiredChange": "Register it or state what carries it."},

  {"id": "S-5", "severity": "SHOULD", "vector": "F8, F9",
   "title": "two by-reference dependencies are not resolvable inside the kit",
   "selectors": [
    "delivery.v4.json $.derivedFrom.operations[17].value.valueEncoding.source "
    "= 'resolved-inputs.v2#planIdContract.canonicalValueEncoding. Eight closed "
    "types, stated encodings, stated constraints.'",
    "docs/v2/contracts/product-v1/README.md lines 4-6 and 51-53"],
   "evidence": {
    "capManifestVerifiable": True, "capManifestConstructible": False,
    "note": "CAP-MANIFEST-ID-V1 reproduced on all seven published vectors "
            "(A17); CVE1 itself is not stated here, so a release builder path "
            "is incomplete from this subset. The host recompute path is "
            "unaffected."},
   "requiredChange": "Restate CVE1's eight closed types in an in-scope "
    "document, or include the owning selector in the consumer subset."},

  {"id": "S-6", "severity": "SHOULD", "vector": "E20",
   "title": "discharged obligations are still written as open",
   "selectors": [
    "security-and-lifecycle.md S9.2 ('the current nine-field, three-operation "
    "workflow schema cannot express a store operation ... (obligation, "
    "Codex)')",
    "invocation-record.schema.json#/$defs/CoreTransitionIntentV1 (11 required "
    "fields, 5 operations)"],
   "evidence": by("E20")["observed"],
   "requiredChange": "Sweep the '(obligation, Codex)' notes across security "
    "S3/S10/S10.2 and native §13 so a blind implementer can tell what is "
    "actually open."},

  {"id": "A-1", "severity": "ADVISORY", "vector": None,
   "title": "rustcDevLlvmDigest is cited one level up from where it lives",
   "selectors": ["identity-and-evidence.md §3", "native-evidence.md §14",
                 "native-evidence.schemas.v2.json#/$defs/ToolchainIdentityV1."
                 "rustcDevLlvmDigest (reached via NativeContextV2.toolchain)"]},
  {"id": "A-2", "severity": "ADVISORY", "vector": None,
   "title": "two textual identifier conventions coexist (<prefix>:<hex> and "
            "sha256:<hex>)",
   "selectors": ["identity-and-evidence.md §3 identifier table",
                 "native-evidence.md §11",
                 "native-evidence.schemas.v2.json#/$defs/CoverageKeyV2 "
                 "(subjectScopeCommitment sha256:-prefixed, sourceUniverse "
                 "bare hex)"]},
  {"id": "A-3", "severity": "ADVISORY", "vector": "B10",
   "title": "cache-key and regeneration-key are byte-identical schemas "
            "separated only by H domain",
   "selectors": ["identity-schemas.v2.json#/$defs/cache-key",
                 "identity-schemas.v2.json#/$defs/regeneration-key"]},
  {"id": "A-4", "severity": "ADVISORY", "vector": None,
   "title": "the finding-fingerprint discriminator array's ordering discipline "
            "is implicit",
   "selectors": ["identity-and-evidence.md §3 ('discriminator is raw SHA256 of "
                 "their canonical JSON string array'; 'declaration-signature "
                 "tokens in grammar order')"],
   "note": "Same class as M-3; stating the array is ordered would settle it."}],
 "invention": {
  "required": [
   "M-1 subjectScopeCommitment recipe",
   "M-2 TypeScript native-context descriptor and domain",
   "M-3 set-vs-ordered classification for PolicyDocumentV1.rules and "
   "RuleProgramV1.rules",
   "M-4 resolved-configuration section-presence rule"],
  "legitimateImplementationFreedom": [
   "query planning (explicitly an optimization that must agree with a retained "
   "full-scan reference)", "provider-internal extraction strategy",
   "storage layout beneath the digest-addressed CAS",
   "retry/backoff scheduling within stated bounds",
   "clone candidate scoring beyond the declared modes",
   "framework recognizer internals",
   "the concrete SQLite schema behind the stated transaction and barrier "
   "obligations"],
  "deferredToQualificationNotDesign": [
   "fsync/SQLite/process-death behaviour", "flock semantics",
   "O_NOFOLLOW/ACL races",
   "sleep-inclusive monotonic behaviour across suspend", "Ed25519 ceremonies",
   "process-group kill bounds", "native compiler measurements",
   "G13 measurement lanes"]},
 "confirmedPositives": [
  {"id": "A17", "claim": "CAP-MANIFEST-ID-V1 implemented from prose reproduces "
   "all seven published committedBytesHex -> capabilityManifestId values and "
   "all seven committedBytesSha256 in delivery.v4.json"},
  {"id": "E19", "claim": "public-detail-registry.v1.json (270 records) and "
   "common.schema.json#/$defs/DomainDetailCode (270 members) are exactly "
   "equal, both sorted, with zero internal-alias leakage"},
  {"id": "E23", "claim": "the §8 SARIF parity MUST holds exactly: "
   "default/analyze/audit/repair-verify each declare all seven common parity "
   "fields, zero omissions"},
  {"id": "A18", "claim": "strict (?![\\s\\S]) end-anchor discipline is "
   "universal across the 12 product-successor schema documents (335 patterns, "
   "0 exceptions)"},
  {"id": "B1,B2", "claim": "a complete minimal positive Run descriptor graph "
   "validates against the normative closed schemas with zero errors and closes "
   "under the identity §3/§4 join rules with zero refusals"},
  {"id": "B7", "claim": "two attempts differing in RequestId, ExecutionId, "
   "wall clock, receipt signer, namespace and commit sequence share one run2, "
   "and no operational token appears anywhere in the sealed closure"},
  {"id": "C1-C7", "claim": "schema-valid, hash-valid hidden facts, unselected "
   "imports, cross-source facts, subset witnesses, tampered witnesses, forged "
   "`verified:true` and forged capabilityManifestId are all refused"},
  {"id": "E1", "claim": "a current-baseline audit with zero entries on both "
   "sides still returns indeterminate when a gating rule's required evidence "
   "was lost"}],
 "limitations": [
  "Every custody, signature, clock, lease, provider-protocol and OS "
  "observation in these vectors is a synthetic assumption, never native "
  "enforcement proof.",
  "Not exercised: provider wire protocol (native §9), clone equivalence modes "
  "(§6), framework recognition (§8), Rust dependency-source/prepared-output "
  "paths (§3), security trust-time state machine (S4/S4.5), lease and "
  "migration state machines (S7/S9), the G13 report gate (admission §2-§3), "
  "HTML/agent rendering. Read for reconstruction and ownership only.",
  "The canonicalizer is one reading of identity §3. Where §3 is ambiguous "
  "(M-3, M-4, S-3) a choice was made and disclosed; a different conforming "
  "reading yields different identities.",
  "Schema validation used jsonschema 4.25.1 under Draft 2020-12 against the "
  "kit's own documents. JSON Schema alone does not establish exact numeric "
  "admission, so a separate lexical layer runs first and is separately "
  "vectored.",
  "Passing 106 self-authored vectors is not independent acceptance, not "
  "product qualification, and not implementation authorization."]}

json.dump(doc, open(os.path.join(OUT, "blind-review.json"), "w"), indent=1)
print("wrote blind-review.json:",
      os.path.getsize(os.path.join(OUT, "blind-review.json")), "bytes")
print("findings:", len(doc["findings"]),
      "MUST:", sum(1 for f in doc["findings"] if f["severity"] == "MUST"),
      "SHOULD:", sum(1 for f in doc["findings"] if f["severity"] == "SHOULD"),
      "ADVISORY:", sum(1 for f in doc["findings"] if f["severity"] == "ADVISORY"))
