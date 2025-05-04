import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer
import ray
import unicodedata


# --- Config ---
LABEL_PATH = "/Users/tanmay/Downloads/US_Sol_LLM/email-policy-ai/data/raw/policy_labels.jsonl"
MODEL_NAME = "distilroberta-base"
TEST_SIZE = 0.2
MAX_LENGTH = 512
SEED = 42
OUTPUT_DIR = "/Users/tanmay/Downloads/US_Sol_LLM/email-policy-ai/data/processed"

# --- Initialize Tokenizer ---
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

# --- Load and Normalize Multi-class Labels ---

def normalize_text(text):
    # Normalize unicode characters (e.g., curly quotes to ASCII)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("utf-8").strip()

def load_jsonl(path):
    records = []
    labels_set = set()

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            try:
                obj = json.loads(line)
                text = normalize_text(obj.get("text", ""))
                label = obj.get("label", "").strip()
                if text and label:
                    labels_set.add(label)
                    records.append({"text": text, "label": label})
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error on line {i}: {e}")

    df = pd.DataFrame(records)

    # Create label2id mappings
    label2id = {label: idx for idx, label in enumerate(sorted(labels_set))}
    id2label = {v: k for k, v in label2id.items()}
    df["label"] = df["label"].map(label2id)

    return df, label2id, id2label


# --- Tokenization Function ---
def tokenize_function(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="np"
    )

# --- Prepare Dataset Function ---
def prepare_dataset():
    df, label2id, id2label = load_jsonl(LABEL_PATH)

    # Train/test split with stratification
    train_df, test_df = train_test_split(
        df,
        test_size=TEST_SIZE,
        stratify=df['label'],
        random_state=SEED
    )

    # Convert to HuggingFace Datasets
    dataset = DatasetDict({
        "train": Dataset.from_pandas(train_df.reset_index(drop=True)),
        "test": Dataset.from_pandas(test_df.reset_index(drop=True))
    })

    # Tokenize the dataset
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

    return tokenized_dataset, label2id, id2label

# --- Ray Entry Point ---
@ray.remote
def preprocess_and_save():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dataset, label2id, id2label = prepare_dataset()
    dataset["train"].to_json(os.path.join(OUTPUT_DIR, "train_tokenized.jsonl"))
    dataset["test"].to_json(os.path.join(OUTPUT_DIR, "test_tokenized.jsonl"))

    with open(os.path.join(OUTPUT_DIR, "label2id.json"), "w") as f:
        json.dump(label2id, f, indent=2)
    with open(os.path.join(OUTPUT_DIR, "id2label.json"), "w") as f:
        json.dump(id2label, f, indent=2)

    print("✅ Tokenized dataset and label mappings saved. Ready for training.")

# --- CLI Execution ---
if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)
    ray.get(preprocess_and_save.remote())
    ray.shutdown()
