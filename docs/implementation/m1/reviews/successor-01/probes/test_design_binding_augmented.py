"""Behavioral refusal tests for the developer design-binding verifier."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2] / "tools/verify_design.py"
SPEC = importlib.util.spec_from_file_location("verify_design", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DesignBindingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        contract = self.write("contract.json", {"current": True})
        source = self.write("source.json", {"files": [contract]})
        application = self.write("application.json", {"files": [], "designSubject": source})
        review = self.write("review.json", {"verdict": "ACCEPT", "subjectManifestSha256": application["sha256"], "newMustIssues": [], "newShouldIssues": []})
        activation = self.write("activation.json", {"applicationManifest": application, "independentApplicationReview": review})
        assent = self.write("assent.json", {"authority": {"rootApplicationAssent": True}, "subjectManifestSha256": application["sha256"], "review": review})
        completion = self.write("completion.json", {"designApprovedForImplementation": True, "passed": True, "applicationManifest": application, "activation": activation, "actualClaudeApplicationReview": review, "codexApplicationAssent": assent})
        self.lock = {"schemaVersion": 1, "architectureRepository": "fixture", "approvals": {"sourceManifest": source, "applicationManifest": application, "activation": activation, "applicationReview": review, "rootAssent": assent, "completion": completion}, "inputs": [contract]}

    def write(self, path, value):
        raw = (json.dumps(value, sort_keys=True) + "\n").encode()
        (self.root / path).write_bytes(raw)
        return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

    def test_valid_approval_and_selected_bytes(self):
        result = MODULE.verify(self.root, self.lock)
        self.assertTrue(result["passed"])
        self.assertEqual(result["inputsVerified"], 1)

    def test_changed_document_refuses_even_with_local_repin(self):
        new = self.write("contract.json", {"current": False})
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, self.lock)
        self.lock["inputs"] = [new]
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, self.lock)

    def test_unreviewed_document_and_duplicate_input_refuse(self):
        self.lock["inputs"] += [self.write("unreviewed.json", {})]
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, self.lock)
        self.lock["inputs"] = [self.lock["inputs"][0]] * 2
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, self.lock)

    def test_unknown_lock_fields_and_boolean_version_refuse(self):
        for alteration in ({"unexpected": True}, {"schemaVersion": True}, {"schemaVersion": 2}):
            changed = copy.deepcopy(self.lock)
            changed.update(alteration)
            with self.assertRaises(MODULE.DesignError):
                MODULE.verify(self.root, changed)

    def test_approval_bytes_and_cross_subject_links_refuse(self):
        changed = copy.deepcopy(self.lock)
        changed["approvals"]["activation"] = self.write("activation.json", {"applicationManifest": {"path": "application.json", "sha256": "0" * 64}, "independentApplicationReview": self.lock["approvals"]["applicationReview"]})
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, self.lock)
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, changed)

    def test_duplicate_json_keys_refuse_before_binding(self):
        for raw in [b'{"x":1,"x":2}', b'{"x":1,"\\u0078":2}', b'{"outer":{"x":1,"x":2}}']:
            with self.assertRaises(MODULE.DesignError):
                MODULE.decode(raw)

    def test_malformed_approval_pins_refuse(self):
        for alteration in ({"note": "ignored"}, {"bytes": True}, {"bytes": -1}, {"sha256": "A" * 64}):
            changed = copy.deepcopy(self.lock)
            changed["approvals"]["completion"].update(alteration)
            with self.assertRaises(MODULE.DesignError):
                MODULE.verify(self.root, changed)
        del self.lock["approvals"]["completion"]["bytes"]
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, self.lock)

    def test_non_object_approval_and_remaining_findings_refuse(self):
        completion = json.loads((self.root / "completion.json").read_bytes())
        for document in ([], {**completion, "remainingRequiredDesignFindings": ["open"]}):
            self.lock["approvals"]["completion"] = self.write("completion.json", document)
            with self.assertRaises(MODULE.DesignError):
                MODULE.verify(self.root, self.lock)

    def test_escaping_paths_and_symlinks_refuse(self):
        for path in ["../contract.json", "/contract.json", "./contract.json", "a//contract.json", "a/../contract.json", "a\\contract.json"]:
            with self.assertRaises(MODULE.DesignError):
                MODULE.relative_file(self.root, path)
        (self.root / "link.json").symlink_to(self.root / "contract.json")
        with self.assertRaises(MODULE.DesignError):
            MODULE.relative_file(self.root, "link.json")


class InventorySuccessorTests(unittest.TestCase):
    write = DesignBindingTests.write

    def setUp(self):
        DesignBindingTests.setUp(self)
        self.parent = {"schemaVersion": 1, "standing": "base", "packages": [{"id": "tooling", "dependencies": []}], "pendingDecisions": [], "files": [{"path": "a.py", "package": "tooling", "role": "validator"}]}
        parent = self.write("contract.json", self.parent)
        source = self.write("source.json", {"files": [parent]})
        # Rebuild the base approval chain to select the inventory fixture.
        app = self.write("application.json", {"files": [], "designSubject": source})
        review = self.write("review.json", {"verdict": "ACCEPT", "subjectManifestSha256": app["sha256"], "newMustIssues": [], "newShouldIssues": []})
        activation = self.write("activation.json", {"applicationManifest": app, "independentApplicationReview": review})
        assent = self.write("assent.json", {"authority": {"rootApplicationAssent": True}, "subjectManifestSha256": app["sha256"], "review": review})
        completion = self.write("completion.json", {"designApprovedForImplementation": True, "passed": True, "applicationManifest": app, "activation": activation, "actualClaudeApplicationReview": review, "codexApplicationAssent": assent})
        self.lock.update(schemaVersion=2, inputs=[parent], approvals=dict(sourceManifest=source, applicationManifest=app, activation=activation, applicationReview=review, rootAssent=assent, completion=completion))
        self.candidate = copy.deepcopy(self.parent)
        self.candidate["standing"] = "historical pending field"
        self.candidate["files"].append({"path": "b.py", "package": "tooling", "role": "test"})
        self.bind()

    def bind(self):
        parent = self.lock["inputs"][0]
        candidate = self.write("candidate.json", self.candidate)
        record = self.write("successor.json", {"parent": parent, "candidate": candidate, "parentArtifactBytesUnchanged": True, "inheritedRowsEqualByValue": True})
        review = self.write("successor-review.json", {"verdict": "ACCEPT-UNIT", "requiredFindings": [], "subjectManifestSha256": "a" * 64, "inventoryCandidateAssessment": {**candidate, "verdict": "ACCEPT", "requiredFindings": [], "parent": parent, "successorRecord": record}})
        assent = self.write("successor-assent.json", {"status": "ACCEPTED-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [], "actualClaudeReview": review, "acceptedInventory": candidate, "subjectManifest": {"sha256": "a" * 64}})
        self.lock["inventorySuccessor"] = dict(parent=parent, candidate=candidate, record=record, review=review, assent=assent)

    def change(self, key, mutate):
        pin = self.lock["inventorySuccessor"][key]
        value = json.loads((self.root / pin["path"]).read_bytes())
        mutate(value)
        self.lock["inventorySuccessor"][key] = self.write(pin["path"], value)

    def refuse(self):
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, self.lock)

    def test_accepted_addition_selects_successor_and_preserves_base(self):
        result = MODULE.verify(self.root, self.lock)
        self.assertEqual(result["inventorySuccessor"]["selected"], "candidate.json")
        self.assertEqual(result["inventorySuccessor"]["addedFiles"], 1)
        self.assertEqual(result["inputsVerified"], 1)
        self.assertFalse(result["productQualification"])
        self.assertEqual(json.loads((self.root / "contract.json").read_bytes()), self.parent)

    def test_candidate_repin_without_review_refuses(self):
        self.change("candidate", lambda d: d["files"].append({"path": "c.py"}))
        self.refuse()

    def test_closed_binding_and_required_pins(self):
        original = copy.deepcopy(self.lock)
        for key in ("parent", "candidate", "record", "review", "assent"):
            with self.subTest(key=key):
                self.lock = copy.deepcopy(original)
                del self.lock["inventorySuccessor"][key]
                self.refuse()
        self.lock = copy.deepcopy(original)
        self.lock["inventorySuccessor"]["extra"] = True
        self.refuse()

    def test_different_parent_record_candidate_or_subject_refuses(self):
        cases = [
            ("record", lambda d: d["parent"].update(sha256="0" * 64)),
            ("record", lambda d: d["candidate"].update(bytes=0)),
            ("record", lambda d: d.update(inheritedRowsEqualByValue=False)),
            ("review", lambda d: d["inventoryCandidateAssessment"].update(sha256="0" * 64)),
            ("review", lambda d: d["inventoryCandidateAssessment"]["successorRecord"].update(sha256="0" * 64)),
            ("assent", lambda d: d["actualClaudeReview"].update(sha256="0" * 64)),
            ("assent", lambda d: d["acceptedInventory"].update(sha256="0" * 64)),
            ("assent", lambda d: d["subjectManifest"].update(sha256="0" * 64)),
        ]
        for key, mutate in cases:
            with self.subTest(key=key):
                self.bind()
                self.change(key, mutate)
                self.refuse()

    def test_review_rejection_and_findings_refuse(self):
        for key, mutate in [
            ("review", lambda d: d.update(verdict="CHANGES-REQUIRED")),
            ("review", lambda d: d.update(requiredFindings=["open"])),
            ("review", lambda d: d["inventoryCandidateAssessment"].update(requiredFindings=["open"])),
            ("assent", lambda d: d.update(rootSubstantiveAssent=False)),
            ("assent", lambda d: d.update(requiredUnitFindings=["open"])),
        ]:
            with self.subTest(key=key):
                self.bind()
                self.change(key, mutate)
                self.refuse()

    def test_fully_rebound_policy_changes_are_outside_additive_profile(self):
        original = copy.deepcopy(self.candidate)
        changes = [
            lambda d: d["packages"][0]["dependencies"].append("host"),
            lambda d: d["files"][0].update(package="host"),
            lambda d: d["files"].pop(0),
            lambda d: d["files"].append(d["files"][0]),
            lambda d: d["files"].reverse(),
            lambda d: d["pendingDecisions"].append("new"),
            lambda d: d.update(schemaVersion=2),
            lambda d: d.update(unknown=True),
        ]
        for mutate in changes:
            self.candidate = copy.deepcopy(original)
            mutate(self.candidate)
            self.bind()
            self.refuse()

    def test_parent_must_be_selected_base_input(self):
        other = self.write("other.json", self.parent)
        self.lock["inventorySuccessor"]["parent"] = other
        self.refuse()

    def test_malformed_nested_records_have_controlled_diagnostics(self):
        for key, field in [("record", "parent"), ("review", "inventoryCandidateAssessment"), ("assent", "actualClaudeReview"), ("assent", "subjectManifest")]:
            for value in (None, [], "text", 1):
                with self.subTest(key=key, field=field, value=value):
                    self.bind()
                    self.change(key, lambda d: d.update({field: value}))
                    self.refuse()


class ReviewerIsolationProbe(InventorySuccessorTests):
    """Reviewer probe: rebind downstream joins so exactly one guard can refuse."""

    def rebound(self, key, mutate):
        self.change(key, mutate)
        if key == "record":
            record = self.lock["inventorySuccessor"]["record"]
            self.change("review", lambda d: d["inventoryCandidateAssessment"]["successorRecord"].update(sha256=record["sha256"]))
            key = "review"
        if key == "review":
            review = self.lock["inventorySuccessor"]["review"]
            self.change("assent", lambda d: d["actualClaudeReview"].update(sha256=review["sha256"]))

    def refuse_with(self, pattern):
        with self.assertRaisesRegex(MODULE.DesignError, pattern):
            MODULE.verify(self.root, self.lock)

    def test_isolated_join_and_decision_guards(self):
        for key, mutate, pattern in [
            ("record", lambda d: d["candidate"].update(bytes=0), "successor candidate"),
            ("record", lambda d: d.update(inheritedRowsEqualByValue=False), "preserve parent"),
            ("review", lambda d: d.update(verdict="CHANGES-REQUIRED"), "independent inventory"),
            ("review", lambda d: d.update(requiredFindings=["open"]), "independent inventory"),
            ("review", lambda d: d["inventoryCandidateAssessment"].update(verdict="CHANGES-REQUIRED"), "independent inventory"),
            ("review", lambda d: d["inventoryCandidateAssessment"].update(requiredFindings=["open"]), "independent inventory"),
            ("review", lambda d: d["inventoryCandidateAssessment"].update(bytes=0), "review candidate"),
            ("review", lambda d: d["inventoryCandidateAssessment"]["parent"].update(sha256="0" * 64), "review parent"),
            ("review", lambda d: d["inventoryCandidateAssessment"]["successorRecord"].update(sha256="0" * 64), "review successor record"),
            ("assent", lambda d: d.update(status="ACCEPTED"), "root inventory assent"),
        ]:
            with self.subTest(pattern=pattern):
                self.bind()
                self.rebound(key, mutate)
                self.refuse_with(pattern)

    def test_isolated_zero_addition(self):
        self.candidate = copy.deepcopy(self.parent)
        self.candidate["standing"] = "changed only"
        self.bind()
        self.refuse_with("additions")

    def test_isolated_parent_selection(self):
        other = self.write("other.json", self.parent)
        self.lock["inputs"] = [other]
        self.bind()
        self.lock["inputs"] = [self.lock["approvals"]["sourceManifest"] and json.loads((self.root / "source.json").read_bytes())["files"][0]]
        self.refuse_with("selected base input")

    def test_isolated_extra_binding_with_valid_pin(self):
        self.lock["inventorySuccessor"]["extra"] = self.lock["inventorySuccessor"]["record"]
        self.refuse_with("five closed")


if __name__ == "__main__":
    unittest.main()
