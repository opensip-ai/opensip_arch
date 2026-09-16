import importlib.util
from pathlib import Path
F=Path('/tmp/opensip-design-corrections/candidate-subject.v25/docs/coop/design-corrections/foundation')
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
EN=load('en',F/'enumeration_model.v1.py')
print('_internal_root(".") ->',repr(EN._internal_root('.')))
print('_internal_root("")  ->',repr(EN._internal_root('')))
for spelling in ['','.']:
    unit={'unitOrdinal':0,'rootPath':spelling,'languageFamily':'tsjs','languageMode':'ts-tsconfig','unitKind':'ts-program','markerPath':'tsconfig.json','markerSha256':'0'*64,'recognizerId':'ts','recognizerVersion':1,'provenance':'DISCOVERED','memberPackageRoots':[]}
    membership={'units':[unit]}
    found=EN._unit_for_cell(membership,'.','ts-tsconfig')
    derived=EN._u1_entry(found,'ts-tsconfig')
    graph_entry='tsconfig.json'
    fault = 'ENUMERATION_BINDING_PROGRAM_ENTRY' if graph_entry!=derived else 'none'
    print('unit rootPath='+repr(spelling),'| cell workspaceRoot="." | _unit_for_cell ->',('FOUND' if found else 'None'),'| derived U-1 entry ->',repr(derived),'| retained graph entryConfigPath ->',repr(graph_entry),'| fault ->',fault)
