---
type: source
title: "SBD: We Have a Filesystem at Home"
author: "Daniel Botha"
publisher: Fly.io
url: https://fly.io/blog/sprites-block-device/
published: 2026-10-22
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms]
---

# SBD: We Have a Filesystem at Home

**In one line:** A Sprite's durable state is a disk in a bucket and its checkpoint a snapshot of that disk; Fly.io replaced a first design whose three separately durable stores could disagree, after a cycle test left machines unable to checkpoint.

## What it says

- **What is durable.** A Sprite's disk is rooted in object storage, not in local NVMe: its durable state is roughly a location in a bucket. Unchanged since launch, this lets a Sprite sleep and wake on another server with its files.
- **First design.** A heavily modified JuiceFS held a single file, a 100 GB disk image formatted as ext4 and mounted through a loop device. Its chunks lived in the bucket and its SQLite metadata was made durable by Litestream. Each checkpoint was a copy-on-write clone, mostly a metadata change, listed in a second SQLite database.
- **The weakness.** Chunks, metadata and the checkpoint list were made durable separately and could disagree. The example given: in writeback mode JuiceFS records a chunk in metadata before uploading its bytes, so a machine killed in between leaves metadata naming a missing chunk, and ext4 goes read-only. Restoring a checkpoint does not help, because the clones share the missing chunk.
- **How it was found.** A harness cycled fleets of Sprites through writing, checkpointing, sleeping, waking and restoring, verifying every byte. On 400 JuiceFS-backed Sprites over about 5,000 cycles, a "nonzero number" could never checkpoint again.
- **Replacement.** The Sprites Block Device (SBD) presents a bucket to the kernel as an NBD block device, which the Sprite formats as ext4. Metadata sits in the bucket beside the blocks it describes, with no separate database. A daemon in the Sprite serves reads and writes from a local cache, uploads dirty blocks in the background and flushes when asked.
- **Checkpoint and restore.** A checkpoint is a versioned block-level snapshot of the entire volume, listed in SBD's own catalogue. A restore unmounts the filesystem, rolls the volume back in place and remounts it, at about the cost of a restart.
- **Failing loudly.** Blocks read from object storage are verified against what was written. A Sprite that cannot trust its disk stops, and if SBD dies the whole Sprite restarts.
- SBD is claimed to be more reliable by orders of magnitude. Sprites created before 10/6 can be migrated.

## What to do with it

- Ask what a vendor's checkpoint contains. One that shares storage with the live disk is not a backup.
- Keep one source of truth for persisted state, not stores that must agree.
- Test pause and resume in a loop that verifies bytes, on many machines.

## Terms

- **SBD (Sprites Block Device)** — the layer that exposes a bucket as a block device.

## Caveats

- A vendor's account, October 2026. No figures for reliability or for how many Sprites broke; the corruption story is told as possibly hypothetical.
- Checkpoints and waking are described only in terms of the disk; memory and running processes are not mentioned. This brain's reading: a restore that unmounts the filesystem does not keep them.
- Nothing on blocks not yet uploaded when a machine dies. The case for such machines: [Code And Let Live](2026-01-09-fly-code-and-let-live.md).
