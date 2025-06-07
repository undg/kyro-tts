import os

import pytest
from fastapi.testclient import TestClient

from api import api

client = TestClient(api)


# def test_synthesize_success(tmp_path, monkeypatch):
#     # Patch out_dir to tmp_path for isolation
#     # monkeypatch.setattr("os.makedirs", lambda *a, **k: None)
#     # monkeypatch.setattr("os.path.join", lambda *a: str(tmp_path.joinpath(a[-1])))
#     monkeypatch.setattr("os.makedirs", lambda *a, **k: None)
#     monkeypatch.setattr("api.datetime", __import__("datetime"))
#     # monkeypatch.setattr("api.out_dir", str(tmp_path))
#     # Patch sf.write to avoid actual file writing
#     import api
#
#     monkeypatch.setattr(api.sf, "write", lambda *a, **k: None)
#
#     # Patch pipeline to return fake audio
#     class FakeGen:
#         def __iter__(self):
#             return self
#
#         def __next__(self):
#             raise StopIteration
#
#     monkeypatch.setattr(
#         api, "pipeline", lambda *a, **k: [(None, None, [0.1, 0.2, 0.3])]
#     )
#     response = client.post("/tts", data={"text": "hello", "voice": "af_heart"})
#     assert response.status_code == 200
#     print(response)
#     # assert "file_path" in response.json()


def test_synthesize_error(monkeypatch):
    monkeypatch.setattr(
        "api.pipeline", lambda *a, **k: (_ for _ in ()
                                         ).throw(Exception("fail"))
    )
    response = client.post("/tts", data={"text": "fail"})
    assert response.status_code == 500
    assert "error" in response.json()
