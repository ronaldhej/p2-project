#import os
#os.environ["ARCADE_HEADLESS"] = "true"

import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

import base64
import json

import sim

class CanvasEntityDto(BaseModel):
    """entity used in simulation"""
    center_x: float
    center_y: float
    width: float
    height: float
    color: str | None = "White"

class SimRequestDto(BaseModel):
    """request containing inputs for a simulation"""
    agent_num: int | None = 1
    runtime: int | None = 10
    map: list[CanvasEntityDto] | None = None

app = FastAPI()
DEV = True
FIELD_RES = 32#32

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """get"""
    return {"message": "This is the root of the simulation API"}

@app.websocket("/ws")
async def run_socket_sim(socket: WebSocket):
    print("handling connection request")
    await socket.accept()
    print("connection established")
    data = await socket.receive_text()
    print(data)
    request = json.loads(data)
    print(request)
    image_buffer, agent_amount_data = await sim.run_agent_sim(socket, 60, False, request["agent_num"], request["runtime"], FIELD_RES)
    image_buffer.seek(0)
    buffer_bytes = image_buffer.getvalue()
    buffer_base64 = base64.b64encode(buffer_bytes)
    try:
        await socket.send_json(data={"type": 0,"sim_gif": buffer_base64.decode('utf-8'), "density_data": agent_amount_data})
        await socket.close()
    except WebSocketDisconnect:
        print("disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)