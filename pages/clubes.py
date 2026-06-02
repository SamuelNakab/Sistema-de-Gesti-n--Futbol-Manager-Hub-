import streamlit as st
import pandas as pd
from models.club import Club, crear_club, leer_clubes, actualizar_club, eliminar_club

st.header("Clubes")
st.markdown("Acá podés ver todos los clubes de la liga, agregar uno nuevo, modificar sus datos o darlo de baja.")

filtro_anio = st.number_input("Clubes fundados a partir de (0 = todos)", min_value=0, step=1, value=0)

rows = leer_clubes()
data = [
    {
        "Número de registro": r[0],
        "Nombre": r[1],
        "Ciudad": r[2],
        "Año en que se fundó": r[3],
        "Club histórico": "Sí" if Club(r[0], r[1], r[2], r[3]).es_historico() else "No",
    }
    for r in rows
]
if filtro_anio > 0:
    data = [d for d in data if d["Año en que se fundó"] >= filtro_anio]

st.dataframe(pd.DataFrame(data), use_container_width=True)

ids_existentes = [r[0] for r in rows]

with st.expander("Agregar club"):
    st.caption("Completá los datos del nuevo club y hacé clic en Agregar.")
    with st.form("form_add_club"):
        nombre = st.text_input("Nombre del club")
        ciudad = st.text_input("Ciudad")
        anio = st.number_input("Año en que se fundó el club", min_value=1800, max_value=2026, step=1, value=1950)
        if st.form_submit_button("Agregar"):
            if not nombre.strip() or not ciudad.strip():
                st.error("Fijate que el nombre y la ciudad no estén vacíos.")
            else:
                crear_club(nombre.strip(), ciudad.strip(), anio)
                st.success("¡Listo! El club fue agregado correctamente.")
                st.rerun()

with st.expander("Modificar club"):
    st.caption("Ingresá el número de registro del club que querés modificar y actualizá sus datos.")
    with st.form("form_edit_club"):
        edit_id = st.number_input("Número de registro del club a modificar", min_value=1, step=1)
        nombre_e = st.text_input("Nuevo nombre")
        ciudad_e = st.text_input("Nueva ciudad")
        anio_e = st.number_input("Nuevo año en que se fundó el club", min_value=1800, max_value=2026, step=1, value=1950)
        if st.form_submit_button("Modificar"):
            if not nombre_e.strip() or not ciudad_e.strip():
                st.error("Fijate que el nombre y la ciudad no estén vacíos.")
            else:
                actualizar_club(edit_id, nombre_e.strip(), ciudad_e.strip(), anio_e)
                st.success("¡Listo! Los datos del club fueron actualizados correctamente.")
                st.rerun()

with st.expander("Dar de baja un club"):
    st.caption("Ingresá el número de registro del club que querés eliminar. Esta acción no se puede deshacer.")
    with st.form("form_del_club"):
        del_id = st.number_input("Número de registro del club a dar de baja", min_value=1, step=1)
        if st.form_submit_button("Dar de baja"):
            if del_id not in ids_existentes:
                st.error("No se encontró ningún registro con ese número. Revisá la tabla y fijate el número correcto.")
            else:
                eliminar_club(del_id)
                st.success("¡Listo! El club fue dado de baja correctamente.")
                st.rerun()