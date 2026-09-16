#!/usr/bin/env python3
"""Install regenerated query artifacts, write the source33 remint account, README and binding,
then rebuild artifact-manifest.json (excluding itself; no circular claim)."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
REMINT = HERE / "remint"
SOURCE_MANIFEST_SHA = "1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299"

REMINTED_TS_GROUPS = ["checkpoint3", "binding-controls", "semantic-controls1"]
REUSED_EXACT_GROUPS = ["normalized-examples6", "rust-selection-examples1"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def install_queries() -> list:
    rows = []
    dest_dir = V10 / "query-checks1"
    for src in sorted((REMINT / "query-checks").iterdir()):
        if src.is_file():
            dest = dest_dir / src.name
            old = V9 / "query-checks1" / src.name
            before = sha(old) if old.is_file() else None
            shutil.copy2(src, dest)
            rows.append({"path": f"query-checks1/{src.name}", "source30Sha256": before,
                         "source33Sha256": sha(dest), "changed": before != sha(dest)})
    shutil.copy2(REMINT / "query-assessment.json", V10 / "query-assessment.json")
    rows.append({"path": "query-assessment.json",
                 "source30Sha256": sha(V9 / "query-assessment.json"),
                 "source33Sha256": sha(V10 / "query-assessment.json"),
                 "changed": sha(V9 / "query-assessment.json") != sha(V10 / "query-assessment.json")})
    # Properties and mixed-universe probe reproduced byte-identically; copy anyway so the
    # package bytes are the ones this pass actually executed.
    for name in ("author-properties.json", "mixed-universe-view.probe.json"):
        shutil.copy2(REMINT / name, V10 / name)
        rows.append({"path": name, "source30Sha256": sha(V9 / name),
                     "source33Sha256": sha(V10 / name),
                     "changed": sha(V9 / name) != sha(V10 / name)})
    return rows


def main() -> int:
    query_rows = install_queries()
    install = json.loads((HERE / "reports" / "install-remint.json").read_text())

    old_claims = {g: json.loads((V9 / g / "claims.json").read_text()) for g in REMINTED_TS_GROUPS}
    new_claims = {g: json.loads((V10 / g / "claims.json").read_text()) for g in REMINTED_TS_GROUPS}
    run_rows = []
    for g in REMINTED_TS_GROUPS:
        old_by = {c["name"]: c["runId"] for c in old_claims[g]}
        for c in new_claims[g]:
            run_rows.append({
                "group": g, "name": c["name"],
                "source30RunId": old_by.get(c["name"]), "source33RunId": c["runId"],
                "runIdChanged": old_by.get(c["name"]) != c["runId"],
                "storeSha256": sha(V10 / g / c["path"]),
                "source30StoreSha256": sha(V9 / g / c["path"]) if (V9 / g / c["path"]).is_file() else None,
            })
    for g in REUSED_EXACT_GROUPS:
        for c in json.loads((V10 / g / "claims.json").read_text()):
            run_rows.append({
                "group": g, "name": c["name"], "source30RunId": c["runId"],
                "source33RunId": c["runId"], "runIdChanged": False,
                "storeSha256": sha(V10 / g / c["path"]),
                "source30StoreSha256": sha(V9 / g / c["path"]),
                "standing": "reused EXACT source30-construction bytes; re-verified against frozen "
                            "source33 in this pass",
            })

    account = {
        "standing": "Source33 REMINT account. The three TypeScript-derived groups are NEW source33 "
                    "constructions; the Rust/normalized groups keep their EXACT source30 "
                    "construction bytes and were re-verified against frozen source33 in the same "
                    "pass. No old execution is relabelled: the superseded source30 bytes are "
                    "preserved verbatim under historical-source33-before-remint/.",
        "sourceManifestSha256": SOURCE_MANIFEST_SHA,
        "predecessorPackage": str(V9),
        "predecessorArtifactManifestSha256": sha(V9 / "artifact-manifest.json"),
        "whyTheRemintWasRequired": {
            "symptom": "checkpoint3/author-ts and the two positive binding controls reached "
                       "structural ADMIT then EVALUATOR_COMPLETE_PROOF_REPLAY on frozen source33.",
            "exactDifference": "One proof field differed: executionDeficiencies. The retained "
                               "source30 proof carried a second item "
                               "(language-tier-unsupported, nativeCause null) for a Coverage record "
                               "that retains (null, null); source33 derives "
                               "(required-cell-unsatisfied, null) for it.",
            "cause": "The BUNDLED author helper author-helpers/evaluator.py still applied the "
                     "pre-source33 carrier rule: `fallback = records[0].deficiency or "
                     "'provider-unavailable'` and `e['deficiency'] or fallback`. A record carrying "
                     "no pair borrowed records[0]'s deficiency while keeping its own null "
                     "nativeCause - an unzipped, re-paired carrier - and a missing-work account "
                     "would have been given a manufactured provider-unavailable.",
            "resolution": "The helper now emits each record's OWN exact pair, with (null, null) "
                          "when a record carries none, reaching required-cell-unsatisfied through "
                          "the existing registry branch. This is a correction of the AUTHOR "
                          "HELPER to the published source33 law. NO frozen source byte was "
                          "changed, and no fixture was adjusted to make an old artifact pass.",
            "notASourceDefect": "Frozen source33 refused correctly. The refusal is the published "
                                "no-invention / exact-per-record-pair law of "
                                "execution-inputs-contract.v1.md sections 4 and 5 and "
                                "evaluator-composition-contract.v3.md section 9.6 doing its job "
                                "against a stale author artifact.",
        },
        "remintedGroups": REMINTED_TS_GROUPS,
        "reusedExactGroups": REUSED_EXACT_GROUPS,
        "runComparison": run_rows,
        "regeneratedDerivedArtifacts": query_rows,
        "installRecord": install["reminted"],
        "beforeImages": "historical-source33-before-remint/",
    }
    (V10 / "source33-remint.v1.json").write_text(json.dumps(account, indent=2) + "\n")

    binding = {
        "standing": "Current source33 binding. The three TypeScript-derived groups are NEW "
                    "source33 constructions produced by the corrected bundled author helper; the "
                    "normalized and Rust groups are the EXACT source30 construction bytes, "
                    "re-verified against frozen source33 in the same pass. Native schema "
                    "unchanged. Independent assessment and blind acceptance remain required; no "
                    "old execution is relabelled.",
        "sourceManifestSha256": SOURCE_MANIFEST_SHA,
        "parentPackageManifestSha256": sha(V9 / "artifact-manifest.json"),
        "constructionAccount": "source33-remint.v1.json",
        "historicalConstructionAccount": "source-rebuild.v1.json",
        "constructionSourceVersion": {"typescriptDerivedGroups": 33,
                                      "normalizedAndRustGroups": 30},
        "currentVerificationSourceVersion": 33,
        "exportsChanged": True,
        "exportsChangedDetail": "checkpoint3, binding-controls and semantic-controls1 only.",
        "helperChanged": ["author-helpers/evaluator.py"],
        "productQualification": False,
    }
    (V10 / "source-binding.v33.json").write_text(json.dumps(binding, indent=2) + "\n")

    readme = """# Source33 author reference package (v10) — review pending

Thirteen cases and seven queries, as before. What changed in this revision, and what did not:

* **Reminted on frozen source33**: `checkpoint3` (the TypeScript positive), `binding-controls`
  (three) and `semantic-controls1` (three). Their predecessors were source30 constructions whose
  retained proof no longer replayed under source33 and are preserved verbatim under
  `historical-source33-before-remint/`.
* **Reused EXACT source30 construction bytes**: `normalized-examples6` (four) and
  `rust-selection-examples1` (two). Their bytes are unchanged and they were re-verified against
  frozen source33 in this same pass, so their standing is measured here, not inherited.
* **Corrected**: the bundled `author-helpers/evaluator.py` execution-deficiency carrier. It had
  kept the pre-source33 rule under which a Coverage record carrying no pair borrowed a sibling's
  deficiency while keeping its own null nativeCause, with a manufactured `provider-unavailable`
  behind that. It now emits each record's own exact pair and `(null, null)` when a record carries
  none. `source33-remint.v1.json` records the exact proof difference this fixed. **No frozen
  source byte was changed and no fixture was adjusted to make an old artifact pass.**
* **Reproduced byte-identically** on source33: `author-properties.json` and
  `mixed-universe-view.probe.json`.

Run the reference interpreter with `-I -B verify-package.py --source <frozen-source33> --out
<new-external-output>`. It verifies exact source/package hashes, executes structural and full
semantic closure on all thirteen cases, then reproduces and asserts seven query checks. Property
and mixed-universe probes remain separate: `check-author-properties.py` and
`probe-mixed-universe-view.py` take `--source/--package/--out`. Prior execution does not imply
current execution.

Evidence limits remain unchanged. Only the TypeScript checkpoint compares a partial consumer
helper with the owner; the six other positives are owner-derived/replayed self-consistency. The
helper exercises `exists`/`none`; `and`/`or`/`not` are unexercised and `count-at-most`/
`all-covered` are unimplemented. The two-binding construction is incomplete and retains a single
explicit binding. Synthetic records qualify no compiler, provider, OS or process-isolation
boundary, and the host TCB assumption of the thirteen cases is unchanged. This package holds
author-assisted reference evidence, never independent review, blind acceptance or final
application approval. It must never be supplied to the blind consumer. All thirty independent
residual grades remain PENDING.
"""
    (V10 / "README.md").write_text(readme)

    files = []
    for p in sorted(V10.rglob("*")):
        if not p.is_file() or p.is_symlink():
            continue
        rel = str(p.relative_to(V10))
        if rel == "artifact-manifest.json":
            continue  # never lists itself; no circular claim
        files.append({"path": rel, "sha256": sha(p), "bytes": p.stat().st_size})
    manifest = {
        "standing": "Source33-bound author reference evidence, independent review pending. This "
                    "manifest does not list itself; it makes no claim about its own bytes.",
        "sourceManifestSha256": SOURCE_MANIFEST_SHA,
        "files": files,
    }
    (V10 / "artifact-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    out = {
        "packageFileCount": len(files),
        "artifactManifestSha256": sha(V10 / "artifact-manifest.json"),
        "manifestListsItself": any(r["path"] == "artifact-manifest.json" for r in files),
        "queryArtifactsChanged": [r["path"] for r in query_rows if r["changed"]],
        "queryArtifactsUnchanged": [r["path"] for r in query_rows if not r["changed"]],
        "runIdsChanged": [f"{r['group']}/{r['name']}" for r in run_rows if r["runIdChanged"]],
        "runIdsUnchanged": [f"{r['group']}/{r['name']}" for r in run_rows if not r["runIdChanged"]],
    }
    (HERE / "reports" / "finalize-package10.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
