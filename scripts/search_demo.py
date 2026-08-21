import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from reguard.retriever import TraditionalRetriever

def print_document_results(
    results: list[dict],
) -> None:

    for result in results:
        print("-" * 70)

        print(
            f"Rank:  {result['rank']}"
        )

        print(
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Document: {result['document_id']}"
        )

        print(
            f"File: {result['file_name']}"
        )

        print(
            f"Best matching clause: "
            f"{result['best_chunk']['chunk_id']}"
        )

        print(
            f"Clause text:\n"
            f"{result['best_chunk']['text']}"
        )


def main() -> None:

    retriever = TraditionalRetriever()

    query = (
        "technical organizational measures "
        "security safeguards protect personal data"
    )

    print("\n" + "=" * 70)
    print("TF-IDF DOCUMENT RESULTS")
    print("=" * 70)

    tfidf_results = (
        retriever.search_documents_tfidf(
            query,
            top_k=5,
        )
    )

    print_document_results(tfidf_results)

    print("\n" + "=" * 70)
    print("BM25 DOCUMENT RESULTS")
    print("=" * 70)

    bm25_results = (
        retriever.search_documents_bm25(
            query,
            top_k=5,
        )
    )

    print_document_results(bm25_results)


if __name__ == "__main__":
    main()
