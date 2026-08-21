import json
import re
from pathlib import Path

import fitz


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REGULATIONS_DIR = PROJECT_ROOT / "data" / "raw" / "regulations"
CONTRACTS_DIR = PROJECT_ROOT / "data" / "raw" / "contracts"

PROCESSED_REGULATIONS_DIR = (
    PROJECT_ROOT / "data" / "processed" / "regulations"
)
PROCESSED_CONTRACTS_DIR = (
    PROJECT_ROOT / "data" / "processed" / "contracts"
)


def clean_text(text: str) -> str:
    """Clean extracted document text."""

    text = text.replace("\x00", " ")

    # Normalize whitespace while preserving paragraphs.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def chunk_text(text: str, max_chars: int = 1500) -> list[str]:
    """
    Split text into reasonably sized chunks.

    We prefer paragraph boundaries so that clauses remain readable.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if not current_chunk:
            current_chunk = paragraph
            continue

        candidate = current_chunk + "\n\n" + paragraph

        if len(candidate) <= max_chars:
            current_chunk = candidate
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def extract_pdf_pages(pdf_path: Path) -> list[dict]:
    """Extract text page by page from a PDF."""

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = clean_text(page.get_text())

        if text:
            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    document.close()

    return pages


def process_regulation(pdf_path: Path) -> list[dict]:
    """Convert a regulation PDF into searchable chunks."""

    document_id = pdf_path.stem

    pages = extract_pdf_pages(pdf_path)

    records = []

    for page_data in pages:
        chunks = chunk_text(page_data["text"])

        for chunk_number, chunk in enumerate(chunks, start=1):
            records.append(
                {
                    "document_id": document_id,
                    "document_type": "regulation",
                    "title": pdf_path.stem.replace("_", " ").title(),
                    "source": "official_indian_regulation",
                    "jurisdiction": "India",
                    "file_name": pdf_path.name,
                    "page": page_data["page"],
                    "chunk_id": f"{document_id}_p{page_data['page']}_c{chunk_number}",
                    "text": chunk,
                }
            )

    return records


def process_contract(contract_path: Path) -> list[dict]:
    """Convert a contract or policy into searchable chunks."""

    document_id = contract_path.stem

    text = contract_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    text = clean_text(text)

    chunks = chunk_text(text)

    records = []

    for chunk_number, chunk in enumerate(chunks, start=1):
        records.append(
            {
                "document_id": document_id,
                "document_type": "company_document",
                "title": contract_path.stem.replace("_", " ").title(),
                "source": "synthetic",
                "jurisdiction": "India",
                "file_name": contract_path.name,
                "page": None,
                "chunk_id": f"{document_id}_c{chunk_number}",
                "text": chunk,
            }
        )

    return records


def write_jsonl(records: list[dict], output_path: Path) -> None:
    """Write records in JSON Lines format."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )


def build_regulation_corpus() -> None:
    """Process all regulatory PDFs."""

    all_records = []

    pdf_files = sorted(REGULATIONS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No regulatory PDFs found.")
        return

    for pdf_file in pdf_files:
        print(f"Processing regulation: {pdf_file.name}")

        records = process_regulation(pdf_file)

        output_file = (
            PROCESSED_REGULATIONS_DIR
            / f"{pdf_file.stem}.jsonl"
        )

        write_jsonl(records, output_file)

        print(
            f"  Created {len(records)} chunks -> "
            f"{output_file.name}"
        )

        all_records.extend(records)

    combined_output = (
        PROCESSED_REGULATIONS_DIR / "regulations.jsonl"
    )

    write_jsonl(
        all_records,
        combined_output,
    )

    print(
        f"\nTotal regulatory chunks: {len(all_records)}"
    )


def build_contract_corpus() -> None:
    """Process all company contracts and policies."""

    all_records = []

    contract_files = sorted(
        CONTRACTS_DIR.glob("*.txt")
    )

    if not contract_files:
        print("No contract documents found.")
        return

    for contract_file in contract_files:
        print(f"Processing contract: {contract_file.name}")

        records = process_contract(contract_file)

        all_records.extend(records)

        print(
            f"  Created {len(records)} chunks"
        )

    output_file = (
        PROCESSED_CONTRACTS_DIR
        / "contracts.jsonl"
    )

    write_jsonl(
        all_records,
        output_file,
    )

    print(
        f"\nTotal contract chunks: {len(all_records)}"
    )


def main() -> None:
    print("=" * 60)
    print("REGUARD CORPUS BUILDER")
    print("=" * 60)

    print("\nBuilding regulatory corpus...")
    build_regulation_corpus()

    print("\nBuilding contract corpus...")
    build_contract_corpus()

    print("\nCorpus construction complete.")


if __name__ == "__main__":
    main()