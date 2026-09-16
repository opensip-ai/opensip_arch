# Reproduction

Python: `/Users/sb/.local/bin/python3.12 -I -B` (3.12.13, Unicode 15.0.0). Not the metadata-reference-env 3.14/UCD 16 interpreter.

Frozen portable gate:

```
python3.12 -I -B \
  $ARCH/docs/implementation/m2/predicate-matching-reference-selection-v1/evidence/check-matching.py \
  --architecture $ARCH
```

Independent declarative gate (star before literal equality; ASCII ordinal `0|[1-9][0-9]*`; effective workflow predecessor includes source-selection-v2 line 380):

```
python3.12 -I -B independent_check.py
```

Both: 609978 glob pairs, 0 mismatches vs law, 1732 changed; 23 ASCII / 805 Unicode address controls, 804 changed; 7 emitted round-trips. Core JSON fields equal `evidence/result.json` `a73be80bf1aac81f91b71d4e013d5b785c359da1d65d2f307b027848efa0e533`.

Local helper evidence only. No full Run, replay, or product execution.
