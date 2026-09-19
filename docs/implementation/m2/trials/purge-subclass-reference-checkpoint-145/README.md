# Candidate 145: purge termination subclass guard

Unaccepted reference correction over frozen 142. Actual Claude142 N1 showed that manually constructed Python `dict` subclasses bypassed the completed-observation guard. The two object checks now use `isinstance(..., dict)` so the same pinned-termination refusal applies to plain dictionaries and subclasses. JSON-derived observations retain the same behavior; this is not a general arbitrary-Python-object validator.

Twelve mandatory regression checks cover subclassed termination, subclassed detail, and both, for full and bare disclosure forms in each workflow major. Both independently reverted type checks are detected by the mandatory checker. 377 purge checks and 2,193 workflow checks pass. All existing reference qualification lanes pass with updated source pins; full budgets and unrelated laws are unchanged. Actual independent review is required before selection.

No host effects, pin transaction, deletion, renderer, spool, generated-consumer or cumulative product approval is claimed.
