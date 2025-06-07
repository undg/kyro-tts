#!/bin/python
import numpy as np
import soundfile as sf
import torch
from IPython.display import Audio, display
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
text = '''
You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings. I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking.
'''
# generator = pipeline(text, voice='af_heart')
# for i, (gs, ps, audio) in enumerate(generator):
#     print(i, gs, ps)
#     display(Audio(data=audio, rate=24000, autoplay=i==0))
#     sf.write(f'out/{i}.wav', audio, 24000)

generator = pipeline(text, voice='af_heart')
audio_list = []
for i, (gs, ps, audio) in enumerate(generator):
    print(i, gs, ps)
    display(Audio(data=audio, rate=24000, autoplay=i==0))
    audio_list.append(audio)
merged = np.concatenate(audio_list)
sf.write('out/merged.wav', merged, 24000)
