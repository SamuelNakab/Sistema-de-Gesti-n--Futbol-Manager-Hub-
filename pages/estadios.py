import streamlit as st
import pandas as pd
from models.estadio import Estadio, crear_estadio, leer_estadios, actualizar_estadio, eliminar_estadio
from models.club import leer_clubes

st.header("Estadios")

filtro_cap = st.number_input("Capacidad minima (0 = todos)", min_value=0, step=1000, value=0)

rows = leer_estadios()
data = [
    {
        "ID": r[0],
        "Estadio": r[1],
        "Capacidad": r[2],
        "Club": r[3],
        "Alta capacidad": "Si" if Estadio(r[0], r[1], r[2], None).es_alta_capacidad() else "No",
    }
    for r in rows
]
if filtro_cap > 0:
    data = [d for d in data if d["Capacidad"] >= filtro_cap]

st.dataframe(pd.DataFrame(data), use_container_width=True)

clubes_map = {row[0]: row[1] for row in leer_clubes()}

with st.expander("Agregar estadio"):
    with st.form("form_add_estadio"):
        nombre_est = st.text_input("Nombre del estadio")
        capacidad = st.number_input("Capacidad", min_value=1, step=100, value=10000)
        id_club = (
            st.selectbox("Club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Agregar"):
            if not nombre_est.strip():
                st.error("El nombre del estadio es obligatorio.")
            elif not clubes_map:
                st.error("Primero debes crear al menos un club.")
            else:
                crear_estadio(nombre_est.strip(), capacidad, id_club)
                st.success("Estadio agregado.")
                st.rerun()

with st.expander("Editar estadio"):
    with st.form("form_edit_estadio"):
        edit_id = st.number_input("ID del estadio a editar", min_value=1, step=1)
        nombre_e = st.text_input("Nuevo nombre")
        cap_e = st.number_input("Nueva capacidad", min_value=1, step=100, value=10000)
        id_club_e = (
            st.selectbox("Nuevo club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Actualizar"):
            if not nombre_e.strip():
                st.error("El nombre del estadio es obligatorio.")
            elif not clubes_map:
                st.error("No hay clubes disponibles.")
            else:
                actualizar_estadio(edit_id, nombre_e.strip(), cap_e, id_club_e)
                st.success("Estadio actualizado.")
                st.rerun()

with st.expander("Eliminar estadio"):
    with st.form("form_del_estadio"):
        del_id = st.number_input("ID del estadio a eliminar", min_value=1, step=1)
        if st.form_submit_button("Eliminar"):
            eliminar_estadio(del_id)
            st.success(f"Estadio #{del_id} eliminado.")
            st.rerun()
