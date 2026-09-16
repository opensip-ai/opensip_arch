"""Probe v1 glob_match vs glob-pattern-contract.v1 for literal '*' candidates."""
from __future__ import annotations

import json
from pathlib import Path

V1 = Path(
    "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/workflows_model.v1.py"
)
PRESERVED = Path(
    "/tmp/opensip-implementation/m2-policy-glob-trial-21/initial-literal-star-law-mismatches.json"
)


def load_v1_glob():
    src = V1.read_text()
    start = src.index("def glob_match(pattern, path):")
    end = src.index("\ndef in_scope(")
    g = {}
    exec(src[start:end], g)
    return g["glob_match"]


def normative_seg(p: str, s: str) -> bool:
    """Contract: * = 0+ scalars in-segment; ? = one scalar; other chars match themselves.
    Braces/brackets are literal. No escapes. Consecutive stars = one star."""
    if p == "*":
        return True
    # collapse consecutive stars in the pattern segment (same matching power)
    collapsed = []
    for ch in p:
        if ch == "*" and collapsed and collapsed[-1] == "*":
            continue
        collapsed.append(ch)
    p = "".join(collapsed)

    def rec(i, j):
        if i == len(p):
            return j == len(s)
        if p[i] == "*":
            return any(rec(i + 1, k) for k in range(j, len(s) + 1))
        if p[i] == "?":
            return j < len(s) and rec(i + 1, j + 1)
        return j < len(s) and p[i] == s[j] and rec(i + 1, j + 1)

    return rec(0, 0)


def normative_glob(pattern: str, candidate: str) -> bool:
    ps, ss = pattern.split("/"), candidate.split("/")

    def rec(pi, si):
        if pi == len(ps):
            return si == len(ss)
        if ps[pi] == "**":
            return any(rec(pi + 1, k) for k in range(si, len(ss) + 1))
        return si < len(ss) and normative_seg(ps[pi], ss[si]) and rec(pi + 1, si + 1)

    return rec(0, 0)


def patched_glob_match(pattern, path):
    """Minimal correction: do not treat pattern '*' as a literal equality match."""

    def seg_match(p, s):
        if p == "*":
            return True
        i = j = 0
        star = -1
        while j < len(s):
            if i < len(p) and (p[i] == "?" or (p[i] == s[j] and p[i] != "*")):
                i += 1
                j += 1
            elif i < len(p) and p[i] == "*":
                star = i
                i += 1
                mark = j
            elif star >= 0:
                i = star + 1
                mark += 1
                j = mark
            else:
                return False
        while i < len(p) and p[i] == "*":
            i += 1
        return i == len(p)

    ps, ss = pattern.split("/"), path.split("/")

    def rec(pi, si):
        if pi == len(ps):
            return si == len(ss)
        if ps[pi] == "**":
            return any(rec(pi + 1, k) for k in range(si, len(ss) + 1))
        return si < len(ss) and seg_match(ps[pi], ss[si]) and rec(pi + 1, si + 1)

    return rec(0, 0)


def main():
    ref = load_v1_glob()
    preserved = json.loads(PRESERVED.read_text())
    extra = [
        {"pattern": "*", "candidate": "*"},
        {"pattern": "*", "candidate": "a"},
        {"pattern": "*a", "candidate": "a"},
        {"pattern": "*a", "candidate": "xa"},
        {"pattern": "a*", "candidate": "a*"},
        {"pattern": "a*", "candidate": "ab"},
        {"pattern": "**/*.ts", "candidate": "src/a.ts"},
        {"pattern": "[ab].ts", "candidate": "[ab].ts"},
        {"pattern": "*", "candidate": "＊"},  # fullwidth asterisk U+FF0A
        {"pattern": "*a", "candidate": "＊ba"},
        {"pattern": "*?", "candidate": "*"},
    ]
    rows = []
    for item in preserved + extra:
        p, c = item["pattern"], item["candidate"]
        actual = ref(p, c)
        law = normative_glob(p, c)
        patched = patched_glob_match(p, c)
        rows.append(
            {
                "pattern": p,
                "candidate": c,
                "actualHelper": actual,
                "normativeLaw": law,
                "proposedPatch": patched,
                "helperVsLaw": actual == law,
                "patchVsLaw": patched == law,
            }
        )
    mismatches = [r for r in rows if not r["helperVsLaw"]]
    patch_miss = [r for r in rows if not r["patchVsLaw"]]
    print(
        json.dumps(
            {
                "preservedCount": len(preserved),
                "rows": rows,
                "helperVsLawMismatches": mismatches,
                "patchVsLawMismatches": patch_miss,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
