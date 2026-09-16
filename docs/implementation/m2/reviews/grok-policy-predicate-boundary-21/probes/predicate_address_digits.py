"""Probe selected predicate_node_at digit classes. Not product code."""
import json
from pathlib import Path

ID = Path(
    "/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/recognition-derived-reference-selection-v1/reference/identity_model.py"
)


class AdmissionError(ValueError):
    pass


def load_helpers():
    src = ID.read_text()
    start = src.index("def predicate_child_addresses")
    end = src.index("_ADMITTED_PREDICATE_NODES")
    g = {"C": type("C", (), {"AdmissionError": AdmissionError})()}
    exec(src[start:end], g)
    return g["predicate_node_at"], g["predicate_child_addresses"]


def catch(fn):
    try:
        v = fn()
        return {"ok": True, "op": v.get("op"), "n": v.get("n")}
    except AdmissionError as e:
        return {"ok": False, "named": True, "msg": str(e)}
    except Exception as e:
        return {"ok": False, "named": False, "type": type(e).__name__, "msg": str(e)}


def main():
    node_at, _ = load_helpers()
    # and of two exists leaves
    root = {
        "op": "and",
        "operands": [
            {"op": "exists", "relation": "file", "minResolution": "enumerated"},
            {"op": "exists", "relation": "package", "minResolution": "manifest-declared"},
        ],
    }
    cases = {
        "p": "p",
        "p.0": "p.0",
        "p.1": "p.1",
        "p.01": "p.01",
        "p.٠٠": "p.\u0660",  # arabic 0 as single segment after p. wait that's p.٠
        "p.arabic_0": "p.\u0660",
        "p.arabic_1": "p.\u0661",
        "p.arabic_01": "p.\u0660\u0661",
        "p.arabic0_ascii1": "p.\u06601",
        "p.ascii0_arabic1": "p.0\u0661",
        "p.fullwidth_0": "p.\uff10",
        "p.fullwidth_1": "p.\uff11",
        "p.fullwidth_01": "p.\uff10\uff11",
        "p.fullwidth0_ascii1": "p.\uff101",
        "p.superscript_0": "p.\u2070",
        "p.superscript_1": "p.\u00b9",
        "p.superscript_2": "p.\u00b2",
        "p.superscript_01": "p.\u2070\u00b9",
    }
    out = {k: catch(lambda a=a: node_at(root, a)) for k, a in cases.items()}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
