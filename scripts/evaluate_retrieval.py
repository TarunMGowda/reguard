import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from reguard.evaluation import (
    load_queries,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)

from reguard.retriever import (
    TraditionalRetriever,
)


def evaluate_method(
    retriever: TraditionalRetriever,
    method: str,
    queries: list[dict],
    k: int = 5,
) -> None:

    precisions = []
    recalls = []
    reciprocal_ranks = []

    print("\n" + "=" * 70)
    print(f"{method.upper()} EVALUATION")
    print("=" * 70)

    for query_data in queries:

        query = query_data["query"]

        relevant = set(
            query_data["relevant_documents"]
        )

        if method == "tfidf":
            results = (
                retriever.search_documents_tfidf(
                    query,
                    top_k=k,
                )
            )

        elif method == "bm25":
            results = (
                retriever.search_documents_bm25(
                    query,
                    top_k=k,
                )
            )

        else:
            raise ValueError(
                f"Unknown method: {method}"
            )

        retrieved = [
            result["document_id"]
            for result in results
        ]

        precision = precision_at_k(
            retrieved,
            relevant,
            k,
        )

        recall = recall_at_k(
            retrieved,
            relevant,
            k,
        )

        rr = reciprocal_rank(
            retrieved,
            relevant,
        )

        precisions.append(precision)
        recalls.append(recall)
        reciprocal_ranks.append(rr)

        print(f"\nQuery: {query}")

        print(
            f"Retrieved: {retrieved}"
        )

        print(
            f"Precision@{k}: {precision:.3f}"
        )

        print(
            f"Recall@{k}:    {recall:.3f}"
        )

        print(
            f"Reciprocal Rank: {rr:.3f}"
        )

    print("\n" + "-" * 70)

    print(
        f"Mean Precision@{k}: "
        f"{sum(precisions) / len(precisions):.3f}"
    )

    print(
        f"Mean Recall@{k}:    "
        f"{sum(recalls) / len(recalls):.3f}"
    )

    print(
        f"MRR: "
        f"{sum(reciprocal_ranks) / len(reciprocal_ranks):.3f}"
    )


def main() -> None:

    retriever = TraditionalRetriever()

    queries = load_queries()

    evaluate_method(
        retriever,
        "tfidf",
        queries,
        k=5,
    )

    evaluate_method(
        retriever,
        "bm25",
        queries,
        k=5,
    )


if __name__ == "__main__":
    main()