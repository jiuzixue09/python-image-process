import sqlite3


class Sqlite3Template:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def find_where(self, sql_script, *args) -> list:
        cursor = self.conn.cursor()
        execute = cursor.execute(sql_script, args)
        return execute.fetchall()

    def create_table(self, schema_file):
        sql_script = open(schema_file, "r").read()
        sqlite3.complete_statement(sql_script)
        cursor = self.conn.cursor()
        cursor.executescript(sql_script)
        self.conn.commit()

    def insert_data(self, sql_script, *values):
        cursor = self.conn.cursor()
        cursor.execute(sql_script, values)
        self.conn.commit()

    def close_db(self):
        if self.conn is not None:
            self.conn.close()
