"""
The main chatbot function.
Initiates the chatbot using API Key.
"""
import pickle
import os
import schedule
import time
import threading
from pytz import timezone
from dotenv import load_dotenv
from telebot import types, TeleBot
from telebot import *
from Messages import Message
from DBR import *
from Links import Links
from Users import ServiceUser as User, Users

DEVELOPMENT = True
def bot(fileName : str | None):

    ##### F U N C T I O N S #####

    def DB_save(DB):
        with open("DB.pickle", "wb") as file:
            pickle.dump(DB, file)
    def DB_load():
        with open("DB.pickle", "rb") as file:
            return pickle.load(file)

    #### U S E R S _ L I S T ######   
    def U_save(U):
        with open("U.pickle", "wb") as file:
            pickle.dump(U, file)
    def U_load():
        try:
            if U:
                return U
        except:
            with open("U.pickle", "rb") as file:
                return pickle.load(file)
        
    def read(fileName):
        with open(fileName + ".pickle", "rb") as file:
            return pickle.load(file)

    def save(fileName, AI):
        with open(fileName + ".pickle", "wb") as file:
            pickle.dump(AI,file)


#############################################            
    try:
        DB = DB_load()
    except:
        DB = dict()
        DB_save(DB)
    try:
        # if DEVELOPMENT:
        #     raise Exception("Under development")
        U =  U_load()
    except:
        U = Users()
        print(f"Created Users 'U' of type {type(U)}")
        U_save(U)
    load_dotenv()
    API_KEY = os.environ['API_KEY']
    bot = telebot.TeleBot(API_KEY)
    # bot = tb.AsyncTeleBot(API_KEY)
    AI = read(fileName)
#############################################
    

    ###### B O T #######

    """ HANDLING CALL-BACKS """
    @bot.callback_query_handler(func=lambda call: True)
    def callbacks(query: str, trial=1):
        if trial == 6:
            raise Exception('To many tries')
        try:
            print("Entering")
            data = query.data
            message = query.message


            """ IF FROM /start """
            if data.startswith('start_'):
                data = data.lstrip('start_')
                if data.startswith('hi_'):
                    bot.delete_message(message.chat.id, message.id)
                    bot.send_message(message.chat.id, 'Hi there')
                elif data.startswith('done_'):
                    m = Message(message.json)
                    bot.delete_message(message.chat.id, message.id)
                    bot.send_message(message.chat.id, f'Great work {m.from_user.first_name}!')  

            """ IF FROM /sub — day """        
            if data.startswith('day_'): 
                try:
                    data = data.lstrip('day_') 
                    user_id, day = data.split('_')  
                    try:
                        if U:
                            pass
                    except:
                        U  = U_load()
                    user = U[user_id]
                    user.waiting = (False,None)
                    user.day = day
                    U.update(user)
                    bot.send_message(message.chat.id, "You are all set now. Explore the commands. Some features are under development.")
                    U_save(U)
                except Exception as err:
                    print(err, "@ callback _day")




        except Exception as Err:
            print(Err)

    """ HANDLING '/' COMMANDS """
    @bot.message_handler(commands=['start'])
    # Welcomes the user
    def start_message(message):
        m = Message(message.json)
        bot.send_message(m.chat.chat_id, f"Welcome {m.from_user.first_name}! We hope you will enjoy this Service. Please use the '/help' command to get started")


    @bot.message_handler(commands=['today'])
    # Sends the Portion for the day
    def today(message):
        m = Message(message.json)
        p = AI[get_day()]
        start = p.start
        end = p.end
        portion = f"Day {p.day} Portion:\n"
        portion += f"{start[0].name} {start[1]}{f':{start[2]} ' if start[2] != 0 else ''}"
        portion += f" {'- '+end[0].name if end[0] != start[0] else ''}{'- '+ str(end[1]) if end[1] != start[1] and end[0] == start[0] else ' '+ str(end[1]) if end[0] != start[0] else ''}{f':{int(end[2])}' if end[2] != 0  and  end[1] != start[1] else int(end[2]) if end[2] != 0 else ''}"
        link = Links()
        keyboard = types.InlineKeyboardMarkup()
        for excerpt in p.portion:
            book, chapter = excerpt
            url = link.get_url(book.name, chapter)
            button = types.InlineKeyboardButton(
            f'{book.name} {chapter}', url=url)
            keyboard.add(button)
        button = types.InlineKeyboardButton(
            'Done', callback_data=f'start_done_{m.chat.chat_id}')
        keyboard.add(button)
        bot.send_message(m.chat.chat_id, portion, reply_markup=keyboard)


    @bot.message_handler(commands=['done'])
    # Allows to user to mark their portion as completed
    def done_message(message):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            'Done', callback_data=f'start_hi_{message.chat.id}')
        keyboard.add(button)

        m = Message(message.json)
        print(m.text)
        bot.send_message(m.chat.chat_id, 'Hello', reply_markup=keyboard)

    @bot.message_handler(commands=['boss'])
    # This is for the boss to handle
    def boss(message):
        print("getting BOSS")
        m = Message(message.json)
        text = m.text
        cmd, psswd = text.split()
        print(cmd, psswd)
        if psswd == "1972":
            print(type(m.from_user.user_id))
            mess = f"{m.from_user.first_name} has been detected as a Boss.\n UID: {m.from_user.user_id}"
            bot.send_message(m.chat.chat_id, mess)
            DB = DB_load()
            DB["BOSS"] = m.from_user.user_id
            DB_save(DB)
            DB = DB_load()
            print(DB)
            bot.send_message(DB['BOSS'], "U R the B055!")

    @bot.message_handler(commands=['sub'])
    # Command to register as a User
    def sub(message):
        m = Message(message.json)
        print(f"/sub message from {m.from_user.first_name}")
        try:
            if U:
                pass
        except:
            U = U_load()
        if str(m.from_user.user_id) in U.keys():
            bot.send_message(m.from_user.user_id, f"Hello {m.from_user.first_name}! You are already subscribed. Use the /unsub command to unsubscribe. But I hope you don't.")
        else:
            try:
                user = User(m.from_user)
                user.waiting = (True, "day")
                U.add(user)
                U_save(U)
                print(f"added {m.from_user.first_name} as {m.from_user.user_id}")
                bot.send_message(m.from_user.user_id, f"Welcome {user.UID.first_name}! Please enter the day from which you would like to continue your Portion Reminders")

            except Exception as err:
                print(err)
    
    @bot.message_handler(commands=['whoami'])
    # For the user to know current status
    def whoami(message): 
        m = Message(message.json)
        print(f"/whoami message from {m.from_user.first_name}")
        U = U_load()
        try:
            if str(m.from_user.user_id) in U.keys():
                user = U[str(m.from_user.user_id)]
                print("Data of User\n", user)
                day = user.AI.day
                portion = user.portion_str
                ch = user.AI.tChapters
                due = len(user.to_complete)
                chat = f"""Name: {m.from_user.first_name}
Day: {day}
Portion: {portion}
Chapters completed: {ch} Chapters
Due for completion: {due} Portions
"""
            else:
                chat = 'You are not registered yet.\nUse /sub to register.'
            bot.send_message(m.from_user.user_id, chat)

        except Exception as err:
            print(err)

    @bot.message_handler()
    def echo(message):
        m = Message(message.json)
        print(f"echo message from {m.from_user.first_name}")
        text = m.text
        if text.startswith("/"):
            if text.lstrip("/") in ["unsub", "today", "due", "done", "dt", "issue", "news", "help"]:
                bot.send_message(m.from_user.user_id, f"Sorry, {text} command is under development. Developer is working hard to implement this feature. Stay tuned")
        try:
            if U:
                pass
        except:
            U = U_load()
        if str(m.from_user.user_id) in U.keys():
            try:
                user = U[m.from_user.user_id]
            except Exception as Err:
                print(Err, "at def echo")

            if user.waiting[0]:
                if user.waiting[1] == "day":
                    day = m.text.strip()
                    if day.isnumeric():
                        keyboard = types.InlineKeyboardMarkup()
                        button = types.InlineKeyboardButton(
                            'Yes', callback_data=f'day_{m.from_user.user_id}_{day}')
                        keyboard.add(button)
                        button = types.InlineKeyboardButton(
                            'No', callback_data=f'delete_{m.from_user.user_id}')
                        keyboard.add(button)
                        bot.send_message(m.from_user.user_id, f"Do you want to start from DAY {day}?", reply_markup= keyboard)




##########################################################
            
##########################################################
            
############# T H R E A D I N G ################
    def poll():
        while True:
            try:
                print("polling 2.0")
                bot.polling()
            except Exception as Err:
                print(f"An Error occurred: {Err}")
    def jobs(bot):
        print("Running Jobs")
        def bot_work(bot):
            print("STARTING")
            try:
                with open("U.pickle", "rb") as file:
                    DB = pickle.load(file)
                print()
                p = AI[get_day()]
                start = p.start
                end = p.end
                portion = f"Day {p.day} Portion:\n"
                portion += f"{start[0].name} {start[1]}{f':{start[2]} ' if start[2] != 0 else ''}"
                portion += f" {'- '+end[0].name if end[0] != start[0] else ''}{'- '+ str(end[1]) if end[1] != start[1] and end[0] == start[0] else ' '+ str(end[1]) if end[0] != start[0] else ''}{f':{int(end[2])}' if end[2] != 0  and  end[1] != start[1] else int(end[2]) if end[2] != 0 else ''}"
                link = Links()
                for excerpt in p.portion:
                    book, chapter = excerpt
                    url = link.get_url(book.name, chapter)
                    url_button = types.InlineKeyboardButton(
                    f'{book.name} {chapter}', url=url)

                for Suser in DB:
                    user = Suser.UID
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(url_button)
                    Done_button = types.InlineKeyboardButton(
                    'Done', callback_data=f'start_done_{user}')
                    keyboard.add(Done_button)
                    bot.send_message(user.user_id, portion, reply_markup=keyboard)
            except Exception as Err:
                print(f"Error: {Err} | at  bot_work")
            
            # Your task code here
        uae_tz = timezone('Asia/Dubai')
        schedule.every().day.at("11:57","Asia/Dubai").do(bot_work, bot)

        while True:
            schedule.run_pending()
            time.sleep(1)  # Check for pending tasks every 1 second

    bot_thread = threading.Thread(target = poll)
    jobs_thread = threading.Thread(target= jobs, args= (bot,))
    jobs_thread.start()
    bot_thread.start()
    
    print("threading began")

##############################################################


  
