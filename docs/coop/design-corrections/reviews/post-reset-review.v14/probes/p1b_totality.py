"""CB4-MUST-1, second half: per-universe Coverage totality. Each `matchOn` coordinate is
probed for whether it is actually load-bearing, rather than trusting the list."""
import copy, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, probe, emit

build = CI.build

# --- the registry decides who owes totality, and only file@enumerated does ----------------
probe("T0-only-file-enumerated-carries-a-totality-row", "check",
      lambda: [n for n, r in M.RELATIONS.items() if "coverageTotality" in r] == ["file"]
              and M.RELATIONS["file"]["coverageTotality"]["rung"] == "enumerated")
probe("T1-matchOn-is-the-four-coverage-key-coordinates-plus-the-snapshot", "check",
      lambda: M.RELATIONS["file"]["coverageTotality"]["matchOn"]
              == ["snapshotId", "relation", "resolution", "sourceUniverse", "targetUniverse"])

# --- positive controls --------------------------------------------------------------------
probe("T2-positive-a-complete-file-scope-with-its-fact-closes-a-run", "positive",
      lambda: M.close_run(*build(relation="file", has_match=True, resolved=True)))
probe("T3-positive-two-universes-each-with-their-own-inventory-fact-close", "positive",
      lambda: CI.two_universe_inventory_view(True))
for rel in ("package", "vcs-change"):
    probe("T4-positive-an-empty-complete-%s-result-is-an-ordinary-finding" % rel, "positive",
          lambda r=rel: M.close_run(*build(relation=r, has_match=False, resolved=True)))

# --- the omission itself --------------------------------------------------------------------
probe("T5-negative-a-complete-file-coverage-cannot-omit-an-inventoried-subject", "negative",
      lambda: M.close_run(*build(relation="file", has_match=False, resolved=True)),
      "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts")
probe("T6-negative-the-same-omission-in-a-grammar-only-repository", "negative",
      lambda: M.close_run(*build(pure_syntax=True, universe_language="syntax", relation="file",
                                 source_path="tool/main.py", has_match=False)),
      "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:tool/main.py")

# --- THE joined case: one universe's fact must not discharge another's obligation ----------
probe("T7-negative-a-second-universes-complete-scope-is-not-paid-by-the-first-fact", "negative",
      lambda: CI.two_universe_inventory_view(False),
      "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts")

# --- each universe coordinate is INDEPENDENTLY load-bearing. The author's case flips both
#     universes together; if the check only compared sourceUniverse, a half-matching fact
#     would still pay. Flip exactly one coordinate at a time and require a refusal.
def half_matching_fact(which):
    run, objects, blobs = None, None, None
    import types
    # rebuild the author's two-universe view but with a fact that agrees on only ONE universe
    src = CI.two_universe_inventory_view
    # replicate inline so only one coordinate is moved
    run, objects, blobs = build(relation="file", has_match=True, resolved=True, source_path="a.ts")
    universe = next(k for k, raw in blobs.items()
                    if raw.startswith(M.FRAME_PREFIX + b"native.semantic-universe.syntax.v2\0"))
    plan = copy.deepcopy(objects[run["planId"]][1]); spec = C.parse(blobs[plan["analysisSpecDigest"]])
    spec["requestedCapabilities"].append({"capabilityId": "inventory", "languageMode": "syntax-only",
                                          "workspaceRoot": ".", "required": True})
    plan["analysisSpecDigest"] = CI.put_blob(blobs, CI.sort_canonical_sets("analysis-spec", spec))
    CI.rekey_plan(objects, blobs, run, plan)
    scope = copy.deepcopy(next(v for d, v in objects.values() if d == "subject-scope"))
    scope.update(sourceUniverse=universe, targetUniverse=universe)
    sid = M.identifier("subject-scope", scope); objects[sid] = ("subject-scope", scope)
    schema = next(v["payloadSchemaDigest"] for d, v in objects.values() if d == "coverage")
    paths = [r["path"] for r in objects[run["snapshotId"]][1]["sourceInventory"]]
    payload = CI.coverage_result(scope, universe, True, blobs, paths)
    admitted = CI.N.admit_coverage_result_v3(payload, scope, [], schema)
    if admitted["result"] != "ADMIT": raise C.AdmissionError("FIXTURE_SECOND_COVERAGE")
    coverage = {"schemaVersion": 2, "scopeId": sid, "payloadSchemaDigest": schema,
                "payloadDigest": CI.put_blob(blobs, payload)}
    cid = M.identifier("coverage", coverage); objects[cid] = ("coverage", coverage)
    vid = objects[run["evidenceId"]][1]["viewIds"][0]; view = copy.deepcopy(objects[vid][1])
    view["scopeIds"].append(sid); view["coverageIds"].append(cid)
    fact = copy.deepcopy(next(v for d, v in objects.values() if d == "fact"))
    fact[which] = universe          # move ONLY one of the two universe coordinates
    fid = M.identifier("fact", fact); objects[fid] = ("fact", fact); view["facts"].append(fid)
    CI.rekey(objects, vid, view, run)
    evidence = copy.deepcopy(objects[run["evidenceId"]][1]); evidence["coverageIds"].append(cid)
    CI.rekey(objects, run["evidenceId"], evidence, run)
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

# ATTEMPT 1 expected COVERAGE_INVENTORY_TOTALITY_OMITS_PATH here and did NOT get it: the
# half-matching fact is refused EARLIER, by `RELATION_UNIVERSE_RULE:same-only`. That is a
# correct and stronger outcome, not a miss - `file` carries universeRule `same-only`, so its
# two universe coordinates CANNOT diverge and the independence of each coordinate is not
# separately observable for this relation. The probe is re-expressed to assert what is
# actually true: the half-matching fact is refused, at the prior law that owns it.
for coord in ("sourceUniverse", "targetUniverse"):
    probe("T8-negative-a-fact-matching-only-%s-is-refused-by-the-prior-same-only-law" % coord,
          "negative", lambda c=coord: half_matching_fact(c),
          "RELATION_UNIVERSE_RULE:same-only")
probe("T8b-file-carries-universeRule-same-only-so-divergence-is-unreachable", "check",
      lambda: M.RELATIONS["file"]["universeRule"] == "same-only")

# --- an `unknown` result with a disclosed deficiency owes nothing --------------------------
probe("T9-the-law-is-conditional-on-complete", "check",
      lambda: "coverage: complete" in M.RELATION_DOCUMENT["x-opensip-relation-registry"]
              ["coverageTotalityLaw"]["whatItDoesNotRequire"])

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-cb4-must-1-totality.json")
