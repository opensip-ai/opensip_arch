# Primary-source follow-up for proposed durable APFS volume identity

Apple File System Reference,2020-06-22, https://developer.apple.com/support/apple-file-system/Apple-File-System-Reference.pdf was successfully fetched by the browser. The volume superblock has apfs_vol_uuid; printed page57 describes it as that volume identifier. This is on-disk format documentation, distinct from a restart-scoped device or fsid value. No complete PDF copy is republished here.

Apple published XNU bsd/vfs/vfs_attrlist.c maps ATTR_VOL_UUID to VFS f_uuid and packs the returned uuid_t. The fetched source is pinned separately if available. It is published-source evidence, not a claim the currently installed kernel is this revision. Neither that VFS code nor the file-format document alone proves the private APFS driver's exact mapping or qualifies restart behavior on every OS/filesystem version.

Together with the installed CFURL persistent-volume-UUID documentation and one-host original-descriptor377 sample, these sources support the proposed durable UUID direction as an inference. Actual supported profile mapping and restart/remount/unsupported-volume checks remain qualification work. No native reboot occurred, no raw disk read was performed, and no registry/owner/source has been changed by this source investigation.
