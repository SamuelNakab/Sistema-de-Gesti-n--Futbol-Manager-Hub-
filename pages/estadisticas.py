import streamlit as st
import pandas as pd
from database import get_connection

st.header("Estadísticas de la Liga")
st.markdown(
    "Acá ves un resumen de los años en que se fundaron los clubes de la liga. "
    "Sirve para darte una idea de qué tan vieja es la liga y si los clubes se fundaron "
    "todos en la misma época o bien repartidos en el tiempo."
)

with get_connection() as conn:
    df = pd.read_sql_query("SELECT * FROM clubes", conn)

if df.empty:
    st.warning("Todavía no hay clubes cargados, así que no hay nada para calcular. Cargá algunos desde la sección Clubes.")
else:
    media = df['anio_fundacion'].mean()
    mediana = df['anio_fundacion'].median()

    conteo = df['anio_fundacion'].value_counts()
    frecuencia_max = conteo.max()
    anios_moda = sorted(conteo[conteo == frecuencia_max].index.tolist())
    moda_texto = ", ".join(str(int(anio)) for anio in anios_moda)

    st.subheader("Los números")

    st.write(f"Media: {media:.2f}")
    st.caption("Es el promedio de los años de fundación de todos los clubes.")

    st.write(f"Mediana: {mediana:.2f}")
    st.caption(
        "Es el año que queda justo en el medio si ordenás todos los clubes "
        "de más antiguo a más nuevo."
    )

    veces = "vez" if frecuencia_max == 1 else "veces"
    st.write(f"Moda: {moda_texto} (se repite {frecuencia_max} {veces})")
    st.caption("Es el año de fundación más común entre los clubes.")

    if len(anios_moda) > 1:
        st.caption(
            "Hay un empate: varios años se repiten la misma cantidad de veces, "
            "así que abajo te mostramos los clubes de cada uno por separado."
        )

    for anio in anios_moda:
        nombres = df[df['anio_fundacion'] == anio]['nombre'].tolist()
        st.write(f"Los clubes fundados en {int(anio)} son: {', '.join(nombres)}.")

    st.subheader("Qué significa esto")

    if abs(media - mediana) < 5:
        interpretacion = (
            "La media y la mediana dan prácticamente lo mismo, así que las fundaciones "
            "están repartidas de manera pareja a lo largo del tiempo: no hay clubes "
            "sueltos muy antiguos ni muy nuevos que corran el promedio para un lado."
        )
    else:
        interpretacion = (
            "Hay una diferencia notable entre la media y la mediana, o sea que aparecen "
            "clubes muy antiguos o muy nuevos que le corren el promedio al conjunto. "
            "En estos casos conviene mirar la mediana, que representa mejor al club típico de la liga."
        )

    if frecuencia_max >= 3:
        interpretacion += (
            f" Además hay una camada clara de clubes fundados en el mismo año ({moda_texto}), "
            "lo que sugiere una época de expansión de la liga."
        )
    else:
        interpretacion += (
            " Los años de fundación están bastante repartidos: no hay un año que domine "
            "por encima del resto."
        )

    st.markdown(interpretacion)
