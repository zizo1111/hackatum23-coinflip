import sqlite3
from datetime import datetime
import re
import os
import pandas as pd

class DBCreator:
    def __init__(self, flag_text=None) -> None:
        self.conn=None
        self.flag_text = flag_text

    def __del__(self):
        if self.conn:
            self.conn.close()
    
    def parse_line(self, line,flag_text=""):
        error_cls = False
        warning_cls = False
        perm_cls =False
        ssh_cls = False
        other_cls = True
        keep_flag = True
        # other_cls = False
        line = line.lower()
        # print(line)
        ts,rsc = line[:16].strip(),line[16:].split(':')[0]
        current_year = datetime.now().year
        date_string_with_year = f"{current_year} {ts}"

        # Convert the string to a datetime object
        ts = datetime.strptime(date_string_with_year, "%Y %b %d %H:%M:%S")
        # print(date_object)
        msg_idx = line[16:].index(':')
        msg = line[16:][msg_idx+1:].strip()
        if('error' in msg):
            error_cls = True
            other_cls =False
        if('warning' in msg):
            warning_cls = True
            other_clas = False
        # if('permission denied' in msg):
        #   perm_cls = True
        if('ssh' in msg):
            ssh_cls = True
            other_cls = False
        if(flag_text and flag_text in msg):
            keep_flag = False
        
        return ts,rsc,msg,error_cls,warning_cls,ssh_cls,other_cls,keep_flag


    def create_db(self, file_name):
        # Connect to SQLite database (it will be created if it doesn't exist)
        db_name = 'logs_' + file_name +'.db'
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create the table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                timestamp TEXT,
                resource TEXT,
                message TEXT,
                error_cls BOOLEAN,
                warning_cls BOOLEAN,
                ssh_cls BOOLEAN,
                other_cls BOOLEAN,
                keep_flag BOOLEAN
            )
        ''')
    # # Function to parse a log line
    # def parse_log_line(self, line):
    #     match = re.match(r'(\w+\s\d+\s\d+:\d+:\d+)\s([\w\-]+)\s([\w\-]+):\s(.+)', line)
    #     if match:
    #         date_str, _, source, message = match.groups()
    #         date = datetime.strptime(date_str, '%b %d %H:%M:%S').date()
    #         time = datetime.strptime(date_str, '%b %d %H:%M:%S').time()
    #         return str(date), str(time), source, message
    #     return None
    
    def run(self, file_path):
        # get file name
        head, tail = os.path.split(file_path)

        # Read and parse the log file
        self.create_db(tail)
        line_ctr = 0
        with open(file_path, 'r') as file:
            for line in file:
                if(not line[:3] == 'Nov'):
                    continue
                parsed_line = self.parse_line(line)
                if parsed_line:
                    line_ctr+=1
                    # print(parsed_line)
                    self.cursor.execute('INSERT INTO logs (timestamp, resource, message, error_cls,warning_cls,ssh_cls,other_cls,keep_flag) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', parsed_line)
        print(line_ctr)
        self.conn.commit()

if __name__ == "__main__":
    db_cr = DBCreator()
    db_cr.run('/home/hackathon26/omar/hackatum23-coinflip/data/test_log1.out')