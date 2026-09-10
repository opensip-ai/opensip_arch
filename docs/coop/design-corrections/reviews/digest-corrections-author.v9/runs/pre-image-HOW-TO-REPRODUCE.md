`runs/pre-image/` held a copy of the work tree with the two FROZEN v10 owned files placed back in,
so the pre-image model could resolve the files it imports and root owns (canonical.py and the schema
documents). It has been pruned rather than shipped, because a recursive repository copy does not
belong in a handoff artifact.

Reproduce with:

    cp -R <work>/docs <sandbox>/docs
    cp digest-corrections-author.v9/PRE-identity-model.py  <sandbox>/docs/coop/design-corrections/foundation/identity-model.py
    cp digest-corrections-author.v9/PRE-check-identity.py  <sandbox>/docs/coop/design-corrections/foundation/check-identity.py

The two PRE files are retained verbatim beside this note and are the ONLY files that differ from the
work tree:
  PRE-identity-model.py  sha256 f200232b9cccc06f280db284280932646baaae050418521ee3f03eafece1b226
  PRE-check-identity.py  sha256 a7f7d393d3b1c9284ce1109b0458b9cb63708794c371365be22e8c5afc4f053c
Both match frozen v10 and my released v8.
