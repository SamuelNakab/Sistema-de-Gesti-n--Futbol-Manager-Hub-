from database import get_connection

query_create_estadio = "INSERT INTO estadios (nombre_estadio, capacidad, id_club) VALUES (?, ?, ?)"
query_read_estadios_con_club = """
SELECT e.id, e.nombre_estadio, e.capacidad, c.nombre AS club
FROM estadios e INNER JOIN clubes c ON e.id_club = c.id
"""
query_update_estadio = "UPDATE estadios SET nombre_estadio = ?, capacidad = ?, id_club = ? WHERE id = ?"
query_delete_estadio = "DELETE FROM estadios WHERE id = ?"


class Estadio:
    def __init__(self, id, nombre_estadio, capacidad, id_club):
        self.id = id
        self.nombre_estadio = nombre_estadio
        self.capacidad = capacidad
        self.id_club = id_club

    def es_alta_capacidad(self):
        return self.capacidad > 40000

    def __str__(self):
        return f"{self.nombre_estadio} - cap. {self.capacidad}"


def crear_estadio(nombre_estadio, capacidad, id_club):
    with get_connection() as conn:
        conn.execute(query_create_estadio, (nombre_estadio, capacidad, id_club))
        conn.commit()


def leer_estadios():
    with get_connection() as conn:
        return conn.execute(query_read_estadios_con_club).fetchall()


def actualizar_estadio(id, nombre_estadio, capacidad, id_club):
    with get_connection() as conn:
        conn.execute(query_update_estadio, (nombre_estadio, capacidad, id_club, id))
        conn.commit()


def eliminar_estadio(id):
    with get_connection() as conn:
        conn.execute(query_delete_estadio, (id,))
        conn.commit()
