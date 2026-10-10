"""Throwaway SM13 accounting of supplied semantic values; not schema/admission.

Worker must supply recursively validated actual candidates and exact envelopes.
No fact production, key selection, completeness, or source authority is supplied.
"""
import hashlib
import unicodedata

UINT64_MAX = 2**64 - 1
MAX_CANDIDATES = 1_000_000
MAX_SPOOL = 2**30
MAX_PAYLOAD = 2**30
MAX_FRAMES = 1_000_000
MAX_FRAME_PAYLOAD = 2**26

def checked_add(a, b, maximum):
    if any(type(n) is not int or not 0 <= n <= UINT64_MAX for n in (a, b, maximum)):
        raise ValueError('invalid unsigned accounting operand')
    if b > UINT64_MAX - a or a + b > maximum:
        raise ValueError('accounting bound')
    return a + b

def encode(value):
    def head(major, n):
        if type(n) is not int or not 0 <= n <= UINT64_MAX:
            raise ValueError('uint64')
        if n < 24:
            return bytes([(major << 5) | n])
        for width, additional in ((1,24),(2,25),(4,26),(8,27)):
            if n < 1 << (8 * width):
                return bytes([(major << 5) | additional]) + n.to_bytes(width, 'big')
    if value is None:
        return b'\xf6'
    if type(value) is bool:
        return b'\xf5' if value else b'\xf4'
    if type(value) is int:
        return head(0, value)
    if type(value) is str:
        if unicodedata.normalize('NFC', value) != value:
            raise ValueError('non-NFC text')
        raw = value.encode('utf8', errors='strict')
        return head(3, len(raw)) + raw
    if type(value) is bytes:
        return head(2, len(value)) + value
    if type(value) is list:
        return head(4, len(value)) + b''.join(encode(x) for x in value)
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise ValueError('non-text key')
        pairs = [(encode(key), encode(item)) for key,item in value.items()]
        pairs.sort(key=lambda row: (len(row[0]), row[0]))
        return head(5,len(pairs)) + b''.join(key+item for key,item in pairs)
    raise ValueError('outside native CBOR data model')

class Observations:
    def __init__(self):
        self.candidates = self.spool_bytes = self.payload_bytes = self.frames = 0

    def candidate_entry(self, analysis_ordinal, stage_id, candidate):
        # Value encoding is not recursive closed-schema validation.
        entry = encode({'analysisOrdinal': analysis_ordinal,
                        'stageId': stage_id, 'candidate': candidate})
        count = checked_add(self.candidates, 1, MAX_CANDIDATES)
        size = checked_add(self.spool_bytes, len(entry), MAX_SPOOL)
        self.candidates, self.spool_bytes = count, size
        return entry

    def response_frame(self, exact_envelope):
        payload = encode(exact_envelope)
        if len(payload) > MAX_FRAME_PAYLOAD:
            raise ValueError('frame payload bound')
        total = checked_add(self.payload_bytes, len(payload), MAX_PAYLOAD)
        count = checked_add(self.frames, 1, MAX_FRAMES)
        frame = len(payload).to_bytes(8,'big') + hashlib.sha256(payload).digest() + payload
        self.payload_bytes, self.frames = total, count
        return frame

    def census_volume(self, exact_census):
        # Caller owes closed schema, complete symbol population, sorting, extent.
        return len(encode(exact_census))
