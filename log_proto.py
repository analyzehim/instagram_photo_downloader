import sqlite3


class logDB:
    def __init__(self):
        self.con = sqlite3.connect('log.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS "Messages"
                    ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                    "user_name" VARCHAR(100),
                    "user_id" VARCHAR(100),
                    "date" VARCHAR(100),
                    "file" VARCHAR(100),
        			"first" INTEGER);
                    ''')
    def add_message(self, user_name, user_id, date, file):
        self.cur.execute('''INSERT INTO  
        				Messages(user_name, user_id, date, file, first) 
        				VALUES ('{0}','{1}','{2}','{3}','{4}')'''.format(user_name, user_id, date, file, 0))
        self.con.commit()
        return
