# Hebrew Voice Acceptance Gate

Target experience: incoming Linphone SIP call on the owner's iPhone with Hebrew conversation, automatic scheduled calls, interruptions, and no paid services.

## Evidence gate sequence
1. **SIP call signaling:** owner iPhone rings and answers; inspect sanitized SIP status, duration and BYE reason.
2. **RTP media:** send fixed PCM reference tone through configured Baresip audio source; prove owner can hear it for ≥ 5 seconds, and inbound owner audio is received.
3. **Hebrew TTS:** replace tone with synthesized Hebrew phrase; human confirms pronunciation and audio quality.
4. **Hebrew STT:** transcribe a spoken Hebrew phrase; compare against reference and guard against false transcription in silence.
5. **Dialogue turn-taking:** connect an actual conversational model; confirm at least three back-and-forth turns with conversational interruption.
6. **Scheduler:** configure owner-consented times and document time zone Israel and job completion.
7. **Free usage:** audit each provider and quotas before every deployment. Open source does not guarantee free compute or persistent hosting.

## Current limitations
The CI workflow can install Baresip, but no durable SIP media host, audio virtual devices, STT/TTS service, or dialogue engine are deployed. GitHub Actions is short-lived and does not prove call longevity. Never label the pipeline as ready solely from a green GitHub workflow.

## Secret handling
Never echo credentials. Keep SIP sender credentials solely in repository Actions secrets. The owner SIP destination is fixed in the call gate. Do not deploy real-money, subscription, or paid API usage.
