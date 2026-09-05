#!/usr/bin/env python3
"""Conformance checker for the candidate VERSIONING v5 EP5/RT10 join."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import pathlib
import sys
from typing import Any, Callable


HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v5.json"
V4 = HERE / "versioning-policy.v4.json"
V4_CHECKER = HERE / "check-versioning.py"
EP5 = HERE / "evaluation-proof.v5.json"
EP_CHECKER = HERE / "check-evaluation-proof.py"
RT10 = HERE / "retention-tiers.v10.json"
RT_CHECKER = HERE / "check-retention-custody.py"

PINS = {
    V4: "8e6933b287a8082ea27647860938bd9cdae93b37132bba21221c2c24b40069e6",
    V4_CHECKER: "67a45b275908afc4bd04cee6c15400f5d429f9f209854630c1caf5a43cf13227",
    EP5: "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    EP_CHECKER: "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    RT10: "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026",
    RT_CHECKER: "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
}

EP_APIS = [
    "resolve_semantic_object_bindings",
    "derive_semantic_requirements",
    "derive_raw_proof_requirements",
    "encode_semantic_object_binding",
    "derive_transitive_requirements",
]
RT_APIS = [
    "resolve_semantic_object_bindings",
    "derive_semantic_requirements",
    "derive_raw_proof_requirements",
    "derive_transitive_requirements",
    "encode_semantic_object_binding",
    "derive_unit_id",
    "encode_semantic_custody_unit",
    "semantic_closure_commitment",
    "derive_effective_capability",
]

ROWS = [
    (
        "historical-semantics",
        "sha256:d6a8d086d9ee0f2693f599ce39ecf90c0be65fd9a9127ddfd95572a2c95c3e04",
        ["predicate-semantics", "policy-semantics"],
        "predicate-semantics",
    ),
    (
        "historical-manifest",
        "sha256:11e923bffcc99c94372d7b575d733b79787da09d5d06286732c691b1158828fa",
        ["verifier-manifest"],
        "verifier-manifest",
    ),
    (
        "historical-executable",
        "sha256:e3be6c3634ac045fd02d4753ac61ed6d9b82ea161e106c143de69a2f196467a5",
        ["verifier-executable"],
        "verifier-executable",
    ),
    (
        "historical-signature",
        "sha256:249a77c07b91bd865b4873c586ea4e41681be89d8d227590bfc44a3b33402ac5",
        ["bundle-signature"],
        "bundle-signature",
    ),
    (
        "historical-trust-root",
        "sha256:b4834d2eb7324dbde0aa0c9c461bedaae1ba6317b02fd441612b96dd4b4778bf",
        ["verifier-trust-root"],
        "verifier-trust-root",
    ),
    (
        "historical-public-key",
        "sha256:21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9",
        ["verifier-public-key"],
        "verifier-public-key",
    ),
]


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def expected_join() -> dict[str, Any]:
    roles = [row[0] for row in ROWS]
    return {
        "id": "VERSIONING-V5-EP5-RT10-CAPABILITY-JOIN",
        "dependencyDirection": "evaluation-proof.v5 -> retention-tiers.v10 -> versioning-policy.v5; this join has no downstream dependency",
        "sources": {
            "evaluationProof": {
                "artifact": "evaluation-proof.v5.json",
                "sha256": PINS[EP5],
                "checker": "check-evaluation-proof.py",
                "checkerSha256": PINS[EP_CHECKER],
                "grammarSha256": "343889cf713931b0e228d84de82cb67d8cb22cc13ae2b3cc71302476f89ef9e0",
                "acceptedVectorId": "EP5-POS-NOMATCH-PASS",
                "requiredCheckerApi": EP_APIS,
            },
            "retentionCustody": {
                "artifact": "retention-tiers.v10.json",
                "sha256": PINS[RT10],
                "checker": "check-retention-custody.py",
                "checkerSha256": PINS[RT_CHECKER],
                "grammarSha256": "abd8c541da028f2a273cc509bb8a2bc1c19eb78618ea56676ac301a83dd82ef8",
                "acceptedClosureCommitment": "sha256:3e2e151273a69e1f9ccb0272f6a507de45e9fd1f43e4094507537ee1e34cac57",
                "requiredCheckerApi": RT_APIS,
            },
        },
        "dependencyProjection": "VERSIONING returns the exact selected semantics, manifest, native payload, detached signature, trust root and raw public-key refs as typed raw-CAS dependencies, each with minimum verifiable capability and typed availability/refusal.",
        "exactSetRule": "Map the six EP5 historical roles to the v4 fixture kinds below, require exact ref and minimum-capability equality, and require all six rows exactly once. RT10 proofRefs must contain the same six typed raw keys. No alias, omission, duplicate, unreachable edge, weakening, or strengthening is valid.",
        "crosswalk": [
            {
                "role": role,
                "ref": ref,
                "allowedVersioningKinds": kinds,
                "selectedFixtureKind": selected,
                "requiredForCapability": "verifiable",
            }
            for role, ref, kinds, selected in ROWS
        ],
        "negativeControls": [
            *[
                {
                    "id": f"VER5-HIST-OMIT-{role.upper()}",
                    "mutation": "omit-row",
                    "role": role,
                    "expected": "REJECT",
                }
                for role in roles
            ],
            *[
                {
                    "id": f"VER5-HIST-MISLABEL-{role.upper()}",
                    "mutation": "mislabel-role-or-kind",
                    "role": role,
                    "expected": "REJECT",
                }
                for role in roles
            ],
            {
                "id": "VER5-HIST-WRONG-MINIMUM",
                "mutation": "replace-verifiable-with-recorded-or-replayable",
                "expected": "REJECT",
            },
            {
                "id": "VER5-HIST-DESCRIPTOR-ONLY",
                "mutation": "replace-native-payload-by-descriptor",
                "expected": "REJECT",
            },
            {
                "id": "VER5-HIST-UNKNOWN-ROLE",
                "mutation": "add-unknown-role",
                "expected": "REJECT",
            },
        ],
        "forbidden": "Do not copy capability ranks, create a second lattice or demotion state machine, mutate sealedCapability, use TOFU/network lookup, accept descriptor/signature presence as payload custody, or include current availability/effectiveCapability in immutable semantics.",
        "authoritativeRead": "Unavailable or incompatible custody refuses through existing D9 vocabulary. VERSIONING adds no D9 code, and read-time availability never changes a sealed Run.",
    }


def function_names(path: pathlib.Path) -> set[str]:
    tree = ast.parse(path.read_text())
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def check(value: Any) -> list[str]:
    out: list[str] = []
    if not isinstance(value, dict):
        return ["root must be an object"]
    for path, expected in PINS.items():
        if not path.exists():
            out.append(f"missing pinned dependency {path.name}")
        elif sha256(path) != expected:
            out.append(f"pinned dependency drift: {path.name}")

    if value.get("artifact") != "opensip.versioning-policy" or value.get("version") != 5:
        out.append("artifact/version must be opensip.versioning-policy v5")
    if value.get("status") != "CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW":
        out.append("v5 must remain candidate awaiting independent combined rereview")
    if value.get("supersedes") != 4:
        out.append("v5 must supersede v4")
    rev = value.get("successorRevision")
    if not isinstance(rev, dict) or rev.get("applicationState") != "NOT-APPLIED" or rev.get("authorityClaim") != "NONE":
        out.append("successorRevision must be NOT-APPLIED with no authority claim")
    else:
        pred = rev.get("predecessor", {})
        if pred.get("sha256") != PINS[V4] or pred.get("checkerSha256") != PINS[V4_CHECKER]:
            out.append("successorRevision predecessor pins drift")

    try:
        v4 = load(V4)
        old = v4["historicalSemanticsPolicy"]
        new = value["historicalSemanticsPolicy"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        out.append(f"historicalSemanticsPolicy unavailable: {exc}")
        return out
    if set(old) != set(new):
        out.append("historicalSemanticsPolicy key set must remain exactly v4")
    for key in sorted(set(old) - {"capabilityJoin"}):
        if new.get(key) != old.get(key):
            out.append(f"v4 custody subtree mutated: historicalSemanticsPolicy.{key}")
    join = new.get("capabilityJoin")
    if join != expected_join():
        out.append("capabilityJoin differs from the exact EP5/RT10 join")
    if "evidence" in json.dumps(join, sort_keys=True).lower():
        out.append("capabilityJoin must not mention or depend on Evidence")

    try:
        ep5 = load(EP5)
        rt10 = load(RT10)
        if ep5.get("normativePreimageGrammarSha256") != expected_join()["sources"]["evaluationProof"]["grammarSha256"]:
            out.append("EP5 grammar hash does not match the v5 join")
        if rt10["capabilityClosure"].get("closureGrammarSha256") != expected_join()["sources"]["retentionCustody"]["grammarSha256"]:
            out.append("RT10 grammar hash does not match the v5 join")
        if rt10["capabilityClosure"]["semanticClosure"].get("closureCommitment") != expected_join()["sources"]["retentionCustody"]["acceptedClosureCommitment"]:
            out.append("RT10 accepted closure commitment does not match the v5 join")
        if rt10["capabilityClosure"]["source"].get("requiredCheckerApi") != RT_APIS:
            out.append("RT10 checker API list differs from the v5 join")
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        out.append(f"EP5/RT10 dependency structure unavailable: {exc}")

    names = function_names(EP_CHECKER) | function_names(RT_CHECKER)
    missing = sorted((set(EP_APIS) | set(RT_APIS)) - names)
    if missing:
        out.append(f"pinned checker API missing definitions: {missing}")

    try:
        fixture = next(
            x
            for x in old["crossMajorFixtures"]
            if x.get("id") == "VER4-HIST-PREDICATE-V1-ON-HOST-V2"
        )
        v4_required = sorted(
            (
                x["ref"],
                x["kind"],
                x["requiredForCapability"],
            )
            for x in fixture["expect"]["requiredDependencies"]
        )
        v5_required = sorted(
            (row[1], row[3], "verifiable")
            for row in ROWS
        )
        if v4_required != v5_required:
            out.append("six-row crosswalk is not exact-equal to the v4 fixture dependency set")

        ep_hist = ep5["versioningV4RoleJoin"]["historicalDependencies"]
        ep_set = sorted((x["role"], x["ref"], x["requiredForCapability"]) for x in ep_hist)
        expected_ep = sorted((role, ref, "verifiable") for role, ref, _, _ in ROWS)
        if ep_set != expected_ep:
            out.append("EP5 historical dependency roles/refs do not equal the crosswalk")

        proof_refs = rt10["capabilityClosure"]["semanticClosure"]["proofRefs"]
        rt_set = {(x["recordCasRef"], x["requiredForCapability"]) for x in proof_refs}
        for _, ref, _, _ in ROWS:
            if (ref, "verifiable") not in rt_set:
                out.append(f"RT10 proofRefs omit v4 custody ref {ref}")
    except (KeyError, StopIteration, TypeError) as exc:
        out.append(f"cross-artifact six-row join unavailable: {exc}")
    return out


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _join(v: dict[str, Any]) -> dict[str, Any]:
    return v["historicalSemanticsPolicy"]["capabilityJoin"]


MUTATIONS: list[Mutation] = []
for index, (role, *_rest) in enumerate(ROWS):
    MUTATIONS.append((f"omit {role}", lambda v, i=index: _join(v)["crosswalk"].pop(i)))
for index, (role, *_rest) in enumerate(ROWS):
    MUTATIONS.append((f"mislabel {role}", lambda v, i=index: _join(v)["crosswalk"][i].__setitem__("role", "historical-unknown")))
MUTATIONS.extend(
    [
        ("weaken required capability", lambda v: _join(v)["crosswalk"][0].__setitem__("requiredForCapability", "recorded")),
        ("strengthen required capability", lambda v: _join(v)["crosswalk"][0].__setitem__("requiredForCapability", "replayable")),
        ("drift EP5 hash", lambda v: _join(v)["sources"]["evaluationProof"].__setitem__("sha256", "0" * 64)),
        ("drift RT10 hash", lambda v: _join(v)["sources"]["retentionCustody"].__setitem__("sha256", "0" * 64)),
        ("inject Evidence dependency", lambda v: _join(v).__setitem__("evidence", {"sha256": "0" * 64})),
        ("mutate preserved trust model", lambda v: v["historicalSemanticsPolicy"]["trustModel"].__setitem__("networkLookup", True)),
        ("drop negative control", lambda v: _join(v)["negativeControls"].pop()),
        ("enable TOFU", lambda v: _join(v).__setitem__("forbidden", "TOFU allowed")),
        ("replace payload by descriptor", lambda v: _join(v)["crosswalk"][2].__setitem__("selectedFixtureKind", "verifier-descriptor")),
    ]
)


def selftest(base: dict[str, Any]) -> int:
    findings = check(base)
    if findings:
        print(f"REFUSING selftest: base has {len(findings)} finding(s)")
        for finding in findings[:10]:
            print("  -", finding)
        return 1
    escaped = 0
    for name, mutate in MUTATIONS:
        candidate = copy.deepcopy(base)
        before = json.dumps(candidate, sort_keys=True, separators=(",", ":"))
        mutate(candidate)
        after = json.dumps(candidate, sort_keys=True, separators=(",", ":"))
        if before == after or not check(candidate):
            escaped += 1
            print(f"ESCAPE  {name}")
        else:
            print(f"reject  {name}")
    if escaped:
        print(f"{escaped}/{len(MUTATIONS)} mutations escaped")
        return 1
    print(f"all {len(MUTATIONS)} mutations rejected")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if not args.path.exists():
        print(f"missing contract: {args.path}", file=sys.stderr)
        return 2
    value = load(args.path)
    if args.selftest:
        return selftest(value)
    findings = check(value)
    if findings:
        print(f"{len(findings)} finding(s) in {args.path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        "versioning v5 OK — v4 custody preserved, EP5/RT10 pins exact, "
        "six historical dependencies joined, candidate NOT-APPLIED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
