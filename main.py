import telebot
from dotenv import load_dotenv
import os

load_dotenv()

telegram_api_key = os.getenv('TELEGRAM_BOT_API_KEY')

bot = telebot.TeleBot(telegram_api_key)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()