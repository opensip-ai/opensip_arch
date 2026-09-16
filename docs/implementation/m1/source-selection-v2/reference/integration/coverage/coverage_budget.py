"""Bind source-addressed coverage to the existing shared-prefix algorithm.

Reference integration only. Caller owns the admitted source snapshot and the
shared panel budget. All bytes of source/descriptor/provenance wrapping count.
The total remains the full source count even when hydration stops at the item cap.
"""
import copy


def bind(read_unit, model, reserved, placement):
    raw = read_unit('report-projection', 'report_model.py')
    text = raw.decode()
    start = text.index('        elif name == "evidence":')
    end = text.index('        elif name == "graph":', start)
    old = text[start:end]
    assert old.count('"coverageId": src["coverageId"]') == 1
    assert old.count('len(entries)') == 2
    new = old.replace('"coverageId": src["coverageId"]', '"source": src["source"]')
    new = new.replace('len(entries)', 'src["total"]')
    new = new.replace('            prefix(', '''            if type(src["total"]) is not int or src["total"] < 0:
                raise ValueError("coverage source total")
            if type(item_cap) is not int or not 0 <= item_cap <= 3956:
                raise ValueError("coverage item cap")
            if len(entries) != min(src["total"], item_cap):
                raise ValueError("coverage hydration prefix incomplete")
            prefix(''')
    changed = (text[:start] + new + text[end:]).encode()
    def selected(unit, name):
        if unit == 'report-projection' and name == 'report_model.py': return changed
        return read_unit(unit, name)
    return placement['parent'].bind(selected, model, reserved, placement['joint'])


def source_from_projection(projection, item_cap):
    """Use the already admitted owner's exact capped prefix, not an object scan.

    This shape is an internal host input, not an untrusted public producer API.
    The original source owner's complete Run admission must have succeeded.
    """
    if type(item_cap) is not int or not 0 <= item_cap <= 3956:
        raise ValueError('coverage item cap')
    total = projection['entriesProjection']['total']
    entries = projection['entries']
    if type(total) is not int or total < 0 or len(entries) != min(total, item_cap):
        raise ValueError('coverage hydration prefix incomplete')
    return copy.deepcopy({'source': projection['source'], 'entries': entries,
                          'total': total, 'cap': item_cap})
