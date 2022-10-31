from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

import os
import torch

import hashlib

from typing import Any, Dict, AnyStr, List, Union


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'
speaker = 'xenia'  # 'aidar', 'baya', 'kseniya', 'xenia', 'random'
sample_rate = 48000  # 8000, 24000, 48000

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)


app = FastAPI()

try:
    os.mkdir("./static")
except:
    pass

app.mount("/static", StaticFiles(directory="./static"), name="static")


#curl -x POST -d '{"text":"posdf"}'  -H  "accept: application/json" -H  "Content-Type: application/json" 127.0.0.1:9898/api

@app.post("/api")
async def tts(request: Request):
    json = await request.json()
    #audio = model.apply_tts(text=example_text, speaker=speaker, sample_rate=sample_rate)


    text_to_tts = json["text"]
    # (text=None, ssml_text=None, speaker: str = 'xenia', audio_path: str = '', sample_rate: int = 48000, put_accent=True, put_yo=True)
    hash_object = hashlib.sha512(bytes(text_to_tts,'UTF-8'))
    hex_dig = hash_object.hexdigest()

    audio_path = "%s.wav" % hex_dig
    res_path = model.save_wav(text=text_to_tts, speaker=speaker, audio_path="./static/"+audio_path, sample_rate=sample_rate)

    return {"url": request.url_for("static", path=audio_path)}
