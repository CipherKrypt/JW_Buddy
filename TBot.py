"""
The main chatbot function.
Initiates the chatbot using API Key.
"""

import os
from dotenv import load_dotenv
from telebot import TeleBot,types
from telebot import *
from Messages import Message

def bot():
  load_dotenv()
  API_KEY = os.environ['API_KEY']
  bot = telebot.TeleBot(API_KEY)
  
  
  @bot.callback_query_handler(func=lambda call: True)
  def callbacks(query: str, trial=1):
      if trial == 6:
          raise Exception('To many tries')
      try:
          data = query.data
          message = query.message
          if data.startswith('start_'):
              if data.lstrip('start_').startswith('hi_'):
                  bot.delete_message(message.chat.id, message.id)
                  bot.send_message(message.chat.id, 'Hi there')
      except Exception as Err:
          print(Err)
  
  
  @bot.message_handler(commands=['start'])
  def start_message(message):
      keyboard = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton(
          'Hi', callback_data=f'start_hi_{message.chat.id}')
      keyboard.add(button)
      bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard)
  
  
  @bot.message_handler(commands=['done'])
  def done_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        'Done', callback_data=f'start_hi_{message.chat.id}')
    keyboard.add(button)
  
    m = Message(message.json)
    print(m.text)
    bot.send_message(m.chat.chat_id, 'Hello', reply_markup=keyboard)
  
  while True:
    try:
      bot.polling()
    except Exception as Err:
      print(f"An Error occurred: {Err}")
  