#!/usr/bin/env python3
"""Generate a standard PCM mono reference tone for validating local audio handling.
NO SIP call is initiated and NO AI synthesis is implied."""
import argparse
import math
import struct
import wave

RATE = 16000
FREQUENCY = 440
SECONDS = 2

def generate(path, rate=RATE, frequency=FREQUENCY, duration=SECONDS):
    if rate != RATE or frequency != FREQUENCY or duration != SECONDS:
        raise ValueError("Reference tone parameters are fixed for reproducible testing")
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(rate)
        frames = bytearray()
        for index in range(rate * duration):
            value = int(6000 * math.sin(2 * math.pi * frequency * index / rate))
            frames.extend(struct.pack("<h", value))
        output.writeframes(frames)

def inspect(path):
    with wave.open(str(path), "rb") as sound:
        result = {"channels": sound.getnchannels(), "sample_rate": sound.getframerate(),
                  "bit_depth": sound.getsampwidth() * 8, "frames": sound.getnframes()}
    if result != {"channels": 1, "sample_rate": RATE, "bit_depth": 16, "frames": RATE * SECONDS}:
        raise ValueError("Unexpected reference WAV characteristics")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    generate(args.path)
    print(inspect(args.path))
    print("PASS: local PCM generation only; SIP/RTP audio is NOT VERIFIED")
