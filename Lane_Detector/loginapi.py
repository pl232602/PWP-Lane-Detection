import sqlite3
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
        checker=self.cur.execute("SELECT * FROM users WHERE username = ?",(self.x[0],)) #retrieve users with matching username (should only be 1)
        full_table=checker.fetchall() #retieve list form of selected entries
        print("this is checker:")
        print(full_table)
        length=len(full_table) #check length of retireved data
        print(length)
        if  length > 0: #if the data has any length (implying existing user), return false
            print("checker is false")
            return False
        self.cur.execute("""INSERT INTO users (username,password,salt) VALUES

        (?,?,?)

        """,(self.x)) #if no other user exists, add hashed entry to database
        self.con.commit()

    def check_user(self): #checks if entered credentials are present in database
        checker=self.cur.execute("SELECT * FROM users WHERE username = ?",(self.x[0],))
        print("this is checker:")
        entry=checker.fetchall() #retrieve database entry with matching username
        salt=entry[0][3] #retireved stored salt
        salted_password=(self.x[1]+salt) #re-salt password
        encoded_password=salted_password.encode("UTF-8") #re-encode password
        print(encoded_password)
        hashed_password = hashlib.sha3_256(encoded_password).hexdigest() #re-hash password
        print(hashed_password)
        print(entry[0][2])
        if hashed_password == entry[0][2]: #check if newly generated hash matches stored one
            return True
        else:
            return False
        
    def credential_hash(self):
        salt=secrets.randbits(32) #generate cryptographically secure random number
        salt_string=str(salt) #convert salt from byte to string
        salted_password=(self.x[1] + salt_string) #concatenate password and salt
        encoded_password=salted_password.encode("UTF-8") #encode password in UTF-8
        print(encoded_password)
        hashed_password = hashlib.sha3_256(encoded_password).hexdigest() #hash password with sha256
        print("hashed password: ",hashed_password)
        self.x[1]=hashed_password #replace user object password variable with hash
        self.x.append(salt_string) #add salt to user object variable
        print(self.x)