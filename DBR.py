# from typing import Any
from Bible import *
import csv
import pickle

class Portion():
    def __init__(self, day, portion, start, end, books_completed) -> None:
        self.day = day
        self.portion = portion
        self.start = start
        self.end = end
        self.books_completed = books_completed

    def __str__(self):
        return f"""Day: {self.day} 
Portion: {self.start} - {self.end}
Read List: {self.portion}
Books Completed: {self.books_completed if len(self.books_completed) else 'None'}"""
        

class Portions():
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    @start.setter
    def start(self, portion:list):
        if len(portion) == 2:
            if isinstance(portion[0],Book) and isinstance(portion[1], int):
                self._start = portion.extend([0, False])
        elif len(portion) == 3:
            if isinstance(portion[0],Book) and isinstance(portion[1], int) and isinstance(portion[2], int):
                v = portion[2]
                if v != 0:
                    if v == portion[0].verses(portion[1]):
                        portion.pop()
                        self._start = portion.extend([0,False])
                    else:
                        self._start = portion.append(True)

    @end.setter
    def end(self, portion:list):
        if len(portion) == 2:
            if isinstance(portion[0],Book) and isinstance(portion[1], int):
                self._end = portion.extend([0, False])
        elif len(portion) == 3:
            if isinstance(portion[0],Book) and isinstance(portion[1], int) and isinstance(portion[2], int):
                v = portion[2]
                if v != 0:
                    if v == portion[0].verses(portion[1]):
                        portion.pop()
                        self._end = portion.extend([0,False])
                    else:
                        self._end = portion.append(True)

    def __init__(self):
        self.day = 1
        self.portions = []

    def __str__(self):
        for portion in self.portions:
            if len(portion.books_completed) != 0:
                print("DAY", portion.day, portion.books_completed)
        return ''
    
    def __getitem__(self, day):
        try:
            return self.portions[day-1]
        except:
            raise IndexError("Index out of range")
        
    def __len__(self) -> int:
        return len(self.portions)
    
    def add(self,start, end, portions:tuple, day:int | None = None):
        books_completed = self.completed(portions, end)
        self.portions.append(Portion(self.day, portions, start, end, books_completed))
        self.day += 1

    def completed(self, portions, end):
        completed = []
        for portion in portions:
            book, chap = portion
            if chap == book.tChap:
                completed.append(book.name)
        return completed[:-1] if bool(end[2])  else completed
    
    def latest(self):
        p = self.portions[-1]
        start = p.start
        end = p.end
        portion = f"Day {p.day} Portion:\n"
        portion += f"{start[0].name} {start[1]}{f':{start[2]} ' if start[2] != 0 else ''}"
        portion += f" {'- '+end[0].name if end[0] != start[0] else ''}{'- '+ str(end[1]) if end[1] != start[1] and end[0] == start[0] else ' '+ str(end[1]) if end[0] != start[0] else ''}{f':{int(end[2])}' if end[2] != 0  and  end[1] != start[1] else int(end[2]) if end[2] != 0 else ''}"
        return portion
                

class DBR_AI():
    def __new__(cls, *args, **kwargs):
        """
        Handles object creation and loading from pickle file.
        """
        try:
            with open(kwargs["fileName"] + ".pickle", "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading pickled object: {e}")

        # Create a new object if pickle loading fails or file doesn't exist
        return super().__new__(cls)
    
    def __init__(self, fileName = "DBR_Schedule.csv", from_new = True):
            self.bible = read(True)
            self.curr_b = 40 if from_new else 1 # Current Book
            self.curr_c = 0 # Current chapter
            self.curr_v = 0 # Current verse - 0 means not tracking
            self.verse = 0 # Total verse so far
            self.chaps = 0 # Total chapters so far
            self.portion = "" # Portion to read of the day
            self.oavg_verse = 80 # Average verses to read per day when reading old testament
            self.navg_verse = 90 # Average verses to read per day when reading new testament
            self.avg_verse = self.navg_verse if from_new else self.oavg_verse
            self.curr_book = self.bible[self.curr_b] # Current book that is being read
            self._totalVerses = 0
            self._totalChapters = 0
            self.tVerses = 0
            self.tChapters = 0
            self.tBooks = 0
            self._day = 0
            self.oldTestament = [929,23145]
            self.newTestament = [260,7956]
            self._fileName = None
            self.fileName = fileName
            self.Portion = Portions()

    def __str__(self) -> str:
        return f"""Books Completed: {self.tBooks} Books
Chapters Completed: {self.tChapters} Chapters
Verses Completed: {self.tVerses} Verses
Books Left: {66 - int(self.tBooks)} Books
Chapters Left: {int(self.oldTestament[0]+ self.newTestament[0]) - int(self.tChapters)} Chapters
Verses Left: {int(self.oldTestament[1]+ self.newTestament[1]) - int(self.tVerses)} Verses"""

    @property
    def fileName(self):
        return self._fileName
    
    @fileName.setter
    def fileName(self, value):
        if value == None:
            self.CSV = False
        else:
            self._fileName = value
            self.CSV = True
            self.make_CSV()

    @property
    def totalVerses(self):
        return self._totalVerses
    
    @totalVerses.setter
    def totalVerses(self, new_value):
        self.tVerses += int(new_value - self._totalVerses) if self._totalVerses != 0 else 0
        self._totalVerses = new_value

    @property
    def totalChapters(self):
        return self._totalChapters
    
    @totalChapters.setter
    def totalChapters(self, new_value):
        self.tChapters += int(new_value - self._totalChapters) if self._totalChapters != 0 else 0
        self._totalChapters = new_value

    @property
    def day(self):
        return self._day
    
    @day.setter
    def day(self, new_value):
        if (self.curr_b == 66 and self.curr_c == self.bible[66].tChap) or (self.curr_b == 39 and self.curr_c == self.bible[39].tChap):
            self._day = 1
            self.totalVerses = 0
            self.totalChapters = 0
        else:
            self._day = new_value

    

    def make_CSV(self): # Makes the DBR_Schedule.csv file to read and write from
        with open(self.fileName + ".csv", "w", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Day", "Portion", "Verses", "Chapters", "AV", "AC"])
            #Day - Day of Reading
            # Portion - Portion to be read
            # Verses - Total verses read in that portion
            # AV - Average Verse per Day (Running average)
            # AC - Average Chapter read Day (Running average)

    def write(self, day:int): # Writes to the Schedule
        
            self.totalVerses += self.verse 
            self.totalChapters += self.chaps
            AV = self.totalVerses / self.day
            AC = self.totalChapters / self.day
            if self.CSV:
                with open(self.fileName + ".csv", "a", newline= "") as csvFile:
                    writer = csv.writer(csvFile)
                    row = [f"Day {day}", self.portion, self.verse, self.chaps, round(AV, 2), round(AC, 2)]
                    writer.writerow(row)
            self.verse = 0
            self.chaps = 0
            self.portion = ""
            return

    def next_day(self):
        # Increments the current day by one
        self.day += 1
        self.next()

    def next(self) -> bool: # Returns if the book has changed

        # Returns the same book if verses are left to be completed
        if self.curr_v != self.curr_book.verses(self.curr_c) and self.curr_v != 0:
            return False
        # Goes to the next chapter or book to read
        if self.curr_c + 1 > self.curr_book.tChap: # Checks if book is over
            # Resets to a new book
            self.curr_b = self.curr_b + 1 if self.curr_b < 66 else 1
            if self.curr_b == 1:
                self.avg_verse = self.oavg_verse
            if self.curr_b == 40:
                self.avg_verse = self.navg_verse
            self.curr_c = 1
            self.curr_v = 0
            self.curr_book = self.bible[self.curr_b]
            self.tBooks += 1
            return True
        else:
            self.curr_c += 1
            self.curr_v = 0
            return False
    
    def previous(self): # Returns if the book has changed
        # Goes to the previous chapter or book to read
        if self.curr_c - 1 < 1: # Checks if book is over
            # Resets to a new book
            self.curr_b = self.curr_b - 1 if self.curr_b != 1 else 66
            if self.curr_b == 39:
                self.avg_verse = 80
            if self.curr_b == 66:
                self.avg_verse = 100
            self.curr_v = 0
            self.curr_book = self.bible[self.curr_b]
            self.curr_c = self.curr_book.tChap
            return True
        else:
            self.curr_c -= 1
            self.curr_v = 0
            return False


    def get_portion(self, changed = False) -> str:
        if self.curr_v != 0: # Checks if a chapter is yet to be completed
            self.verse += self.curr_book.verses(self.curr_c) - self.curr_v
            self.chaps += 1
            self.curr_v = self.curr_book.verses(self.curr_c)
            # end = f"{self.curr_book.tVer}"
            end = (self.curr_book, self.curr_c, self.curr_v)
            if self.verse < self.avg_verse + 10:
                result = self.get_portion(self.next())
                if isinstance(result, tuple):
                    return result
                else:
                    return end
            else:
                return end
                    
        else:
            end = (self.curr_book, self.curr_c, 0)
            total = self.verse + self.curr_book.verses(self.curr_c)
            # Checks if the total rounded to the nearest ten is more than the average + 20%
            if round(total/ 10) * 10> self.avg_verse + 10: 
                # Checks if the previous total rounded to the nearest ten is less than the average - 20%
                if self.verse < self.avg_verse - 10:
                    self.curr_v = int(self.curr_book.verses(self.curr_c)/2)
                    self.verse += self.curr_v
                    end = end[:2] + (self.curr_v,)
                    return end
                else:
                    self.previous()
                    return None
            else:
                self.verse = total
                self.chaps += 1
                if self.curr_b == 66 or self.curr_b == 39: # Returns the last chapter of the last book of the current Testament
                    if self.curr_c == self.curr_book.tChap:
                        return end
                # Continues if not the end of the current Testament
                result = self.get_portion(self.next())
                if isinstance(result, tuple):
                    return result
                else:
                    return end
                

    def generate_schedule(self, until:int = 366):
        for day in range(1,until):
            self.portion = self.generate_portion()
            # P.day = day
            # print(P)
            self.write(day)
        if self.CSV:
            print(len(self.Portion))
            with open (f"{self.fileName}.pickle", "wb") as file:
                pickle.dump(self.Portion, file)
            print(f"Schedule created as {self.fileName}.csv")
        else:
            return True

    def generate_portion(self):
        self.next_day()
        if self.curr_v != 0: # Checks if a chapter is yet to be completed
            start = (self.curr_book, self.curr_c, self.curr_v+1)
        else:
            
            start = (self.curr_book, self.curr_c, 0)
        self.portion = f"{start[0].name} {start[1]}{f':{start[2]} ' if start[2] != 0 else ''}"
        end = self.get_portion()
        self.portion += f" {'- '+end[0].name if end[0] != start[0] else ''}{'- '+ str(end[1]) if end[1] != start[1] and end[0] == start[0] else ' '+ str(end[1]) if end[0] != start[0] else ''}{f':{int(end[2])}' if end[2] != 0  and  end[1] != start[1] else int(end[2]) if end[2] != 0 else ''}"
        portions = self.bible.chapters_between(start[:2], end[:2])
        P = self.Portion.add(list(start), list(end), portions)
        return self.portion

    
def get_day():
    import datetime
    start_date = datetime.date(2024, 1, 1)
    print(type(start_date))
    today = datetime.datetime.today().date()
    days = today - start_date
    return int(days.days+1)
    

    

if __name__ == "__main__":

    AI =  DBR_AI(fileName = None)
    if AI.generate_schedule(until = int(23)+1):
        print("D O N E")
        print (AI.Portion.latest())
        print (AI)
    # trial.newTestament()
    # trial.oldTestament()
    # AI = DBR_AI(fileName="DBR_Schedule")
    # Fam = DBR_AI(fileName="FamilyDBR")
    # AI.curr_b = 39+23
    # AI.curr_c = 2
    # AI.curr_v = 0
    # AI.curr_book = AI.bible[AI.curr_b]
    # AI.day = 87
    # AI.avg_verse = 100
    # AI.generate_schedule()
    # Fam.curr_b = 4
    # Fam.curr_c = 35
    # Fam.curr_v = 0
    # Fam.curr_book = AI.bible[4]
    # Fam.day = 1
    # Fam.generate_schedule()

    # with open ("FamilyDBR.pickle", "rb") as file:
    #     P = pickle.load(file)
    # import datetime
    # start_date = datetime.date(2024, 1, 1)
    # print(type(start_date))
    # today = datetime.datetime.today().date()
    # days = today - start_date
    # print(days.days+1)





