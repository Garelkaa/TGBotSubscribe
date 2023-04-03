import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    
    def addUser(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
    
    def user_exists(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM users WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(res))

    def Sub(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT 'sub' FROM users WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in res:
                sub = str(row[0])
            return sub
    
    def settime(self, user_id, time):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time` = ? WHERE `user_id` = ?", (time, user_id,))
    
    def get_time(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT `time` FROM users WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in res:
                time = int(row[0])
            return time
        
    def getSub(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT `time` FROM users WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in res:
                time = int(row[0])
            
            if time > int(time.time()):
                return True
            else:
                return False
    
    def get_UserInfo(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT `user_id` FROM users WHERE `user_id` = ?", (user_id,)).fetchall()
