import streamlit as st
import pandas as pd
from models.jugador import Jugador, crear_jugador, leer_jugadores, actualizar_jugador, eliminar_jugador
from models.club import leer_clubes

st.header("Jugadores")

POSICIONES = ["Arquero", "Defensor", "Mediocampista", "Delantero"]

filtro_pos = st.selectbox("Filtrar por posicion", ["Todas"] + POSICIONES)

rows = leer_jugadores()
data = [
    {
        "ID": r[0],
        "Nombre": r[1],
        "Apellido": r[2],
        "Posicion": r[3],
        "Edad": r[4],
        "Categoria": Jugador(r[0], r[1], r[2], r[3], r[4], None).categoria(),
        "Club": r[5],
    }
    for r in rows
]
if filtro_pos != "Todas":
    data = [d for d in data if d["Posicion"] == filtro_pos]

st.dataframe(pd.DataFrame(data), use_container_width=True)

clubes_map = {row[0]: row[1] for row in leer_clubes()}

with st.expander("Agregar jugador"):
    with st.form("form_add_jugador"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        posicion = st.selectbox("Posicion", POSICIONES)
        edad = st.number_input("Edad", min_value=15, max_value=45, step=1, value=20)
        id_club = (
            st.selectbox("Club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Agregar"):
            if not nombre.strip() or not apellido.strip():
                st.error("Nombre y apellido son obligatorios.")
            elif not clubes_map:
                st.error("Primero debes crear al menos un club.")
            else:
                j = Jugador(None, nombre, apellido, posicion, edad, id_club)
                if j.es_valido():
                    crear_jugador(nombre.strip(), apellido.strip(), posicion, edad, id_club)
                    st.success("Jugador agregado.")
                    st.rerun()
                else:
                    st.error("Edad invalida (debe estar entre 15 y 45).")

with st.expander("Editar jugador"):
    with st.form("form_edit_jugador"):
        edit_id = st.number_input("ID del jugador a editar", min_value=1, step=1)
        nombre_e = st.text_input("Nuevo nombre")
        apellido_e = st.text_input("Nuevo apellido")
        posicion_e = st.selectbox("Nueva posicion", POSICIONES)
        edad_e = st.number_input("Nueva edad", min_value=15, max_value=45, step=1, value=20)
        id_club_e = (
            st.selectbox("Nuevo club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Actualizar"):
            if not nombre_e.strip() or not apellido_e.strip():
                st.error("Nombre y apellido son obligatorios.")
            elif not clubes_map:
                st.error("No hay clubes disponibles.")
            else:
                j = Jugador(edit_id, nombre_e, apellido_e, posicion_e, edad_e, id_club_e)
                if j.es_valido():
                    actualizar_jugador(edit_id, nombre_e.strip(), apellido_e.strip(), posicion_e, edad_e, id_club_e)
                    st.success("Jugador actualizado.")
                    st.rerun()
                else:
                    st.error("Edad invalida.")

with st.expander("Eliminar jugador"):
    with st.form("form_del_jugador"):
        del_id = st.number_input("ID del jugador a eliminar", min_value=1, step=1)
        if st.form_submit_button("Eliminar"):
            eliminar_jugador(del_id)
            st.success(f"Jugador #{del_id} eliminado.")
            st.rerun()
