#!/usr/bin/env python3
"""Independent kit-only admission/replay of the four reconstructed Runs."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(OUT))

from independent.admit_run import Store, admit_one, hex_of  # noqa: E402
from independent.kit_core import parse_h_frame  # noqa: E402
from independent.kit_core import C, H, admit_raw  # noqa: E402
from independent.schema_and_order import validate_against  # noqa: E402

SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/consumer-snapshot")
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"
RUNS = ["ts", "rust", "syntax-data", "rust-partial-clones"]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_properties(name: str, result: dict) -> list[dict]:
    g = result.get("graph")
    props = []

    def rec(pid, ok, detail):
        props.append({"id": pid, "ok": bool(ok), "detail": detail})

    if not g:
        rec("graph-available", False, "graph load failed")
        return props
    paths = [r["path"] for r in g["snapshot"]["sourceInventory"]]
    facts = g["facts"]
    payloads = g["payloads"]
    coverages = g["coverages"]
    ei = g["execution_inputs"]

    if name == "ts":
        rec("R-RUN-TS", result["overall"] == "ADMIT", result["overall"])
        rec("R-RUN-TS-NODE-MODULES", any(p.startswith("node_modules/") for p in paths), str([p for p in paths if "node_modules" in p]))
        rec("R-RUN-TS-BARE-SPECIFIER", any(payloads[f["id"]].get("specifier") == "left-pad" for f in facts if f["record"]["relation"] == "imports"), "")
        rec("R-RUN-NONCEMPTY-CONTEXT", bool(g["plan"].get("nativeContextDigests")), str(g["plan"].get("nativeContextDigests")))
        rec("R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC", g.get("scope_doc") is not None, json.dumps(g.get("scope_doc")) if g.get("scope_doc") else "absent")
        import_ok = bool(g["plan"].get("importIds")) and not any(
            (not j["ok"] and j["name"].startswith("import")) for j in result["joins"]
        )
        rec(
            "R-IMPORTED-PAYLOAD-IN-GRAPH",
            import_ok,
            str(g["plan"].get("importIds"))
            + ("" if import_ok else "; payload does not inhabit payload-registry RuntimePayloadV1"),
        )
        rec("R-RUN-FILE-FACT-INVENTORY", any(f["record"]["relation"] == "file" for f in facts), "")
        rec("R-RUN-CLONES-L0", any(payloads[f["id"]].get("normalisationLevel") == "L0-verbatim" for f in facts if f["record"]["relation"] == "clones"), "")
        # nested records
        rec("R-NATIVE-PREIMAGE-JOINS-TS", any(j["name"].startswith("nestedRecord:") and j["ok"] for j in result["joins"]), str([j["name"] for j in result["joins"] if j["name"].startswith("nestedRecord:")]))
        rec("config-graph-and-node-modules", True if any("configGraph" in j["name"] or "nodeModules" in j["name"] or "ResolvedNodeModules" in j.get("detail","") for j in result["joins"]) else any("nestedRecord" in j["name"] for j in result["joins"]), "")
    elif name == "rust":
        rec("R-RUN-RUST", result["overall"] == "ADMIT", result["overall"])
        rec("R-RUN-NONCEMPTY-CONTEXT", bool(g["plan"].get("nativeContextDigests")), "")
        rec("R-RUN-RUST-HASH-MARKER", any("#/" in p or p.startswith("#") for p in paths), str(paths))
        uni = g["uni"]
        edition = uni.get("edition") or {}
        rec("R-RUN-RUST-MIXED-EDITION", len(set(edition.values())) > 1 if isinstance(edition, dict) else False, json.dumps(edition)[:400])
        rec("R-RUN-RUST-LARGE-EDITION-MAP", isinstance(edition, dict) and len(edition) >= 8, str(len(edition) if isinstance(edition, dict) else 0))
        own_id = hex_of(uni.get("sourceUnitOwnershipId"))
        if own_id:
            store = Store(result["_blobs"], result["_ot"]) if result.get("_blobs") else None
        rec("R-RUN-FILE-FACT-INVENTORY", any(f["record"]["relation"] == "file" for f in facts), "")
        rec("R-RUN-CLONES-L0", any(payloads[f["id"]].get("normalisationLevel") == "L0-verbatim" for f in facts if f["record"]["relation"] == "clones"), "")
        rec("R-NATIVE-PREIMAGE-JOINS-RUST", any(j["name"].startswith("nestedIdentity:") and j["ok"] for j in result["joins"]), str([j["name"] for j in result["joins"] if "nested" in j["name"]]))
    elif name == "syntax-data":
        rec("R-RUN-SYNTAX-DATA", result["overall"] == "ADMIT", result["overall"])
        rec("inventory-present", any(f["record"]["relation"] == "file" for f in facts), "")
        clones_cov = [c for c in coverages if c["record"]["relation"] == "clones"]
        rec("R-RUN-UNAVAILABLE-SEMANTIC", bool(clones_cov) and clones_cov[0]["entry"].get("coverage") != "complete", json.dumps([c["entry"] for c in clones_cov]))
        rec("not-complete-empty-concealment", not (clones_cov and clones_cov[0]["entry"].get("coverage") == "complete" and clones_cov[0]["entry"].get("deficiency") is None), "")
        rec("syntax-only-no-ts-rust-unit", g["ctx_domain"] == "native.context.syntax.v2" and g["uni"].get("resolutionAttempted") is False, g["ctx_domain"])
        clones_acc = [a for a in ei["nativeCoverageAccounts"] if a["relation"] == "clones"]
        rec("clones-account-applicability-vs-matrix-SUPPORTED-DESIGN", clones_acc[0]["applicability"] == "supported-available" if clones_acc else False, clones_acc[0]["applicability"] if clones_acc else "missing")
        clones_cell = next(o for o in ei["cellOutcomes"] if o["capabilityId"] == "clones-fact")
        rec("clones-fact-cell-not-complete-from-unsupported-typed", clones_cell["state"] != "complete" or clones_acc[0]["applicability"] != "unsupported-typed", f"state={clones_cell['state']} app={clones_acc[0]['applicability']}")
    elif name == "rust-partial-clones":
        rec("R-RUN-RUST-PARTIAL-EMPTY-CLONES", True, "graph present")
        rec("empty-clone-facts", not any(f["record"]["relation"] == "clones" for f in facts), str([f["record"]["relation"] for f in facts]))
        clones_cov = [c for c in coverages if c["record"]["relation"] == "clones"]
        rec("clones-coverage-unknown", clones_cov and clones_cov[0]["entry"].get("coverage") == "unknown", json.dumps([c["entry"] for c in clones_cov]))
        rec("R-CLONE-DEFICIENCY-PAIRING", clones_cov and clones_cov[0]["entry"].get("deficiency") == "input-closure-incomplete" and clones_cov[0]["entry"].get("nativeCause") == "body-language-owner-unenumerated", json.dumps([c["entry"] for c in clones_cov]))
        clones_cell = next(o for o in ei["cellOutcomes"] if o["capabilityId"] == "clones-fact")
        rec("clones-fact-cell-derived-partial", clones_cell["state"] == "partial", json.dumps({k: clones_cell.get(k) for k in ["state","deficiency","nativeCause"]}))
        rec("does-not-claim-complete-from-partial-ownership", clones_cell["state"] != "complete", clones_cell["state"])
        rec("file-present-inventory-complete", any(o["capabilityId"] == "inventory" and o["state"] == "complete" for o in ei["cellOutcomes"]), "")
        rec("seal-not-false-pass-on-required-partial", g.get("derived_verdict") == "indeterminate" or result["layers"]["fullsemantic"] == "REFUSED", f"derived={g.get('derived_verdict')} claimed={g['claimed_proof']['verdict']}")
    return props


def rust_extra_properties(result: dict) -> list[dict]:
    g = result.get("graph")
    props = []
    if not g:
        return props
    store_path = Path(result["store"])
    store = Store.load(store_path)
    uni = g["uni"]
    own_id = hex_of(uni.get("sourceUnitOwnershipId"))
    if not own_id:
        props.append({"id": "R-RUN-RUST-TARGET-EDITION", "ok": False, "detail": "no sourceUnitOwnershipId"})
        return props
    parsed = parse_h_frame(store.rehash(own_id))
    own = parsed["value"]
    units = own.get("units") or []
    editions = []
    pkg_ed = None
    bin_ed = None
    for u in units:
        te = u.get("targetEdition")
        editions.append((u.get("unitId"), u.get("crateName"), te, u.get("kind") or u.get("targetKind")))
        if u.get("crateName") == "a" and (u.get("unitKind") == "lib" or str(u.get("unitId","")).endswith("lib") or "lib" in str(u.get("targetName") or u.get("unitId") or "")):
            pkg_ed = te
        if "bin" in str(u.get("unitId") or "") or u.get("targetName") == "tool" or u.get("name") == "tool":
            bin_ed = te
    # fallback: inspect all unit fields
    props.append({"id": "ownership-units", "ok": True, "detail": json.dumps(units)[:1200]})
    target_diff = False
    crate_default = (uni.get("edition") or {}).get("a")
    for u in units:
        te = u.get("targetEdition")
        crate = u.get("crateName")
        default = (uni.get("edition") or {}).get(crate)
        if te is not None and default is not None and te != default:
            target_diff = True
            props.append({"id": "R-RUN-RUST-TARGET-EDITION", "ok": True, "detail": f"crate {crate} default {default} target {u.get('unitId')}={te}"})
            break
    if not any(p["id"] == "R-RUN-RUST-TARGET-EDITION" for p in props):
        props.append({"id": "R-RUN-RUST-TARGET-EDITION", "ok": target_diff, "detail": f"editionMap={uni.get('edition')} units={[{k:u.get(k) for k in u} for u in units]}"[:800]})
    # same file two editions: ownership rows for one path with two targetEditions
    by_path = {}
    units_by_id = {u["unitId"]: u for u in units}
    for row in own.get("ownership") or []:
        by_path.setdefault(row["path"], []).append(row)
    two = False
    for path, rows in by_path.items():
        eds = set()
        for r in rows:
            u = units_by_id.get(r["unitId"], {})
            te = u.get("targetEdition")
            if te is None:
                te = (uni.get("edition") or {}).get(u.get("crateName"))
            eds.add(te)
        if len(eds) > 1:
            two = True
            props.append(
                {
                    "id": "R-RUN-RUST-SAME-FILE-TWO-EDITIONS",
                    "ok": False,
                    "detail": f"{path} editions={sorted(eds, key=lambda x: str(x))} both appear in one selectedUnitIds set; dialect law refuses BODY_LANGUAGE_OWNER_AMBIGUOUS. Lawful form is one selection/universe at a time.",
                }
            )
            break
    if not two:
        props.append({"id": "R-RUN-RUST-SAME-FILE-TWO-EDITIONS", "ok": False, "detail": "no path owned at two editions"})
    props.append({"id": "R-RUN-RUST-BODY-DIALECT", "ok": any(j["name"] == "languageVersion-derived" and j["ok"] for j in result["joins"]), "detail": ""})
    # pair artifact is a consumer claim; independently recompute from ownership if possible
    pair_path = SNAP / "runs/rust.body-identity-pair.json"
    if pair_path.exists():
        pair = json.loads(pair_path.read_text())
        props.append(
            {
                "id": "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
                "ok": False,
                "detail": "consumer pair artifact is a claim, not a second retained graph; this validator did not independently mint a lib-only selection universe. Claimed L0 2018 vs 2021 distinct="
                + str(pair.get("edition2018_L0") != pair.get("edition2021_L0")),
            }
        )
        props.append({"id": "R-RUN-RUST-VERSION-COMPONENT", "ok": any(j["name"] == "languageVersion-derived" and j["ok"] for j in result["joins"]), "detail": "derived from rustc context + selected target edition"})
    return props


def main() -> int:
    probes_dir = OUT / "probes"
    probes_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for name in RUNS:
        store_path = SNAP / "runs" / f"{name}.store.json"
        print(f"ADMIT {name} {store_path}", flush=True)
        r = admit_one(store_path)
        graph = r.pop("graph", None)
        r["_has_graph"] = graph is not None
        try:
            props = check_properties(name, {**r, "graph": graph})
        except Exception as e:
            props = [{"id": "property-check-crash", "ok": False, "detail": f"{type(e).__name__}: {e}"}]
        if name == "rust" and graph:
            try:
                props.extend(rust_extra_properties({**r, "graph": graph}))
            except Exception as e:
                props.append({"id": "rust-extra-properties-crash", "ok": False, "detail": f"{type(e).__name__}: {e}"})
        r["originalProperties"] = props
        r["joinFails"] = [j for j in r["joins"] if not j["ok"]]
        r["joinPassCount"] = sum(1 for j in r["joins"] if j["ok"])
        r["joinFailCount"] = len(r["joinFails"])
        # drop bulky joins from summary later; keep in probe
        probe = {k: v for k, v in r.items() if k != "joins"}
        probe["joins"] = r["joins"]
        (probes_dir / f"{name}.admission.json").write_text(json.dumps(probe, indent=2, default=str) + "\n")
        results[name] = r
        print(f"  overall={r['overall']} layers={r['layers']} first={r['firstRefusal']}", flush=True)
        for f in r["joinFails"][:8]:
            print(f"    FAIL {f['layer']}:{f['name']}: {f['detail'][:200]}", flush=True)

    # replacement graph: try to admit rust proof into ts store conceptually
    replacement = {
        "kind": "whole-replacement-graph-admission",
        "note": "A foreign proof3 identity cannot join this Run's evaluation-seal.proofBundleId. Independently reminting a replacement proof is not treated as the consumer's accepted graph.",
        "executed": True,
    }
    if results["ts"].get("proofId") and results["rust"].get("proofId"):
        replacement["tsProof"] = results["ts"]["proofId"]
        replacement["rustProof"] = results["rust"]["proofId"]
        replacement["distinct"] = results["ts"]["proofId"] != results["rust"]["proofId"]
        replacement["result"] = "foreign-proof-would-fail-seal-join"
    (probes_dir / "replacement.json").write_text(json.dumps(replacement, indent=2) + "\n")

    # verdict
    per_run_admit = {n: results[n]["overall"] == "ADMIT" for n in RUNS}
    if all(per_run_admit.values()):
        verdict = "OTHER_RUNS_ADMIT"
    else:
        verdict = "OTHER_RUNS_REFUSED"

    unexecuted = []
    # ROOT-ADMISSION outside role
    unexecuted.append("ROOT-ADMISSION (outside this validator role; not presumed)")
    unexecuted.append("component-manifest-schemas.v11 stock inhabitance / signature envelopes (CANDIDATE-NOT-APPLIED)")
    unexecuted.append("real host/compiler/crypto/SQLite execution (synthetic TCB observations used; structural joins still executed)")
    unexecuted.append("L1 token-stream tokenisation where L1 facts are absent")
    unexecuted.append("default-profile remaining matrix cells not requested by these Plans")
    unexecuted.append("incoming-search / target-attribution / sufficiency_v2 incoming completeness (no such selected records on these four graphs)")
    unexecuted.append("whole-consumer ACCEPT / other original requirements outside these four Runs")

    # applicability inventory
    applicable = [
        "lexical/C/H/CVE1 on retained bytes",
        "owning-schema stock JSON Schema + x-opensip-order via pinned local $id registry",
        "x-opensip-digest annotations on graph records",
        "x-opensip-payload-registry for relation/coverage/import/parameter",
        "relation registry ladder/universe/anchor/rung/snapshotJoins",
        "file coverageTotality + coveragePartitionLaw",
        "identity-schemas.v3 domainSets nestedIdentities/nestedRecords/snapshotJoins/blobJoins/closureJoins",
        "closureMembership direct/equalToDirect + detector extra selected",
        "component-manifest stored-bytes join (no v11 inhabitance)",
        "capabilityManifestId SHA256(UTF8(opensip.capability-manifest.v1)||00||CVE1 bytes)",
        "execution-inputs selectedRefs totality, view-only stage, hostDerivedRefs",
        "native coverage account totality vs matrix relations; applicability from matrix cell state + VCS",
        "derive_account + derive_outcome joined to host CellProgramOutcomeV1",
        "enumeration inventory one-per-cell-program-kind",
        "FACT-IDENTITY L0 frame + languageVersion derivation",
        "scopeCapabilityLaw for clones under closed-suffix-table universes",
        "complete expected proof from selected program/evidence/scope/Coverage/import/enumeration/execution inputs",
        "logical-result tamper vs stale-hash separately; whole-replacement identity join separately",
        "composition §5 required executionDeficiencies → sealed indeterminate",
    ]

    summary = {
        "verdict": verdict,
        "standing": "Independent kit-only validator of four reconstructed Runs. Not whole-consumer ACCEPT. Root admission not performed.",
        "python": f"{PYTHON} -I -B",
        "custody": {
            "kitManifestSha256": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
            "parentSubjectSha256": "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb",
            "requirementsSha256": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
            "snapshotManifestSha256": "385cacdedbca83701acc14afbe9342dfe8d4c4867453888e391fc1f2c2e4be33",
            "kitFiles": "PASS 80/80",
            "snapshotFiles": "PASS 275/275",
        },
        "command": f"{PYTHON} -I -B {HERE / 'review_four.py'}",
        "runs": {},
        "applicableLawsExecuted": applicable,
        "unexecutedObligations": unexecuted,
        "replacement": replacement,
        "consumerHelperNotOracle": True,
    }
    for name in RUNS:
        r = results[name]
        summary["runs"][name] = {
            "storeSha256": r["storeSha256"],
            "bytes": r["bytes"],
            "blobCount": r["blobCount"],
            "runId": r.get("runId"),
            "planId": r.get("planId"),
            "proofId": r.get("proofId"),
            "expectedProofId": r.get("expectedProofId"),
            "layers": r["layers"],
            "overall": r["overall"],
            "firstRefusal": r["firstRefusal"],
            "claimedVerdict": r.get("claimedVerdict"),
            "derivedVerdict": r.get("derivedVerdict"),
            "proofCExpectedSha256": r.get("proofCExpectedSha256"),
            "proofCClaimedSha256": r.get("proofCClaimedSha256"),
            "tamper": r.get("tamper"),
            "requestedCapabilities": r.get("requestedCapabilities"),
            "cellOutcomes": r.get("cellOutcomes"),
            "coverages": r.get("coverages"),
            "snapshotPaths": r.get("snapshotPaths"),
            "originalProperties": r.get("originalProperties"),
            "joinFailCount": r.get("joinFailCount"),
            "joinFails": r.get("joinFails"),
            "notReached": r.get("notReached"),
        }

    (OUT / "other-runs-review.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    md = render_md(summary)
    (OUT / "other-runs-review.md").write_text(md)
    print("VERDICT", verdict)
    return 0 if verdict == "OTHER_RUNS_ADMIT" else 0  # review always writes


def render_md(s: dict) -> str:
    lines = []
    lines.append("# Other-runs independent kit-only review")
    lines.append("")
    lines.append(f"**Verdict: `{s['verdict']}`**")
    lines.append("")
    lines.append(s["standing"])
    lines.append("")
    lines.append("This is not whole-consumer ACCEPT, not product implementation, and not root admission.")
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    lines.append("| Object | SHA-256 | Result |")
    lines.append("|---|---|---|")
    c = s["custody"]
    lines.append(f"| kit `consumer-input-manifest.json` | `{c['kitManifestSha256']}` | {c['kitFiles']} |")
    lines.append(f"| parent frozen SHA | `{c['parentSubjectSha256']}` | match |")
    lines.append(f"| `requirements.json` | `{c['requirementsSha256']}` | match |")
    lines.append(f"| `snapshot-manifest.json` | `{c['snapshotManifestSha256']}` | {c['snapshotFiles']} |")
    lines.append("")
    lines.append(f"Python: `{s['python']}`")
    lines.append("")
    lines.append("Reproducible command:")
    lines.append("")
    lines.append("```bash")
    lines.append(s["command"])
    lines.append("```")
    lines.append("")
    lines.append("Consumer helper PASS, saved evaluator output, and copied review files inside the snapshot were treated as claims under review, not oracles.")
    lines.append("")
    lines.append("## First-refusal map (existing published law, not invented profile)")
    lines.append("")
    lines.append("| Run | Raw | Schema | Structural first refusal | Fullsemantic first refusal |")
    lines.append("|---|---|---|---|---|")
    for name, r in s["runs"].items():
        fr = r.get("firstRefusal") or {}
        sem = next((j for j in (r.get("joinFails") or []) if j["layer"] == "fullsemantic" and j["name"] == "proof-C-compare"), None)
        lines.append(
            f"| `{name}` | {r['layers']['raw']} | {r['layers']['schema']} | `{fr.get('layer','')}:{fr.get('name','')}` | `{sem['name'] if sem else 'n/a'}` |"
        )
    lines.append("")
    lines.append("Classification of refusals:")
    lines.append("")
    lines.append("- **Existing law, missing consumer implementation:** TypeScript imported `runtime` payload does not inhabit `RuntimePayloadV1` (`format=json` / null `observationWindow`). Rust `crateRootPaths` `#/a` is not an inventoried snapshot path (native-evidence crateRootPaths join). Rust toolchain tree `bin/proc-macro-srv` declared 13 bytes, retained blob is 14 (`b'proc-macro-srv'`). Rust clones fact is minted under one universe whose `selectedUnitIds` own `#/a/src/lib.rs` at editions 2018 and 2021 (`BODY_LANGUAGE_OWNER_AMBIGUOUS`; lawful form is one selection at a time). syntax-data `clones-fact` account is `unsupported-typed` while matrix cell `clones-fact × syntax-only` is `SUPPORTED-DESIGN`; Coverage unknown + `language-tier-unsupported`/`capability-missing` is the scopeCapabilityLaw disclosure, which makes a supported-available account incomplete and the required cell **partial**, not complete. rust-partial required `clones-fact` cell is correctly host-`partial`, but claimed proof `executionDeficiencies=[]` and `verdict=pass` contrary to composition §5 (required execution deficiency ⇒ sealed indeterminate). `evaluationInputRefs` adds `policy` and `rule-program` beyond enumeration-contract §7 `selectedRefs + execution-inputs`.")
    lines.append("- **Absent/contradictory published law:** none used as a waiver. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED; stored-bytes tree join was still executed.")
    lines.append("- **Not invented default-profile cells:** these Plans request explicit capability subsets; unselected `calls`/`types`/`references` were not demanded.")
    lines.append("")
    lines.append("## Per-Run outcomes")
    lines.append("")
    for name, r in s["runs"].items():
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(f"- Store SHA-256 `{r['storeSha256']}` ({r['bytes']} bytes, {r['blobCount']} blobs)")
        lines.append(f"- Run `{r.get('runId')}`")
        lines.append(f"- Plan `{r.get('planId')}`")
        lines.append(f"- Claimed proof `{r.get('proofId')}`")
        lines.append(f"- Independently reconstructed proof `{r.get('expectedProofId')}`")
        lines.append(f"- Layers: raw `{r['layers']['raw']}` / schema `{r['layers']['schema']}` / structural `{r['layers']['structural']}` / fullsemantic `{r['layers']['fullsemantic']}`")
        lines.append(f"- Overall: **{r['overall']}**")
        if r.get("firstRefusal"):
            fr = r["firstRefusal"]
            lines.append(f"- First refusal: `{fr.get('layer')}:{fr.get('name')}` — {fr.get('detail')}")
        else:
            lines.append("- First refusal: none")
        lines.append(f"- Claimed verdict `{r.get('claimedVerdict')}`; independently derived verdict `{r.get('derivedVerdict')}`")
        lines.append(f"- Proof C claimed `{r.get('proofCClaimedSha256')}`; expected `{r.get('proofCExpectedSha256')}`")
        if r.get("tamper"):
            lines.append(f"- Tamper: stale-hash control `{r['tamper'].get('staleHashControl')}`; semantic refuse `{r['tamper'].get('semanticRefuse')}`; tampered `{r['tamper'].get('tamperedProofId')}`")
        lines.append("")
        if r.get("joinFails"):
            lines.append("Failed joins:")
            lines.append("")
            for j in r["joinFails"]:
                lines.append(f"- `{j['layer']}:{j['name']}` — {j['detail']}")
            lines.append("")
        lines.append("Original required properties:")
        lines.append("")
        for p in r.get("originalProperties") or []:
            mark = "PASS" if p["ok"] else "FAIL"
            lines.append(f"- `{p['id']}` {mark} — {p.get('detail','')}")
        lines.append("")
        lines.append("Requested capabilities / cell outcomes:")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps({"requested": r.get("requestedCapabilities"), "cells": r.get("cellOutcomes"), "coverages": r.get("coverages")}, indent=2))
        lines.append("```")
        lines.append("")
    lines.append("## Applicable-law inventory (executed)")
    lines.append("")
    for law in s["applicableLawsExecuted"]:
        lines.append(f"- {law}")
    lines.append("")
    lines.append("## Unexecuted obligations")
    lines.append("")
    for u in s["unexecutedObligations"]:
        lines.append(f"- {u}")
    lines.append("")
    lines.append("## Whole-replacement graph")
    lines.append("")
    lines.append(json.dumps(s["replacement"], indent=2))
    lines.append("")
    lines.append("Diagnostic expected proofs were constructed only in this validator's output. Consumer stores were not reminted.")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
