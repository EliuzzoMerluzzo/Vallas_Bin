import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("cestino.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

ZONE = ["Quadrilatero", "Centro", "San Salvario", "Vanchiglia", "Crocetta", "Lingotto"]
GIORNI = 7

# Cestini
for zona in ZONE:
    cur.execute("INSERT INTO Cestini (zona) VALUES (?)", (zona,))

cur.execute("SELECT id FROM Cestini")
id_cestini = [r[0] for r in cur.fetchall()]

# Registrazioni: una ogni ora, ultimi 7 giorni
fine = datetime.now().replace(minute=0, second=0, microsecond=0)
inizio = fine - timedelta(days=GIORNI)

dati = []
for id_cestino in id_cestini:
    livello = random.randint(0, 40)
    velocita = random.uniform(1.0, 4.0)
    t = inizio
    while t <= fine:
        livello += velocita * random.uniform(0.5, 1.5)
        if livello >= 95:      # cestino svuotato
            livello = random.randint(0, 5)
        dati.append((id_cestino, int(livello), t.strftime("%Y-%m-%d %H:%M:%S")))
        t += timedelta(hours=1)

cur.executemany(
    "INSERT INTO Registrazioni (idCestino, capacita, tempo) VALUES (?, ?, ?)",
    dati
)

conn.commit()
conn.close()
print(f"Inseriti {len(ZONE)} cestini e {len(dati)} registrazioni")