import uvicorn
# from typing import Any
from fastapi import FastAPI, Request

from typing import Any, Dict, AnyStr, List, Union
from melo.api import TTS
from pydantic import BaseModel


from typing import Dict

import json


speed = 1.0
device = 'cuda:0'

# text = "안녕하세요! 오늘은 날씨가 정말 좋네요."
model = TTS(language='KR', device=device)

app = FastAPI()


# from apitally.flask import ApitallyMiddleware
#
# app.wsgi_app = ApitallyMiddleware(
#     app,
#     client_id="65bd9a71-da0f-4bbc-8f07-5a64cac1e548",
#     env="prod",  # or "dev"
# )


class TtsPostRequest(BaseModel):
    languageCode: str | None = None
    name: str| None = None
    text: str
    
    # voice: dict[str, str]
    # input: dict[str, str]
    # audioconfig: dict[str, str]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/synthesize")
async def apifunction_generate_tts(request: Request): 
    _json = await request.json()
    # => ('{"languageCode":"ko-KR","name":"ko-KR-Standard-B","text":"1번. 또 파이썬은 순수한 ''프로그램 언어로서의 기능 외에도 다른 언어로 쓰인 모듈들을 연결하는 접착제 언어로써 자주 이용된다. 실제 파이썬은 많은 상용 응용 ''프로그램에서 스크립트 언어로 채용되고 있다. 도움말 문서도 정리가 잘 되어 있으며, 유니코 드 문자열을 지원해서 다양한 언어의 문자 ' '처리에도 능하다."}')
    # get text
    text = _json['text']
    
    print(text)
   
    speaker_ids = model.hps.data.spk2id
    # # output_path = 'kr.wav'
    # # model.tts_to_file(data, speaker_ids['KR'], output_path, speed=speed)
    
    response_data = model.tts_to_base64(text, speaker_ids['KR'], speed=speed)
    



    return response_data




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")