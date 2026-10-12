#!/usr/bin/env python3
"""Generate a mono 16kHz 16-bit looping reference tone for Baresip SIP media testing.
No outbound calling is performed. Tone is NOT Hebrew TTS."""
import argparse
import math
import struct
import wave
RATE=16000
def generate(path, seconds=90, frequency=440):
    if not 2 <= seconds <= 180 or frequency != 440:
        raise ValueError("Unsafe duration/frequency")
    with wave.open(str(path),"wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        batch=bytearray()
        for i in range(RATE * seconds):
            # 2 seconds tone, 1 second silence repeated; facilitates hearing checks
            value = int(6000 * math.sin(2*math.pi*frequency*i/RATE)) if (i//RATE)%3 != 2 else 0
            batch.extend(struct.pack("<h",value))
            if len(batch)>=32768:
                out.writeframesraw(batch)
                batch.clear()
        if batch: out.writeframesraw(batch)
        out.writeframes(b"")
def inspect(path):
    with wave.open(str(path),"rb") as w:
        return {"channels":w.getnchannels(),"sample_rate":w.getframerate(),"bit_depth":w.getsampwidth()*8,"frames":w.getnframes()}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--seconds",type=int,default=90)
    a=p.parse_args()
    generate(a.path, a.seconds)
    result=inspect(a.path)
    assert result=={"channels":1,"sample_rate":RATE,"bit_depth":16,"frames":RATE*a.seconds}
    print("PASS: PCM WAV created; does not prove SIP/RTP",result)
