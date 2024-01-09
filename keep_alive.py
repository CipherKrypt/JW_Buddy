"""
A function that will generate a webpage that can be pinged to keep the bot alive.
"""

from flask import Flask
from threading import Thread

app=Flask('')

@app.route('/')
def home():
  return('Telebot is alive')

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t=Thread(target=run)
  t.start()
