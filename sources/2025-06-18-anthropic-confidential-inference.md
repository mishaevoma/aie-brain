---
type: source
title: "Confidential Inference via Trusted Virtual Machines"
author: "Anthropic"
publisher: "Anthropic"
url: https://www.anthropic.com/research/confidential-inference-trusted-vms
published: 2025-06-18
ingested: 2026-11-17
kind: article
read: full
concepts: [sandboxing-and-permissions]
---

# Confidential Inference via Trusted Virtual Machines

**In one line:** keep prompts and model weights encrypted everywhere except inside one small, attested component, and release decryption keys only to environments that prove what code they run.

## What it says

- Two goals: protect frontier model weights from capable attackers, and be able to prove that user data stays private.
- Cleartext user data appears in two places: the **API Server** (tokenizes, runs request logic) and the **Inference Server** (runs the model on accelerators). Only the Inference Server touches weights; the post covers only it.
- Because many accelerators lack confidential-computing support, a small trusted **model loader and invoker** sits in front of the hardware. It alone decrypts inputs, drives the accelerator and encrypts outputs. The rest of the Inference Server is treated as untrusted and can change freely.
- The loader runs in its own hypervisor-isolated VM, appears as a model-agnostic "virtual accelerator", and runs only programs signed by Anthropic's secure CI server, which implies review by multiple engineers.
- The environment needs encrypted, hardware-isolated memory, debugging disabled, and cryptographic proof of the running code. Encrypted memory shared with accelerators is not mature yet, so Anthropic currently trusts the compute provider for physical and hypervisor security.
- A **TPM** is the root of trust: it measures each boot stage into an attestation hash. A **keyserver** verifies it and alone decides whether to release keys. Independent third-party keyservers are being explored.
- Possible future layers: egress bandwidth limits on servers holding cleartext weights, and requiring a safety classifier's signature before inference. Chipmakers are urged to put a root of trust on the accelerator itself (NVIDIA H100 cited).

## What to do with it

- Shrink the code that can see plaintext to one small, separately reviewed component.
- Gate secret release on attestation, not on network location or operator trust.
- Allow only signed, reviewed builds inside the trust boundary.
- Where hardware cannot guarantee something, record which party you are trusting.

## Terms

- **Confidential Inference** — processing encrypted requests and weights so they are readable only in servers that can prove they are trustworthy.
- **virtual accelerator** — the minimal trusted loader VM that fronts the real accelerator.
- **keyserver** — verifies attestation and decides whether to release keys.

## Caveats

- An early research sketch, not a product; Anthropic says it is building it for internal use. Written with Pattern Labs; the linked full report was not read.
- Mid-2025 hardware state; accelerator support may have moved on.
- About provider-side infrastructure, not agent sandboxing; for that see the Anthropic notes of 2025-10-20 and 2026-05-25.
