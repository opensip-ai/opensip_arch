"""R2 fix 2 (design closure, no new vocabulary): recommend's recommendations carry zero rows in this profile because no
recommendation detail is registered; the only advisory next step is the explicit discovery.workspaceRoots config2
proposal. Policy-test refusal wording names the suite admission route and keeps resolver refusals as result data."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2/tools')
from textedit import apply, edit_json  # noqa: E402

ENV = 'docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
rows = []


def close_recommendations(doc):
    rec = doc["$defs"]["DiscoveryRecommendationRecordV1"]["properties"]["recommendations"]
    assert rec["maxItems"] == 1024
    rec["maxItems"] = 0
    rec["description"] = ("Zero rows in this profile: no recommendation detail is registered. The only advisory next step is the explicit "
                          "discovery.workspaceRoots config2 proposal. A recommendation vocabulary requires registered details and a successor of this record.")


rows.append(edit_json('R2 fix2 recommendations closed', ENV, close_recommendations))
rows.append(apply('R2 fix2 prose', WS, [
    ('''`recommendations` (`DomainDetail[]`), `config2Proposals` |''',
     '''`recommendations` (`DomainDetail[]`, zero rows in this profile), `config2Proposals` (at most one) |'''),
    ('''`policy-test` an inadmissible suite `CONFIG.INVALID` / `CONFIG.INVALID`
(resolver refusals are result data);''',
     '''`policy-test` a suite that fails `PolicyTestSuiteV1` admission `CONFIG.INVALID` with the registered
`CONFIG.INVALID` detail (candidate-policy and waiver resolver refusals are result data with
`resolverAccepted=false`);'''),
    ('''not a baseline-show failure. The only config2 proposal is
explicit `discovery.workspaceRoots`; config2 publishes no other proposal grammar.''',
     '''not a baseline-show failure. `recommend` is advisory: its only next-step suggestion in this profile is
the explicit `discovery.workspaceRoots` config2 proposal (zero or one), whose roots are discovered
unit roots. `recommendations` carries zero rows because no recommendation detail is registered; a
recommendation vocabulary requires registered details and a successor of this record. config2
publishes no other proposal grammar.'''),
]))
rows.append(apply('R2 fix2 recommendation closure control', CWP, [
    ('''must_invalid("r2-recommend-unregistered-recommendation-refused", _R2_ENV, _r2_unregistered)
''', '''must_invalid("r2-recommend-unregistered-recommendation-refused", _R2_ENV, _r2_unregistered)
_r2_registered_row = {"code": "native.explicit-root-without-marker", "remedy": "r"}
must_valid("r2-recommend-closure-control-row-is-a-registered-domain-detail", U + "common:3#/$defs/DomainDetail", _r2_registered_row)
_r2_registered = copy.deepcopy(_R2_ENVS["recommend"])
_r2_registered["queryRecord"]["recommendations"] = [_r2_registered_row]
must_invalid("r2-recommend-registered-detail-is-not-a-recommendation-in-this-profile", _R2_ENV, _r2_registered)
check("r2-recommend-config2-proposal-roots-are-the-discovered-unit-roots",
      [QS.DD.normalize_explicit_root(r) for r in _R2_ENVS["recommend"]["queryRecord"]["config2Proposals"][0]["workspaceRoots"]]
      == sorted({u["rootPath"] for u in _r2_discovery["units"]}, key=lambda s: QS.DD.spell_root(s))
      and _R2_ENVS["recommend"]["query"]["items"] == 0)
'''),
]))
print(json.dumps(rows, indent=1))
