"""Independent source/control probes for report-help01. Browser lane is separate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-grok-report-help-review-01/review/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-report-help-review-01/review/results")
FROZEN = Path("/tmp/opensip-implementation/m1-report-help-subject-01")
HIST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/report-help-start")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    rows = []
    ts = (COPY / "help-view.ts").read_text()
    rec(
        rows,
        "source-never-assigns-html-sinks",
        "innerHTML" not in ts
        and "outerHTML" not in ts
        and "insertAdjacentHTML" not in ts
        and "paragraph.textContent = text" in ts
        and 'dialog.setAttribute("aria-label"' in ts
        and "heading.textContent = title" in ts
        and "opener.textContent" in ts,
    )
    rec(
        rows,
        "native-modal-dialog-and-idempotent-dispose",
        "dialog.showModal()" in ts
        and "closeButton.autofocus = true" in ts
        and "if (disposed) return" in ts
        and "dialog.removeEventListener(\"close\", returnFocus)" in ts,
    )
    rec(
        rows,
        "fresh-tsc-emit-equals-frozen-emitted",
        sha(COPY / "tsc-out/help-view.js") == sha(COPY / "emitted/help-view.js") == sha(FROZEN / "emitted/help-view.js"),
        observed=sha(COPY / "tsc-out/help-view.js"),
    )
    rec(
        rows,
        "product-snapshot-bytes-match-freeze",
        sha(PRODUCT / "apps/report/src/help-view.ts") == sha(FROZEN / "help-view.ts")
        and sha(PRODUCT / "apps/report/src/report.css") == sha(FROZEN / "report.css"),
    )
    rec(
        rows,
        "print-css-hides-help-control",
        "@media print { .report-help { display: none; } }" in (COPY / "report.css").read_text().replace("\n", " ")
        or ".report-help { display: none; }" in (COPY / "report.css").read_text(),
    )
    rec(
        rows,
        "historical-enter-harness-failures-preserved",
        json.loads((HIST / "browser-01/failure.json").read_bytes())["checks"][1]["passed"] is False
        and json.loads((HIST / "browser-02/failure.json").read_bytes())["checks"][1]["passed"] is False
        and "keyboard opens labelled modal" in json.loads((HIST / "browser-01/failure.json").read_bytes())["error"],
    )
    tree = json.loads((COPY / "accessibility-tree.json").read_bytes())
    names = []
    for node in tree.get("nodes", []):
        name = node.get("name", {})
        if isinstance(name, dict):
            names.append(name.get("value"))
        role = node.get("role", {})
        if isinstance(role, dict) and role.get("value") in ("Dialog", "dialog"):
            names.append(("dialog", name.get("value") if isinstance(name, dict) else name))
    rec(
        rows,
        "ax-tree-has-labelled-dialog-and-close",
        "About Evidence scope" in json.dumps(tree) and "Close help" in json.dumps(tree) and "activeModalDialog" in json.dumps(tree),
    )
    rec(
        rows,
        "help-copy-is-caller-supplied-inert-text-only",
        "This control does not read report data" in ts
        and "must describe the actual evidence limitations" in (COPY / "README.md").read_text(),
    )
    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok report-help01 source/control probes; not screen-reader/CSP/all-browser qualification",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-help.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
