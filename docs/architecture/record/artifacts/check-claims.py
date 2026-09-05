#!/usr/bin/env python3
"""Validate the claim register against the architecture/steering documents.

Implements CHK-1..CHK-4 from artifacts/claim-register.v1.json.

The failure class this exists to catch: a container's status marker silently
promotes its contents, so one claim ends up with two statuses depending on where
the reader looks. Three human audit rounds found three instances of that class;
this makes it a diff instead of a discovery.

Usage:  python3 artifacts/check-claims.py [--self-test]
Exit:   0 all checks pass · 1 findings · 2 usage/IO error
"""
from __future__ import annotations
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTER = ROOT / "artifacts" / "claim-register.v1.json"

# Weakest to strongest. A container may not present a claim above its own status.
LATTICE = {"OPEN": 0, "CANDIDATE": 1, "REOPENED": 1, "SEALED": 3}
MARKER = re.compile(r"\*\*(SEALED|CANDIDATE|REOPENED|OPEN)\b", re.I)
WEAK_WORD = r"\b(candidate|open|not settled|unsealed|reopened|no sign-?off|not.{0,20}sign-?off)\b"


def section_of(text: str, offset: int) -> str:
    """The markdown section containing `offset`, bounded by headings of the same
    or shallower depth. A character window let a marker in a PRECEDING SIBLING
    section rescue an unmarked claim (B-CSIR2-02)."""
    heads = [(m.start(), len(m.group(1))) for m in re.finditer(r"^(#{1,6}) ", text, re.M)]
    start, depth = 0, 6
    for pos, d in heads:
        if pos <= offset:
            start, depth = pos, d
        else:
            break
    end = len(text)
    for pos, d in heads:
        if pos > start and d <= depth:
            end = pos
            break
    return text[start:end]


def inline_marked(window: str, cid: str) -> bool:
    """True if `window` marks claim `cid` as weaker than its container.

    The previous pattern only recognised C-n/R-n/P-n ids, so claims such as D9,
    ARCH.PROBE-CONTRACT and METHOD.CLAIM-STATUS-INTEGRITY could not be marked at
    all — the check was unsatisfiable for them rather than merely unsatisfied.
    """
    esc = re.escape(cid)
    return bool(re.search(esc + r"[^.\n]{0,160}?" + WEAK_WORD, window, re.I)
                or re.search(WEAK_WORD + r"[^.\n]{0,160}?" + esc, window, re.I))

# Signature phrases used to find *unregistered* restatements (CHK-3).
SIGNATURES = {
    "ARCH.BASELINE.PRODUCER-DERIVED": r"only artifact (that )?liv\w+ in|only such artifact|only contract whose artifacts",
    "ARCH.IDENTITY.LATEST": r"`latest` ambiguity never arises",
    "C-1": r"semantics is the primary fact tier|primary fact tier\b",
}


def docs() -> dict[str, str]:
    out = {}
    for d in ("architecture", "steering"):
        for f in sorted((ROOT / d).glob("*.md")):
            out[f"{d}/{f.name}"] = f.read_text()
    return out


def slug(heading: str) -> str:
    """GitHub-style anchor slug for a markdown heading."""
    h = heading.strip().lstrip("#").strip().lower()
    h = re.sub(r"[^\w\s-]", "", h)
    return re.sub(r"[\s_]+", "-", h).strip("-")


def resolve_anchor(text: str, fragment: str) -> int:
    """Offset of the heading matching `fragment`, or -1.

    Coverage used to depend on a hand-added `_probe`, so 54 of 55 locations were
    silently skipped while the checker reported clean (B-CSI-01). Anchors are now
    derived from the fragments the register already carries, making coverage a
    property of the data rather than opt-in.
    """
    if not fragment:
        return -1
    want = fragment.lower()
    for m in re.finditer(r"^#{1,6} +(.+)$", text, re.M):
        if slug(m.group(1)) == want:
            return m.start()
    return -1


def status_at(text: str, offset: int) -> str | None:
    """Nearest preceding status marker — the container status governing `offset`."""
    best = None
    for m in MARKER.finditer(text, 0, offset):
        best = m.group(1).upper()
    return best


def check(reg: dict, corpus: dict[str, str], stats: dict | None = None) -> list[str]:
    findings: list[str] = []
    if stats is None:
        stats = {}
    for k in ("home_total", "home_checked", "rest_total", "rest_checked",
              "art_total", "art_checked"):
        stats.setdefault(k, 0)
    claims = {c["id"]: c for c in reg["claims"]}

    for cid, c in claims.items():
        home = LATTICE[c["status"]]

        # CHK-1a — the claim's OWN HOME must not sit inside a stronger-status
        # container. Previously only restatements were checked, so a claim whose
        # home was inside a SEALED document went unexamined — the exact Error 5
        # class this check exists to catch. Found by a negative test.
        hloc = c.get("home", "")
        hpath = hloc.split("#")[0].split(" ")[0]
        hfrag = hloc.split("#")[1].split(" ")[0] if "#" in hloc else ""
        htext = corpus.get(hpath)
        if htext is None and hpath:
            stats["art_total"] += 1
            if (ROOT / hpath).exists():
                stats["art_checked"] += 1
            else:
                findings.append(f"CHK-0 {cid}: home {hloc} does not exist")
        if htext is not None:
            probe = c.get("_probe", {}).get(hpath)
            off = htext.find(probe) if probe else resolve_anchor(htext, hfrag)
            if off < 0:
                findings.append(
                    f"CHK-0 {cid}: home location {hloc} does not resolve to a heading "
                    f"or probe — coverage is mandatory, not optional")
            stats["home_total"] += 1
            if off >= 0:
                stats["home_checked"] += 1
            if off >= 0:
                st = status_at(htext, off)
                if st and LATTICE[st] > home:
                    # An inline mark at the claim site rescues it.
                    window = section_of(htext, off)
                    if not inline_marked(window, cid):
                        findings.append(
                            f"CHK-1 {cid}: home in {hpath} sits under **{st}** but its "
                            f"status is {c['status']}, with no inline mark")

        # CHK-1 — a restatement may not sit under a stronger container status,
        # unless the clause is marked inline as a candidate.
        for r in c.get("restatements", []):
            path = r.split("#")[0].split(" ")[0]
            text = corpus.get(path)
            if text is None:
                # Non-markdown locations (artifacts) cannot be section-scoped, but
                # they must still be COUNTED and existence-checked. Excluding them
                # from the denominator let "55/55" hide 7 unexamined locations
                # (B-CSIR2-01) — Error 6 recurring in a new form.
                stats["art_total"] += 1
                if (ROOT / path).exists():
                    stats["art_checked"] += 1
                    continue
                findings.append(f"CHK-3 {cid}: restatement points at missing file {path}")
                continue
            if "marked inline" in r or "marked as candidate" in r:
                if not inline_marked(text, cid):
                    findings.append(
                        f"CHK-1 {cid}: {path} claims an inline candidate mark but none found")
                continue
            frag = r.split("#")[1].split(" ")[0] if "#" in r else ""
            anchor = c.get("_probe", {}).get(path)
            off = text.find(anchor) if anchor else resolve_anchor(text, frag)
            stats["rest_total"] += 1
            if off < 0:
                findings.append(
                    f"CHK-0 {cid}: restatement {r} does not resolve to a heading "
                    f"or probe — coverage is mandatory, not optional")
                continue
            stats["rest_checked"] += 1
            st = status_at(text, off)
            if st and LATTICE[st] > home:
                window = section_of(text, off)
                if not inline_marked(window, cid):
                    findings.append(
                        f"CHK-1 {cid}: restated in {path} under **{st}** but its "
                        f"status is {c['status']}, with no inline mark")

        # CHK-2 — a sealed claim may not depend on an unsealed one.
        if c["status"] == "SEALED":
            for dep in c.get("dependsOn", []):
                d = claims.get(dep)
                if d and d["status"] != "SEALED":
                    findings.append(
                        f"CHK-2 {cid}: SEALED but depends on {dep} ({d['status']})")

        # CHK-4 — product-owned claims may not be sealed WITHOUT a recorded disposition.
        # (Sealing with one is the whole point; the earlier phrasing forbade it outright.)
        if c.get("owner") == "product" and c["status"] == "SEALED" and not c.get("disposition"):
            findings.append(f"CHK-4 {cid}: product-owned claim is SEALED without a disposition")

        # CHK-3 — every occurrence of a retired/legacy phrasing must be gone or registered.
        sig = SIGNATURES.get(cid)
        if sig:
            known = {r.split("#")[0].split(" ")[0] for r in c.get("restatements", [])}
            for path, text in corpus.items():
                for m in re.finditer(sig, text, re.I):
                    line = text[:m.start()].count("\n") + 1
                    # Retirement context may precede OR follow the quoted phrase:
                    # "X. That argument is withdrawn" and "previously said X" both count.
                    ctx = text[max(0, m.start() - 200):m.start() + 300].lower()
                    if any(w in ctx for w in ("rejected", "withdrawn", "previously",
                                              "history", "prior", "no longer",
                                              "earlier version", "open question",
                                              "not settled", "underived")):
                        continue  # quoted as retired — fine
                    if path not in known:
                        findings.append(
                            f"CHK-3 {cid}: unregistered restatement {path}:{line}")
    # CHK-5 — prose must not cite a superseded binding artifact (B-CSI-03).
    # Status can be right in the register while readers are sent to a dead object.
    for cid, c in claims.items():
        ba = c.get("bindingArtifact")
        if not ba:
            continue
        stem = re.sub(r"\.v[\d.]+\.json$", "", ba.split("/")[-1])
        if stem == ba.split("/")[-1].replace(".json", ""):
            continue  # unversioned artifact: nothing to drift
        cur = ba.split("/")[-1]
        for path, text in corpus.items():
            for m in re.finditer(re.escape(stem) + r"\.v[\d.]+\.json", text):
                cited = m.group(0)
                if cited == cur:
                    continue
                line = text[:m.start()].count("\n") + 1
                # The exemption must sit ADJACENT to the citation. A 380-char
                # window meant an unrelated sentence containing "Earlier"
                # suppressed a real stale binding (B-CSIR2-04).
                ctx = text[max(0, m.start() - 90): m.end() + 90].lower()
                if re.search(r"\b(superseded|earlier candidate|prior version|historical)\b", ctx):
                    continue
                findings.append(
                    f"CHK-5 {cid}: {path}:{line} cites {cited} but the register binds {cur}")
    return findings


def self_test() -> int:
    """Prove the checks catch the three historical recurrences."""
    reg = {"claims": [
        {"id": "C-X", "status": "CANDIDATE", "owner": "agents",
         "home": "architecture/04-fact-plane.md",
         "restatements": ["architecture/00-overview.md"],
         "_probe": {"architecture/00-overview.md": "PROMOTED CLAIM"}},
        {"id": "S-X", "status": "SEALED", "owner": "agents",
         "home": "architecture/02-domain-model.md", "dependsOn": ["C-X"]},
        {"id": "P-X", "status": "SEALED", "owner": "product",
         "home": "architecture/01-product-boundary.md"},
    ]}
    corpus = {"architecture/00-overview.md": "## T\n\n**SEALED.** intro\n\nPROMOTED CLAIM here\n"}
    # B-CSI-02: the old self-test proved a happy path and missed the dominant live
    # failure mode — omitted coverage. It now includes an unresolvable location and
    # asserts that EVERY required location was examined.
    reg["claims"].append({"id": "U-X", "status": "CANDIDATE", "owner": "agents",
                          "home": "architecture/00-overview.md#no-such-heading",
                          "restatements": [], "dependsOn": []})
    stats: dict = {}
    got = check(reg, corpus, stats)
    expect = ["CHK-1 C-X", "CHK-2 S-X", "CHK-4 P-X", "CHK-0 U-X"]
    ok = all(any(f.startswith(e) for f in got) for e in expect)
    # coverage assertion: no location may be silently skipped
    unexamined = (stats["home_total"] - stats["home_checked"]) + \
                 (stats["rest_total"] - stats["rest_checked"])
    reported = sum(1 for f in got if f.startswith("CHK-0"))
    if unexamined != reported:
        ok = False
        print(f"  COVERAGE HOLE: {unexamined} unexamined location(s), "
              f"{reported} reported")
    print("self-test:", "PASS" if ok else "FAIL")
    for f in got:
        print("  caught:", f)
    return 0 if ok else 1


def main() -> int:
    # The exercise-wide runner standardises on ``--selftest``.  Keep the
    # hyphenated spelling for compatibility, but do not silently run the normal
    # checker when the caller asked for a self-test.
    if "--selftest" in sys.argv or "--self-test" in sys.argv:
        return self_test()
    if not REGISTER.exists():
        print(f"missing register: {REGISTER}", file=sys.stderr)
        return 2
    reg = json.loads(REGISTER.read_text())
    stats: dict = {}
    findings = check(reg, docs(), stats)
    cov = (f"{stats['home_checked']}/{stats['home_total']} homes, "
           f"{stats['rest_checked']}/{stats['rest_total']} restatements, "
           f"{stats['art_checked']}/{stats['art_total']} artifact refs")
    if not findings:
        print(f"claim register OK — {len(reg['claims'])} claims, {cov}, CHK-0..CHK-5 clean")
        return 0
    print(f"coverage: {cov}")
    print(f"{len(findings)} finding(s):")
    for f in findings:
        print("  -", f)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
