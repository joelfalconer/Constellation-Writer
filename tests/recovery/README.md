# Failure Injection Suite

Status: **candidate scenario suite, runtime execution pending issue #6**.

The suite defines controlled failure points for atomic writes, recovery buffers, cache rebuild, conflict preservation, snapshot restore, and multi-file mutation recovery. A future harness must emit receipts for every scenario rather than simply assert process exit codes.

Hard invariant: no injected failure may silently destroy acknowledged canonical text.
