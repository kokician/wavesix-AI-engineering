import asyncio
import os
import sys
import datetime
import logging

sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
from agent.github_agents import github_agent
from agents import Runner

load_dotenv()

# Set up logging to a file
log_file = "agent_log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY in .env")
        sys.exit(1)

    print("GitHub Agent is ready. Type your question or 'exit' to quit.\n")

    while True:
        user_input = input("Ask the GitHub Agent anything: ")

        if user_input.strip().lower() in ["exit", "quit"]:
            print("Exiting. Goodbye!")
            break

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] Processing your query...\n")

        try:
            result = await Runner.run(github_agent, user_input)
            response = result.final_output

            print("\n=== AGENT RESPONSE ===\n")
            print(response)

            logging.info(f"USER: {user_input}")
            logging.info(f"AGENT: {response}")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            logging.error(error_msg)

if __name__ == "__main__":
    asyncio.run(main())
