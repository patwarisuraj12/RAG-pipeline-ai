# System Architecture

## 1. Overview

R → Retrieval
    FAISS finds relevant chunks

A → Augmented
    Retrieved chunks are added to the prompt

G → Generation
    Llama generates the answer

The YouTube RAG Assistant is a local Retrieval-Augmented Generation application.

Its purpose is to answer user questions based only on the transcript of a selected YouTube video.

Instead of sending the complete transcript to the language model, the system first retrieves the transcript sections most relevant to the user's question.

This reduces unnecessary context and improves the grounding of the generated answer.

## 2. High-Level Architecture

```text
                 ┌─────────────────────┐
                 │    YouTube Video    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Transcript Service  │
                 │ YouTubeTranscriptAPI│
                 └──────────┬──────────┘
                            │
                            ▼
                    Raw Transcript
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Text Chunker     │
                 │ RecursiveCharacter │
                 │    TextSplitter     │
                 └──────────┬──────────┘
                            │
                            ▼
                    Transcript Chunks
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Embedding Service   │
                 │ nomic-embed-text    │
                 │      Ollama         │
                 └──────────┬──────────┘
                            │
                            ▼
                   Vector Embeddings
                            │
                            ▼
                 ┌─────────────────────┐
                 │        FAISS        │
                 │    Vector Store     │
                 └──────────┬──────────┘
                            │
                  User Question
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Retriever      │
                 │ Similarity Search   │
                 └──────────┬──────────┘
                            │
                            ▼
                   Relevant Documents
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Prompt Template   │
                 │ Context + Question  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     ChatOllama      │
                 │    Llama 3.2 1B     │
                 └──────────┬──────────┘
                            │
                            ▼
                       Final Answer
```

## 3. Application Layers

The project is divided into three main areas.

### Application Layer

`main.py` coordinates the complete workflow.

It does not contain the detailed implementation of transcript extraction, embeddings, retrieval, or LLM processing.

Its responsibility is orchestration.

Example flow:

```text
main.py

    fetch_transcript()
          ↓
    split_transcript()
          ↓
    get_embeddings()
          ↓
    create_vector_store()
          ↓
    create_retriever()
          ↓
    get_llm()
          ↓
    answer_question()
```

### Service Layer

The `services/` package contains integrations with external or runtime services.

```text
services/
│
├── transcript_service.py
├── embedding_service.py
├── llm_service.py
└── ollama_service.py
```

#### transcript_service.py

Responsibility:

```text
YouTube Video ID
       ↓
Transcript Text
```

It interacts with the YouTube Transcript API.

#### embedding_service.py

Creates the Ollama embedding model used to convert text into numerical vectors.

Current model:

```text
nomic-embed-text
```

#### llm_service.py

Creates the language model used for final answer generation.

Current model:

```text
llama3.2:1b
```

#### ollama_service.py

Responsible for verifying that the local Ollama service is available.

The RAG pipeline should not contain Ollama process-management logic.

## 4. RAG Layer

The `rag/` package contains the Retrieval-Augmented Generation logic.

```text
rag/
│
├── chunker.py
├── vector_store.py
├── prompts.py
└── pipeline.py
```

### chunker.py

The complete transcript may be too large or too broad for effective retrieval.

It is therefore split into smaller overlapping chunks.

Current configuration:

```text
chunk size    = 1000
chunk overlap = 200
```

Conceptually:

```text
Transcript

---------------------------------------------------

Chunk 1
xxxxxxxxxxxxxxxxxxxxxxxx

          Chunk 2
          xxxxxxxxxxxxxxxxxxxxxxxx

                    Chunk 3
                    xxxxxxxxxxxxxxxxxxxxxxxx
```

The overlap helps preserve information located near chunk boundaries.

### vector_store.py

Transcript chunks are converted into embeddings and stored in FAISS.

FAISS enables similarity-based retrieval.

Conceptually:

```text
Chunk 1 → [0.12, 0.84, 0.17, ...]
Chunk 2 → [0.61, 0.32, 0.74, ...]
Chunk 3 → [0.19, 0.92, 0.26, ...]
```

These vectors represent semantic meaning rather than exact words.

### prompts.py

Contains prompt templates used by the application.

The current prompt instructs the LLM to answer only from the retrieved transcript context.

This helps reduce unsupported answers.

### pipeline.py

Contains the core question-answering workflow.

```text
Question
   ↓
Retriever
   ↓
Relevant transcript chunks
   ↓
Combine chunks into context
   ↓
Prompt Template
   ↓
LLM
   ↓
Answer
```

## 5. Indexing Flow

The first part of the system prepares the transcript for retrieval.

```text
YouTube Video
     ↓
Transcript API
     ↓
Transcript
     ↓
Chunking
     ↓
Embedding Model
     ↓
Vectors
     ↓
FAISS
```

This can be considered the indexing phase.

## 6. Query Flow

When the user asks a question:

```text
User Question
      ↓
Embedding Representation
      ↓
FAISS Similarity Search
      ↓
Top K Relevant Chunks
      ↓
Context Construction
      ↓
Prompt
      ↓
LLM
      ↓
Answer
```

Current retrieval configuration:

```text
k = 4
```

Therefore, four relevant chunks are retrieved for each question.

## 7. Separation of Responsibilities

Each module should have one primary responsibility.

```text
config.py
    Configuration

main.py
    Workflow orchestration

transcript_service.py
    YouTube transcript retrieval

chunker.py
    Text splitting

embedding_service.py
    Embedding model creation

vector_store.py
    FAISS creation and retrieval

prompts.py
    Prompt definitions

llm_service.py
    LLM creation

pipeline.py
    RAG question-answering logic
```

This makes individual components easier to test and replace.

For example, FAISS could later be replaced by another vector database without significantly changing transcript handling or LLM code.

## 8. Model Architecture

Two separate models perform different jobs.

### Embedding Model

```text
nomic-embed-text
```

Purpose:

```text
Text → Numerical Vector
```

It is used for semantic search.

### Generative Model

```text
llama3.2:1b
```

Purpose:

```text
Context + Question → Natural Language Answer
```

The embedding model performs retrieval.

The LLM performs generation.

These responsibilities should remain separate.

## 9. Data Storage

FAISS indexes may be stored under:

```text
data/faiss_index/
```

Persisting the index avoids recalculating transcript embeddings every time the application starts.

Future implementations should identify indexes by video ID.

For example:

```text
data/
└── faiss_index/
    ├── LnNQ_Z3esjo/
    └── another_video_id/
```

## 10. Error Handling

Expected application errors include:

```text
YouTube captions disabled
Transcript unavailable
Ollama unavailable
Embedding model missing
LLM model missing
FAISS creation failure
Retrieval failure
```

These errors should be raised by the module responsible for them and handled appropriately by the application layer.

## 11. Future Architecture

The current architecture supports future extensions without requiring a complete rewrite.

Possible architecture:

```text
                 ┌───────────────┐
                 │ Web / CLI UI  │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ RAG Service   │
                 └───────┬───────┘
                         │
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
       Retriever                    LLM
            │                         │
            ▼                         ▼
       Vector DB                  Ollama
            │
            ▼
     Transcript Store
```

Possible future additions include:

* Multiple YouTube videos
* Persistent vector indexes
* Interactive chat
* REST API
* Streamlit or web UI
* Conversation history
* Source citations
* Timestamp-aware responses
* RAG evaluation
* Observability and logging
* Alternative vector databases
* Alternative LLM providers
