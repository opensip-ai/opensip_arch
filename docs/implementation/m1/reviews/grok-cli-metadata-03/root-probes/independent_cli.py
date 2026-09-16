#!/usr/bin/env python3
"""Independent CLI metadata03 probes. Not a restatement of startup_tests.rs."""
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-root-cli03-reproduction/copy")
BIN = COPY / "target/debug/opensip"
OUT = Path("/tmp/opensip-implementation/m1-root-cli03-reproduction/results")
rows: list[dict] = []


def run(args: list[str], *, cwd: Path, extra_env: dict | None = None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    env = {
        "LANG": "C",
        "PATH": "/usr/bin:/bin",
        "HOME": str(cwd / "missing-home"),
        "OPENSIP_BUILD_CHANNEL": "release",
        "OPENSIP_HOST_RELEASE": "99.99.99",
        "OPENSIP_CLOSURE_IDS": "closure2:" + "f" * 64,
        "OPENSIP_STORE": str(cwd / "missing-store"),
        "OPENSIP_COMPONENTS": str(cwd / "missing-providers"),
    }
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [str(BIN), *args],
        cwd=cwd,
        env=env,
        stdout=stdout,
        stderr=stderr,
        check=False,
    )


def check(name: str, passed: bool, detail: str = "") -> None:
    rows.append({"name": name, "passed": bool(passed), "detail": detail})
    print(("PASS" if passed else "FAIL"), name, detail)


def main() -> int:
    if not BIN.is_file():
        raise SystemExit(f"missing binary {BIN}")
    tmp = Path(tempfile.mkdtemp(prefix="opensip-grok-cli-"))
    (tmp / ".opensip").mkdir()
    (tmp / ".opensip/config.json").write_text("not valid configuration")
    (tmp / "package.json").write_text("not valid package data")
    try:
        p = run(["version", "--format=json"], cwd=tmp)
        v = json.loads(p.stdout)
        check(
            "env-release-ignored-development-only",
            p.returncode == 0
            and p.stderr == b""
            and v["schemaMajor"] == 7
            and v["meta"]["buildChannel"] == "development"
            and v["meta"]["hostRelease"] != "99.99.99"
            and v["meta"]["closureIds"] == [],
            f"hostRelease={v['meta']['hostRelease']!r} channel={v['meta']['buildChannel']!r}",
        )
        check(
            "request-id-is-host-minted-req1",
            isinstance(v.get("requestId"), str)
            and v["requestId"].startswith("req1_")
            and len(v["requestId"]) == 37
            and all(c in "0123456789abcdef" for c in v["requestId"][5:]),
            v.get("requestId", "")[:12],
        )
        p = run(["version", "--request-id", "req1_00000000000000000000000000000000", "--format=json"], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "caller-request-id-refused-and-not-used",
            p.returncode == 2
            and r["requestId"] != "req1_00000000000000000000000000000000"
            and r["termination"]["errorCode"] == "REQUEST.UNKNOWN_OPTION"
            and r.get("errors") == [],
            r.get("requestId", "")[:12],
        )
        p = run(["version", "--build-channel=release", "--format=json"], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "caller-build-channel-refused",
            p.returncode == 2
            and r["termination"]["errorCode"] == "REQUEST.UNKNOWN_OPTION"
            and "meta" not in r,
        )
        p = run(["--format=json"], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "no-args-honestly-unimplemented",
            p.returncode == 2
            and any("Default analysis is not implemented" in d for d in r.get("diagnostics", [])),
            str(r.get("diagnostics")),
        )
        # 1024 arguments: 1024 'help' words is too many (count 1024 is allowed; 1025th fails).
        p = run(["--format=json", *(["help"] * 1024)], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "1024-words-plus-format-is-too-many",
            p.returncode == 2 and any("Too many command arguments." in d for d in r.get("diagnostics", [])),
            str(r.get("diagnostics")),
        )
        # Option values count: attached --format=json + 1022 words + option name + value = 1025.
        # If the value were not counted, this would be an unknown-command refusal instead.
        p = run(["--format=json", *(["help"] * 1022), "--client-correlation-id", "z"], cwd=tmp)
        r = json.loads(p.stdout)
        diags = r.get("diagnostics") or []
        check(
            "option-value-counts-toward-1024",
            p.returncode == 2 and any("Invalid client correlation ID." in d for d in diags),
            str(diags),
        )
        huge = "x" * 4097
        p = run(["--format", huge, "version"], cwd=tmp)
        text = p.stdout.decode()
        check(
            "option-value-4097-bytes-refused-not-echoed",
            p.returncode == 2 and huge not in text and huge not in p.stderr.decode(),
            f"exit={p.returncode}",
        )
        p = run(["version", "--format=json", "--client-correlation-id", "x" * 129], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "oversize-correlation-omits-field",
            p.returncode == 2 and "clientCorrelationId" not in r,
        )
        p = run(["version", "--format=json", "--client-correlation-id", "🙂" * 128], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "unicode-correlation-128-scalars-ok-distinct-from-request",
            p.returncode == 0 and r["clientCorrelationId"] == "🙂" * 128 and r["requestId"] != r["clientCorrelationId"],
        )
        bad = b"version\xff"
        p = subprocess.run(
            [str(BIN), "--format=json", bad],
            cwd=tmp,
            env={"LANG": "C", "PATH": "/usr/bin:/bin", "HOME": str(tmp / "missing-home")},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        r = json.loads(p.stdout)
        check(
            "non-unicode-argument-refused",
            p.returncode == 2 and any("valid Unicode" in d for d in r.get("diagnostics", [])),
            str(r.get("diagnostics")),
        )
        p = run(["help", "\x1b]0;caller\x07", "--format=json"], cwd=tmp)
        r = json.loads(p.stdout)
        human = run(["help", "\x1b]0;caller\x07"], cwd=tmp)
        htxt = human.stdout.decode()
        check(
            "escape-topic-json-diagnostic-human-no-raw-escape",
            p.returncode == 2
            and "\x1b" not in htxt
            and "caller" not in htxt
            and human.returncode == 2,
            repr(htxt[:80]),
        )
        p = run(["version", "--format=sarif"], cwd=tmp)
        htxt = p.stdout.decode()
        check(
            "human-detail-remedy-labels-format-not-applicable",
            p.returncode == 2
            and "Detail: OUTPUT.FORMAT_NOT_APPLICABLE\n" in htxt
            and "Remedy: Choose an applicable output format.\n" in htxt
            and "Termination: request-rejected\n" in htxt
            and "Error: REQUEST.UNKNOWN_OPTION\n" in htxt
            and "Request: req1_" in htxt,
            htxt,
        )
        p = run(["--nope"], cwd=tmp)
        htxt = p.stdout.decode()
        check(
            "human-unknown-option-empty-errors-still-has-termination",
            p.returncode == 2
            and "Termination: request-rejected\n" in htxt
            and "Error: REQUEST.UNKNOWN_OPTION\n" in htxt
            and "Detail:" not in htxt,
        )
        # Read-only stdout: JSON and human, exact fixed stderr, no second envelope.
        for mode, args in [("json", ["version", "--format=json"]), ("human", ["version"])]:
            ro = os.open(tmp / "package.json", os.O_RDONLY)
            p = subprocess.run(
                [str(BIN), *args],
                cwd=tmp,
                env={"LANG": "C", "PATH": "/usr/bin:/bin", "HOME": str(tmp / "missing-home")},
                stdout=ro,
                stderr=subprocess.PIPE,
                check=False,
            )
            os.close(ro)
            check(
                f"readonly-stdout-{mode}-exit4-fixed-stderr",
                p.returncode == 4
                and p.stderr == b"OUTPUT.SERIALIZATION_FAILED: required output emission failed.\n"
                and b"{" not in p.stderr
                and b"req1_" not in p.stderr,
                repr(p.stderr),
            )
        # Real EPIPE: close the read end before the child writes.
        for mode, args in [
            ("json", ["--format=json", "version"]),
            ("human", ["version"]),
            ("completion", ["completion", "bash"]),
        ]:
            rfd, wfd = os.pipe()
            os.close(rfd)
            p = subprocess.Popen(
                [str(BIN), *args],
                cwd=tmp,
                env={"LANG": "C", "PATH": "/usr/bin:/bin", "HOME": str(tmp / "missing-home")},
                stdout=wfd,
                stderr=subprocess.PIPE,
            )
            os.close(wfd)
            err = p.stderr.read()
            code = p.wait()
            check(
                f"epipe-{mode}-exit4-fixed-stderr",
                code == 4 and err == b"OUTPUT.SERIALIZATION_FAILED: required output emission failed.\n",
                f"exit={code} stderr={err!r}",
            )
        # Side effects: no project/store/home created; config not rewritten.
        before = (tmp / ".opensip/config.json").read_bytes()
        run(["help", "--format=json"], cwd=tmp)
        run(["version"], cwd=tmp)
        run(["completion", "zsh"], cwd=tmp)
        check(
            "no-project-store-home-side-effects",
            not (tmp / "missing-home").exists()
            and not (tmp / "missing-store").exists()
            and not (tmp / "missing-providers").exists()
            and (tmp / ".opensip/config.json").read_bytes() == before
            and list((tmp / ".opensip").iterdir()) == [tmp / ".opensip/config.json"],
        )
        p = run(["completion", "bash", "--format=json"], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "completion-json-format-not-applicable",
            p.returncode == 2 and r["errors"][0]["code"] == "OUTPUT.FORMAT_NOT_APPLICABLE",
        )
        p = run(["--"], cwd=tmp)
        check("option-terminator-not-selected", p.returncode == 2)
        p = run(["help", "--format=json", "--format=json"], cwd=tmp)
        r = json.loads(p.stdout)
        check(
            "duplicate-format-refused",
            p.returncode == 2 and any("more than once" in d for d in r.get("diagnostics", [])),
            str(r.get("diagnostics")),
        )
        # 45-command scope: advertised catalogue remains 3 names.
        p = run(["help", "--format=json"], cwd=tmp)
        names = [row["name"] for row in json.loads(p.stdout)["meta"]["commands"]]
        check("advertised-catalogue-is-three-implemented", names == ["completion", "help", "version"], str(names))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failed = [r["name"] for r in rows if not r["passed"]]
    (OUT / "independent-cli.json").write_text(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed, "cases": rows}, indent=2) + "\n")
    print(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed}))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
