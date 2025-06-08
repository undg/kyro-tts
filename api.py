#!/bin/python
import os
from datetime import datetime

import numpy as np
import soundfile as sf
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from kokoro import KPipeline
from pydantic import BaseModel

api = FastAPI()
pipeline = KPipeline(lang_code="a")


class SynthesizeRequest(BaseModel):
    text: str
    voice: str = "af_heart"


# CHOICES = {
# '🇺🇸 🚺 Heart ❤️': 'af_heart',
# '🇺🇸 🚺 Bella 🔥': 'af_bella',
# '🇺🇸 🚺 Nicole 🎧': 'af_nicole',
# '🇺🇸 🚺 Aoede': 'af_aoede',
# '🇺🇸 🚺 Kore': 'af_kore',
# '🇺🇸 🚺 Sarah': 'af_sarah',
# '🇺🇸 🚺 Nova': 'af_nova',
# '🇺🇸 🚺 Sky': 'af_sky',
# '🇺🇸 🚺 Alloy': 'af_alloy',
# '🇺🇸 🚺 Jessica': 'af_jessica',
# '🇺🇸 🚺 River': 'af_river',
# '🇺🇸 🚹 Michael': 'am_michael',
# '🇺🇸 🚹 Fenrir': 'am_fenrir',
# '🇺🇸 🚹 Puck': 'am_puck',
# '🇺🇸 🚹 Echo': 'am_echo',
# '🇺🇸 🚹 Eric': 'am_eric',
# '🇺🇸 🚹 Liam': 'am_liam',
# '🇺🇸 🚹 Onyx': 'am_onyx',
# '🇺🇸 🚹 Santa': 'am_santa',
# '🇺🇸 🚹 Adam': 'am_adam',
# '🇬🇧 🚺 Emma': 'bf_emma',
# '🇬🇧 🚺 Isabella': 'bf_isabella',
# '🇬🇧 🚺 Alice': 'bf_alice',
# '🇬🇧 🚺 Lily': 'bf_lily',
# '🇬🇧 🚹 George': 'bm_george',
# '🇬🇧 🚹 Fable': 'bm_fable',
# '🇬🇧 🚹 Lewis': 'bm_lewis',
# '🇬🇧 🚹 Daniel': 'bm_daniel',
# }


@api.post("/tts")
async def tts(text: str = Form(...), voice: str = Form("af_heart")):
    try:
        generator = pipeline(text, voice=voice)
        audio_list = []
        for _, _, audio in generator:
            audio_list.append(audio)
        merged = np.concatenate(audio_list)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = "out"
        os.makedirs(out_dir, exist_ok=True)
        file_path = os.path.join(out_dir, f"{now}.wav")
        sf.write(file_path, merged, 24000)
        return JSONResponse({"file_path": file_path})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
