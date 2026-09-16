"""Review-02 probe: hashlib oracle for raw_sha256 and product H through the public API.

gen:     writes probes/sha-inputs.hex (pattern lengths 0..1100, seeded random blobs,
         NIST CAVP SHA256 Short/Long messages checked against hashlib first, and
         large blobs around and above the 4 MiB descriptor cap).
compare: checks results/sha-outcomes.txt against hashlib, and results/h-outcomes.txt
         against hashlib over the product frame of each Rust ACCEPT canonical byte
         string in results/rust-outcomes.txt (itself compared with canonical.py).
Writes results/sha-differential.json.
"""
import hashlib
import json
import random
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
CRATE = Path("/Users/sb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sha2-const-stable-0.1.0")
SEED = 20260914
LARGE = (4194303, 4194304, 4194305, 4194306, 8388609)


def nist(name):
    text = (CRATE / "tests/data" / name).read_text()
    for length, message, digest in re.findall(r"Len = (\d+)\s+Msg = ([0-9a-f]+)\s+MD = ([0-9a-f]+)", text):
        yield bytes.fromhex(message)[: int(length) // 8], digest


def inputs():
    rng = random.Random(SEED)
    rows = []
    for length in range(1101):
        rows.append((f"pattern-{length}", bytes((i * 37 + 11) % 256 for i in range(length))))
    for index in range(300):
        length = rng.randrange(0, 1 << 16)
        rows.append((f"random-{index}-{length}", rng.randbytes(length)))
    for name in ("SHA256ShortMsg.rsp", "SHA256LongMsg.rsp"):
        for position, (data, digest) in enumerate(nist(name)):
            if hashlib.sha256(data).hexdigest() != digest:
                raise SystemExit(f"NIST vector disagrees with hashlib: {name} {position}")
            rows.append((f"{name}-{position}-{len(data)}", data))
    for length in LARGE:
        rows.append((f"large-{length}", bytes((i * 131 + 7) % 256 for i in range(length))))
    return rows


def generate():
    rows = inputs()
    with open(HERE / "sha-inputs.hex", "w") as handle:
        for _, data in rows:
            handle.write(data.hex() + "\n")
    print(json.dumps({"shaInputs": len(rows), "nistRows": sum(label.startswith("SHA256") for label, _ in rows)}))


def compare():
    rows = inputs()
    rust = (RESULTS / "sha-outcomes.txt").read_text().split("\n")[:-1]
    sha_mismatches = [label for (label, data), actual in zip(rows, rust) if hashlib.sha256(data).hexdigest() != actual]
    corpus = (HERE / "corpus.hex").read_text().split("\n")[:-1]
    outcomes = (RESULTS / "rust-outcomes.txt").read_text().split("\n")[:-1]
    h_lines = (RESULTS / "h-outcomes.txt").read_text().split("\n")[:-1]
    h_mismatches = []
    h_checked = 0
    for index, (outcome, actual) in enumerate(zip(outcomes, h_lines)):
        if outcome.startswith("ACCEPT "):
            canonical = bytes.fromhex(outcome[len("ACCEPT "):])
            frame = b"opensip.product.v1\x00probe\x00" + len(canonical).to_bytes(8, "big") + canonical
            h_checked += 1
            if hashlib.sha256(frame).hexdigest() != actual:
                h_mismatches.append(index)
        elif actual != "-":
            h_mismatches.append(index)
    result = {
        "shaInputs": len(rows),
        "shaOutcomes": len(rust),
        "shaMismatches": sha_mismatches[:50],
        "nistRows": sum(label.startswith("SHA256") for label, _ in rows),
        "largeLengths": list(LARGE),
        "corpusCases": len(corpus),
        "hOutcomes": len(h_lines),
        "hAcceptsChecked": h_checked,
        "hMismatches": h_mismatches[:50],
    }
    result["passed"] = (
        len(rust) == len(rows)
        and not sha_mismatches
        and len(h_lines) == len(outcomes) == len(corpus)
        and h_checked > 0
        and not h_mismatches
    )
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "sha-differential.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["gen"]:
        generate()
    elif sys.argv[1:] == ["compare"]:
        raise SystemExit(compare())
    else:
        raise SystemExit("usage: sha_differential.py gen|compare")
