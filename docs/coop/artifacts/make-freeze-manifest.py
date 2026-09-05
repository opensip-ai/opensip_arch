#!/usr/bin/env python3
"""Deterministic freeze-payload manifest for IMPLEMENTATION-FREEZE §9.2.

§9.2 specifies the recipe and leaves the execution to the signer:

    "create a deterministic file manifest for the complete `docs/coop/`
     snapshot, excluding this file and the manifest itself so neither is
     self-referential. The manifest records every other sorted relative path,
     byte length, and SHA-256 digest. Hash the canonical manifest bytes with
     SHA-256 and record that digest in this file."

Improvising that at signing time is how a payload hash ends up covering a
slightly different set of files than anyone believes it covers.  This makes it
reproducible, and — more usefully — re-runnable *after* signature, so a later
reader can ask whether the payload still hashes to what the signature claims.

DETERMINISM, which is the whole point:
  - paths are POSIX-relative to `docs/coop/`, sorted bytewise, so the order does
    not depend on filesystem enumeration order or locale;
  - the canonical form is UTF-8, LF-terminated, one record per line, no trailing
    whitespace;
  - the two self-referential files are excluded BY NAME and the exclusion is
    recorded in the header, so it cannot be silently widened;
  - nothing about the run (time, host, user, tool version) enters the hashed
    bytes.  A manifest that embedded a timestamp would never reproduce, which
    would make the payload hash unfalsifiable rather than merely unverified.

Exit codes match the corpus convention:
  0  wrote (or, under --verify, the payload matches)
  1  --verify found drift
  2  bad invocation
"""

from __future__ import annotations

import hashlib
import pathlib
import sys

COOP = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = COOP / "artifacts" / "freeze-payload-manifest.txt"

# Excluded so neither is self-referential, exactly as §9.2 requires.  Named
# here and echoed into the header: a reader can see the exclusion set without
# reading this source, and widening it changes the hashed bytes.
EXCLUDED = ("IMPLEMENTATION-FREEZE.md", "artifacts/freeze-payload-manifest.txt")

# Build products, not payload.  These are regenerable from the payload and
# their presence varies by whether anything has been executed, which would make
# the manifest depend on run history rather than on content.
SKIP_DIRS = {"__pycache__", ".git", ".DS_Store"}
SKIP_SUFFIX = (".pyc", ".pyo")


def payload_files() -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for p in COOP.rglob("*"):
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(COOP)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.name.startswith(".") or rel.suffix in SKIP_SUFFIX:
            continue
        if rel.as_posix() in EXCLUDED:
            continue
        out.append(p)
    # Sort on the POSIX string, not the path object: path ordering is
    # component-wise and would differ from a plain bytewise sort of the
    # rendered line, which is what a reader reproduces by hand.
    return sorted(out, key=lambda q: q.relative_to(COOP).as_posix())


def canonical_manifest() -> tuple[bytes, int, int]:
    lines = [
        "# IMPLEMENTATION-FREEZE §9.2 freeze payload manifest",
        "# format: <sha256>  <byteLength>  <posixRelativePath>",
        "# root: docs/coop",
        f"# excluded (self-referential, per §9.2): {', '.join(EXCLUDED)}",
        f"# skipped (build products, not payload): {', '.join(sorted(SKIP_DIRS))}, *"
        + ", *".join(SKIP_SUFFIX),
    ]
    total = 0
    files = payload_files()
    for p in files:
        data = p.read_bytes()
        total += len(data)
        rel = p.relative_to(COOP).as_posix()
        lines.append(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}")
    blob = ("\n".join(lines) + "\n").encode("utf-8")
    return blob, len(files), total


def main(argv: list[str]) -> int:
    args = argv[1:]
    if args not in ([], ["--verify"], ["--print"]):
        print(f"usage: {pathlib.Path(argv[0]).name} [--verify|--print]", file=sys.stderr)
        return 2

    blob, count, total = canonical_manifest()
    digest = hashlib.sha256(blob).hexdigest()

    if args == ["--print"]:
        sys.stdout.write(blob.decode("utf-8"))
        return 0

    if args == ["--verify"]:
        if not MANIFEST.exists():
            print(f"NO-MANIFEST: {MANIFEST.relative_to(COOP)} does not exist; nothing to verify")
            return 1
        stored = MANIFEST.read_bytes()
        if stored == blob:
            print("PAYLOAD MATCHES the stored manifest")
            print(f"  files {count}   bytes {total}   manifest sha256 {digest}")
            return 0
        print("PAYLOAD DRIFT — the stored manifest does not describe the live tree")
        old = {l.split("  ")[-1]: l for l in stored.decode("utf-8").splitlines() if not l.startswith("#")}
        new = {l.split("  ")[-1]: l for l in blob.decode("utf-8").splitlines() if not l.startswith("#")}
        for rel in sorted(set(new) - set(old)):
            print(f"  ADDED    {rel}")
        for rel in sorted(set(old) - set(new)):
            print(f"  REMOVED  {rel}")
        changed = [r for r in sorted(set(old) & set(new)) if old[r] != new[r]]
        for rel in changed:
            print(f"  CHANGED  {rel}")
        print(f"  live manifest sha256 {digest}")
        return 1

    MANIFEST.write_bytes(blob)
    print(f"WROTE {MANIFEST.relative_to(COOP)}")
    print(f"  files {count}   bytes {total}")
    print(f"  Manifest artifact: artifacts/{MANIFEST.name}")
    print(f"  Manifest SHA-256:  {digest}")
    print()
    print("  Record the digest above in §9.2. It covers the payload EXCEPT the two")
    print("  self-referential files named in the manifest header. Re-run --verify at")
    print("  any later time to establish whether the payload still hashes to it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
