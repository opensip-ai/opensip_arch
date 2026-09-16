"""Pre-correction baseline over the unedited work/source39 capture: workflow projection, query projection, evaluator
composition and the historical workflow1 checker, each with a receipt; reports go to the runtime, never into the capture."""
import sys
from pathlib import Path

R = Path("/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1")
sys.path.insert(0, str(R))
import runner  # noqa: E402

DC = R / "work/source39/docs/coop/design-corrections"
out = R / "work/baseline-checks"
out.mkdir(parents=True, exist_ok=True)
runner.run("baseline-check-composition-v3", [runner.PY, "-I", "-B", "check-composition.v3.py"], cwd=DC / "foundation")
runner.run("baseline-check-workflows-v1", [runner.PY, "-I", "-B", "check_workflows.v1.py", "--report", str(out / "workflows-report.v1.json")], cwd=DC / "workflows")
runner.run("baseline-check-query-projection-v3", [runner.PY, "-I", "-B", "check-query-projection.v3.py", "--report", str(out / "query-projection-report.json")], cwd=DC / "workflows")
runner.run("baseline-check-workflow-projection-v3", [runner.PY, "-I", "-B", "check-workflow-projection.v3.py"], cwd=DC / "workflows")
(out / "DONE").write_text("done\n")
