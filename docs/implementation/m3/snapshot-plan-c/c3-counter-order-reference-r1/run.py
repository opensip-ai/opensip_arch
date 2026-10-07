from pathlib import Path
import sys,unittest
p=Path('/tmp/opensip-implementation/c3-counter-order-reference');sys.path.insert(0,str(p));suite=unittest.defaultTestLoader.discover(str(p),pattern='test_reference.py');r=unittest.TextTestRunner(verbosity=2).run(suite);raise SystemExit(not r.wasSuccessful())
