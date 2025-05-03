import telebot
from dotenv import dotenv_values
import os
import OpenAI

config = dotenv_values(".env")
print(config)
telegram_api_key = os.getenv("TELEGRAM_BOT_API_KEY")
bot = telebot.TeleBot(telegram_api_key)
print("Started telegram bot")


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=["chatgpt"])
def openai(message):
    ForceReply = telebot.types.ForceReply(selective=True)
    bot.send_message(
        message.chat.id,
        "Please enter your question to ChatGPT",
        reply_markup=ForceReply,
    )
    bot.register_next_step_handler(message, process_chatgpt_prompt)


def process_chatgpt_prompt(message):
    response = OpenAI.get_chatgpt_response(message.text)
    if response is not None:
        try:
            bot.send_message(message.chat.id, response, parse_mode="Markdown")
        except telebot.apihelper.ApiException as e:
            print(f"Error sending message: {e}")
            bot.send_message(
                message.chat.id,
                "Sorry, I couldn't send the response. Please try again later.",
            )
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, I couldn't generate a response. Please try again later.",
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
