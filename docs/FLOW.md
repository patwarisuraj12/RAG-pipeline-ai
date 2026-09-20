# Execution Flow

1. main.py starts.
2. Configuration is loaded.
3. YouTube transcript is fetched.
4. Transcript is split into chunks.
5. Each chunk is converted into an embedding.
6. Embeddings are stored in FAISS.
7. User submits a question.
8. Question is converted into an embedding.
9. FAISS finds the four closest chunks.
10. Retrieved chunks are combined into context.
11. Context + question are inserted into the prompt.
12. Llama 3.2 generates the final answer.