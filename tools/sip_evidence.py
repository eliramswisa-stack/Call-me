#!/usr/bin/env python3
"""Classify Baresip output without reporting a false success.
Logs may include sensitive SIP metadata; do not publish logs by default.
"""
import argparse
import re
from pathlib import Path

FAIL_PATTERNS = [
    r"Populated 0 audio codecs",
    r"module (?:g711|aufile)\.so: No such file",
    r"cannot open shared object file",
    r"registration failed",
    r"SIP/2\.0 (?:403|404|408|480|486|500|503)",
]
PASS_PATTERNS = [r"call established", r"call connected", r"SIP/2\.0 200 OK"]
def classify(log):
    if any(re.search(p,log,re.I) for p in FAIL_PATTERNS):
        return "FAIL_MEDIA_OR_SIGNALING"
    if any(re.search(p,log,re.I) for p in PASS_PATTERNS):
        return "SIGNALING_POSSIBLY_CONNECTED_MEDIA_NOT_VERIFIED"
    return "UNVERIFIED_NO_CALL_EVIDENCE"
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("log")
    args=p.parse_args()
    print(classify(Path(args.log).read_text(errors="replace")))
