import streamlit as st
import pandas as pd
from models.estadio import Estadio, crear_estadio, leer_estadios, actualizar_estadio, eliminar_estadio
from models.club import leer_clubes

st.header("Canchas")
st.markdown("Administrá las canchas donde se juegan los partidos. Cada cancha está asociada a un club.")

filtro_cap = st.number_input("Aforo mínimo (0 = todas)", min_value=0, step=1000, value=0)

rows = leer_estadios()
data = [
    {
        "Número de registro": r[0],
        "Cancha": r[1],
        "Aforo de la cancha": r[2],
        "Club": r[3],
        "Cancha grande (más de 40.000 personas)": "Sí" if Estadio(r[0], r[1], r[2], None).es_alta_capacidad() else "No",
    }
    for r in rows
]
if filtro_cap > 0:
    data = [d for d in data if d["Aforo de la cancha"] >= filtro_cap]

st.dataframe(pd.DataFrame(data), use_container_width=True)

clubes_map = {row[0]: row[1] for row in leer_clubes()}
ids_existentes = [r[0] for r in rows]

with st.expander("Agregar cancha"):
    st.caption("Completá los datos de la nueva cancha y hacé clic en Agregar.")
    with st.form("form_add_estadio"):
        nombre_est = st.text_input("Nombre de la cancha")
        capacidad = st.number_input("Aforo de la cancha", min_value=1, step=100, value=10000)
        id_club = (
            st.selectbox("Club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Agregar"):
            if not nombre_est.strip():
                st.error("Fijate que el nombre de la cancha no esté vacío.")
            elif not clubes_map:
                st.error("Primero tenés que crear al menos un club antes de agregar canchas.")
            else:
                crear_estadio(nombre_est.strip(), capacidad, id_club)
                st.success("¡Listo! La cancha fue agregada correctamente.")
                st.rerun()

with st.expander("Modificar cancha"):
    st.caption("Ingresá el número de registro de la cancha que querés modificar y actualizá sus datos.")
    with st.form("form_edit_estadio"):
        edit_id = st.number_input("Número de registro de la cancha a modificar", min_value=1, step=1)
        nombre_e = st.text_input("Nuevo nombre")
        cap_e = st.number_input("Nuevo aforo de la cancha", min_value=1, step=100, value=10000)
        id_club_e = (
            st.selectbox("Nuevo club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Modificar"):
            if not nombre_e.strip():
                st.error("Fijate que el nombre de la cancha no esté vacío.")
            elif not clubes_map:
                st.error("No hay clubes disponibles.")
            else:
                actualizar_estadio(edit_id, nombre_e.strip(), cap_e, id_club_e)
                st.success("¡Listo! Los datos de la cancha fueron actualizados correctamente.")
                st.rerun()

with st.expander("Dar de baja una cancha"):
    st.caption("Ingresá el número de registro de la cancha que querés eliminar. Esta acción no se puede deshacer.")
    with st.form("form_del_estadio"):
        del_id = st.number_input("Número de registro de la cancha a dar de baja", min_value=1, step=1)
        if st.form_submit_button("Dar de baja"):
            if del_id not in ids_existentes:
                st.error("No se encontró ningún registro con ese número. Revisá la tabla y fijate el número correcto.")
            else:
                eliminar_estadio(del_id)
                st.success("¡Listo! La cancha fue dada de baja correctamente.")
                st.rerun()