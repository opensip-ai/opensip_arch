from pathlib import Path
import json,hashlib,re
B=Path(__file__).resolve().parent;j=json.loads((B/'source-receipt.json').read_text());root=Path(j['originalRoot']);assert j['upstreamCommit']=='f2d3ce0bd7f24a49f8f72d9000448f8838c4e850'
rules={
 'direct-process-environment':r'\b(?:(?:std::)?env::(?:var|var_os|vars|vars_os|current_dir|current_exe|temp_dir|home_dir|set_var|remove_var)|(?:std::process::)?Command::new|jobserver::Client::from_env|home::(?:cargo_home|rustup_home))\s*\(',
 'global-context-constructor-and-lazy-state':r'\b(?:Env::new|CacheLocker::new|GlobalContext::(?:new|default)|get_or_try_init|global_cache_tracker|deferred_global_last_use|load_values|reload_rooted_at|load_credentials|configure|set_values)\s*\(',
 'filesystem-and-output':r'\b(?:(?:std::)?fs::(?:read|read_to_string|read_dir|write|create_dir|create_dir_all|remove_file|remove_dir_all|copy|rename|metadata|symlink_metadata|canonicalize)|File::(?:open|create)|OpenOptions::new|(?:\.)(?:open_ro|open_rw|acquire_package_cache_lock))\s*\(',
 'external-source-or-process':r'\b(?:ProcessBuilder::new|process|http_handle|http_config|enable_download|finish_download|download|load_source|query|preload|save)\s*\(',
}
compiled={k:re.compile(v)for k,v in rules.items()};records=[];pins=[]
for row in j['files']:
 rel=row['path']
 if not rel.endswith('.rs')or not rel.startswith(('src/cargo/','src/bin/','crates/cargo-util/','crates/cargo-util-schemas/')):continue
 raw=(root/rel).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256'];pins.append(row)
 for n,line in enumerate(raw.decode().splitlines(),1):
  families=[k for k,r in compiled.items()if r.search(line)]
  if families:records.append(dict(path=rel,line=n,families=families,sourceLine=line.strip()))
report=dict(standing='UNREVIEWED CONSERVATIVE LEXICAL BOUNDARY CENSUS OF EXACT UPSTREAM SOURCE; NOT RUST CALLGRAPH OR ADMISSION LIST',upstreamCommit=j['upstreamCommit'],sourceReceipt=dict(path=str(B/'source-receipt.json'),sha256=hashlib.sha256((B/'source-receipt.json').read_bytes()).hexdigest()),rules=rules,scannedRustFiles=pins,matches=records,counts={k:sum(k in r['families']for r in records)for k in rules},limitations=['Regex retains comments/declarations as conservative false positives and can miss aliased/multiline calls.','This is not an exhaustive parser result or transitive call graph. Metadata reachability and every allowed operation must still be proven against the complete producer.','No source operation was run; no real process environment/private installation/held fixture was inspected.','Plain operational inputs and source selectors do not confer SourceCap, Tool capability or signed profile authority.'],sourceProfilePublished=False,compatibleProducerImplemented=False,sourceAdmissionImplemented=False,productQualification=False)
(B/'boundary-census.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(scannedFiles=len(pins),matchingLines=len(records),counts=report['counts'])))
