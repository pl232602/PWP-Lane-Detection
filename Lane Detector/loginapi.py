import sqlite3
from csv import writer,reader
import hashlib
import secrets


class user(): #creates class that allows the addition of users
    def __init__(self,credential):
        self.x = credential
        self.con=sqlite3.connect("userstorage.db")
        self.cur=self.con.cursor()
        try: #checks if a user database file exists, and if one doesn't, will create one
            self.cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(255), password varchar(255), salt varchar(255))")
            print("created")
        except:
            print("exists")

    def add_user(self): #adds username and passwored entered on user creation page to sqlite3 managed database
        checker=self.cur.execute("SELECT * FROM users WHERE username = ?",(self.x[0],))
        print(checker.fetchall())
        print("this is checker:")
        length=len(checker.fetchall())
        if  length > 0:
            print("checker is false")
            return False
        self.cur.execute("""INSERT INTO users (username,password,salt) VALUES

        (?,?,?)

        """,(self.x))
        self.con.commit()

    def check_user(self): #checks if entered credentials are present in database
        checker=self.cur.execute("SELECT * FROM users WHERE username = ? AND password=?",(self.x))
        print("this is checker:")
        print(checker)
        if checker.fetchall() != []:
            return True
        else:
            return False
        
    def credential_hash(self):
        salt=secrets.randbits(32)
        salt_string=str(salt)
        salted_password=(self.x[1] + salt_string)
        encoded_password=salted_password.encode("UTF-8")
        print(encoded_password)
        hashed_password = hashlib.sha3_256(encoded_password).hexdigest()
        print("hashed password: ",hashed_password)
        self.x[1]=hashed_password
        self.x.append(salt_string)
        print(self.x)