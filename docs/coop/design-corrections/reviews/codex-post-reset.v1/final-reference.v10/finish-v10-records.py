from pathlib import Path
import json,shutil,hashlib
r=Path.cwd();dc=r/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections/codex-post-reset.v1')
assert (dc/'historical-preservation-report.v10.json').is_file()
checks=Path('/tmp/opensip-design-corrections/final-reference-v10');report=json.loads((checks/'reference-checks.json').read_text());assert report['passed']
dest=out/'final-reference.v10';assert not dest.exists();shutil.copytree(checks,dest)
for name in ['run-final-v10.py','adapt-integration-builder-v10.py','refresh-pins-v6.py','record-v10.py','finish-v10-records.py']:
 shutil.copyfile(tmp/name,dest/name)
rows=[{'path':str(p.relative_to(dest)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file()]
(dest/'custody.json').write_text(json.dumps({'standing':'Codex executed final-source commands and integration/recording scripts, not independent acceptance.','files':rows},indent=2)+'\n')
p=dc/'post-reset-dispositions.v10.proposed.json';d=json.loads(p.read_text());d['actualCoauthorHistory']=[{'path':f'docs/coop/design-corrections/reviews/digest-corrections-author.{v}/handoff.json','sha256':hashlib.sha256((dc/f'reviews/digest-corrections-author.{v}/handoff.json').read_bytes()).hexdigest(),'sessionId':'5dec928a-6357-4726-9ea8-49a3079fb726','role':'Actual Claude coauthor, not independent acceptance'} for v in ('v7','v8')];p.write_text(json.dumps(d,indent=2)+'\n')
tech='''# Codex technical review of proposed v10 corrections

Standing: coauthor/integration assessment, **not independent acceptance or implementation readiness**. Actual Claude coauthor session `5dec928a-6357-4726-9ea8-49a3079fb726` completed follow-ups v7 and v8. Both exact handoffs, released source images, successful CLI responses and substantive tool evidence are retained. The completed independent v9 review remains CHANGES_REQUIRED for its single SHOULD v9-S1; no headline or passing authored check substitutes for its correction.

## Correction and scope

The existing relation-schema law declares three inadmissible conditions: an annotated field lacking its join, a join naming an absent field, and an unannotated digest/path field. The v9 reference enforced only the first two. Its shipped 13 closed selectors contained no unannotated governed fields, so this finding concerns the declared design/reference guard against future registered schema edits. It is not a demonstrated current payload or Run attack.

Claude v7 added a schema traversal for DigestHex, Sha256Text and CanonicalPath, including exact governed inline patterns, aliases, nullable branches, referenced containers and nested/array values. Codex's executed draft probes found three refinements: referenced containers were initially skipped; an annotated alternative could overwrite an unannotated alternative according to branch order; and a lawful annotation on an intermediate scalar alias was initially missed. Those exact draft sources, results and valid controls remain historical evidence. Final v7 corrected them.

Codex then found that v7's new inherited annotation account reached only the coverage rule. Its earlier retention/join rules still inspected direct property annotations. A nine-case field/alias/branch matrix showed that all six alias/branch variants admitted, including invalid retention and missing-join cases; the three direct-field controls behaved correctly. Claude's completed v8 substantively reviewed the full final v7 note and root's v8 note, acknowledged this inconsistency and unified all three rules around the same effective annotation sightings. No prior unread note is treated as agreement.

The final reference preserves invalid-retention and missing-join cause strings across all three supported annotation locations. Lawful not-joined controls and joined preimage controls remain admitted. An annotation on a terminal governed type does not give every field a blanket exemption. Conflicting annotations refuse rather than acquiring an invented precedence; identical annotations remain lawful. Existing join rows address top-level properties, so nested or array leaves cannot claim a joinable retention that the join vocabulary cannot reach. This is the present reference boundary, not a claim about a future path-addressing vocabulary. No shipped field is affected by these added boundaries.

Current normative product contracts, schemas and registry bytes are unchanged from frozen v9. The integration fixture is copied from the released checker with its exact source SHA and explicit declaration list; this remains synthetic construction, not an independently authored oracle. Current pins and deterministic reports were regenerated against the final reference source. No product implementation or historical repin occurred.

## Final-source evidence

All four Codex rechecks are retained with exact released source and results:

- `annotation-coverage-final-recheck.v10/`: all 13 actual selectors admit; 39 injected unannotated governed fields and one removed existing annotation refuse at RELATION_DIGEST_UNANNOTATED; both prior residue rules retain their intended causes.
- `annotation-traversal-final-recheck.v10/`: referenced-container and both branch-order negatives refuse while the actual document admits.
- `annotation-alias-final-recheck.v10/`: unannotated alias refuses; field-local and intermediate-alias annotations admit.
- `annotation-inherited-limbs-final-recheck.v10/`: the nine field/alias/branch cases consistently reject missing joins and invented retention with the exact causes, while all lawful not-joined controls admit.

Claude separately retained a measured v7/v8 source-image comparison and representative frozen-v9/current Run/body identity stability controls. Its initial neutralisation stub failed to represent the old split-account behavior and is explicitly retained as such; it is not a passing enforcement-removal test. The source-image comparison supplies the discriminating evidence. Authored tests did not originally discover Codex's counterexamples, and increased test counts are not a completeness claim.

The six executed final commands and source hashes are retained in `final-reference.v10/`; the current validation summary records their measured counts. All pass. A fresh independent session must reproduce those reports and assess the changed reference itself before acceptance.

## Remaining gates and preserved limits

The 25 carried advisory dispositions from completed v5 through v9 reviews remain in `advisory-application-account.v10.proposed.json`. The v9 723-byte example is the canonical wrapped edition record; its bare map is 711 bytes. L1–L3 normalization and synthetic level-specification assets remain unqualified. No clone facts alone does not authorize complete Coverage when owning dialect prerequisites are absent or partial. Complete-ledger comparison and host failure classification remain implementation obligations, not pure-helper effect authority.

All prior AR/FW findings, inherited residuals and scoped review owners remain accounted. All 32 product qualification gates remain undemonstrated. Original frozen subjects and the 31 protected historical evidence files remain intact. The original user-specified v1 manifest and all 1,192 subject files were verified again during this continuation.

Fresh independent acceptance at zero unresolved MUST/SHOULD, a NEW fresh blind consumer on the same accepted normative bytes, and complete independently reviewed application/readiness reconciliation remain required. This technical assessment does not apply D-372, authorize implementation, commit or push.
'''
p=out/'technical-review.v10.md';assert not p.exists();p.write_text(tech)
p=dc/'README.md';old=p.read_text();p.write_text('''# Architecture corrections — v10 ready for independent review

**Not ready for implementation.** Actual Claude and Codex completed the correction to the relation-schema law and its annotation traversal. [The technical assessment](reviews/codex-post-reset.v1/technical-review.v10.md) records the final-source counterexample rechecks, preserved valid controls and exact limits. All six final reference commands pass; this is not independent acceptance.

A newly frozen v10 must pass fresh independent review with zero unresolved MUST/SHOULD, a new blind consumer on those accepted bytes, and complete independently reviewed application/readiness reconciliation. No product implementation, commit or push is authorized. [The resume guide](reviews/NEXT-REVIEW.md) owns current work status.

## Earlier progress — historical

'''+old)
print('V10 final logs, technical assessment, both coauthor references and README recorded; independent review remains pending.')
