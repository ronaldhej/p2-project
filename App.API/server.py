#import os
#os.environ["ARCADE_HEADLESS"] = "true"

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi import FastAPI
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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/image")
async def get_image():
    """get"""
    image_buffer = sim.run_sim([10, 128], 1000, False)

    # buf = io.BytesIO()
    # image.save(buf, "GIF")
    image_buffer.seek(0)  # important here!

    buffer_bytes = image_buffer.getvalue()
    buffer_base64 = base64.b64encode(buffer_bytes)
    # print(buffer_base64)

    return JSONResponse(content={"image_gif": buffer_base64.decode('utf-8')})

@app.post("/simulate")
async def run_sim(request: SimRequestDto):
    """post"""
    print("simulate")
    try:

        # buf = io.BytesIO()
        # image.save(buf, "GIF")
        image_buffer = sim.run_agent_sim(60, False, request.agent_num, request.runtime)

        image_buffer.seek(0)  # important here!

        buffer_bytes = image_buffer.getvalue()
        buffer_base64 = base64.b64encode(buffer_bytes)
        return JSONResponse(content={"image_gif": buffer_base64.decode('utf-8')}, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"msg": "deez"}, status_code=500)

@app.get("/")
async def root():
    """get"""
    return {"message": "Hello World"}
