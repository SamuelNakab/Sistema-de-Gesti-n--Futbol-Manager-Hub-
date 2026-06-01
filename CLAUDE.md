# Futbol Manager Hub

## Descripción del proyecto
Aplicación de gestión para la liga "ORT League". Permite administrar jugadores, clubes y estadios con CRUD completo, persistencia en SQLite e interfaz gráfica con Streamlit.

## Stack
- Python 3
- SQLite (base de datos local, archivo `liga.db`)
- Streamlit (interfaz gráfica)

## Estructura de archivos EXACTA y OBLIGATORIA
futbol-manager-hub/
├── CLAUDE.md
├── app.py                  # Entry point de Streamlit, solo navegación
├── database.py             # Conexión a SQLite e inicialización de tablas
├── models/
│   ├── __init__.py         # vacío
│   ├── club.py             # clase Club + métodos CRUD de clubes
│   ├── jugador.py          # clase Jugador + métodos CRUD de jugadores
│   └── estadio.py          # clase Estadio + métodos CRUD de estadios
├── pages/
│   ├── clubes.py           # página Streamlit de clubes
│   ├── jugadores.py        # página Streamlit de jugadores
│   └── estadios.py         # página Streamlit de estadios
├── liga.db                 # Se genera automáticamente
└── requirements.txt

## Reglas de arquitectura ESTRICTAS
- NUNCA mezclar SQL con el código de Streamlit.
- Cada archivo en models/ contiene: la clase con __init__ y métodos de instancia + las funciones CRUD (crear, leer, actualizar, eliminar) de esa entidad.
- app.py solo importa de models/ y renderiza la navegación.
- database.py solo maneja la conexión y la creación de tablas.

## Base de datos

### Tabla clubes
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- nombre (TEXT)
- ciudad (TEXT)
- anio_fundacion (INTEGER)

### Tabla jugadores
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- nombre (TEXT)
- apellido (TEXT)
- posicion (TEXT) — valores válidos: Arquero, Defensor, Mediocampista, Delantero
- edad (INTEGER) — mínimo 15, máximo 45
- id_club (INTEGER, FK a clubes)

### Tabla estadios
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- nombre_estadio (TEXT)
- capacidad (INTEGER) — debe ser positivo
- id_club (INTEGER, FK a clubes)

## Queries exactas a usar

### clubs (en models/club.py)
```python
query_create_club = "INSERT INTO clubes (nombre, ciudad, anio_fundacion) VALUES (?, ?, ?)"
query_read_all_clubes = "SELECT * FROM clubes"
query_update_club = "UPDATE clubes SET nombre = ?, ciudad = ?, anio_fundacion = ? WHERE id = ?"
query_delete_club = "DELETE FROM clubes WHERE id = ?"
```

### jugadores (en models/jugador.py)
```python
query_create_jugador = "INSERT INTO jugadores (nombre, apellido, posicion, edad, id_club) VALUES (?, ?, ?, ?, ?)"
query_read_jugadores_con_club = """
SELECT j.id, j.nombre, j.apellido, j.posicion, j.edad, c.nombre AS club
FROM jugadores j LEFT JOIN clubes c ON j.id_club = c.id
"""
query_update_jugador = "UPDATE jugadores SET nombre = ?, apellido = ?, posicion = ?, edad = ?, id_club = ? WHERE id = ?"
query_delete_jugador = "DELETE FROM jugadores WHERE id = ?"
```

### estadios (en models/estadio.py)
```python
query_create_estadio = "INSERT INTO estadios (nombre_estadio, capacidad, id_club) VALUES (?, ?, ?)"
query_read_estadios_con_club = """
SELECT e.id, e.nombre_estadio, e.capacidad, c.nombre AS club
FROM estadios e INNER JOIN clubes c ON e.id_club = c.id
"""
query_update_estadio = "UPDATE estadios SET nombre_estadio = ?, capacidad = ?, id_club = ? WHERE id = ?"
query_delete_estadio = "DELETE FROM estadios WHERE id = ?"
```

## Clases requeridas
Cada clase tiene __init__ y 2 métodos de instancia:

- **Club** (models/club.py): `es_historico()` → True si anio_fundacion < 1950. `__str__` → "{nombre} ({ciudad})"
- **Jugador** (models/jugador.py): `categoria()` → "Sub-20" si edad<20, "Senior" si edad<=32, "Veterano" si edad>32. `es_valido()` → True si 15 <= edad <= 45
- **Estadio** (models/estadio.py): `es_alta_capacidad()` → True si capacidad > 40000. `__str__` → "{nombre_estadio} - cap. {capacidad}"

## Instalación de dependencias
En requirements.txt incluir: streamlit y cualquier otra dependencia necesaria.
La instalación se hace con: pip install -r requirements.txt
Si streamlit no queda en el PATH, el comando para correrlo es: python -m streamlit run app.py

## Interfaz Streamlit
- app.py con sidebar para navegar entre Jugadores, Clubes y Estadios
- Cada página (en pages/) tiene: tabla con filtros + formulario de alta + editar/eliminar por ID
- Filtros: jugadores por posición, clubes por año de fundación, estadios por capacidad mínima
- Validar campos vacíos y valores inválidos antes de insertar/actualizar