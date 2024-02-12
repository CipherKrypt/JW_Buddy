from bs4 import BeautifulSoup
import requests
import datetime
# import schedule
from time import sleep
# from multiprocess import Process

interval = 5


# Returns the date add-on for the Base URL
def today():
    Now = datetime.datetime.now()
    now = Now.strftime("%Y|%m|%d|")
    date = []
    num = ''
    for i in now:
        if i == '|':
            date.append(num)
            num = ''
        else:
            num += i

    today = ''
    for i in date:
        today += i.lstrip('0') + '/'

    return today.rstrip('/')


def get_time(tag=''):
    Now = datetime.datetime.now()
    time = Now.strftime("%H:%M")
    time = time.split(":")
    Time = str(int(time[0]) + 4) + ':' + str(time[1])
    content = "\n<div><p><h6>Sent at <em>" + Time + "</em></h6></p></div>"
    if tag == 't':
        return Time
    return content


#Extracts relevant texts from the tml doc provided
def extract_DT(doc):
    day_tags = doc.find_all("h2")
    day = day_tags[1].text.strip()
    scrip_tag = doc.find_all("p", attrs={'class': 'themeScrp'})
    scripture = scrip_tag[1].text.strip()
    list = scripture.split('—')
    scrip = list[0].strip()
    verse = '—' + list[1].strip()
    para_tag = doc.find_all("p", attrs={'class': 'sb'})
    para = para_tag[1].text.strip()
    TEXT = {"day": day, "scrip": scrip, "verse": verse, "para": para}
    for key in TEXT:
        TEXT[key] = ' '.join(TEXT[key].strip("\u200b").split())
        # TEXT[key] = ' '.join(TEXT[key].strip("\u200b").split())
    return (TEXT["day"], TEXT["scrip"], TEXT["verse"], TEXT["para"])


# Sends mail to the recipients provided along with the subject and content
def send_mail(recipient, subject, content):
    mail = gMail('sandrosujith47@gmail.com', app_pass())
    mail.set_sub(subject)
    mail.set_message(content + get_time())
    try:
        mail.send(recipient)
        sleep(10)
        color = fg('green')
        print(color + get_time('t') + '::' + 'sent to:' + recipient)
    except:
        color = fg('blue')
        print(color + get_time('t') + '::' + 'not sent to:' + recipient)
        sleep(10)
    mail.end_mail()


# Extracts text and formats it to be sent to all recipients
def send_DT():
    import pickle
    global Sub
    print('Extracting Daily Text...')
    base_URL = "https://wol.jw.org/en/wol/h/r1/lp-e/"
    URL = base_URL + today()
    result = requests.get(URL)
    doc = BeautifulSoup(result.text, "html.parser")
    day, scrip, verse, para = extract_DT(doc)
    DailyText = (day, scrip, verse, para)
    with open('DT.pickle', 'wb') as f:
      pickle.dump(DailyText, f)
    content = ("<h4>Did you read the Daily Text Today </h4><br> \n" +
               "-" * 33 + '<br> <br>')
    content += "<h2>" + day + "</h2> <br>\n" + "<p><em>" + scrip + "</em>" + verse + "</p><br>\n" + "<div><p>" + para + "</p></div>\n<br>"
    
    return DailyText

from datetime import datetime

def is_today(date_str):
  """
  Checks if a date string in the format "Month Day" is today's date.

  Args:
      date_str: The date string to check (e.g., "February 5").

  Returns:
      True if the date string is today's date, False otherwise.
  """

  try:
    # Convert the date string to a datetime object, assuming the current year
    date_obj = datetime.strptime(date_str, "%B %d")

    # Get today's date
    today = datetime.now().date()
    print("Today",today, "Date", date_obj.date())

    # Check if the date and year parts are the same
    return date_obj.date() == today
  except ValueError:
    print(f"Invalid date format: {date_str}. Please use 'Month Day' format.")
    return False
