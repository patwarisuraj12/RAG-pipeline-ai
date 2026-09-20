# YouTube RAG Assistant

A local Retrieval-Augmented Generation (RAG) application that answers questions about a YouTube video using its transcript.

The application fetches the video transcript, splits it into chunks, generates embeddings using Ollama, stores them in FAISS, retrieves relevant transcript sections, and sends the retrieved context to a local LLM for answer generation.

## Features

* Fetches YouTube transcripts
* Splits long transcripts into smaller overlapping chunks
* Generates embeddings locally using Ollama
* Stores embeddings in FAISS
* Retrieves semantically relevant transcript sections
* Uses a local LLM to answer questions
* Answers only from retrieved transcript context

## Tech Stack

* Python
* LangChain
* Ollama
* Llama 3.2
* Nomic Embed Text
* FAISS
* YouTube Transcript API

## Project Structure

```text
youtube_rag/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
│
├── services/
│   ├── __init__.py
│   ├── ollama_service.py
│   ├── transcript_service.py
│   ├── embedding_service.py
│   └── llm_service.py
│
├── rag/
│   ├── __init__.py
│   ├── chunker.py
│   ├── vector_store.py
│   ├── prompts.py
│   └── pipeline.py
│
├── data/
│   └── faiss_index/
│
└── docs/
    ├── ARCHITECTURE.md
    ├── DESIGN.md
    └── DECISIONS.md
```

## Prerequisites

Install Python and Ollama.

Required Ollama models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:1b
```

Verify installed models:

```bash
ollama list
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Application configuration is stored in `config.py`.

Example:

```python
VIDEO_ID = "LnNQ_Z3esjo"

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:1b"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 4
```

## Running the Application

Make sure Ollama is running:

```bash
ollama serve
```

Then run:

```bash
python main.py
```

The application will:

1. Fetch the YouTube transcript.
2. Split the transcript into chunks.
3. Generate embeddings.
4. Create a FAISS vector store.
5. Retrieve relevant transcript chunks.
6. Send the retrieved context and question to the LLM.
7. Print the generated answer.

## Example Question

```text
What are the main points to note in this video?
```

## RAG Flow

```text
YouTube Video
      ↓
Transcript
      ↓
Text Chunking
      ↓
Embeddings
      ↓
FAISS Vector Store
      ↓
Similarity Retrieval
      ↓
Relevant Transcript Context
      ↓
Prompt + Question
      ↓
Local LLM
      ↓
Answer
```

## Current Limitations

* Requires the YouTube video to have accessible captions.
* Currently configured primarily for English transcripts.
* FAISS index may be rebuilt unless persistence is enabled.
* Small local LLMs may produce lower-quality answers than larger models.
* The application currently handles one video at a time.

## Future Improvements

Possible improvements include:

* Save and reload FAISS indexes.
* Accept YouTube URLs from the command line.
* Support multiple videos.
* Add an interactive chat interface.
* Add source chunk references to generated answers.
* Add metadata such as transcript timestamps.
* Add evaluation and logging.
* Support additional LLM providers.

## Documentation

Detailed architecture is available in:

```text
docs/ARCHITECTURE.md
```

Design decisions and technical reasoning are documented in:

```text
docs/DESIGN.md
docs/DECISIONS.md
```
