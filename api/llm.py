from groq import Groq
from prompt import generate_prompt
from config import settings

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(
            api_key=settings.groq_api_key,            
        )
    return _client

def complete(question: str, chunks: list[dict], stream: bool = False):
    return get_client().chat.completions.create(
        messages=generate_prompt(question=question, chunks=chunks),
        model=settings.groq_model,
        stream=stream
    )

    #print(chat_completion.choices[0].message.content)
    #return chat_completion.choices[0].message.content
