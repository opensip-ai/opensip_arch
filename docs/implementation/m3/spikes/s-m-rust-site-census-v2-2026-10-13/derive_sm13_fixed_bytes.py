from pathlib import Path
import json, hashlib
# U-3 desk record (S-M report plan PLAN-r2): SM-13 part two, the exact fixed bytes that (b)-(e) add per candidate, per
# frame and per census row, from the registered schemas and RPP candidateSpoolAccounting (PROPOSAL-r6:589), with the
# closed formulas for (a)-(e) and SM-14 with every later-owned parameter UNSET. Reference encoder: the RFC 8949
# deterministic-CBOR head-size rule implemented below (`head`), lead-written, unreviewed outside this unit. It encodes
# no value; it counts the bytes of fixed keys, headers and fixed values only. Writes sm13-fixed-bytes.json beside itself.
H = Path(__file__).resolve().parent; A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = Path('/Users/sb/code/opensip-ai/opensip')
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def head(n):  # RFC 8949 §3 / §4.2.1 shortest head for a major type carrying argument n
    return 1 if n < 24 else 2 if n < 2**8 else 3 if n < 2**16 else 5 if n < 2**32 else 9
def text(s): b = s.encode(); return head(len(b)) + len(b)
def keys(*ks): return sum(text(k) for k in ks)
RPP = A / 'docs/coop/artifacts/rust-provider-protocol.v2.json'; FP = A / 'docs/coop/artifacts/fact-plane.v1.json'
REG = P / 'schemas/sources/relation-payload-v2.schema.json'; FB3 = P / 'schemas/sources/fact-batch-v3.schema.json'; OCC = P / 'schemas/sources/occupancy-v1.schema.json'
CEN = A / 'docs/implementation/m3/native-successors-fa/fa-2/product/schemas/sources/symbol-census-v1.schema.json'; NE = A / 'docs/v2/contracts/product-v1/native-evidence.md'
rpp = json.loads(RPP.read_text()); fp = json.loads(FP.read_text()); reg = json.loads(REG.read_text())['x-opensip-relation-registry']['relations']
cand = fp['factRecordContractV1']['candidateSchema']; anchor = fp['factRecordContractV1']['anchorSchema']; spool = rpp['limitPolicy']['candidateSpoolAccounting']
assert cand['id'] == 'opensip.fact-candidate.v1' and cand['optional'] == [] and len(cand['required']) == 14
assert anchor['id'] == 'opensip.anchor-ref.v1' and anchor['optional'] == [] and len(anchor['required']) == 7
assert spool['entryShape'].startswith('the closed map {analysisOrdinal,stageId,candidate}')
assert 'layer `semantic`' in NE.read_text().splitlines()[2188]  # NE:2189 unresolved-edge layer
layer = {k: v['layer'] for k, v in fp['relationRegistry']['relations'].items() if v}; layer['unresolved-edge'] = 'semantic'
# The rust-cargo cells of NE's capability table (NE:591-601), as relation@rung.
ROWS = [('declares', 'syntactic'), ('literal', 'syntactic'), ('control-flow', 'syntactic'), ('imports', 'resolved-target'), ('references', 'resolved-binding'),
        ('calls', 'resolved-callee'), ('types', 'checked'), ('reachability', 'from-resolved-calls'), ('clones', 'normalized-body-hash'), ('clones', 'near (candidate only)'),
        ('unresolved-edge', 'observed')]
PRODUCER = 'rust-semantic'; LANGUAGE = 'rust'; SOURCE_UNIVERSE_LEN = len('sha256:') + 64
candidate_fixed_common = 1 + keys(*cand['required']) + text(PRODUCER) + text(LANGUAGE) + head(SOURCE_UNIVERSE_LEN) + SOURCE_UNIVERSE_LEN  # map(14) head + 14 keys + fixed values
rows = []
for rel, rung in ROWS:
    r = reg[rel]; resolution = rung if not rung.startswith('near') else None
    fixed = candidate_fixed_common + text(rel) + text(layer[rel]) + text(r['schemaId']) + head(r['schemaVersion']) + (text(resolution) if resolution else 0)
    rows.append(dict(relationAtRung=f'{rel}@{rung}', relation=rel, layer=layer[rel], relationSchemaId=r['schemaId'], schemaVersion=r['schemaVersion'], resolution=resolution,
                     candidateFixedBytes=fixed, candidateFixedBytesExcludes=None if resolution else 'text(resolution_near): the encoded resolution value, required but unbound (A6; owner unresolved)',
                     resolutionUnsetReason=None if resolution else 'clones mode near is candidate-only; its resolution value is not fixed by the registered ladder (ambiguity A6)'))
anchor_fixed = 1 + keys(*anchor['required']) + text('source-span') + 1  # map(7) head + 7 keys + kind value + factId null
spool_fixed = 1 + keys('analysisOrdinal', 'stageId', 'candidate')
env_keys = ['payload', 'sequence', 'direction', 'frameType', 'protocolMajor']
envelope_fixed = 1 + keys(*env_keys) + text('worker-to-host') + text('FactBatch') + head(3)  # protocolMajor 3 under Rust3 (NE:122)
fb2_fixed = 1 + keys('stageId', 'batchIndex', 'candidates', 'analysisOrdinal')
fb3_fixed = 1 + keys('stageId', 'batchIndex', 'candidates', 'analysisOrdinal', 'schemaVersion', 'occupancyCompanions') + head(3)
occ_keys = ['kind', 'exported', 'occupancy', 'logicalPath', 'schemaVersion', 'targetNativeId', 'candidateOrdinal', 'targetUniverseId', 'evaluationNativeId', 'packageManifestPath']
occ_fixed = 1 + keys(*occ_keys) + head(1)  # map(10) head + 10 keys + schemaVersion const 1 (occupancy-v1; Codex SM-SITE-V2-R1-RF-01)
census_row_fixed = 1 + keys('path', 'exported', 'qualifiedName', 'nativeSubjectId', 'signatureTokens')
census_complete_fixed = 1 + keys('rows', 'state', 'examinedPaths') + text('complete')
result = dict(
    standing='UNREVIEWED DESK RECORD (U-3, SM-13 PART TWO AND THREE); FIXED BYTES AND CLOSED FORMULAS ONLY; NO SM-13 OR SM-14 VALUE; LATER-OWNED PARAMETERS UNSET',
    referenceEncoder=dict(name='derive_sm13_fixed_bytes.head (RFC 8949 shortest-head rule)', standing='lead-written, unreviewed outside this unit; counts heads, fixed keys and fixed values; encodes no value'),
    sources=[pin(p) for p in [RPP, FP, REG, FB3, OCC, CEN, NE]],
    perCandidate=dict(rows=rows, commonFixedBytes=candidate_fixed_common,
                      variable=dict(candidateOrdinal='uint head, 1-9 bytes (value)', producerVersion='text, the release providerBuildId (release)', targetUniverseId='text (host-admitted target domain; G3 emission)',
                                    confidenceMillionths='uint 0..1000000, 1-5 bytes (G3)', canonicalRelationPayload='byte string, head + payload bytes (G3 emission)', anchors='array head + per-anchor bytes; anchor count G3', resolution_near='clones near only: text(resolution value), required, unbound (A6; owner unresolved); added to that row candidateFixedBytes'),
                      perSourceSpanAnchorFixedBytes=anchor_fixed, anchorVariable='path text, startByte/endByte uints, snapshotId text, contentSha256 text (formats: ambiguity A5)'),
    b_spool=dict(perEntryFixedBytes=spool_fixed, formula='b = Σ_candidates [spoolFixed + text(stageId) + uint(analysisOrdinal) + candidateBytes]; stageId is C4a (1..255 bytes); candidateBytes = candidateFixed(relation@rung) + variable members', source='RPP:137-150'),
    c_payload=dict(envelopeFixedBytes=envelope_fixed, factBatchV2FixedBytes=fb2_fixed, factBatchV3FixedBytes=fb3_fixed, occupancyCompanionFixedBytes=occ_fixed,
                   formula='c = Σ over the FactBatch frames of the G3 partition [envelopeFixed + uint(sequence) + factBatchFixed + text(stageId) + uint(batchIndex) + uint(analysisOrdinal) + arrayHead(n) + Σ candidateBytes (+ V3: arrayHead(m) + Σ companion bytes)] + Coverage and terminal frame payloads',
                   readings=dict(A1='RPP:151 envelope payload bytes read as the whole 5-key envelope map (the framing text RPP:161,167); the other reading counts only the payload value, i.e. subtract envelopeFixed + uint(sequence) per frame',
                                 A2='FactBatchV2 or V3 depends on whether M3 negotiates target-attribution-v2 (NE:2801-2810); both fixed sizes are given')),
    d_frames=dict(prefixBytesPerFrame=40, formula='d = Σ_stages [factBatchFrames_stage + coverageFrames_stage] + terminal + handshake/acceptance replies; factBatchFrames_stage is the number of FactBatch frames in the G3 batch partition of that stage (unset; each nonempty batch <= 4096 candidates and within frame bounds)',
                  conditionalCase='only under a uniform full-packing partition with batch size B: factBatchFrames_stage = ceil(candidates_stage / B); not the general formula (Codex SM-SITE-V2-R1-RF-02)', readingA3='which frames maxResponseFrames counts is not stated by RPP'),
    e_census=dict(rowFixedBytes=census_row_fixed, completeContainerFixedBytes=census_complete_fixed,
                  formula='e_rows = census symbol rows (G3 census kinds); e_bytes = completeFixed + arrayHead(rows) + arrayHead(examinedPaths) + Σ_rows [rowFixed + text(path) + text(exported value) + text(qualifiedName) + text(nativeSubjectId) + arrayHead(tokens) + Σ text(token)] + Σ text(examinedPath)',
                  standing='FA-2 symbol-census-v1 is proposed in FA-2, not yet a product schema', readingA4='one census per Analyze (CompleteV3), not per stage; whether the 4 MiB bound covers the census map or the whole Complete frame'),
    a_candidates=dict(formula='a = Σ_site kinds [sites(kind) × emissionFactor(kind)] per relation@rung and stage; emissionFactor is G3; stage grouping is C4a'),
    SM14=dict(formula='SM-14 = Σ_stages S_stage × K_stage; S per workload exact (census r1/v2, RUST3-LIM); K_stage unset (C4a)'),
    ambiguities=dict(A1='RPP:151 payload scope', A2='FactBatch V2 or V3', A3='maxResponseFrames scope', A4='census per Analyze vs per stage; census bound scope', A5='anchor snapshotId/contentSha256 formats under snapshot2 (RPP:464 snap1 vs FA-2 snapshot2)', A6='clones near candidate resolution value'),
    unsetParameters=dict(G3=['emission factor per site kind', 'census symbol kinds', 'batching', 'confidence', 'targetUniverseId', 'relation payload', 'anchors per candidate'], C4a=['stage grouping', 'stageId', 'requested keys K_stage'], release=['producerVersion']),
    SM13ValueDerived=False, SM14ValueDerived=False, ownedParametersChosen=False)
(H / 'sm13-fixed-bytes.json').write_text(json.dumps(result, indent=1) + '\n')
for r in rows: print(r['relationAtRung'], r['candidateFixedBytes'])
print('anchor', anchor_fixed, 'spool', spool_fixed, 'envelope', envelope_fixed, 'fb2', fb2_fixed, 'fb3', fb3_fixed, 'occ', occ_fixed, 'censusRow', census_row_fixed, 'censusComplete', census_complete_fixed)
