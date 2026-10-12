# Call-me — Linphone AI Calls

Independent proof-of-concept, unrelated to AI Trading Quantum.

## Goal
Receive a scheduled, two-way Hebrew AI voice call on an iPhone through Linphone SIP, with no subscription, credit card or paid calling minutes.

## Target
`sip:eliramswis@sip.linphone.org` (provided by owner; not independently verified by an actual call).

## Current verified state
- This GitHub repository is writable via ChatGPT's GitHub connector.
- The owner reported Linphone status **Connected**.
- **NO actual SIP call has been made; NO server or AI voice agent is deployed.**

## Remaining engineering work
1. Identify a free, reachable SIP origin and prove incoming iPhone ring using an actual call.
2. Prove duplex RTP media and iOS foreground/background ringing.
3. Integrate Hebrew STT, Hebrew TTS, and AI conversation with interruption support.
4. Schedule owner-approved calls, preserving free-only restrictions.
5. Record evidence for each step; do not mark successful until live proof.

## Guardrails
Never commit passwords, SIP registration credentials, tokens, or private keys. No chargeable trials, credit-card entry, payments, or real-money trading. Never expose owner account credentials. GitHub Actions is not itself a permanent SIP/PBX host. Free availability and unlimited calls cannot be guaranteed.
