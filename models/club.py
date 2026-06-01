from database import get_connection

query_create_club = "INSERT INTO clubes (nombre, ciudad, anio_fundacion) VALUES (?, ?, ?)"
query_read_all_clubes = "SELECT * FROM clubes"
query_update_club = "UPDATE clubes SET nombre = ?, ciudad = ?, anio_fundacion = ? WHERE id = ?"
query_delete_club = "DELETE FROM clubes WHERE id = ?"


class Club:
    def __init__(self, id, nombre, ciudad, anio_fundacion):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.anio_fundacion = anio_fundacion

    def es_historico(self):
        return self.anio_fundacion < 1950

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"


def crear_club(nombre, ciudad, anio_fundacion):
    with get_connection() as conn:
        conn.execute(query_create_club, (nombre, ciudad, anio_fundacion))
        conn.commit()


def leer_clubes():
    with get_connection() as conn:
        return conn.execute(query_read_all_clubes).fetchall()


def actualizar_club(id, nombre, ciudad, anio_fundacion):
    with get_connection() as conn:
        conn.execute(query_update_club, (nombre, ciudad, anio_fundacion, id))
        conn.commit()


def eliminar_club(id):
    with get_connection() as conn:
        conn.execute(query_delete_club, (id,))
        conn.commit()
