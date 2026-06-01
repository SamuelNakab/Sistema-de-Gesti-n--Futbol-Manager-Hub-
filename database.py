import sqlite3

DB_PATH = "liga.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clubes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                ciudad TEXT,
                anio_fundacion INTEGER
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                apellido TEXT,
                posicion TEXT,
                edad INTEGER,
                id_club INTEGER,
                FOREIGN KEY (id_club) REFERENCES clubes(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS estadios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_estadio TEXT,
                capacidad INTEGER,
                id_club INTEGER,
                FOREIGN KEY (id_club) REFERENCES clubes(id)
            )
        """)
        conn.commit()


init_db()
