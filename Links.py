"""
Function that can generate the URL for the Bible API.
"""

O_T = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy','Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai','Zechariah', 'Malachi']
N_T = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

BOOKS = {}


def get_url(book,start_chap,language = 'en'):
  global BOOKS
  print(f'recieved {book},{start_chap}')
  if language.lower == 'en':
    return  f"https://wol.jw.org/en/wol/b/r1/lp-e/nwtsty/{BOOKS[book]}/{start_chap}#study=discover"
    
#https://wol.jw.org/ml/wol/b/r162/lp-my/nwtsty/1/5#study=discover

#https://wol.jw.org/en/wol/b/r1/lp-e/nwtsty/{BOOKS[book]}/{start_chap}#study=discover"
def set_up():
  global O_T
  global N_T
  global BOOKS
  for i,b in enumerate(O_T+N_T,1):
    BOOKS[b.upper()] = str(i)
  return BOOKS

def set_lang(lang):
  if lang.lower() == 'english':
    return 'en/wol/b/r1/lp-e' 
  elif lang.lower() == 'malayalam':
    return 'ml/wol/b/r162/lp-my'

class Links():
  def __init__(self):
    self.bible = set_up()
    self.lang = None

  def get_url(self, book:str, chap:int, lang = "english"):
    self.lang = set_lang(lang)
    book = book.upper()
    return f"https://wol.jw.org/{self.lang}/nwtsty/{self.bible[book]}/{chap}#study=discover"