import uvicorn
from fastapi import FastAPI, Request

from melo.api import TTS


speed = 1.0
device = "cuda:0"
model = TTS(language="KR", device=device)

app = FastAPI()


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

    speaker_ids = model.hps.data.spk2id
    response_data = model.tts_to_base64(text, speaker_ids["KR"], speed=speed)
    return response_data


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
