SYSTEM_PROMPT = """You are an expert Algebra tutor helping a student understand
a concept or problem. Your goal is to answer algebra questions.

Rules:
- Use the provided context to ground your explanation
- Break down concepts into clear steps
- Use simple language — avoid jargon unless you explain it
- If the context does not contain enough information to answer well, say so
  rather than making things up

You are talking to a elementary sudent learning pre Algebra."""

def get_chunk_fitting_budget(question: str, chunks:list[dict], context_limit: int = 10000) ->list[dict]:
    budget = context_limit - (len(SYSTEM_PROMPT) +  len(question.split()))
    
    if budget < 0: budget = 100    
    # Sort chunks by 'score' property descending
    sorted_chunks = sorted(chunks, key=lambda c: c["score"], reverse=True)
    chunks_fitting_budget = []
    current_words = 0

    for c in sorted_chunks:
        word_count = len(c["text"].split())
        # Stop before adding if it exceeds the limit
        if current_words + word_count >= budget:
            break
        chunks_fitting_budget.append(c)
        current_words += word_count

    print(f"Budget: {budget}, chunks fitting: {len(chunks_fitting_budget)}")
    
    return chunks_fitting_budget


def generate_prompt(question: str, chunks:list[dict]) -> list[dict]:
    system_prompt = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }

    context = "\n\n".join(f"Context {i+1}:\n{chunk}" for i, chunk in enumerate([c["text"] for c in chunks]))
    content = f"{context}\n\nQuestion: {question}"

    user_prompt = {
        "role": "user",
        "content": content
    }
    
    return [system_prompt, user_prompt]
