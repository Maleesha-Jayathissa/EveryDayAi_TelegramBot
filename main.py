from dotenv import load_dotenv
from langchain_groq import ChatGroq
import telebot
import os

#below code used for flusk server from claude to keep bot alive
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)
#end

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")
bot = telebot.TeleBot(token=os.getenv("API_TOKEN"))

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = 'Welcome! What do you want to know?'
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_reply(message):
    query=message.text
    messages = [
    ("system", "Reply in one short plain paragraph only. No extra details, no symbols, no markdown, no lists."),
    ("human", query),
    ]  
    output=llm.invoke(messages).content
    bot.reply_to(message,output)
    bot.send_message(message.chat.id, "What else do you want to know?")


Thread(target=run_web).start()
bot.infinity_polling()