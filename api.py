#!/bin/python
import logging
import os
from datetime import datetime

import colorlog
import numpy as np
import soundfile as sf
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from kokoro import KPipeline
from pydantic import BaseModel

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s: [%(asctime)s]  %(name)s %(message)s"
    )
)

logging.basicConfig(level=logging.INFO, handlers=[handler])

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
async def tts(
    text: str = Form(...), voice: str = Form("af_heart"), file_path: str = Form(...)
):
    try:
        logging.info(
            f"Received TTS request: text='{text[:30]}...', voice='{
                voice}', file_path='{file_path}'"
        )
        generator = pipeline(text, voice=voice)
        audio_list = []
        for _, _, audio in generator:
            audio_list.append(audio)
        merged = np.concatenate(audio_list)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = "out"
        os.makedirs(out_dir, exist_ok=True)
        file_path_date = os.path.join(out_dir, f"{now}.wav")
        fp = file_path if file_path else file_path_date
        logging.info(f"Writing audio to '{fp}'")
        sf.write(fp, merged, 24000)
        logging.info(f"Audio written successfully: '{fp}'")
        return JSONResponse({"file_path": fp})
    except Exception as e:
        logging.error(f"Error in TTS: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)
