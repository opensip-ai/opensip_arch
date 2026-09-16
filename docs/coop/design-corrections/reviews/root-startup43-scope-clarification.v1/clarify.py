"""Document the completed author's R-4/R-5/R-6 limits in reference summaries, without changing behavior."""
from pathlib import Path
import hashlib,json,shutil
B=Path('/tmp/opensip-design-corrections')
T=B/'source43-provider-wire-successor.v1/source'
O=Path(__file__).resolve().parent
assert (B/'root-startup43-integration.v1/integration.json').is_file()
assert not (O/'clarification.json').exists()
edits=[
('docs/v2/contracts/product-v1/native-evidence.md',
'''**Reference scope.** `provider_startup_exchange` admits Hello, HelloAck, OpenUniverse,
UniverseAccepted, NativeContextVerified, Unavailable, the Coverage frame and Cancelled, each in
the phase the published machine is in. Snapshot, dependency-source, prepared, Analyze and
FactBatch frames are abstract events there. No framing, process or compiler is exercised.''',
'''**Reference scope.** `provider_startup_exchange` checks the published startup payload schemas
and selected cross-record joins in the phase of the abstract machine. Coverage checks cover
the wrapper shape and requested-key correspondence; they do not recompute commitments or
perform the complete inherited entry and request-ordinal admission. Its Cancelled check
covers only TypeScript's inserted `observedPhase` interval, not the complete inherited
Cancel/Cancelled record, correlation, Rust phase validation or host user-interruption reduction.
Those inherited validation and supervision laws remain required by their owners. Snapshot,
dependency-source, prepared, Analyze and FactBatch frames are abstract events here. Fixture
host inputs and placeholder commitments do not constitute a verified Plan or complete Run.
No framing, process or compiler is exercised.'''),
('docs/coop/design-corrections/native/native_evidence_model.v2.py',
'''    Hello, HelloAck, OpenUniverse, UniverseAccepted, NativeContextVerified, Unavailable, the Coverage frame and
    Cancelled are admitted here; snapshot, dependency-source, prepared, Analyze and FactBatch frames are abstract events
    whose payload laws are owned elsewhere. No framing, process or compiler is exercised."""''',
'''    Hello, HelloAck, OpenUniverse, UniverseAccepted, NativeContextVerified and Unavailable have the selected
    schema/join checks here. Coverage checks only wrapper shape and requested-key correspondence, not commitment,
    complete entry or request-ordinal admission. Cancelled checks only TypeScript's inserted observedPhase interval,
    not the inherited full record/correlation, Rust phase or host cancellation reduction. Other inherited owner
    checks remain prerequisites; snapshot, dependency-source, prepared, Analyze and FactBatch frames are abstract
    events. Fixture host inputs and placeholder commitments do not establish a verified Plan or complete Run.
    No framing, process or compiler is exercised."""'''),
('docs/coop/design-corrections/native/check_native_evidence.v2.py',
'''        "Provider startup exchanges admit Hello, HelloAck, OpenUniverse, UniverseAccepted, NativeContextVerified, Unavailable, the Coverage frame and Cancelled; snapshot, dependency-source, prepared, Analyze and FactBatch frames are abstract events, and the event machines are abstract host tables, not a framed process.",''',
'''        "Provider startup exchanges exercise selected startup schema/join checks. Coverage checks wrapper shape and requested-key correspondence, not commitments or complete entry/request-ordinal admission. Cancelled checks only the inserted TypeScript observedPhase interval, not full inherited record/correlation, Rust phase or host cancellation reduction. Other inherited owner checks remain prerequisites; snapshot, dependency-source, prepared, Analyze and FactBatch are abstract events. Fixture host inputs and placeholder commitments do not establish a verified Plan, complete Run or framed process.",''')]
rows=[]
for rel,old,new in edits:
 p=T/rel;raw=p.read_bytes();text=raw.decode();assert text.count(old)==1,rel
 before=O/'before'/rel;before.parent.mkdir(parents=True,exist_ok=True);before.write_bytes(raw)
 p.write_text(text.replace(old,new,1))
 rows.append({'path':rel,'beforeSha256':hashlib.sha256(raw).hexdigest(),'afterSha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/'clarification.json').write_text(json.dumps({'standing':'Root documentation-only clarification of existing helper scope and completed author R-4/R-5/R-6, plus actual trusted-input/placeholder fixture limits. No executable behavior changed. Included in pending successor; no independent assent.','files':rows},indent=2)+'\n')
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')/O.name
assert not L.exists();shutil.copytree(O,L);print(json.dumps(rows))
