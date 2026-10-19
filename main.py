from dotenv import load_dotenv
from langchain_groq import ChatGroq
import telebot
import os
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
bot.infinity_polling()
