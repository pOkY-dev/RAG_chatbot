from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from query_handler import handle_complex_queries, get_lowest_priced_cars
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '7457454740:AAHwDNrD3uRh8cNiByDmoR1wSn4fMJZPQBs'

async def start(update: Update, context):
    await update.message.reply_text('Hello! How can I help you with your car rental needs?')

async def clear(update: Update, context):
    context.user_data.clear()
    await update.message.reply_text('Memory cleared! How can I help you next?')

async def handle_message(update: Update, context):
    user_query = update.message.text

    try:
        if user_query.startswith("Give me a list of 3 cars with lowest price in both locations"):
            locations = ["Spain", "Italy"] 
            cars = get_lowest_priced_cars(locations=locations)
            response = "\n".join([f"Brand: {car['Brand']}, Model: {car['Model']}, Price: {car['Price']} euro/day, Location: {car['Location']}" for car in cars])
        else:
            response = handle_complex_queries(user_query)
        
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Error handling message '{user_query}': {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('clear', clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
