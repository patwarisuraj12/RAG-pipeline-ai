from langchain_ollama import OllamaEmbeddings

def get_embeddings(model_name: str):
    return OllamaEmbeddings(
        model=model_name
    )