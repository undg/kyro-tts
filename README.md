---
title: Kokoro TTS
emoji: ❤️
colorFrom: indigo
colorTo: pink
sdk: gradio
sdk_version: 5.24.0
app_file: app.py
pinned: true
license: apache-2.0
short_description: Upgraded to v1.0!
disable_embedding: true
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

TTS for (kyro)[https://github.com/undg/kyro] (private)

Base on Kokoro and Gradio

```bash
make run
```

Generate voice:

```bash
curl -X POST -F "text=test voice" -F "voice=bf_lily" -F "file_path=1.wav" http://localhost:8000/tts
```

