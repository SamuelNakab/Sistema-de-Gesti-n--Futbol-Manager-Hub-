import streamlit as st
import pandas as pd
from models.jugador import Jugador, crear_jugador, leer_jugadores, actualizar_jugador, eliminar_jugador
from models.club import leer_clubes

st.header("Jugadores")
st.markdown("Gestioná el plantel de la liga. Podés registrar jugadores nuevos, asignarlos a su club y actualizar su información.")

POSICIONES = ["Arquero", "Defensor", "Mediocampista", "Delantero"]

filtro_pos = st.selectbox("Filtrar por puesto en la cancha", ["Todos"] + POSICIONES)

rows = leer_jugadores()
data = [
    {
        "Número de registro": r[0],
        "Nombre": r[1],
        "Apellido": r[2],
        "Puesto en la cancha": r[3],
        "Edad": r[4],
        "Categoría": Jugador(r[0], r[1], r[2], r[3], r[4], None).categoria(),
        "Club": r[5],
    }
    for r in rows
]
if filtro_pos != "Todos":
    data = [d for d in data if d["Puesto en la cancha"] == filtro_pos]

st.dataframe(pd.DataFrame(data), use_container_width=True)

clubes_map = {row[0]: row[1] for row in leer_clubes()}
ids_existentes = [r[0] for r in rows]

with st.expander("Agregar jugador"):
    st.caption("Completá los datos del nuevo jugador y hacé clic en Agregar.")
    with st.form("form_add_jugador"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        posicion = st.selectbox("Puesto en la cancha", POSICIONES)
        edad = st.number_input("Edad", min_value=15, max_value=45, step=1, value=20)
        id_club = (
            st.selectbox("Club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Agregar"):
            if not nombre.strip() or not apellido.strip():
                st.error("Fijate que ningún campo esté vacío y que la edad esté entre 15 y 45 años.")
            elif not clubes_map:
                st.error("Primero tenés que crear al menos un club antes de agregar jugadores.")
            else:
                j = Jugador(None, nombre, apellido, posicion, edad, id_club)
                if j.es_valido():
                    crear_jugador(nombre.strip(), apellido.strip(), posicion, edad, id_club)
                    st.success("¡Listo! El jugador fue agregado correctamente.")
                    st.rerun()
                else:
                    st.error("Fijate que ningún campo esté vacío y que la edad esté entre 15 y 45 años.")

with st.expander("Modificar jugador"):
    st.caption("Ingresá el número de registro del jugador que querés modificar y actualizá sus datos.")
    with st.form("form_edit_jugador"):
        edit_id = st.number_input("Número de registro del jugador a modificar", min_value=1, step=1)
        nombre_e = st.text_input("Nuevo nombre")
        apellido_e = st.text_input("Nuevo apellido")
        posicion_e = st.selectbox("Nuevo puesto en la cancha", POSICIONES)
        edad_e = st.number_input("Nueva edad", min_value=15, max_value=45, step=1, value=20)
        id_club_e = (
            st.selectbox("Nuevo club", options=list(clubes_map.keys()), format_func=lambda x: clubes_map[x])
            if clubes_map
            else None
        )
        if st.form_submit_button("Modificar"):
            if not nombre_e.strip() or not apellido_e.strip():
                st.error("Fijate que ningún campo esté vacío y que la edad esté entre 15 y 45 años.")
            elif not clubes_map:
                st.error("No hay clubes disponibles.")
            else:
                j = Jugador(edit_id, nombre_e, apellido_e, posicion_e, edad_e, id_club_e)
                if j.es_valido():
                    actualizar_jugador(edit_id, nombre_e.strip(), apellido_e.strip(), posicion_e, edad_e, id_club_e)
                    st.success("¡Listo! Los datos del jugador fueron actualizados correctamente.")
                    st.rerun()
                else:
                    st.error("Fijate que ningún campo esté vacío y que la edad esté entre 15 y 45 años.")

with st.expander("Dar de baja un jugador"):
    st.caption("Ingresá el número de registro del jugador que querés eliminar. Esta acción no se puede deshacer.")
    with st.form("form_del_jugador"):
        del_id = st.number_input("Número de registro del jugador a dar de baja", min_value=1, step=1)
        if st.form_submit_button("Dar de baja"):
            if del_id not in ids_existentes:
                st.error("No se encontró ningún registro con ese número. Revisá la tabla y fijate el número correcto.")
            else:
                eliminar_jugador(del_id)
                st.success("¡Listo! El jugador fue dado de baja correctamente.")
                st.rerun()