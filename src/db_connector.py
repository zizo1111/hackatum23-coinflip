import sqlite3
from datetime import datetime
import re
import os
import pandas as pd

class DBConnector:

    def __init__(self, file_path) -> None:
        self.path=file_path
        self.connection=None


    def __del__(self):
        if self.connection:
            self.connection.close()

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

        return cols


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
    
