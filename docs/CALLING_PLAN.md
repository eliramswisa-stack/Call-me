# SIP voice call readiness

## Evidence
- GitHub Actions run #4 succeeded according to screenshot supplied by owner.
- Workflow tests URI parsing and SIP DNS/TLS only, not SIP INVITE, ringing or audio.
- No SIP calling backend has been deployed.

## Minimal viable actual call
1. Obtain an **outbound SIP identity** from a legitimate free provider (or host a standards-compliant SIP UA). The target address alone is insufficient to place a call. No credentials may appear in public repositories.
2. Deploy a reachable SIP user agent with SRTP/RTP and NAT traversal. GitHub Actions runners are ephemeral, not durable media services. The project has no such deployment yet.
3. Establish an owner-authorized SIP-to-SIP INVITE to the verified owner account only.
4. Prove incoming iPhone ring and bi-directional audio with timestamped logs, masking all credentials.
5. Add Hebrew ASR + TTS + dialogue manager. Verify latency and that barge-in works.
6. Schedule future calls only after the above has passed and explicit owner opt-in is recorded.

## Financial and security constraints
No paid trial, credit-card requirement, commercial PSTN dialing, or automatic calls to arbitrary recipients. Treat zero-cost forever as an unproven goal, not a provider guarantee.

## Gate
`python tools/call_gate.py --dry-run --owner-consent` validates the intended recipient and correctly reports `NO_SIP_BACKEND_CONNECTED`. It never initiates a network call.
