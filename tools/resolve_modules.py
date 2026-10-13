#!/usr/bin/env python3
"""Locate Baresip modules from the OS package, fail closed if missing."""
import argparse
import subprocess
from pathlib import Path

REQUIRED=("g711","aufile")
OPTIONAL=("stdio","menu")
def resolve(config, roots=None):
    config=Path(config)
    if roots is None:
        files=[]
        for package in ("baresip-core", "baresip", "baresip-modules"):
            result=subprocess.run(["dpkg","-L",package],capture_output=True,text=True)
            if result.returncode==0:
                files.extend(Path(x) for x in result.stdout.splitlines())
    else:
        files=[Path(x) for x in roots]
    found={}
    for name in REQUIRED+OPTIONAL:
        matches=[x for x in files if x.name==name+".so" and x.is_file()]
        if matches: found[name]=matches[0]
    missing=[name for name in REQUIRED if name not in found]
    if missing: raise RuntimeError("Missing required Baresip module(s): "+", ".join(missing))
    folder=found["g711"].parent
    if any(p.parent!=folder for p in found.values()):
        raise RuntimeError("Modules have incompatible directories")
    with config.open("a",encoding="utf-8") as out:
        out.write("\nmodule_path "+str(folder)+"\n")
        for name in REQUIRED+OPTIONAL:
            if name in found: out.write(("module_app " if name == "stdio" else "module ") + name + ".so\n")
    return sorted(found)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("config")
    args=p.parse_args()
    print("Resolved modules:",", ".join(resolve(args.config)))
