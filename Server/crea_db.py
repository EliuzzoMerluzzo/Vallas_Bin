import sqlite3
import datetime

conn = sqlite3.connect("cestino.db")
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON")  # da attivare a ogni connessione

cur.execute("""
    CREATE TABLE IF NOT EXISTS Cestini (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zona VARCHAR(100) NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Registrazioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idCestino INTEGER NOT NULL,
        capacita INTEGER NOT NULL,
        tempo DATETIME NOT NULL,
        FOREIGN KEY (idCestino) REFERENCES Cestini(id)
    )
""")

cur.execute(
    "INSERT OR IGNORE INTO Cestini (zona) VALUES (?)",
    (["Quadrilatero"])
)

cur.execute(
    "INSERT OR IGNORE INTO Registrazioni (idCestino, capacita, tempo) VALUES (?, ?, ?)",
    ([1, 100, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
)

conn.commit()  # salva le modifiche

cur.execute("SELECT * FROM Cestini")
print(cur.fetchall())

cur.execute("SELECT * FROM Registrazioni")
print(cur.fetchall())

conn.close()