from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

class ContentSummarizerAgent:
    def __init__(self, memory):
        self.memory = memory
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        self.chain = ConversationChain(llm=self.llm, memory=self.memory)

    def run(self, issues: list[str]) -> list[str]:
        summaries = []
        for issue in issues:
            prompt = f"Summarize this GitHub issue for a changelog entry:\n\n{issue}"
            result = self.chain.run(prompt)
            summaries.append(result)
        return summaries
