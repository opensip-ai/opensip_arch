"""Inert replay of already observed candidate events; not an acquisition decoder."""
from dataclasses import dataclass
from enum import Enum

GIB = 1024**3
class Field(Enum):
    SOURCES = "sources"
    FILES = "files"
    CONTENT = "content"
@dataclass(frozen=True)
class Bound:
    field: Field
    observed: int
    limit: int
@dataclass(frozen=True)
class FileEvent:
    # Number of already observed whole-file events, not a tar-header declaration.
    # Grouping is used solely by symbolic authoring controls.
    count: int
    bytes_each: int
@dataclass(frozen=True)
class Candidate:
    key: tuple[str, str, str]
    events: tuple[FileEvent, ...]
    # These labels are supplied observations; they grant no admission/activation.
    admitted: bool
    activated: bool

def checked(candidates):
    candidates = tuple(candidates)
    if len({c.key for c in candidates}) != len(candidates):
        raise ValueError("duplicate declared candidate tuple")
    for candidate in candidates:
        if len(candidate.key) != 3 or any(type(v) is not str for v in candidate.key):
            raise ValueError("authoring tuple shape")
        if type(candidate.admitted) is not bool or type(candidate.activated) is not bool:
            raise ValueError("authoring labels are booleans")
        for event in candidate.events:
            if type(event.count) is not int or type(event.bytes_each) is not int or event.count < 0 or event.bytes_each < 0:
                raise ValueError("authoring quantities are nonnegative integer observations")
    return candidates

def replay_acquisition(candidates):
    candidates = checked(candidates)
    ordered = sorted(candidates, key=lambda c: tuple(v.encode("utf-8") for v in c.key))
    if len({c.key for c in ordered}) != len(ordered):
        raise ValueError("duplicate declared candidate tuple")
    sources = files = content = 0
    for candidate in ordered:
        sources += 1
        if sources > 16384:
            return Bound(Field.SOURCES, sources, 16384)
        for event in candidate.events:
            if event.count < 0 or event.bytes_each < 0:
                raise ValueError("negative authoring event quantity")
            # The first file event that crosses either count or content is known
            # arithmetically. A simultaneous crossing uses files before content.
            files_left = 4_000_000 - files
            bytes_left = 32 * GIB - content
            file_cross = files_left + 1 if event.count > files_left else None
            content_cross = bytes_left // event.bytes_each + 1 if event.bytes_each and event.count * event.bytes_each > bytes_left else None
            crossings = [n for n in [file_cross, content_cross] if n is not None]
            if crossings:
                n = min(crossings)
                files += n
                content += n * event.bytes_each
                if files > 4_000_000:
                    return Bound(Field.FILES, files, 4_000_000)
                return Bound(Field.CONTENT, content, 32 * GIB)
            files += event.count
            content += event.count * event.bytes_each
    return sources, files, content

def final_population(candidates):
    # Exact logical totals of labelled admitted+activated, non-path candidates.
    # Path packages must be excluded by the producer; this replay cannot prove it.
    selected = [c for c in checked(candidates) if c.admitted and c.activated]
    return len(selected), sum(e.count for c in selected for e in c.events), sum(e.count*e.bytes_each for c in selected for e in c.events)

def final_overflow(candidates):
    totals = final_population(candidates)
    # Return all proven field crossings. No unselected multi-field precedence
    # is invented for the one-time final check.
    return tuple(Bound(f,n,limit) for f,n,limit in zip(Field,totals,(4096,1_000_000,8*GIB)) if n>limit)
