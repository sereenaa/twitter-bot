from dotenv import load_dotenv
import os
import telebot
import time 

load_dotenv()
TOKEN = os.environ['NOTNOTXSPYBOT_TOKEN']

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    print(message.text)
    bot.send_message(message.chat.id, "hi pibbles")








while True: 
    try: 
        bot.polling()
    except: 
        time.sleep(5)