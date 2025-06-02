from dotenv import load_dotenv

from memory import get_memory, save_context, get_memory_qa_chain
from agents.issue_collector import IssueCollectorAgent
from agents.content_summarizer import ContentSummarizerAgent
from agents.quality_reviewer import QualityReviewerAgent
from agents.markdown_formatter import MarkdownFormatterAgent

from nl_to_repo import get_repo_url_from_nl

load_dotenv()


def run_pipeline(repo_url: str):
    memory = get_memory()

    issues = IssueCollectorAgent(repo_url, memory).run()
    summaries = ContentSummarizerAgent(memory).run(issues)
    refined = QualityReviewerAgent(memory).run(summaries)
    markdown = MarkdownFormatterAgent(memory).run(refined)

    print("\n=== Release Notes ===\n")
    print(markdown)

    save_context(memory, "Final formatted notes", markdown)


def run_pipeline_with_natural_language():
    query = input("Describe the Python library or repo you're interested in:\n> ")
    repo_url = get_repo_url_from_nl(query)
    if repo_url:
        print(f"Identified repository: {repo_url}")
        run_pipeline(repo_url)
    else:
        print("Sorry, couldn't find a matching repository.")


def query_memory():
    qa = get_memory_qa_chain()
    while True:
        q = input("\nAsk memory (or type 'exit'): ")
        if q.lower() in ["exit", "quit"]:
            break
        try:
            response = qa.invoke({"query": q})
            print("Answer:", response['result']) 
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("1. Run release note generator with repository URL")
    print("2. Run release note generator with natural language query")
    print("3. Query memory")
    print("4. Exit")

    choice = input("\nChoose [1/2/3/4]: ").strip()

    if choice == "1":
        repo_url = input("\nEnter GitHub repo URL:\n> ").strip()
        run_pipeline(repo_url)
    elif choice == "2":
        run_pipeline_with_natural_language()
    elif choice == "3":
        query_memory()
    else:
        print("Exiting.")
