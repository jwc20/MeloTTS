import uvicorn
from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware 
from pprint import pprint
from melo.api import TTS
import string

speed = 1.0
device = "cuda:0"
model = TTS(language="KR", device=device)
speaker_ids = model.hps.data.spk2id

app = FastAPI()

punc = ''';:@#$%^&*_-~※○●□■△▲◇◆▽▼→←↑↓↔↕↗↘↙↖↙↗↘↖↔↕─│┌┐└┘├┤┬┴┼━┃┏┓┗'''

# allowed_origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "https://localhost:44345/",
#     "https://localhost:44345",
# ]

allowed_origins=["*"]

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
    pprint(_json)
    text = _json["text"]
    print(text)

    for c in text:
        if c in punc:
            text = text.replace(c, "")
    
    text = text.replace('\n', ' ')
    
    response_data = model.tts_to_base64(text, speaker_ids["KR"], speed=speed)
    return response_data


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
