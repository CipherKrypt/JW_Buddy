from keep_alive import keep_alive
import TBot
import Bible
from DBR import *

# keep_alive()
# TBot.bot()

AI = DBR_AI(fileName="DBR_Schedule")
# AI.generate_schedule()
p = AI[get_day()]
print(p)