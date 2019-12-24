import sqlite3

conn = sqlite3.connect("log.db")
c = conn.cursor()

c.executescript("schema.sql")

conn.commit()
conn.close()
