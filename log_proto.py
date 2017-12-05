import sqlite3
import datetime
import time



def human_time(unixtime):
    return datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')


class logDB:
    def __init__(self):
        self.con = sqlite3.connect('log.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS "Messages"
                    ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                    "user_name" VARCHAR(100),
                    "user_id" VARCHAR(100),
                    "date" VARCHAR(100),
                    "human_date" VARCHAR(100),
                    "file" VARCHAR(100),
        			"first" INTEGER);
                    ''')

    def add_message(self, user_name, user_id, date, file_path):
        self.cur.execute('SELECT * FROM Messages WHERE user_id ={0}'.format(user_id))
        first_flag = 1
        if self.cur.fetchone():
            first_flag = 0

        self.cur.execute('''INSERT INTO  
        				Messages(user_name, user_id, date, human_date, file, first) 
        				VALUES ('{0}','{1}','{2}','{3}','{4}', '{5}')'''.format(user_name, user_id, date, human_time(date), file_path, first_flag))
        self.con.commit()
        return

    def get_status(self, hours_counr):
        time_right = time.time()
        time_left = time_right - hours_counr*60*60
        self.cur.execute('SELECT * FROM Messages Where date >={0} AND date<={1} AND first =1'.format(time_left, time_right))
        count_newcomer = len(self.cur.fetchall())
        return count_newcomer

