import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from openai import OpenAI


def get_open_ai_client(api_key: str) -> OpenAI:
    return OpenAI(
        api_key=api_key
    )
