from agent import run_agent

def main():
    print(" GitAgent-lite - Find the Best GitHub Tool for Your Task\n")
    user_goal = input("Enter your goal (e.g., 'extract text from PDFs'): ")

    print("\n Thinking...")
    result = run_agent(user_goal)

    print("\n Final Recommendation:\n")
    print(result)

if __name__ == "__main__":
    main()
