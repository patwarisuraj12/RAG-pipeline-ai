# Design

## Transcript Source

YouTubeTranscriptApi is used because the project works directly
with captioned YouTube videos without downloading video/audio.

## Chunking

RecursiveCharacterTextSplitter is used with:

chunk_size = 1000
chunk_overlap = 200

Overlap helps preserve context across chunk boundaries.

## Embeddings

Model:
nomic-embed-text

Reason:
Runs locally through Ollama and avoids external API dependency.

## Vector Database

FAISS is used because:
- lightweight
- local
- fast for small/medium projects
- easy to persist

## LLM

Model:
llama3.2:1b

Reason:
Small enough for local experimentation.

## Retrieval

Top K:
4

Four semantically relevant transcript chunks are passed to the LLM.