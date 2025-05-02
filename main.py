import telebot
from dotenv import load_dotenv
import os
import OpenAI

load_dotenv()

telegram_api_key = os.getenv("TELEGRAM_BOT_API_KEY")

bot = telebot.TeleBot(telegram_api_key)
print("Started telegram bot")

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     print(message)
#     bot.reply_to(message, message.text)

command = telebot.types.BotCommand("start", "Start the bot")


# @bot.set_my_commands([command], scope=telebot.types.BotCommandScopeDefault())
@bot.message_handler(commands=["chatgpt"])
def openai(message):
    bot.reply_to(
        message,
        "OpenAI is an AI research and deployment company. Their mission is to ensure that artificial general intelligence (AGI) benefits all of humanity.",
    )


@bot.message_handler(commands=["dalle"])
def openai(message):
    ForceReply = telebot.types.ForceReply(selective=True)
    bot.send_message(
        message.chat.id,
        "Please enter a prompt for DALL-E to generate an image.",
        reply_markup=ForceReply,
    )
    bot.register_next_step_handler(message, process_dalle_prompt)


def process_dalle_prompt(message):
    bot.send_message(message.chat.id, "Generating image...")
    imageurl, revisedprompt = OpenAI.get_dalle_image(message.text)
    if imageurl is not None:
        bot.send_photo(
            message.chat.id, imageurl, caption="Used revised prompt: " + revisedprompt
        )
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, I couldn't generate an image. Please try again later.",
        )


bot.infinity_polling()
