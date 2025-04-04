import sqlite3
import os


def drop_all_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = cursor.fetchall()

    print(f"Suppression de toutes les tables")
    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    conn.commit()
    conn.close()

def execute_sql_files(db_path):
    """
    Execute all SQL files in the current directory. The order is alphabetic
    :param db_path: the path to the database
    :return: None
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    for filename in sorted(os.listdir(current_directory)):
        if filename.endswith(".sql"):
            file_path = os.path.join(current_directory, filename)
            print(f"Exécution de {file_path}...")
            with open(file_path, 'r') as file:
                sql_script = file.read()
                cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print("Tous les fichiers SQL ont été exécutés.")


def initialize(database_path):
    if os.path.exists(database_path):
        drop_all_tables(database_path)

    print(database_path)
    execute_sql_files(database_path)


def is_initialized(database_path):
    if os.path.exists(database_path):
        return True
    return False

if __name__ == "__main__":
    initialize("database.sqlite")