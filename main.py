import TBot
import Bible
from DBR import *
from DailyText import *

DT = ('Monday, February 5', 'I . . . saw the holy city, New Jerusalem.', '—Rev. 21:2.', 'Revelation chapter 21 compares the 144,000 to an extremely beautiful city called “New Jerusalem.” This city is based on 12 foundation stones that have written on them “the 12 names of the 12 apostles of the Lamb.” (Rev. 21:10-14; Eph. 2:20) This symbolic city looks like no other. It has a main street of pure gold, 12 gates of pearl, walls and foundations adorned with precious stones\u200b—and with perfectly balanced measurements. (Rev. 21:15-21) Still, something seems to be missing! Notice what John next tells us: “I did not see a temple in it, for Jehovah God the Almighty is its temple, also the Lamb is. And the city has no need of the sun nor of the moon to shine on it, for the glory of God illuminated it, and its lamp was the Lamb.” (Rev. 21:22, 23) Those who make up the New Jerusalem will have direct access to Jehovah.\u200b—Heb. 7:27; Rev. 22:3, 4. w22.05 17-18 ¶14-15')
date_str = DT[0].split(', ')[1].strip()
print(date_str)
if is_today(date_str):
    print("Already Checked")
else:
    print(send_DT())
# TBot.bot("DBR_Schedule") 

