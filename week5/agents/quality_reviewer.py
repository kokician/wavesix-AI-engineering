from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

class QualityReviewerAgent:
    def __init__(self, memory):
        self.memory = memory
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.2)
        self.chain = ConversationChain(llm=self.llm, memory=self.memory)

    def run(self, summaries: list[str]) -> list[str]:
        improved = []
        for summary in summaries:
            review_prompt = f"Review this changelog entry for clarity and tone. Suggest improvements:\n\n{summary}"
            result = self.chain.run(review_prompt)
            improved.append(result)
        return improved
