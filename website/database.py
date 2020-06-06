import sqlite3
from sqlite3 import Error
from datetime import datetime
import time

#Defined Constants
DATABASE = "messages.db"
PLAYLIST_TABLE = "Chats"

class DataBase:
    """
    To connect to Database for reading and writing to and from
    a local sqlite3 database
    """
    def __init__(self):
        """
        connect To File and create pointer
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(DATABASE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        """
        Close The Database connection
        return None
        """
        self.conn.close()

    def _create_table(self):
        """
        Create a New Table for database 
        return None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, content TEXT, time DATE)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit = 200, name = None):
        """
        returns all the messages stored in database
        limit 
        return list[dict]
        """
        if not name:
            query = f"SELECT * FROM {PLAYLIST_TABLE}"
            self.cursor.execute(query)
        else:
            query = f"SELECT * FROM {PLAYLIST_TABLE} where NAME = ?"
            self.cursor.execute(query, (name,))

        result = self.cursor.fetchall()

        #return meassages sorted by date
        results = []
        for r in sorted(result, key=lambda x: x[3], reverse=True)[:limit]:
            name, content, date, _id = r
            data = {"name": name, "message": content, "time": str(date)}
            results.append(data)
        return list(reversed(results))

    def get_messages_by_user(self, name, limit = 200):
        """
        Gets the messages from a particular user
        """
        return self.get_all_messages(limit, name)

    def save_messages(self, name, msg):
        """
        Saves the messages to local SQL databse
        """
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (None, name, msg, datetime.now()))
        self.conn.commit()
