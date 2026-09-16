"""One content-addressed store keyed by raw SHA-256, plus a typed object table.

identity-and-evidence section 3: "Because H(D, X) is SHA256 of the framed preimage, ONE
content-addressed store keyed by raw SHA256 retains all three of raw artifacts, canonical
records and H identities: the object retained under a bare-hex h-identity digest is the
exact H preimage frame."

So: put_blob(bytes) for raw artifacts, put_record(obj) for canonical-record preimages,
put_framed(domain, obj) for h-identity preimage frames. A digest DECLARATION alone does
not retain its bytes -- only a put does.
"""
import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K


class Store:
    def __init__(self):
        self.blobs = {}        # sha256hex -> bytes
        self.objects = {}      # typed id (e.g. "plan2:<hex>") -> parsed record
        self.meta = {}         # typed id -> {'domain':..., 'frameDigest':...}
        self.labels = {}       # free label -> typed id or digest, for human reading

    # -------- raw artifacts
    def put_blob(self, b, label=None):
        d = K.raw_sha256(b)
        if d in self.blobs and self.blobs[d] != b:
            raise RuntimeError('CAS collision on %s' % d)
        self.blobs[d] = b
        if label:
            self.labels[label] = d
        return d

    def get_blob(self, d):
        return self.blobs.get(d)

    # -------- canonical records (raw SHA-256 of C(record))
    def put_record(self, obj, label=None):
        b = K.C(obj)
        return self.put_blob(b, label)

    # -------- h-identity frames
    def put_framed(self, domain, obj, label=None):
        frame = K.h_frame(domain, obj)
        d = self.put_blob(frame)
        tid = K.PREFIX[domain] + ':' + d if domain in K.PREFIX else domain + ':' + d
        self.objects[tid] = obj
        self.meta[tid] = {'domain': domain, 'frameDigest': d}
        if label:
            self.labels[label] = tid
        return tid

    def put_native_framed(self, domain, obj, label=None):
        """Native H domains carry `sha256:<H hex>` text and a bare-hex suffix form."""
        frame = K.h_frame(domain, obj)
        d = self.put_blob(frame)
        tid = domain + '#' + d
        self.objects[tid] = obj
        self.meta[tid] = {'domain': domain, 'frameDigest': d}
        if label:
            self.labels[label] = tid
        return d

    def suffix(self, tid):
        return tid.split(':', 1)[1] if ':' in tid else tid

    # -------- export / reload
    def export(self, path, extra=None):
        doc = {
            'standing': ('Exact exported object table plus ALL referenced retained blob/frame '
                         'bytes keyed by raw SHA-256, base64 for transport. Sufficient for '
                         'independent root admission of these exact bytes.'),
            'objectTable': {k: {'domain': self.meta[k]['domain'],
                                'frameDigest': self.meta[k]['frameDigest'],
                                'record': v}
                            for k, v in sorted(self.objects.items())},
            'labels': dict(sorted(self.labels.items())),
            'blobs': {d: base64.b64encode(b).decode('ascii')
                      for d, b in sorted(self.blobs.items())},
            'blobCount': len(self.blobs),
            'objectCount': len(self.objects),
            'totalBlobBytes': sum(len(b) for b in self.blobs.values()),
        }
        if extra:
            doc.update(extra)
        with open(path, 'w') as f:
            json.dump(doc, f, indent=1, sort_keys=False)
        return doc

    @classmethod
    def load(cls, path):
        doc = json.load(open(path))
        s = cls()
        for d, b64 in doc['blobs'].items():
            b = base64.b64decode(b64)
            if K.raw_sha256(b) != d:
                raise RuntimeError('exported blob key does not re-hash: %s' % d)
            s.blobs[d] = b
        for tid, row in doc['objectTable'].items():
            s.objects[tid] = row['record']
            s.meta[tid] = {'domain': row['domain'], 'frameDigest': row['frameDigest']}
        s.labels = doc.get('labels', {})
        return s, doc
