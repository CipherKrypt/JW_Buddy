"""
A Pbject implementation to make using the json data 
from the telegram bot easier.
Classes includes the...
Message Class: The main object that has data regarding chat, user and text.
User Class: Sub class implemented within the Message class to have data regarding user.
Chat Class: Sub class implemented within the Message class to have data regarding chat.
"""

class User():
    def __init__(self, user: dict):
      self.user_id = user['id']
      self.first_name = user['first_name']
      self.last_name = user['last_name']
      self.username = user['username']

class Chat():
  def __init__(self, chat: dict):
    self.chat_id = chat['id']
    self.first_name = chat['first_name']
    self.last_name = chat['last_name']
    self.username = chat['username']
    self.type = chat['type']
      
class Message():
  def __init__(self, message: dict):
    self.message_id = message['message_id']
    self.from_user = User(message['from'])
    self.chat = Chat(message['chat'])
    self.text = message['text']