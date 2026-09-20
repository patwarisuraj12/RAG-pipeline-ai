import os

from config import (
    VIDEO_ID,
    EMBEDDING_MODEL,
    LLM_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RETRIEVER_K,
    FAISS_INDEX_PATH
)

from services.transcript_service import fetch_transcript
from services.embedding_service import get_embeddings
from services.llm_service import get_llm

from rag.chunker import split_transcript
from rag.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    create_retriever
)

from rag.pipeline import answer_question


def main():

    embeddings = get_embeddings(
        EMBEDDING_MODEL
    )

    if os.path.exists(FAISS_INDEX_PATH):
        print("Loading existing FAISS index...")

        vector_store = load_vector_store(
            FAISS_INDEX_PATH,
            embeddings
        )

    else:
        print("Creating FAISS index...")

        transcript = fetch_transcript(
            VIDEO_ID
        )

        chunks = split_transcript(
            transcript,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        vector_store = create_vector_store(
            chunks,
            embeddings
        )

        save_vector_store(
            vector_store,
            FAISS_INDEX_PATH
        )

        print("FAISS index saved.")

    retriever = create_retriever(
        vector_store,
        RETRIEVER_K
    )

    llm = get_llm(
        LLM_MODEL
    )

    question = "What are the main points to note in this video?"

    answer = answer_question(
        question,
        retriever,
        llm
    )

    print(answer)


if __name__ == "__main__":
    main()