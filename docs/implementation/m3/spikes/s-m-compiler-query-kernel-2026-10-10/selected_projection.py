"""Exact selected reference functions, experimental data projection only.
Caller path sets are data; this does not verify snapshot or closure admission.
"""
import re

_CFG_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*(="[^"\\]*")?$')

_LINT_RE = re.compile(r'^[a-z0-9_:]+$')

_ALLOWED_C = {"target-feature", "target-cpu", "opt-level", "debuginfo", "panic", "overflow-checks", "debug-assertions", "strip"}

_ALLOWED_C_VALUES = re.compile(r'^[A-Za-z0-9_+,\-.=]+$')

def rustflags_projection(flags: list[str], snapshot_paths: set[str], closure_paths: set[str]) -> dict:
    """Exact allowlist. Anything selecting a tool, a path, a link argument, a sysroot, a response
    file or a codegen backend is stripped and disclosed. --remap-path-prefix is honored only when
    its FROM component is a verified in-snapshot or in-closure path."""
    honored: list[str] = []; stripped: list[dict] = []
    i = 0
    while i < len(flags):
        f = flags[i]; nxt = flags[i + 1] if i + 1 < len(flags) else None
        def take2(reason_ok: bool, why: str) -> None:
            nonlocal i
            if nxt is None:
                stripped.append({"flag": f, "reason": "dangling"}); i += 1; return
            if reason_ok:
                honored.extend([f, nxt])
            else:
                stripped.append({"flag": f + " " + nxt, "reason": why})
            i += 2
        if f.startswith("@"):
            stripped.append({"flag": f, "reason": "response-file"}); i += 1
        elif f == "--cfg":
            take2(nxt is not None and bool(_CFG_RE.match(nxt)), "cfg-syntax")
        elif f.startswith("--cfg="):
            v = f[len("--cfg="):]
            (honored.append(f) if _CFG_RE.match(v) else stripped.append({"flag": f, "reason": "cfg-syntax"})); i += 1
        elif f in ("-A", "-W", "-D", "-F", "--allow", "--warn", "--deny", "--forbid"):
            take2(nxt is not None and bool(_LINT_RE.match(nxt)), "lint-syntax")
        elif f.startswith("--cap-lints=") or f.startswith(("-A", "-W", "-D", "-F")) and len(f) > 2 and _LINT_RE.match(f[2:]):
            honored.append(f); i += 1
        elif f == "--cap-lints":
            take2(nxt in ("allow", "warn", "deny", "forbid"), "cap-lints-value")
        elif f in ("-C", "--codegen"):
            ok = nxt is not None and "=" in nxt and nxt.split("=", 1)[0] in _ALLOWED_C and bool(_ALLOWED_C_VALUES.match(nxt.split("=", 1)[1]))
            take2(ok, "codegen-option-not-allowlisted")
        elif f.startswith("-C"):
            body = f[2:]
            ok = "=" in body and body.split("=", 1)[0] in _ALLOWED_C and bool(_ALLOWED_C_VALUES.match(body.split("=", 1)[1]))
            (honored.append(f) if ok else stripped.append({"flag": f, "reason": "codegen-option-not-allowlisted"})); i += 1
        elif f == "--remap-path-prefix" or f.startswith("--remap-path-prefix="):
            val = nxt if f == "--remap-path-prefix" else f[len("--remap-path-prefix="):]
            src = val.split("=", 1)[0] if val and "=" in val else None
            ok = src is not None and (src in snapshot_paths or src in closure_paths)
            if f == "--remap-path-prefix":
                take2(ok, "remap-from-outside-snapshot-or-closure")
            else:
                (honored.append(f) if ok else stripped.append({"flag": f, "reason": "remap-from-outside-snapshot-or-closure"})); i += 1
        else:
            stripped.append({"flag": f, "reason": "not-allowlisted"}); i += 1
    return {"honored": honored, "stripped": stripped, "executableSelected": False}
