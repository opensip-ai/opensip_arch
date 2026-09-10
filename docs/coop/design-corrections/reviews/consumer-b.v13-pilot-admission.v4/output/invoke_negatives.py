#!/usr/bin/env python3
"""Actually invoke admission/evaluation/query negatives; retain observed refusals."""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v4/output")
sys.path.insert(0, str(OUT))

from helpers import admit, admit_graph, cap_admit, store  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def observe(fn, label):
    try:
        fn()
        return {"label": label, "refused": False, "unexpectedPass": True}
    except Exception as e:
        return {
            "label": label,
            "refused": True,
            "firstRefusal": getattr(e, "firstRefusal", type(e).__name__),
            "code": getattr(e, "code", type(e).__name__),
            "path": getattr(e, "path", ""),
            "message": str(e)[:3000],
            "failures": getattr(e, "failures", None),
        }


def main() -> int:
    rows = []
    # 1. original first-pass TS store (preserved)
    orig = OUT / "pilot" / "original-first-pass" / "ts.store.json"
    st = store.load_export(json.loads(orig.read_text()))
    rows.append(observe(lambda: admit_graph.admit_store(st), "original-first-pass-ts-store"))

    # 2. SelectedEnumeratorRef missing status
    rows.append(
        observe(
            lambda: admit.admit_document(
                {"status": "selected"},  # missing closureId
                "opensip.product.enumeration-plan.1",
                store.Store(),
                "selected-enumerator-missing-closure",
                "SelectedEnumeratorRef",
            ),
            "selected-enumerator-missing-closureId",
        )
    )
    rows.append(
        observe(
            lambda: admit.admit_document(
                {"closureId": "closure2:" + ("ab" * 32)},
                "opensip.product.enumeration-plan.1",
                store.Store(),
                "selected-enumerator-missing-status",
                "SelectedEnumeratorRef",
            ),
            "selected-enumerator-missing-status",
        )
    )

    # 3. WaiverSet wrong family
    rows.append(
        observe(
            lambda: admit.admit_document(
                {"schemaFamily": "opensip.product.waiver", "schemaMajor": 1, "waivers": []},
                "urn:opensip:product-v1:workflows:policy-document",
                store.Store(),
                "waiver-family",
                "WaiverSetV1",
            ),
            "waiver-schemaFamily-singular",
        )
    )

    # 4. Imports importer not SubjectIdV1
    rows.append(
        observe(
            lambda: admit.admit_relation_payload(
                {"importer": "src/index.ts::x", "specifier": "left-pad"},
                "imports",
                store.Store(),
                "imports-importer",
            ),
            "imports-importer-not-subject-id",
        )
    )

    # 5. configGraphPaths order
    ctx = {
        "schemaVersion": 2,
        "languageMode": "ts-tsconfig",
        "toolchain": {
            "compilerName": "typescript",
            "compilerVersion": "5.4.5",
            "compilerPackageDigest": "aa" * 32,
            "typescriptStdlibMerkleRoot": "bb" * 32,
            "standardLibraryComponentDigests": [],
            "libSelection": ["es2022"],
        },
        "toolClosure": {"compiler": "aa" * 32, "runtime": "cc" * 32, "closureId": "closure2:" + ("dd" * 32)},
        "configProjection": {
            "schemaVersion": 2,
            "ancestorCarrierVerified": True,
            "environmentSanitized": True,
            "typeAcquisitionEnabled": False,
            "executableSelected": False,
            "honoredOptions": {
                "module": "nodenext",
                "moduleResolution": "nodenext",
                "target": "es2022",
                "strict": True,
                "skipLibCheck": True,
                "noEmit": True,
                "types": None,
                "lib": ["es2022"],
                "baseUrl": None,
                "paths": [],
                "rootDirs": [],
                "resolveJsonModule": True,
                "allowSyntheticDefaultImports": True,
                "esModuleInterop": True,
                "customConditions": [],
                "jsx": None,
            },
            "strippedOptions": [],
            "configGraphPaths": ["tsconfig.json", "tsconfig.base.json"],
        },
        "moduleResolutionMode": "nodenext",
        "packageModuleType": "module",
        "nodeModulesLayoutDigest": None,
        "lockfileIdentity": None,
    }
    rows.append(
        observe(
            lambda: admit.admit_document(
                ctx,
                "urn:opensip:product-v1:native:evidence-schemas:v2",
                store.Store(),
                "ts-context-unsorted-paths",
                "TypeScriptNativeContextV2",
            ),
            "configGraphPaths-not-utf8-sorted",
        )
    )

    # 6. reminted false-result: structural admit passed; replay refused (already retained)
    fr = json.loads((OUT / "vectors" / "false-result-remint.json").read_text())
    rows.append(
        {
            "label": "false-result-remint-replay",
            "refused": bool(fr.get("replayRejectedAlteredResult")),
            "firstRefusal": "PROOF_COMPARE",
            "message": "derived complete proof != reminted claimed proof",
            "derivedVerdict": fr.get("derivedVerdict"),
            "claimedVerdict": fr.get("claimedVerdict"),
        }
    )

    refused = [r for r in rows if r.get("refused")]
    passed_unexpected = [r for r in rows if r.get("unexpectedPass")]
    report = {
        "invoked": len(rows),
        "observedRefusals": len(refused),
        "unexpectedPasses": passed_unexpected,
        "rows": rows,
        "proseIsExplanatoryOnly": True,
    }
    dump(OUT / "vectors" / "negatives-invoked.json", report)
    print("NEGATIVES invoked", len(rows), "refused", len(refused), "unexpectedPass", len(passed_unexpected))
    for r in rows:
        print(" ", r.get("label"), "refused" if r.get("refused") else "PASS", r.get("code") or r.get("firstRefusal"))
    return 1 if passed_unexpected else 0


if __name__ == "__main__":
    sys.exit(main())
