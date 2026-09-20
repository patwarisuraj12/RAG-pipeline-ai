import os
from langchain_community.vectorstores import FAISS


def create_vector_store(documents, embeddings):
    return FAISS.from_documents(
        documents,
        embeddings
    )


def save_vector_store(vector_store, path):
    os.makedirs(path, exist_ok=True)
    vector_store.save_local(path)


def load_vector_store(path, embeddings):
    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )


def create_retriever(vector_store, k=4):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )