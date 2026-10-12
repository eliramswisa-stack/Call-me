#!/usr/bin/env python3
"""Create a no-credential Baresip headless audio config (NO CALLS)."""
import argparse
from pathlib import Path

CONFIG = """# Temporary experimental headless audio test
audio_source aufile,{wav}
audio_player aufile,{sink}
module stdio.so
module g711.so
module aufile.so
module menu.so
"""

def write_config(folder, wav):
    folder = Path(folder)
    wav = Path(wav)
    if not wav.is_file() or wav.suffix.lower() != ".wav":
        raise ValueError("An existing WAV input is required")
    if any(c in str(wav) for c in ("\n", "\r", ",")):
        raise ValueError("Unsupported WAV path")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "config"
    target.write_text(CONFIG.format(wav=wav.absolute(), sink=(folder / "received.wav").absolute()), encoding="utf-8")
    return target

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("folder")
    p.add_argument("wav")
    args = p.parse_args()
    out = write_config(args.folder, args.wav)
    print("Prepared non-dialing experimental audio config:", out)
