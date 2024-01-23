from DBR import *
from Messages import User as Us
class ServiceUser():
    def __init__(self, user_id:Us ):
        self.UID = user_id
        self._day = None
        self.AI = None
        self.portion_str = None
        self.to_complete = []
        self.completed = False
        self.status = None
        self.waiting = (False,)

    @property
    def day(self):
        return self._day
    
    @day.setter
    def day(self, value):
        if value != None:
            if type(value) == type(1):
                self._day = value
            else:
                try:
                    self._day = int(value)

                except:
                    return False
            self.AI = DBR_AI(fileName = None)
            self.AI.generate_schedule(int(value))
            self.portion_str = self.AI.Portion.latest()
            self.to_complete.append(int(value))

    def add(self, day):
        self.to_complete.append(day)
        self.completed = False

    def completed(self, day):
        if len(self.to_complete.remove(day)) < 1:
            self.completed = True
            return self.completed
        else:
            return False
        
class Users():
    def __init__(self):
        self.UsersD = dict()

    def __getitem__(self, ID):
        ID: str = str(ID)
        return self.UsersD.get(ID)

    def add(self, user:ServiceUser) -> None:
        if user.status:
            if user.status.upper() == "BOSS":
                self.UsersD["BOSS"] = user
        else:
            self.UsersD[str(user.UID.user_id)] = user

    def update(self, user:ServiceUser):
        print(f"updated {user.UID.first_name}")
        self.UsersD[str(user.UID.user_id)] = user

    def remove(self, uid) -> bool:
        try:
            del self.UsersD[uid]
            return True
        except:
            return False
    
    def keys(self):
        return self.UsersD.keys()