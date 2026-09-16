#!/usr/bin/env python3
"""Independent Unicode 15 default-lowercase algorithm vs Python 3.12/UCD15.

Reimplements Final_Sigma on the original string with Case_Ignorable precedence
on Cased overlap. Does not import the product generator at runtime for the
mapping itself; it rereads the three pinned sources.
"""
from pathlib import Path
import hashlib, json, sys, unicodedata

assert unicodedata.unidata_version == "15.0.0", unicodedata.unidata_version
DATA = Path(sys.argv[1])
OUT = Path(sys.argv[2])


def scalar(n):
    return 0 <= n <= 0x10FFFF and not 0xD800 <= n <= 0xDFFF


def load():
    manifest = json.loads((DATA / "sources.json").read_bytes())
    assert manifest["unicodeVersion"] == "15.0.0"
    expected = {"UnicodeData.txt", "SpecialCasing.txt", "DerivedCoreProperties.txt"}
    assert {r["file"] for r in manifest["files"]} == expected
    pins = {}
    for row in manifest["files"]:
        raw = (DATA / row["file"]).read_bytes()
        assert len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"]
        pins[row["file"]] = {"bytes": row["bytes"], "sha256": row["sha256"]}
    lower = {}
    for line in (DATA / "UnicodeData.txt").read_text().splitlines():
        fields = line.split(";")
        assert len(fields) == 15
        if fields[13]:
            lower[int(fields[0], 16)] = (int(fields[13], 16),)
    default_contexts = []
    tailored = 0
    for line in (DATA / "SpecialCasing.txt").read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        fields = [s.strip() for s in line.split(";")]
        code = int(fields[0], 16)
        image = tuple(int(s, 16) for s in fields[1].split())
        conditions = fields[4].split()
        if not conditions:
            lower[code] = image
        elif any(c in ("tr", "az", "lt") for c in conditions):
            tailored += 1
        else:
            default_contexts.append((code, image, conditions))
    assert default_contexts == [(0x03A3, (0x03C2,), ["Final_Sigma"])]
    props = {"Cased": [], "Case_Ignorable": []}
    for line in (DATA / "DerivedCoreProperties.txt").read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        fields = [x.strip() for x in line.split(";")]
        if fields[1] not in props:
            continue
        ends = [int(s, 16) for s in fields[0].split("..")]
        lo, hi = ends[0], ends[-1]
        props[fields[1]].append((lo, hi))
    for name, ranges in props.items():
        merged = []
        for lo, hi in sorted(ranges):
            if merged and lo == merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], hi)
            else:
                merged.append((lo, hi))
        props[name] = merged
    return lower, props, pins, tailored


def member(cp, ranges):
    lo, hi = 0, len(ranges)
    while lo < hi:
        mid = (lo + hi) // 2
        if ranges[mid][0] <= cp:
            lo = mid + 1
        else:
            hi = mid
    return lo > 0 and cp <= ranges[lo - 1][1]


def default_lower(text, lower, props):
    chars = list(text)
    following = [False] * len(chars)
    nxt = False
    for i in range(len(chars) - 1, -1, -1):
        following[i] = nxt
        c = ord(chars[i])
        if not member(c, props["Case_Ignorable"]):
            nxt = member(c, props["Cased"])
    before = False
    out = []
    for i, ch in enumerate(chars):
        c = ord(ch)
        if c == 0x03A3 and before and not following[i]:
            out.append("\u03c2")
        elif c in lower:
            out.append("".join(chr(n) for n in lower[c]))
        else:
            out.append(ch)
        if not member(c, props["Case_Ignorable"]):
            before = member(c, props["Cased"])
    return "".join(out)


def main():
    lower, props, pins, tailored = load()
    cased = set()
    ign = set()
    for lo, hi in props["Cased"]:
        cased.update(range(lo, hi + 1))
    for lo, hi in props["Case_Ignorable"]:
        ign.update(range(lo, hi + 1))
    overlap = sorted(cased & ign)
    samples = [
        "ES2022",
        "İ",
        "ß",
        "I",
        "ΑΣ",
        "ΣΑ",
        "Σ",
        "ΟΣ.",
        "I\u0307",
        "AΣ\u0345",
        "AΣ\u0345A",
        "1Σ",
        "AΣ.",
        "\u1c89",
        "\ua7cb",
        "\U00010d50",
        "\U00010400",
        "AΣ" + "\u0345" * 50,
        "I\u0301",
        "\u1e9e",
        "\ufb03",
        "",
        "Hello",
    ]
    if overlap:
        o = chr(overlap[0])
        samples.extend(["AΣ" + o, "AΣ" + o + "A", o + "Σ"])
    miss = []
    for s in samples:
        got = default_lower(s, lower, props)
        exp = s.lower()
        if got != exp:
            miss.append({"input": s, "algo": got, "python": exp})
    report = {
        "unidata": unicodedata.unidata_version,
        "python": sys.version.split()[0],
        "sourcePins": pins,
        "tailoredSpecialCasingRowsIgnored": tailored,
        "defaultContexts": [[0x03A3, [0x03C2], ["Final_Sigma"]]],
        "casedRanges": len(props["Cased"]),
        "ignorableRanges": len(props["Case_Ignorable"]),
        "overlapCount": len(overlap),
        "overlapHead": ["U+%04X" % n for n in overlap[:12]],
        "ypogegrammeniOverlap": 0x0345 in overlap,
        "sampleCount": len(samples),
        "mismatchCount": len(miss),
        "mismatches": miss,
        "lowerMappings": len(lower),
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps({k: report[k] for k in ("unidata", "python", "overlapCount", "ypogegrammeniOverlap", "sampleCount", "mismatchCount", "tailoredSpecialCasingRowsIgnored")}))
    if miss:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
