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


    # Adapted from actual Claude SUCC-R1-01 independent isolation probes.
    def rebound(self, key, mutate):
        self.change(key, mutate)
        if key == "record":
            record = self.lock["inventorySuccessor"]["record"]
            self.change("review", lambda d: d["inventoryCandidateAssessment"]["successorRecord"].update(record))
            key = "review"
        if key == "review":
            review = self.lock["inventorySuccessor"]["review"]
            self.change("assent", lambda d: d["actualClaudeReview"].update(review))

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
        base_inputs = self.lock["inputs"]
        self.lock["inputs"] = [other]
        self.bind()
        self.lock["inputs"] = base_inputs
        self.refuse_with("selected base input")

    def test_isolated_extra_binding_with_valid_pin(self):
        self.lock["inventorySuccessor"]["extra"] = self.lock["inventorySuccessor"]["record"]
        self.refuse_with("five closed")


class ContractSuccessorTests(unittest.TestCase):
    write = DesignBindingTests.write
    bind = InventorySuccessorTests.bind

    def setUp(self):
        InventorySuccessorTests.setUp(self)
        self.lock["schemaVersion"] = 3
        self.member = self.write("new-contract.json", {"schemaMajor": 4})
        self.build_contract()

    def build_contract(self, record_change=None, manifest_change=None, review_change=None, assent_change=None):
        record = {"schemaVersion": 1, "parents": copy.deepcopy(self.lock["inputs"]), "candidates": [self.member],
                  "passageOverrides": [{"parent": copy.deepcopy(self.lock["inputs"][0]), "selector": {"jsonPointer": "/standing"}, "before": "base", "after": "corrected"}]}
        record = copy.deepcopy(record)
        if record_change:
            record_change(record)
        record_pin = self.write("unit-record.json", record)
        manifest = {"schemaVersion": 1, "files": sorted([self.member, record_pin], key=lambda row: row["path"])}
        if manifest_change:
            manifest_change(manifest)
        manifest_pin = self.write("unit-manifest.json", manifest)
        review = {"verdict": "ACCEPT-DESIGN-UNIT", "requiredFindings": [], "subjectManifestSha256": manifest_pin["sha256"]}
        if review_change:
            review_change(review)
        review_pin = self.write("unit-review.json", review)
        assent = {"status": "ACCEPTED-DESIGN-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [], "actualClaudeReview": review_pin, "subjectManifest": manifest_pin, "acceptedSuccessor": record_pin}
        assent = copy.deepcopy(assent)
        if assent_change:
            assent_change(assent)
        assent_pin = self.write("unit-assent.json", assent)
        self.lock["contractSuccessor"] = dict(record=record_pin, subjectManifest=manifest_pin, review=review_pin, assent=assent_pin)

    def refuse_with(self, pattern):
        with self.assertRaisesRegex(MODULE.DesignError, pattern):
            MODULE.verify(self.root, self.lock)

    def test_selected_contract_and_exact_override_preserve_parent(self):
        before = (self.root / "contract.json").read_bytes()
        result = MODULE.verify(self.root, self.lock)
        self.assertEqual(result["contractSuccessor"]["inputs"], [self.member])
        self.assertEqual(result["contractSuccessor"]["passageOverrides"][0]["after"], "corrected")
        self.assertFalse(result["productQualification"])
        self.assertEqual((self.root / "contract.json").read_bytes(), before)

    def test_decision_guards_with_downstream_joins_rebound(self):
        for mutate, pattern in [
            (lambda d: d.update(verdict="CHANGES-REQUIRED"), "independent contract acceptance"),
            (lambda d: d.update(requiredFindings=["open"]), "independent contract acceptance"),
            (lambda d: d.pop("requiredFindings"), "independent contract acceptance"),
            (lambda d: d.update(subjectManifestSha256="0" * 64), "review names a different manifest"),
        ]:
            self.build_contract(review_change=mutate)
            self.refuse_with(pattern)
        for mutate, pattern in [
            (lambda d: d.update(status="PENDING"), "root contract assent"),
            (lambda d: d.update(rootSubstantiveAssent=1), "root contract assent"),
            (lambda d: d.update(requiredUnitFindings=["open"]), "root contract assent"),
            (lambda d: d["subjectManifest"].update(sha256="0" * 64), "contract root subject"),
            (lambda d: d["actualClaudeReview"].update(bytes=0), "contract root review"),
            (lambda d: d["acceptedSuccessor"].update(sha256="0" * 64), "contract root successor"),
        ]:
            self.build_contract(assent_change=mutate)
            self.refuse_with(pattern)

    def test_closed_binding_and_version_selection(self):
        original = copy.deepcopy(self.lock)
        for key in self.lock["contractSuccessor"]:
            self.lock = copy.deepcopy(original)
            del self.lock["contractSuccessor"][key]
            self.refuse_with("four closed")
        self.lock = copy.deepcopy(original)
        self.lock["contractSuccessor"]["extra"] = self.lock["contractSuccessor"]["review"]
        self.refuse_with("four closed")
        self.lock = copy.deepcopy(original)
        self.lock["schemaVersion"] = 2
        self.refuse_with("unsupported design lock")

    def test_reviewed_subject_membership_and_complete_candidate_set(self):
        self.build_contract(manifest_change=lambda d: d["files"].pop())
        self.refuse_with("record is not in the reviewed subject")
        extra = self.write("extra-contract.json", {})
        self.build_contract(record_change=lambda d: d["candidates"].insert(0, extra))
        self.refuse_with("do not cover the reviewed subject")
        self.build_contract(record_change=lambda d: d["candidates"][0].update(sha256="0" * 64))
        self.refuse_with("candidate pin differs")
        self.build_contract(manifest_change=lambda d: d["files"].append(d["files"][-1]))
        self.refuse_with("sorted and unique")

    def test_unaccepted_parent_and_parent_overwrite_refuse(self):
        other = self.write("other-parent.json", {"standing": "base"})
        self.build_contract(record_change=lambda d: d.update(parents=[other]))
        self.refuse_with("not an accepted base")
        self.member = self.lock["inputs"][0]
        self.build_contract()
        self.refuse_with("overwrite its parent")

    def test_reviewed_override_must_select_exact_parent_text(self):
        changes = [
            (lambda d: d["passageOverrides"][0].update(before="wrong"), "before text differs"),
            (lambda d: d["passageOverrides"][0].update(after="base"), "must change one text value"),
            (lambda d: d["passageOverrides"].append(copy.deepcopy(d["passageOverrides"][0])), "duplicate passage"),
            (lambda d: d["passageOverrides"][0].update(selector={"line": True}), "line outside"),
            (lambda d: d["passageOverrides"][0]["parent"].update(sha256="0" * 64), "outside the accepted parent set"),
        ]
        for mutate, pattern in changes:
            self.build_contract(record_change=mutate)
            self.refuse_with(pattern)

    def test_candidate_bytes_cannot_be_locally_repinned(self):
        self.write("new-contract.json", {"schemaMajor": 99})
        self.refuse_with("digest mismatch")

    def test_passage_pointer_escaping_and_array_bounds(self):
        raw = b'{"a/b":{"~key":["selected"]}}'
        self.assertEqual(MODULE.selected_passage(raw, {"jsonPointer": "/a~1b/~0key/0"}), "selected")
        for pointer in ("/a~1b/~0key/-1", "/a~1b/~0key/01", "/a~1b/~0key/1", "/a~2b", "/a~"):
            with self.assertRaises(MODULE.DesignError):
                MODULE.selected_passage(raw, {"jsonPointer": pointer})


class SuccessorChainTests(unittest.TestCase):
    write = DesignBindingTests.write
    bind = InventorySuccessorTests.bind
    build_contract = ContractSuccessorTests.build_contract

    def setUp(self):
        InventorySuccessorTests.setUp(self)
        self.candidate['files'][1]['description'] = 'original description'
        self.bind()
        self.member = self.write('new-contract.json', {'schemaMajor': 4})
        parent = self.lock['inventorySuccessor']['candidate']
        self.build_contract(record_change=lambda record: record.update(parents=[parent], passageOverrides=[
            {'parent': parent, 'selector': {'jsonPointer': '/files/1/description'},
             'before': 'original description', 'after': 'accepted description'}]))
        self.lock['schemaVersion'] = 4
        self.lock['inventorySuccessors'] = [self.lock.pop('inventorySuccessor')]
        self.lock['contractSuccessors'] = [self.lock.pop('contractSuccessor')]
        self.lock['inventoryPassageInheritance'] = []

    def next_inventory(self, parent=None):
        parent = parent or self.lock['inventorySuccessors'][-1]['candidate']
        document = json.loads((self.root / parent['path']).read_text())
        document['files'].append({'path': 'aa.py', 'package': 'tooling', 'role': 'test'})
        document['files'].sort(key=lambda row: row['path'])
        candidate = self.write('candidate2.json', document)
        record = self.write('successor2.json', {'parent': parent, 'candidate': candidate,
                            'parentArtifactBytesUnchanged': True, 'inheritedRowsEqualByValue': True})
        review = self.write('successor-review2.json', {'verdict': 'ACCEPT-UNIT', 'requiredFindings': [],
                            'subjectManifestSha256': 'b' * 64, 'inventoryCandidateAssessment':
                            {**candidate, 'verdict': 'ACCEPT', 'requiredFindings': [], 'parent': parent, 'successorRecord': record}})
        assent = self.write('successor-assent2.json', {'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True,
                            'requiredUnitFindings': [], 'actualClaudeReview': review, 'acceptedInventory': candidate,
                            'subjectManifest': {'sha256': 'b' * 64}})
        self.lock['inventorySuccessors'].append(dict(parent=parent, candidate=candidate, record=record, review=review, assent=assent))
        self.lock['inventoryPassageInheritance'] = [{'parent': candidate, 'selector': {'jsonPointer': '/files/2/description'},
                                                   'before': 'original description', 'after': 'accepted description'}]

    def next_contract(self, parents=None, member=None, overrides=None):
        member = member or self.write('new-contract2.json', {'schemaMajor': 5})
        record = self.write('unit-record2.json', {'parents': parents or [self.member], 'candidates': [member],
                            'passageOverrides': overrides or []})
        manifest = self.write('unit-manifest2.json', {'files': sorted([record, member], key=lambda row: row['path'])})
        review = self.write('unit-review2.json', {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': manifest['sha256']})
        assent = self.write('unit-assent2.json', {'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True,
                            'requiredUnitFindings': [], 'actualClaudeReview': review, 'subjectManifest': manifest, 'acceptedSuccessor': record})
        self.lock['contractSuccessors'].append(dict(record=record, subjectManifest=manifest, review=review, assent=assent))

    def test_current_single_unit_selects_identically(self):
        result = MODULE.verify(self.root, self.lock)
        self.assertEqual(result['contractSuccessors'][0]['inputs'], [self.member])
        self.assertEqual(result['inventoryPassageInheritance'], [])

    def test_inventory_history_keeps_prior_contract_parent_and_reindexes_description(self):
        old = (self.root / 'candidate.json').read_bytes()
        self.next_inventory()
        result = MODULE.verify(self.root, self.lock)
        self.assertEqual(result['selectedInventory']['path'], 'candidate2.json')
        self.assertEqual(result['inventoryPassageInheritance'][0]['selector'], {'jsonPointer': '/files/2/description'})
        self.assertEqual((self.root / 'candidate.json').read_bytes(), old)
        self.assertEqual(json.loads((self.root / 'candidate2.json').read_text())['files'][2]['description'], 'original description')

    def test_inheritance_cannot_be_omitted_changed_or_target_another_row(self):
        self.next_inventory(); original = copy.deepcopy(self.lock['inventoryPassageInheritance'])
        for value in [[], [{**original[0], 'after': 'unreviewed'}], [{**original[0], 'selector': {'jsonPointer': '/files/1/description'}}]]:
            self.lock['inventoryPassageInheritance'] = value
            with self.assertRaisesRegex(MODULE.DesignError, 'passage inheritance differs'):
                MODULE.verify(self.root, self.lock)

    def test_contracts_can_extend_prior_accepted_candidate(self):
        self.next_contract()
        self.assertEqual(len(MODULE.verify(self.root, self.lock)['contractSuccessors']), 2)

    def test_reordered_contracts_and_unaccepted_parent_refuse(self):
        self.next_contract(); self.lock['contractSuccessors'].reverse()
        with self.assertRaisesRegex(MODULE.DesignError, 'parent is not an accepted'):
            MODULE.verify(self.root, self.lock)

    def test_inventory_branch_and_repeated_candidate_refuse(self):
        self.next_inventory(parent=self.lock['inputs'][0])
        with self.assertRaisesRegex(MODULE.DesignError, 'immediate predecessor'):
            MODULE.verify(self.root, self.lock)

    def test_duplicate_contract_and_existing_path_reuse_refuse(self):
        original = copy.deepcopy(self.lock['contractSuccessors'])
        self.lock['contractSuccessors'] *= 2
        with self.assertRaisesRegex(MODULE.DesignError, 'reuses an accepted path'):
            MODULE.verify(self.root, self.lock)
        self.lock['contractSuccessors'] = original
        self.next_contract(member=self.lock['inputs'][0])
        with self.assertRaisesRegex(MODULE.DesignError, 'reuses an accepted path'):
            MODULE.verify(self.root, self.lock)

    def test_conflicting_individually_reviewed_passages_refuse(self):
        parent = self.lock['inventorySuccessors'][0]['candidate']
        self.next_contract(parents=[parent], overrides=[{'parent': parent, 'selector': {'jsonPointer': '/files/1/description'},
                           'before': 'original description', 'after': 'different accepted description'}])
        with self.assertRaisesRegex(MODULE.DesignError, 'conflicting contract passage'):
            MODULE.verify(self.root, self.lock)

    def test_chains_are_closed_and_nonempty(self):
        original = copy.deepcopy(self.lock)
        for field in ['inventorySuccessors', 'contractSuccessors']:
            for value in [[], None, {}]:
                self.lock = copy.deepcopy(original); self.lock[field] = value
                with self.assertRaisesRegex(MODULE.DesignError, 'nonempty lists'):
                    MODULE.verify(self.root, self.lock)
        self.lock = copy.deepcopy(original); self.lock['contractSuccessor'] = original['contractSuccessors'][0]
        with self.assertRaisesRegex(MODULE.DesignError, 'unsupported design lock'):
            MODULE.verify(self.root, self.lock)


# Independent fixture builder adapted from actual Claude binding4 review01.
# Pins/reviews/assents are fully rebound so negative tests reach semantic guards.
def by_path(rows):
    return sorted(rows, key=lambda row: row["path"])


class Fx:
    def __init__(self, root):
        self.root = Path(root)

    def write(self, path, value, indent=None):
        raw = (json.dumps(value, sort_keys=True, indent=indent) + "\n").encode()
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

    def row(self, path, description):
        return {"path": path, "package": "tooling", "role": "r", "description": description}

    def base(self, rows, overlay=()):
        doc = {"schemaVersion": 1, "standing": "s", "packages": [{"id": "tooling", "dependencies": []}],
               "pendingDecisions": [], "files": by_path([self.row(p, d) for p, d in rows.items()])}
        inv0 = self.write("inv0.json", doc, indent=2)
        overlay_pins = [self.write(p, {"overlay": p}) for p in overlay]
        source = self.write("source.json", {"files": [inv0, *overlay_pins]})
        app = self.write("application.json", {"files": [], "designSubject": source})
        review = self.write("review.json", {"verdict": "ACCEPT", "subjectManifestSha256": app["sha256"], "newMustIssues": [], "newShouldIssues": []})
        activation = self.write("activation.json", {"applicationManifest": app, "independentApplicationReview": review})
        assent = self.write("assent.json", {"authority": {"rootApplicationAssent": True}, "subjectManifestSha256": app["sha256"], "review": review})
        completion = self.write("completion.json", {"designApprovedForImplementation": True, "passed": True, "applicationManifest": app, "activation": activation, "actualClaudeApplicationReview": review, "codexApplicationAssent": assent})
        self.lock = {"schemaVersion": 4, "architectureRepository": "fixture",
                     "approvals": dict(sourceManifest=source, applicationManifest=app, activation=activation, applicationReview=review, rootAssent=assent, completion=completion),
                     "inputs": [inv0], "inventorySuccessors": [], "contractSuccessors": [], "inventoryPassageInheritance": []}
        self.inv = [inv0]
        return inv0

    def hop(self, added, parent=None, candidate_path=None, append=True):
        parent = parent or self.inv[-1]
        n = len(self.lock["inventorySuccessors"]) + 1
        doc = json.loads((self.root / parent["path"]).read_bytes())
        doc["files"] = by_path(doc["files"] + [self.row(p, d) for p, d in added.items()])
        cand = self.write(candidate_path or f"inv{n}.json", doc, indent=2) if added is not None else parent
        rec = self.write(f"inv-record{n}.json", {"parent": parent, "candidate": cand, "parentArtifactBytesUnchanged": True, "inheritedRowsEqualByValue": True})
        subject = hashlib.sha256(f"inventory-subject-{n}".encode()).hexdigest()
        rev = self.write(f"inv-review{n}.json", {"verdict": "ACCEPT-UNIT", "requiredFindings": [], "subjectManifestSha256": subject,
                                                 "inventoryCandidateAssessment": {**cand, "verdict": "ACCEPT", "requiredFindings": [], "parent": parent, "successorRecord": rec}})
        ass = self.write(f"inv-assent{n}.json", {"status": "ACCEPTED-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                                 "actualClaudeReview": rev, "acceptedInventory": cand, "subjectManifest": {"sha256": subject}})
        binding = dict(parent=parent, candidate=cand, record=rec, review=rev, assent=ass)
        if not append:
            return binding
        self.lock["inventorySuccessors"].append(binding)
        self.inv.append(cand)
        return cand

    def rebind_hop(self, parent, candidate):
        """Rebind an inventory binding for an existing candidate pin (no file rewrite)."""
        n = len(self.lock["inventorySuccessors"]) + 1
        rec = self.write(f"inv-record{n}.json", {"parent": parent, "candidate": candidate, "parentArtifactBytesUnchanged": True, "inheritedRowsEqualByValue": True})
        subject = hashlib.sha256(f"inventory-subject-{n}".encode()).hexdigest()
        rev = self.write(f"inv-review{n}.json", {"verdict": "ACCEPT-UNIT", "requiredFindings": [], "subjectManifestSha256": subject,
                                                 "inventoryCandidateAssessment": {**candidate, "verdict": "ACCEPT", "requiredFindings": [], "parent": parent, "successorRecord": rec}})
        ass = self.write(f"inv-assent{n}.json", {"status": "ACCEPTED-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                                 "actualClaudeReview": rev, "acceptedInventory": candidate, "subjectManifest": {"sha256": subject}})
        binding = dict(parent=parent, candidate=candidate, record=rec, review=rev, assent=ass)
        self.lock["inventorySuccessors"].append(binding)
        return binding

    def contract(self, parents, overrides=(), members=None):
        n = len(self.lock["contractSuccessors"]) + 1
        if members is None:
            members = [self.write(f"c{n}/member.json", {"unit": n})]
        rec = self.write(f"c{n}/record.json", {"schemaVersion": 1, "parents": by_path(copy.deepcopy(parents)),
                                               "candidates": by_path(copy.deepcopy(members)), "passageOverrides": copy.deepcopy(list(overrides))})
        man = self.write(f"c{n}/manifest.json", {"files": by_path([rec, *members])})
        rev = self.write(f"c{n}/review.json", {"verdict": "ACCEPT-DESIGN-UNIT", "requiredFindings": [], "subjectManifestSha256": man["sha256"]})
        ass = self.write(f"c{n}/assent.json", {"status": "ACCEPTED-DESIGN-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                               "actualClaudeReview": rev, "subjectManifest": man, "acceptedSuccessor": rec})
        self.lock["contractSuccessors"].append(dict(record=rec, subjectManifest=man, review=rev, assent=ass))
        return {"members": members, "record": rec}

    def line_of(self, pin, needle):
        lines = (self.root / pin["path"]).read_text().splitlines()
        matches = [i for i, line in enumerate(lines) if needle in line]
        assert len(matches) == 1, matches
        return matches[0] + 1, lines[matches[0]]


def ov(parent, index, before, after):
    return {"parent": parent, "selector": {"jsonPointer": f"/files/{index}/description"}, "before": before, "after": after}


def pointer(parent, value, before, after):
    return {"parent": parent, "selector": {"jsonPointer": value}, "before": before, "after": after}


def proj(final, index, before, after):
    return ov(final, index, before, after)



class BindingHistoryRegressionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.fx = Fx(tmp.name)

    def history(self, count=1):
        fx = self.fx
        base = fx.base({'b.py': 'B0', 'd.py': 'D0'})
        first = fx.hop({'c.py': 'C0'})
        if count == 1:
            return base, first
        return base, first, fx.hop({'a.py': 'A0'})

    def verify(self):
        return MODULE.verify(self.fx.root, self.fx.lock)

    def refuse(self, pattern):
        with self.assertRaisesRegex(MODULE.DesignError, pattern):
            self.verify()

    def test_inventory_candidate_cannot_reuse_overlay_path(self):
        fx = self.fx
        base = fx.base({'b.py': 'B0'}, overlay=['overlay.json'])
        fx.hop({'c.py': 'C0'}, candidate_path='overlay.json')
        fx.contract([base])
        self.refuse('inventory candidate reuses an accepted path')

    def test_inventory_candidate_cycle_refuses_before_additive_comparison(self):
        base, first, final = self.history(2)
        self.fx.rebind_hop(final, first)
        self.fx.contract([base])
        self.refuse('inventory candidate reuses an accepted path')

    def test_unsupported_ancestor_selector_cannot_be_projected_as_description(self):
        base, final = self.history()
        self.fx.contract([base], [pointer(base, '/files/1/role', 'r', 'changed')])
        self.fx.lock['inventoryPassageInheritance'] = [proj(final, 2, 'r', 'changed')]
        self.refuse('unsupported inherited inventory passage selector')

    def test_direct_final_override_conflicting_with_ancestor_refuses(self):
        base, final = self.history()
        self.fx.contract([base], [ov(base, 1, 'D0', 'D1')])
        self.fx.contract([final], [ov(final, 2, 'D0', 'D2')])
        self.refuse('conflicts with direct override')

    def test_different_ancestor_overrides_of_same_file_refuse(self):
        base, first, final = self.history(2)
        self.fx.contract([base], [ov(base, 1, 'D0', 'D1')])
        self.fx.contract([first], [ov(first, 2, 'D0', 'D2')])
        self.fx.lock['inventoryPassageInheritance'] = [proj(final, 3, 'D0', 'D2')]
        self.refuse('inherited inventory passage meanings conflict')

    def test_identical_final_override_suppresses_inheritance(self):
        base, final = self.history()
        self.fx.contract([base, final], [ov(base, 1, 'D0', 'D1'), ov(final, 2, 'D0', 'D1')])
        self.assertEqual(self.verify()['inventoryPassageInheritance'], [])
        self.fx.lock['inventoryPassageInheritance'] = [proj(final, 2, 'D0', 'D1')]
        self.refuse('passage inheritance differs')

    def test_selector_sort_is_lexicographic_not_insertion_or_numeric(self):
        fx = self.fx
        base = fx.base({f'r{i:02d}.py': f'R{i}' for i in range(11)})
        final = fx.hop({'a.py': 'A0'})
        fx.contract([base], [ov(base, 1, 'R1', 'X1'), ov(base, 9, 'R9', 'X9')])
        expected = [proj(final, 10, 'R9', 'X9'), proj(final, 2, 'R1', 'X1')]
        fx.lock['inventoryPassageInheritance'] = expected
        self.assertEqual(self.verify()['inventoryPassageInheritance'], expected)
        fx.lock['inventoryPassageInheritance'] = expected[::-1]
        self.refuse('passage inheritance differs')

    def test_line_pointer_alias_on_final_json_parent_refuses(self):
        base, final = self.history()
        number, line = self.fx.line_of(final, '"D0"')
        self.fx.contract([final], [ov(final, 2, 'D0', 'D1')])
        self.fx.contract([final], [{'parent': final, 'selector': {'line': number},
                                  'before': line, 'after': line.replace('D0', 'D2')}])
        self.refuse('JSON parent passages require JSON Pointer')

    def test_json_detection_is_content_based_not_filename(self):
        base, final = self.history()
        misleading = self.fx.write('json-content.md', {'description': 'before'})
        self.fx.contract([base], members=[misleading])
        line = (self.fx.root / misleading['path']).read_text().splitlines()[0]
        self.fx.contract([misleading], [{'parent': misleading, 'selector': {'line': 1},
                                       'before': line, 'after': line.replace('before', 'after')}])
        self.refuse('JSON parent passages require JSON Pointer')

    def test_text_document_line_selectors_remain_valid(self):
        base, final = self.history()
        raw = b'# Markdown\nOriginal text.\n'
        (self.fx.root / 'text.md').write_bytes(raw)
        parent = {'path': 'text.md', 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        self.fx.contract([base], members=[parent])
        self.fx.contract([parent], [{'parent': parent, 'selector': {'line': 2},
                                    'before': 'Original text.', 'after': 'Reviewed replacement.'}])
        self.assertTrue(self.verify()['passed'])

    def test_malformed_candidate_path_has_controlled_diagnostic(self):
        base, final = self.history()
        self.fx.contract([base])
        for value in ([], {}, None, 1, ''):
            with self.subTest(value=value):
                self.fx.lock['inventorySuccessors'][0]['candidate']['path'] = value
                self.refuse('candidate path must be a nonempty string')

    def test_version3_retains_reviewed_json_line_selector_compatibility(self):
        base, final = self.history()
        number, line = self.fx.line_of(final, '"D0"')
        self.fx.contract([final], [{'parent': final, 'selector': {'line': number},
                                   'before': line, 'after': line.replace('D0', 'D1')}])
        lock = self.fx.lock
        lock['schemaVersion'] = 3
        lock['inventorySuccessor'] = lock.pop('inventorySuccessors')[0]
        lock['contractSuccessor'] = lock.pop('contractSuccessors')[0]
        del lock['inventoryPassageInheritance']
        self.assertTrue(self.verify()['passed'])


class GenerationSourceBindingTests(unittest.TestCase):
    write = DesignBindingTests.write

    def setUp(self):
        DesignBindingTests.setUp(self)
        self.implementation = self.root / 'implementation'
        (self.implementation / 'schemas/sources').mkdir(parents=True)
        # Add the schema to the accepted source manifest and rebind all approval joins.
        self.owner = self.write('schema.json', {'$id': 'urn:test:1', 'type': 'object'})
        source = self.write('source.json', {'files': [*self.lock['inputs'], self.owner]})
        app = self.write('application.json', {'files': [], 'designSubject': source})
        review = self.write('review.json', {'verdict': 'ACCEPT', 'subjectManifestSha256': app['sha256'], 'newMustIssues': [], 'newShouldIssues': []})
        activation = self.write('activation.json', {'applicationManifest': app, 'independentApplicationReview': review})
        assent = self.write('assent.json', {'authority': {'rootApplicationAssent': True}, 'subjectManifestSha256': app['sha256'], 'review': review})
        completion = self.write('completion.json', {'designApprovedForImplementation': True, 'passed': True, 'applicationManifest': app, 'activation': activation, 'actualClaudeApplicationReview': review, 'codexApplicationAssent': assent})
        self.lock['approvals'] = dict(sourceManifest=source, applicationManifest=app, activation=activation, applicationReview=review, rootAssent=assent, completion=completion)
        self.metadata = {'schemaId': 'urn:test:1', 'declaredMajor': 1, 'profile': 'json-schema', 'semanticValidatorOwner': 'test'}
        self.map = {'schemaVersion': 1, 'sources': [{'implementationPath': 'schemas/sources/test.json', 'architectureSource': self.owner, **self.metadata}]}
        self.registry = {'schemaVersion': 1, 'sources': [{'sourcePath': 'schemas/sources/test.json', 'sourceSha256': self.owner['sha256'], **self.metadata}]}
        (self.implementation / 'schemas/sources/test.json').write_bytes((self.root / 'schema.json').read_bytes())

    def verify(self):
        (self.implementation / 'schemas/source-map.json').write_text(json.dumps(self.map))
        (self.implementation / 'schemas/registry.json').write_text(json.dumps(self.registry))
        return MODULE.verify(self.root, self.lock, self.implementation)

    def test_accepted_source_bytes_bind_without_generator_execution(self):
        self.assertEqual(self.verify()['generationSources'], {'sourcesVerified': 1, 'executedGeneratorCode': False, 'productQualification': False})

    def test_local_repin_cannot_select_unaccepted_architecture_source(self):
        pin = self.write('unaccepted.json', {'$id': 'urn:test:1', 'type': 'string'})
        self.map['sources'][0]['architectureSource'] = pin
        self.registry['sources'][0]['sourceSha256'] = pin['sha256']
        (self.implementation / 'schemas/sources/test.json').write_bytes((self.root / 'unaccepted.json').read_bytes())
        with self.assertRaisesRegex(MODULE.DesignError, 'not selected by accepted design'):
            self.verify()

    def test_accepted_owner_changed_on_disk_refuses(self):
        (self.root / 'schema.json').write_text('{}')
        with self.assertRaisesRegex(MODULE.DesignError, 'digest mismatch'):
            self.verify()

    def test_different_local_copy_refuses(self):
        (self.implementation / 'schemas/sources/test.json').write_text('{}')
        with self.assertRaisesRegex(MODULE.DesignError, 'bytes differ from accepted architecture'):
            self.verify()

    def test_registry_digest_and_id_cannot_be_locally_rebound(self):
        original = copy.deepcopy(self.registry)
        self.registry['sources'][0]['sourceSha256'] = '0' * 64
        with self.assertRaisesRegex(MODULE.DesignError, 'registry digest differs'):
            self.verify()
        self.registry = original
        self.registry['sources'][0]['schemaId'] = 'urn:other:1'
        self.map['sources'][0]['schemaId'] = 'urn:other:1'
        with self.assertRaisesRegex(MODULE.DesignError, 'schema ID differs from accepted source'):
            self.verify()

    def test_missing_duplicate_and_escaping_mapping_refuse(self):
        self.map['sources'].append(copy.deepcopy(self.map['sources'][0]))
        with self.assertRaisesRegex(MODULE.DesignError, 'duplicate mapped source path'):
            self.verify()
        self.map['sources'].pop()
        self.registry['sources'].append({**self.registry['sources'][0], 'sourcePath': 'extra.json'})
        with self.assertRaisesRegex(MODULE.DesignError, 'coverage differ'):
            self.verify()
        self.registry['sources'].pop()
        self.map['sources'][0]['implementationPath'] = '../schema.json'
        with self.assertRaisesRegex(MODULE.DesignError, 'noncanonical path'):
            self.verify()


if __name__ == "__main__":
    unittest.main()
