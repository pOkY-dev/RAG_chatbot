from query_handler import QueryHandler

def cli_chatbot():
    print("Welcome to the rental car chatbot!")
    bot = QueryHandler('rental_car_index.pkl')
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/clear':
            print("Memory cleared! How can I help you next?")
            continue
        response = bot.handle_query(user_input)
        print("Bot:", response)

if __name__ == '__main__':
    cli_chatbot()