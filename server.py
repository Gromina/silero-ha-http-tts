from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

import os
import torch

from typing import Any, Dict, AnyStr, List, Union


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'
speaker = 'xenia'  # 'aidar', 'baya', 'kseniya', 'xenia', 'random'
sample_rate = 48000  # 8000, 24000, 48000


# put this in docker image preparation
if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/ru_v3.pt',
                                   local_file)  


model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)


app = FastAPI()

try:
    os.mkdir("./static")
except:
    pass

app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


#curl -x POST -d '{"text":"posdf"}'  -H  "accept: application/json" -H  "Content-Type: application/json" 127.0.0.1:9898/api

@app.post("/api")
async def tts(request: Request):
    json = await request.json()
    #audio = model.apply_tts(text=example_text, speaker=speaker, sample_rate=sample_rate)


    # (text=None, ssml_text=None, speaker: str = 'xenia', audio_path: str = '', sample_rate: int = 48000, put_accent=True, put_yo=True)
    audio_path = "output.wav"
    res_path = model.save_wav(text=json["text"],speaker=speaker, audio_path="./static/"+audio_path, sample_rate=sample_rate)

    return {"url": request.url_for("static", path=audio_path)}
