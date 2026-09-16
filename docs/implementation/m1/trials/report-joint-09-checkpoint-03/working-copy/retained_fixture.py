"""Reuse unchanged pinned history02 retained-Run fixture setup, without its tests.

Actual reference close_run is executed over synthetic retained evidence. These
objects are not product storage handles, signatures or operational receipts.
"""
from pathlib import Path
from contextlib import contextmanager
import ast
import copy
import hashlib
import json
import types
HERE=Path(__file__).resolve().parent

@contextmanager
def world(read_unit,subjects):
    raw=read_unit('history-selection','check_query.py')
    marker=b'rows=[]\n';assert raw.count(marker)==1
    prefix=raw.split(marker)[0]
    # Keep all original owner sources and isolation behavior. Only the newly
    # proposed typed query producer/schema are rebound, as declared by joint09.
    old=b"(HERE/'query_history.py').read_bytes()"
    assert prefix.count(old)==1
    prefix=prefix.replace(old,b'JOINT_QUERY_BYTES')
    old=b"(HERE/'graph-query.history-candidate.schema.json').read_bytes()"
    assert prefix.count(old)==1;prefix=prefix.replace(old,b'JOINT_QUERY_SCHEMA_BYTES')
    # The setup builds its own old four-document registry. Use the complete
    # composed registry for query4 after source verification by the caller.
    namespace={'__file__':str(subjects['history-selection']/'check_query.py'),
               'JOINT_QUERY_BYTES':(HERE/'models/history/query_history.py').read_bytes(),
               'JOINT_QUERY_SCHEMA_BYTES':(HERE/'composed-sources/graph-query.proposed.schema.json').read_bytes()}
    try:
        exec(compile(prefix,'pinned-history02-retained-setup#query4','exec'),namespace)
        yield namespace
    finally:
        if 'original_get_code' in namespace:
            namespace['importlib'].machinery.SourceFileLoader.get_code=namespace['original_get_code']
