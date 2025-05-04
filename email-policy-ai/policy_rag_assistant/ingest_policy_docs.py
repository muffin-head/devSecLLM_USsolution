import fitz  # PyMuPDF
import os
import re
import json
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# --- Config ---
PDF_DIR = "/Users/tanmay/Downloads/US_Sol_LLM/email-policy-ai/data/raw"
PROCESSED_JSON = "/Users/tanmay/Downloads/US_Sol_LLM/email-policy-ai/data/processed/policy_rules.json"
QDRANT_HOST = "localhost"  # Change if using cloud endpoint
QDRANT_PORT = 6333
COLLECTION_NAME = "policy_rules"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Initialize ---
model = SentenceTransformer(EMBEDDING_MODEL)
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# --- Helper: Extract Sections ---
def extract_sections(text):
    sections = []
    pattern = re.compile(r"(?<=\n)(\d{1,2}\.?\s+[A-Z][^\n]{5,})(?=\n)")
    matches = list(pattern.finditer(text))

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading = match.group(1).strip()
        content = text[start:end].strip()
        if content:
            sections.append({"title": heading, "content": content})
    return sections

# --- Helper: PDF to Text ---
def pdf_to_text(filepath):
    doc = fitz.open(filepath)
    return "\n".join([page.get_text() for page in doc])


def clean_content(text):
    # Remove visible bullets and sub-bullets
    text = text.replace("\u2022", " ")  # black bullet (•)
    text = text.replace("\u25cb", " ")  # hollow bullet (○)
    text = text.replace("\u25cf", " ")  # filled bullet (●)

    # Remove invisible characters (zero-width spaces, etc.)
    text = re.sub(r"[\u200b\u200c\u200d]", "", text)

    # Normalize whitespace: collapse multiple spaces, trim
    text = re.sub(r"\s+", " ", text).strip()

    return text


# --- Process PDFs ---
def process_pdfs(pdf_dir):
    all_sections = []
    for file in os.listdir(pdf_dir):
        if not file.endswith(".pdf"):
            continue
        text = pdf_to_text(os.path.join(pdf_dir, file))
        sections = extract_sections(text)

        meta = {
            "source": file,
            "timestamp": datetime.utcnow().isoformat(),
        }

        for section in sections:
            record = {
                "title": section["title"],
                "content": clean_content(section["content"].lower()),  # 🧼 cleaning applied here
                "metadata": meta,
            }
            all_sections.append(record)
    return all_sections


# --- Save to JSON ---
def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# --- Upload to Qdrant Vector DB ---
def upload_to_qdrant(records):
    if COLLECTION_NAME not in client.get_collections().collections:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE),
        )

    points = []
    for idx, rec in enumerate(records):
        vector = model.encode(rec["content"]).tolist()
        payload = {
            "title": rec["title"],
            "source": rec["metadata"]["source"],
            "timestamp": rec["metadata"]["timestamp"]
        }
        points.append(PointStruct(id=idx, vector=vector, payload=payload))

    client.upsert(collection_name=COLLECTION_NAME, points=points)


if __name__ == "__main__":
    records = process_pdfs(PDF_DIR)
    save_json(records, PROCESSED_JSON)
    upload_to_qdrant(records)
    print(f"✅ Processed and indexed {len(records)} policy sections.")
