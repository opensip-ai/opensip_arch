#!/usr/bin/env python3
"""Read-only checks for the S-OP-2b r1 design unit."""

import hashlib
import json
import sys
from pathlib import Path

ARCH = Path(__file__).resolve().parents[6]
PARENT = "docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md"
LAW = "docs/implementation/m3/operability/o1/PROPOSAL-r2.md"
UNIT = "docs/implementation/m3/operability/s-op-2b"
RECORD = UNIT + "/successor.json"
SUBJECT = "docs/implementation/m3/operability/s-op-2b-subject.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(rel: str) -> bytes:
    return (ARCH / rel).read_bytes()


def pin_ok(row: dict, data: bytes, label: str) -> None:
    if row.get("bytes") != len(data) or row.get("sha256") != sha256(data):
        raise SystemExit(f"{label} pin mismatch for {row.get('path')}")


def owed_body() -> str:
    lines = load(LAW).decode("utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("> **S-OP-2b."))
    body = []
    for line in lines[start:]:
        if line == ">":
            body.append("")
        elif line.startswith("> "):
            body.append(line[2:])
        else:
            break
    while body and body[-1] == "":
        body.pop()
    return "\n".join(body) + "\n"


def main() -> None:
    record = json.loads(load(RECORD))
    subject = json.loads(load(SUBJECT))
    parent = load(PARENT)
    parents = record["parents"]
    if len(parents) != 1 or parents[0]["path"] != PARENT:
        raise SystemExit("parent set")
    pin_ok(parents[0], parent, "parent")
    before = parent.decode("utf-8").splitlines()[428]
    overrides = record["passageOverrides"]
    if len(overrides) != 1:
        raise SystemExit("override count")
    override = overrides[0]
    if override["parent"] != parents[0]:
        raise SystemExit("override parent pin")
    if override["selector"] != {"line": 429}:
        raise SystemExit("selector")
    if override["before"] != before:
        raise SystemExit("before text")
    harness, kept = override["after"].split("\n")
    if kept != before or not harness.startswith("| harness |"):
        raise SystemExit("after text")
    if record.get("passageSupersessions") != []:
        raise SystemExit("supersessions")
    proposal = load(UNIT + "/PROPOSAL.md").decode("utf-8")
    marker = "**S-OP-2b. The harness instrumentation sink.**"
    if proposal.split(marker, 1)[1] != owed_body().split(marker, 1)[1]:
        raise SystemExit("owed body drifted")
    files = subject["files"]
    paths = [row["path"] for row in files]
    if paths != sorted(set(paths)):
        raise SystemExit("subject paths")
    if RECORD not in paths:
        raise SystemExit("record missing from subject")
    candidates = record["candidates"]
    cand_paths = [row["path"] for row in candidates]
    if cand_paths != sorted(set(cand_paths)):
        raise SystemExit("candidate paths")
    if set(cand_paths) != set(paths) - {RECORD}:
        raise SystemExit("candidates do not cover the subject")
    by_path = {row["path"]: row for row in files}
    if by_path[RECORD]["bytes"] != len(load(RECORD)) or by_path[RECORD]["sha256"] != sha256(load(RECORD)):
        raise SystemExit("record pin")
    for row in candidates:
        if by_path[row["path"]] != row:
            raise SystemExit("candidate differs from subject")
        pin_ok(row, load(row["path"]), "candidate")
    if PARENT in cand_paths:
        raise SystemExit("parent is also a candidate")
    print("CHECKS-OK")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
