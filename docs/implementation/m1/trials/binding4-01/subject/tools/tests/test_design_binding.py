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


if __name__ == "__main__":
    unittest.main()
