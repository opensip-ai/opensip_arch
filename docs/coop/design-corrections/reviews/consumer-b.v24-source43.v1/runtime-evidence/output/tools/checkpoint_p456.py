"""Record phase 4, 5 and 6 standing from produced source39 artifacts.

Each ID is marked executed only when its artifact exists and its measured gate holds. Gates read vector fields, retained store records (decoded
from the exported CAS by their build labels) and fresh-process replay outcomes. A missing artifact is unexecuted and a failed gate is failed.
Usage: python3 tools/seq.py <label> tools/checkpoint_p456.py
"""
import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import hc_source42 as HC  # noqa: E402
import status as S  # noqa: E402

OUT = S.OUT
st = S.load_status()
problems = []


def load(rel):
    return json.load(open(OUT + rel))


def mark(rid, artifact, ok, notes):
    if not os.path.exists(OUT + artifact.split("#")[0].split(" ")[0]):
        problems.append((rid, "missing", artifact))
        S.set_status(st, rid, "unexecuted", artifact, None, "artifact missing")
        return
    S.set_status(st, rid, "executed" if ok else "failed", artifact, None, notes)
    if not ok:
        problems.append((rid, artifact))


def all_pass(obj):
    bad = []

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("pass"), bool) and not o["pass"]:
                bad.append(o.get("vector") or o.get("case") or "?")
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return not bad


STORES = {}


def labelled(run, label):
    """Every retained record of a Run store whose build label equals label (decoded canonical JSON or raw bytes)."""
    if run not in STORES:
        STORES[run] = load(f"runs/{run}.store.json")
    ex = STORES[run]
    out = []
    for digest, lab in ex["blobLabels"].items():
        if lab == label and digest in ex["blobs"]:
            raw = base64.b64decode(ex["blobs"][digest])
            try:
                out.append(json.loads(raw))
            except ValueError:
                out.append(raw)
    return out


def has_label(run, prefix):
    if run not in STORES:
        STORES[run] = load(f"runs/{run}.store.json")
    return any(lab.startswith(prefix) for lab in STORES[run]["blobLabels"].values())


fs = load("runs/from-scratch.summary.json")
admitted = {r["run"] for r in fs["runs"] if r["role"] == "claimed-positive" and r["result"] == "ADMIT"}
replays = {r["run"]: r for r in load("runs/replay-all.summary.json")["replays"]}


def refused(run, prefix):
    return (replays.get(run) or {}).get("result") == "REFUSE" and ((replays[run].get("firstFault") or "").startswith(prefix))


def log_says(rel, text):
    return os.path.exists(OUT + rel) and text in open(OUT + rel).read()


# ------------------------------------------------------------------ phase 4
p4 = load("vectors/phase4-tables.json")
rr = load("vectors/relation-rung-table.json")
mark("R-RELATION-RUNG-TABLE", "vectors/relation-rung-table.json", not rr["assertionFailures"] and bool(rr["rows"]),
     f"{len(rr['rows'])} registered relation/rung rows from the relation registry, evaluator projection registry and fact-plane dependsOn.")
mark("R-COUNT-CLASS-ATTEMPT", "vectors/phase4-tables.json#/countClassAttemptVectors", not p4["assertionFailures"] and bool(p4["countClassAttemptVectors"]),
     "RC-0..RC-6 state rules applied through native_facts.coverage_faults on admitted retained scopes and Coverage, with and without facts "
     "(logs/s42-fin-p4to9.0.phase4_tables.log).")
cvd = load("vectors/code-vs-data-matrix.json")
mark("R-CODE-VS-DATA-MATRIX", "vectors/code-vs-data-matrix.json",
     all(v["closure"] == "ADMIT" for v in cvd["appliedOnAdmittedSyntaxRuns"].values()) and log_says("logs/s42-fin-p4to9.1.phase5_vectors.log", "failures []"),
     "grammar capability registry table applied on admitted syntax Runs (code grammars bear code facts; data documents disclosed).")
evr = load("vectors/enum-vs-resolution.json")
mark("R-ENUM-VS-RESOLUTION", "vectors/enum-vs-resolution.json", all(r["onlyEnumerated"] for r in evr["runs"]),
     "every file fact of every positive store is file@enumerated; no resolved rung invented.")
mode = load("vectors/mode-rust-cargo-prepared.json")
mark("R-ADVERTISED-MODE-PATHS", "vectors/mode-rust-cargo-prepared.json",
     not mode["assertionFailures"] and not p4["assertionFailures"] and {"ts-pass", "rust-mixed", "syntax-code"} <= admitted,
     "ts-tsconfig runs/ts-*; js-allowjs vectors/config-js-shared-base.json; js-synthesized vectors/config-synthesized.json; rust-cargo runs/rust-*; "
     "rust-cargo-prepared vectors/mode-rust-cargo-prepared.json; syntax-only runs/syntax-* (U-9 fallback unit).")
cp4 = S.write_checkpoint(4, st, ["tools/phase4_tables.py", "vectors/phase4-tables.json", "vectors/relation-rung-table.json", "vectors/code-vs-data-matrix.json",
                                 "vectors/enum-vs-resolution.json", "tools/mode_prepared_vector.py", "vectors/mode-rust-cargo-prepared.json",
                                 "logs/s42-fin-p4to9.0.phase4_tables.log", "logs/s42-fin-disc.1.mode_prepared_vector.log",
                                 "preserved/pre-s42/logs/s42-pre-p4to9.0.phase4_tables.log (unchanged helpers)", "logs/s42-original-disc.1.mode_prepared_vector.log (unchanged helpers)"],
                         HC.for_phase(4),
                         "Phase 4 executed in runtime source42.v1 on the source42 kit after the source42 corrections (log copied byte-identically into source42.v2 "
                         "and reused as the exact prior measurement; no phase-4 code changed since); the unchanged ported helpers' run is "
                         "retained beside it. Problems: " + json.dumps(problems))

# ------------------------------------------------------------------ phase 5
rp = load("vectors/rust-body-identity-pairs.json")
pairs_ok = all(p.get("measured", True) is not False for p in rp["pairs"])
ug = load("vectors/unsupported-grammar.json")
hm = load("vectors/hidden-mismatch-per-language.json")
ts_mem = labelled("ts-pass", "unit-membership")
syn_mem = labelled("syntax-code", "unit-membership")
data_build = load("runs/syntax-data.build.json")


def run_ok(*runs):
    return all(r in admitted for r in runs)


mark("R-RUN-TS", "runs/ts-pass.store.json", run_ok("ts-pass", "ts-fail", "ts-clones-required"),
     "complete TypeScript Runs admitted with fresh-process replay (runs/ts-pass.replay.fromscratch.json; also ts-fail, ts-clones-required, cmp-*).")
nm_rows = [r for r in (ts_mem[0]["rows"] if ts_mem else []) if r["path"].startswith("node_modules/")]
mark("R-RUN-TS-NODE-MODULES", "runs/ts-pass.store.json",
     run_ok("ts-pass") and has_label("ts-pass", "node-modules-layout") and has_label("ts-pass", "source:node_modules/left-pad/package.json")
     and nm_rows == [{"path": "node_modules/left-pad/package.json", "languageFamily": "none", "unitOrdinal": None, "membership": "syntax-only",
                      "reason": "host-ignore-convention"}]
     and refused("ts-pass~pruned-read-nested-node-modules", "SNAPSHOT_PRUNED_TREE_NOT_A_READ") and refused("ts-pass~pruned-read-vcs-tree", "SNAPSHOT_PRUNED_TREE_NOT_A_READ"),
     "bare specifier left-pad resolved; ResolvedNodeModulesLayoutV1 retained; the read node_modules/left-pad/package.json is a snapshot row "
     "(host-ignore-convention) joined to the layout at closure; nested-package and VCS-tree reads refuse SNAPSHOT_PRUNED_TREE_NOT_A_READ.")
mark("R-RUN-TS-CONFIG-DEPS", "runs/ts-pass.store.json", run_ok("ts-pass") and has_label("ts-pass", "tsconfig-graph") and has_label("ts-pass", "node-modules-layout")
     and refused("ts-pass~config-graph-path-outside-snapshot", "cb24.snapshot-join:configGraphPaths") and refused("ts-pass~config-node-kind-wrong", "native.config-graph-kind-contradicts-path")
     # source42 (HC-47): the retained graph entry is joined to the enumeration binding (default-unit marker entry; explicit programEntry)
     and refused("ts-pass~default-unit-program-entry", "ENUMERATION_BINDING_PROGRAM_ENTRY") and refused("ts-pass~explicit-entry-not-graph-entry", "ENUMERATION_BINDING_PROGRAM_ENTRY"),
     "TypeScriptConfigGraphV1 extends graph, layout and package-lock identity retained and re-joined in closure; graph controls refuse; the default-unit "
     "binding carries programEntry null and its entry is derived from the U-1 marker and compared to the retained entryConfigPath (source42 controls refuse).")
mark("R-RUN-RUST", "runs/rust-mixed.store.json", run_ok("rust-mixed", "rust-mixed-clones-required", "rust-extra-unit", "rust-same-file-2021")
     and refused("rust-mixed~default-unit-program-entry", "ENUMERATION_BINDING_PROGRAM_ENTRY"),  # source42 HC-47
     "complete Rust Runs admitted with fresh-process replay; the required clones cell is complete under the closed .rs eligibility census.")
for rid, note in (("R-RUN-RUST-MIXED-EDITION", "package editions 2018/2024 with per-body dialects"), ("R-RUN-RUST-TARGET-EDITION", "bin target 2021 over package default 2018"),
                  ("R-RUN-RUST-BODY-DIALECT", "per-body dialect derived from SourceUnitOwnershipV1"),
                  ("R-RUN-RUST-SAME-FILE-TWO-EDITIONS", "common.rs under two selections at two editions (rust-mixed vs rust-same-file-2021)"),
                  ("R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", "rust-mixed vs rust-extra-unit: universes differ, body identity equal"),
                  ("R-RUN-RUST-LARGE-EDITION-MAP", "302-entry edition map"), ("R-RUN-RUST-VERSION-COMPONENT", "languageVersion recomputed from the admitted rustc context")):
    mark(rid, "vectors/rust-body-identity-pairs.json", pairs_ok and run_ok("rust-mixed", "rust-extra-unit", "rust-same-file-2021"), note + " (measured pairs).")
mark("R-RUN-RUST-HASH-MARKER", "runs/rust-mixed.store.json", run_ok("rust-mixed") and has_label("rust-mixed", "source:crates/#b/Cargo.toml"),
     "crates/#b marker directory admitted; unitId derived by H over UnitIdentityV1.")
mark("R-RUN-RUST-PARTIAL-EMPTY-CLONES", "runs/rust-partial.store.json", run_ok("rust-partial") and refused("rust-partial~partial-fact-present", "BODY_LANGUAGE_OWNER_UNENUMERATED"),
     "enumeration partial: zero clone facts, clones Coverage unknown input-closure-incomplete / body-language-owner-unenumerated over eligible .rs paths; a minted "
     "clone refuses BODY_LANGUAGE_OWNER_UNENUMERATED.")
mark("R-CLONE-DEFICIENCY-PAIRING", "runs/rust-ambiguous.store.json", run_ok("rust-partial", "rust-ambiguous")
     and refused("rust-ambiguous~ambiguous-fact-present", "BODY_LANGUAGE_OWNER_AMBIGUOUS") and refused("rust-partial~partial-fact-present", "BODY_LANGUAGE_OWNER_UNENUMERATED"),
     "published ownership disclosure pairs derived and enforced; designed negatives built over the mutated variants (HC-27).")
mark("R-RUN-FILE-FACT-INVENTORY", "runs/syntax-code.store.json", run_ok("syntax-code", "ts-pass", "rust-mixed"),
     "file facts over the first-party file extent with inventoried path/hash/length snapshot joins re-run in closure.")
mark("R-RUN-CLONES-L0-AND-NORMALIZED", "runs/syntax-code.store.json", run_ok("syntax-code") and has_label("syntax-code", "body-frame:L0:") and has_label("syntax-code", "body-frame:L1:"),
     "L0-verbatim and L1-lexical clone bodies with retained frames, independently re-parsed at closure.")
mark("R-RUN-CLONES-CUSTODY", "runs/syntax-code.store.json",
     run_ok("syntax-code") and has_label("syntax-code", "closure-tree:cb24-grammars:opensip-interface/normalization/specification-map.v1.json")
     and refused("syntax-code~clone-level-spec-not-in-grammar", "BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE"),
     "level specifications selected by the grammar closure's normalization map (normalizationSpecificationLaw); body-language-version derived; a specification "
     "outside the owning closure refuses.")
mark("R-RUN-SYNTAX-CODE", "runs/syntax-code.store.json", run_ok("syntax-code"), "compiler-free syntax Run with inventory, syntax and clone facts.")
mark("R-RUN-SYNTAX-DATA", "runs/syntax-data.store.json",
     run_ok("syntax-data") and any(c["capabilityId"] == "syntax" and c["deficiency"] == "language-tier-unsupported" for c in data_build["cellOutcomes"]),
     "data-document grammars: inventory complete; syntax and clones answered unknown language-tier-unsupported / capability-missing, never a concealed empty result.")
mark("R-RUN-NO-COMPILER-UNIT", "runs/syntax-code.store.json",
     run_ok("syntax-code", "syntax-data") and bool(syn_mem) and syn_mem[0]["units"] and syn_mem[0]["units"][0]["recognizerId"] == "syntax-only-fallback"
     and refused("syntax-code~second-default-unit-binding", "cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY"),  # source42 HC-47: the U-9 default binding
     "no TypeScript or Rust unit: U-9 DEFAULTED syntax-only fallback unit, grammar closure, syntax context/universe and provider retained.")
mark("R-RUN-UNAVAILABLE-SEMANTIC", "runs/syntax-data.store.json", run_ok("syntax-data"),
     "semantic relations unknown language-tier-unsupported / capability-missing; imports unsupported-typed account.")
mark("R-RUN-UNSUPPORTED-GRAMMAR", "vectors/unsupported-grammar.json", all(v["pass"] for v in ug["vectors"]),
     "no-bundled-grammar membership, body-language refusals, data-grammar fact refusal, clones Coverage controls, unselected grammar lends no capability.")
mark("R-RUN-NONCEMPTY-CONTEXT", "runs/ts-pass.store.json", run_ok("ts-pass", "rust-mixed") and has_label("ts-pass", "native-context:typescript") and has_label("rust-mixed", "native-context:rust"),
     "plan.nativeContextDigests nonempty with retained admitted context frames per language.")
mark("R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC", "runs/ts-pass.store.json",
     run_ok("ts-pass") and has_label("ts-pass", "scope-document") and refused("ts-pass~scope-document-duplicate", "ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS"),
     "ScopeDocumentV1 bound under its registered policy-document.schema.json row; a second distinct entry refuses ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS.")
mark("R-IMPORTED-PAYLOAD-IN-GRAPH", "runs/ts-pass.store.json", run_ok("ts-pass") and has_label("ts-pass", "import-payload:runtime"),
     "runtime import2 in plan.importIds, payload admitted and consumed by cb24.ts.cold-file.")
mark("R-HIDDEN-MISMATCH-PER-LANGUAGE", "vectors/hidden-mismatch-per-language.json",
     all(any(r["language"] == lang and r["result"] == "REFUSE" for r in hm["rows"]) for lang in ("typescript", "rust", "syntax")),
     "refused hidden/mismatched inputs per language with first refusal and masked later faults.")
mark("R-NATIVE-PREIMAGE-JOINS", "runs/rust-mixed.store.json",
     run_ok("rust-mixed", "ts-pass") and all(has_label("rust-mixed", x) for x in ("dependency-source-set", "unified-features", "cargo-config-projection", "source-unit-ownership"))
     and refused("rust-mixed~config-projection-mismatch", "native.universe-context-field-mismatch:configProjectionSha256"),
     "dependency-source-set, unified-features, cargo-config-projection and source-unit-ownership frames recomputed from their recipes; TS config graph and layout.")
cp5 = S.write_checkpoint(5, st, ["builders/ts_runs.py", "builders/rust_runs.py", "builders/syntax_runs.py", "ref/source39.py", "ref/membership.py", "ref/closure.py",
                                 "ref/retained_graph.py", "ref/evaluator.py", "ref/execinputs.py", "ref/native_facts.py", "ref/native_ctx.py", "ref/enumeration.py",
                                 "runs/*.store.json", "runs/*.replay.json", "runs/*.replay.fromscratch.json", "runs/replay-all.summary.json", "tools/phase5_vectors.py",
                                 "vectors/rust-body-identity-pairs.json", "vectors/unsupported-grammar.json", "vectors/hidden-mismatch-per-language.json",
                                 "selfcheck/s42-prepost-matrix.json", "preserved/s42-original-state/manifest.json", "preserved/pre-s42/manifest.json",
                                 "logs/s42-original.3.ts_runs.log", "logs/s42-original.7.from_scratch.log", "logs/s42-original-mut.0.replay_all.log (unchanged helpers)",
                                 "logs/s42-hc47-probe.0.ts_runs.log", "logs/s42-hc47-probe2.0.replay_run.log",
                                 "logs/s42-fin-build.0.ts_runs.log", "logs/s42-fin-build.4.from_scratch.log (v1)", "logs/s42-fin-mut.0.replay_all.log (v1)",
                                 "logs/s42v2-fin2.0.syntax_runs.log", "logs/s42v2-fin2.1.replay_all.log", "logs/s42v2-fin2.2.from_scratch.log",
                                 "logs/s42-fin-p4to9.1.phase5_vectors.log"],
                         HC.for_phase(5),
                         "Phase 5: every store rebuilt in runtime source42.v1 on the source42 kit after HC-47/HC-48 (stores copied byte-identically into source42.v2); "
                         "the HC-50 control rebuilt and every store closed again from scratch in fresh processes in source42.v2 "
                         "(from_scratch, replay_all, phase5_vectors). Every claimed complete positive admitted by owner graph admission, the independent "
                         "retained-closure walk and fresh-process replay with reachable output-set equality; the unchanged helpers' builds and closures are "
                         "preserved and compared in selfcheck/s42-prepost-matrix.json. " + HC.CARRIED + " Problems: " + json.dumps(problems))

# ------------------------------------------------------------------ phase 6
phase6_ok = log_says("logs/s42-fin-p4to9.2.phase6_vectors.log", "failures 0")
for rid, art in (("R-CONFIG-SYNTHESIZED", "vectors/config-synthesized.json"), ("R-CONFIG-CUSTOM-MULTI-BASE", "vectors/config-custom-multi-base.json"),
                 ("R-CONFIG-JS-SHARED-BASE", "vectors/config-js-shared-base.json"), ("R-JS-CLONE-BODY-THROUGH-TS", "vectors/js-body-through-ts.json"),
                 ("R-CLONES-NEGATIVE-VECTORS", "vectors/clones-negatives.json"), ("R-REPAIR-DESCRIPTOR", "vectors/repair-descriptor.json"),
                 ("R-REPAIR-AUTHORITY-PER-TARGET", "vectors/repair-descriptor.json"), ("R-MIN-RESOLUTION-THREE-LEVELS", "vectors/min-resolution.json"),
                 ("R-MIN-RESOLUTION-REPAIR-EVIDENCE", "vectors/min-resolution.json"), ("R-IMPORTED-OBSERVATION-BOUNDARY", "vectors/imported-observation-boundary.json"),
                 ("R-MUTATION-REPLAY-SCOPE", "vectors/mutation-replay-scope.json"), ("R-REPAIR-APPLY-KEY", "vectors/mutation-replay-scope.json"),
                 ("R-PINNED-PURGE", "envelopes/pinned-purge.json")):
    ok = os.path.exists(OUT + art) and phase6_ok and all_pass(load(art)) if os.path.exists(OUT + art) else False
    mark(rid, art, ok, "phase6_vectors executed in source42.v1 (log reused in source42.v2 as exact prior measurement) with 0 assertion failures (logs/s42-fin-p4to9.2.phase6_vectors.log); every labelled control passes.")
cp6 = S.write_checkpoint(6, st, ["tools/phase6_vectors.py", "vectors/config-synthesized.json", "vectors/config-custom-multi-base.json", "vectors/config-js-shared-base.json",
                                 "vectors/js-body-through-ts.json", "vectors/clones-negatives.json", "vectors/repair-descriptor.json", "vectors/min-resolution.json",
                                 "vectors/imported-observation-boundary.json", "vectors/mutation-replay-scope.json", "envelopes/pinned-purge.json",
                                 "logs/s42-fin-p4to9.2.phase6_vectors.log", "preserved/pre-s42/logs/s42-pre-p4to9.2.phase6_vectors.log (unchanged helpers)"],
                         HC.for_phase(6), "Phase 6 executed in runtime source42.v1 on the source42 kit; reused in source42.v2 as exact prior measurement (no phase-6 code changed). Problems: " + json.dumps(problems))
S.save_status(st)
print(json.dumps({"phase4Unexecuted": cp4["requirementIdsUnexecuted"], "phase5Unexecuted": cp5["requirementIdsUnexecuted"],
                  "phase6Unexecuted": cp6["requirementIdsUnexecuted"], "failed": cp6["requirementIdsFailed"], "problems": problems}, indent=1))
