"""Load the reference check-identity fixture module without running its CLI exit."""
import importlib.util,sys,pathlib
def load_kit(foundation:str):
    H=pathlib.Path(foundation).resolve()
    argv=sys.argv;sys.argv=['check-identity.py']
    spec=importlib.util.spec_from_file_location('kit_check_identity',H/'check-identity.py')
    m=importlib.util.module_from_spec(spec);sys.modules['kit_check_identity']=m
    try:spec.loader.exec_module(m)
    except SystemExit:pass
    finally:sys.argv=argv
    return m
