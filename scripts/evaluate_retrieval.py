import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from reguard.evaluation import (
    f1_at_k,
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
) -> dict:
    """Evaluate one retrieval method."""

    precisions = []
    recalls = []
    f1_scores = []
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

        f1 = f1_at_k(
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
        f1_scores.append(f1)
        reciprocal_ranks.append(rr)

        print(
            f"\n{query_data['query_id']}: "
            f"{query}"
        )

        print(
            f"Retrieved: {retrieved}"
        )

        print(
            f"P@{k}: {precision:.3f} | "
            f"R@{k}: {recall:.3f} | "
            f"F1@{k}: {f1:.3f} | "
            f"RR: {rr:.3f}"
        )

    summary = {
        "method": method,
        "queries": len(queries),
        "precision_at_k": (
            sum(precisions)
            / len(precisions)
        ),
        "recall_at_k": (
            sum(recalls)
            / len(recalls)
        ),
        "f1_at_k": (
            sum(f1_scores)
            / len(f1_scores)
        ),
        "mrr": (
            sum(reciprocal_ranks)
            / len(reciprocal_ranks)
        ),
    }

    return summary


def print_summary(
    summaries: list[dict],
    k: int,
) -> None:
    """Print a compact comparison table."""

    print("\n")
    print("=" * 70)
    print("TRADITIONAL IR BASELINE")
    print("=" * 70)

    print(
        f"{'Method':<12}"
        f"{'P@' + str(k):<10}"
        f"{'R@' + str(k):<10}"
        f"{'F1@' + str(k):<10}"
        f"{'MRR':<10}"
    )

    print("-" * 70)

    for summary in summaries:
        print(
            f"{summary['method']:<12}"
            f"{summary['precision_at_k']:<10.3f}"
            f"{summary['recall_at_k']:<10.3f}"
            f"{summary['f1_at_k']:<10.3f}"
            f"{summary['mrr']:<10.3f}"
        )


def main() -> None:

    retriever = TraditionalRetriever()

    queries = load_queries()

    k = 5

    summaries = []

    summaries.append(
        evaluate_method(
            retriever,
            "tfidf",
            queries,
            k,
        )
    )

    summaries.append(
        evaluate_method(
            retriever,
            "bm25",
            queries,
            k,
        )
    )

    print_summary(
        summaries,
        k,
    )


if __name__ == "__main__":
    main()