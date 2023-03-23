import os
os.environ["ARCADE_HEADLESS"] = "true"

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi import FastAPI

import base64
import json

import sim

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


@app.get("/")
async def root():
    """get"""
    return {"message": "Hello World"}
