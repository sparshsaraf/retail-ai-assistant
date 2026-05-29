from dotenv import load_dotenv
load_dotenv()

from agent.agent_loop import run_agent

def main():
    print("=== Retail AI Assistant ===")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        print("\nAssistant: ", end="", flush=True)
        response = run_agent(user_input)
        print(response)
        print()

if __name__ == "__main__":
    main()