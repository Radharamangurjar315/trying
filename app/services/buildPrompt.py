def build_prompt(query: str, chunks: list[str]) -> str:
    context = "\n".join(chunks)  # join strings
    # print(f"query = {query}")
    # print(f"Context = {context}")
    prompt = (
        f"Question: {query}\n\n"
        f"Context:\n{context}\n\n"
    )
    return prompt

