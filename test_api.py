import numpy as np
import pytest
from fastapi.testclient import TestClient

from api import api

client = TestClient(api)


def test_synthesize_success(tmp_path, monkeypatch):
    """Test successful synthesis returns 200 and file path."""
    # Import here so monkeypatches apply
    import api

    # Set fixed timestamp for predictable filename
    class MockDatetime:
        @staticmethod
        def now():
            class MockNow:
                @staticmethod
                def strftime(format_str):
                    return "20240101_120000"

            return MockNow()

    monkeypatch.setattr(api, "datetime", MockDatetime)

    # Avoid making directories
    monkeypatch.setattr("os.makedirs", lambda *a, **k: None)

    # Avoid writing files
    monkeypatch.setattr(api.sf, "write", lambda *a, **k: None)

    # Create fake audio generator that pipeline would return
    def fake_pipeline(*args, **kwargs):
        yield (None, None, np.array([0.1, 0.2, 0.3]))

    monkeypatch.setattr(api, "pipeline", fake_pipeline)

    # Test API
    response = client.post("/tts", data={"text": "hello", "voice": "af_heart"})

    # If test fails, show error content
    if response.status_code != 200:
        print(f"Error: {response.json()}")

    assert response.status_code == 200
    assert response.json() == {"file_path": "out/20240101_120000.wav"}


def test_synthesize_error(monkeypatch):
    """Test that exceptions return 500 status code."""
    import api

    # Make pipeline throw exception
    def fake_error_pipeline(*args, **kwargs):
        raise Exception("Test error")

    monkeypatch.setattr(api, "pipeline", fake_error_pipeline)

    response = client.post("/tts", data={"text": "fail"})
    assert response.status_code == 500
    assert "error" in response.json()
