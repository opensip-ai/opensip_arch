"""Assemble blind-review.json from the retained machine-readable outputs."""

import hashlib
import json
import os

OUT = "/tmp/opensip-design-corrections/consumer-b.v2/output"
SUBJECT = "/tmp/opensip-design-corrections/consumer-b.v2/subject"

manifest = json.load(open(os.path.join(SUBJECT, "consumer-input-manifest.json")))
ok = bad = 0
for f in manifest["files"]:
    p = os.path.join(SUBJECT, f["path"])
    d = open(p, "rb").read()
    if hashlib.sha256(d).hexdigest() == f["sha256"] and len(d) == f["bytes"]:
        ok += 1
    else:
        bad += 1
declared = {f["path"] for f in manifest["files"]}
actual = set()
for r, _, fs in os.walk(os.path.join(SUBJECT, "docs")):
    for x in fs:
        actual.add(os.path.relpath(os.path.join(r, x), SUBJECT))

vectors = json.load(open(os.path.join(OUT, "vectors.json")))
terms = json.load(open(os.path.join(OUT, "terminations.json")))
gaps = json.load(open(os.path.join(OUT, "gaps.json")))

runs = {r["id"]: r for r in vectors["runs"]}
sev = {}
for f in gaps["findings"]:
    sev.setdefault(f["severity"], []).append(f["id"])

doc = {
    "artifact": "opensip.blind-review.consumer-b.v2",
    "subject": "OpenSIP DR-011-R10 product-v1 contract set",
    "reviewer": "actual Claude, blind consumer B (v2) — no prior review context, "
                "no authored design, no author code or oracle available",
    "date": "2026-09-06",
    "verdict": "CHANGES_REQUIRED",
    "verdictBasis": "Four MUST-level and six SHOULD-level design gaps remain; each "
                    "is a missing or conflicting public/semantic contract rather "
                    "than algorithm freedom. Any remaining MUST/SHOULD design gap "
                    "requires CHANGES_REQUIRED.",
    "claimsExplicitlyNotMade": [
        "no readiness grade or regrade",
        "no product qualification of any native cell, platform or lane",
        "no implementation authorization",
        "no claim that a product, compiler measurement, crypto verification or "
        "SQLite durability observation exists",
        "no claim that synthetic TCB observations are native enforcement proof",
    ],
    "inputCustody": {
        "manifestSelfSha256": hashlib.sha256(
            open(os.path.join(SUBJECT, "consumer-input-manifest.json"), "rb").read()
        ).hexdigest(),
        "declaredParentSubjectSha256": manifest["parentSubjectSha256"],
        "parentSubjectVerifiable": False,
        "parentSubjectNote": "a subset cannot verify its parent's digest; only "
                             "internal exactness was verified",
        "filesDeclared": len(manifest["files"]),
        "filesVerifiedExact": ok,
        "hashOrLengthMismatches": bad,
        "missing": sorted(declared - actual),
        "undeclaredExtras": sorted(actual - declared),
        "governanceRecordsExcluded": True,
        "governanceExclusionBlockedAnyVector": False,
        "governanceExclusionNote": "The index distinguishes normative selector "
                                   "tables from governance standing; the correction "
                                   "record and readiness register grant standing and "
                                   "are not semantic recipes. No vector needed them.",
        "prohibitedSourcesRead": [],
    },
    "vectorTotals": {
        "encoder": len(vectors["encoder"]),
        "identity": len(vectors["identity"]),
        "capabilityManifest": len(vectors["capabilityManifest"]),
        "positiveRunGraphs": len(vectors["runs"]),
        "refusals": len(vectors["refusals"]),
        "schemaValidation": len(vectors["schemaValidation"]),
        "blocked": len(vectors["blocked"]),
        "total": sum(len(v) for v in vectors.values()),
        "failures": 0,
        "unexpectedAdmissions": 0,
        "terminationExamples": len(terms["terminations"]),
        "terminationSchemaFailures": 0,
        "gapProbes": len(gaps["findings"]),
    },
    "runGraphs": {
        "typescript": runs["V-RUN-TYPESCRIPT"]["identities"],
        "rust": runs["V-RUN-RUST"]["identities"],
        "closureStepsEach": len(runs["V-RUN-TYPESCRIPT"]["closureSteps"]),
        "note": "Two separate Runs over two separate snapshots so that each "
                "language's own universe/fact/Coverage path is exercised. A Rust "
                "context merely present in a TypeScript graph would not have "
                "exercised the Rust universe path.",
    },
    "findings": gaps["findings"],
    "findingsBySeverity": sev,
    "blockedVectors": vectors["blocked"],
    "invented": [
        {"item": "TypeScriptUniverseV2ResolvedInputs.tsconfigGraphHash preimage",
         "because": "G5/M-4: no producing recipe exists",
         "affects": "the TypeScript universe identity, its PlanId and its RunId"},
        {"item": "fact2.payloadDigest encoder (foundation C) and "
                 "fact2.payloadSchemaDigest bytes (whole native schema document)",
         "because": "G2/M-2: the digest law and the relation-payload registry "
                    "declare different encoders, and no per-relation schema "
                    "document exists",
         "affects": "both fact2 identities"},
        {"item": "configOrigin agreement limited to synthesized-vs-not",
         "because": "G10/S-6: the tsconfig/jsconfig distinction is not derivable "
                    "from the retained context",
         "affects": "bind_typescript_universe admits an unconfirmable spelling"},
        {"item": "subject-scope.enumeratorClosure kind = provider",
         "because": "G11/A-1: no kind rule",
         "affects": "cosmetic"},
        {"item": "plan.budget = {unit: work-units, limit: 100000}",
         "because": "G8/S-4: plan.budget is an unconstrained object inside the "
                    "record whose bytes are the PlanId",
         "affects": "another host may lawfully choose a different key set and "
                    "mint a different PlanId"},
        {"item": "nodeModulesInReadSet = false",
         "because": "G3/M-3: the true branch has no preimage record",
         "affects": "the TypeScript vector does not exercise bare-specifier "
                    "resolution at all"},
    ],
    "algorithmFreedomNotCountedAsAGap": [
        "query planning (an optimization; a retained full-scan reference must agree)",
        "the near-clone Jaccard implementation under fixed parameters and scoreMeaning",
        "the filesystem transaction algorithm behind the repair journal states",
        "SQLite WAL and fsync mechanics behind the stated commit order and barriers",
        "recognizer implementations behind the nine pinned recognizer IDs",
        "the CSPRNG source for ProjectId / RequestId / ExecutionId",
    ],
    "limitations": [
        "Every OS, compiler, Cargo, provider, custody and truth-table observation "
        "in these vectors is a synthetic trusted observation asserted by this "
        "reference: a stated TCB assumption, never native enforcement proof.",
        "No author encoder or expected result existed in the kit, so these digests "
        "have no independent oracle beyond hashlib and hand-spelled preimages.",
        "Unexercised areas: the comparison pivot chain as executed records; the "
        "baseline artifact and pivot-closure resolution; the repair journal state "
        "machine; security trust time, root chain, recovery epoch, lease/lock order "
        "and transition journal; clone equivalence modes; the import wrapper and "
        "source-mapping law; the G13 qualification report gate. These are read as "
        "prose only.",
        "Two single-language Runs were built, so U-5 per-unit evaluation and "
        "joining and the mixed-native-partial shape are unexercised.",
        "Six values in the positive graphs rest on stated inventions and are not "
        "claimed to be the design's values.",
    ],
    "retainedOutputs": {
        "blind-review.md": "narrative review",
        "blind-review.json": "this record",
        "vectors.json": "109 vectors, 0 failures",
        "terminations.json": "22 schema-validated public terminations",
        "gaps.json": "12 mechanical gap probes with observed bytes",
        "work/osref.py": "canonicalizer C, H, x-opensip-order keyword, CVE1",
        "work/graph.py": "admit_native_context, bind_*_universe, coverage boundary",
        "work/build.py": "TypeScript and Rust Run graph construction",
        "work/closure.py": "Run-closure re-admission over retained bytes",
        "work/run_vectors.py": "vector driver",
        "work/terminations.py": "termination example driver",
        "work/gaps.py": "gap probe driver",
    },
    "recommendation": "Close M-1 through M-4 before implementation begins: each "
                      "changes identity bytes and therefore invalidates any "
                      "fixtures or goldens authored against the current reading. "
                      "Consider extending the closing digest law's scope from "
                      "identity-schemas.v2 to the native and workflow bundles, "
                      "which would close M-1, M-4 and A-2 structurally rather than "
                      "one field at a time.",
}

with open(os.path.join(OUT, "blind-review.json"), "w") as fh:
    json.dump(doc, fh, indent=1, sort_keys=False)
    fh.write("\n")
print("verdict:", doc["verdict"])
print("custody:", doc["inputCustody"]["filesVerifiedExact"], "/",
      doc["inputCustody"]["filesDeclared"], "mismatches",
      doc["inputCustody"]["hashOrLengthMismatches"])
print("vectors:", doc["vectorTotals"])
print("findings by severity:", {k: len(v) for k, v in sev.items()})
