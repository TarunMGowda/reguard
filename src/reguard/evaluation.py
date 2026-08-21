import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

QUERIES_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "queries.json"
)


def load_queries() -> list[dict]:
    """Load evaluation queries."""

    with QUERIES_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def precision_at_k(
    retrieved: list[str],
    relevant: set[str],
    k: int,
) -> float:
    """Calculate Precision@K."""

    retrieved_at_k = retrieved[:k]

    if not retrieved_at_k:
        return 0.0

    relevant_count = sum(
        document_id in relevant
        for document_id in retrieved_at_k
    )

    return relevant_count / len(
        retrieved_at_k
    )


def recall_at_k(
    retrieved: list[str],
    relevant: set[str],
    k: int,
) -> float:
    """Calculate Recall@K."""

    if not relevant:
        return 0.0

    retrieved_at_k = retrieved[:k]

    relevant_count = sum(
        document_id in relevant
        for document_id in retrieved_at_k
    )

    return relevant_count / len(relevant)


def reciprocal_rank(
    retrieved: list[str],
    relevant: set[str],
) -> float:
    """Calculate Reciprocal Rank."""

    for rank, document_id in enumerate(
        retrieved,
        start=1,
    ):
        if document_id in relevant:
            return 1.0 / rank

    return 0.0