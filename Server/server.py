import os
import sqlite3

from flask import Flask, jsonify, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "cestino.db")
PORTA = 8000

app = Flask(__name__)

QUERY_CESTINI = """
SELECT *
FROM Cestini 
ORDER BY id
"""

QUERY_REGISTRAZIONI = """
SELECT * 
FROM Registrazioni r
"""

def connetti():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def crea_tabelle():
    conn = connetti()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Cestini (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zona VARCHAR(100) NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Registrazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idCestino INTEGER NOT NULL,
            capacita INTEGER NOT NULL,
            tempo DATETIME NOT NULL,
            FOREIGN KEY (idCestino) REFERENCES Cestini(id)
        )
    """)
    conn.commit()
    conn.close()


# ---------- GET ----------
@app.get("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.get("/api/cestini")
def lista_cestini():
    conn = connetti()
    try:
        righe = conn.execute(QUERY_CESTINI).fetchall()
    finally:
        conn.close()
    return jsonify([
        {"id": r[0], "zona": r[1]}
        for r in righe
    ])

@app.get("/api/records")
def records():
    conn = connetti()
    try:
        righe = conn.execute(QUERY_REGISTRAZIONI).fetchall()
    finally:
        conn.close()
    return jsonify([
        {"id": r[0], "idCestino": r[1], "capacita": r[2], "tempo": r[3]}
        for r in righe
    ])

@app.get("/api/forecast")
def previsione():
    conn = connetti()
    try:
        righe = conn.execute("""
            WITH t AS (
                SELECT idCestino, capacita, tempo,
                       LAG(capacita) OVER (PARTITION BY idCestino ORDER BY tempo, id) AS prev
                FROM Registrazioni
            )
            SELECT c.id, c.zona,
                   (SELECT capacita FROM Registrazioni WHERE idCestino = c.id
                    ORDER BY tempo DESC, id DESC LIMIT 1),
                   COALESCE((SELECT SUM(capacita - prev) FROM t
                             WHERE t.idCestino = c.id AND capacita > prev
                               AND tempo >= datetime('now', 'localtime', '-24 hours')), 0)
            FROM Cestini c
            ORDER BY c.id
        """).fetchall()
    finally:
        conn.close()
    return jsonify([
        {"id": r[0], "zona": r[1], "capacita": r[2], "fill_last_24h": r[3]}
        for r in righe
    ])

# ---------- POST ----------
@app.post("/api/registrazioni")
def nuova_registrazione():
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict):
        return jsonify(errore="JSON non valido"), 400

    id_cestino, cap = dati.get("idCestino"), dati.get("capacita")
    if not isinstance(id_cestino, int) or not isinstance(cap, int) or not 0 <= cap <= 100:
        return jsonify(errore="servono idCestino (int) e capacita (0-100)"), 400

    conn = connetti()
    try:
        conn.execute(
            "INSERT INTO Registrazioni (idCestino, capacita, tempo) "
            "VALUES (?, ?, datetime('now', 'localtime'))",
            (id_cestino, cap),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify(errore="cestino inesistente"), 400
    finally:
        conn.close()
    return jsonify(ok=True)


@app.post("/api/cestini")
def nuovo_cestino():
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict):
        return jsonify(errore="JSON non valido"), 400

    zona = dati.get("zona")
    if not isinstance(zona, str) or not zona.strip() or len(zona) > 100:
        return jsonify(errore="serve zona (testo, max 100 caratteri)"), 400

    conn = connetti()
    try:
        cur = conn.execute("INSERT INTO Cestini (zona) VALUES (?)", (zona.strip(),))
        conn.commit()
        nuovo_id = cur.lastrowid
    finally:
        conn.close()
    return jsonify(ok=True, id=nuovo_id)


if __name__ == "__main__":
    crea_tabelle()
    app.run(host="0.0.0.0", port=PORTA)