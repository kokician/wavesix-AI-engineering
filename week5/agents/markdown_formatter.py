class MarkdownFormatterAgent:
    def __init__(self, memory):
        self.memory = memory

    def run(self, entries: list[str]) -> str:
        self.memory.save_context({"input": "final summaries"}, {"output": str(entries)})
        return "# Release Notes\n\n" + "\n".join(f"- {entry}" for entry in entries)
