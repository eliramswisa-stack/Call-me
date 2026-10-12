#!/usr/bin/env python3
"""Local free-software Hebrew voice dialogue prototype.
Runs only on a host with an audio input/output device, local Ollama,
whisper.cpp command, and a Hebrew-capable speech synthesizer.
Does not place calls, does not use paid cloud APIs.
"""
import argparse
import json
import shutil
import subprocess
import tempfile
import urllib.request
import wave
from pathlib import Path

def check_dependencies(whisper_cli="whisper-cli", tts="espeak-ng"):
    return {name: bool(shutil.which(binary)) for name, binary in
            [("ffmpeg", "ffmpeg"), ("whisper", whisper_cli),
             ("tts", tts)]}

def ask_local_model(history, model="qwen2.5:3b", endpoint="http://127.0.0.1:11434/api/chat"):
    if endpoint != "http://127.0.0.1:11434/api/chat":
        raise ValueError("Only localhost Ollama allowed")
    payload=json.dumps({"model":model,"messages":history,"stream":False,
                       "options":{"temperature":0.4}}).encode()
    request=urllib.request.Request(endpoint,data=payload,
                 headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(request,timeout=90) as response:
        obj=json.load(response)
    answer=obj["message"]["content"].strip()
    if not answer:
        raise ValueError("Model returned empty response")
    return answer

def transcribe(wav_path,model_path,whisper_cli="whisper-cli"):
    with tempfile.TemporaryDirectory() as tmp:
        out=Path(tmp)/"result"
        command=[whisper_cli,"-m",str(model_path),"-f",str(wav_path),"-l","he",
                 "-otxt","-of",str(out),"-nt"]
        subprocess.run(command,check=True,timeout=120,capture_output=True,text=True)
        result=Path(str(out)+".txt").read_text(encoding="utf-8").strip()
        return result

def speak_hebrew(text,tts="espeak-ng"):
    # Test only: espeak-ng Hebrew voices depend on the installed package.
    if not text or len(text)>3000:
        raise ValueError("Speech text length invalid")
    subprocess.run([tts,"-v","he",text],check=True,timeout=120)

def test_only():
    return {"check":"offline_voice_pipeline_dependencies",
            "dependencies":check_dependencies(),
            "runtime":"NOT_DEPLOYED",
            "sip_rtp":"NOT_CONNECTED",
            "hebrew_quality":"NOT_VERIFIED"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--input-wav")
    p.add_argument("--whisper-model")
    p.add_argument("--ollama-model",default="qwen2.5:3b")
    p.add_argument("--playback",action="store_true")
    args=p.parse_args()
    if args.check:
        print(json.dumps(test_only(),ensure_ascii=False))
        return
    if not args.input_wav or not args.whisper_model:
        p.error("--input-wav and --whisper-model are required for one local voice turn")
    utterance=transcribe(args.input_wav,args.whisper_model)
    if not utterance:
        print("No speech recognized; not responding.")
        return
    history=[{"role":"system","content":"אתה עוזר קולי אישי. דבר בעברית תקנית וטבעית בלבד. אל תמציא עובדות או טענות על התקדמות פרויקטים. ענה בקצרה."},
             {"role":"user","content":utterance}]
    reply=ask_local_model(history,args.ollama_model)
    print(json.dumps({"heard":utterance,"reply":reply},ensure_ascii=False))
    if args.playback:
        speak_hebrew(reply)

if __name__=="__main__":
    main()
