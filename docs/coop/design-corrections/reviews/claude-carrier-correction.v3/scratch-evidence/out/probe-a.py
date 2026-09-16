import hashlib, importlib.util, inspect, json, os, re, sqlite3, sys
SRC = sys.argv[1]
OUT = sys.argv[2]
SEQ_MAX = 9007199254740991
def sha(path):
    b = open(path, 'rb').read()
    return hashlib.sha256(b).hexdigest(), len(b)
print('A ok')
