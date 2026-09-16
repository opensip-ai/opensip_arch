# Generated summary (scripts/summarize.py)

## Positive

- `confined-1`: exit 0, stderr '', collection {"ok": true, "sha256": {"owners.json": "079d02da7aff1ae70fcfab9a30f2e6e5c08967cb359068a21c867dc6a2db4567", "rust-projection.json": "0923c4c4d8797586631f78b700cf2b3f7f092f14fff7e374dbd36bd3aeb15f92", "ts-projection.json": "2fec47ad98e20ad7788e4724cc755c142c9d8406ccb6f6c30148e7fb01a6b05a"}}
- `confined-2`: exit 0, stderr '', collection {"ok": true, "sha256": {"owners.json": "079d02da7aff1ae70fcfab9a30f2e6e5c08967cb359068a21c867dc6a2db4567", "rust-projection.json": "0923c4c4d8797586631f78b700cf2b3f7f092f14fff7e374dbd36bd3aeb15f92", "ts-projection.json": "2fec47ad98e20ad7788e4724cc755c142c9d8406ccb6f6c30148e7fb01a6b05a"}}
- `unconfined-entry`: exit 0, stderr '', collection {"ok": true, "sha256": {"owners.json": "079d02da7aff1ae70fcfab9a30f2e6e5c08967cb359068a21c867dc6a2db4567", "rust-projection.json": "0923c4c4d8797586631f78b700cf2b3f7f092f14fff7e374dbd36bd3aeb15f92", "ts-projection.json": "2fec47ad98e20ad7788e4724cc755c142c9d8406ccb6f6c30148e7fb01a6b05a"}}

```json
{
 "confinedRunsIdentical": true,
 "confinedEqualsUnconfinedEntry": true,
 "confinedEqualsDirectPrepareReference": true,
 "directReferenceAlsoWroteTargetsJson": true,
 "confinedEqualsTrial01PreparedInputs": true,
 "trial01PreparedInputsNote": "trial-01 work/inputs came from candidate-03 prepare.py of that moment; informational"
}
```

- direct reference files: {"owners.json": "079d02da7aff1ae70fcfab9a30f2e6e5c08967cb359068a21c867dc6a2db4567", "rust-projection.json": "0923c4c4d8797586631f78b700cf2b3f7f092f14fff7e374dbd36bd3aeb15f92", "targets.json": "598c0496ef0e08d320afa1a290a18e20a8eb182139d6780cf9b488aa95e4fcc3", "ts-projection.json": "2fec47ad98e20ad7788e4724cc755c142c9d8406ccb6f6c30148e7fb01a6b05a"}
- work tree unchanged: True; grants still pinned: True
- collector: `/private/tmp/opensip-implementation/m1-generator-integration-candidate-03/tools/generate_contracts.py` sha256 `79db5021c0e80181e1e135321c8e93d53ae01dc8a26c43992f216237c2de406d`

## Probe (main)

confined exit 1 stderr `prepare-inputs: PrepareInputsError: prepare emitted a different output set`; control exit 1 stderr `prepare-inputs: PrepareInputsError: prepare emitted a different output set`

| attempt | confined | unconfined control |
|---|---|---|
| chmodOutputRoot | PermissionError (errno 1) | ALLOWED |
| create:codeDir | PermissionError (errno 1) | ALLOWED |
| create:inputsDir | PermissionError (errno 1) | ALLOWED |
| create:outputParent | PermissionError (errno 1) | ALLOWED |
| create:privateTmp | PermissionError (errno 1) | — |
| create:stdlibDir | PermissionError (errno 1) | — |
| create:stdlibPycache | PermissionError (errno 1) | — |
| create:trialRoot | PermissionError (errno 1) | ALLOWED |
| create:varTmp | PermissionError (errno 1) | — |
| fork | PermissionError (errno 1) | ALLOWED |
| hardlinkCanaryIntoOutput | PermissionError (errno 1) | ALLOWED |
| import:_ctypes | ModuleNotFoundError | ALLOWED |
| import:_socket | ModuleNotFoundError | ALLOWED |
| import:pip | ModuleNotFoundError | ModuleNotFoundError |
| import:site | ALLOWED | ALLOWED |
| import:socket | ModuleNotFoundError | ALLOWED |
| import:ssl | ModuleNotFoundError | ALLOWED |
| import:subprocess | ModuleNotFoundError | ALLOWED |
| import:yaml | ModuleNotFoundError | ModuleNotFoundError |
| list:outputParent | PermissionError (errno 1) | ALLOWED = 4 |
| list:privateTmp | PermissionError (errno 1) | ALLOWED = 526 |
| list:stdlibGrantedDir | ALLOWED = 200 | ALLOWED = 200 |
| list:trial | PermissionError (errno 1) | ALLOWED = 12 |
| list:work | PermissionError (errno 1) | ALLOWED = 3 |
| osSystem | ALLOWED = 32512 | ALLOWED = 0 |
| posixSpawnSelf | PermissionError (errno 1) | ALLOWED |
| posixSpawnSh | PermissionError (errno 1) | ALLOWED |
| read:bundleInfoPlist | PermissionError (errno 1) | ALLOWED = 64 |
| read:canary | PermissionError (errno 1) | ALLOWED = 15 |
| read:candidate03Source | PermissionError (errno 1) | ALLOWED = 64 |
| read:etcPasswd | PermissionError (errno 1) | ALLOWED = 64 |
| read:frameworkSibling | PermissionError (errno 1) | ALLOWED = 64 |
| read:sitePackages | PermissionError (errno 1) | ALLOWED = 64 |
| read:stdlibBytecodeCache | PermissionError (errno 1) | ALLOWED = 64 |
| read:trialSourceCopy | PermissionError (errno 1) | ALLOWED = 64 |
| read:unimportedStdlib | PermissionError (errno 1) | ALLOWED = 64 |
| read:unselectedRuntime | PermissionError (errno 1) | ALLOWED = 64 |
| readThroughSymlink | PermissionError (errno 1) | ALLOWED = 15 |
| rmdirOutputRoot | PermissionError (errno 1) | ALLOWED |
| stat:canary | PermissionError (errno 1) | ALLOWED = 15 |
| stat:frameworkSibling | PermissionError (errno 1) | ALLOWED = 4399 |
| symlinkCanaryAsOwners | ALLOWED | ALLOWED |
| undeclaredOutput | ALLOWED | ALLOWED |
| writeOpen:entry | PermissionError (errno 1) | ALLOWED |
| writeOpen:optionsJson | PermissionError (errno 1) | ALLOWED |
| writeOpen:preparePy | PermissionError (errno 1) | ALLOWED |
| writeOpen:rawSchemasJson | PermissionError (errno 1) | ALLOWED |

```json
{
 "bytecodeWritten": true,
 "cpuCount": "ALLOWED",
 "environ": [
  "LC_CTYPE",
  "__CF_USER_TEXT_ENCODING"
 ],
 "getcwd": "PermissionError",
 "hostnameReadable": "ALLOWED",
 "openFds": [
  "0",
  "1",
  "2",
  "3",
  "4"
 ],
 "siteLoaded": true,
 "sysPath": [
  "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python314.zip",
  "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14",
  "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/lib-dynload"
 ],
 "usernameLookup": "ALLOWED"
}
```

output entries after confined probe: {"owners.json": {"symlink": true, "nlink": 1, "sameInodeAsCanary": false}, "targets.json": {"symlink": false, "nlink": 1, "sameInodeAsCanary": false}}

## Probe (exec)

confined exit 1 stderr `prepare-inputs: PermissionError: [Errno 1] Operation not permitted: '/private/tmp/opensip-implementation/m1-generator-python-confinement-trial-01/canary/secret.txt'`; control exit 0 stderr ``

| attempt | confined | unconfined control |
|---|---|---|
| execSh | PermissionError (errno 1) | — |
| execShNext | True | True |
| shExecRan | — | True |

output entries after confined probe: {}

## Network

| attempt | confined (+_socket) | confined (+_socket, no map-executable) | unconfined control |
|---|---|---|---|
| tcpConnectLoopback | PermissionError (errno 1) | PermissionError (errno 1) | ALLOWED |
| tcpListenLoopback | PermissionError (errno 1) | PermissionError (errno 1) | ALLOWED |
| udpSendLoopback | PermissionError (errno 1) | PermissionError (errno 1) | ALLOWED = 5 |
| unixConnectSyslog | ALLOWED | ALLOWED | ALLOWED |

listeners: confined {'tcp': False, 'udp': False}, no-map {'tcp': False, 'udp': False}, control {'tcp': True, 'udp': True}

collection of confined probe output: {"ok": false, "error": "GenerationError: undeclared, linked or nonregular generated output"}

## Ablations

| run | exit | output entries | stderr | sandbox denials reported |
|---|---|---|---|---|
| withoutIsolatedFlag | 1 | [] | `prepare-inputs: PrepareInputsError: invoke Python with -I -B -S and without optimization` | 0 |
| withoutNoSiteFlag | 1 | [] | `prepare-inputs: PrepareInputsError: invoke Python with -I -B -S and without optimization` | 0 |
| withoutBytecodeFlag | 1 | [] | `prepare-inputs: PrepareInputsError: invoke Python with -I -B -S and without optimization` | 0 |
| withoutMapExecutable | 0 | ['owners.json', 'rust-projection.json', 'ts-projection.json'] | `` | 0 |
| withoutRuntimeVocabularyGrant | 1 | [] | `prepare-inputs: PermissionError: [Errno 1] Operation not permitted: '/private/tmp/opensip-implementation/m1-generator-python-confinement-trial-01/work/code/runtime/schema.ts'` | 0 |
| nonEmptyOutputRoot | 1 | ['stale.json'] | `prepare-inputs: PrepareInputsError: output root is not empty` | 0 |
| undeclaredExec | 71 | [] | `sandbox-exec: execvp() of '/bin/sh' failed: Operation not permitted` | 0 |
| launcherStubExec | 71 | [] | `sandbox-exec: execvp() of '/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14' failed: Operation not permitted` | 0 |

canary unchanged: True; forbidden outside paths absent: {"/private/tmp/opensip-python-confinement-forbidden": true, "/private/var/tmp/opensip-python-confinement-forbidden": true, "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/opensip-python-confinement-forbidden.py": true, "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/__pycache__/opensip-python-confinement-forbidden.pyc": true}

## Pinned interpreter grants

3.14.6 (main, Jun 10 2026, 10:03:53) [Clang 21.0.0 (clang-2100.0.123.102)]

- executable `/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python` `0c9a985712bb1235d8fe474a6a99810dc118bcae0dfb429a237aac0c907fa3af`
- library `/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Python` `696ffa2cf9562522c387f7c2b3a990ef67e574df2d921822fe310ea35587cce0`
- `collections/__init__.py` `dbd563752a57c6633b7566b1e9c95bc8ea81df1a1d213b23f61c5335424e5af5`
- `contextlib.py` `c1e0d67b2007de11ae93cd36cf6faf38d9ab32656a832d592a49325eec579f96`
- `copyreg.py` `6376eb5722806396f5842997ac18add369ea9ac3ff4fcfe1460c41a088cac425`
- `encodings/__init__.py` `2b708410495acf12a6fad9d2de928dd89e567537c253eaa2b51aaae578e96c59`
- `encodings/aliases.py` `1ee993f8eb4986999b6501381e53947be9a04443626cb48b4190bcff2e87d3b4`
- `encodings/utf_8.py` `ba0cac060269583523ca9506473a755203037c57d466a11aa89a30a5f6756f3d`
- `enum.py` `fd23a7598fa1104ef892abcd4154d3627283e6361eb7a91cd11dc4a7b6fb3a93`
- `fnmatch.py` `ce582bc266922e4c682e2a85d72095124430a6bf58716c6f2537103480eae742`
- `functools.py` `9db56d38172c4c9e689b21cc58c8538008b09d86b682faf4dd193b529cdd79d5`
- `glob.py` `2f0e12f02f0223681ba92976d3c68d3638a805ddc18240e5ac4d47e2d3dcdde4`
- `json/__init__.py` `2dd10f1bf4c9ea5478e589216805e7f279d0e4bce134a19efa297404fb87407d`
- `json/decoder.py` `302ce57cb6f411122d7ef2ad2997c1fc0f184849fab3f1f585752f18f2195c73`
- `json/encoder.py` `d68a4d04d2cfd95897498307f29349058b42c3f48ea6aa6739714a09200a7d01`
- `json/scanner.py` `572958017eae8842eeddd0e3d18d3c56cc0a197348224915e1d87ce937841764`
- `keyword.py` `18c2be738c04ad20ad375f6a71db34b3823c7f40b0340f5294d0e89f3c9b093b`
- `operator.py` `a9f9910965c31f841caad0447ee47299ac539a371422aefe200c86c60f3b4697`
- `pathlib/__init__.py` `042a4d0a5e1ef66778daa86dc269af205bd42d06e793e53d8b99dff4c45928ca`
- `pathlib/_os.py` `61e844988e54bdf47c0b11ad2b3fd961f058bb370793428f4c6868bd40cab6f2`
- `re/__init__.py` `741a9de729ed8207bfa19db990f8826f1bf3661f33d0970a80c08cd1338ebc35`
- `re/_casefix.py` `1b12d9136f23db6c3f6f26053fefc15ca964b886838c7b9c1fabf8d2efc1e5c8`
- `re/_compiler.py` `d49f30cf9a1dbae33b200ed8befd9d0ce3ac612783a10ac35196536f98923e91`
- `re/_constants.py` `42253b3181b81aad6c46392f44a0ab26dcfa31feea411296f43ba16616a1ab0b`
- `re/_parser.py` `e57bd194a2d42398355ae7c1ccc2ddfb78421dd431eb81e3809dbe8ca9057dc4`
- `reprlib.py` `b04872e10d76252e44eae50cc785eb0fe478491afc4d7f0825a93f82b2eaba5f`
- `types.py` `8c54d3d5ffc1d1204237e6c69b25c27c7b05b483128f185eeed9ba7ef2229ac2`
- `lib-dynload/_json.cpython-314-darwin.so` `de2ac2f4cf406cf42b4ebeb210789c902121763503ad5f7510897a1dc969db62` links ['/usr/lib/libSystem.B.dylib']
- `lib-dynload/fcntl.cpython-314-darwin.so` `0a54b8fc819837d545ee95da563421303e0cfaae73c5a4881ef56d32da3d667d` links ['/usr/lib/libSystem.B.dylib']
- `lib-dynload/grp.cpython-314-darwin.so` `1db91321c25d305b7082a3d2c9bba6d933aeb817723ffcdcef94ebcc3757ce46` links ['/usr/lib/libSystem.B.dylib']

directories (listing only): `/`, `/collections/`, `/encodings/`, `/json/`, `/lib-dynload/`, `/pathlib/`, `/re/`

built-in/frozen/not-found: {"_io": "built-in", "marshal": "built-in", "posix": "built-in", "_frozen_importlib_external": "frozen", "time": "built-in", "zipimport": "frozen", "_codecs": "built-in", "codecs": "frozen", "_signal": "built-in", "_types": "built-in", "_sre": "built-in", "_abc": "built-in", "abc": "frozen", "_collections_abc": "frozen", "itertools": "built-in", "_operator": "built-in", "_collections": "built-in", "_functools": "built-in", "_stat": "built-in", "stat": "frozen", "errno": "built-in", "genericpath": "frozen", "posixpath": "frozen", "os": "frozen", "io": "frozen", "_winapi": "not-found", "nt": "not-found", "ntpath": "frozen", "pwd": "built-in"}
