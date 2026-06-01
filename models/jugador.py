from database import get_connection

query_create_jugador = "INSERT INTO jugadores (nombre, apellido, posicion, edad, id_club) VALUES (?, ?, ?, ?, ?)"
query_read_jugadores_con_club = """
SELECT j.id, j.nombre, j.apellido, j.posicion, j.edad, c.nombre AS club
FROM jugadores j LEFT JOIN clubes c ON j.id_club = c.id
"""
query_update_jugador = "UPDATE jugadores SET nombre = ?, apellido = ?, posicion = ?, edad = ?, id_club = ? WHERE id = ?"
query_delete_jugador = "DELETE FROM jugadores WHERE id = ?"


class Jugador:
    def __init__(self, id, nombre, apellido, posicion, edad, id_club):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.posicion = posicion
        self.edad = edad
        self.id_club = id_club

    def categoria(self):
        if self.edad < 20:
            return "Sub-20"
        elif self.edad <= 32:
            return "Senior"
        else:
            return "Veterano"

    def es_valido(self):
        return 15 <= self.edad <= 45


def crear_jugador(nombre, apellido, posicion, edad, id_club):
    with get_connection() as conn:
        conn.execute(query_create_jugador, (nombre, apellido, posicion, edad, id_club))
        conn.commit()


def leer_jugadores():
    with get_connection() as conn:
        return conn.execute(query_read_jugadores_con_club).fetchall()


def actualizar_jugador(id, nombre, apellido, posicion, edad, id_club):
    with get_connection() as conn:
        conn.execute(query_update_jugador, (nombre, apellido, posicion, edad, id_club, id))
        conn.commit()


def eliminar_jugador(id):
    with get_connection() as conn:
        conn.execute(query_delete_jugador, (id,))
        conn.commit()
