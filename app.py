import streamlit as st
from models.club import leer_clubes
from models.jugador import leer_jugadores
from models.estadio import leer_estadios

st.set_page_config(page_title="Futbol Manager Hub", layout="wide")

st.title("Futbol Manager Hub")
st.subheader("ORT League")
st.markdown("Usa el menu lateral para navegar entre **Jugadores**, **Clubes** y **Estadios**.")

col1, col2, col3 = st.columns(3)
col1.metric("Clubes", len(leer_clubes()))
col2.metric("Jugadores", len(leer_jugadores()))
col3.metric("Estadios", len(leer_estadios()))
