from langchain_core.prompts import PromptTemplate


QA_PROMPT = PromptTemplate(
    template="""
You are a helpful assistant.

Answer ONLY from the provided transcript context.

If the context is insufficient to answer the question,
say: "I don't know based on the provided transcript."

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=[
        "context",
        "question"
    ]
)