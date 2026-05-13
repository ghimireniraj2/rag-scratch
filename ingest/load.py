import pdfplumber
import re

def load_pdf(file:str) -> list[dict]:
    pages = []

    try:
        with pdfplumber.open(file) as pdf:
            print(f"Loading pdf file:", {file})

            for i, page in enumerate(pdf.pages[:30]):
                page_text = page.extract_text()
                if page_text:
                    pages.append({"page": i + 1, "text": page_text})

    except FileNotFoundError:
        print(f"file not found", {file})
        return []
    
    return pages

def get_max(strings:list[str]):
    return max(len(s) for s in strings)

def get_min(strings:list[str]):
    return min(len(s) for s in strings)

def get_average(strings:list[str]):
    return sum(len(s) for s in strings) / len(strings)


def chunk_fixed(text: str, size: int = 512) -> list[str]:
    return [text[i:i + size] for i in range(0, len(text), size)]

def chunk_sentences(text: str, n: int = 5) -> list[str]:
    sentences = re.split(r'(?<=[.?!])\s+', text)
    return ["".join(sentences[i: i + n]) for i in range(0, len(sentences), n)]

def chunk_sliding(text: str, size: int = 512, step: int = 256) -> list[str]:
    return [text[i:i + size] for i in range(0, len(text), step) if len(text[i:i + size]) > 50]

def chunk_stats(strings:list[str]):
    print(f"Chunks count: {len(strings)}")
    print(f"Min chunk size: {get_min(strings)}")
    print(f"Max chunk size: {get_max(strings)}")
    print(f"Average chunk size: {get_average(strings)}")
    print()



# pages = load_pdf(file="../data/raw/openstax-prealgebra.pdf")
# print(pages[2]["text"])

# chunks_fixed = chunk_fixed(pages[2]["text"])
# print("Statistics for chunk_fixed")
# chunk_stats(chunks_fixed)

# chunks_sentences = chunk_sentences(pages[2]["text"])
# print("Statistics for chunks_sentences")
# chunk_stats(chunks_sentences)

# chunks_sliding = chunk_sliding(pages[2]["text"])
# print("Statistics for chunks_sliding")
# chunk_stats(chunks_sliding)

# for chunk in chunks_fixed:
#     print(chunk)
#     print()
