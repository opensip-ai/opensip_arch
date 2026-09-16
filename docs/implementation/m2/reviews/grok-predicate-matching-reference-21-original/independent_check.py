"""Independent local reference checks. Not a copy of evidence/check-matching.py.
Declarative glob law from glob-pattern-contract.v1.md. ASCII ordinal 0|[1-9][0-9]*.
No full Run or replay claim.
"""
from __future__ import annotations

import ast
import functools
import hashlib
import itertools
import json
import re
import sys
import types
import unicodedata
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
UNIT = ARCH / "docs/implementation/m2/predicate-matching-reference-selection-v1"
OLD_I = ARCH / "docs/implementation/m2/recognition-derived-reference-selection-v1/reference/identity_model.py"
OLD_W = ARCH / "docs/coop/design-corrections/workflows/workflows_model.v1.py"
NEW_I = UNIT / "reference/identity_model.py"
NEW_W = UNIT / "reference/workflows_model.v1.py"
SS = ARCH / "docs/implementation/m1/source-selection-v2/successor.json"

ORDINAL = re.compile(r"^(?:0|[1-9][0-9]*)$")


class AdmissionError(ValueError):
    pass


def sha(p: Path) -> tuple[int, str]:
    b = p.read_bytes()
    return len(b), hashlib.sha256(b).hexdigest()


def extract(path: Path, names: set[str]) -> dict:
    module = ast.parse(path.read_bytes())
    nodes = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == names, (path, {n.name for n in nodes}, names)
    env = {"C": types.SimpleNamespace(AdmissionError=AdmissionError)}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), env)
    return env


def remainder_ast(src: str, drop: str) -> str:
    m = ast.parse(src)
    m.body = [n for n in m.body if not (isinstance(n, ast.FunctionDef) and n.name == drop)]
    return ast.dump(m, include_attributes=False)


def effective_workflow_src() -> str:
    raw = OLD_W.read_text()
    record = json.loads(SS.read_bytes())
    override = next(o for o in record["passageOverrides"] if "workflows_model.v1.py" in o["parent"]["path"])
    assert override["selector"]["line"] == 380
    assert raw.splitlines()[379] == override["before"]
    assert raw.count(override["before"]) == 1
    return raw.replace(override["before"], override["after"])


# Contract law: split on '/', ordinary * = 0+ scalars, ? = 1 scalar, others literal,
# whole-segment ** = 0+ segments. Star is decided before literal equality.
@functools.lru_cache(None)
def ordinary(pattern: str, candidate: str) -> bool:
    if pattern == "":
        return candidate == ""
    if pattern[0] == "*":
        return any(ordinary(pattern[1:], candidate[k:]) for k in range(len(candidate) + 1))
    if candidate == "":
        return False
    if pattern[0] == "?":
        return ordinary(pattern[1:], candidate[1:])
    return pattern[0] == candidate[0] and ordinary(pattern[1:], candidate[1:])


def normative(pattern: str, candidate: str) -> bool:
    p, s = pattern.split("/"), candidate.split("/")

    @functools.lru_cache(None)
    def walk(i: int, j: int) -> bool:
        if i == len(p):
            return j == len(s)
        if p[i] == "**":
            return any(walk(i + 1, k) for k in range(j, len(s) + 1))
        return j < len(s) and ordinary(p[i], s[j]) and walk(i + 1, j + 1)

    return walk(0, 0)


def address_result(fn, tree, address):
    try:
        return {"node": fn(tree, address)}
    except AdmissionError as e:
        return {"refusal": str(e)}
    except Exception as e:
        return {"exception": type(e).__name__}


def main() -> None:
    effective = effective_workflow_src()
    candidate_w = NEW_W.read_text()
    old_i_src = OLD_I.read_text()
    new_i_src = NEW_I.read_text()

    ast_identity = remainder_ast(old_i_src, "predicate_node_at") == remainder_ast(new_i_src, "predicate_node_at")
    ast_workflow_effective = remainder_ast(effective, "glob_match") == remainder_ast(candidate_w, "glob_match")
    ast_workflow_raw = remainder_ast(OLD_W.read_text(), "glob_match") == remainder_ast(candidate_w, "glob_match")
    interruption_in_candidate = (
        "for r in results if r['outcome'] == 'completed' and r.get('result', {}).get('runId')"
        in candidate_w
        and "for r in required if r['outcome'] == 'completed' and r.get('result', {}).get('runId')"
        not in candidate_w
    )

    old_glob = extract(OLD_W, {"glob_match"})["glob_match"]
    new_glob = extract(NEW_W, {"glob_match"})["glob_match"]
    old_env = extract(OLD_I, {"predicate_node_at", "predicate_child_addresses"})
    new_env = extract(NEW_I, {"predicate_node_at", "predicate_child_addresses"})

    strings = ["".join(p) for n in range(5) for p in itertools.product("ab*?/", repeat=n)]
    extras = [
        ("*a", "*ba"),
        ("a*b", "a*xb"),
        ("**a", "**ba"),
        ("*?", "*ab"),
        ("**/*.ts", "a.ts"),
        ("**/*.ts", "src/a.ts"),
        ("?.ts", "é.ts"),
        ("?.ts", "e\u0301.ts"),
        ("?", "💠"),
        ("[ab]", "a"),
        ("[ab]", "[ab]"),
        ("{a,b}", "a"),
        ("{a,b}", "{a,b}"),
        ("src/**", "src"),
        ("src/", "src"),
        ("a/**/b", "a/x/y/b"),
        ("a/*/b", "a//b"),
    ]
    count = 0
    changes = 0
    mismatches = 0
    examples = []
    for p, s in itertools.chain(itertools.product(strings, strings), extras):
        before, after, want = old_glob(p, s), new_glob(p, s), normative(p, s)
        count += 1
        if after != want:
            mismatches += 1
            if mismatches <= 8:
                print("MISMATCH", p, s, before, after, want, file=sys.stderr)
        if before != after:
            changes += 1
            if len(examples) < 12:
                examples.append({"pattern": p, "candidate": s, "before": before, "after": after})

    original = json.loads((UNIT / "evidence/original-glob-counterexamples.json").read_bytes())
    original_ok = True
    for row in original:
        helper_old = old_glob(row["pattern"], row["candidate"])
        helper_new = new_glob(row["pattern"], row["candidate"])
        law = normative(row["pattern"], row["candidate"])
        if helper_old != row["actualReference"] or law != row["normativeWildcardLawExpected"]:
            original_ok = False
        if helper_new is not True or law is not True:
            original_ok = False

    contract_rows = [
        ("**/*.ts", "a.ts", True),
        ("**/*.ts", "src/nested/a.ts", True),
        ("*.ts", "src/a.ts", False),
        ("src/**", "src", True),
        ("src/**", "src/legacy.js", True),
        ("src/**", "src/nested/legacy.js", True),
        ("src/**/*", "src", False),
        ("src/**/*", "src/legacy.js", True),
        ("a/**/b", "a/b", True),
        ("a/**/b", "a/x/y/b", True),
        ("a/*/b", "a/b", False),
        ("a**b", "a/x/b", False),
        ("a**b", "axxb", True),
        ("*", ".hidden", True),
        ("a.ts", "A.ts", False),
        ("a.ts", "a.ts.extra", False),
        ("?.ts", "é.ts", True),
        ("?.ts", "e\u0301.ts", False),
        ("[ab].ts", "a.ts", False),
        ("[ab].ts", "[ab].ts", True),
        ("{a,b}.ts", "a.ts", False),
        ("{a,b}.ts", "{a,b}.ts", True),
        ("src/", "src", False),
        ("*", "*", True),
        ("?", "*", True),
        ("*a", "＊ba", True),
    ]
    contract_ok = all(new_glob(p, s) is want and normative(p, s) is want for p, s, want in contract_rows)

    leaf = {"op": "exists"}
    tree = {"op": "and", "operands": [leaf, {"op": "not", "operand": leaf}, {"op": "or", "operands": [leaf, leaf]}]}
    ascii_addresses = [
        "p",
        "p.0",
        "p.1",
        "p.1.0",
        "p.2",
        "p.2.0",
        "p.2.1",
        "p.3",
        "p.0.0",
        "p.1.1",
        "p.00",
        "p.01",
        "p.",
        "p..0",
        "q",
        "P",
        "p.-1",
        "p.+0",
        "p. 0",
        "p.0 ",
        "p.0\n",
        "p.1_0",
        "p." + "9" * 4094,
    ]
    ascii_equal = True
    ascii_order_ok = True
    for address in ascii_addresses:
        before = address_result(old_env["predicate_node_at"], tree, address)
        after = address_result(new_env["predicate_node_at"], tree, address)
        if before != after:
            ascii_equal = False
        parts = address.split(".")
        if parts[0] == "p" and any(parts[1:]):
            bad = any(not ORDINAL.fullmatch(part or "") for part in parts[1:])
            if bad and after != {"refusal": "PREDICATE_ADDRESS"}:
                ascii_order_ok = False

    # Bound: p + '.' + 4094 nines = 4096, schema Text maxLength.
    bound_addr = "p." + "9" * 4094
    assert len(bound_addr) == 4096
    bound_result = address_result(new_env["predicate_node_at"], tree, bound_addr)
    # huge ASCII ordinal is well-formed spelling, then RANGE
    bound_ok = bound_result == {"refusal": "PREDICATE_ADDRESS_RANGE"}

    numeric = [chr(n) for n in range(128, 0x110000) if chr(n).isdigit()]
    unicode_count = 0
    unicode_changed = []
    unicode_after_ok = True
    for part in numeric + ["٠١", "０１", "٠1", "0١", "１0", "²0", "𝟘1"]:
        address = "p." + part
        before = address_result(old_env["predicate_node_at"], tree, address)
        after = address_result(new_env["predicate_node_at"], tree, address)
        unicode_count += 1
        if after != {"refusal": "PREDICATE_ADDRESS"}:
            unicode_after_ok = False
        if before != after:
            unicode_changed.append({"address": address, "before": before, "after": after})

    stack = [(tree, "p")]
    emitted = 0
    roundtrip_ok = True
    while stack:
        node, address = stack.pop()
        emitted += 1
        if new_env["predicate_node_at"](tree, address) != node:
            roundtrip_ok = False
        if new_env["predicate_child_addresses"](node, address) != old_env["predicate_child_addresses"](node, address):
            roundtrip_ok = False
        children = node.get("operands", [node["operand"]] if "operand" in node else [])
        for i, child in enumerate(children):
            child_addr = address + "." + str(i)
            if not ORDINAL.fullmatch(str(i)):
                roundtrip_ok = False
            stack.append((child, child_addr))

    v3 = (ARCH / "docs/coop/design-corrections/workflows/workflows_model.v3.py").read_text()
    first_kind = "kind=('symbol' if subject_kind=='export' else subject_kind) if subject_kind else next((k for k in kinds if k),None)"
    v3_pin = sha(ARCH / "docs/coop/design-corrections/workflows/workflows_model.v3.py")

    out = {
        "python": sys.version.split()[0],
        "unicode": unicodedata.unidata_version,
        "unchangedAstOutsideTwoFunctionsAgainstSelectedEffectivePredecessor": ast_identity and ast_workflow_effective,
        "inheritedInterruptionOverridePreserved": interruption_in_candidate and ast_workflow_effective and not ast_workflow_raw,
        "globCases": count,
        "globChangedResults": changes,
        "globMismatches": mismatches,
        "globChangeExamples": examples,
        "asciiAddressControls": len(ascii_addresses),
        "unicodeAddressControls": unicode_count,
        "unicodeChangedResults": len(unicode_changed),
        "unicodeChangeExamples": unicode_changed[:12],
        "emittedAddressRoundTrips": emitted,
        "originalCounterexamplesCorrected": original_ok,
        "contractExamplesMatchLawAndCandidate": contract_ok,
        "asciiControlsUnchanged": ascii_equal and ascii_order_ok,
        "schemaBound4096RangeOnWellFormedOverIndex": bound_ok,
        "unicodeAllRefusePredicateAddress": unicode_after_ok,
        "emittedRoundTripsOk": roundtrip_ok,
        "firstKindFallbackPresentInUnchangedV3": first_kind in v3,
        "workflowsV3Pin": {"bytes": v3_pin[0], "sha256": v3_pin[1]},
        "scope": "Local actual reference function/AST checks, independent declarative glob law; no complete Run or replay.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
