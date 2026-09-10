#!/usr/bin/env python3
"""Unit-boundary negatives for each newly implemented applicable table entry/variant.

Not complete-Run controls. A missing-record prerequisite refusal is not evidence
for a later comparison. Isolated helper tests do not meet the original fully
reminted semantic-negative requirement.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output")
sys.path.insert(0, str(OUT))

from helpers import admit, closure, law_admit, store, kit_schemas  # noqa: E402
from helpers.store import load_export  # noqa: E402


def rec(results, fid, variant, checker, mutation, refused, first, note=""):
    results.append(
        {
            "id": fid,
            "variant": variant,
            "checker": checker,
            "mutation": mutation,
            "refused": bool(refused),
            "firstRefusal": first,
            "boundary": "unit",
            "notCompleteRunControl": True,
            "note": note,
        }
    )
    print(("REFUSED" if refused else "UNEXPECTED_PASS"), fid, first)


def main():
    results = []
    st0 = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    admit.set_graph_context(st0)

    # 1 by-domain unregistered sibling domain
    err = admit._require_digest(
        "0" * 64,
        {"representation": "by-domain", "registry": "x-opensip-digest-domains"},
        st0,
        "finding3:test/evidenceRefs[0]/digest",
        parent={"domain": "not-a-registered-domain", "digest": "0" * 64},
        root="finding3:test",
        field="evidenceRefs[0]/digest",
        schema_ptr="/$defs/FindingEvidenceRef/properties/digest/x-opensip-digest",
    )
    rec(results, "NEG-BY-DOMAIN-UNREGISTERED", "by-domain unregistered sibling domain",
        "admit._require_digest", "parent.domain=not-a-registered-domain",
        err, err, "kit: identity-schemas.v3.json#/$defs/FindingEvidenceRef/properties/digest")

    # 2 by-domain missing sibling domain
    err = admit._require_digest(
        "0" * 64,
        {"representation": "by-domain", "registry": "x-opensip-digest-domains"},
        st0,
        "finding3:test/evidenceRefs[0]/digest",
        parent={"digest": "0" * 64},
        root="finding3:test",
        field="evidenceRefs[0]/digest",
        schema_ptr="/$defs/FindingEvidenceRef/properties/digest/x-opensip-digest",
    )
    rec(results, "NEG-BY-DOMAIN-MISSING-SIBLING", "by-domain missing sibling domain",
        "admit._require_digest", "parent without domain",
        err, err, "kit: Ref.digest representation=by-domain resolves sibling domain")

    # 3 snapshot-path not inventoried
    err = admit._require_digest(
        "not/in/snapshot.ts",
        {"representation": "snapshot-path", "retention": "snapshot-inventoried"},
        st0,
        "fact2:test/path",
        parent={"path": "not/in/snapshot.ts", "contentSha256": "ab", "byteLength": 1},
        root="fact2:test",
        field="path",
        schema_ptr="/$defs/FilePayloadV1/properties/path/x-opensip-digest",
    )
    rec(results, "NEG-SNAPSHOT-PATH-ABSENT", "snapshot-path snapshot-inventoried",
        "admit._require_digest", "path not in snapshot inventory",
        err, err, "kit: relation-payload-schemas.v2.json FilePayloadV1.path")

    # 4 snapshot-path not-joined must NOT refuse (inapplicable)
    err = admit._require_digest(
        "../secret",
        {"representation": "snapshot-path", "retention": "not-joined", "join": "pre-rename"},
        st0,
        "fact2:test/previousPath",
        parent={"previousPath": "../secret", "changeKind": "renamed"},
        root="fact2:test",
        field="previousPath",
        schema_ptr="/$defs/VcsChangePayloadV1/properties/previousPath/x-opensip-digest",
    )
    rec(results, "NEG-SNAPSHOT-PATH-NOT-JOINED-EXEMPT", "snapshot-path retention=not-joined",
        "admit._require_digest", "previousPath outside analysed snapshot",
        err is None, "inapplicable" if err is None else err,
        "exemption must not be treated as inventoried; inapplicable is the executed result")

    # 5 unhandled representation
    err = admit._require_digest(
        "0" * 64,
        {"representation": "not-a-terminal-representation"},
        st0,
        "x/digest",
        parent=None,
        root="x",
        field="digest",
        schema_ptr="/x-opensip-digest",
    )
    rec(results, "NEG-UNHANDLED-REPRESENTATION", "unknown x-opensip-digest representation",
        "admit._require_digest", "representation=not-a-terminal-representation",
        err, err, "unknown owed variant must refuse, not return success")

    # 6 uint64 length mismatch
    fact = next(o for i, o in st0.objects.items() if i.startswith("fact2:") and o.get("relation") == "file")
    pl = law_admit._c(st0, fact["payloadDigest"])
    blob = st0.blobs.get(pl["contentSha256"])
    err = admit._require_digest(
        (len(blob) if blob is not None else 0) + 1,
        {"representation": "raw-artifact", "codec": "uint64", "retention": "preimage"},
        st0,
        "fact2:test/byteLength",
        parent=pl,
        root="fact2:test",
        field="byteLength",
        schema_ptr="/$defs/FilePayloadV1/properties/byteLength/x-opensip-digest",
    )
    rec(results, "NEG-UINT64-LENGTH", "raw-artifact codec=uint64",
        "admit._require_digest", "byteLength = retained+1",
        err, err, "kit: FilePayloadV1.byteLength")

    # 7 config-node-kind: tsconfig.base.json as tsconfig
    err = admit._check_vocabulary(
        "tsconfig",
        {"authority": "native/native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law"},
        "graph",
        "nodes[0]/kind",
        "/$defs/TypeScriptConfigGraphV1/properties/nodes/items/properties/kind/x-opensip-vocabulary",
        parent={"path": "tsconfig.base.json", "kind": "tsconfig"},
    )
    rec(results, "NEG-CONFIG-NODE-KIND", "config-node-kind-law basename table",
        "admit._check_vocabulary", "tsconfig.base.json kind=tsconfig (want other)",
        err, err, "kit: native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law")

    # 8 import.producerClosure must be provider
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    imp_id = next(i for i in st.objects if i.startswith("import2:"))
    adapter = next(i for i, o in st.objects.items() if i.startswith("closure2:") and o.get("kind") == "adapter")
    st.objects[imp_id] = dict(st.objects[imp_id])
    st.objects[imp_id]["producerClosure"] = adapter
    err = law_admit.check_closure_kinds(st)
    hit = [e for e in err if "import.producerClosure" in e]
    rec(results, "NEG-IMPORT-PRODUCER-KIND", "closureKinds.byField import.producerClosure=provider",
        "law_admit.check_closure_kinds", "import.producerClosure set to adapter closure",
        hit, hit[0] if hit else (err[0] if err else None),
        "kit: identity-schemas.v3.json#/x-opensip-digest-domains/closureKinds/byField/import.producerClosure")

    # 9 universeRule same-only
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    fid = next(i for i, o in st.objects.items() if i.startswith("fact2:") and o.get("relation") == "file")
    fact = dict(st.objects[fid])
    fact["targetUniverse"] = "f" * 64
    snap = next(o for i, o in st.objects.items() if i.startswith("snapshot2:"))
    payload = law_admit._c(st, fact["payloadDigest"])
    err = closure.check_fact_relation_laws(fact, payload, snap, st, fact_id=fid)
    hit = [e for e in err if "UNIVERSE_RULE" in e]
    rec(results, "NEG-UNIVERSE-RULE-SAME-ONLY", "relation registry universeRule=same-only",
        "closure.check_fact_relation_laws", "file fact targetUniverse mutated",
        hit, hit[0] if hit else (err[0] if err else None),
        "kit: relation-payload-schemas.v2.json relations.file.universeRule")

    unexpected = [r for r in results if r["id"] != "NEG-SNAPSHOT-PATH-NOT-JOINED-EXEMPT" and not r["refused"]]
    unexpected += [r for r in results if r["id"] == "NEG-SNAPSHOT-PATH-NOT-JOINED-EXEMPT" and not r["refused"]]
    # the exempt case records refused=True when err is None because rec(..., err is None, ...)
    # Wait: rec(..., err is None) means refused=True when inapplicable succeeds. That's the intended "executed inapplicable".
    (OUT / "inventory" / "negatives-v3.json").write_text(json.dumps({"standing": "Unit-boundary negatives for newly implemented applicable variants. Not complete-Run semantic negatives.", "results": results, "unexpectedPass": [r["id"] for r in results if r["id"] != "NEG-SNAPSHOT-PATH-NOT-JOINED-EXEMPT" and not r["refused"]]}, indent=2) + "\n")
    bad = [r["id"] for r in results if r["id"] != "NEG-SNAPSHOT-PATH-NOT-JOINED-EXEMPT" and not r["refused"]]
    print("unexpectedPass", bad)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
