"""Q0 r13 §9.5/QD-27 sample accounting component of K1c.

Consumes driver-supplied slot evidence; runs no workload and attests no
settlement, leaf, operational record, baseline, D12 lane or qualification.
The driver/envelope validator must establish those joins independently.
"""
from canonical import Refusal, canonical


BOTH_NULL = frozenset({
    "run-failed", "timeout", "cgroup-not-empty", "settlement-failed",
})
MEMORY_NULL = frozenset({
    "cgroup-unavailable", "cgroup-v1-only", "cgroup-no-delegation",
    "cgroup-escape-unprevented", "cgroup-isolation-unverified",
    "cgroup-read-failed", "memory-peak-unverified",
    "memory-peak-unavailable-platform",
})
ELAPSED_NULL = frozenset({"settlement-unverified-platform"})
EVIDENCE_ONLY = frozenset({"record-missing", "record-invalid"})
RUN_REASONS = BOTH_NULL | MEMORY_NULL | ELAPSED_NULL | EVIDENCE_ONLY


def _positive_or_null(value):
    if value is not None and (type(value) is not int or
                              not 1 <= value <= 2**64 - 1):
        raise Refusal("POSITIVE_UINT64_OR_NULL_REQUIRED")


def _slot(value):
    if type(value) is not dict or set(value) != {"kind", "index"}:
        raise Refusal("RUN_SLOT_SHAPE")
    kind, index = value["kind"], value["index"]
    if type(kind) is not str or kind not in {"priming", "warmup", "measured"}:
        raise Refusal("RUN_SLOT_KIND")
    if type(index) is not int or not 0 <= index <= {
            "priming": 0, "warmup": 2, "measured": 6}[kind]:
        raise Refusal("RUN_SLOT_INDEX")
    return kind, index


def summarize_slots(reset, slots):
    """Validate a full batch's slots and return its sample-accounting fields.

    Internal slot rows have `slot` and `reasons`; measured rows additionally
    have elapsedNanos, cgroupMemoryPeakBytes and rootReapedElapsedNanos.
    Warmup/priming rows carry no numeric samples. Values must already match
    the reason mapping exactly; inconsistent evidence is refused, never fixed.
    Root-reaped time is informational, nullable even on a failed macOS launch.
    Output `incomplete` does not determine complete-row budget/baseline status.
    """
    if type(reset) is not str or reset not in {"cold", "warm"}:
        raise Refusal("RESET_REQUIRED")
    if type(slots) is not list:
        raise Refusal("SLOT_ARRAY_REQUIRED")
    canonical(slots)
    expected = {("warmup", i) for i in range(3)} | {
        ("measured", i) for i in range(7)}
    if reset == "warm":
        expected.add(("priming", 0))
    if len(slots) != len(expected):
        raise Refusal("EXACT_SLOT_COVERAGE_REQUIRED")
    indexed = {}
    reason_rows = []
    for row in slots:
        if type(row) is not dict or "slot" not in row:
            raise Refusal("SLOT_ROW_SHAPE")
        key = _slot(row["slot"])
        fields = {"slot", "reasons"}
        if key[0] == "measured":
            fields |= {"elapsedNanos", "cgroupMemoryPeakBytes",
                       "rootReapedElapsedNanos"}
        if set(row) != fields:
            raise Refusal("SLOT_ROW_SHAPE")
        if key not in expected or key in indexed:
            raise Refusal("EXACT_SLOT_COVERAGE_REQUIRED")
        reasons = row["reasons"]
        if (type(reasons) is not list or any(type(r) is not str or
                r not in RUN_REASONS for r in reasons) or
                len(reasons) != len(set(reasons))):
            raise Refusal("UNIQUE_NAMED_RUN_REASONS_REQUIRED")
        reasons = frozenset(reasons)
        if key[0] == "measured":
            elapsed, peak, root = (row[k] for k in (
                "elapsedNanos", "cgroupMemoryPeakBytes",
                "rootReapedElapsedNanos"))
            for value in (elapsed, peak, root):
                _positive_or_null(value)
            if ((elapsed is None) != bool(reasons & (BOTH_NULL | ELAPSED_NULL)) or
                    (peak is None) != bool(reasons & (BOTH_NULL | MEMORY_NULL))):
                raise Refusal("SAMPLE_REASON_NULL_MISMATCH")
            if root is not None and not reasons & ELAPSED_NULL:
                raise Refusal("ROOT_REAPED_TIME_REQUIRES_UNVERIFIED_SETTLEMENT")
            if root is None and reasons & ELAPSED_NULL and "run-failed" not in reasons:
                raise Refusal("ROOT_REAPED_TIME_REQUIRED_UNLESS_RUN_FAILED")
        indexed[key] = row
        if reasons:
            reason_rows.append({"slot": dict(row["slot"]),
                                "reasons": sorted(reasons, key=canonical)})
    elapsed = [indexed[("measured", i)]["elapsedNanos"] for i in range(7)]
    peaks = [indexed[("measured", i)]["cgroupMemoryPeakBytes"] for i in range(7)]
    roots = [indexed[("measured", i)]["rootReapedElapsedNanos"] for i in range(7)]
    return {
        "warmupRuns": 3,
        "elapsedNanos": elapsed,
        "medianElapsedNanos": None if None in elapsed else sorted(elapsed)[3],
        "cgroupMemoryPeakBytes": peaks,
        "maxCgroupMemoryPeakBytes": None if None in peaks else max(peaks),
        "rootReapedElapsedNanos": roots,
        "slotReasons": sorted(reason_rows, key=canonical),
        "incomplete": bool(reason_rows),
    }
