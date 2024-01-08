"""Class to store information regarding each book of the Bible."""
class Book():
    def __init__(self, name: str, tChap:int, tVer:int, aVer:float, chap:tuple):
        self.name = name
        self.tChap = tChap
        self.tVer = tVer
        self.aVer = aVer
        self.chapters = chap  # Use the property setter
    
    def __str__(self) -> str:
#         return f"""{self.name}
# Total Chapters: {self.tChap}
# Total Verse: {self.tVer}
# Average Verse: {self.aVer}
# Last tuple element: {self.chapters[-1]}"""
        return f"{self.name}"
    
    def about(self) -> str:
         return f"""Book: {self.name}
Total Chapters: {self.tChap}
Total Verse: {self.tVer}
Average Verse: {self.aVer}"""

    
    @property
    def chapters(self):
        return self._chapters
    
    @chapters.setter
    def chapters(self, value):
        for i, v in enumerate(value):
            try:
                v = int(v)
            except:
                self._chapters = value[:i]
                return  # Exit the loop after the condition is met
        self._chapters = value
            

    def verses(self, ch:int):
        if ch <= self.tChap:
            return self.chapters[ch-1]
        else:
            return ValueError(f"Chapter number exceeds total chapter in the book of {self.name}")


######################################################################################
######################################################################################
######################################################################################        

      
"""Class to contain a list of Book Objects. Pickled to later be used for faster read write."""
class Bible():
    def __init__(self):
        self.books = {}
        self.bList = list(range(66))

    def add(self,book:Book):
        if isinstance(book, Book):
            self.books[book.name] = book
            print(f"Added the book of {book.name}")
        else:
            raise ValueError("Expected a Book object")

    def __getitem__(self, ID) -> Book:
        try:
            if isinstance(ID,int):
                return self.books.get(self.bList[int(ID)-1])
            else:
                return self.books.get(ID)
        except:
            raise IndexError()
        
    
        
    def chapters_between(self, start:tuple, end:tuple) -> tuple: 
        """Takes two lists containing book name and chapter number and verse
        Returns a nested tuples with all the books and chapters between those two points (inclusive)"""
        def next(book:Book, chapter:int) -> tuple:
            #Function to return the next book and chapter as tuple
            if chapter + 1 > book.tChap: # Checks if book is over
                # Resets to a new book
                b = self.bList.index(book.name) + 1
                book = self.books.get(self.bList[int(b)]) if b <= 65 else self.books.get(self.bList[0])
                return (book, 1)
            else:
                return (book, chapter+1)
            
        ##################################################
        book, chapter = start
        chapterList = list()
        chapterList.append((book,chapter))
        while (book,chapter) != end:
            book, chapter = next(book,chapter)
            chapterList.append((book,chapter))
        chapterList = tuple(chapterList)
        return tuple(chapterList)

        
def save(bible:Bible):
    import pickle
    with open("Bible.pickle","wb") as f:
        pickle.dump(bible, f)
        print('Done')
    f.close()

def read(fullBible = False):
    import pickle
    try:
        with open("Bible.pickle","rb") as f:
            return pickle.load(f)
    except:
        if fullBible:
            make_Bible()
            return read()
        return Bible()
    
"""Function to make the bible and save as a Pickled Object"""
def make_Bible():
    oldTestament()
    newTestament()
    

"""Function to read from the DB - NT.csv file and make Book Objects to add to the Bible"""
def newTestament():
    bible = read()
    import pandas as pd
    df = pd.read_csv("DB - NT.csv")
    books = df['BookName']
    for i in range(len(books)-1):
        book = df.iloc[i]
        # print(str(book[0]), int(book[1]), int(book[2]), float(book[-1]), tuple(book[3:-1]), sep="\n")
        b = Book(str(book[0]), int(book[1]), int(book[2]), float(book[-1]), tuple(book[3:-1]))
        bible.bList[39+i] = str(book[0])
        bible.add(b)

    save(bible)
        

"""Function to read from the DB - OT.csv file and make Book Objects to add to the Bible"""
def oldTestament():
    bible = read()
    import pandas as pd
    df = pd.read_csv("DB - OT.csv")
    books = df['BookName']
    delta = 0
    pTuple = tuple()
    for i in range(len(books)-1):
        book = df.iloc[i]
        # print(str(book[0]), int(book[1]), int(book[2]), float(book[-1]), tuple(book[3:-1]), sep="\n")
        if str(book[0]).startswith("Psalms"):
            if str(book[0]) == "Psalms (101-150)":
                delta = 2
                pTuple = pTuple + tuple(book[3:-1])
                b = Book("Psalms", int(book[1]), int(book[2]), float(book[-1]), pTuple)
                bible.bList[i-delta] = "Psalms"
                bible.add(b)
                pTuple = tuple()
            else:
                pTuple = pTuple + tuple(book[3:-1])
        
        elif str(book[0]).startswith("Isaiah"):
            if str(book[0]) == "Isaiah (51-66)":
                delta += 1
                pTuple = pTuple + tuple(book[3:-1])
                b = Book("Isaiah", int(book[1]), int(book[2]), float(book[-1]), pTuple)
                bible.bList[i-delta] = "Isaiah"
                bible.add(b)
                pTuple = tuple()
            else:
                pTuple = pTuple + tuple(book[3:-1])
                

        elif str(book[0]).startswith("Jeremiah"):
            if str(book[0]) == "Jeremiah (51-52)":
                delta += 1
                pTuple = pTuple + tuple(book[3:-1])
                b = Book("Jeremiah", int(book[1]), int(book[2]), float(book[-1]), pTuple)
                bible.bList[i-delta] = "Jeremiah"
                bible.add(b)
                pTuple = tuple()
            else:
                pTuple = pTuple + tuple(book[3:-1])
                
        else:
            b = Book(str(book[0]), int(book[1]), int(book[2]), float(book[-1]), tuple(book[3:-1]))
            bible.bList[i-delta] = str(book[0])
            bible.add(b)
        
    save(bible)
