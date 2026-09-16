"""A record-level harness for laws whose owner is the (universe, native context) pair and
the configuration graph, without minting a whole Run.

Two distinct claims are kept apart and BOTH are reported:
  * owning-schema admission of the constructed records (B.Builder.admit / native_framed);
  * the named closure laws that take only (dom, universe, context) or (configGraph, universe)
    -- native-evidence section 1.2's mode table and x-opensip-config-node-kind-law -- executed
    by the SAME closure code the complete Runs use, with a snapshot inventory injected.

A harness result is explicitly NOT a complete Run: no Plan, proof, evidence, seal or Run
identity exists here, so nothing in this module may be reported as a complete positive.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_closure as CL

STANDING = ('record-level representable-path harness: owning-schema admission plus the '
            '(universe, context) and config-graph laws. NOT a complete Run.')


class Harness:
    def __init__(self, project_id, files):
        self.b = B.Builder(project_id)
        self.st = self.b.st
        for d in (B.IDENTITY_DOC, B.RELATION_DOC, B.NATIVE_DOC, B.COMMON_DOC):
            self.b.retain_schema_doc(d)
        self.files = dict(files)
        self.inv = {}
        for p, by in sorted(self.files.items()):
            self.st.put_blob(by, label='harness-source:' + p)
            self.inv[p] = {'sha256': K.raw_sha256(by), 'length': len(by)}
        self.c = CL.Closure(self.st)
        self.c.inv = self.inv

    def record(self, doc, selector, inst, label):
        return self.b.record(doc, selector, inst, label)

    def native(self, domain, doc, selector, inst, label):
        return self.b.native_framed(domain, doc, selector, inst, label)

    def mode_law(self, dom, uni, ctx):
        """Run native-evidence section 1.2's closed mode table over this pair and return the
        checks it actually executed, by name."""
        before = len(self.c.checks)
        self.c.check_language_mode_recognition(dom, uni, ctx)
        return [self._row(x) for x in self.c.checks[before:]]

    def config_kind_law(self, graph, uni):
        before = len(self.c.checks)
        self.c.check_config_node_kind_law(graph, uni)
        return [self._row(x) for x in self.c.checks[before:]]

    @staticmethod
    def _row(x):
        return {'check': x['check'], 'result': x['result'],
                'detail': CL.Closure._printable(x.get('detail'))}

    @staticmethod
    def refusals(rows):
        return [r for r in rows if r['result'] == 'REFUSE']
