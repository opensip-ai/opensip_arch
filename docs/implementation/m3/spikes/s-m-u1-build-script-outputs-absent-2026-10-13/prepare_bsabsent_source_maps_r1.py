from pathlib import Path
# U-1: the accepted source-map recipe (prepare_sm_remaining_graph_source_maps_r1.py as specialised by the accepted
# prepare_sm_actual_command_source_maps_r1.py), pointed at the variant's attempts receipt and output. No compiler use.
B=Path('/tmp/opensip-implementation')
s=(B/'prepare_sm_remaining_graph_source_maps_r1.py').read_text()
def rep(a,b):
 global s; assert s.count(a)==1,a[:60]; s=s.replace(a,b)
rep("V=B/'sm-graph-typecheck-2026-10-10'","V=B/'sm-command-data-bsabsent-2026-10-13'")
rep("remaining-graph-source-maps-r1.json","bsabsent-command-source-maps-r1.json")
rep("receipt_path=D/'corpus-graph-attempts-r61.json'","receipt_path=V/'bsabsent-command-data-attempts-r1.json'")
rep("if not entry.get('graph') or entry['ordinal']==3:continue","if not entry.get('graph'):continue")
rep("packet=entry['packet'],sourceMap","packet=entry['packet'],unitCommandData=entry['unitCommandData'],sourceMap")
rep('assert len(results)==6','assert len(results)==9')
rep("prefix=f'opensip-sm-graph-map-{entry[\"ordinal\"]}-'","prefix=f'opensip-sm-bsabsent-map-{entry[\"ordinal\"]}-'")
rep('UNREVIEWED ADDITIONAL PREPARED EXPERIMENTAL GRAPH SOURCE MAPS; NO COMPILER USE','UNREVIEWED U-1 VARIANT CONTEXT SOURCE MAPS FOR NINE ORIGINAL COMMAND DATA ENTRIES; NO COMPILER USE')
rep("result=dict(id=entry['id']","checked(Path(entry['unitCommandData']['path']),entry['unitCommandData'])\n result=dict(id=entry['id']")
exec(compile(s,str(__file__),'exec'))
