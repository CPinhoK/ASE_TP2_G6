from fastapi import FastAPI , HTTPException, Request ,WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


import random
import string

import os
import time
import subprocess
import signal


pid=None

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(s: str):
	global pid
	if(pid!=None):
		os.killpg(pid, signal.SIGTERM)
	if(s=="Ambient"):
		proc = subprocess.Popen("python script.py", shell=True, preexec_fn=os.setsid)
		pid= proc.pid
	if(s=="Chip"):
		proc = subprocess.Popen("python test2.py", shell=True, preexec_fn=os.setsid)
		pid= proc.pid
	return {"message": "Running "+pid}

@app.get("/status")
async def get_status():
    return 0

def killlast():
	pass
