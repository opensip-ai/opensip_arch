# Proposed publication failure reference78

315 stage/error/boundary cases and two synthetic allowed rename-EIO target outcomes. The retained primary reference promises old target preservation for all EIO/rename failures; POSIX excludes EIO from that guarantee. Proposal retains exact failure stage/errno and treats rename EIO/unknown plus every post-replacement barrier failure as indeterminate. Private staging cleanup is separate. Existing public I/O codes are reused; full selected-contract/reference reconciliation and independent review remain.

Initial draft also treated lost operation-class labels at rename as known non-EIO; beforeimage/280-case result retained, corrected before freeze to require a captured non-EIO error explicitly. No actual host kernel/disk fault, power-loss or hardware qualification was performed. Mechanism implementation/tests are separate.
