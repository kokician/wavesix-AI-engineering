import json
import os

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "memory_store.json")

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def append_to_memory(user_input, summary):
    memory = load_memory()
    memory[user_input] = summary
    save_memory(memory)

def retrieve_summary(user_input):
    memory = load_memory()
    return memory.get(user_input)
