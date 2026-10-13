#!/usr/bin/env python3
"""Pure validation for a user-authorized future SIP appointment.

This module does not call phones, access secrets, or dispatch workflows.
"""
from datetime import datetime, timezone, timedelta
import re

UTC = timezone.utc
OWNER = "eliramswisa-stack"
TITLE = "CALL_ME_SIP_V1"
FORMAT = re.compile(r"CALL_AT_UTC=(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)\nOWNER_CONSENT=YES\n?\Z")

def validate(title, body, author, now=None):
    if title != TITLE or author != OWNER:
        return "REJECTED"
    found = FORMAT.fullmatch(body or "")
    if not found:
        return "REJECTED"
    try:
        scheduled = datetime.strptime(found.group(1), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        return "REJECTED"
    now = now or datetime.now(UTC)
    if scheduled > now:
        return "WAITING"
    if scheduled < now - timedelta(minutes=20):
        return "EXPIRED"
    return "DUE"

def make_body(scheduled):
    if scheduled.tzinfo is None:
        raise ValueError("timezone-aware datetime required")
    return "CALL_AT_UTC=" + scheduled.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ") + "\nOWNER_CONSENT=YES"
