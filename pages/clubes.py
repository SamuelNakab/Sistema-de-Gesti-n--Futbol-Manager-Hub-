import streamlit as st
import pandas as pd
from models.club import Club, crear_club, leer_clubes, actualizar_club, eliminar_club

st.header("Clubes")

filtro_anio = st.number_input("Fundados desde el ano (0 = todos)", min_value=0, step=1, value=0)

rows = leer_clubes()
data = [
    {
        "ID": r[0],
        "Nombre": r[1],
        "Ciudad": r[2],
        "Ano Fundacion": r[3],
        "Historico": "Si" if Club(r[0], r[1], r[2], r[3]).es_historico() else "No",
    }
    for r in rows
]
if filtro_anio > 0:
    data = [d for d in data if d["Ano Fundacion"] >= filtro_anio]

st.dataframe(pd.DataFrame(data), use_container_width=True)

with st.expander("Agregar club"):
    with st.form("form_add_club"):
        nombre = st.text_input("Nombre del club")
        ciudad = st.text_input("Ciudad")
        anio = st.number_input("Ano de fundacion", min_value=1800, max_value=2026, step=1, value=1950)
        if st.form_submit_button("Agregar"):
            if not nombre.strip() or not ciudad.strip():
                st.error("Nombre y ciudad son obligatorios.")
            else:
                crear_club(nombre.strip(), ciudad.strip(), anio)
                st.success("Club agregado.")
                st.rerun()

with st.expander("Editar club"):
    with st.form("form_edit_club"):
        edit_id = st.number_input("ID del club a editar", min_value=1, step=1)
        nombre_e = st.text_input("Nuevo nombre")
        ciudad_e = st.text_input("Nueva ciudad")
        anio_e = st.number_input("Nuevo ano de fundacion", min_value=1800, max_value=2026, step=1, value=1950)
        if st.form_submit_button("Actualizar"):
            if not nombre_e.strip() or not ciudad_e.strip():
                st.error("Nombre y ciudad son obligatorios.")
            else:
                actualizar_club(edit_id, nombre_e.strip(), ciudad_e.strip(), anio_e)
                st.success("Club actualizado.")
                st.rerun()

with st.expander("Eliminar club"):
    with st.form("form_del_club"):
        del_id = st.number_input("ID del club a eliminar", min_value=1, step=1)
        if st.form_submit_button("Eliminar"):
            eliminar_club(del_id)
            st.success(f"Club #{del_id} eliminado.")
            st.rerun()
