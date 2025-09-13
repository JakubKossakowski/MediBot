# app/services/llm_client.py
from typing import Any, Dict, List
from Chat_bot_medyczny.app.services.settings_store import get_settings_from_db

class LLMClient:
    def __init__(self, *args, **kwargs):
        pass

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Messages: lista obiektów {"role": "...", "content": "..."}.
        Zwraca odpowiedź z modelu. Dostosuj do używanego SDK.
        """
        settings = get_settings_from_db()
        model = settings.llm_model
        temperature = settings.temperature

        return {
            "ok": True,
            "model_used": model,
            "temperature_used": temperature,
            "messages_sent": messages,
            "note": "Podłącz SDK LLM w app/services/llm_client.py"
        }

def send_to_openai(messages: List[Dict[str, str]], **kwargs) -> Any:
    client = LLMClient()
    return client.generate(messages, **kwargs)
