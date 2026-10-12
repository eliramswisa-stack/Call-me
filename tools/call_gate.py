#!/usr/bin/env python3
"""Gate for an owner-authorized SIP calling experiment.

Important: This tool intentionally DOES NOT dial. It validates conditions that
must be satisfied before connecting an actual SIP UA and media engine.
"""
import argparse
import json
import os
import sys
from preflight import parse_target

OWNER_TARGET = "sip:eliramswis@sip.linphone.org"

def decision(target, consent, dry_run, backend_configured):
    try:
        parse_target(target)
    except ValueError as exc:
        return False, f"INVALID_TARGET: {exc}"
    if target != OWNER_TARGET:
        return False, "ONLY_OWNER_TARGET_ALLOWED"
    if not consent:
        return False, "OWNER_CONSENT_REQUIRED"
    if not backend_configured:
        return False, "NO_SIP_BACKEND_CONNECTED"
    if dry_run:
        return False, "DRY_RUN_ONLY"
    return True, "READY_FOR_IMPLEMENTED_BACKEND"

def main():
    p = argparse.ArgumentParser(description="Validate owner-only SIP calling prerequisites; never places calls")
    p.add_argument("--target", default=OWNER_TARGET)
    p.add_argument("--owner-consent", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    ok, reason = decision(args.target, args.owner_consent, args.dry_run, backend_configured=False)
    print(json.dumps({"ready": ok, "reason": reason, "dialed": False}, ensure_ascii=False))
    return 0 if args.dry_run else (0 if ok else 2)

if __name__ == "__main__":
    sys.exit(main())
