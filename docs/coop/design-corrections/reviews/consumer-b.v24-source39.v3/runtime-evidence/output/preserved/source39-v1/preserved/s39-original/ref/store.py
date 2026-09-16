"""One content-addressed store keyed by raw SHA-256 (identity-and-evidence section 3):
raw artifacts, canonical records and H frames live side by side; an object table names the typed
identities. Export is JSON with base64 bytes. Import re-hashes every blob before use."""
import base64
import hashlib
import json

import canonical as K


class Store:
    def __init__(self):
        self.blobs = {}          # hex -> bytes
        self.objects = {}        # typed id -> (domain, frame hex)
        self.labels = {}         # hex -> role label (informational)

    def put_bytes(self, data, label=None):
        h = hashlib.sha256(data).hexdigest()
        prev = self.blobs.get(h)
        if prev is not None and prev != data:
            raise AssertionError("sha256 collision")
        self.blobs[h] = bytes(data)
        if label and h not in self.labels:
            self.labels[h] = label
        return h

    def put_record(self, value, label=None):
        return self.put_bytes(K.C(value), label)

    def put_frame(self, domain, value, label=None):
        fb = K.frame(domain, value)
        h = self.put_bytes(fb, label or ("frame:" + domain))
        return h

    def put_object(self, domain, value, label=None):
        h = self.put_frame(domain, value, label)
        ident = K.PREFIX[domain] + ":" + h
        self.objects[ident] = (domain, h)
        return ident

    def get_bytes(self, h):
        b = self.blobs.get(h)
        if b is None:
            raise K.AdmissionError("EVIDENCE_UNAVAILABLE", h)
        if hashlib.sha256(b).hexdigest() != h:
            raise K.AdmissionError("CAS_DIGEST_MISMATCH", h)
        return b

    def get_record(self, h):
        b = self.get_bytes(h)
        v = K.parse_raw(b)
        if K.C(v) != b:
            raise K.AdmissionError("RECORD_NOT_CANONICAL", h)
        return v

    def get_frame(self, h, allowed):
        return K.parse_frame(self.get_bytes(h), allowed)

    def get_object(self, ident):
        prefix, hx = ident.split(":", 1)
        domain = next((d for d, p in K.PREFIX.items() if p == prefix), None)
        if domain is None:
            raise K.AdmissionError("OBJECT_PREFIX_UNREGISTERED", prefix)
        d, value = self.get_frame(hx, {domain})
        return value

    def export(self, extra=None):
        table = [{"id": i, "domain": d, "frameSha256": h, "frameBytes": len(self.blobs[h])}
                 for i, (d, h) in sorted(self.objects.items())]
        out = {"format": "consumer-b.v24.store.v1",
               "objectTable": table,
               "blobs": {h: base64.b64encode(b).decode('ascii') for h, b in sorted(self.blobs.items())},
               "blobLabels": dict(sorted(self.labels.items()))}
        if extra:
            out.update(extra)
        return out

    @classmethod
    def load(cls, exported):
        s = cls()
        for h, b64 in exported["blobs"].items():
            b = base64.b64decode(b64)
            if hashlib.sha256(b).hexdigest() != h:
                raise K.AdmissionError("EXPORT_BLOB_DIGEST_MISMATCH", h)
            s.blobs[h] = b
        for row in exported["objectTable"]:
            s.objects[row["id"]] = (row["domain"], row["frameSha256"])
        s.labels = dict(exported.get("blobLabels", {}))
        return s
