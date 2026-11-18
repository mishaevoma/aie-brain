---
type: source
title: "Sandbox persistence"
author: "E2B"
publisher: E2B Docs
url: https://docs.e2b.dev/sandbox/persistence
published: 2026-11-12
ingested: 2026-11-17
kind: docs
read: full
concepts: [durable-execution]
---

# Sandbox persistence

**In one line:** An E2B pause saves disk and memory and a resume restores running processes in about a second, but client connections drop, and a hung sandbox, a backlogged node or a filesystem-only snapshot can each end in a reboot from disk with memory lost.

## What it says

- **Pages covered.** "Sandbox persistence" and its sub-page "Filesystem-only snapshots".
- **Pause and resume.** By default a pause takes a full snapshot, filesystem plus memory, so `connect()` later restores files, running processes and loaded variables. Stated speeds: about 4 seconds per 1 GiB of RAM to pause, about 1 second to resume.
- **Connections.** A paused sandbox's services are unreachable and their clients are disconnected. After a resume, clients must reconnect.
- **Limits.** A sandbox may run unpaused for 24 hours on the Pro tier and 1 hour on the Hobby tier; a pause and resume resets this. A paused sandbox is retained indefinitely until killed, with no time-to-live and no tier mentioned. At timeout the default is to kill; auto-pause is set at creation.
- **Filesystem-only.** `mode: 'filesystem'` on a pause, an auto-pause or `createSnapshot()` keeps the disk and drops memory. It is smaller and quicker to take, but using it is a reboot of several seconds with processes gone. It cannot be woken by inbound traffic, and creating one returns a 400 unless enabled for the project.
- **Backlogged node.** While the node has not finished the sandbox's previous snapshot, a pause is refused with HTTP 503 and nothing is lost (a 500 where this has not rolled out).
- **Hung sandbox.** Before a snapshot, E2B checks that `envd`, its in-sandbox daemon, answers a health check. If it does not, a default pause proceeds but flags the snapshot, and a filesystem-only pause, fork or snapshot is refused. A flagged sandbox cannot resume with memory: `connect()` returns HTTP 409 until called with `onResume: 'reboot'`, which restores files flushed before the pause. Processes and memory are lost, and unflushed writes may be. `strict: true` refuses the pause instead.
- **Auto-pause.** If the node keeps refusing for about two minutes past the timeout, the sandbox is paused filesystem-only and memory is lost, which the docs say never happens normally. A sandbox still unresponsive after that wait is paused with memory and flagged.

## What to do with it

- Set `onTimeout` to pause; the default kills the sandbox.
- Flush state to disk before pausing and keep services restartable: several paths end in a reboot.
- Retry a pause on 503, reboot when a resume raises `GuestUnresponsiveError`, and read `envdUnresponsiveAtPause` or the pause event's `pause_mode` to learn that memory was lost.
- After a reboot, pause again, or the sandbox reverts to the flagged snapshot at timeout.

## Terms

- **Full snapshot** — filesystem and memory, restored in place.
- **Filesystem-only snapshot** — disk only; any use of it is a reboot.

## Caveats

- No publication date: the date above is the persistence page's last-modified date, and the sub-page's is 16 November 2026.
- Vendor documentation. Timings are approximate, with no conditions given, and no price for a paused sandbox. Behaviour depends on region rollout and SDK version (2.48.0, 2.55.0, 2.63.0).
- Compare the disk-snapshot checkpoint in [SBD: We Have a Filesystem at Home](2026-10-22-fly-sprites-block-device.md).
