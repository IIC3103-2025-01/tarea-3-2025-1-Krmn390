import requests
from my_config import (
    LLM_API_URL,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    LLM_REPEAT_LAST_N,
    LLM_TOP_K
)


def query_llm(context: str, question: str) -> str:
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Responde de forma clara, precisa y detallada usando únicamente el contexto entregado. Si no sabes la respuesta, indícalo explícitamente."
            },
            {
                "role": "user",
                "content": f"Contexto:\n{context}\n\nPregunta:\n{question}"
            }
        ],
        "stream": False,
        "options": {
            "temperature": LLM_TEMPERATURE,
            "num_ctx": LLM_MAX_TOKENS,
            "repeat_last_n": LLM_REPEAT_LAST_N,
            "top_k": LLM_TOP_K
        }
    }

    try:
        response = requests.post(LLM_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al conectar con la API del LLM: {e}")
    except KeyError:
        raise Exception("La respuesta del modelo no tiene el formato esperado.")
