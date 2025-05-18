import os
import json

def save_vectors(vectors, file_path: str):
    """Save vectors to a JSON file, creating directories if needed."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(vectors, f)

def load_vectors(file_path: str):
    """Load vectors from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)
