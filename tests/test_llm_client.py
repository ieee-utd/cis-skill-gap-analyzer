from types import SimpleNamespace

from skill_gap import llm_client


class FakeModels:
    def generate_content(self, model, contents):
        return SimpleNamespace(text=f"fake reply to: {contents}")


class FakeClient:
    def __init__(self, api_key):
        self.models = FakeModels()


def test_ask_llm_returns_text(monkeypatch):
    monkeypatch.setattr(llm_client, "get_api_key", lambda: "fake-key")
    monkeypatch.setattr(llm_client.genai, "Client", FakeClient)
    assert llm_client.ask_llm("hi") == "fake reply to: hi"
