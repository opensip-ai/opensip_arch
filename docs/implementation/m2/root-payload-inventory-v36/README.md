# Complete root-payload fixture v36

Add one consistently named root-payload-cases.ndjson fixture under security/tests/fixtures. The private61 fixture represents7515 complete root payload checks with17624 pooled nodes. Every input is reconstituted and checked against its original canonical SHA256; accepted output is checked against independent reference metadata/root digests and canonical byte count.227 cases admit. Pooling reduces58,161,875 bytes to4,202,350 without changing an expectation. Each NDJSON line is separately bounded; this file is not one metadata document. Private validated payloads own their bytes but confer no authenticated root-chain/current-trust/operational authority.

419 planned files,20packages.418 inherited rows remain equal by value; parent35 and33/34 are pending actual review. This layout, reference60/58/56/53, private61 source and dependency profile are unaccepted. Four description overrides remain addressed by filepath, not row index.
