"""Portable reconstruction verifier for the Claude XA-01 + XA-02/CR-25 correction.

Replaces the v1 reproduce.sh, which was NOT runnable as advertised. Three defects, all reproduced:
  1. it invoked WORK/apply-correction.py and WORK/stages/*.json without ever copying the bundled
     scripts or stage files into WORK;
  2. it used mkdir -p, so it would happily write into a populated directory;
  3. it replayed development edit stages instead of applying the authored result.
Root also asked whether the pre-copy of successor was redundant because the XA-01 applier owns
creation. Verified: it does NOT. apply-reference-correction.py reads (copy/rel) and asserts it equals
the source bytes, so it REQUIRES an existing tree; with a missing --copy it exits 1 with
FileNotFoundError. Evidence: evidence/xa01-applier-behaviour/. The pre-copy was correct.

This verifier applies the AUTHORED FULL FILES as an exact overlay, so the audit package and the XA-01
applier are no longer dependencies at all: the authored bytes already contain the XA-01 result.

Order: verify every bundled artifact against the manifest, then verify every before-hash against the
frozen source, then overlay, then verify every after-hash, then run the suites. Nothing is written
outside the new output root, and the frozen source is only ever read.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frozen-source", type=Path, required=True, help="frozen candidate25 root; read only")
    ap.add_argument("--out", type=Path, required=True, help="NEW output root; must not already exist")
    ap.add_argument("--interpreter", default=sys.executable, help="python 3.12 with jsonschema")
    ap.add_argument("--skip-suites", action="store_true")
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit("REFUSED: output root already exists: %s" % args.out)
    src = args.frozen_source.resolve()
    if not (src / "docs").is_dir():
        raise SystemExit("REFUSED: frozen source has no docs/ tree: %s" % src)
    out = args.out.resolve()
    if str(out) == str(src) or str(out).startswith(str(src) + os.sep) or str(src).startswith(str(out) + os.sep):
        raise SystemExit("REFUSED: output root overlaps the frozen source")
