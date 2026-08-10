"""Importa los clubes de data/clubes_dataset.csv a la base usando el CRUD existente.

Se corre con: python importar_csv.py
"""

import pandas as pd

from models.club import crear_club

df = pd.read_csv('data/clubes_dataset.csv')

importados = 0
for indice, fila in df.iterrows():
    crear_club(fila['nombre'], fila['ciudad'], int(fila['anio_fundacion']))
    importados += 1

print(f"Se importaron {importados} clubes correctamente.")
