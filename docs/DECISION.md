# Architecture Decisions

## ADR-001: Use Ollama instead of OpenAI

Decision:
Use local Ollama models.

Reason:
- No API cost
- Local learning environment
- Data stays local

Trade-off:
Smaller local models may provide lower answer quality.

---

## ADR-002: Use FAISS

Decision:
Use FAISS instead of Chroma/Pinecone.

Reason:
Project is currently local and single-user.

Future:
Consider Chroma/PostgreSQL pgvector if persistence or
multi-user access becomes important.