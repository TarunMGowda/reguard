import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REGULATIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "regulations"
    / "regulations.jsonl"
)

CONTRACTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "contracts"
    / "contracts.jsonl"
)


REQUIRED_FIELDS = {
    "document_id",
    "document_type",
    "title",
    "source",
    "jurisdiction",
    "file_name",
    "chunk_id",
    "text",
}


def validate_file(path: Path) -> list[dict]:
    records = []

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line_number, line in enumerate(
            file,
            start=1,
        ):
            if not line.strip():
                continue

            record = json.loads(line)

            missing_fields = (
                REQUIRED_FIELDS
                - record.keys()
            )

            if missing_fields:
                raise ValueError(
                    f"{path.name}, line {line_number}: "
                    f"missing fields {missing_fields}"
                )

            if not record["text"].strip():
                raise ValueError(
                    f"{path.name}, line {line_number}: "
                    "empty text"
                )

            records.append(record)

    return records


def main() -> None:
    print("Validating Reguard corpus...\n")

    regulation_records = validate_file(
        REGULATIONS_FILE
    )

    contract_records = validate_file(
        CONTRACTS_FILE
    )

    print(
        f"Regulatory chunks: {len(regulation_records)}"
    )

    print(
        f"Contract chunks:   {len(contract_records)}"
    )

    regulation_documents = {
        record["document_id"]
        for record in regulation_records
    }

    contract_documents = {
        record["document_id"]
        for record in contract_records
    }

    print(
        f"Regulatory documents: {len(regulation_documents)}"
    )

    print(
        f"Company documents:    {len(contract_documents)}"
    )

    print("\nCorpus validation successful.")


if __name__ == "__main__":
    main()