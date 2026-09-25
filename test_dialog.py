from dialog_manager import get_response

print("===== College Chatbot Test =====\n")
print("Type 'exit' to stop\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Bot: Thank you! Have a great day.")
        break
    
    response = get_response(user_input)
    print("Bot:", response)
    print()
