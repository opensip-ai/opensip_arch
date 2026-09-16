"""New naming must preserve complete review/source joins, not just pin syntax.

Uses explicitly synthetic acceptance fixtures from the inherited verifier tests.
These fixtures are not review evidence or actual Grok/Claude approvals.
"""
import copy
import json
import unittest
import test_design_binding as fixtures
MODULE = fixtures.MODULE


class ReviewerReferenceTests(unittest.TestCase):
    def fixture(self, kind):
        fixture = (fixtures.InventorySuccessorTests if kind == 'inventory' else fixtures.ContractSuccessorTests)()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        return fixture, fixture.lock[kind + 'Successor']

    def rewrite(self, fixture, binding, key, change):
        pin = binding[key]
        value = json.loads((fixture.root / pin['path']).read_bytes())
        change(value)
        binding[key] = fixture.write(pin['path'], value)

    @staticmethod
    def neutral(value):
        value['independentReview'] = value.pop('actualClaudeReview')

    def test_neutral_reference_selects_same_reviewed_unit(self):
        for kind in ('inventory', 'contract'):
            with self.subTest(kind=kind):
                f, b = self.fixture(kind)
                before = MODULE.verify(f.root, f.lock)
                self.rewrite(f, b, 'assent', self.neutral)
                after = MODULE.verify(f.root, f.lock)
                self.assertEqual(before, after)
                self.assertFalse(after['productQualification'])

    def test_missing_reference_refuses(self):
        for kind in ('inventory', 'contract'):
            f, b = self.fixture(kind)
            self.rewrite(f, b, 'assent', lambda v: v.pop('actualClaudeReview'))
            with self.assertRaisesRegex(MODULE.DesignError, 'exactly one review reference'):
                MODULE.verify(f.root, f.lock)

    def test_dual_names_refuse_even_when_identical(self):
        for kind in ('inventory', 'contract'):
            for same in (True, False):
                with self.subTest(kind=kind, same=same):
                    f, b = self.fixture(kind)
                    def change(v):
                        v['independentReview'] = copy.deepcopy(v['actualClaudeReview'])
                        if not same:
                            v['independentReview']['sha256'] = '0' * 64
                    self.rewrite(f, b, 'assent', change)
                    with self.assertRaisesRegex(MODULE.DesignError, 'exactly one review reference'):
                        MODULE.verify(f.root, f.lock)

    def test_neutral_bad_or_mismatched_pin_refuses(self):
        for kind in ('inventory', 'contract'):
            for invalid in (None, {}, 'not-a-pin', {'path': 'other-review.json', 'sha256': '0' * 64, 'bytes': 1}):
                with self.subTest(kind=kind, invalid=invalid):
                    f, b = self.fixture(kind)
                    def change(v):
                        v.pop('actualClaudeReview')
                        v['independentReview'] = invalid
                    self.rewrite(f, b, 'assent', change)
                    with self.assertRaises(MODULE.DesignError):
                        MODULE.verify(f.root, f.lock)

    def test_neutral_name_does_not_allow_changes_required_review(self):
        for kind in ('inventory', 'contract'):
            f, b = self.fixture(kind)
            self.rewrite(f, b, 'review', lambda v: v.update(verdict='CHANGES-REQUIRED'))
            def change(v):
                v.pop('actualClaudeReview')
                v['independentReview'] = b['review']
            self.rewrite(f, b, 'assent', change)
            with self.assertRaisesRegex(MODULE.DesignError, 'independent .* acceptance'):
                MODULE.verify(f.root, f.lock)

    def test_neutral_name_does_not_allow_unresolved_review_findings(self):
        for kind in ('inventory', 'contract'):
            f, b = self.fixture(kind)
            self.rewrite(f, b, 'review', lambda v: v.update(requiredFindings=['still-open']))
            def change(v):
                v.pop('actualClaudeReview')
                v['independentReview'] = b['review']
            self.rewrite(f, b, 'assent', change)
            with self.assertRaisesRegex(MODULE.DesignError, 'independent .* acceptance'):
                MODULE.verify(f.root, f.lock)

    def test_neutral_contract_reference_still_requires_exact_review_size(self):
        f, b = self.fixture('contract')
        def change(v):
            self.neutral(v)
            v['independentReview']['bytes'] = 0
        self.rewrite(f, b, 'assent', change)
        with self.assertRaisesRegex(MODULE.DesignError, 'contract root review'):
            MODULE.verify(f.root, f.lock)
