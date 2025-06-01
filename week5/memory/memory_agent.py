from autogen import ConversableAgent
from memory.vector_memory import save_chat_memory, get_chat_memory

class MemoryAgent(ConversableAgent):
    def __init__(self, name):
        super().__init__(name)
        self.memory = ""

    def load_memory(self, repo_url):
        self.memory = get_chat_memory(repo_url)

    def remember(self, repo_url, new_msg):
        self.memory += f"\n{new_msg}"
        save_chat_memory(repo_url, self.memory)