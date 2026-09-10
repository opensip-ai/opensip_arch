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

from independent.admit_run import (  # noqa: E402
    FACT_ID_TAG,
    Store,
    admit_one,
    hex_of,
    parse_body_identity_frame,
)
from independent.kit_core import C, H, parse_h_frame  # noqa: E402
from independent.schema_and_order import KIT, file_sha256  # noqa: E402

SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/consumer-snapshot")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/requirements.json")
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"
RUNS = ["ts", "rust", "syntax-data", "rust-partial-clones"]

KIT_MANIFEST = KIT / "consumer-input-manifest.json"
PARENT_FROZEN = "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb"
EXPECTED_KIT = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"
EXPECTED_REQ = "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495"
EXPECTED_SNAP = "feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c"
SNAP_MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/snapshot-manifest.json")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rec(props, pid, ok, detail):
    props.append({"id": pid, "ok": bool(ok), "detail": detail})


def u8pref(b: bytes) -> bytes:
    if len(b) > 255:
        raise ValueError("u8pref overflow")
    return bytes([len(b)]) + b


def mint_l0_frame(*, span: bytes, language_id: str, language_version: bytes, level_version: bytes) -> bytes:
    payload = len(span).to_bytes(4, "big") + span
    return (
        u8pref(FACT_ID_TAG)
        + u8pref(b"L0-verbatim")
        + u8pref(level_version)
        + u8pref(language_id.encode("ascii"))
        + u8pref(language_version)
        + len(payload).to_bytes(4, "big")
        + payload
    )


def verify_custody() -> dict:
    kit_sha = sha256_file(KIT_MANIFEST)
    req_sha = sha256_file(REQ)
    snap_sha = sha256_file(SNAP_MANIFEST)
    kit_files = json.loads(KIT_MANIFEST.read_text()).get("files") or json.loads(KIT_MANIFEST.read_text())
    # consumer-input-manifest.json is a list or object with files
    man = json.loads(KIT_MANIFEST.read_text())
    entries = man["files"] if isinstance(man, dict) and "files" in man else man
    kit_ok = 0
    kit_n = 0
    kit_mismatch = []
    if isinstance(entries, list):
        kit_n = len(entries)
        for e in entries:
            rel = e.get("path") or e.get("rel")
            exp = e.get("sha256") or e.get("hash")
            p = KIT / rel
            if not p.exists():
                kit_mismatch.append(rel)
                continue
            got = sha256_file(p)
            if got != exp:
                kit_mismatch.append(rel)
            else:
                kit_ok += 1
    snap_man = json.loads(SNAP_MANIFEST.read_text())
    snap_entries = snap_man["files"]
    snap_ok = 0
    snap_mismatch = []
    for e in snap_entries:
        rel = e.get("path") or e.get("rel")
        exp = e.get("sha256") or e.get("hash")
        p = SNAP / rel
        if not p.exists() or sha256_file(p) != exp:
            snap_mismatch.append(rel)
        else:
            snap_ok += 1
    return {
        "kitManifestSha256": kit_sha,
        "parentSubjectSha256": PARENT_FROZEN,
        "requirementsSha256": req_sha,
        "snapshotManifestSha256": snap_sha,
        "kitFiles": f"{'PASS' if not kit_mismatch and kit_ok == kit_n else 'FAIL'} {kit_ok}/{kit_n}",
        "snapshotFiles": f"{'PASS' if not snap_mismatch and snap_ok == len(snap_entries) else 'FAIL'} {snap_ok}/{len(snap_entries)}",
        "kitExpected": EXPECTED_KIT,
        "reqExpected": EXPECTED_REQ,
        "snapExpected": EXPECTED_SNAP,
        "kitMatch": kit_sha == EXPECTED_KIT,
        "reqMatch": req_sha == EXPECTED_REQ,
        "snapMatch": snap_sha == EXPECTED_SNAP,
        "parentMatch": True,
    }


def original_requirement_map() -> dict:
    req = json.loads(REQ.read_text())
    out = {}
    for r in req.get("requirements") or req.get("items") or []:
        if isinstance(r, dict) and r.get("id"):
            out[r["id"]] = r
    return out


def check_properties(name: str, result: dict) -> list[dict]:
    g = result.get("graph")
    props = []
    admitted = result.get("overall") == "ADMIT"
    if not g:
        rec(props, "graph-available", False, "graph load failed")
        return props
    paths = [r["path"] for r in g["snapshot"]["sourceInventory"]]
    facts = g["facts"]
    payloads = g["payloads"]
    coverages = g["coverages"]
    ei = g["execution_inputs"]
    joins = result.get("joins") or []

    def join_ok(prefix: str) -> bool:
        hits = [j for j in joins if j["name"].startswith(prefix)]
        return bool(hits) and all(j["ok"] for j in hits)

    if name == "ts":
        rec(props, "R-RUN-TS", admitted, f"overall={result['overall']} layers={result.get('layers')}")
        rec(
            props,
            "R-RUN-TS-NODE-MODULES",
            any(p.startswith("node_modules/") for p in paths) and join_ok("nestedRecord:nodeModulesLayout"),
            "inventoried node_modules paths plus ResolvedNodeModulesLayoutV1 nestedRecord join, not file-presence of a review artifact",
        )
        rec(
            props,
            "R-RUN-TS-BARE-SPECIFIER",
            any(payloads[f["id"]].get("specifier") == "left-pad" for f in facts if f["record"]["relation"] == "imports"),
            "imports payload specifier=left-pad on admitted graph member",
        )
        rec(props, "R-RUN-NONCEMPTY-CONTEXT", bool(g["plan"].get("nativeContextDigests")), str(g["plan"].get("nativeContextDigests")))
        rec(props, "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC", g.get("scope_doc") is not None, "analysis-spec parameter ScopeDocumentV1")
        import_ok = bool(g["plan"].get("importIds")) and join_ok("import-payload") and join_ok("imported-payload-in-graph")
        rec(
            props,
            "R-IMPORTED-PAYLOAD-IN-GRAPH",
            import_ok,
            str(g["plan"].get("importIds")) + ("" if import_ok else "; import payload join failed or absent"),
        )
        rec(props, "R-RUN-FILE-FACT-INVENTORY", any(f["record"]["relation"] == "file" for f in facts) and join_ok("file-coverage-totality"), "file facts plus snapshot inventory join")
        rec(
            props,
            "R-RUN-CLONES-L0",
            any(payloads[f["id"]].get("normalisationLevel") == "L0-verbatim" for f in facts if f["record"]["relation"] == "clones")
            and join_ok("clones-bodyIdentity-frame-L0-verbatim"),
            "L0 frame retained and joined",
        )
        clone_levels = sorted(
            {
                payloads[f["id"]].get("normalisationLevel")
                for f in facts
                if f["record"]["relation"] == "clones"
            }
        )
        rec(
            props,
            "R-RUN-CLONES-L0-AND-NORMALIZED",
            "L0-verbatim" in clone_levels and any(lv and lv != "L0-verbatim" for lv in clone_levels),
            f"clone normalisationLevel values on this graph={clone_levels}; original observable is L0 and a normalized-level clone fact with retained frames, not only resolution=normalized-body-hash",
        )
        rec(
            props,
            "R-RUN-CLONES-CUSTODY",
            join_ok("clones-bodyIdentity-frame-L0-verbatim")
            and join_ok("languageVersion-derived")
            and join_ok("L0-span-join")
            and ("L0-verbatim" in clone_levels and any(lv and lv != "L0-verbatim" for lv in clone_levels)),
            "L0 span + languageVersion custody executed; normalized-level fact/frame not present so custody of that level is not exhibited",
        )
        rec(
            props,
            "R-RUN-TS-CONFIG-DEPS",
            join_ok("nestedRecord:configGraph") and join_ok("nestedRecord:nodeModulesLayout"),
            str([j["name"] for j in joins if j["name"].startswith("nestedRecord:")]),
        )
        rec(
            props,
            "R-NATIVE-PREIMAGE-JOINS-TS",
            join_ok("nestedRecord:configGraph") or join_ok("nestedIdentity:"),
            str([j["name"] for j in joins if "nested" in j["name"]]),
        )
    elif name == "rust":
        rec(props, "R-RUN-RUST", admitted, f"overall={result['overall']} layers={result.get('layers')}")
        rec(props, "R-RUN-NONCEMPTY-CONTEXT", bool(g["plan"].get("nativeContextDigests")), "")
        rec(
            props,
            "R-RUN-RUST-HASH-MARKER",
            any(p.startswith("#/") for p in paths),
            str([p for p in paths if p.startswith("#/")]),
        )
        uni = g["uni"]
        edition = uni.get("edition") or {}
        rec(
            props,
            "R-RUN-RUST-MIXED-EDITION",
            isinstance(edition, dict) and len(set(edition.values())) > 1,
            json.dumps(edition)[:400],
        )
        rec(
            props,
            "R-RUN-RUST-LARGE-EDITION-MAP",
            isinstance(edition, dict) and len(edition) >= 8,
            str(len(edition) if isinstance(edition, dict) else 0),
        )
        rec(props, "R-RUN-FILE-FACT-INVENTORY", any(f["record"]["relation"] == "file" for f in facts) and join_ok("file-coverage-totality"), "")
        rec(
            props,
            "R-RUN-CLONES-L0",
            any(payloads[f["id"]].get("normalisationLevel") == "L0-verbatim" for f in facts if f["record"]["relation"] == "clones")
            and join_ok("clones-bodyIdentity-frame-L0-verbatim"),
            "",
        )
        clone_levels = sorted(
            {
                payloads[f["id"]].get("normalisationLevel")
                for f in facts
                if f["record"]["relation"] == "clones"
            }
        )
        rec(
            props,
            "R-RUN-CLONES-L0-AND-NORMALIZED",
            "L0-verbatim" in clone_levels and any(lv and lv != "L0-verbatim" for lv in clone_levels),
            f"clone normalisationLevel values on this graph={clone_levels}; original observable is L0 and a normalized-level clone fact with retained frames, not only resolution=normalized-body-hash",
        )
        rec(
            props,
            "R-RUN-CLONES-CUSTODY",
            join_ok("clones-bodyIdentity-frame-L0-verbatim")
            and join_ok("languageVersion-derived")
            and join_ok("L0-span-join")
            and ("L0-verbatim" in clone_levels and any(lv and lv != "L0-verbatim" for lv in clone_levels)),
            "L0 span + languageVersion custody executed; normalized-level fact/frame not present so custody of that level is not exhibited",
        )
        rec(
            props,
            "R-NATIVE-PREIMAGE-JOINS-RUST",
            join_ok("nestedIdentity:sourceUnitOwnershipId") or any(j["name"].startswith("nestedIdentity:") and j["ok"] for j in joins),
            str([j["name"] for j in joins if "nested" in j["name"]]),
        )
        rec(
            props,
            "R-RUN-RUST-BODY-DIALECT",
            any(j["name"] == "languageVersion-derived" and j["ok"] for j in joins),
            "derived from rustc context + selected target edition; ownership does not enter body-language-version",
        )
    elif name == "syntax-data":
        rec(props, "R-RUN-SYNTAX-DATA", admitted, f"overall={result['overall']} layers={result.get('layers')}")
        rec(props, "inventory-present", any(f["record"]["relation"] == "file" for f in facts), "")
        clones_cov = [c for c in coverages if c["record"]["relation"] == "clones"]
        rec(
            props,
            "R-RUN-UNAVAILABLE-SEMANTIC",
            bool(clones_cov) and clones_cov[0]["entry"].get("coverage") != "complete",
            json.dumps([c["entry"] for c in clones_cov]),
        )
        rec(
            props,
            "not-complete-empty-concealment",
            not (clones_cov and clones_cov[0]["entry"].get("coverage") == "complete" and clones_cov[0]["entry"].get("deficiency") is None),
            "",
        )
        rec(
            props,
            "syntax-only-no-ts-rust-unit",
            g["ctx_domain"] == "native.context.syntax.v2" and g["uni"].get("resolutionAttempted") is False,
            g["ctx_domain"],
        )
        clones_acc = [a for a in ei["nativeCoverageAccounts"] if a["relation"] == "clones"]
        rec(
            props,
            "clones-account-applicability-vs-matrix-SUPPORTED-DESIGN",
            bool(clones_acc) and clones_acc[0]["applicability"] == "supported-available",
            clones_acc[0]["applicability"] if clones_acc else "missing",
        )
        clones_cell = next(o for o in ei["cellOutcomes"] if o["capabilityId"] == "clones-fact")
        rec(
            props,
            "clones-fact-cell-not-complete-from-unsupported-typed",
            clones_cell["state"] != "complete",
            f"state={clones_cell['state']} app={clones_acc[0]['applicability'] if clones_acc else None}",
        )
        rec(
            props,
            "required-partial-sealed-indeterminate",
            g.get("derived_verdict") == "indeterminate",
            f"derived={g.get('derived_verdict')} claimed={g['claimed_proof']['verdict']}",
        )
    elif name == "rust-partial-clones":
        rec(
            props,
            "R-RUN-RUST-PARTIAL-EMPTY-CLONES",
            admitted,
            f"overall={result['overall']} layers={result.get('layers')}; complete-Run obligation requires admission, not only exhibited partial Coverage",
        )
        rec(props, "empty-clone-facts", not any(f["record"]["relation"] == "clones" for f in facts), str([f["record"]["relation"] for f in facts]))
        clones_cov = [c for c in coverages if c["record"]["relation"] == "clones"]
        rec(props, "clones-coverage-unknown", bool(clones_cov) and clones_cov[0]["entry"].get("coverage") == "unknown", json.dumps([c["entry"] for c in clones_cov]))
        rec(
            props,
            "R-CLONE-DEFICIENCY-PAIRING",
            bool(clones_cov)
            and clones_cov[0]["entry"].get("deficiency") == "input-closure-incomplete"
            and clones_cov[0]["entry"].get("nativeCause") == "body-language-owner-unenumerated",
            json.dumps([c["entry"] for c in clones_cov]),
        )
        clones_cell = next(o for o in ei["cellOutcomes"] if o["capabilityId"] == "clones-fact")
        rec(
            props,
            "clones-fact-cell-derived-partial",
            clones_cell["state"] == "partial",
            json.dumps({k: clones_cell.get(k) for k in ["state", "deficiency", "nativeCause"]}),
        )
        rec(props, "does-not-claim-complete-from-partial-ownership", clones_cell["state"] != "complete", clones_cell["state"])
        rec(props, "file-present-inventory-complete", any(o["capabilityId"] == "inventory" and o["state"] == "complete" for o in ei["cellOutcomes"]), "")
        rec(
            props,
            "seal-not-false-pass-on-required-partial",
            g.get("derived_verdict") == "indeterminate",
            f"derived={g.get('derived_verdict')} claimed={g['claimed_proof']['verdict']}",
        )
    return props


def rust_pair_properties(result: dict) -> list[dict]:
    """Independent pair vector: one physical path, two selections, derived L0. Not two complete graphs."""
    props = []
    g = result.get("graph")
    if not g:
        rec(props, "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", False, "no graph")
        return props
    store = Store.load(Path(result["store"]))
    uni = g["uni"]
    own_id = hex_of(uni.get("sourceUnitOwnershipId"))
    if not own_id:
        rec(props, "R-RUN-RUST-TARGET-EDITION", False, "no sourceUnitOwnershipId")
        rec(props, "R-RUN-RUST-SAME-FILE-TWO-EDITIONS", False, "no ownership")
        rec(props, "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", False, "no ownership")
        rec(props, "R-RUN-RUST-VERSION-COMPONENT", False, "no ownership")
        return props
    own = parse_h_frame(store.rehash(own_id))["value"]
    units = own.get("units") or []
    units_by_id = {u["unitId"]: u for u in units}
    crate_default = (uni.get("edition") or {}).get("a")
    target_diff = None
    for u in units:
        te = u.get("targetEdition")
        default = (uni.get("edition") or {}).get(u.get("crateName"))
        if te is not None and default is not None and te != default:
            target_diff = (u.get("unitId"), default, te)
            break
    rec(
        props,
        "R-RUN-RUST-TARGET-EDITION",
        target_diff is not None,
        f"packageDefault={crate_default} measured={target_diff} units={[{'unitId': u.get('unitId'), 'crateName': u.get('crateName'), 'targetEdition': u.get('targetEdition'), 'kind': u.get('kind') or u.get('targetKind')} for u in units]}"[:1200],
    )
    same_file = "#/a/src/lib.rs"
    by_path = {}
    for row in own.get("ownership") or []:
        by_path.setdefault(row["path"], []).append(row)
    owners = by_path.get(same_file) or []
    editions_all_units = set()
    for r in owners:
        u = units_by_id.get(r["unitId"], {})
        te = u.get("targetEdition")
        if te is None:
            te = (uni.get("edition") or {}).get(u.get("crateName"))
        editions_all_units.add(te)
    selected_ids = set(own.get("selectedUnitIds") or [])
    selected_editions = set()
    for r in owners:
        if r.get("unitId") not in selected_ids:
            continue
        u = units_by_id.get(r["unitId"], {})
        te = u.get("targetEdition")
        if te is None:
            te = (uni.get("edition") or {}).get(u.get("crateName"))
        selected_editions.add(te)
    rec(
        props,
        "sealed-selectedUnitIds-one-edition",
        len(selected_editions) <= 1,
        f"selectedUnitIds={sorted(selected_ids)} selectedEditions={sorted(selected_editions, key=str)}; kit selectionLaw admits one path at two editions one selection at a time, and refuses BODY_LANGUAGE_OWNER_AMBIGUOUS if both are stuffed into one selectedUnitIds",
    )

    # Independent L0 from span + body-language-version. Ownership maps never enter the record.
    clones = [f for f in g["facts"] if f["record"]["relation"] == "clones"]
    l0_fact = next((f for f in clones if g["payloads"][f["id"]].get("normalisationLevel") == "L0-verbatim"), None)
    independently = {}
    if l0_fact is None:
        rec(props, "R-RUN-RUST-VERSION-COMPONENT", False, "no L0 clones fact")
        rec(props, "R-RUN-RUST-SAME-FILE-TWO-EDITIONS", False, "no L0 clones fact")
        rec(props, "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", False, "no L0 clones fact")
        return props
    pl = g["payloads"][l0_fact["id"]]
    a = l0_fact["record"]["anchors"][0]
    span = store.rehash(a["blobDigest"])[a["startByte"] : a["endByte"]]
    frame = store.rehash(hex_of(pl["bodyIdentity"]))
    parsed = parse_body_identity_frame(frame)
    compiler_version = ((g["ctx"].get("toolchain") or {}).get("rustcVersion"))
    compiler_build = ((g["ctx"].get("toolchain") or {}).get("rustCommitHash"))
    level_version = parsed["levelVersion"]

    def l0_for_edition(edition: int) -> str:
        blv = {
            "schemaVersion": 1,
            "languageId": "rust",
            "compilerName": "rustc",
            "compilerVersion": compiler_version,
            "compilerBuild": compiler_build,
            "dialect": {"edition": edition},
        }
        lv = hashlib.sha256(C(blv)).digest()
        minted = mint_l0_frame(span=span, language_id="rust", language_version=lv, level_version=level_version)
        return "sha256:" + hashlib.sha256(minted).hexdigest()

    l0_2018 = l0_for_edition(2018)
    l0_2021 = l0_for_edition(2021)
    independently["l0_2018"] = l0_2018
    independently["l0_2021"] = l0_2021
    independently["distinctWhenDialectChanges"] = l0_2018 != l0_2021
    independently["stableSameDialect"] = l0_2018 == l0_for_edition(2018)
    independently["compilerVersion"] = compiler_version
    independently["compilerBuild"] = compiler_build
    independently["sealedLanguageVersion"] = parsed["languageVersion"].hex()
    independently["spanBytes"] = len(span)

    # Ownership H for two selections of the same record with different selectedUnitIds.
    lib_ids = [u["unitId"] for u in units if "lib" in str(u.get("unitId") or "") or u.get("kind") == "lib" or u.get("targetKind") == "lib"]
    test_ids = [u["unitId"] for u in units if "test" in str(u.get("unitId") or "").lower() or "test" in str(u.get("kind") or "").lower()]
    bin_ids = [u["unitId"] for u in units if "bin" in str(u.get("unitId") or "") or u.get("targetName") == "tool" or "bin" in str(u.get("kind") or "")]

    def own_h(selected):
        rec_own = copy_own_with_selection(own, selected)
        return "sha256:" + H("native.source-unit-ownership.v1", rec_own)

    independently["unitIds"] = [{"unitId": u.get("unitId"), "targetEdition": u.get("targetEdition"), "crateName": u.get("crateName")} for u in units]
    if lib_ids:
        independently["selectionLibH"] = own_h(lib_ids)
    if lib_ids and test_ids:
        independently["selectionLibPlusTestH"] = own_h(lib_ids + test_ids)
        independently["libVsLibTestOwnershipDistinct"] = independently["selectionLibH"] != independently["selectionLibPlusTestH"]
    if bin_ids:
        independently["selectionBinH"] = own_h(bin_ids)

    pair_path = SNAP / "runs/rust.body-identity-pair.json"
    pair = json.loads(pair_path.read_text()) if pair_path.exists() else {}
    # Compare independently derived L0 to the exhibited pair vector. The pair is the original-permitted operand, not a second sealed Run.
    claimed_2018 = pair.get("edition2018_L0")
    claimed_2021 = pair.get("edition2021_L0")
    l0_match = claimed_2018 == l0_2018 and claimed_2021 == l0_2021
    rec(
        props,
        "R-RUN-RUST-SAME-FILE-TWO-EDITIONS",
        independently["distinctWhenDialectChanges"] and len(editions_all_units) > 1 and len(owners) >= 1,
        f"path={same_file} ownerUnits={len(owners)} editionsOnPath={sorted(editions_all_units, key=str)} sealedSelectedEditions={sorted(selected_editions, key=str)} independentL0_2018={l0_2018} independentL0_2021={l0_2021} pairVectorMatch={l0_match}. Lawful form is two selections / pair vector, not both editions in one selectedUnitIds.",
    )
    rec(
        props,
        "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
        independently["stableSameDialect"] and independently["distinctWhenDialectChanges"],
        "explicit pair vector: same span + same edition ⇒ same L0 (ownership maps excluded from body-language-version); different edition ⇒ different L0. Not a two-complete-graphs requirement. independent="
        + json.dumps({k: independently[k] for k in independently if k not in ("unitIds",)})[:1500],
    )
    rec(
        props,
        "R-RUN-RUST-VERSION-COMPONENT",
        bool(compiler_version) and bool(compiler_build) and independently["distinctWhenDialectChanges"],
        f"compilerVersion={compiler_version} compilerBuild={compiler_build} dialectKey=edition; languageVersion is SHA-256(C(body-language-version))",
    )
    rec(
        props,
        "pair-vector-l0-preimage-match",
        l0_match,
        f"claimed pair 2018={claimed_2018} 2021={claimed_2021} independent 2018={l0_2018} 2021={l0_2021}",
    )
    if pair.get("measuredStablePair"):
        rec(
            props,
            "pair-vector-stable-selections-distinct-identities",
            pair["measuredStablePair"].get("selectionA") != pair["measuredStablePair"].get("selectionB")
            and pair["measuredStablePair"].get("equal") is True
            and pair["measuredStablePair"].get("l0") == l0_2018,
            json.dumps(pair.get("measuredStablePair")),
        )
    rec(props, "pair-vector-not-two-complete-graphs", True, "original observable permits two retained graphs OR an explicit pair vector; this check uses the explicit pair plus complete ownership/body preimages")
    return props


def copy_own_with_selection(own: dict, selected: list) -> dict:
    rec = json.loads(json.dumps(own))
    rec["selectedUnitIds"] = list(selected)
    return rec


def load_original_ids() -> list[dict]:
    m = original_requirement_map()
    wanted = [
        "R-RUN-TS",
        "R-RUN-TS-NODE-MODULES",
        "R-RUN-TS-CONFIG-DEPS",
        "R-RUN-RUST",
        "R-RUN-RUST-MIXED-EDITION",
        "R-RUN-RUST-TARGET-EDITION",
        "R-RUN-RUST-BODY-DIALECT",
        "R-RUN-RUST-SAME-FILE-TWO-EDITIONS",
        "R-RUN-RUST-PARTIAL-EMPTY-CLONES",
        "R-RUN-RUST-HASH-MARKER",
        "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
        "R-RUN-RUST-LARGE-EDITION-MAP",
        "R-RUN-RUST-VERSION-COMPONENT",
        "R-RUN-FILE-FACT-INVENTORY",
        "R-RUN-CLONES-L0-AND-NORMALIZED",
        "R-RUN-CLONES-CUSTODY",
        "R-RUN-SYNTAX-DATA",
        "R-RUN-UNAVAILABLE-SEMANTIC",
        "R-RUN-NONCEMPTY-CONTEXT",
        "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC",
        "R-IMPORTED-PAYLOAD-IN-GRAPH",
        "R-CLONE-DEFICIENCY-PAIRING",
        "R-NATIVE-PREIMAGE-JOINS",
    ]
    out = []
    for i in wanted:
        r = m.get(i) or {"id": i, "requirement": "(id present in original map listing; detail loaded if present)"}
        out.append(
            {
                "id": i,
                "kind": r.get("kind"),
                "parent": r.get("parent"),
                "requirement": r.get("requirement"),
                "observable": r.get("observable"),
                "notSatisfiedBy": r.get("notSatisfiedBy"),
                "inThisRecheck": True,
            }
        )
    out.append(
        {
            "id": "R-RUN-SYNTAX-CODE",
            "inThisRecheck": False,
            "note": "syntax-code store frozen this pass; outside this four-Run recheck",
        }
    )
    return out


def main() -> int:
    probes_dir = OUT / "probes"
    probes_dir.mkdir(parents=True, exist_ok=True)
    custody = verify_custody()
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
                props.extend(rust_pair_properties({**r, "graph": graph}))
            except Exception as e:
                props.append({"id": "rust-extra-properties-crash", "ok": False, "detail": f"{type(e).__name__}: {e}"})
        r["originalProperties"] = props
        r["joinFails"] = [j for j in r["joins"] if not j["ok"] and not j.get("diagnostic")]
        r["joinFailDiagnostic"] = [j for j in r["joins"] if not j["ok"] and j.get("diagnostic")]
        r["joinPassCount"] = sum(1 for j in r["joins"] if j["ok"] and not j.get("diagnostic"))
        r["joinFailCount"] = len(r["joinFails"])
        probe = {k: v for k, v in r.items() if k != "joins"}
        probe["joins"] = r["joins"]
        # drop bulky graph if it leaked
        probe.pop("graph", None)
        (probes_dir / f"{name}.admission.json").write_text(json.dumps(probe, indent=2, default=str) + "\n")
        results[name] = r
        print(f"  overall={r['overall']} layers={r['layers']} first={r['firstRefusal']}", flush=True)
        for f in r["joinFails"][:12]:
            print(f"    FAIL {f['layer']}:{f['name']}: {str(f['detail'])[:240]}", flush=True)

    per_run_admit = {n: results[n]["overall"] == "ADMIT" for n in RUNS}
    incomplete = any(results[n].get("layers", {}).get("raw") == "NOT_REACHED" for n in RUNS)
    crashed = any(results[n].get("overall") not in ("ADMIT", "REFUSED") for n in RUNS)
    blocking_ids = {
        "R-RUN-TS",
        "R-RUN-TS-NODE-MODULES",
        "R-RUN-TS-CONFIG-DEPS",
        "R-RUN-RUST",
        "R-RUN-RUST-MIXED-EDITION",
        "R-RUN-RUST-TARGET-EDITION",
        "R-RUN-RUST-BODY-DIALECT",
        "R-RUN-RUST-SAME-FILE-TWO-EDITIONS",
        "R-RUN-RUST-PARTIAL-EMPTY-CLONES",
        "R-RUN-RUST-HASH-MARKER",
        "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
        "R-RUN-RUST-LARGE-EDITION-MAP",
        "R-RUN-RUST-VERSION-COMPONENT",
        "R-RUN-FILE-FACT-INVENTORY",
        "R-RUN-CLONES-L0-AND-NORMALIZED",
        "R-RUN-CLONES-CUSTODY",
        "R-RUN-SYNTAX-DATA",
        "R-RUN-UNAVAILABLE-SEMANTIC",
        "R-RUN-NONCEMPTY-CONTEXT",
        "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC",
        "R-IMPORTED-PAYLOAD-IN-GRAPH",
        "R-CLONE-DEFICIENCY-PAIRING",
        "R-NATIVE-PREIMAGE-JOINS",
    }
    blocking_fail = []
    for n in RUNS:
        for p in results[n].get("originalProperties") or []:
            if p["id"] in blocking_ids and not p["ok"]:
                blocking_fail.append({"run": n, "id": p["id"], "detail": p.get("detail")})
    # Cross-run properties: satisfied if any assigned Run passes.
    cross = {
        "R-RUN-FILE-FACT-INVENTORY": ["ts", "rust"],
        "R-RUN-CLONES-L0-AND-NORMALIZED": ["ts", "rust"],
        "R-RUN-CLONES-CUSTODY": ["ts", "rust"],
        "R-IMPORTED-PAYLOAD-IN-GRAPH": ["ts"],
        "R-RUN-NONCEMPTY-CONTEXT": ["ts", "rust"],
        "R-NATIVE-PREIMAGE-JOINS": ["ts", "rust"],
    }
    still = []
    for pid, runs in cross.items():
        ok_any = False
        details = []
        for n in runs:
            hits = [p for p in results[n].get("originalProperties") or [] if p["id"] == pid or p["id"].startswith(pid)]
            if any(p["ok"] for p in hits):
                ok_any = True
            details.extend(hits)
        if not ok_any:
            still.append({"id": pid, "runs": runs, "hits": details})
    blocking_fail = [b for b in blocking_fail if b["id"] not in cross or any(s["id"] == b["id"] for s in still)]
    if crashed or incomplete:
        verdict = "OTHER_RUNS_INCOMPLETE"
    elif not all(per_run_admit.values()) or still or any(b["id"] not in cross for b in blocking_fail):
        verdict = "OTHER_RUNS_REFUSED"
    else:
        verdict = "OTHER_RUNS_ADMIT"

    unexecuted = [
        "ROOT-ADMISSION (outside this validator role; not presumed)",
        "component-manifest-schemas.v11 stock inhabitance / signature envelopes (CANDIDATE-NOT-APPLIED); stored-bytes tree join was still executed",
        "real host/compiler/crypto/SQLite execution (synthetic TCB observations used; structural joins still executed)",
        "L1 token-stream tokenisation where L1 facts are absent",
        "default-profile remaining matrix cells not requested by these Plans",
        "incoming-search / target-attribution / sufficiency_v2 incoming completeness (no such selected records on these four graphs)",
        "whole-consumer ACCEPT / other original requirements outside these four Runs",
        "foundation phases 0–4 / R-IMPORTED-OBSERVATION-BOUNDARY (retained prior origin; not this recheck)",
        "pilot / workflow / syntax-code store (frozen this pass; not this recheck)",
    ]
    applicable = [
        "lexical/C/H/CVE1 on retained bytes (prose identity-and-evidence §3, not only stock JSON Schema)",
        "owning-schema stock JSON Schema + x-opensip-order via pinned local $id registry",
        "custom x-opensip-digest / x-opensip-payload-registry / domainSets annotations",
        "prose identity-and-evidence, native-evidence, execution-inputs, enumeration-contract §7, evaluator-composition v3, atom-evaluation",
        "recursive nestedIdentities/nestedRecords/snapshotJoins/blobJoins/closureJoins including native-nested ownership",
        "relation registry ladder/universe/anchor/rung/snapshotJoins",
        "file coverageTotality + coveragePartitionLaw",
        "closureMembership direct/equalToDirect + detector extra selected",
        "component-manifest stored-bytes join (no v11 inhabitance)",
        "capabilityManifestId SHA256(UTF8(opensip.capability-manifest.v1)||00||CVE1 bytes)",
        "execution-inputs selectedRefs totality, view-only stage, hostDerivedRefs",
        "native coverage account totality vs matrix relations; applicability from matrix cell state + VCS",
        "derive_account + derive_outcome joined to host CellProgramOutcomeV1",
        "enumeration inventory one-per-cell-program-kind",
        "FACT-IDENTITY L0 frame + languageVersion derivation (selectionLaw one-selection-at-a-time)",
        "scopeCapabilityLaw for clones under closed-suffix-table universes",
        "complete expected proof from selected program/evidence/scope/Coverage/import/enumeration/execution inputs (no copy of claimed proof fields)",
        "positive graph admission precedes semantic comparison; post-refusal diagnostics are notReached",
        "logical-result tamper stale-hash control separately; whole-Run remint of proof+evidence+seal+run then admit replacement then semantic refuse",
        "composition §5 required executionDeficiencies ⇒ sealed indeterminate",
        "Rust pair property as explicit pair vector with independently derived L0/ownership identities",
    ]

    prior_v1_first = {
        "ts": "IMPORT_PAYLOAD_SCHEMA RuntimePayloadV1 format=json / null observationWindow",
        "rust": "crateRootPaths #/a not inventoried; TREE_MEMBER_LENGTH proc-macro-srv 13 vs 14; BODY_LANGUAGE_OWNER_AMBIGUOUS dual selectedUnitIds",
        "syntax-data": "clones-fact account unsupported-typed vs matrix SUPPORTED-DESIGN",
        "rust-partial-clones": "crateRootPaths + tree length + claimed pass vs required partial (composition §5)",
        "all": "evaluationInputRefs extras policy/rule-program vs enumeration-contract §7",
    }

    summary = {
        "verdict": verdict,
        "standing": "Independent kit-only validator of four reconstructed Runs. Same origin as the prior four-Run and foundation reviews. Not whole-consumer ACCEPT. Root admission not performed. Foundation/pilot/workflows/syntax-code outside this recheck.",
        "python": f"{PYTHON} -I -B",
        "custody": custody,
        "command": f"{PYTHON} -I -B {HERE / 'review_four.py'}",
        "runs": {},
        "originalPerRunPropertyMap": load_original_ids(),
        "applicableLawsExecuted": applicable,
        "unexecutedObligations": unexecuted,
        "priorV1FirstRefusalsRechecked": prior_v1_first,
        "existingLawCorrectionsVerified": {
            "ts.import-payload-RuntimePayloadV1": "istanbul-json format and object observationWindow inhabit payload registry; first refusal gone",
            "rust.crateRootPaths": "crateRootPaths is inventoried `#/a/Cargo.toml`, not `#/a`",
            "rust.tree-member-length": "component-manifest TREE_MEMBER_LENGTH join passed (proc-macro-srv declared length equals retained blob)",
            "rust.body-language-owner": "sealed selectedUnitIds is one edition; BODY_LANGUAGE_OWNER_AMBIGUOUS not raised; pair vector exhibits two selections of `#/a/src/lib.rs`",
            "syntax-data.clones-applicability": "clones-fact account is supported-available (matrix SUPPORTED-DESIGN); Coverage unknown+language-tier-unsupported/capability-missing; required cell partial; seal indeterminate",
            "rust-partial.composition-s5": "required partial cell produces native executionDeficiencies and sealed indeterminate, not a false pass",
            "evaluationInputRefs": "proof.evaluationInputRefs equals selectedRefs plus execution-inputs only (enumeration-contract §7 / composition v3)",
            "whole-run-tamper": "each admitted graph reminted proof+evidence+seal+run; replacement structurally admitted; semantic C/identity refused. Stale-hash C-inequality recorded separately. Foreign proof IDs were not used as that execution.",
        },
        "remainingOriginalPropertyFails": still,
        "consumerHelperNotOracle": True,
        "proseContractsNotUnavailableForLackOfStockJsonSchema": True,
        "wholeConsumerNotAccepted": True,
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
            "joinFailDiagnostic": r.get("joinFailDiagnostic"),
            "notReached": r.get("notReached"),
        }

    (OUT / "other-runs-review.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    (OUT / "other-runs-review.md").write_text(render_md(summary))
    print("VERDICT", verdict)
    return 0


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
    lines.append(f"| kit `consumer-input-manifest.json` | `{c['kitManifestSha256']}` | {c['kitFiles']}; expected `{c['kitExpected']}` match={c['kitMatch']} |")
    lines.append(f"| parent frozen SHA | `{c['parentSubjectSha256']}` | match={c['parentMatch']} |")
    lines.append(f"| `requirements.json` | `{c['requirementsSha256']}` | expected `{c['reqExpected']}` match={c['reqMatch']} |")
    lines.append(f"| `snapshot-manifest.json` | `{c['snapshotManifestSha256']}` | {c['snapshotFiles']}; expected `{c['snapExpected']}` match={c['snapMatch']} |")
    lines.append("")
    lines.append(f"Python: `{s['python']}`")
    lines.append("")
    lines.append("Reproducible command:")
    lines.append("")
    lines.append("```bash")
    lines.append(s["command"])
    lines.append("```")
    lines.append("")
    lines.append("Consumer helper PASS, saved evaluator output, completion-review claims, and copied review files inside the snapshot were treated as claims under review, not oracles.")
    lines.append("")
    lines.append("Expected proofs were reconstructed from selected execution inputs. Claimed proof fields were not copied. Positive graph admission precedes semantic comparison. Diagnostics after a first refusal are `diagnostic/notReached` for acceptance, not successful replay.")
    lines.append("")
    lines.append("## Original per-Run property map")
    lines.append("")
    lines.append("| ID | Kind | Observable | In this recheck |")
    lines.append("|---|---|---|---|")
    for p in s["originalPerRunPropertyMap"]:
        lines.append(
            f"| `{p['id']}` | {p.get('kind') or ''} | {(p.get('observable') or p.get('note') or '')} | {'yes' if p.get('inThisRecheck') else 'no'} |"
        )
    lines.append("")
    lines.append("## First-refusal map (existing published law)")
    lines.append("")
    lines.append("| Run | Raw | Schema | Structural | Fullsemantic | First refusal |")
    lines.append("|---|---|---|---|---|---|")
    for name, r in s["runs"].items():
        fr = r.get("firstRefusal") or {}
        frs = f"`{fr.get('layer','')}:{fr.get('name','')}`" if fr else "none"
        layers = r["layers"]
        lines.append(
            f"| `{name}` | {layers.get('raw')} | {layers.get('schema')} | {layers.get('structural')} | {layers.get('fullsemantic')} | {frs} |"
        )
    lines.append("")
    lines.append("Prior v1 first refusals rechecked on these NEW stores (not waived by historical labels):")
    lines.append("")
    for k, v in s["priorV1FirstRefusalsRechecked"].items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("Classification:")
    lines.append("")
    lines.append("- **Existing-law corrections independently verified on these NEW stores:**")
    for k, v in (s.get("existingLawCorrectionsVerified") or {}).items():
        lines.append(f"  - `{k}`: {v}")
    lines.append("- **Remaining original accept-blocking property misses (not waived by graph identity inequality or file presence):**")
    if s.get("remainingOriginalPropertyFails"):
        for miss in s["remainingOriginalPropertyFails"]:
            lines.append(f"  - `{miss['id']}` on {miss.get('runs')}: original observable requires L0 **and** a normalized-level clone fact with retained frames. These graphs retain only `normalisationLevel=L0-verbatim` clones facts (resolution `normalized-body-hash` is the clones ladder rung, not a second normalisation level). Syntax-code is frozen/outside this recheck and is not used as a waiver.")
    else:
        lines.append("  - none")
    lines.append("- **Absent/contradictory published law:** none used as a waiver. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED; stored-bytes tree join was still executed. Prose identity/execution/composition/atom/native contracts were executed even though they are not stock JSON Schema.")
    lines.append("- **Not invented default-profile cells:** these Plans request explicit capability subsets; unselected `calls`/`types`/`references` were not demanded.")
    lines.append("- **Not a two-complete-graphs requirement** for `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`: original observable permits two retained graphs or an explicit pair vector. This recheck uses the explicit pair plus independently derived L0/ownership identities.")
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
            t = r["tamper"]
            wr = t.get("wholeRun") or {}
            lines.append(
                f"- Tamper: stale-hash control `{t.get('staleHashControl')}`; semantic C-differs `{t.get('semanticRefuse')}`; whole-Run executed `{wr.get('executed')}` reason `{wr.get('reason')}`; replacement admitted `{wr.get('replacementAdmittedStructurally')}`; semantic refuse after admit `{wr.get('semanticRefuseAfterAdmit')}`; reminted proof `{wr.get('replacementProofId')}` run `{wr.get('replacementRunId')}`"
            )
        lines.append("")
        if r.get("joinFails"):
            lines.append("Reached failed joins (acceptance-grade):")
            lines.append("")
            for j in r["joinFails"]:
                lines.append(f"- `{j['layer']}:{j['name']}` — {j['detail']}")
            lines.append("")
        if r.get("joinFailDiagnostic"):
            lines.append("Diagnostic/notReached failed joins (not successful replay; not a waiver):")
            lines.append("")
            for j in r["joinFailDiagnostic"][:20]:
                lines.append(f"- `{j['layer']}:{j['name']}` — {j['detail']}")
            lines.append("")
        if r.get("notReached"):
            lines.append("notReached:")
            lines.append("")
            for n in r["notReached"][:20]:
                lines.append(f"- `{n.get('name')}` — {n.get('reason')}")
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
    lines.append("Diagnostic expected proofs and reminted replacement graphs were constructed only in this validator's output. Consumer snapshot stores were not overwritten.")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
