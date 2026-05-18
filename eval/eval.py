# Load questions.json
# For each question, call retrieve() and get top-k chunks
# Check if any of the expected keywords appear in any of the retrieved chunks
# Track how many questions passed at k=3 and k=5
# Print a summary table showing recall@3, recall@5, and breakdown by question type

# Strategy        | recall@3 | recall@5
# ----------------|----------|----------
# chunk_fixed     | 19/20    | 19/20
# chunk_sentences | 19/20    | 19/20
# chunk_sliding   | 19/20    | 19/20


import json
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
ingest_dir = current_dir.parent / "ingest"
sys.path.append(str(ingest_dir))

from qdrant_store import retrieve

def contains_expected_keywords(keywords: list[str], points: list[dict]) -> bool:
    any_exist = any(
        any(kw.lower() in p[0]["text"].lower() for kw in keywords) for p in points
    )
    return any_exist

with open("eval/questions.json", 'r') as json_file:
    questions = json.load(json_file)
    count_questions = len(questions)
    passed = 0
    failed = 0
    for question in questions:
        # print("---------- Question ------------")
        # print(question["question"])
        # print(question["expected_keywords"])
        # print(question["type"])
        # print("---------- Result ------------")

        #result = retrieve(collection="rag-sliding", query=question["question"], k=5)
        #result = retrieve(collection="rag-fixed", query=question["question"], k=5)
        result = retrieve(collection="rag-sentences", query=question["question"], k=5)
        #print(type(result))
        exists = contains_expected_keywords(keywords=question["expected_keywords"], points=result)
        if exists:
            passed += 1
            #print("Passed - Keywords exits")
        else:
            failed += 1
            #print("Failed - Keywords do not exits")
        
    print(f"Passed - {passed}")
    print(f"Failed - {failed}")



