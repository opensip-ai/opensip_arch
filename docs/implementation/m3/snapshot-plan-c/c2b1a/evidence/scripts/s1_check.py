import re, subprocess, sys
# (file, line range, required substring) for SLOT-DERIVATION-r1's citations
R='crates/evaluator/src/native_retention.rs'; C='crates/evaluator/src/native_context.rs'; U='crates/evaluator/src/native_universe.rs'
checks = [
 (R,'90-92','budget.steps == 0'),(R,'100-103','sourceInventory'),(R,'104-113','NativeRetention {'),
 (R,'269-287','fn frame('),(R,'131-139','fn optional_rows'),(R,'149-166','fn path<'),
 (R,'195-227','inventoried-paths'),(R,'228-246','inventoried-path-and-digest'),(R,'288-303','nestedRecords'),
 (R,'184-200','fn blob_joins'),(R,'341-356','closureJoins'),(R,'247-266','fn closure('),(R,'256-259','closures.insert'),
 (R,'359-370','contextField'),(R,'372-400','inspect_native_context'),(R,'377','Refused(owner.refusals().into())'),
 (R,'400','Refused(owner.refusals().into())'),(R,'115-119','NativeRetentionChecks {'),
 (C,'376-380','Checks {'),(C,'76-78','configProjection'),(C,'80-83','closure2:'),(C,'189-222','fn closure('),
 (C,'87','moduleResolutionMode'),(C,'93-96','libSelection'),(C,'97-100','fold(s)'),(C,'101','selected_set'),
 (C,'102-110','lib-selection-order'),(C,'111-119','options_lib'),(C,'120-127','standardLibraryComponentDigests'),
 (C,'128-144','by_component'),(C,'145','declared'),(C,'146-151','stdlib-tree-mismatch'),(C,'152-156','inventory-incomplete'),
 (C,'157-161','lib-not-retained'),(C,'168-171','digests'),(C,'172-182','tool-not-in-closure'),(C,'387-391','to_string'),
 (C,'222','descriptor().clone()'),(C,'141','ambiguous-basename'),(C,'212','closure-{cause}'),(C,'218','kind-mismatch'),
 (U,'154-163','bind_typescript_universe'),(U,'164-169','contextField'),(U,'173-175','ContextDomain'),(U,'176-177','inspect_native_context'),
 (U,'182-185','sourceInventory'),(U,'186-188','cloned()'),(U,'348-416','fn fields'),(U,'190','configGraph'),
 (U,'193-196','paths'),(U,'197-200','configGraphPaths'),(U,'201','paths != context_paths'),(U,'204-214','source-mismatch'),
 (U,'417-487','fn graph'),(U,'418','include_bytes!'),(U,'216-234','configOrigin'),(U,'238','nodeModulesLayout'),
 (U,'271-293','fn layout_real_path_faults'),(U,'248-255','path-not-inventoried'),(U,'256-260','NativeUniverseChecks {'),
 (U,'202','configGraphPaths'),(U,'212','source-mismatch'),(U,'228','CONFIG_GRAPH_ENTRY_NOT_A_NODE'),(U,'233','configOrigin'),
 (U,'236','retained-input-missing:configGraph'),(U,'245','retained-input-missing:nodeModulesLayout'),(U,'288','realPath'),(U,'252','path-not-inventoried'),
 (R,'224','SnapshotPath(p.into())'),(R,'238','SnapshotSource(p.into())'),(R,'316-320','canonical_record'),(R,'303','self.blob(d, None)'),
 (U,'297-319','fn nested_record'),(U,'304-307','retainedAs'),(U,'319','format!("sha256:{}"'),(U,'320','inputs.blob(digest)'),(U,'337','canonical_record'),
 (U,'190','"configGraph"'),(U,'238','"nodeModulesLayout"'),
]
bad=0
for f,rng,sub in checks:
    lines=subprocess.run(['git','show','HEAD:'+f],capture_output=True,text=True,check=True).stdout.split('\n')
    a,b=(rng.split('-')+[rng])[:2]; a,b=int(a),int(b)
    seg='\n'.join(lines[a-1:b])
    if sub not in seg:
        bad+=1; print('MISS',f.split('/')[-1],rng,repr(sub))
print('checked',len(checks),'missing',bad)
