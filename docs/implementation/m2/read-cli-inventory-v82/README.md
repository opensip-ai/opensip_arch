# Read-only CLI inventory82

Adds exactly three sources to selected inventory81, which is X1a's ordinary writer layout:
- apps/cli/tests/doctor_tests.rs
- crates/host/src/doctor_ingress.rs
- crates/host/src/doctor_ingress_tests.rs

It keeps every existing row by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations. No crate or dependency is added. The rows are unit X10a, law X10 r3 (accepted by Codex on 2026-09-30), based on product f7acb6d.

- **doctor_ingress.rs (adapter)** is the `opensip doctor` ingress beside the metadata ingress. It makes one producer call, `observe_installation_for_doctor`, and projects doctor's outcome onto command-envelope v7 per item 3:
  - a report, or a report that cannot be produced, is `kind: doctor`;
  - an unreachable installation is `kind: failure` with its law 468 item 6 row.
- **doctor_ingress_tests.rs (test)** is the host layer of item 5. It covers projection, rendering, schema validity and parity for every value the security layer produces, plus the explicitly synthetic report-bound vectors.
- **doctor_tests.rs (test)** is the binary layer of item 5:
  - the real dev-build `opensip doctor` in both formats;
  - help and completion;
  - the source pins.

The unit's other changes edit existing rows, whose descriptions stay accurate except one:
- **apps/cli:**
  - arguments.rs parses `doctor`;
  - bootstrap.rs dispatches it;
  - startup_tests.rs lists `doctor` in the catalogue.
- **host:**
  - outcomes.rs gains the catalogue row and a request-id accessor;
  - lib.rs wires the ingress;
  - doctor_report.rs uses the selected golden's `doctor-defects-found` remedy, and the human label is now the renderer's constant.
- **reporting:** human_renderer.rs gains the doctor and detailed-failure renderings with the shared termination lines, and lib.rs exports the label.
- **security:** installation_doctor_tests.rs adds the chain finding and the account, no-premise, budget and not-initialized rows.

The exception is doctor_report.rs, whose inherited description ends "Library only: nothing emits it yet." Inventory successors carry inherited rows by value, so the fix belongs to a later description-only contract successor on this inventory once it is selected, as 461b did for 458c.

The projection carries the sixteen effective description overrides bound to inventory81, all by stable file path: the eight inherited through inventory80 and 461b's eight overrides on inventory80. The projection helper is inventory80's helper with the row count set to sixteen. Run it with python3 -I -B.

`evidence/build_v82.py` rebuilds inventory82 and successor.json deterministically. If X10a were integrated before X1a, it builds inventory81 from inventory80 instead (`--parent 80 --candidate 81 --prior doctor-report-inventory-v80`). The X10b contract successor (golden wording only) is independent of this inventory. The selected product verifier is unchanged.
