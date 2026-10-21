# OWNPAT-CBR-R1-RF-1 correction

The rejected round remains unchanged. This revision changes no runtime wrapper, postchecker, frozen binding, tool, authority, interpreter, method, population, disclosure allowance or main commit. It adds inspectable pure control source, full synthetic receipt and sequence vectors, expected and observed outputs, source/vector/AST SHA-256 provenance and the successful owning-lane execution log.

`check_receipt_decisions.py` compiles only the actual receipt_ready function and actual blind loop, ordinary loop and eligibility assignment extracted from the hash-pinned wrapper AST. It never imports the wrapper. The branch controls replace subprocess and path operations with in-memory fakes. Fifteen receipt predicate cases and fifteen actual-branch cases check discovery/companion invocation counts and order, stop-on-error at every ordinary step and final eligibility. The observed synthetic calls are shown per case; real blind invocations are zero.

Reproduction (pure synthetic control, no corpus access): run the pinned Python with -I -B, check_receipt_decisions.py and a new results JSON path. This is explicitly allowed for the correction review; neither blind mode nor postchecker is permitted.
