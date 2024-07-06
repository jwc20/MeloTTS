import os
import sys
import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import asyncio

from melo.api import TTS

speed = 1.0
device = "cuda:0"
model = TTS(language="KR", device=device)
speaker_ids = model.hps.data.spk2id

app = FastAPI()

special_characters = """;:@#$%^&*-~※○●□■△▲◇◆▽▼→←↑↓↔↕↗↘↙↖↙↗↘↖↔↕─│┌┐└┘├┤┬┴┼━┃┏┓┗+"#$%&'()*+-/<=>?@[\\]^`{|}~©®™•√π÷×¶∆£€¥₽₹"""

# allowed_origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "https://localhost:44345/",
#     "https://localhost:44345",
# ]

allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
    allow_origins=allowed_origins,
)


# from apitally.flask import ApitallyMiddleware
#
# app.wsgi_app = ApitallyMiddleware(
#     app,
#     client_id="65bd9a71-da0f-4bbc-8f07-5a64cac1e548",
#     env="prod",  # or "dev"
# )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/synthesize")
async def apifunction_generate_tts(request: Request):
    _json = await request.json()
    text = _json["text"]

    for c in text:
        if c in special_characters:
            text = text.replace(c, "")
    text = text.replace("\n", " ")

    loop = asyncio.get_event_loop()
    response_data = await loop.run_in_executor(None, model.tts_to_base64, text, speaker_ids["KR"], speed)
    return response_data


if __name__ == "__main__":
    # uvicorn.run("tts_server:app", host="127.0.0.1", port=8000, log_level="info")
    
    # mpiexec -n 2 python tts_server.py
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv('PORT', 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)