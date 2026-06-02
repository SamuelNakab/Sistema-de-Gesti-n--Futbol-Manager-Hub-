import streamlit as st
from models.club import leer_clubes
from models.jugador import leer_jugadores
from models.estadio import leer_estadios

st.set_page_config(page_title="ORT League - Sistema de Gestión", layout="wide")

st.title("ORT League — Sistema de Gestión")
st.markdown(
    """
    **Bienvenido al sistema de la ORT League.**
    Desde acá podés administrar los jugadores, clubes y canchas de la liga.
    Usá el menú de la izquierda para navegar entre las secciones.
    """
)
st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Clubes registrados", len(leer_clubes()))
col2.metric("Jugadores en el sistema", len(leer_jugadores()))
col3.metric("Canchas registradas", len(leer_estadios()))