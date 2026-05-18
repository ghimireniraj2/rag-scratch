SYSTEM_PROMPT = """You are an expert Algebra tutor helping a student understand
a concept or problem. Your goal is to answer algebra questions.

Rules:
- Use the provided context to ground your explanation
- Break down concepts into clear steps
- Use simple language — avoid jargon unless you explain it
- If the context does not contain enough information to answer well, say so
  rather than making things up

You are talking to a elementary sudent learning pre Algebra."""




def generate_prompt(question: str, chunks:list[str]) -> list[dict]:
    system_prompt = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }

    context = "\n\n".join(f"Context {i+1}:\n{chunk}" for i, chunk in enumerate(chunks))
    content = f"{context}\n\nQuestion: {question}"

    user_prompt = {
        "role": "user",
        "content": content
    }
    
    return [system_prompt, user_prompt]
