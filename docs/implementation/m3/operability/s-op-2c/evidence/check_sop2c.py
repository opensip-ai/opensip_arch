#!/usr/bin/env python3
"""Read-only checks for the S-OP-2c r1 design unit (the four record tables).

Usage: check_sop2c.py [--product PATH] [--product-commit SHA] [--libc-crate PATH]

It reads the architecture files in place, product files with `git show` at the
pinned product commit, and the pinned libc crate archive. It writes nothing,
takes no lock and runs no cargo.
"""

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path

ARCH = Path(__file__).resolve().parents[6]
PARENT = "docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md"
UNIT = "docs/implementation/m3/operability/s-op-2c"
RECORD = UNIT + "/successor.json"
SUBJECT = "docs/implementation/m3/operability/s-op-2c-subject.json"
PRODUCT_COMMIT = "5de9fd4740ea17018d0bd3fbff9496c94ddacda9"

P3T = ("docs/coop/design-corrections/native/protocol3-transitions.v1.json",
       "b0aca55d89482be14e9c34554c1febb66d9751754b7c3057a383a010515feb0b")
T2O = ("docs/coop/design-corrections/native/typescript-protocol2-order.v1.json",
       "007ef7affce224c7bac6af3bb7897e86691085e2dd788f4a613e45c1fa5b8bbb")
STARTUP = ("docs/coop/design-corrections/native/provider-startup.schemas.v1.json",
           "1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c")

REAPED_BEFORE = "`signal` K1 (Signal), optional"
REAPED_AFTER = "`signal` K1 (ChildSignal, item 23a), optional"
BEGIN = "<!-- S-OP-2c item 23a begins -->"
END = "<!-- S-OP-2c item 23a ends -->"
K1 = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}\Z")

# POSIX.1-2017 <signal.h> signals with default action T or A.
POSIX_TERMINATING = {
    "SIGABRT", "SIGALRM", "SIGBUS", "SIGFPE", "SIGHUP", "SIGILL", "SIGINT", "SIGKILL",
    "SIGPIPE", "SIGPOLL", "SIGPROF", "SIGQUIT", "SIGSEGV", "SIGSYS", "SIGTERM", "SIGTRAP",
    "SIGUSR1", "SIGUSR2", "SIGVTALRM", "SIGXCPU", "SIGXFSZ",
}
LIBC_SETS = {
    "macos": ["src/unix/mod.rs", "src/unix/bsd/mod.rs", "src/unix/bsd/apple/mod.rs"],
    "linux-x86_64-gnu": [
        "src/unix/mod.rs", "src/unix/linux_like/mod.rs", "src/unix/linux_like/linux/mod.rs",
        "src/unix/linux_like/linux/arch/generic/mod.rs", "src/unix/linux_like/linux/gnu/mod.rs",
        "src/unix/linux_like/linux/gnu/b64/mod.rs", "src/unix/linux_like/linux/gnu/b64/x86_64/mod.rs",
    ],
    "linux-aarch64-gnu": [
        "src/unix/mod.rs", "src/unix/linux_like/mod.rs", "src/unix/linux_like/linux/mod.rs",
        "src/unix/linux_like/linux/arch/generic/mod.rs", "src/unix/linux_like/linux/gnu/mod.rs",
        "src/unix/linux_like/linux/gnu/b64/mod.rs", "src/unix/linux_like/linux/gnu/b64/aarch64/mod.rs",
    ],
}


class CheckError(Exception):
    pass


def need(cond: bool, label: str) -> None:
    if not cond:
        raise CheckError(label)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def arch(rel: str) -> bytes:
    return (ARCH / rel).read_bytes()


def arch_pinned(pin) -> bytes:
    data = arch(pin[0])
    need(sha256(data) == pin[1], f"architecture pin {pin[0]}")
    return data


class Product:
    def __init__(self, root: Path, commit: str):
        self.root, self.commit = root, commit
        self.env = {k: v for k, v in os.environ.items()
                    if k not in ("GIT_DIR", "GIT_WORK_TREE") and not k.startswith("GIT_CONFIG")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")

    def show(self, rel: str) -> bytes:
        out = subprocess.run(["git", "-C", str(self.root), "show", f"{self.commit}:{rel}"],
                             capture_output=True, env=self.env, check=False)
        need(out.returncode == 0, f"git show {rel}")
        return out.stdout


def enum_members(source: str, name: str) -> list:
    lines = source.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == f"pub enum {name} {{"), None)
    need(start is not None, f"generated enum {name}")
    members = []
    for line in lines[start + 1:]:
        if line.strip() == "}":
            return members
        match = re.search(r'#\[serde\(rename = "([^"]+)"\)\]', line)
        if match:
            members.append(match.group(1))
    raise CheckError(f"unterminated enum {name}")


def passage() -> str:
    text = arch(UNIT + "/PROPOSAL.md").decode("utf-8")
    need(text.count(BEGIN) == 1 and text.count(END) == 1, "passage markers")
    body = text.split(BEGIN, 1)[1].split(END, 1)[0]
    need(body.startswith("\n") and body.endswith("\n"), "passage framing")
    return body[1:-1]


def table_members(text: str, name: str) -> list:
    lines = text.split("\n")
    heads = [i for i, line in enumerate(lines) if line.startswith(f"- **`{name}`** (")]
    need(len(heads) == 1, f"table heading {name}")
    for line in lines[heads[0] + 1:]:
        if line.startswith("- "):
            break
        if line.startswith("  - Members: "):
            return re.findall(r"`([^`]+)`", line)
    raise CheckError(f"members line {name}")


def provenance(text: str, name: str) -> str:
    line = next(line for line in text.split("\n") if line.startswith(f"- **`{name}`** ("))
    return re.match(r"- \*\*`[^`]+`\*\* \(`([a-z-]+)`", line).group(1)


def libc_constants(crate: Path, lock: str) -> dict:
    data = crate.read_bytes()
    block = re.search(r'name = "libc"\nversion = "0\.2\.189"\nsource = "[^"]+"\nchecksum = "([0-9a-f]{64})"', lock)
    need(block is not None, "Cargo.lock libc 0.2.189 entry")
    need(sha256(data) == block.group(1), "libc crate archive checksum differs from Cargo.lock")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(gzip.decompress(data)), mode="r:") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.startswith("libc-0.2.189/"):
                rel = member.name[len("libc-0.2.189/"):]
                if any(rel in paths for paths in LIBC_SETS.values()):
                    files[rel] = tar.extractfile(member).read().decode("utf-8")
    result = {}
    for platform, paths in LIBC_SETS.items():
        values = {}
        for rel in paths:
            need(rel in files, f"libc file {rel}")
            for name, value in re.findall(r"pub const (SIG[A-Z0-9]+): (?:crate::)?c_int = (\d+);", files[rel]):
                values.setdefault(name, set()).add(int(value))
        result[platform] = values
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", default=str(ARCH.parent / "opensip"))
    parser.add_argument("--product-commit", default=PRODUCT_COMMIT)
    parser.add_argument("--libc-crate", default=None)
    args = parser.parse_args()
    product = Product(Path(args.product), args.product_commit)

    record = json.loads(arch(RECORD))
    subject = json.loads(arch(SUBJECT))
    parent = arch(PARENT)
    parents = record["parents"]
    need(len(parents) == 1 and parents[0]["path"] == PARENT, "parent set")
    need(parents[0]["bytes"] == len(parent) and parents[0]["sha256"] == sha256(parent), "parent pin")
    lines = parent.decode("utf-8").splitlines()
    overrides = record["passageOverrides"]
    need(len(overrides) == 2, "override count")
    for override in overrides:
        need(override["parent"] == parents[0], "override parent pin")
    reaped, insert = overrides
    need(reaped["selector"] == {"line": 881} and insert["selector"] == {"line": 894}, "selectors")
    need(reaped["before"] == lines[880] and lines[880].startswith("| `provider.process.reaped` |"), "reaped before")
    need(lines[880].count(REAPED_BEFORE) == 1, "reaped field text")
    need(reaped["after"] == lines[880].replace(REAPED_BEFORE, REAPED_AFTER), "reaped after")
    need(insert["before"] == lines[893] and lines[893].startswith('"P, P, E" is Project'), "insert before")
    text = passage()
    need(insert["after"] == lines[893] + "\n\n" + text, "insert after is not the PROPOSAL passage")
    need(record.get("passageSupersessions") == [], "supersessions")

    tables = {name: table_members(text, name) for name in
              ("StageKind", "ProviderState", "Signal", "ChildSignal", "ProviderReason")}
    expected_class = {"StageKind": "protocol-enum", "ProviderState": "protocol-enum", "Signal": "generated-contract",
                      "ChildSignal": "registry-literal", "ProviderReason": "protocol-enum"}
    for name, members in tables.items():
        need(provenance(text, name) == expected_class[name], f"provenance {name}")
        need(members and len(members) == len(set(members)), f"members unique {name}")
        for member in members:
            need(K1.match(member) is not None, f"K1 member {name} {member}")

    # StageKind: the two protocols' stage operator.
    carriers = json.loads(product.show("schemas/wire/native-carriers-v1.json"))
    operators = set()
    for record_name in ("Ts2StageRequestV1", "Rust3C2PlanStageV3"):
        rows = [m for m in carriers["records"][record_name]["members"] if m["name"] == "operator"]
        need(len(rows) == 1 and set(rows[0]["type"]) == {"t", "nfc", "const"}, f"operator shape {record_name}")
        operators.add(rows[0]["type"]["const"])
    protocol = product.show("crates/contracts/src/generated/protocol.rs").decode("utf-8")
    for enum in ("Ts2StageRequestV1Field2Value", "Rust3C2PlanStageV3Field5Value"):
        need(set(enum_members(protocol, enum)) == operators, f"generated {enum}")
    need(tables["StageKind"] == sorted(operators), "StageKind members")
    identity = json.loads(product.show("schemas/sources/identity-v3.schema.json"))
    operation = identity["$defs"]["stage-spec"]["properties"]["operation"]
    need("enum" not in operation and "const" not in operation, "stage-spec operation is open")

    # ProviderState: P3T's phases; T2O's are a subset.
    p3t, t2o = json.loads(arch_pinned(P3T))["phases"], json.loads(arch_pinned(T2O))["phases"]
    need(set(t2o) <= set(p3t), "T2O phases are not a subset of P3T's")
    need(tables["ProviderState"] == p3t, "ProviderState members")
    for pin in (P3T, T2O):
        copy = product.show("crates/components/data/" + pin[0].rsplit("/", 1)[1])
        need(sha256(copy) == pin[1], f"product vendored copy {pin[0]}")

    # Signal: COMMON4 D9Signal.
    common = json.loads(product.show("schemas/sources/common-v4.schema.json"))
    d9 = common["$defs"]["D9Signal"]["enum"]
    evidence = product.show("crates/contracts/src/generated/evidence.rs").decode("utf-8")
    need(enum_members(evidence, "Common4D9Signal") == d9, "generated Common4D9Signal")
    need(tables["Signal"] == d9, "Signal members")

    # ChildSignal: POSIX terminating signals defined on every platform.
    lock = product.show("Cargo.lock").decode("utf-8")
    need('libc = { version = "=0.2.189"' in product.show("crates/platform/Cargo.toml").decode("utf-8"), "platform libc pin")
    crate = Path(args.libc_crate) if args.libc_crate else next(
        iter(sorted(Path.home().glob(".cargo/registry/cache/*/libc-0.2.189.crate"))), None)
    need(crate is not None and crate.is_file(), "libc-0.2.189.crate not found; pass --libc-crate")
    constants = libc_constants(crate, lock)
    everywhere = {name for name in POSIX_TERMINATING
                  if all(len(constants[p].get(name, ())) == 1 for p in LIBC_SETS)}
    need(tables["ChildSignal"] == sorted(everywhere), "ChildSignal members")
    need(POSIX_TERMINATING - everywhere == {"SIGPOLL"}, "only SIGPOLL is dropped")
    need("SIGPOLL" not in constants["macos"], "SIGPOLL on macOS")
    numbers = {name: {p: next(iter(constants[p][name])) for p in LIBC_SETS} for name in tables["ChildSignal"]}

    # ProviderReason: the admitted Unavailable reasons.
    startup_arch = json.loads(arch_pinned(STARTUP))["$defs"]
    startup_product = json.loads(product.show("schemas/sources/startup-v1.schema.json"))["$defs"]
    reasons = set()
    for name in ("PreAnalyzeUnavailableV1", "TypeScriptUnavailableV2", "UnavailableV3"):
        schema = startup_arch[name]["properties"]["reason"]
        need(schema == startup_product[name]["properties"]["reason"], f"startup copies differ {name}")
        reasons.update(schema["enum"] if "enum" in schema else [schema["const"]])
    need(set(enum_members(protocol, "Startup1TypeScriptUnavailableV2Reason"))
         == set(startup_arch["TypeScriptUnavailableV2"]["properties"]["reason"]["enum"]), "generated TS2 reason")
    need(set(enum_members(protocol, "Startup1UnavailableV3Reason"))
         == set(startup_arch["UnavailableV3"]["properties"]["reason"]["enum"]), "generated Rust3 reason")
    need(tables["ProviderReason"] == sorted(reasons), "ProviderReason members")

    # Subject and candidates.
    files = subject["files"]
    paths = [row["path"] for row in files]
    need(paths == sorted(set(paths)) and RECORD in paths, "subject paths")
    candidates = record["candidates"]
    cand_paths = [row["path"] for row in candidates]
    need(cand_paths == sorted(set(cand_paths)) and set(cand_paths) == set(paths) - {RECORD}, "candidates")
    by_path = {row["path"]: row for row in files}
    data = arch(RECORD)
    need(by_path[RECORD]["bytes"] == len(data) and by_path[RECORD]["sha256"] == sha256(data), "record pin")
    for row in candidates:
        need(by_path[row["path"]] == row, f"candidate differs from subject {row['path']}")
        data = arch(row["path"])
        need(row["bytes"] == len(data) and row["sha256"] == sha256(data), f"candidate pin {row['path']}")

    print(json.dumps({
        "tables": tables,
        "t2oPhasesSubsetOfP3T": True,
        "childSignalNumbers": numbers,
        "libcCrate": {"path": str(crate), "sha256": sha256(crate.read_bytes())},
        "productCommit": args.product_commit,
    }, indent=1))
    print("CHECKS-OK")


if __name__ == "__main__":
    try:
        main()
    except CheckError as error:
        print(f"CHECK-FAILED: {error}")
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(0)
