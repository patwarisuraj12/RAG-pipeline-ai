from langchain_ollama import ChatOllama

def get_llm(model_name: str):
    return ChatOllama(
        model=model_name
    )