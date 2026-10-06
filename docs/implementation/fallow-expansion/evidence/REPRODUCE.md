# Reproduce frozen author subjects

The accepted builders intentionally use the pre-expansion selected lock. After binding, do not rebuild them against a lock containing their own insertion or supersession. Retrieve the recorded baseline first:

```sh
git -C /Users/sb/code/opensip-ai/opensip show f5f5b4d20eca34ab2312b3ffc141c378da326afe:design-lock.json > /tmp/opensip-fx-author-base-lock.json
cd /Users/sb/code/opensip-ai/opensip_arch
python3 -I -B docs/implementation/fallow-expansion/capacity-r2/build.py --lock /tmp/opensip-fx-author-base-lock.json --check
python3 -I -B docs/implementation/fallow-expansion/components-r2/build.py --lock /tmp/opensip-fx-author-base-lock.json --check
python3 -I -B docs/implementation/fallow-expansion/components-r2/check.py --deps /tmp/opensip-fx-python/python-packages
```

The dependencies were provisioned from the product's pinned offline wheel manifest; that `/tmp` directory is session-local. The accepted subjects and actual review/assent byte pins remain authoritative. Reference fixture success is design evidence, not product qualification.

For selected design integrity, run from the product checkout:

```sh
python3 -I -B tools/verify_design.py --architecture ../opensip_arch
```

Schema generation/materialization is the separate FX-CAP-M implementation unit. This binding does not declare generated implementation sources current under the widened schema.
