---
type: source
title: "AI Identity Management System"
author: "Pieter Kasselman, Jean-François Lombardo, Yaroslav Rosomakho, Brian Campbell, Nick Steele, Aaron Parecki"
publisher: IETF WIMSE Working Group
url: https://datatracker.ietf.org/doc/html/draft-ietf-wimse-aims
published: 2026-11-02
ingested: 2026-11-17
kind: docs
read: full
concepts: [agent-identity]
---

# AI Identity Management System

**In one line:** An IETF draft that treats an agent as a workload: one stable identifier, short-lived credentials bound to it, authority obtained through OAuth 2.0 grants, and no approval click in the agent's own interface counted as authorisation.

## What it says

- **Scope.** No new protocol: it composes WIMSE, SPIFFE, OAuth 2.0 and OpenID specifications into a model it calls AIMS.
- **Identifier.** An agent MUST have exactly one WIMSE identifier, a URI unique within a trust domain, which MAY be a SPIFFE ID. It outlives its credentials and is never reassigned after retirement.
- **Credentials.** They MUST be cryptographically bound to the identifier and carry an explicit expiry, SHOULD be short-lived, and are issued and rotated at runtime. The LLM MUST NOT have access to the agent's credentials or those for its tools, so prompt injection cannot extract them.
- **Acting for a user.** Use the Authorization Code Grant: the user authenticates to the authorisation server and approves, then the agent redeems the code by authenticating as itself. The access token names the agent in `client_id` and the user in `sub`; resource servers MUST use both. The agent never handles the user's credentials.
- **Acting as itself.** Use the Client Credentials Grant or the JWT Authorization Grant. As an OAuth client the agent authenticates with the credentials above, not a static, long-lived client secret.
- **Anti-patterns.** Static API keys as agent identity: not cryptographically bound, conveying no identity, long-lived, hard to rotate. And a tool forwarding the agent's access token to services behind it; it should obtain a new one through OAuth 2.0 Token Exchange.
- **Human confirmation.** When access needs explicit confirmation, the authorisation server SHOULD decline or obtain the user's approval, for example out of band through OpenID CIBA. Approval given in the agent framework's UI is not authorisation by itself: it MUST be bound to a verifiable grant from the authorisation server, which keeps the final decision.
- **Long sessions.** Authorisation holds only for the life of the credential or token presented; on expiry the accepting party re-validates, and revocation or risk signals end or down-scope the session.
- **Audit.** Deployments MUST keep durable, tamper-evident audit logs. Each event records at least: the authenticated agent identifier; the delegated user or system, if any; the resource or tool; the action and decision; a timestamp and correlation identifier; the posture or risk state that influenced it; any remediation or revocation, with its cause.

## What to do with it

- Give each agent its own identity and short-lived credentials, kept out of the model's reach; retire static API keys and client secrets.
- Record the agent and the person it acts for on every authorisation decision.
- Back sensitive actions with a grant from the authorisation server, not just an in-product prompt.

## Terms

- **AIMS** — Agent Identity Management System: the functions that establish, maintain and evaluate an agent's identity and permissions; not a product.

## Caveats

- A working-group Internet-Draft (draft-ietf-wimse-aims-01, intended status Informational, expires 6 May 2027), not a standard. It may change, be replaced or lapse; the link follows the latest revision. Several specifications it builds on are drafts too.
- It admits a gap: CIBA is client-initiated, a poor fit when confirmation is needed mid-run.
