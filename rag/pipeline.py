from rag.prompts import QA_PROMPT


def answer_question(
    question: str,
    retriever,
    llm
) -> str:

    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    final_prompt = QA_PROMPT.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(final_prompt)

    return response.content