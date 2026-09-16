#!/bin/sh
# Challenge old CLI02 B-01: dropping Detail/Remedy labels must now fail the human test.
set -e
SRC=/tmp/opensip-implementation/m1-grok-cli-metadata-review-03/review
MUT="$SRC/mutants/drop-detail-labels"
rm -rf "$MUT"
# Copy only crates/apps needed; reuse workspace files from private copy via symlink of lock/toml
mkdir -p "$MUT"
# Work in a copy of reporting + full workspace is simpler: copy source tree excluding target
python3 - <<'PY'
import shutil, pathlib
src=pathlib.Path("/tmp/opensip-implementation/m1-grok-cli-metadata-review-03/review/copy")
dst=pathlib.Path("/tmp/opensip-implementation/m1-grok-cli-metadata-review-03/review/mutants/drop-detail-labels")
if dst.exists(): shutil.rmtree(dst)
def ignore(dir, names):
    return [n for n in names if n in {"target", "metadata-current03", "metadata-current04", "compiled-report", "schemas", "tools", "providers", "apps/report"}]
shutil.copytree(src, dst, ignore=ignore, symlinks=True)
p=dst/"crates/reporting/src/human_renderer.rs"
t=p.read_text()
old='''                    writeln!(
                        &mut text,
                        "Detail: {}\\nRemedy: {}",
                        detail.code,
                        detail.remedy.as_str()
                    )'''
new='''                    writeln!(
                        &mut text,
                        "{}{}",
                        detail.code,
                        detail.remedy.as_str()
                    )'''
if old not in t:
    raise SystemExit("mutant site not found")
p.write_text(t.replace(old, new, 1))
print("mutated", p)
PY
export PATH="/opt/homebrew/bin:/usr/bin:/bin"
cd "$MUT"
# Isolate target
export CARGO_TARGET_DIR="$SRC/results/mutant-target"
echo "=== mutant cargo test human_failure... ==="
set +e
cargo test --locked --offline -p opensip-cli --test startup_tests human_failure_and_success_display_termination_and_registered_details -- --exact > "$SRC/results/b01-mutant.stdout" 2> "$SRC/results/b01-mutant.stderr"
echo "mutant-exit=$?"
# also run the other 5 startup tests to see if only that one dies
cargo test --locked --offline -p opensip-cli --test startup_tests -- --test-threads=1 >> "$SRC/results/b01-mutant-all.stdout" 2>> "$SRC/results/b01-mutant-all.stderr"
echo "mutant-all-exit=$?"
python3 - <<'PY'
from pathlib import Path
for name in ["b01-mutant.stdout","b01-mutant.stderr","b01-mutant-all.stdout","b01-mutant-all.stderr"]:
    t=Path("/tmp/opensip-implementation/m1-grok-cli-metadata-review-03/review/results")/name
    print("====", name, "====")
    print(t.read_text()[-2500:])
PY
