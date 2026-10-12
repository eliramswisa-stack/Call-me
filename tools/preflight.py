#!/usr/bin/env python3
"""Non-dialing SIP endpoint preflight. No credentials, packets with personal data, or billable calls."""
import argparse
import ipaddress
import re
import socket
import ssl
import sys

PATTERN = re.compile(r"^sip:([A-Za-z0-9_.!~*'()&=+$,;?/-]+)@([A-Za-z0-9.-]+)$")

def parse_target(target):
    match = PATTERN.fullmatch(target)
    if not match:
        raise ValueError("Invalid SIP address")
    user, host = match.groups()
    if len(user) > 100 or len(host) > 253:
        raise ValueError("SIP address exceeds limits")
    if host != "sip.linphone.org":
        raise ValueError("This project only permits the owner's Linphone server")
    return user, host

def main():
    p = argparse.ArgumentParser(description="SIP DNS/TLS test. NEVER places calls.")
    p.add_argument("--target", default="sip:eliramswis@sip.linphone.org")
    p.add_argument("--network", action="store_true", help="Check DNS and TLS reachability without signing in or calling")
    args = p.parse_args()
    try:
        user, host = parse_target(args.target)
    except ValueError as exc:
        print("FAIL:", exc)
        return 2
    print("PASS: SIP address syntax and server allowlist. No call attempted.")
    if not args.network:
        return 0
    try:
        addresses = socket.getaddrinfo(host, 5061, type=socket.SOCK_STREAM)
        public_addresses = sorted({str(x[4][0]) for x in addresses if ipaddress.ip_address(x[4][0]).is_global})
        if not public_addresses:
            print("FAIL: no globally routable DNS addresses")
            return 1
        print("PASS: server DNS resolves to public address(es)")
        with socket.create_connection((host, 5061), timeout=8) as sock:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(sock, server_hostname=host) as tls:
                print("PASS: server SIP TLS port is reachable (TLS version:", tls.version(), ")")
    except (OSError, ssl.SSLError) as exc:
        print("BLOCKED: DNS or SIP TLS connection:", type(exc).__name__, str(exc))
        return 1
    print("NOTICE: this does NOT prove account registration, incoming ringing, media, or AI voice.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
