import os
import sqlite3
from datetime import datetime, timedelta
from db.db_init import initialize

class ConnectionManager:
    """
    A class to manage the connection to the database.
    """
    def __init__(self, db_path):
        """
        Constructor of the class ConnectionManager.
        :param db_path:
        """
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            initialize(self.db_path)
        self.conn = None

    def __enter__(self):
        """
        Enter the context.
        Create a connection to the database and return a cursor.
        :return:
        """
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context.
        Commit the changes and close the connection.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.conn.commit()
        self.conn.close()

def get_connexion():
    """
    Get a connection to the database.
    :return:
    """
    db_path = "db/database.sqlite"
    return ConnectionManager(db_path)
