import time
from typing import List, Dict

# from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODELS = [
    "all-MiniLM-L6-v2",
    "all-mpnet-base-v2"
]

CHUNK_SIZES = [256, 512, 1024]

CHUNK_OVERLAPS = [20, 50, 100]

TOP_K = 5


documents = [
    "Employees must complete cybersecurity training every year.",
    "Annual leave can be applied through the HR portal.",
    "Managers approve reimbursement requests.",
    "Passwords must be changed every 90 days.",
    "Employees should report phishing emails immediately.",
    "Remote work is allowed twice a week."
]


queries = [
    {
        "question": "How often should passwords be changed?",
        "answer": "Passwords must be changed every 90 days."
    },
    {
        "question": "Where do I apply for leave?",
        "answer": "Annual leave can be applied through the HR portal."
    },
    {
        "question": "Who approves reimbursements?",
        "answer": "Managers approve reimbursement requests."
    }
]


def chunk_documents(chunk_size, overlap):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    chunks = []

    for doc in documents:
        chunks.extend(splitter.split_text(doc))

    return chunks


def benchmark_model(model_name, chunk_size, overlap):

    embedding = HuggingFaceEmbeddings(
        model_name=f"sentence-transformers/{model_name}"
    )

    chunks = chunk_documents(chunk_size, overlap)

    start = time.time()

    vector_store = FAISS.from_texts(
        chunks,
        embedding
    )

    build_time = time.time() - start

    total_latency = 0
    correct = 0

    for item in queries:

        start = time.time()

        results = vector_store.similarity_search(
            item["question"],
            k=TOP_K
        )

        latency = time.time() - start
        total_latency += latency

        retrieved = [doc.page_content for doc in results]

        if item["answer"] in retrieved:
            correct += 1

    accuracy = correct / len(queries)
    avg_latency = total_latency / len(queries)

    return {
        "model": model_name,
        "chunk_size": chunk_size,
        "chunk_overlap": overlap,
        "build_time": round(build_time, 4),
        "latency": round(avg_latency, 4),
        "accuracy": round(accuracy, 2)
    }

def run_benchmark():

    results = []

    for model in EMBEDDING_MODELS:

        for chunk_size in CHUNK_SIZES:

            for overlap in CHUNK_OVERLAPS:

                result = benchmark_model(
                    model,
                    chunk_size,
                    overlap
                )

                results.append(result)

                print(result)

    generate_report(results)


import os

def generate_report(results: List[Dict]):

    # Create the evaluation directory if it doesn't exist
    os.makedirs("evaluation", exist_ok=True)

    with open(
        "evaluation/retrieval_report.md",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("# Retrieval Benchmark Report\n\n")

        file.write("|Embedding Model|Chunk Size|Overlap|Latency(s)|Accuracy|Build Time(s)|\n")
        file.write("|---|---|---|---|---|---|\n")

        for row in results:
            file.write(
                f"|{row['model']}|"
                f"{row['chunk_size']}|"
                f"{row['chunk_overlap']}|"
                f"{row['latency']}|"
                f"{row['accuracy']}|"
                f"{row['build_time']}|\n"
            )

        best = max(results, key=lambda x: x["accuracy"])

        file.write("\n## Best Configuration\n\n")
        file.write(f"- Embedding Model: {best['model']}\n")
        file.write(f"- Chunk Size: {best['chunk_size']}\n")
        file.write(f"- Chunk Overlap: {best['chunk_overlap']}\n")
        file.write(f"- Accuracy: {best['accuracy']}\n")
        file.write(f"- Average Latency: {best['latency']} sec\n")

if __name__ == "__main__":
    run_benchmark()