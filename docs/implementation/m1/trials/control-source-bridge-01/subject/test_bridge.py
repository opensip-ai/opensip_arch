"""Bridge tests over a mirror that contains only declared, pinned architecture inputs.

Run from anywhere with TMPDIR outside this closure:
  OPENSIP_ARCHITECTURE=<opensip_arch checkout> python3 -B test_bridge.py -v

Review and assent documents built here are SYNTHETIC verifier-test fixtures,
written only under TMPDIR. They are not reviews, assent or acceptance.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

if not sys.flags.dont_write_bytecode:
    raise SystemExit("run tests with python -B")

UNIT = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("check_bridge", UNIT / "check_bridge.py")
CB = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CB)
SCHEMA = CB.SCHEMA
SYNTHETIC = "SYNTHETIC verifier-test fixture under TMPDIR: not an independent review, not root assent, not acceptance"


def dump(value):
    return (json.dumps(value, indent=2) + "\n").encode()


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        CB.require_environment()
        real = os.environ.get("OPENSIP_ARCHITECTURE")
        if not real:
            raise RuntimeError("set OPENSIP_ARCHITECTURE to the architecture checkout")
        cls.V, _ = CB.load_verifier(UNIT)
        cls.inputs = json.loads((UNIT / "inputs.json").read_bytes())
        cls.lock = json.loads((UNIT / "snapshot" / "design-lock.json").read_bytes())
        cls.store = tempfile.TemporaryDirectory(prefix="control-bridge-tests-")
        cls.pristine = Path(cls.store.name) / "architecture"
        for row in cls.inputs["architecture"]:
            CB.write_tree(cls.pristine, {row["path"]: cls.V.pinned_bytes(Path(real).resolve(), row)})

    @classmethod
    def tearDownClass(cls):
        cls.store.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="control-bridge-case-")
        self.addCleanup(self.tmp.cleanup)
        self.arch = Path(self.tmp.name) / "architecture"
        shutil.copytree(self.pristine, self.arch)

    def refuses(self, pattern, call):
        # Each checker call loads its own verifier module, so match the shared base class.
        with self.assertRaisesRegex(ValueError, pattern):
            call()

    def unit(self, record=None, subject=None, inputs=None, snapshot_suffix=b""):
        """Copy the closure with fully rebound successor and selection subject."""
        unit = Path(tempfile.mkdtemp(prefix="unit-", dir=self.tmp.name))
        (unit / "snapshot").mkdir()
        for name in ("snapshot/verify_design.py", "snapshot/design-lock.json"):
            shutil.copyfile(UNIT / name, unit / name)
        with (unit / "snapshot" / "verify_design.py").open("ab") as handle:
            handle.write(snapshot_suffix)
        document = json.loads((UNIT / "successor.json").read_bytes())
        if record:
            record(document)
        record_raw = dump(document)
        (unit / "successor.json").write_bytes(record_raw)
        selection = json.loads((UNIT / "selection-subject.json").read_bytes())
        selection["files"] = sorted([*document["candidates"], CB.pin_of(f"{CB.STAGED}/successor.json", record_raw)],
                                    key=lambda row: row["path"])
        if subject:
            subject(selection)
        (unit / "selection-subject.json").write_bytes(dump(selection))
        declared = copy.deepcopy(self.inputs)
        if inputs:
            inputs(declared)
        (unit / "inputs.json").write_bytes(dump(declared))
        return unit

    def put(self, path, value):
        raw = value if isinstance(value, bytes) else dump(value)
        CB.write_tree(self.arch, {path: raw})
        return CB.pin_of(path, raw)

    def stage(self, unit=UNIT, review=None, assent=None, directory="synthetic-not-acceptance"):
        """Place the staged successor and SYNTHETIC review/assent fixtures in the mirror."""
        record_pin = self.put(f"{CB.STAGED}/successor.json", (unit / "successor.json").read_bytes())
        subject_pin = self.put(f"{CB.STAGED}/selection-subject.json", (unit / "selection-subject.json").read_bytes())
        review_doc = {"schemaVersion": 1, CB.SYNTHETIC_MARKER: SYNTHETIC, "verdict": "ACCEPT-DESIGN-UNIT",
                      "subjectManifestSha256": subject_pin["sha256"], "requiredFindings": []}
        if review:
            review(review_doc)
        review_pin = self.put(f"{directory}/review.json", review_doc)
        assent_doc = {"schemaVersion": 1, CB.SYNTHETIC_MARKER: SYNTHETIC, "status": "ACCEPTED-DESIGN-UNIT",
                      "rootSubstantiveAssent": True, "requiredUnitFindings": [], "subjectManifest": subject_pin,
                      "actualClaudeReview": review_pin, "acceptedSuccessor": record_pin}
        if assent:
            assent(assent_doc)
        assent_pin = self.put(f"{directory}/assent.json", assent_doc)
        return {"record": record_pin, "subjectManifest": subject_pin, "review": review_pin, "assent": assent_pin}

    def staged_lock(self, binding):
        lock = copy.deepcopy(self.lock)
        lock["contractSuccessors"].append(binding)
        return lock

    def declared(self):
        return CB.Declared(self.V, self.arch, self.inputs["architecture"])

    def effective(self):
        rows = {}
        for key in ("sourceManifest", "applicationManifest"):
            for row in json.loads(self.V.pinned_bytes(self.arch, self.lock["approvals"][key]))["files"]:
                rows[row["path"]] = row
        return rows

    def test_closure_verifies_historical_chain_from_declared_inputs_only(self):
        mirrored = {path.relative_to(self.arch).as_posix() for path in self.arch.rglob("*") if path.is_file()}
        self.assertEqual(mirrored, {row["path"] for row in self.inputs["architecture"]})
        report = CB.verify_bridge(self.arch)
        self.assertIs(report["passed"], True)
        self.assertEqual(report["candidate"], SCHEMA)
        self.assertEqual(report["parent"], CB.APPLICATION)
        self.assertEqual((report["reviewVerdict"], report["reviewMustFindings"], report["frozenMembersVerified"]),
                         (CB.REVIEW_VERDICT, 0, 8))
        self.assertEqual(report["sourcePreflight"], {"liveRefusal": CB.REFUSAL, "sourcesVerifiedWithoutControl": 28})
        self.assertEqual((report["acceptance"], report["productQualification"]), (False, False))
        self.assertEqual(CB.verify_bridge(self.arch, discover=True), self.inputs["architecture"])

    def test_closure_file_set_matches_explicit_subject_list(self):
        listed = json.loads((UNIT / "subject-files.json").read_bytes())["files"]
        present = sorted(path.relative_to(UNIT).as_posix() for path in UNIT.rglob("*") if path.is_file())
        self.assertEqual(present, sorted([row["path"] for row in listed] + ["subject-files.json"]))
        for row in listed:
            raw = (UNIT / row["path"]).read_bytes()
            self.assertEqual((hashlib.sha256(raw).hexdigest(), len(raw)), (row["sha256"], row["bytes"]), row["path"])

    def test_live_lock_refuses_control_source_and_synthetic_stage_selects_it(self):
        files, control = CB.check_generation_join(self.V, self.declared())
        self.refuses(CB.REFUSAL, lambda: self.V.verify(self.arch, self.lock, CB.write_tree(Path(self.tmp.name) / "impl", files)))
        binding = self.stage()
        result = CB.verify_staged(self.arch, binding, allow_synthetic=True)
        self.assertEqual(result["selectedInputs"], [SCHEMA])
        self.assertEqual((result["contractSuccessors"], result["generationSourcesVerified"]), (2, 29))
        direct = self.V.verify(self.arch, self.staged_lock(binding))
        self.assertEqual(direct["contractSuccessors"][-1]["selected"], f"{CB.STAGED}/successor.json")
        self.assertEqual(direct["contractSuccessors"][-1]["passageOverrides"], [])
        self.assertEqual(control, "schemas/sources/control.v3.schema.json")

    def test_synthetic_fixtures_cannot_stand_as_acceptance(self):
        self.refuses("synthetic review fixture", lambda: CB.verify_staged(self.arch, self.stage()))
        unmarked = self.stage(review=lambda doc: doc.pop(CB.SYNTHETIC_MARKER), assent=lambda doc: doc.pop(CB.SYNTHETIC_MARKER))
        self.refuses("synthetic review fixture", lambda: CB.verify_staged(self.arch, unmarked))
        other = self.stage()
        other["record"] = {**other["record"], "bytes": 1}
        self.refuses("staged record is not this successor", lambda: CB.verify_staged(self.arch, other, allow_synthetic=True))

    def test_v4_contract_rules_still_refuse_rejected_or_mismatched_fixtures(self):
        cases = [
            ("independent contract acceptance missing", {"review": lambda doc: doc.update(verdict="ACCEPT-UNIT")}),
            ("independent contract acceptance missing", {"review": lambda doc: doc.update(requiredFindings=["F"])}),
            ("contract review names a different manifest", {"review": lambda doc: doc.update(subjectManifestSha256="0" * 64)}),
            ("root contract assent missing", {"assent": lambda doc: doc.update(status="ACCEPTED-UNIT")}),
            ("root contract assent missing", {"assent": lambda doc: doc.update(rootSubstantiveAssent=False)}),
            ("contract root successor names a different subject",
             {"assent": lambda doc: doc.update(acceptedSuccessor={**doc["acceptedSuccessor"], "bytes": 1})}),
        ]
        for pattern, change in cases:
            with self.subTest(pattern):
                binding = self.stage(**change)
                self.refuses(pattern, lambda: self.V.verify(self.arch, self.staged_lock(binding)))

    def test_schema_byte_drift_refuses(self):
        binding = self.stage()
        path = self.arch / SCHEMA["path"]
        path.write_bytes(path.read_bytes() + b" ")
        self.refuses("design digest mismatch", lambda: CB.verify_bridge(self.arch))
        self.refuses("design digest mismatch", lambda: CB.verify_staged(self.arch, binding, allow_synthetic=True))
        self.refuses("design digest mismatch", lambda: self.V.verify(self.arch, self.staged_lock(binding)))

    def test_rebound_schema_drift_passes_verifier_alone_but_bridge_refuses(self):
        raw = (self.arch / SCHEMA["path"]).read_bytes() + b"\n"
        drift = CB.pin_of(SCHEMA["path"], raw)

        def repin(record):
            record["candidates"] = [drift]
            for row in record["evidence"]["frozenMembers"]:
                if row["path"] == SCHEMA["path"]:
                    row.update(drift)

        unit = self.unit(record=repin)
        self.put(SCHEMA["path"], raw)
        binding = self.stage(unit)
        # The product verifier trusts the pinned review; a synthetic one shows why the joins below matter.
        self.assertEqual(self.V.verify(self.arch, self.staged_lock(binding))["contractSuccessors"][-1]["inputs"], [drift])
        self.refuses("design digest mismatch", lambda: CB.verify_bridge(self.arch, unit))
        self.refuses("frozen member pins differ from freeze", lambda: CB.verify_bridge(self.pristine, unit))
        only_candidate = self.unit(record=lambda record: record.update(candidates=[drift]))
        self.refuses("exactly the existing control schema", lambda: CB.verify_bridge(self.pristine, only_candidate))

    def test_selector_drift_refuses(self):
        pointer = lambda value: lambda record: record["selection"]["parentSelector"].update(jsonPointer=value)
        for value in ("/units/protocol", "/units/control/review", "/units/controls", "/units/control/"):
            with self.subTest(value):
                self.refuses("parent selector differs", lambda: CB.verify_bridge(self.pristine, self.unit(record=pointer(value))))
        evidence = lambda record: record["selection"]["parentSchemaEvidence"].update(jsonPointer="/evidenceTargets/C.BODIES/sources/0")
        self.refuses("parent schema evidence selector differs", lambda: CB.verify_bridge(self.pristine, self.unit(record=evidence)))

    def test_application_and_parent_drift_refuses(self):
        document = json.loads((self.arch / CB.APPLICATION["path"]).read_bytes())
        document["units"]["control"]["review"]["pin"] = "0" * 64
        changed = self.put(CB.APPLICATION["path"], dump(document))
        self.refuses("design digest mismatch", lambda: CB.verify_bridge(self.arch))

        def reparent(record):
            record["parents"] = [changed]
            for key in ("parentSelector", "parentSchemaEvidence"):
                record["selection"][key]["parent"] = changed

        def redeclare(inputs):
            for row in inputs["architecture"]:
                if row["path"] == changed["path"]:
                    row.update(changed)

        unit = self.unit(record=reparent, inputs=redeclare)
        self.refuses("parent must be exactly the accepted architecture application", lambda: CB.verify_bridge(self.arch, unit))
        other = next(row for row in self.lock["inputs"] if row["path"].endswith("14-repository-and-module-layout.md"))
        self.refuses("parent must be exactly", lambda: CB.verify_bridge(self.pristine, self.unit(record=lambda r: r.update(parents=[other]))))
        shutil.copyfile(self.pristine / CB.APPLICATION["path"], self.arch / CB.APPLICATION["path"])
        forged = self.unit(record=lambda record: record.update(parents=[{**CB.APPLICATION, "sha256": "0" * 64}]))
        binding = self.stage(forged)
        self.refuses("contract parent is not an accepted base", lambda: self.V.verify(self.arch, self.staged_lock(binding)))

    def test_evidence_and_member_pin_drift_refuses(self):
        cases = [
            ("successor independentReview differs", lambda r: r["evidence"]["independentReview"].update(sha256="0" * 64)),
            ("successor freeze size or declared pin differs", lambda r: r["evidence"]["freeze"].update(bytes=1)),
            ("frozen member pins differ from freeze", lambda r: r["evidence"]["frozenMembers"].pop(0)),
            ("frozen member pins differ from freeze", lambda r: r["evidence"]["frozenMembers"][0].update(sha256="f" * 64)),
            ("review verdict or findings differ", lambda r: r["evidence"].update(reviewVerdict="ACCEPT")),
            ("review verdict or findings differ", lambda r: r["evidence"].update(reviewMustFindings=["M"])),
            ("base approval differs from live lock", lambda r: r["selection"]["baseApproval"].update(parentOverriddenByApplication=True)),
            ("control schema ID differs", lambda r: r["selection"].update(schemaId="urn:opensip:design:control-schema:4")),
        ]
        for pattern, change in cases:
            with self.subTest(pattern):
                self.refuses(pattern, lambda: CB.verify_bridge(self.pristine, self.unit(record=change)))

    def test_review_and_freeze_document_drift_refuses(self):
        record = json.loads((UNIT / "successor.json").read_bytes())
        review = json.loads(self.V.pinned_bytes(self.arch, record["evidence"]["independentReview"]))
        freeze = json.loads(self.V.pinned_bytes(self.arch, record["evidence"]["freeze"]))
        digest = record["evidence"]["freeze"]["sha256"]
        self.assertEqual(len(CB.check_review_freeze(review, freeze, digest)), 8)
        name = SCHEMA["path"].rsplit("/", 1)[1]

        def everywhere(review_doc, freeze_doc):
            for files in (freeze_doc["files"], review_doc["subject"]["files"], review_doc["postReviewHashes"]):
                files[name] = "0" * 64

        cases = [
            ("not the control independent review5", lambda r, f: r.update(artifact="control-completion-review")),
            ("verdict differs", lambda r, f: r.update(verdict="OBJECTION")),
            ("findings remain", lambda r, f: r.update(mustFindings=["M1"])),
            ("findings remain", lambda r, f: r.update(requiredFindings=["R1"])),
            ("subject changed", lambda r, f: r.update(subjectUnchanged=False)),
            ("names a different freeze", lambda r, f: r["subject"].update(freezeSha256="0" * 64)),
            ("post-review hashes differ", lambda r, f: r["postReviewHashes"].update({name: "0" * 64})),
            ("replay does not join", lambda r, f: r["replay"].update(passed=483)),
            ("replay does not join", lambda r, f: r["replay"].update(reportSha256="0" * 64)),
            ("exactly eight members", lambda r, f: f["files"].pop("control-completion.contract.v5.md")),
            ("exactly eight members", lambda r, f: f["files"].update({"extra.json": "0" * 64})),
            ("does not pin the exact schema", everywhere),
        ]
        for pattern, change in cases:
            with self.subTest(pattern):
                review_doc, freeze_doc = copy.deepcopy(review), copy.deepcopy(freeze)
                change(review_doc, freeze_doc)
                self.refuses(pattern, lambda: CB.check_review_freeze(review_doc, freeze_doc, digest))
        self.refuses("names a different freeze", lambda: CB.check_review_freeze(review, freeze, "0" * 64))

    def test_scope_drift_refuses(self):
        contract = next(row for row in json.loads((UNIT / "successor.json").read_bytes())["evidence"]["frozenMembers"]
                        if row["path"].endswith("contract.v5.md"))
        override = {"parent": CB.APPLICATION, "selector": {"jsonPointer": "/units/control/boundary"}, "before": "a", "after": "b"}
        cases = [
            ("exactly the existing control schema", self.unit(record=lambda r: r["candidates"].append(contract))),
            ("must not override passages", self.unit(record=lambda r: r.update(passageOverrides=[override]))),
            ("disclaim product qualification", self.unit(record=lambda r: r.update(acceptanceDoesNotQualifyProduct=False))),
            ("selection subject must contain exactly", self.unit(subject=lambda s: s["files"].insert(0, contract))),
        ]
        for pattern, unit in cases:
            with self.subTest(pattern):
                self.refuses(pattern, lambda: CB.verify_bridge(self.pristine, unit))

    def test_already_selected_or_duplicated_schema_refuses(self):
        declared, record = self.declared(), json.loads((UNIT / "successor.json").read_bytes())
        members = record["evidence"]["frozenMembers"]
        CB.check_candidate_scope(self.V, declared, record, {}, members)
        self.refuses("already selected by accepted design",
                     lambda: CB.check_candidate_scope(self.V, declared, record, {SCHEMA["path"]: SCHEMA}, members))
        copy_row = {**SCHEMA, "path": "docs/implementation/m1/control-copy.schema.json"}
        self.refuses("under another path",
                     lambda: CB.check_candidate_scope(self.V, declared, record, {copy_row["path"]: copy_row}, members))
        binding = self.stage()
        effective = {**self.effective(), SCHEMA["path"]: SCHEMA}
        self.refuses("contract candidate reuses an accepted path",
                     lambda: self.V.successor_chain(self.arch, self.staged_lock(binding), effective))

    def test_generation_join_drift_refuses(self):
        path = f"{CB.TRIAL_SUBJECT}/schemas/source-map.json"
        raw = (self.arch / path).read_bytes() + b" "
        self.put(path, raw)
        self.refuses("design digest mismatch", lambda: CB.verify_bridge(self.arch))

        def redeclare(inputs):
            for row in inputs["architecture"]:
                if row["path"] == path:
                    row.update(CB.pin_of(path, raw))

        self.refuses("trial copy differs from reviewed subject", lambda: CB.verify_bridge(self.arch, self.unit(inputs=redeclare)))

    def test_snapshot_and_declared_input_drift_refuses(self):
        self.refuses("snapshot verifier differs", lambda: CB.verify_bridge(self.pristine, self.unit(snapshot_suffix=b"\n")))
        drop = lambda target: lambda inputs: inputs.update(architecture=[row for row in inputs["architecture"] if row["path"] != target])
        self.refuses(f"undeclared architecture read: {CB.ROUTE}", lambda: CB.verify_bridge(self.pristine, self.unit(inputs=drop(CB.ROUTE))))
        self.refuses("undeclared=\\['docs/v2/contracts/product-v1/README.md'\\]",
                     lambda: CB.verify_bridge(self.pristine, self.unit(inputs=drop("docs/v2/contracts/product-v1/README.md"))))
        extra = {"path": "docs/coop/completion/control-completion.independent-review.v5.md", "sha256": "0" * 64, "bytes": 0}
        add = lambda inputs: inputs.update(architecture=sorted([*inputs["architecture"], extra], key=lambda row: row["path"]))
        self.refuses("unused=\\['docs/coop/completion/control-completion.independent-review.v5.md'\\]",
                     lambda: CB.verify_bridge(self.pristine, self.unit(inputs=add)))
        snapshots = lambda inputs: inputs["snapshots"][0].update(sha256="0" * 64)
        self.refuses("declared snapshots differ", lambda: CB.verify_bridge(self.pristine, self.unit(inputs=snapshots)))


if __name__ == "__main__":
    unittest.main()
