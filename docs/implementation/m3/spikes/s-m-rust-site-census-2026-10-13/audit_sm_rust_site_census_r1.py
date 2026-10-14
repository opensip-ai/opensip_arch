from pathlib import Path
import json, hashlib, sys, os, stat
# Read-only audit of the S-M Rust site census r1. For each workload: the RUST3-LIM subject count S (non-empty regular
# .rs blobs of the verified T2 store tree, overlays by mount), the first-party site files mapped to subjects with
# byte equality against the store, subject coverage, and per-kind site totals for first-party and dependency crates
# kept apart. It checks population repetition and site-count determinism. It chooses no stage, key, emission factor,
# census kind or batching, and derives no SM-13 value. Writes site-census-checks-r1.json beside itself.
H = Path(__file__).resolve().parent; P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'
sys.path.insert(0, str(P / 'tools/quality')); from corpus import manifest_document; from store import verify
STORE = Path('/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store')
raw = (A / 'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes(); assert hashlib.sha256(raw).hexdigest() == 'c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578'
manifest = manifest_document(raw); entries = {r['id']: r for r in manifest['repositories']}; overlays = {w['id']: w for w in manifest['workspaces']}
counts = {r['id']: r for r in json.loads((A / 'docs/implementation/m3/native-successors-fa/rust3-lim/evidence/rust-subject-counts.json').read_text())['repositories']}
census = json.loads((H / 'site-census-r1.json').read_text())
# Site kinds are grouped by the relation@rung they are OFFERED for (NE:590-601). This grouping is a label, not an emission recipe.
OFFERED = {
 'declares@syntactic': dict(prefix='def.'),
 'imports@resolved-target': dict(kinds=['use', 'externCrate']),
 'references@resolved-binding': dict(kinds=['pathExpr.def', 'path.def', 'field', 'methodCall.resolved']),
 'calls@resolved-callee': dict(kinds=['call', 'methodCall']),
 'types@checked': dict(kinds=['expr.typed']),
 'unresolved-edge@observed': dict(kinds=['methodCall.dynReceiver', 'methodCall.paramReceiver', 'call.other', 'path.err', 'pathExpr.err', 'use.err', 'methodCall.unresolved']),
 'clones@normalized-body-hash': dict(kinds=['body']),
}
# A key ending in `.expanded` is the macro-expanded SUBSET of its base kind (site_walk.rs Walk::add). Base totals exclude
# it; the subset is reported separately and is never added to its base (Codex SM-SITE-R1-RF-01).
def offered_for(rule, k): return not k.endswith('.expanded') and (k.startswith(rule['prefix']) if 'prefix' in rule else k in rule['kinds'])
def offered_subset(rule, k): return k.endswith('.expanded') and offered_for(rule, k[:-len('.expanded')])
def subjects(root, prefix=''):
 out = {}
 for dirpath, dirnames, filenames in os.walk(root):
  for name in filenames:
   p = Path(dirpath) / name; st = p.lstat()
   if name.endswith('.rs') and stat.S_ISREG(st.st_mode) and st.st_size > 0: out[prefix + p.relative_to(root).as_posix()] = p
 return out
def workload_subjects(wid):
 if wid in overlays:
  result = {}
  for m in overlays[wid]['overlay']['members']:
   root = STORE / m['treeDigest']; verify(root, entries[m['entry']]); result.update(subjects(root, m['mount'] + '/'))
  return result
 root = STORE / entries[wid]['treeDigest']['value']; verify(root, entries[wid]); return subjects(root)
def add(total, files):
 for f, c in files.items():
  for k, v in c.items(): total[k] = total.get(k, 0) + v
rows = []
for rec in census['results']:
 wid = rec['id']; cwd = Path(rec['cwd']); root = cwd.parent if wid in overlays else cwd
 subj = workload_subjects(wid); run = rec['runs'][0]
 first = {}; deps = {}; per_subject = {}; outside = {}; units = dict(firstPartyAnalysed=0, dependencyAnalysed=0, firstPartyUnavailable=0, launchedIncomplete=0)
 for u in run['units']:
  if not u['compilerLaunched']:
   if u['firstParty']: units['firstPartyUnavailable'] += 1
   continue
  if u['standing'] != 'analysis-and-metadata-completed' or u['siteWalkEvents'] != 1: units['launchedIncomplete'] += 1; continue
  files = u['siteWalk']['files']
  if not u['firstParty']: units['dependencyAnalysed'] += 1; add(deps, files); continue
  units['firstPartyAnalysed'] += 1; add(first, files)
  for f, c in files.items():
   path = Path(f)
   rel = path.relative_to(root).as_posix() if path.is_absolute() and path.is_relative_to(root) else None
   if rel is None or rel not in subj: add(outside, {f: c}); continue
   assert path.read_bytes() == subj[rel].read_bytes(), rel
   bucket = per_subject.setdefault(rel, {})
   for k, v in c.items(): bucket[k] = bucket.get(k, 0) + v
 S = len(subj); covered = len(per_subject); known = counts.get(wid, {}).get('nonEmptyRsSubjects')
 offered = {rel: sum(v for k, v in first.items() if offered_for(rule, k)) for rel, rule in OFFERED.items()}
 offered_dep = {rel: sum(v for k, v in deps.items() if offered_for(rule, k)) for rel, rule in OFFERED.items()}
 offered_exp = {rel: sum(v for k, v in first.items() if offered_subset(rule, k)) for rel, rule in OFFERED.items()}
 offered_dep_exp = {rel: sum(v for k, v in deps.items() if offered_subset(rule, k)) for rel, rule in OFFERED.items()}
 dist = {}
 for rel, rule in OFFERED.items():
  vals = sorted(sum(v for k, v in c.items() if offered_for(rule, k)) for c in per_subject.values())
  if vals: dist[rel] = dict(coveredSubjects=len(vals), total=sum(vals), meanPerCoveredSubject=sum(vals) / len(vals), median=vals[len(vals) // 2], max=vals[-1])
 rows.append(dict(id=wid, ordinal=rec['ordinal'], subjectCountS=S, rust3LimRecordedS=known, rust3LimAgrees=(known == S) if known is not None else None,
                  firstPartySubjectsWithSites=covered, subjectCoverage=covered / S if S else None, coverageExact=covered == S,
                  units=units, firstPartySitesByKind=dict(sorted(first.items())), firstPartySitesOfferedByRelation=offered, firstPartyExpandedSubsetByRelation=offered_exp, firstPartyPerCoveredSubjectDistribution=dist,
                  firstPartySitesOutsideSubjects=sorted(outside), dependencyCrateSitesOfferedByRelation=offered_dep, dependencyCrateExpandedSubsetByRelation=offered_dep_exp, dependencyCrateSitesAreNotWorkloadSubjects=True,
                  acceptedPilotPopulationRepeated=rec['acceptedPilotPopulationRepeated'], siteCountsDeterministic=rec['siteCountsDeterministic']))
result = dict(standing='UNREVIEWED READONLY AUDIT OF THE S-M RUST SITE CENSUS r1; SITES ARE NOT CANDIDATES; NO SM-13 VALUE',
              relationGroupingIsLabelOnly=True, expandedKeysAreSubsetsNotAddedToBase=True, offeredRelationGrouping=OFFERED,
              unownedParameters=dict(emissionFactorPerSiteKind='G3', censusSymbolKinds='G3 with FA-2 enumeration contract', batching='G3', stageGrouping='C4a', requestedKeysPerStage='C4a', fixedOverheadBytes='not supplied by this unit'),
              workloads=rows, allPopulationsRepeated=all(r['acceptedPilotPopulationRepeated'] for r in rows), allSiteCountsDeterministic=all(r['siteCountsDeterministic'] for r in rows),
              workloadsWithExactCoverage=[r['id'] for r in rows if r['coverageExact']], SM11QuotientsDerived=False, SM13ValueDerived=False, SM14ValueDerived=False, SMComplete=False, LG1Met=False, effectiveL=False)
(H / 'site-census-checks-r1.json').write_text(json.dumps(result, indent=1) + '\n')
for r in rows: print(r['ordinal'], r['id'], 'S', r['subjectCountS'], 'R3L', r['rust3LimRecordedS'], 'covered', r['firstPartySubjectsWithSites'], r['units'], r['acceptedPilotPopulationRepeated'], r['siteCountsDeterministic'])
