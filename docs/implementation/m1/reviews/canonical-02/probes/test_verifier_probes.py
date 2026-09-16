"""Reviewer probes for tools/verify_design.py beyond the snapshot's own tests.

Loads the frozen verifier from digest-checked bytes, so no bytecode is written into
the snapshot. Temporary fixtures live under results/work in the review directory.
Tests named test_observed_* document observed behaviour; they are evidence for
advisories, not requirements. Review-02 inverts the three review-01 permissive
observations and the non-object observation, because successor03 claims to refuse them.
"""
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WORK = HERE.parent / "results" / "work"
SNAPSHOT = Path("/tmp/opensip-implementation/m1-canonical-subject-03")
VERIFIER = SNAPSHOT / "tools/verify_design.py"
VERIFIER_SHA256 = "c6b272a0dd440cf7533c736cbcd9616dac3140fdfcc9e5ceee2d4d0c749ef73b"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")

_RAW = VERIFIER.read_bytes()
if hashlib.sha256(_RAW).hexdigest() != VERIFIER_SHA256:
    raise SystemExit("snapshot verifier digest mismatch")
MODULE = importlib.util.module_from_spec(importlib.util.spec_from_loader("verify_design_probe", loader=None))
exec(compile(_RAW, str(VERIFIER), "exec"), MODULE.__dict__)


class Fixture(unittest.TestCase):
    def setUp(self):
        WORK.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=WORK)
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "arch"
        self.root.mkdir()
        self.contract = self.write("docs/contract.json", {"current": True})

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        data = (json.dumps(value, sort_keys=True) + "\n").encode()
        target.write_bytes(data)
        return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}

    def chain(self, inputs=None, source_files=None, application_files=(), review=None, assent=None, completion=None):
        inputs = [self.contract] if inputs is None else inputs
        source_files = [self.contract] if source_files is None else source_files
        source = self.write("source.json", {"files": list(source_files)})
        application = self.write("application.json", {"files": list(application_files), "designSubject": source})
        review_doc = {"verdict": "ACCEPT", "subjectManifestSha256": application["sha256"],
                      "newMustIssues": [], "newShouldIssues": []}
        review_doc.update(review or {})
        review_row = self.write("review.json", review_doc)
        activation = self.write("activation.json", {"applicationManifest": application,
                                                    "independentApplicationReview": review_row})
        assent_doc = {"authority": {"rootApplicationAssent": True},
                      "subjectManifestSha256": application["sha256"], "review": review_row}
        assent_doc.update(assent or {})
        assent_row = self.write("assent.json", assent_doc)
        completion_doc = {"designApprovedForImplementation": True, "passed": True,
                          "applicationManifest": application, "activation": activation,
                          "actualClaudeApplicationReview": review_row, "codexApplicationAssent": assent_row}
        completion_doc.update(completion or {})
        completion_row = self.write("completion.json", completion_doc)
        return {"schemaVersion": 1, "architectureRepository": "probe",
                "approvals": {"sourceManifest": source, "applicationManifest": application,
                              "activation": activation, "applicationReview": review_row,
                              "rootAssent": assent_row, "completion": completion_row},
                "inputs": list(inputs)}

    def assertRefuses(self, lock):
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, lock)


class ApprovalChainProbes(Fixture):
    def test_baseline_chain_passes(self):
        self.assertEqual(MODULE.verify(self.root, self.chain())["inputsVerified"], 1)

    def test_review_verdict_must_be_accept(self):
        self.assertRefuses(self.chain(review={"verdict": "CHANGES-REQUIRED"}))

    def test_review_must_issue_refuses(self):
        self.assertRefuses(self.chain(review={"newMustIssues": ["open"]}))

    def test_review_should_issue_refuses(self):
        self.assertRefuses(self.chain(review={"newShouldIssues": ["open"]}))

    def test_review_missing_issue_list_refuses(self):
        self.assertRefuses(self.chain(review={"newShouldIssues": None}))

    def test_review_of_other_subject_refuses(self):
        self.assertRefuses(self.chain(review={"subjectManifestSha256": "0" * 64}))

    def test_assent_must_be_boolean_true(self):
        self.assertRefuses(self.chain(assent={"authority": {"rootApplicationAssent": "true"}}))

    def test_assent_of_other_subject_refuses(self):
        self.assertRefuses(self.chain(assent={"subjectManifestSha256": "0" * 64}))

    def test_assent_of_other_review_refuses(self):
        self.assertRefuses(self.chain(assent={"review": {"path": "review.json", "sha256": "0" * 64}}))

    def test_completion_must_approve(self):
        self.assertRefuses(self.chain(completion={"designApprovedForImplementation": False}))

    def test_completion_passed_must_be_boolean_true(self):
        self.assertRefuses(self.chain(completion={"passed": "true"}))

    def test_completion_naming_other_assent_refuses(self):
        self.assertRefuses(self.chain(completion={"codexApplicationAssent": {"path": "assent.json", "sha256": "0" * 64}}))

    def test_completion_naming_other_activation_refuses(self):
        self.assertRefuses(self.chain(completion={"activation": {"path": "activation.json", "sha256": "0" * 64}}))

    def test_application_naming_other_source_refuses(self):
        lock = self.chain()
        lock["approvals"]["sourceManifest"] = self.write("source-other.json", {"files": [self.contract]})
        self.assertRefuses(lock)

    def test_missing_or_extra_approval_refuses(self):
        lock = self.chain()
        missing = copy.deepcopy(lock)
        del missing["approvals"]["completion"]
        self.assertRefuses(missing)
        extra = copy.deepcopy(lock)
        extra["approvals"]["other"] = lock["approvals"]["completion"]
        self.assertRefuses(extra)

    def test_float_schema_version_refuses(self):
        lock = self.chain()
        lock["schemaVersion"] = 1.0
        self.assertRefuses(lock)


class InputSelectionProbes(Fixture):
    def test_application_overlay_supersedes_source_row(self):
        old = self.contract
        new = self.write("docs/contract.json", {"current": "v2"})
        self.assertRefuses(self.chain(inputs=[old], source_files=[old], application_files=[new]))
        lock = self.chain(inputs=[new], source_files=[old], application_files=[new])
        self.assertEqual(MODULE.verify(self.root, lock)["inputsVerified"], 1)

    def test_unsorted_inputs_refuse(self):
        a = self.write("docs/a.json", {"a": 1})
        b = self.write("docs/b.json", {"b": 1})
        self.assertRefuses(self.chain(inputs=[b, a], source_files=[a, b]))
        self.assertEqual(MODULE.verify(self.root, self.chain(inputs=[a, b], source_files=[a, b]))["inputsVerified"], 2)

    def test_empty_inputs_refuse(self):
        self.assertRefuses(self.chain(inputs=[]))

    def test_input_extra_field_refuses(self):
        self.assertRefuses(self.chain(inputs=[dict(self.contract, note="x")]))

    def test_selected_row_with_wrong_length_refuses(self):
        row = dict(self.contract, bytes=self.contract["bytes"] + 1)
        self.assertRefuses(self.chain(inputs=[row], source_files=[row]))

    def test_duplicate_source_manifest_path_refuses(self):
        self.assertRefuses(self.chain(source_files=[self.contract, self.contract]))


class PathProbes(Fixture):
    def test_trailing_separator_empty_and_dot_segments_refuse(self):
        for path in ["docs/", "docs/./contract.json", "docs/contract.json/", "", ".", ".."]:
            with self.assertRaises(MODULE.DesignError, msg=repr(path)):
                MODULE.relative_file(self.root, path)

    def test_nul_byte_refuses(self):
        with self.assertRaises(ValueError):
            MODULE.relative_file(self.root, "docs/con\x00tract.json")

    def test_symlinked_parent_leaving_root_refuses(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "contract.json").write_bytes((self.root / "docs/contract.json").read_bytes())
        (self.root / "escape").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(MODULE.DesignError):
            MODULE.relative_file(self.root, "escape/contract.json")

    def test_observed_symlinked_parent_inside_root_is_allowed(self):
        (self.root / "alias").symlink_to(self.root / "docs", target_is_directory=True)
        self.assertTrue(MODULE.relative_file(self.root, "alias/contract.json").is_file())


class SuccessorStrictnessProbes(Fixture):
    def test_successor_approval_row_without_bytes_refuses(self):
        lock = self.chain()
        del lock["approvals"]["completion"]["bytes"]
        self.assertRefuses(lock)

    def test_successor_approval_row_unknown_field_refuses(self):
        lock = self.chain()
        lock["approvals"]["completion"]["note"] = "ignored"
        self.assertRefuses(lock)

    def test_successor_completion_remaining_findings_refuse(self):
        lock = self.chain(completion={"remainingRequiredDesignFindings": ["open"]})
        self.assertRefuses(lock)

    def test_successor_non_object_review_refuses_cleanly(self):
        lock = self.chain()
        review = self.write("review.json", [])
        activation = self.write("activation.json", {"applicationManifest": lock["approvals"]["applicationManifest"],
                                                    "independentApplicationReview": review})
        lock["approvals"]["applicationReview"] = review
        lock["approvals"]["activation"] = activation
        self.assertRefuses(lock)


class SuccessorPinProbes(Fixture):
    def test_pin_value_types_refuse(self):
        for alteration in ({"sha256": "A" * 64}, {"sha256": "0" * 63}, {"sha256": 0}, {"bytes": 1.0},
                           {"bytes": True}, {"bytes": -1}, {"bytes": "12"}, {"path": ["docs"]}):
            lock = self.chain()
            lock["approvals"]["activation"].update(alteration)
            with self.assertRaises(MODULE.DesignError, msg=repr(alteration)):
                MODULE.verify(self.root, lock)

    def test_non_object_pin_lock_and_approvals_refuse(self):
        lock = self.chain()
        lock["approvals"]["applicationReview"] = [lock["approvals"]["applicationReview"]]
        self.assertRefuses(lock)
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(self.root, [])
        lock = self.chain()
        lock["approvals"] = []
        self.assertRefuses(lock)

    def test_remaining_findings_non_empty_list_values_refuse(self):
        for value in (None, {}, "", 0, False, ["x"]):
            with self.subTest(value=value):
                self.assertRefuses(self.chain(completion={"remainingRequiredDesignFindings": value}))

    def test_observed_absent_remaining_findings_key_passes(self):
        self.assertTrue(MODULE.verify(self.root, self.chain())["passed"])

    def test_observed_nested_non_object_reference_escapes_main_catch_set(self):
        import subprocess
        lock = self.chain()
        lock["approvals"]["activation"] = self.write("activation.json", {
            "applicationManifest": "application.json",
            "independentApplicationReview": lock["approvals"]["applicationReview"]})
        with self.assertRaises(AttributeError):
            MODULE.verify(self.root, lock)
        lock_path = self.base / "lock.json"
        lock_path.write_text(json.dumps(lock))
        completed = subprocess.run([sys.executable, "-I", "-B", str(VERIFIER), "--architecture", str(self.root),
                                    "--lock", str(lock_path)], capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("AttributeError", completed.stderr)
        self.assertNotIn("Design verification failed", completed.stderr)


class RealArchitectureProbes(unittest.TestCase):
    def setUp(self):
        self.lock = MODULE.decode((SNAPSHOT / "design-lock.json").read_bytes())

    def test_pinned_lock_verifies_46_inputs(self):
        self.assertEqual(MODULE.verify(ARCH.resolve(), self.lock), {
            "passed": True, "inputsVerified": 46,
            "applicationManifestSha256": "dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7",
            "productQualification": False})

    def test_governing_sources_for_this_unit_are_pinned(self):
        paths = {row["path"] for row in self.lock["inputs"]}
        for path in ["docs/v2/contracts/product-v1/identity-and-evidence.md",
                     "docs/v2/contracts/product-v1/admission-and-qualification.md",
                     "docs/coop/design-corrections/foundation/canonical.py",
                     "docs/coop/design-corrections/foundation/check-foundation.py"]:
            self.assertIn(path, paths)

    def test_altered_input_digest_refuses(self):
        lock = copy.deepcopy(self.lock)
        lock["inputs"][0]["sha256"] = "0" * 64
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(ARCH.resolve(), lock)

    def test_altered_source_manifest_pin_refuses(self):
        lock = copy.deepcopy(self.lock)
        lock["approvals"]["sourceManifest"]["sha256"] = "0" * 64
        with self.assertRaises(MODULE.DesignError):
            MODULE.verify(ARCH.resolve(), lock)


if __name__ == "__main__":
    unittest.main()
