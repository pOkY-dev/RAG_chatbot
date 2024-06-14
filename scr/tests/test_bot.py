import pytest
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder
from query_handler import handle_complex_queries

TOKEN = '7457454740:AAHwDNrD3uRh8cNiByDmoR1wSn4fMJZPQBs'
bot = Bot(token=TOKEN)

@pytest.fixture
def telegram_app():
    app = ApplicationBuilder().token(TOKEN).build()
    return app

def test_start(telegram_app):
    # Test the /start command
    update = Update(update_id=1, message=None)  # Create an update instance with a mock message
    context = telegram_app.dispatcher.bot
    response = start(update, context)
    assert "Hello! How can I help you with your car rental needs?" in response.text

def test_clear(telegram_app):
    # Test the /clear command
    update = Update(update_id=1, message=None)  # Create an update instance with a mock message
    context = telegram_app.dispatcher.bot
    response = clear(update, context)
    assert "Memory cleared! How can I help you next?" in response.text

def test_handle_message(telegram_app):
    # Test handling a message
    update = Update(update_id=1, message=None)  # Create an update instance with a mock message
    context = telegram_app.dispatcher.bot
    user_query = "Find an SUV in Spain"
    response = handle_complex_queries(user_query)
    assert "Brand" in response
    assert "Model" in response
