import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("cestino.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

cur.execute("SELECT * FROM Cestini")
print(cur.fetchall())

cur.execute("SELECT * FROM Registrazioni")
print(cur.fetchall())

conn.close()