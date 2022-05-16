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


@app.post("/") 
async def root(s: str):
	global pid
	if(pid!=None):
		os.kill(pid,signal.SIGTERM)
		pid=None
		time.sleep(1)
	if(s=="None"):
		proc = subprocess.Popen(['python', 'blink.py'])
		pid= proc.pid
		print(pid)
	if(s=="Ambient"):
		proc = subprocess.Popen(['python', 'sensor_temp.py'])
		pid= proc.pid
		print(pid)
	if(s=="Chip"):
		proc = subprocess.Popen(['python', 'chip_temp.py'])
		pid= proc.pid
		print(pid)
	return {"message": "Running "+str(pid)}

@app.get("/status")
async def get_status():
    return 0
