#!/usr/bin/env python3
"""Independent UCD15 lowercase samples using Python 3.12, not 3.14/NFC16."""
import json, subprocess, sys, unicodedata
from pathlib import Path

assert unicodedata.unidata_version == "15.0.0", unicodedata.unidata_version
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
    "\u1c89",
    "\ua7cb",
    "\U00010d50",
    "\U00010400",
    "AΣ" + "\u0345" * 50,
]
expected = [s.lower() for s in samples]
print(json.dumps({"unidata": unicodedata.unidata_version, "n": len(samples), "expected": expected}, ensure_ascii=True))
open(sys.argv[1], "w").write(json.dumps({"unidata": unicodedata.unidata_version, "samples": samples, "expected": expected}, ensure_ascii=True) + "\n")
