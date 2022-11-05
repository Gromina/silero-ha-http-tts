from fastapi import FastAPI, Request, Body, Form
from fastapi.staticfiles import StaticFiles
from urllib.parse import urlparse, parse_qs
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse

import tempfile


import json
import os
import torch
import hashlib
import pprint

from normalization import NormText

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


pp = pprint.PrettyPrinter(indent=2)

@app.post("/process")
async def tts(request: Request):
    body = await request.body()
    params = parse_qs(body.decode("utf-8"))
    params = {k: next(iter(v or []), "") for k, v in params.items()}


    text_to_tts = params["INPUT_TEXT"]
    text_to_tts = NormText(text_to_tts)
    hash_object = hashlib.sha512(bytes(text_to_tts,'UTF-8'))
    hex_dig = hash_object.hexdigest()

    audio_path = "%s.wav" % hex_dig
    text_norm = text_to_tts

    orig_wav_file = "./static/orig_"+audio_path
    wav_file = "./static/"+audio_path

    # (text=None, ssml_text=None, speaker: str = 'xenia', audio_path: str = '', sample_rate: int = 48000, put_accent=True, put_yo=True)
    res_path = model.save_wav(text=text_norm, speaker=speaker, audio_path=orig_wav_file, sample_rate=sample_rate)
    command_eff =(f'sox {orig_wav_file} {wav_file} reverb 50 50 100')

    #print(command_mp3)
    os.system(command_eff)

    def iterfile():  # 
        with open(wav_file, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="audio/wav")

@app.post("/tts")
async def tts(request: Request):
    body = await request.body()
    params = parse_qs(body.decode("utf-8"))
    params = {k: next(iter(v or []), "") for k, v in params.items()}


    text_to_tts = params["INPUT_TEXT"]
    text_to_tts = NormText(text_to_tts)

    hash_object = hashlib.sha512(bytes(text_to_tts,'UTF-8'))
    hex_dig = hash_object.hexdigest()

    audio_path = "%s.wav" % hex_dig
    text_norm = text_to_tts
    wav_file = "./static/"+audio_path

    # (text=None, ssml_text=None, speaker: str = 'xenia', audio_path: str = '', sample_rate: int = 48000, put_accent=True, put_yo=True)
    res_path = model.save_wav(ssml_text=f'<speak><break time="1s"/>{text_norm}<break time="1s"/></speak>', speaker=speaker, audio_path=wav_file, sample_rate=sample_rate)
    command_mp3 =(f'sox {wav_file} {wav_file}.mp3 reverb 50 50 100')
# sox f2btrop6.0.wav f2btr.mp3 reverb 50 50 10

    #print(command_mp3)
    os.system(command_mp3)

    return {"url": request.url_for("static", path=audio_path+".mp3")}
