"""Pre-edit baseline: run the historical workflow1 checker, the current query checker and the current workflow projection
checker against the unedited work/source copy, each with a receipt. The historical checker's report goes to the runtime,
never into the source copy."""
import sys
from pathlib import Path

R = Path("/private/tmp/opensip-design-corrections/claude-policy-test-profile-author.v1")
sys.path.insert(0, str(R))
import runner  # noqa: E402

W = R / "work/source/docs/coop/design-corrections/workflows"
F = R / "work/source/docs/coop/design-corrections/foundation"
out = R / "work/baseline-checks"
out.mkdir(parents=True, exist_ok=True)
runner.run("baseline-check-workflows-v1", [runner.PY, "-I", "-B", "check_workflows.v1.py", "--report", str(out / "workflows-report.v1.json")], cwd=W)
runner.run("baseline-check-array-orders", [runner.PY, "-I", "-B", "check-array-orders.py", "--report", str(out / "array-orders-report.json")], cwd=F)
runner.run("baseline-check-query-projection-v3", [runner.PY, "-I", "-B", "check-query-projection.v3.py"], cwd=W)
runner.run("baseline-check-workflow-projection-v3", [runner.PY, "-I", "-B", "check-workflow-projection.v3.py"], cwd=W)
(out / "DONE").write_text("done\n")
