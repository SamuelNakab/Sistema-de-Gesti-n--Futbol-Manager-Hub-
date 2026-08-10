# Futbol Manager Hub

## Descripción del proyecto
Aplicación de gestión para la liga "ORT League". Permite administrar jugadores, clubes y estadios con CRUD completo, persistencia en SQLite e interfaz gráfica con Streamlit. El usuario final es un coordinador de la liga que no sabe programación.

## Stack
- Python 3.13.4
- SQLite (base de datos local, archivo `liga.db`)
- Streamlit (interfaz gráfica)

## Estructura de archivos EXACTA y OBLIGATORIA
futbol-manager-hub/
├── CLAUDE.md
├── app.py # Entry point de Streamlit, contexto general y navegación
├── database.py # Conexión a SQLite e inicialización de tablas
├── models/
│ ├── init.py # vacío
│ ├── club.py # clase Club + métodos CRUD de clubes
│ ├── jugador.py # clase Jugador + métodos CRUD de jugadores
│ └── estadio.py # clase Estadio + métodos CRUD de estadios
├── pages/
│ ├── clubes.py # página Streamlit de clubes
│ ├── jugadores.py # página Streamlit de jugadores
│ ├── estadios.py # página Streamlit de estadios
│ └── estadisticas.py # página de estadísticas con Pandas (ampliación)
├── data/
│ └── clubes_dataset.csv # dataset propio para la ampliación
├── importar_csv.py # script standalone que importa clubes_dataset.csv
├── liga.db # se genera automáticamente
└── requirements.txt

## Reglas de arquitectura ESTRICTAS
- NUNCA mezclar SQL con el código de Streamlit.
- Cada archivo en `models/` contiene: la clase con `__init__` y métodos de instancia + las funciones CRUD (crear, leer, actualizar, eliminar) de esa entidad.
- `app.py` solo importa de `models/` y `pages/`, y renderiza la navegación y el contexto general.
- `database.py` solo maneja la conexión y la creación de tablas.
- No modificar el CRUD existente de ninguna entidad al agregar funcionalidad nueva.

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

### clubes (en models/club.py)
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
Cada clase tiene `__init__` y 2 métodos de instancia:

- **Club** (models/club.py): `es_historico()` → True si anio_fundacion < 1950. `__str__` → "{nombre} ({ciudad})"
- **Jugador** (models/jugador.py): `categoria()` → "Sub-20" si edad<20, "Senior" si edad<=32, "Veterano" si edad>32. `es_valido()` → True si 15 <= edad <= 45
- **Estadio** (models/estadio.py): `es_alta_capacidad()` → True si capacidad > 40000. `__str__` → "{nombre_estadio} - cap. {capacidad}"

## Instalación de dependencias
En requirements.txt incluir: streamlit, pandas y cualquier otra dependencia necesaria.
Instalación: `pip install -r requirements.txt`
Si streamlit no queda en el PATH (común en Windows), el comando para correrlo SIEMPRE debe ser: `python -m streamlit run app.py`

## Interfaz Streamlit
- app.py con encabezado que explica qué es la app y qué rol cumple el usuario (coordinador de la liga), y sidebar para navegar entre Clubes, Jugadores, Estadios y Estadísticas
- Cada página tiene: tabla con filtros + formulario de alta con instrucción breve + editar/eliminar por ID
- Filtros: jugadores por posición, clubes por año de fundación, estadios por capacidad mínima
- Validar campos vacíos y valores inválidos antes de insertar/actualizar, con mensajes de error claros

## Idioma e interfaz (argentino)
Usar lenguaje argentino/coloquial en toda la interfaz, evitando términos técnicos en inglés o traducciones muy literales.

Etiquetas a usar:
- Año de fundación → "Año en que se fundó el club"
- Filtro de año → "Clubes fundados a partir de"
- Capacidad → "Aforo de la cancha"
- Capacidad mínima (filtro) → "Aforo mínimo"
- Crear/Agregar → "Agregar"
- Actualizar/Editar → "Modificar"
- Eliminar → "Dar de baja"
- ID en formularios → "Número de registro"
- Posición → "Puesto en la cancha"
- Alta capacidad → "Cancha grande (más de 40.000 personas)"

Descripciones por sección (arriba de cada página):
- Clubes: "Acá podés ver todos los clubes de la liga, agregar uno nuevo, modificar sus datos o darlo de baja."
- Jugadores: "Gestioná el plantel de la liga. Podés registrar jugadores nuevos, asignarlos a su club y actualizar su información."
- Estadios: "Administrá las canchas donde se juegan los partidos. Cada cancha está asociada a un club."

Mensajes:
- Éxito: "¡Listo! El [club/jugador/estadio] fue agregado correctamente."
- Error de validación: mensaje específico indicando qué campo está mal (ej: "Fijate que la edad esté entre 15 y 45 años.")
- Error al eliminar/modificar: "No se encontró ningún registro con ese número. Revisá la tabla y fijate el número correcto."

## AMPLIACIÓN — Estadística con Pandas (Parte 2 del integrador)

### Objetivo
Agregar un dataset propio en CSV, importarlo a la base usando el CRUD ya existente, y crear una sección de estadísticas que calcule medidas de tendencia central con Pandas.

### Entidad elegida: Clubes
Se usa Clubes porque `anio_fundacion` es numérico y la tabla no depende de otra (no tiene FK), lo que simplifica la importación.

### data/clubes_dataset.csv
- Columnas exactas: `nombre,ciudad,anio_fundacion`
- Mínimo 12 filas, datos ficticios pero razonables
- Repetir `anio_fundacion` en 3 filas distintas (mismo año) para que la moda tenga sentido. El resto de los años no debe repetirse.

### importar_csv.py
- Script standalone, se corre con: `python importar_csv.py`
- Leer el CSV con `pandas.read_csv('data/clubes_dataset.csv')`
- Recorrer el DataFrame con un `for` (no usar insert masivo)
- Por cada fila, llamar a la MISMA función de alta que ya existe en `models/club.py` (la que usa `query_create_club`). No reescribir la lógica de inserción.
- Al final, imprimir por consola cuántos registros se importaron correctamente.

### pages/estadisticas.py
- Agregar esta página a la navegación existente del proyecto.
- Título: "📊 Estadísticas de la Liga", con texto introductorio breve.
- Leer los clubes de la base con `pandas.read_sql_query`, usando la misma conexión que expone `database.py`. Columna a analizar: `anio_fundacion`.
- Calcular con Pandas:
  - `media = df['anio_fundacion'].mean()`
  - `mediana = df['anio_fundacion'].median()`
  - moda: usar `value_counts()` para identificar el/los año(s) más frecuente(s) y cuántas veces aparece(n). Si hay empate, mostrar todos separados por coma.
- Mostrar los tres resultados rotulados: "Media: {valor}", "Mediana: {valor}", "Moda: {valor} (se repite {N} veces)"
- Párrafo de interpretación con lógica condicional (no texto fijo):
  - Si `abs(media - mediana) < 5`: texto indicando distribución pareja de fundaciones, sin outliers que corran el promedio.
  - Si `abs(media - mediana) >= 5`: texto indicando diferencia notable, con clubes muy antiguos o muy nuevos corriendo el promedio.
  - Si la frecuencia máxima de `value_counts()` es >= 3: agregar que hay una camada clara de clubes fundados en el mismo año (posible época de expansión de la liga).
  - Si la frecuencia máxima es < 3: agregar que los años están bastante repartidos, sin uno que domine.
- No usar groupby. No agregar gráficos.

## Verificación automática (obligatorio después de cada implementación)
Después de generar o modificar código, verificar que funciona de verdad antes de darlo por terminado — no alcanza con que no tire errores de sintaxis:
- Ejecutar `importar_csv.py` y capturar cuántas filas se importaron.
- Consultar la base directamente (con `sqlite3` o un script Python corto) para confirmar cuántos registros hay en `clubes` antes y después de importar.
- Ejecutar la lógica de `estadisticas.py` (media, mediana, moda) fuera de Streamlit, en un script o consola de Python, y mostrar los resultados numéricos reales para confirmar que coinciden con lo que se calculó.
- Al terminar, resumir en texto plano: qué se ejecutó, qué resultado dio cada verificación, y si algo falló o quedó pendiente.