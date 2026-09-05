#!/usr/bin/env python3
"""Successor retained checker for the Rust semantic-provider protocol v4 candidate.

Supported invocations:
  python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v5.py
  python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v5.py --selftest

WHY THIS FILE EXISTS (freeze S7.2 / S7.6 / S7.8).

  check-rust-provider-protocol-v2.py:1377 enumerates files by shelling out:

      subprocess.run(["rg", "--files", "docs/coop/artifacts"],
                     cwd=REPO_ROOT, check=True, capture_output=True, text=True)

  check-rust-provider-protocol-v4.py loads v2 (and v3, which loads v2 again) via
  importlib and inherits that call.  Where `rg` is not a binary on PATH -- for
  example where it is a shell function, which satisfies `command -v rg` but not
  `shutil.which` and not `subprocess` -- every one of v2, v3 and v4 dies with an
  unhandled FileNotFoundError before checking anything.

  claim-register.v1.json names check-rust-provider-protocol-v4.py as the
  validator for the RUST-PROVIDER-PROTOCOL binding: the protocol overlay, the
  DELIVERY join and the RESOLVED-INPUTS join.  In an environment without a real
  ripgrep binary that validator has never validated any of them -- it aborts
  first.  The recorded PASSED verdict for the five-file v4 set was produced in an
  environment that cannot be reproduced here.  That is freeze S7.2 exactly: a
  verdict binds bytes AND an environment, and this is the sharpest live instance
  of it in the corpus.

  S7.2 forbids repairing v2/v3/v4 in place; S7.6 records that immutability
  therefore prevents a proven fix from propagating; S7.8 records the answer --
  a new checker is a new file and edits nothing.  This file is the propagation
  mechanism.  v2, v3 and v4 stay broken, which is correct.

WHAT CHANGED, STATED NARROWLY.

  `rg --files` is used for ONE purpose: enumerating the regular files under
  docs/coop/artifacts.  This checker replaces that single external process with
  a standard-library enumeration and changes nothing else.  Every check v4
  performs is performed here, by executing v4's own pinned bytes in-process --
  not by reimplementing them, because a reimplementation would be testing this
  author's transcription of v4 rather than v4 (S7.8).

  `rg --files` applies ignore rules (.gitignore, .ignore, .rgignore,
  .git/info/exclude, a global excludes file); a standard-library walk does not.
  Today nothing under docs/coop/artifacts is ignored, so the two sets coincide.
  The divergence hazard is therefore LATENT, NOT ACTIVE.  This checker's
  enumeration is ignore-independent BY CONSTRUCTION -- it consults no ignore
  file at all -- so what this repair removes is a latent environment dependency.
  It does not fix an active bug, and this file does not claim to.  The in-repo
  ignore surface is measured every run and an ACTIVE ignore rule over the
  subtree is a finding, so the disclosure cannot go stale (S7.8 move 6).

WHAT A GREEN RUN IS EVIDENCE OF (freeze S7.8, answered in the banner).

  That the reviewed bytes are the bytes on disk and drift stops the run; that
  everything recomputable was recomputed and agrees; that the artifacts' own
  recorded execution measurements match a run that actually happened here.  NOT
  that the artifacts' prose is true.  This file publishes the measured count of
  narrative leaves that can be falsified without any check firing.

EXIT CODES
  0  clean
  1  findings
  2  unsupported invocation
  3  declared environment precondition unmet, or this instrument failed to
     complete (RPPV5-INTERNAL) -- the run could not happen.  Distinct from 1 so
     that "the instrument could not run" is never read as "the artifact is
     wrong".  A crash looks like a failure looks like a finding; that
     resemblance is why the defect above went unnoticed for three versions, and
     it is why no code path here may surface as a bare traceback.
"""
from __future__ import annotations

import sys

if sys.flags.isolated != 1 or not sys.dont_write_bytecode:
    print("RPPV5-UNSUPPORTED-INVOCATION: require python3 -I -B", file=sys.stderr)
    raise SystemExit(2)
if sys.argv[1:] not in ([], ["--selftest"]):
    print("RPPV5-UNSUPPORTED-INVOCATION: require no arguments or --selftest", file=sys.stderr)
    raise SystemExit(2)

import ast
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import sysconfig
import traceback
import types
from typing import Any, Callable, Iterable

# ---------------------------------------------------------------------------
# Identity and the one recorded anchor.
# ---------------------------------------------------------------------------

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
CHECKER = "check-rust-provider-protocol-v5.py"
V4_CHECKER = "check-rust-provider-protocol-v4.py"
V3_CHECKER = "check-rust-provider-protocol-v3.py"
V2_CHECKER = "check-rust-provider-protocol-v2.py"
D9_CHECKER = "check-d9-v1.13.py"
REGISTER = "claim-register.v1.json"
CLAIM_ID = "RUST-PROVIDER-PROTOCOL"

# The single transcribed constant in this file.  Everything else about the v4
# closure -- which files it hash-pins, at which digests, which counts it expects
# -- is read out of v4's own executed bytes or out of the artifacts themselves.
V4_SHA256 = "85e022c8e2470dab7c1fc42e45b9a36b10ee436f5d5198ed7750a30cb3ae642f"

# Recorded measurements.  Freeze S7.2.2: a recorded measurement gets a hard
# comparison, because an uncompared measurement is prose that looks like
# evidence.  Every one of these fails the build when it goes stale.
RECORDED = {
    # External-process touch points in the four executed files, by AST.
    "closureInventoryCounts": {
        V4_CHECKER: 0,
        V3_CHECKER: 0,
        V2_CHECKER: 3,
        D9_CHECKER: 17,
    },
    "closureInventorySha256": "62591e54828bf87955b0962c2669ac27a234ab4265c51459717f40198295bbe9",
    # Times the replaced enumeration is reached during one v4 run (v4's own v2
    # replay is 2, and v4's replay of v3 -- which loads its own v2 -- is 2 more).
    "enumerationCallsPerV4Run": 4,
    # Active ignore patterns in the repository that could make a standard-library
    # walk disagree with `rg --files` over the subtree.
    "activeInRepoIgnorePatterns": 0,
    # S7.8 residual, with its definition attached, measured by --selftest.
    # A "narrative leaf" is a string leaf of one of the four v4 documents that
    # contains a space and is longer than 25 characters.  The probe appends one
    # false sentence, leaving path and type unchanged.
    "narrativeLeafDefinition": "string leaf containing a space and longer than 25 characters",
    "narrativeLeavesProbed": 252,
    "narrativeLeavesFalsifiableWithoutDetection": 108,
    # This file's own mutation suite.
    "ownMutations": 26,
}

FORBIDDEN_MODULES = frozenset({"subprocess", "multiprocessing", "pty", "popen2", "commands"})
FORBIDDEN_ATTRS = frozenset({
    ("os", "system"), ("os", "popen"), ("os", "fork"), ("os", "forkpty"),
    ("os", "posix_spawn"), ("os", "posix_spawnp"), ("os", "execv"), ("os", "execve"),
    ("os", "execvp"), ("os", "execvpe"), ("os", "execl"), ("os", "execle"),
    ("os", "execlp"), ("os", "execlpe"), ("os", "spawnv"), ("os", "spawnve"),
    ("os", "spawnl"), ("os", "spawnle"), ("os", "spawnlp"), ("os", "spawnlpe"),
    ("platform", "popen"),
})
IGNORE_FILE_NAMES = (".gitignore", ".ignore", ".rgignore")


class EnvironmentUnmet(RuntimeError):
    """A declared environment precondition does not hold.  Exit 3, never 1."""


class PinDrift(RuntimeError):
    """A pinned input's live bytes are not the bytes this file was written
    against.  That is a statement about bytes, so it is a finding (exit 1) and
    not an environment problem -- freeze S7.2: a verdict binds bytes."""


class ExternalProcessRefused(RuntimeError):
    """The closure attempted an external-process operation this file will not do."""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


class Findings:
    def __init__(self) -> None:
        self.rows: list[str] = []
        self.checks = 0

    def require(self, condition: bool, code: str, detail: str = "") -> bool:
        self.checks += 1
        if not condition:
            self.rows.append(code + (": " + detail if detail else ""))
        return bool(condition)

    def add(self, code: str, detail: str = "") -> None:
        self.rows.append(code + (": " + detail if detail else ""))


# ---------------------------------------------------------------------------
# Static scan: where does external-process capability live?
#
# This is disclosure, hard-compared so that a broken scanner is a finding.  It
# is NOT the safety mechanism -- freeze S7.6 records that "which files record
# this digest" is a text question while "which checkers compare it at runtime"
# is a code question, and that a static scan cannot tell them apart.  The safety
# mechanism is the runtime guard below, which refuses rather than reports.
# ---------------------------------------------------------------------------

def _attr_chain(node: ast.AST) -> str:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return ""


def _attr_base(node: ast.AST) -> str:
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else ""


def scan_external_process(source: bytes, label: str) -> list[tuple[int, str, str]]:
    """Every syntactic touch point of an external-process API in `source`."""
    rows: set[tuple[int, str, str]] = set()
    for node in ast.walk(ast.parse(source, label)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_MODULES:
                    rows.add((node.lineno, "IMPORT", alias.name))
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in FORBIDDEN_MODULES:
                rows.add((node.lineno, "IMPORT-FROM", node.module or ""))
        elif isinstance(node, ast.Attribute):
            chain = _attr_chain(node)
            parts = chain.split(".")
            if _attr_base(node) in FORBIDDEN_MODULES:
                rows.add((node.lineno, "ATTR", chain))
            elif len(parts) >= 2 and (parts[-2], parts[-1]) in FORBIDDEN_ATTRS:
                rows.add((node.lineno, "ATTR", chain))
        elif isinstance(node, ast.Name):
            if node.id in FORBIDDEN_MODULES and not isinstance(node.ctx, ast.Store):
                rows.add((node.lineno, "NAME", node.id))
    return sorted(rows)


def derive_enumeration_invocation(source: bytes, label: str) -> tuple[tuple[str, ...], frozenset[str]]:
    """Read the replaced invocation out of the predecessor's own bytes.

    Freeze S7.8 move 2: re-derive constants from the artifact rather than
    transcribing them, or the instrument tests its own transcription.  The argv
    and keyword set this file emulates are extracted from v2's AST, not typed in.
    """
    found: list[tuple[tuple[str, ...], frozenset[str]]] = []
    for node in ast.walk(ast.parse(source, label)):
        if not isinstance(node, ast.Call):
            continue
        if _attr_chain(node.func) not in ("subprocess.run", "subprocess.check_output", "subprocess.Popen"):
            continue
        if not node.args or not isinstance(node.args[0], (ast.List, ast.Tuple)):
            raise ExternalProcessRefused(label + ": non-literal argv at line " + str(node.lineno))
        try:
            argv = tuple(ast.literal_eval(element) for element in node.args[0].elts)
        except ValueError as exc:
            raise ExternalProcessRefused(label + ": unreadable argv at line " + str(node.lineno)) from exc
        found.append((argv, frozenset(kw.arg or "" for kw in node.keywords)))
    if len(found) != 1:
        raise ExternalProcessRefused(label + ": expected exactly one external invocation, found " + str(len(found)))
    argv, kwargs = found[0]
    if len(argv) != 3 or argv[1] != "--files" or not all(type(x) is str for x in argv):
        raise ExternalProcessRefused(label + ": unexpected invocation shape " + repr(argv))
    return argv, kwargs


# ---------------------------------------------------------------------------
# The replacement: two independently written standard-library enumerations.
#
# Neither reads an ignore file, so ignore-independence is a property of the
# construction rather than of today's tree.  They are cross-checked against each
# other so that the result is not an artefact of one API's own filtering.
# ---------------------------------------------------------------------------

def walk_pathlib(root: pathlib.Path, base: pathlib.Path) -> list[str]:
    out: list[str] = []
    for path in root.rglob("*"):
        if path.is_symlink():
            continue
        if path.is_file():
            out.append(path.relative_to(base).as_posix())
    return sorted(out)


def walk_scandir(root: pathlib.Path, base: pathlib.Path) -> tuple[list[str], list[str]]:
    out: list[str] = []
    irregular: list[str] = []
    stack = [root]
    while stack:
        current = stack.pop()
        with os.scandir(current) as entries:
            for entry in entries:
                path = pathlib.Path(entry.path)
                if entry.is_symlink():
                    irregular.append(path.relative_to(base).as_posix() + " (symlink)")
                    continue
                if entry.is_dir(follow_symlinks=False):
                    stack.append(path)
                elif entry.is_file(follow_symlinks=False):
                    out.append(path.relative_to(base).as_posix())
                else:
                    irregular.append(path.relative_to(base).as_posix() + " (not a regular file)")
    return sorted(out), sorted(irregular)


class Completed:
    """The three attributes v2 reads off subprocess.run's result, and no more."""

    def __init__(self, argv: tuple[str, ...], stdout: str) -> None:
        self.args = list(argv)
        self.returncode = 0
        self.stdout = stdout
        self.stderr = ""


class ProcessGuard:
    """Stands in for `subprocess` inside the executed closure.

    It answers exactly one invocation -- the file enumeration measured out of
    v2's own bytes -- and refuses everything else by name.  It never starts a
    process.  Anything the closure asks for that is not the enumeration produces
    `RPPV5-GUARD-REFUSED` naming the operation, not an opaque traceback.
    """

    def __init__(self, argv: tuple[str, ...], kwargs: frozenset[str]) -> None:
        object.__setattr__(self, "_argv", argv)
        object.__setattr__(self, "_kwargs", kwargs)
        object.__setattr__(self, "calls", 0)
        object.__setattr__(self, "refusals", [])
        object.__setattr__(self, "observations", [])
        object.__setattr__(self, "__name__", "subprocess")
        object.__setattr__(self, "__spec__", None)

    # `run` is the only capability offered.  check-d9-v1.13.py reads
    # `subprocess.run` at module scope, so the attribute must exist.
    def run(self, args: Iterable[str], **kwargs: Any) -> Completed:
        argv = tuple(args)
        if argv != self._argv:
            return self._refuse("run argv=" + repr(argv))
        if frozenset(kwargs) != self._kwargs:
            return self._refuse("run kwargs=" + repr(sorted(kwargs)))
        if kwargs.get("check") is not True or kwargs.get("capture_output") is not True or kwargs.get("text") is not True:
            return self._refuse("run flags=" + repr(sorted((k, v) for k, v in kwargs.items() if k != "cwd")))
        base = pathlib.Path(kwargs["cwd"]).resolve()
        root = (base / argv[2]).resolve()
        if not root.is_dir():
            raise EnvironmentUnmet("enumeration root is not a directory: " + str(root))
        # Two independently written walks plus a repeat of the first.  A single
        # disagreement can be a file arriving mid-walk in a live tree, so the
        # triple is retried; only a disagreement that SURVIVES retries is a
        # statement about the enumerator rather than about concurrency.
        settled = False
        attempts = 0
        first: list[str] = []
        irregular: list[str] = []
        while attempts < 3 and not settled:
            attempts += 1
            first = walk_pathlib(root, base)
            second, irregular = walk_scandir(root, base)
            third = walk_pathlib(root, base)
            settled = first == second == third
        object.__setattr__(self, "calls", self.calls + 1)
        self.observations.append({
            "root": root.relative_to(base).as_posix(),
            "count": len(first),
            "settled": settled,
            "attempts": attempts,
            "irregular": irregular,
            "sha256": sha(("\n".join(first)).encode("utf-8")),
        })
        return Completed(argv, "\n".join(first) + ("\n" if first else ""))

    def _refuse(self, what: str) -> Completed:
        self.refusals.append(what)
        raise ExternalProcessRefused(
            "this checker starts no external process; refused: " + what)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        self.refusals.append("attribute " + name)
        raise ExternalProcessRefused(
            "this checker starts no external process; refused attribute: subprocess." + name)


# ---------------------------------------------------------------------------
# Ignore surface: is the latent divergence still latent?
# ---------------------------------------------------------------------------

def active_ignore_patterns(root: pathlib.Path, subtree: pathlib.Path) -> tuple[int, list[str]]:
    """Count ignore patterns in the repository that bear on the subtree.

    In-repo sources only: every ancestor from the repository root down to the
    subtree, every directory inside it, and .git/info/exclude.  Blank lines and
    comments are not patterns.
    """
    sources: list[pathlib.Path] = []
    node = subtree
    chain = [node]
    while node != root and node.parent != node:
        node = node.parent
        chain.append(node)
    for directory in chain:
        for name in IGNORE_FILE_NAMES:
            candidate = directory / name
            if candidate.is_file():
                sources.append(candidate)
    for dirpath, _dirnames, filenames in os.walk(subtree):
        for name in filenames:
            if name in IGNORE_FILE_NAMES:
                sources.append(pathlib.Path(dirpath) / name)
    exclude = root / ".git" / "info" / "exclude"
    if exclude.is_file():
        sources.append(exclude)
    total = 0
    described: list[str] = []
    for source in sorted(set(sources)):
        lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
        patterns = [x for x in (line.strip() for line in lines) if x and not x.startswith("#")]
        total += len(patterns)
        described.append(source.relative_to(root).as_posix() + "=" + str(len(patterns)))
    return total, described


def global_ignore_disclosure() -> str:
    """A git excludes file outside the repository cannot change this file's
    enumeration -- it is complete by construction -- but it WOULD change what
    `rg --files` returns, so it is reported rather than gated."""
    found: list[str] = []
    home = pathlib.Path(os.path.expanduser("~"))
    for candidate in (home / ".config" / "git" / "ignore",):
        if candidate.is_file():
            found.append(candidate.name)
    for config in (home / ".gitconfig", home / ".config" / "git" / "config"):
        if config.is_file():
            text = config.read_text(encoding="utf-8", errors="replace").lower()
            if "excludesfile" in text:
                found.append(config.name + ":excludesfile")
    return ",".join(found) if found else "none"


# ---------------------------------------------------------------------------
# Environment declaration.  Failing here is exit 3, never exit 1.
# ---------------------------------------------------------------------------

def declared_environment(argv_needed: tuple[str, ...]) -> dict[str, Any]:
    """Everything this file assumes about where it runs, checked before use."""
    facts: dict[str, Any] = {}
    if sys.implementation.name != "cpython":
        raise EnvironmentUnmet("requires CPython, found " + sys.implementation.name)
    if sys.version_info < (3, 10):
        raise EnvironmentUnmet("requires Python >= 3.10, found " + sys.version.split()[0])
    facts["python"] = sys.version.split()[0]

    stdlib = pathlib.Path(sysconfig.get_paths()["stdlib"]).resolve()
    builtin = set(sys.builtin_module_names)
    for name in ("ast", "contextlib", "copy", "hashlib", "importlib.util", "io",
                 "json", "os", "pathlib", "sysconfig", "traceback", "types"):
        module = sys.modules.get(name)
        if module is None:
            raise EnvironmentUnmet("standard-library module not loaded: " + name)
        origin = getattr(module, "__file__", None)
        if origin is None:
            if name.split(".")[0] not in builtin:
                raise EnvironmentUnmet("standard-library module has no origin: " + name)
            continue
        resolved = pathlib.Path(origin).resolve()
        if stdlib not in resolved.parents:
            raise EnvironmentUnmet(
                "standard-library module " + name + " resolves outside the standard library: " + str(resolved))
    facts["stdlib"] = str(stdlib)

    for name in (CHECKER, V4_CHECKER, V3_CHECKER, V2_CHECKER, D9_CHECKER, REGISTER):
        if not (HERE / name).is_file():
            raise EnvironmentUnmet("required input missing: " + name)
    if not (REPO_ROOT / "docs" / "coop" / "artifacts").is_dir():
        raise EnvironmentUnmet("repository layout: docs/coop/artifacts not found under " + str(REPO_ROOT))

    # The declared external tool of the PREDECESSOR, reported and not required.
    tool = argv_needed[0]
    facts["predecessorExternalTool"] = tool
    facts["predecessorToolOnPath"] = _tool_on_path(tool)
    facts["externalProcessesStartedByThisChecker"] = 0
    facts["globalGitExcludes"] = global_ignore_disclosure()
    return facts


def _tool_on_path(tool: str) -> bool:
    """Disclosure only.  A shell function named `rg` satisfies `command -v rg`
    and does NOT satisfy this, which is the whole defect."""
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry:
            continue
        candidate = pathlib.Path(entry) / tool
        try:
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return True
        except OSError:
            continue
    return False


# ---------------------------------------------------------------------------
# Loading v4's pinned bytes.
# ---------------------------------------------------------------------------

class SnapshotLoader:
    def __init__(self, path: pathlib.Path, source: bytes) -> None:
        self.path = path
        self.source = source

    def create_module(self, spec: Any) -> None:
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.path), "exec", dont_inherit=True), module.__dict__)


def execute_verified(name: str, expected: str, module_name: str) -> types.ModuleType:
    path = (HERE / name).resolve()
    source = path.read_bytes()
    actual = sha(source)
    if actual != expected:
        raise PinDrift(name + " digest drift: expected " + expected + " found " + actual)
    spec = importlib.util.spec_from_file_location(module_name, path, loader=SnapshotLoader(path, source))
    if spec is None or spec.loader is None:
        raise EnvironmentUnmet(name + " could not be prepared for execution")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pyc_snapshot() -> dict[str, str]:
    return {
        str(path.relative_to(HERE)): sha(path.read_bytes())
        for path in sorted(HERE.rglob("*.pyc"))
    }


def parse_banner(text: str, prefix: str) -> dict[str, str] | None:
    for line in text.splitlines():
        if line.startswith(prefix):
            out: dict[str, str] = {}
            for token in line.split()[1:]:
                if "=" in token:
                    key, _, value = token.partition("=")
                    out[key] = value
            return out
    return None


def run_v4(v4mod: types.ModuleType, selftest: bool) -> tuple[int, str, str]:
    stdout, stderr = io.StringIO(), io.StringIO()
    saved = sys.argv
    sys.argv = [str(HERE / V4_CHECKER)] + (["--selftest"] if selftest else [])
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = v4mod.main()
    finally:
        sys.argv = saved
    return int(code), stdout.getvalue(), stderr.getvalue()


# ---------------------------------------------------------------------------
# Re-derivation.  Freeze S7.2.2: a recorded measurement gets a hard comparison.
#
# v4 compares the response artifact's checkerExecutionRecord against hand-typed
# Python literals inside v4.  It never compares that record to what it actually
# measured on the run in progress.  This file does, which is the check the
# corpus has never been able to perform in this environment because v4 aborted.
# ---------------------------------------------------------------------------

def load_v4_documents(v4mod: types.ModuleType) -> dict[str, Any]:
    docs: dict[str, Any] = {}
    for name, expected in v4mod.LOCAL_JSON_HASHES.items():
        docs[name], _ = v4mod.read_hashed(name, expected)
    docs[v4mod.RESPONSE] = v4mod.strict_loads((HERE / v4mod.RESPONSE).read_text(encoding="utf-8"))
    return docs


def derived_from_artifacts(v4mod: types.ModuleType, docs: dict[str, Any]) -> dict[str, int]:
    protocol = docs[v4mod.PROTOCOL]["orderingAndStateMachineV4"]
    boundary = docs[v4mod.DELIVERY]["hostFinalizerBoundaryV4"]
    domain = boundary["finiteContextDomain"]
    return {
        "v4TransitionRules": len(protocol["transitionRulesV4"]),
        "v4RepairWitnesses": len(protocol["modelCheckDomain"]["requiredRepairWitnesses"]),
        "v4FsmTraces": protocol["modelCheckDomain"]["retainedV3TraceCount"],
        "v4FsmTotalityComparisons": protocol["modelCheckDomain"]["retainedV3TotalityComparisonCount"],
        "v4FinalizerFullDomain": domain["fullCartesianSize"],
        "v4FinalizerAdmitted": domain["admittedCount"],
        "v4FinalizerInvalid": domain["invalidCombinations"]["count"],
        "v4FinalizerGoldens": len(boundary["narrowGoldens"]),
        "v4Mutations": len(v4mod.mutation_specs(docs)),
    }


BANNER_JOIN_ALWAYS = {
    "v2SemanticPositive": "v2_positive",
    "v2SemanticAdversarial": "v2_adversarial",
    "v4ReducerTuples": "reducer",
    "v2ReducerTuples": "reducer",
    "v4FsmTraces": "fsm_traces",
    "v4FsmTotalityComparisons": "fsm_totality",
    "v4TransitionRules": "rules",
    "v4NominalTypeProbes": "nominal_probes",
    "v4RepairWitnesses": "repair_witnesses",
    "v4FinalizerFullDomain": "finalizer_full",
    "v4FinalizerAdmitted": "finalizer_admitted",
    "v4FinalizerInvalid": "finalizer_invalid",
    "v4FinalizerGoldens": "finalizer_goldens",
}
BANNER_JOIN_NORMAL = {
    "normalPositiveCount": "positive",
    "normalAdversarialCount": "adversarial",
}
BANNER_JOIN_SELFTEST = {
    "selftestPositiveCount": "positive",
    "selftestAdversarialCount": "adversarial",
    "v2Mutations": "v2_mutations",
    "v4Mutations": "mutations",
    "harnessEscapes": "harness_escapes",
}


def record_agreement_errors(record: dict[str, Any], banner: dict[str, str], selftest: bool) -> list[str]:
    """Every recorded execution figure joined to the run that just happened."""
    errors: list[str] = []
    join = dict(BANNER_JOIN_ALWAYS)
    join.update(BANNER_JOIN_SELFTEST if selftest else BANNER_JOIN_NORMAL)
    for recorded_key, banner_key in sorted(join.items()):
        if recorded_key not in record:
            errors.append("record has no " + recorded_key)
            continue
        if banner_key not in banner:
            errors.append("banner has no " + banner_key)
            continue
        try:
            observed = int(banner[banner_key])
        except ValueError:
            errors.append(banner_key + " is not an integer: " + banner[banner_key])
            continue
        if record[recorded_key] != observed:
            errors.append(recorded_key + " recorded " + repr(record[recorded_key]) + " but this run measured " + str(observed))
    return errors


def derived_agreement_errors(derived: dict[str, int], record: dict[str, Any], banner: dict[str, str], selftest: bool) -> list[str]:
    """Artifact-derived count == recorded count == count this run printed."""
    errors: list[str] = []
    join = dict(BANNER_JOIN_ALWAYS)
    join.update(BANNER_JOIN_SELFTEST if selftest else BANNER_JOIN_NORMAL)
    for key, value in sorted(derived.items()):
        if key in record and record[key] != value:
            errors.append(key + " derived " + str(value) + " but recorded " + repr(record[key]))
        banner_key = join.get(key)
        if banner_key is not None and banner_key in banner:
            if str(value) != banner[banner_key]:
                errors.append(key + " derived " + str(value) + " but run printed " + banner[banner_key])
    full = derived["v4FinalizerFullDomain"]
    if derived["v4FinalizerAdmitted"] + derived["v4FinalizerInvalid"] != full:
        errors.append("admitted + invalid != full cartesian domain")
    return errors


def declared_command_errors(record: dict[str, Any]) -> list[str]:
    """The artifact records the command under which its verdict was produced.
    Bind it to the flags this process is actually running under (freeze S7.2:
    a verdict binds bytes AND an environment)."""
    errors: list[str] = []
    for key, expect_selftest in (("requiredNormalCommand", False), ("requiredSelftestCommand", True)):
        command = record.get(key)
        if not isinstance(command, str):
            errors.append(key + " is not a string")
            continue
        tokens = command.split()
        if "-I" not in tokens or "-B" not in tokens:
            errors.append(key + " does not declare -I -B: " + command)
        if not any(token.endswith(V4_CHECKER) for token in tokens):
            errors.append(key + " does not name " + V4_CHECKER)
        if expect_selftest != ("--selftest" in tokens):
            errors.append(key + " selftest flag mismatch")
    return errors


# ---------------------------------------------------------------------------
# Claim register: the recorded binding this file is a validator for.
# ---------------------------------------------------------------------------

def register_errors(findings: Findings) -> dict[str, Any]:
    register = json.loads((HERE / REGISTER).read_text(encoding="utf-8"))
    claims = [c for c in register.get("claims", []) if c.get("id") == CLAIM_ID]
    if len(claims) != 1:
        findings.add("RPPV5-REGISTER-CLAIM", "expected exactly one " + CLAIM_ID + " claim, found " + str(len(claims)))
        return {}
    claim = claims[0]
    members = claim.get("bindingArtifactSet", {}).get("members", [])
    findings.require(bool(members), "RPPV5-REGISTER-CLAIM", "binding artifact set is empty")
    drift: list[str] = []
    for member in members:
        path = REPO_ROOT / "docs" / "coop" / str(member.get("path", ""))
        recorded = member.get("sha256")
        if not path.is_file():
            drift.append(str(member.get("path")) + " missing")
            continue
        live = sha(path.read_bytes())
        if live != recorded:
            drift.append(str(member.get("path")) + " recorded " + str(recorded)[:12] + " live " + live[:12])
    findings.require(not drift, "RPPV5-REGISTER-DIGEST", "; ".join(drift))
    binding = claim.get("bindingArtifact", "")
    binding_path = REPO_ROOT / "docs" / "coop" / str(binding)
    findings.require(
        binding_path.is_file() and sha(binding_path.read_bytes()) == claim.get("bindingArtifactSha256"),
        "RPPV5-REGISTER-DIGEST", "bindingArtifactSha256 does not match " + str(binding))
    validator = str(claim.get("validator", ""))
    findings.require(
        (REPO_ROOT / "docs" / "coop" / validator).is_file(),
        "RPPV5-REGISTER-VALIDATOR", "named validator does not exist: " + validator)
    return {"validator": validator, "members": len(members)}


# ---------------------------------------------------------------------------
# Self-scan.  Freeze S7.2.2 rider: a measurement that cannot fail the build is
# prose.  This file asserts its own zero-external-process property mechanically.
# ---------------------------------------------------------------------------

DIRTY_PROBES = (
    ("import-subprocess", b"import subprocess\nx = 1\n"),
    ("from-subprocess", b"from subprocess import run\n"),
    ("subprocess-run", b"import json\nimport subprocess as sp\nsubprocess.run(['rg'])\n"),
    ("os-system", b"import os\nos.system('rg --files')\n"),
    ("os-popen", b"import os\nh = os.popen('rg --files')\n"),
    ("os-execvp", b"import os\nos.execvp('rg', ['rg'])\n"),
    ("multiprocessing", b"import multiprocessing\n"),
    ("os-posix-spawn", b"import os\nos.posix_spawn('/bin/sh', ['sh'], {})\n"),
)
CLEAN_PROBES = (
    ("string-only", b"NAMES = ['subprocess', 'os.system', 'os.popen']\n"),
    ("pathlib-walk", b"import pathlib\nlist(pathlib.Path('.').rglob('*'))\n"),
    ("os-scandir", b"import os\nlist(os.scandir('.'))\n"),
)


def self_scan_errors(findings: Findings) -> int:
    own = (HERE / CHECKER).read_bytes()
    rows = scan_external_process(own, CHECKER)
    findings.require(
        not rows, "RPPV5-SELF-EXTERNAL-PROCESS",
        "; ".join(str(r) for r in rows[:6]))
    # Non-vacuity: the scanner must fire on wrong input, not merely pass on empty.
    caught = 0
    for label, source in DIRTY_PROBES:
        if scan_external_process(source, label):
            caught += 1
        else:
            findings.add("RPPV5-SELF-SCANNER-BLIND", label)
    for label, source in CLEAN_PROBES:
        if scan_external_process(source, label):
            findings.add("RPPV5-SELF-SCANNER-FALSE-POSITIVE", label)
    findings.require(caught == len(DIRTY_PROBES), "RPPV5-SELF-SCANNER-BLIND",
                     str(caught) + " of " + str(len(DIRTY_PROBES)) + " probes caught")
    return caught


# ---------------------------------------------------------------------------
# Mutation suite for this file's own additions.
# ---------------------------------------------------------------------------

def own_mutations(v4mod: types.ModuleType, docs: dict[str, Any], banner: dict[str, str],
                  derived: dict[str, int], guard: ProcessGuard) -> tuple[int, int, list[str]]:
    """Each probe is an input that is WRONG rather than merely EMPTY (S7.8).

    Every probe operates on in-memory copies.  It proves the classes fire; it
    does not prove the tree is safe to edit.
    """
    record = docs[v4mod.RESPONSE]["checkerExecutionRecord"]
    attempted = 0
    caught = 0
    missed: list[str] = []

    def probe(label: str, fires: Callable[[], bool]) -> None:
        nonlocal attempted, caught
        attempted += 1
        try:
            fired = fires()
        except Exception as exc:  # a raised refusal is a catch, not an escape
            fired = isinstance(exc, (ExternalProcessRefused, EnvironmentUnmet, PinDrift))
            if not fired:
                missed.append(label + " (unexpected " + type(exc).__name__ + ": " + str(exc)[:80] + ")")
                return
        if fired:
            caught += 1
        else:
            missed.append(label)

    # 1..13 -- every recorded execution figure falsified one at a time.
    for key in sorted(set(BANNER_JOIN_ALWAYS) | set(BANNER_JOIN_NORMAL)):
        if key not in record:
            continue
        mutated = dict(record)
        mutated[key] = record[key] + 1 if isinstance(record[key], int) else "FALSE"
        probe("record-" + key,
              lambda m=mutated: bool(record_agreement_errors(m, banner, False)))

    # 14..17 -- artifact-derived counts falsified.
    for key in ("v4FinalizerAdmitted", "v4FinalizerInvalid", "v4TransitionRules", "v4RepairWitnesses"):
        mutated = dict(derived)
        mutated[key] = derived[key] + 1
        probe("derived-" + key,
              lambda m=mutated: bool(derived_agreement_errors(m, record, banner, False)))

    # 18..19 -- the declared command stripped of the flags it declares.
    probe("command-flags", lambda: bool(declared_command_errors(
        {**record, "requiredNormalCommand": "python3 docs/coop/artifacts/" + V4_CHECKER})))
    probe("command-target", lambda: bool(declared_command_errors(
        {**record, "requiredSelftestCommand": "python3 -I -B other.py --selftest"})))

    # 20 -- the guard refuses an invocation that is not the enumeration.
    probe("guard-foreign-argv", lambda: _raises(lambda: guard.run(["rg", "--files", "/etc"], cwd=str(REPO_ROOT), check=True, capture_output=True, text=True)))
    # 21 -- the guard refuses any other subprocess capability.
    probe("guard-foreign-attr", lambda: _raises(lambda: guard.Popen))
    # 22 -- the guard refuses the enumeration with weakened flags.
    probe("guard-weak-flags", lambda: _raises(lambda: guard.run(list(guard._argv), cwd=str(REPO_ROOT), check=False, capture_output=True, text=True)))

    # 23 -- a second external invocation appearing in a predecessor is refused.
    probe("closure-second-invocation", lambda: _raises(lambda: derive_enumeration_invocation(
        b"import subprocess\nsubprocess.run(['rg','--files','a'])\nsubprocess.run(['curl','x'])\n", "probe")))
    # 24 -- an invocation whose shape is not the enumeration is refused.
    probe("closure-foreign-shape", lambda: _raises(lambda: derive_enumeration_invocation(
        b"import subprocess\nsubprocess.run(['curl','https://x'])\n", "probe")))

    return caught, attempted, missed


def _raises(thunk: Callable[[], Any]) -> bool:
    try:
        thunk()
    except (ExternalProcessRefused, EnvironmentUnmet, PinDrift):
        return True
    except Exception:
        return False
    return False


# ---------------------------------------------------------------------------
# Published residual: narrative leaves that can be falsified undetected.
# ---------------------------------------------------------------------------

def narrative_leaves(node: Any, path: tuple[Any, ...] = ()) -> Iterable[tuple[tuple[Any, ...], str]]:
    if isinstance(node, dict):
        for key, value in node.items():
            yield from narrative_leaves(value, path + (key,))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from narrative_leaves(value, path + (index,))
    elif isinstance(node, str) and " " in node and len(node) > 25:
        yield path, node


def measure_narrative_residual(v4mod: types.ModuleType, docs: dict[str, Any], v2docs: dict[str, Any],
                               d9doc: Any, d9mod: types.ModuleType, checker_hash: str) -> tuple[int, int]:
    probed = 0
    escaped = 0
    for document in (v4mod.PROTOCOL, v4mod.DELIVERY, v4mod.RI_JOIN, v4mod.RESPONSE):
        for path, value in list(narrative_leaves(docs[document])):
            probed += 1
            mutated = copy.deepcopy(docs)
            target = mutated[document]
            for part in path[:-1]:
                target = target[part]
            target[path[-1]] = value + " This statement is false and the opposite holds."
            errors = v4mod.all_document_errors(mutated, v2docs, d9doc, checker_hash)
            if not errors:
                fsm, _, _, _ = v4mod.safe_fsm_checks(mutated[v4mod.PROTOCOL], v2docs[v4mod.V2_PROTOCOL])
                final, _, _ = v4mod.safe_finalizer_checks(mutated[v4mod.DELIVERY], v2docs[v4mod.V2_DELIVERY], d9doc, d9mod)
                nominal, _ = v4mod.nominal_probe_checks(mutated[v4mod.PROTOCOL])
                witnesses, _ = v4mod.repair_witness_checks(mutated[v4mod.PROTOCOL], v2docs[v4mod.V2_PROTOCOL])
                errors = fsm + final + nominal + witnesses
            if not errors:
                escaped += 1
    return escaped, probed


# ---------------------------------------------------------------------------

def main() -> int:
    selftest = sys.argv[1:] == ["--selftest"]
    mode = "selftest" if selftest else "normal"
    findings = Findings()
    before_pyc = pyc_snapshot()

    # --- environment, declared then checked; failures here are exit 3 --------
    try:
        v2_source = (HERE / V2_CHECKER).read_bytes()
        argv_needed, kwargs_needed = derive_enumeration_invocation(v2_source, V2_CHECKER)
        facts = declared_environment(argv_needed)
    except EnvironmentUnmet as exc:
        print("RPPV5-ENVIRONMENT-UNMET: " + str(exc), file=sys.stderr)
        print("  this is not a finding about the artifacts; the check did not run", file=sys.stderr)
        return 3
    except ExternalProcessRefused as exc:
        print("RPPV5-CLOSURE-UNEXPECTED-INVOCATION: " + str(exc), file=sys.stderr)
        print("  the predecessor's external invocation is not the one this file replaces;", file=sys.stderr)
        print("  a statement about bytes, so a finding: this file may not stand in for it", file=sys.stderr)
        return 1

    # --- this file starts no process, asserted against its own bytes ---------
    probes_caught = self_scan_errors(findings)

    # --- where external-process capability lives in the executed closure -----
    inventory: dict[str, list[tuple[int, str, str]]] = {}
    for name in (V4_CHECKER, V3_CHECKER, V2_CHECKER, D9_CHECKER):
        inventory[name] = scan_external_process((HERE / name).read_bytes(), name)
    inventory_counts = {name: len(rows) for name, rows in inventory.items()}
    findings.require(inventory_counts == RECORDED["closureInventoryCounts"],
                     "RPPV5-CLOSURE-INVENTORY",
                     "measured " + repr(inventory_counts) + " recorded " + repr(RECORDED["closureInventoryCounts"]))
    inventory_sha = sha(compact({k: [list(r) for r in v] for k, v in inventory.items()}))
    findings.require(inventory_sha == RECORDED["closureInventorySha256"],
                     "RPPV5-CLOSURE-INVENTORY",
                     "inventory digest " + inventory_sha[:16] + " recorded " +
                     str(RECORDED["closureInventorySha256"])[:16])

    # --- is the ignore-rule divergence still latent? -------------------------
    subtree = REPO_ROOT / "docs" / "coop" / "artifacts"
    ignore_count, ignore_detail = active_ignore_patterns(REPO_ROOT, subtree)
    findings.require(ignore_count == RECORDED["activeInRepoIgnorePatterns"],
                     "RPPV5-IGNORE-SURFACE-ACTIVE",
                     str(ignore_count) + " active in-repo ignore patterns (" + ", ".join(ignore_detail) +
                     ") -- the divergence between an ignore-respecting enumeration and this one is no longer latent")

    # --- install the enumeration in place of the external process ------------
    guard = ProcessGuard(argv_needed, kwargs_needed)
    had_module = "subprocess" in sys.modules
    saved_module = sys.modules.get("subprocess")
    sys.modules["subprocess"] = guard  # type: ignore[assignment]
    try:
        try:
            v4mod = execute_verified(V4_CHECKER, V4_SHA256, "opensip_rppv4_pinned")
        except PinDrift as exc:
            print("RPPV5-PIN-DRIFT: " + str(exc), file=sys.stderr)
            print("  the checker this file was written against is not the checker on disk;", file=sys.stderr)
            print("  under freeze S7.2 that requires a successor and a new verdict, not a re-run", file=sys.stderr)
            return 1
        except EnvironmentUnmet as exc:
            print("RPPV5-ENVIRONMENT-UNMET: " + str(exc), file=sys.stderr)
            return 3

        normal_code, normal_out, normal_err = run_v4(v4mod, False)
        normal_banner = parse_banner(normal_out, "RPPV4-PASS")
        findings.require(normal_code == 0 and normal_banner is not None,
                         "RPPV5-V4-VERDICT",
                         "v4 normal exit=" + str(normal_code) + " stderr=" + normal_err.strip()[:200])

        selftest_code = None
        selftest_banner = None
        if selftest:
            selftest_code, selftest_out, selftest_err = run_v4(v4mod, True)
            selftest_banner = parse_banner(selftest_out, "RPPV4-PASS")
            findings.require(selftest_code == 0 and selftest_banner is not None,
                             "RPPV5-V4-VERDICT",
                             "v4 selftest exit=" + str(selftest_code) + " stderr=" + selftest_err.strip()[:200])

        # --- the enumeration actually replaced something --------------------
        # A refusal is always meaningful.  The remaining enumeration invariants
        # are only meaningful if v4 got far enough to reach the enumeration; if
        # it refused its own inputs first, saying so once beats four cascaded
        # findings that hide the one that matters.
        findings.require(not guard.refusals, "RPPV5-GUARD-REFUSED", "; ".join(guard.refusals[:4]))
        digests = [obs["sha256"] for obs in guard.observations]
        irregular = sorted({x for obs in guard.observations for x in obs["irregular"]})
        findings.require(not irregular, "RPPV5-ENUM-NONREGULAR", "; ".join(irregular[:4]))
        v4_reached_verdict = (normal_code == 0 and normal_banner is not None
                              and (not selftest or (selftest_code == 0 and selftest_banner is not None)))
        if v4_reached_verdict:
            findings.require(guard.calls > 0, "RPPV5-GUARD-UNUSED",
                             "the replaced enumeration was never reached; this file repaired nothing")
            expected_calls = RECORDED["enumerationCallsPerV4Run"] * (2 if selftest else 1)
            findings.require(guard.calls == expected_calls, "RPPV5-ENUMERATION-CALLS",
                             "measured " + str(guard.calls) + " recorded " + str(expected_calls))
            unsettled = [obs for obs in guard.observations if not obs["settled"]]
            findings.require(not unsettled, "RPPV5-ENUM-DISAGREE",
                             str(len(unsettled)) + " enumeration(s) never settled across 3 attempts -- either "
                             "the two independent walkers disagree or the tree is changing continuously")
        elif guard.calls == 0:
            findings.add("RPPV5-ENUMERATION-NOT-REACHED",
                         "v4 refused before the replaced enumeration was reached, so the enumeration "
                         "invariants were not exercised on this run; the finding above is the cause")
        # The file count is a continuing quantity, not a recorded measurement:
        # the corpus legitimately grows, so it gets a semantic gate (two walkers
        # agree, nothing irregular) and never a byte pin (freeze S7.2.2).  How
        # many DISTINCT sets were seen across the run is disclosed, because a
        # tree edited by a neighbouring lane mid-run is a fact about this run's
        # conditions and belongs in its record (freeze S7.2.1 item 4).
        enumerated = guard.observations[-1]["count"] if guard.observations else 0
        enum_sha = digests[-1] if digests else ""
        enum_variants = len(set(digests))

        # --- register: the recorded binding this file validates --------------
        try:
            register = register_errors(findings)
        except Exception as exc:
            register = {}
            findings.add("RPPV5-REGISTER-UNREADABLE", type(exc).__name__ + ": " + str(exc)[:160])

        # --- re-derivation and three-way agreement ---------------------------
        # A pinned document that will not load is a NAMED finding, never a
        # traceback: v4 has already refused the same bytes above, and the two
        # diagnostics must be legible together.
        docs: dict[str, Any] = {}
        record: Any = {}
        derived: dict[str, int] = {}
        loaded = True
        try:
            docs = load_v4_documents(v4mod)
            record = docs[v4mod.RESPONSE].get("checkerExecutionRecord", {})
            derived = derived_from_artifacts(v4mod, docs)
        except Exception as exc:
            loaded = False
            findings.add("RPPV5-DOCUMENT-LOAD",
                         type(exc).__name__ + ": " + str(exc)[:160] +
                         " -- the pinned candidate documents could not be loaded, so the "
                         "re-derivation and record-agreement checks did not run")
        if loaded:
            findings.require(isinstance(record, dict) and bool(record), "RPPV5-RECORD-MISSING",
                             "the response artifact carries no checkerExecutionRecord")
        if loaded and normal_banner is not None and isinstance(record, dict):
            errs = record_agreement_errors(record, normal_banner, False)
            findings.require(not errs, "RPPV5-RECORD-AGREEMENT", "; ".join(errs[:4]))
            errs = derived_agreement_errors(derived, record, normal_banner, False)
            findings.require(not errs, "RPPV5-DERIVED-AGREEMENT", "; ".join(errs[:4]))
        if loaded and selftest_banner is not None and isinstance(record, dict):
            errs = record_agreement_errors(record, selftest_banner, True)
            findings.require(not errs, "RPPV5-RECORD-AGREEMENT", "; ".join(errs[:4]))
            findings.require(record.get("state") == "NORMAL-AND-SELFTEST-PASS" and normal_code == 0 and selftest_code == 0,
                             "RPPV5-RECORD-AGREEMENT",
                             "recorded state " + repr(record.get("state")) + " with observed exits " +
                             str(normal_code) + "/" + str(selftest_code))
        if loaded:
            findings.require(not declared_command_errors(record if isinstance(record, dict) else {}),
                             "RPPV5-DECLARED-COMMAND",
                             "; ".join(declared_command_errors(record if isinstance(record, dict) else {})[:3]))

        # --- selftest: own mutations and the published residual --------------
        own_caught = own_attempted = 0
        residual_escaped = residual_probed = -1
        if selftest:
            if findings.rows:
                print("RPPV5-DIRTY-BASE: mutation suite refused; normal checks are not clean", file=sys.stderr)
                for row in findings.rows[:30]:
                    print("  " + row, file=sys.stderr)
                return 1
            own_caught, own_attempted, missed = own_mutations(v4mod, docs, normal_banner or {}, derived, guard)
            findings.require(not missed and own_attempted == RECORDED["ownMutations"] and own_caught == own_attempted,
                             "RPPV5-MUTATION",
                             str(own_caught) + "/" + str(own_attempted) + " caught, recorded " +
                             str(RECORDED["ownMutations"]) + "; missed " + "; ".join(missed[:4]))
            # refusals raised by the guard probes are expected; clear them
            guard.refusals.clear()

            preserved: dict[str, Any] = {}
            for name, expected in v4mod.PRESERVED_HASHES.items():
                if not name.endswith(".py"):
                    preserved[name], _ = v4mod.read_hashed(name, expected)
            deps: dict[str, Any] = {}
            for name, expected in v4mod.DEPENDENCY_HASHES.items():
                if not name.endswith(".py"):
                    deps[name], _ = v4mod.read_hashed(name, expected, True)
            v2docs = {key: preserved[key] for key in (
                v4mod.V3_PROTOCOL, v4mod.V3_DELIVERY, v4mod.V3_RI, v4mod.V3_RESPONSE,
                v4mod.V2_PROTOCOL, v4mod.V2_DELIVERY, v4mod.V2_RI, v4mod.V2_RESPONSE)}
            d9mod = execute_verified(D9_CHECKER, v4mod.DEPENDENCY_HASHES[D9_CHECKER], "opensip_d9v113_pinned")
            checker_hash = sha((HERE / V4_CHECKER).read_bytes())
            residual_escaped, residual_probed = measure_narrative_residual(
                v4mod, docs, v2docs, deps[v4mod.D9], d9mod, checker_hash)
            findings.require(
                (residual_escaped, residual_probed) ==
                (RECORDED["narrativeLeavesFalsifiableWithoutDetection"], RECORDED["narrativeLeavesProbed"]),
                "RPPV5-RESIDUAL-STALE",
                "measured " + str(residual_escaped) + "/" + str(residual_probed) + " published " +
                str(RECORDED["narrativeLeavesFalsifiableWithoutDetection"]) + "/" +
                str(RECORDED["narrativeLeavesProbed"]))
    except ExternalProcessRefused as exc:
        print("RPPV5-GUARD-REFUSED: " + str(exc), file=sys.stderr)
        print("  the closure asked for an external-process capability this file does not provide;", file=sys.stderr)
        print("  the enumeration replacement covers exactly " + " ".join(argv_needed), file=sys.stderr)
        return 1
    except PinDrift as exc:
        print("RPPV5-PIN-DRIFT: " + str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        # Nothing this instrument does may surface as a bare traceback.  The
        # defect this file repairs went unnoticed for three versions precisely
        # because a crash looks like a failure looks like a finding.
        frames = traceback.extract_tb(exc.__traceback__)
        where = (frames[-1].filename.rsplit("/", 1)[-1] + ":" + str(frames[-1].lineno)) if frames else "unknown"
        print("RPPV5-INTERNAL: " + type(exc).__name__ + ": " + str(exc)[:200] + " at " + where, file=sys.stderr)
        print("  this instrument failed to complete; that is NOT a verdict about the artifacts", file=sys.stderr)
        return 3
    finally:
        if had_module:
            sys.modules["subprocess"] = saved_module  # type: ignore[assignment]
        else:
            sys.modules.pop("subprocess", None)

    findings.require(pyc_snapshot() == before_pyc, "RPPV5-PYC", "bytecode files were created or changed")

    header = ("RPPV5-FAIL" if findings.rows else "RPPV5-PASS")
    line = (header + " mode=" + mode +
            " checks=" + str(findings.checks) +
            " v4_exit=" + str(normal_code) +
            (" v4_selftest_exit=" + str(selftest_code) if selftest else "") +
            " enumerated=" + str(enumerated) +
            " enumeration_sha256=" + enum_sha[:16] +
            " enumeration_calls=" + str(guard.calls) +
            " enumeration_variants=" + str(enum_variants) +
            " external_processes=0" +
            " scanner_probes=" + str(probes_caught) + "/" + str(len(DIRTY_PROBES)) +
            " closure_touchpoints=" + str(sum(inventory_counts.values())) +
            " active_ignore_patterns=" + str(ignore_count) +
            (" own_mutations=" + str(own_caught) + "/" + str(own_attempted) if selftest else "") +
            (" narrative_escapes=" + str(residual_escaped) + "/" + str(residual_probed) if selftest else ""))
    if findings.rows:
        print(line, file=sys.stderr)
        for row in findings.rows[:40]:
            print("  " + row, file=sys.stderr)
        return 1

    print(line)
    for relayed in (normal_banner, selftest_banner):
        if relayed is not None:
            print("RPPV5-RELAY RPPV4-PASS " + " ".join(k + "=" + v for k, v in relayed.items()))
    print("RPPV5-ENVIRONMENT python=" + str(facts["python"]) +
          " isolated=true dont_write_bytecode=true" +
          " predecessor_external_tool=" + str(facts["predecessorExternalTool"]) +
          " predecessor_tool_on_path=" + ("true" if facts["predecessorToolOnPath"] else "false") +
          " global_git_excludes=" + str(facts["globalGitExcludes"]) +
          " closure_inventory_sha256=" + inventory_sha[:16] +
          " register_validator=" + str(register.get("validator", "?")) +
          " register_members=" + str(register.get("members", 0)))
    if not facts["predecessorToolOnPath"]:
        print("RPPV5-SECTION-7.2 the validator claim-register.v1.json names for " + CLAIM_ID + " is " +
              str(register.get("validator", "?")) + ", which requires the external tool '" +
              str(facts["predecessorExternalTool"]) + "'; it is NOT an executable on PATH here, so that " +
              "validator cannot run in this environment and its recorded PASSED verdict is not reproducible " +
              "here. A verdict binds bytes AND an environment.")
    print("RPPV5-REPAIR the replaced call enumerated files only. This file enumerates with the standard "
          "library and consults no ignore file, so it is ignore-independent BY CONSTRUCTION. That removes a "
          "LATENT environment dependency; it does not fix an active bug -- measured this run, "
          + str(ignore_count) + " active in-repo ignore patterns bear on the subtree, so an ignore-respecting "
          "enumeration and this one return the same set today.")
    print("RPPV5-RESIDUAL independent-review-required applied=false self_review=false product=false "
          "integration=false freeze=false release=false")
    print("RPPV5-BOUND a green run here is author-side evidence: the bytes are the reviewed bytes and drift "
          "stops the run, everything recomputable was recomputed and agrees, and the artifacts' own recorded "
          "execution figures match a run that actually happened. It is NOT evidence that the artifacts are "
          "right. Measured by --selftest: " +
          (str(residual_escaped) + " of " + str(residual_probed) if selftest else
           str(RECORDED["narrativeLeavesFalsifiableWithoutDetection"]) + " of " +
           str(RECORDED["narrativeLeavesProbed"])) +
          " narrative leaves (" + str(RECORDED["narrativeLeafDefinition"]) + ") can be falsified with an "
          "appended false sentence and no check fires. This file does not close them and does not claim to.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
