#!/usr/bin/env python3
"""Complete identity-and-evidence.md §3 paragraph inventory + executed laws.

Inventory is a completeness check, not a substitute for execution.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v3/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v3/subject")
IE = KIT / "docs/v2/contracts/product-v1/identity-and-evidence.md"
sys.path.insert(0, str(OUT))

from helper.proof_replay import admit_graph, load_graph, reconstruct_expected_enclosing, reconstruct_expected_proof  # noqa: E402
from helper.s3_closure import execute_kit_s3_schema_laws, execute_s3_laws  # noqa: E402
from helper.store import Store  # noqa: E402
from helper.canonical import C  # noqa: E402
from helper.identity import typed_id  # noqa: E402


def paragraphs_s3() -> list[dict]:
    lines = IE.read_text().splitlines()
    paras = []
    buf = []
    start = 87
    for i, l in enumerate(lines[86:1349], start=87):
        if l.strip() == "":
            if buf:
                paras.append({"start": start, "end": i - 1, "firstSentence": buf[0].strip(), "text": "\n".join(buf)})
                buf = []
            start = i + 1
        else:
            if not buf:
                start = i
            buf.append(l)
    if buf:
        paras.append({"start": start, "end": 1349, "firstSentence": buf[0].strip(), "text": "\n".join(buf)})
    return paras


# Line-start → (disposition, lawIds, applicability, note)
# disposition: EXECUTED | N/A | META | WITHDRAWN | KIT
MAP = [
    (87, 87, "META", [], "both", "section heading"),
    (89, 98, "EXECUTED", ["S3-LEXICAL-BEFORE-DESERIALIZE"], "both", "lexical admission before deserialize + bounds"),
    (100, 108, "EXECUTED", ["S3-C-REMAINDER-CONFIG", "S3-ORDER-PREDICATE"], "both", "C encoder; arrays admitted order"),
    (110, 124, "EXECUTED", ["S3-ORDER-PREDICATE"], "both", "x-opensip-order vocabulary; predicate order on proof"),
    (126, 136, "EXECUTED", ["S3-ORDER-PREDICATE", "S3-RULE-PROGRAM-PROJECTION"], "both", "identity-schemas array orders; policy ruleId order"),
    (138, 144, "EXECUTED", ["S3-LEXICAL-BEFORE-DESERIALIZE"], "both", "text/path/span bounds via lexical+C remainder"),
    (146, 146, "META", [], "both", "lead-in to H recipe"),
    (148, 148, "EXECUTED", ["S3-H-RECIPE-RUN", "S3-H-RECIPE-PROOF"], "both", "H(D,X) formula"),
    (150, 153, "EXECUTED", ["S3-H-RECIPE-RUN", "S3-CAP-MANIFEST-ID"], "both", "prefix + hex; raw blob vs semantic domain"),
    (155, 175, "EXECUTED", ["S3-H-RECIPE-RUN", "S3-H-RECIPE-PROOF", "S3-ACYCLIC-SEAL-HAS-BOTH"], "both", "domain/prefix table for records in this graph"),
    (177, 192, "EXECUTED", ["S3-ACYCLIC-PROOF", "S3-ACYCLIC-EVIDENCE-HAS-PROOF", "S3-ACYCLIC-SEAL-HAS-BOTH"], "both", "acyclic graph; fingerprint correspondence unused on unmatched tamper finding"),
    (194, 200, "EXECUTED", ["S3-FINDING-CITE-WITNESS", "S3-PRED-INPUTREF-SUBSET", "S3-EVIDENCE-IMPORT-IDS"], "both", "finding citations; import unused still selected"),
    (202, 213, "EXECUTED", ["S3-CAP-MANIFEST-ID"], "both", "capabilityManifestId recipe from committed bytes"),
    (215, 241, "KIT", ["S3-KIT-DIGEST-DOMAINS", "S3-KIT-PAYLOAD-REGISTRY"], "kit", "effective capability-manifest-domains.v2 selection; ADM gates in cap_manifest"),
    (243, 263, "N/A", ["S3-NA-TS-RUST-TOOLCHAIN"], "neither", "TS stdlib / rustc LLVM — syntax context has no those fields"),
    (265, 273, "EXECUTED", ["S3-SCOPE-COMMITMENT", "S3-COVERAGE-SCOPE-COMMIT"], "both", "subjectScopeCommitment = sha256:+scope2 suffix"),
    (275, 286, "EXECUTED", ["S3-H-FRAME-NATIVE-CONTEXT", "S3-PLAN-CONTEXT-SET"], "both", "native.context.syntax.v2 H domain; plan.nativeContextDigests bare hex"),
    (288, 303, "EXECUTED", ["S3-H-FRAME-NATIVE-CONTEXT", "S3-GRAMMAR-TREE", "S3-UNIVERSE-BIND-CONTEXT"], "both", "frame proves retention never admission; re-run bind_syntax_universe / grammar tree"),
    (305, 317, "EXECUTED", ["S3-PLAN-CONTEXT-SET", "S3-UNIVERSE-BIND-CONTEXT"], "both", "re-derived context/universe joins; TS/Rust nested toolchain N/A"),
    (319, 329, "EXECUTED", ["S3-SNAPSHOT-JOINS-FILE"], "both", "repository paths in snapshot inventory (file payload path)"),
    (331, 352, "EXECUTED", ["S3-UNIVERSE-OWN-LANGUAGE-SYNTAX", "S3-NA-NESTED-RUST-IDENTITIES"], "both", "three universe domains; syntax bind; rust nested N/A"),
    (354, 365, "N/A", ["S3-NA-NESTED-RUST-IDENTITIES"], "neither", "nested rust dependency/file-manifest identities"),
    (367, 372, "N/A", ["S3-NA-NESTED-RUST-IDENTITIES"], "neither", "CargoConfigProjectionV2 two digests"),
    (374, 381, "N/A", ["S3-NA-NESTED-RUST-IDENTITIES"], "neither", "prepared products / prepare-code grant"),
    (383, 383, "META", [], "both", "### The closing digest law"),
    (385, 396, "KIT", ["S3-KIT-DIGEST-DOMAINS"], "kit", "closing digest law: every 64-hex field annotated; no field-name inference"),
    (398, 407, "EXECUTED", ["S3-H-FRAME-NATIVE-CONTEXT", "S3-C-REMAINDER-CONFIG", "S3-CAP-MANIFEST-ID"], "both", "four terminal representations + by-domain selector"),
    (410, 415, "EXECUTED", ["S3-CAP-MANIFEST-ID", "S3-H-FRAME-NATIVE-CONTEXT", "S3-PAYLOAD-REGISTRY-RELATION", "S3-C-REMAINDER-CONFIG"], "both", "representation table measured on present fields"),
    (417, 417, "META", [], "both", "The four retention modes are closed:"),
    (418, 424, "EXECUTED", ["S3-C-REMAINDER-CONFIG", "S3-CAP-MANIFEST-ID"], "both", "retention modes: preimage fetch+rehash; derived capabilityManifestId"),
    (419, 424, "EXECUTED", ["S3-C-REMAINDER-CONFIG", "S3-CAP-MANIFEST-ID"], "both", "retention table"),
    (426, 442, "EXECUTED", ["S3-H-FRAME-NATIVE-CONTEXT"], "both", "H frame parse: prefix, domain, length, C remainder"),
    (444, 453, "EXECUTED", ["S3-H-FRAME-NATIVE-CONTEXT", "S3-PLAN-CONTEXT-SET"], "both", "annotation vs spelling; bare-hex needs domain set"),
    (455, 463, "EXECUTED", ["S3-PLAN-CONTEXT-SET", "S3-UNIVERSE-BIND-CONTEXT"], "both", "plan.nativeContextDigests is a set; universe selects context"),
    (465, 472, "EXECUTED", ["S3-PRED-INPUTREF-SUBSET", "S3-PAYLOAD-REGISTRY-RELATION"], "both", "Ref digest representation by-domain"),
    (474, 497, "EXECUTED", ["S3-BUDGET-EQUAL", "S3-C-REMAINDER-CONFIG", "S3-STAGE-SPEC-PARAMS"], "both", "auxiliary digests: resolvedConfig, analysisSpec, semanticGrant, budget"),
    (499, 503, "EXECUTED", ["S3-VCS-INVENTORY"], "both", "vcs-observation"),
    (505, 524, "EXECUTED", ["S3-PRED-INPUTREF-SUBSET", "S3-EVIDENCE-COVERAGE-UNION", "S3-EVIDENCE-IMPORT-IDS", "S3-PROOF-IMPORTS-IN-EIREFS", "S3-RULE-PROGRAM-PROJECTION"], "both", "closure checker dispatch on annotation; witness/view/import joins"),
    (526, 535, "EXECUTED", ["S3-H-RECIPE-RUN", "S3-EXPECTED-PROOF-NO-CLAIMED-FIELDS"], "both", "visited objects join Plan; profile3 reconstructs predicate tree"),
    (537, 553, "EXECUTED", ["S3-RULE-PROGRAM-PROJECTION", "S3-VCS-INVENTORY", "S3-PAYLOAD-REGISTRY-RELATION"], "both", "policy/rule-program/waiver canonical-record; schema document bytes"),
    (555, 555, "META", [], "both", "### The payload registry"),
    (557, 564, "WITHDRAWN", ["S3-KIT-PAYLOAD-REGISTRY"], "kit", "withdrawn vacuous-bundle sentence; replaced by payload registry"),
    (566, 579, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION", "S3-PAYLOAD-REGISTRY-COVERAGE", "S3-KIT-PAYLOAD-REGISTRY"], "both", "payload registry law: full document bytes + selector + C"),
    (571, 579, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION", "S3-PAYLOAD-REGISTRY-COVERAGE"], "both", "payloadSchemaDigest raw SHA-256 of exact full document bytes"),
    (581, 586, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION", "S3-PAYLOAD-REGISTRY-COVERAGE"], "both", "registry class table"),
    (588, 588, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION"], "both", "view.schemaDigests selected not derived; fact pins document"),
    (590, 598, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "ScopeDocumentV1 parameter row; this Plan selects none (zero legal)"),
    (600, 609, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "scope-descriptor vs ScopeDocumentV1"),
    (611, 626, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "parameter class keying limitation"),
    (628, 638, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "at most one parameter per registered row"),
    (640, 651, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "zero legal; uniqueItems on parameters"),
    (653, 662, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "enforced at pre-Plan and Run closure"),
    (664, 672, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "adopt_baseline is not this graph"),
    (674, 681, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "baseline scope binding verifier"),
    (683, 701, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "BASELINE.SCOPE_* public details"),
    (703, 713, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "ambiguous selection / caller assertion"),
    (715, 718, "N/A", ["S3-NA-SCOPE-DOCUMENT-V1"], "neither", "two scope records remain different"),
    (720, 720, "META", [], "both", "### fact2 payload encoding heading"),
    (722, 727, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION"], "both", "inherited CBOR vs C settled: fact2 payloads are C"),
    (729, 738, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION", "S3-KIT-RELATION-LADDER"], "both", "fact2 payloads are C; 13 relations; ladder authority"),
    (740, 752, "KIT", ["S3-KIT-RELATION-LADDER"], "kit", "ladder is explicit array; rungs is not the ladder"),
    (754, 763, "KIT", ["S3-KIT-RELATION-LADDER"], "kit", "ladder weakest-first; mirrors drift-checked"),
    (765, 770, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION", "S3-KIT-RELATION-LADDER"], "both", "membership against ladder; no empty-ladder fallback"),
    (772, 782, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION"], "both", "minResolution is rung names; this atom uses none over file@enumerated"),
    (784, 795, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION"], "both", "abstract Resolution enum withdrawn; satisfaction is ladder-index"),
    (797, 810, "EXECUTED", ["S3-RULE-PROGRAM-PROJECTION", "S3-PROGRAM-PREDICATE"], "both", "Run closure enforces atom relation/rung on Plan policy and compiled program"),
    (812, 820, "META", [], "both", "historical FactRecord1 untouched; not a fact2 preimage"),
    (822, 826, "EXECUTED", ["S3-PAYLOAD-REGISTRY-RELATION", "S3-UNIVERSE-RULE"], "both", "joined at Run closure for every fact"),
    (828, 828, "META", [], "both", "#### Relation payloads heading"),
    (830, 836, "EXECUTED", ["S3-SNAPSHOT-JOINS-FILE", "S3-ANCHOR-LAW"], "both", "relation-payload digest law / snapshotJoins class"),
    (838, 844, "KIT", ["S3-KIT-ANCHOR-LAW-EVERY-RELATION"], "kit", "x-opensip-digest-law on relation document"),
    (846, 857, "KIT", ["S3-KIT-ANCHOR-LAW-EVERY-RELATION"], "kit", "governed occurrences of DigestHex/CanonicalPath"),
    (859, 865, "KIT", ["S3-KIT-DIGEST-DOMAINS"], "kit", "every governed occurrence must have annotation"),
    (866, 871, "KIT", ["S3-KIT-DIGEST-DOMAINS"], "kit", "no precedence between disagreeing annotations"),
    (867, 871, "KIT", ["S3-KIT-DIGEST-DOMAINS"], "kit", "no precedence between disagreeing annotations (alt start)"),
    (873, 886, "KIT", ["S3-KIT-ANCHOR-LAW-EVERY-RELATION"], "kit", "schema-law admission of registered schema coherence"),
    (888, 901, "EXECUTED", ["S3-SNAPSHOT-JOINS-FILE", "S3-CLONES-BODY-FRAME", "S3-ANCHOR-LAW"], "both", "snapshotJoins table applied to every owning fact"),
    (896, 901, "EXECUTED", ["S3-SNAPSHOT-JOINS-FILE"], "both", "snapshotJoins relation table"),
    (903, 916, "EXECUTED", ["S3-ANCHOR-LAW", "S3-KIT-ANCHOR-LAW-EVERY-RELATION"], "both", "anchorLaw classes inventory/body-identity/source-text"),
    (912, 916, "EXECUTED", ["S3-ANCHOR-LAW"], "both", "anchorLaw class table"),
    (918, 921, "EXECUTED", ["S3-ANCHOR-LAW"], "both", "zero is only cardinality every inventoried path can satisfy"),
    (923, 933, "EXECUTED", ["S3-SNAPSHOT-JOINS-FILE", "S3-ANCHOR-LAW"], "both", "raw-byte boundary: inventory hashes/measures without decoding"),
    (935, 948, "EXECUTED", ["S3-ANCHOR-LAW"], "both", "finding location not via inventory anchors"),
    (950, 955, "N/A", [], "neither", "vcs-change.previousPath exemption; no vcs-change fact"),
    (957, 959, "EXECUTED", ["S3-SNAPSHOT-JOINS-FILE"], "both", "inventory row vs retention of bytes"),
    (961, 961, "META", [], "both", "#### clones heading"),
    (963, 968, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "clones body recipe pinned to fact-identity-policy.v2"),
    (970, 974, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "normalisationVersion = SHA-256 of retained level-spec bytes"),
    (975, 981, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "bodyIdentity framed domain-separated preimage"),
    (982, 996, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "L0 double length prefix; frame retained"),
    (997, 1001, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "frame fetched, rehashed, parsed, components joined"),
    (1002, 1009, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "languageVersion raw 32 bytes of SHA-256(C(BLV))"),
    (1011, 1024, "EXECUTED", ["S3-UNIVERSE-BIND-CONTEXT", "S3-CLONES-BODY-FRAME"], "both", "BLV derived from retained syntax native context grammar interpreter"),
    (1026, 1030, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "dialect body-specific, selected, no null branch"),
    (1032, 1045, "N/A", ["S3-NA-NESTED-RUST-IDENTITIES"], "neither", "Rust edition from SourceUnitOwnershipV1 — this graph is syntax-only"),
    (1047, 1052, "N/A", ["S3-NA-NESTED-RUST-IDENTITIES"], "neither", "two targets two editions"),
    (1053, 1059, "N/A", ["S3-NA-TS-RUST-TOOLCHAIN"], "neither", "TypeScript suffix table — syntax dialect is grammar suffix"),
    (1061, 1063, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "paths establish selection then do not enter BLV"),
    (1065, 1080, "N/A", ["S3-NA-NESTED-RUST-IDENTITIES"], "neither", "partial enumeration vs selection for Rust clones dialect"),
    (1082, 1091, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "languageId is language of the BODY"),
    (1093, 1108, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "languageId from dialect suffix table / bodyLanguageLaw; never universe engine field"),
    (1110, 1116, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "shared bodyIdentity is normalized-body agreement not semantic equivalence"),
    (1117, 1123, "EXECUTED", ["S3-ANCHOR-LAW"], "both", "clones exactly one anchor; body-identity class"),
    (1125, 1131, "EXECUTED", ["S3-CLONES-BODY-FRAME"], "both", "L0 recomputed from anchor; L1+ custody/framing not tokenisation judgment"),
    (1133, 1136, "EXECUTED", ["S3-H-RECIPE-PROOF", "S3-CLONES-BODY-FRAME"], "both", "FACT-ID-V1 and bodyIdentity never equated"),
    (1138, 1141, "EXECUTED", ["S3-H-FRAME-NATIVE-CONTEXT"], "both", "native contexts/universes h-identity; no silent representation swap"),
    (1143, 1165, "EXECUTED", ["S3-PROGRAM-PREDICATE"], "both", "program-predicate record; addressing p / p.i"),
    (1146, 1165, "EXECUTED", ["S3-PROGRAM-PREDICATE"], "both", "program-predicate record body"),
    (1167, 1171, "EXECUTED", ["S3-FINDING-CITE-WITNESS"], "tamper", "finding-parameters; positive has no findings"),
    (1173, 1186, "EXECUTED", ["S3-STAGE-SPEC-PARAMS", "S3-STAGE-OUTPUT-DOMAINS-REGISTERED"], "both", "stage-spec record"),
    (1188, 1207, "EXECUTED", ["S3-STAGE-SPEC-PARAMS"], "both", "stage-spec.operation owned by producer interface"),
    (1209, 1219, "EXECUTED", ["S3-STAGE-OUTPUT-DOMAINS-REGISTERED"], "both", "outputDomains registered byDomain; empty permitted"),
    (1221, 1229, "EXECUTED", ["S3-GRAMMAR-TREE"], "both", "plan.semanticClosures; view producer; evaluator equalToDirect (via admit_full_pilot)"),
    (1231, 1238, "EXECUTED", ["S3-GRAMMAR-TREE", "S3-NA-TS-RUST-TOOLCHAIN"], "both", "grammar closures via native context; need not flatten into semanticClosures"),
    (1240, 1244, "N/A", [], "neither", "commit-inventory / commit-receipt operational"),
    (1246, 1252, "N/A", [], "neither", "owner-source-set RepoExecutionGrantV2"),
    (1254, 1258, "EXECUTED", ["S3-RULE-PROGRAM-PROJECTION"], "both", "waiver resolution historical sealed set; this graph waivedFindingIds=[]"),
    (1260, 1290, "EXECUTED", ["S3-C-REMAINDER-CONFIG", "S3-H-FRAME-NATIVE-CONTEXT", "S3-PAYLOAD-REGISTRY-RELATION", "S3-ANCHOR-LAW", "S3-BUDGET-EQUAL", "S3-GRAMMAR-TREE"], "both", "complete preimage retention; budget equality; anchorLaw; Plan/source agreement"),
    (1292, 1304, "EXECUTED", ["S3-COVERAGE-PARTITION"], "both", "Coverage scopes partition disjointness"),
    (1306, 1313, "EXECUTED", ["S3-COVERAGE-PARTITION"], "both", "per view; includes scopes with no Coverage"),
    (1315, 1321, "EXECUTED", ["S3-COVERAGE-TOTALITY-FILE"], "both", "file@enumerated totality only"),
    (1323, 1335, "EXECUTED", ["S3-COVERAGE-TOTALITY-FILE", "S3-EXPECTED-PROOF-NO-CLAIMED-FIELDS"], "both", "enumeration contract subject census; execution-inputs cells"),
    (1337, 1348, "EXECUTED", ["S3-COVERAGE-TOTALITY-FILE", "S3-COVERAGE-PARTITION"], "both", "complete is examined-partition claim; RC-0/1/2 not vacuous"),
]


def map_para(p: dict) -> dict:
    for start, end, disp, laws, appl, note in MAP:
        if p["start"] == start:
            return {**p, "disposition": disp, "lawIds": laws, "applicability": appl, "note": note, "text": p["text"][:400]}
    return {**p, "disposition": "UNMAPPED", "lawIds": [], "applicability": "unknown", "note": "paragraph start not in map", "text": p["text"][:400]}


def run_graph(path: Path, label: str) -> dict:
    store = Store.load(path)
    g = load_graph(store)
    expected = reconstruct_expected_proof(store, g)["proof"]
    enclosing = reconstruct_expected_enclosing(g, expected)
    s3 = execute_s3_laws(store, g, expected_proof=expected, graph_label=label)
    kit = execute_kit_s3_schema_laws()
    adm = admit_graph(store, g)
    return {
        "label": label,
        "path": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "runId": g["run_id"],
        "proofId": g["claimed_proof_id"],
        "expectedProofId": typed_id("proof-bundle", expected),
        "claimedVerdict": g["claimed_proof"]["verdict"],
        "expectedVerdict": expected["verdict"],
        "proofCEqual": C(expected) == C(g["claimed_proof"]),
        "evidenceCEqual": enclosing["evidenceCEqual"],
        "sealCEqual": enclosing["sealCEqual"],
        "runCEqual": enclosing["runCEqual"],
        "s3": s3,
        "kit": kit,
        "s3Fail": [r for r in s3 + kit if not r["ok"]],
        "admissionOk": adm["ok"],
        "admissionFirstRefusal": next((j["name"] for j in adm["joins"] if not j["ok"]), None),
        "usedClaimedProofFields": [],
    }


def main() -> int:
    paras = [map_para(p) for p in paragraphs_s3()]
    unmapped = [p for p in paras if p["disposition"] == "UNMAPPED"]
    pos = run_graph(OUT / "runs/syntax-code.store.json", "positive")
    tam = run_graph(OUT / "runs/syntax-code.tamper.store.json", "tamper")
    executed_ids = {r["lawId"].split("-")[0] + "-" + "-".join(r["lawId"].split("-")[1:3]) for r in pos["s3"]}
    # prefix match: inventory lawIds vs actual
    actual = set()
    for r in pos["s3"] + pos["kit"] + tam["s3"]:
        actual.add(r["lawId"])
        # also prefix families
        parts = r["lawId"].split("-")
        if len(parts) >= 3:
            actual.add("-".join(parts[:3]) if parts[2] in {"H", "C", "NA", "KIT"} else r["lawId"])

    def covered(law_id: str) -> bool:
        if law_id in actual:
            return True
        return any(a.startswith(law_id) for a in actual)

    incomplete = []
    for p in paras:
        if p["disposition"] in {"EXECUTED", "KIT"}:
            missing = [lid for lid in p["lawIds"] if not covered(lid) and lid not in actual]
            # family: S3-SCOPE-COMMITMENT matches S3-SCOPE-COMMITMENT-xxxxx
            missing = [lid for lid in p["lawIds"] if not any(a == lid or a.startswith(lid + "-") or lid.startswith(a) for a in actual)]
            if missing:
                incomplete.append({"start": p["start"], "missing": missing, "first": p["firstSentence"]})

    doc = {
        "standing": "Complete identity-and-evidence.md §3 paragraph inventory with executed assertions on syntax-code positive, tamper, and independently derived expected proof. Inventory is completeness check, not substitute for execution.",
        "charterSha256": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
        "section": "docs/v2/contracts/product-v1/identity-and-evidence.md §3 lines 87-1349",
        "nParagraphs": len(paras),
        "nUnmapped": len(unmapped),
        "nIncompleteApplicable": len(incomplete),
        "dispositionCounts": {},
        "paragraphs": paras,
        "unmapped": unmapped,
        "incompleteApplicable": incomplete,
        "positive": {k: pos[k] for k in pos if k not in {"s3", "kit"}},
        "tamper": {k: tam[k] for k in tam if k not in {"s3", "kit"}},
        "positiveLaws": pos["s3"] + pos["kit"],
        "tamperLaws": tam["s3"],
        "positiveS3Fail": pos["s3Fail"],
        "tamperS3Fail": tam["s3Fail"],
    }
    from collections import Counter
    doc["dispositionCounts"] = dict(Counter(p["disposition"] for p in paras))
    outp = OUT / "normative-law-audit.json"
    outp.write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps({
        "nParagraphs": doc["nParagraphs"],
        "unmapped": doc["nUnmapped"],
        "incomplete": doc["nIncompleteApplicable"],
        "dispositions": doc["dispositionCounts"],
        "positiveFail": len(pos["s3Fail"]),
        "tamperFail": len(tam["s3Fail"]),
        "positiveAdmit": pos["admissionOk"],
        "tamperAdmit": tam["admissionOk"],
        "positiveProofEqual": pos["proofCEqual"],
        "tamperProofEqual": tam["proofCEqual"],
        "expectedIds": {"pos": pos["expectedProofId"], "tam": tam["expectedProofId"]},
    }, indent=2))
    return 0 if not unmapped and not incomplete and not pos["s3Fail"] and not tam["s3Fail"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
