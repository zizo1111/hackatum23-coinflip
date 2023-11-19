import sqlite3
import pandas as pd
import numpy as np
from transformers import pipeline

class DBConnector:

    def __init__(self, file_path) -> None:
        self.path=file_path
        self.connection=None
        self.classifier = pipeline("zero-shot-classification")


    # def __del__(self):
    #     if self.connection:
    #         self.connection.close()

    def connect(self):
        # Connect to the logs.db file
        self.connection = sqlite3.connect(self.path)

        # Create a cursor object
        self.cursor =self.connection.cursor()

    def get_tables_names(self):
        # Execute a query to get the names of all tables in the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Fetch the result as a list of tuples
        tables = self.cursor.fetchall()

        # Print the names of the tables
        print("The tables in the database are:")
        for table in tables:
            print(table[0])

        return tables

    def get_columns_names(self, table_name='logs'):
        # Execute a query to get the names of all columns in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")

        # Fetch the result as a list of tuples
        columns = self.cursor.fetchall()

        # Print the names of the columns
        print(f"The columns in the table {table_name} are:")
        for column in columns:
            print(column[1])
        
        return columns

    def query_col(self, column_name, table_name='logs', get_index = False):
        # SQL query to fetch all entries from the 'message' column in the 'logs' table
        if(get_index):
            query = f"SELECT ROWID,{column_name} FROM {table_name}"
        else:
            query = f"SELECT {column_name} FROM {table_name}"

        # Execute the query
        self.cursor.execute(query)

        # Fetch all rows
        cols = self.cursor.fetchall()

        return [item[0] for item in cols]


    def get_data_in_time_range(self, start_time, end_time, table_name='logs'):
        """
        Query the database for entries within the specified time range.
        
        :param db_path: Path to the SQLite database.
        :param start_time: Start of the time range.
        :param end_time: End of the time range.
        :return: List of tuples with the queried data.
        """
        print(start_time, end_time)
        query = f"""
        SELECT ROWID,message FROM {table_name}
        WHERE timestamp BETWEEN ? AND ?
        """
        self.cursor.execute(query, (start_time, end_time))
        data = self.cursor.fetchall()
        return data


    def get_db_labels(self, query, context=None):
    
        label_to_column_map = {'all':['ssh_cls','error_cls','warning_cls'],
                                'ssh':['ssh_cls'],
                                'error':['error_cls'],
                                'warning':['warning_cls'],
                            'ssh or error':['ssh_cls','error_cls'],
                            'ssh or warning':['ssh_cls','warning_cls'],
                            'error or warning':['error_cls','warning_cls']
                            }
        candidate_labels = list(label_to_column_map.keys())
        if(context):
            sequence = "I have a log file. It has different fields in each line like timestamp and category of message. I am going to ask questions about this file. Please tell me what category the question refers to. The previous context was : "+ context + "The question is :"+ query + "?. What are the types of categories referred to in this query?"
        else:
            sequence = "I have a log file. It has different fields in each line like timestamp and category of message. I am going to ask questions about this file. Please tell me what category the question refers to. The question is :"+ query + "?. What are the types of categories referred to in this query?"
        return self.classifier(sequence,candidate_labels)['labels'][:1]
    
    def get_class_hist(self,filter_type,table_name='logs'):

        create_query = "SELECT "
        for i in range(len(filter_type)):
            create_query+=f"SUM("+filter_type[i]+")"
            if(i<len(filter_type)-1):
                create_query+=','
        create_query+=f" FROM {table_name} GROUP BY keep_flag;"
        # print(create_query)
        self.cursor.execute(create_query) 
        text_data = self.cursor.fetchall()[1]
        # df = pd.DataFrame({'Class':filter_type,'Occurences':list(text_data)})

        return pd.DataFrame({'Class':filter_type,'Occurences':list(text_data)})
    
    def get_resource_hist(self,class_label,table_name='logs'):

        self.cursor.execute(f"SELECT SUM({class_label})as sum,resource FROM {table_name} GROUP BY resource ORDER BY sum desc;")
        output = self.cursor.fetchall()
        return pd.DataFrame(columns=[class_label,'Devices'],data=np.array(output)).head(5)

if __name__ == "__main__":
    db_conn = DBConnector('/home/hackathon26/omar/hackatum23-coinflip/data/logs_test_log1.out.db')
    db_conn.connect()
    print(type(db_conn.query_col('message')[0]),)