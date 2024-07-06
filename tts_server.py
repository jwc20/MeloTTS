import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

# from melo.api import TTS

# speed = 1.0
# device = "cuda:0"
# model = TTS(language="KR", device=device)
# speaker_ids = model.hps.data.spk2id

app = FastAPI()

punc = """;:@#$%^&*-~※○●□■△▲◇◆▽▼→←↑↓↔↕↗↘↙↖↙↗↘↖↔↕─│┌┐└┘├┤┬┴┼━┃┏┓┗+"""

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










##################################################################################
## Utils #########################################################################
##################################################################################

def remove_match(text, start_position, match_length):
    """_summary_

    Args:
        text (str): _description_
        start_position (int): _description_
        match_length (int): _description_

    Returns:
        str: _description_
    """

    start_position, match_length = abs(start_position), abs(match_length)
    front = text[:start_position]   # up to but not including n
    back = text[start_position + match_length:]  # n+1 through end of string
    return front + back

def KnuthMorrisPratt(text, pattern):
    """
    https://en.m.wikibooks.org/wiki/Algorithm_Implementation/String_searching/Knuth-Morris-Pratt_pattern_matcher

    Knuth-Morris-Pratt string matching
    David Eppstein, UC Irvine, 1 Mar 2002

    Yields all starting positions of copies of the pattern in the text.
    Calling conventions are similar to string.find, but its arguments can be
    lists or iterators, not just strings, it returns all matches, not just
    the first one, and it does not need the whole text in memory at once.
    Whenever it yields, it will have read the text exactly up to and including
    the match that caused the yield.

    input: text as a string, pattern as a string
    output: iterator (list) of starting positions of matches
    """

    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos - shift]:
            shift += shifts[pos - shift]
        shifts[pos + 1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            yield startPos


##################################################################################
##################################################################################
##################################################################################














@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/synthesize")
async def apifunction_generate_tts(request: Request):
    _json = await request.json()
    text = _json["text"]

    for c in text:
        if c in punc:
            text = text.replace(c, "")

    text = text.replace("\n", " ")

    pattern = "프로그램"
    pattern_length = len(pattern)
    matches = list(KnuthMorrisPratt(text, pattern))
    print(matches)  # Output: [10]

    print(text)

    # print new line
    print("\n")
    print("\n")
    print("\n")

    if len(matches) > 0:
        for match in matches:
            print(remove_match(text, match, pattern_length))
            print("\n")




    # response_data = model.tts_to_base64(text, speaker_ids["KR"], speed=speed)
    # return response_data



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
