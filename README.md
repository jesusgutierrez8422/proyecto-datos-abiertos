# Sistema Web de Consulta de Datos Abiertos de Colombia

Asignatura: Desarrollo de Aplicaciones con Acceso a Datos

Integrantes:
- Integrante 1: Jesus Gutierrez

## Objetivo

Aplicación web hecha con Flask que consulta una API de datos.gov.co, guarda los registros en SQL Server y permite consultarlos desde el navegador con una búsqueda y un resumen numérico. El código está organizado con el patrón MVC.

## Dataset elegido

- Nombre: DIVIPOLA - Códigos municipios
- Entidad: DANE
- Propósito: consultar los municipios y departamentos de Colombia con sus códigos.
- Enlace: https://www.datos.gov.co/d/gdxc-w37w
- ID del recurso: gdxc-w37w
- Endpoint: https://www.datos.gov.co/resource/gdxc-w37w.json?$limit=100

## Campos usados

| Campo del JSON | Columna en SQL Server | Qué representa |
|---|---|---|
| cod_mpio | id_api | Código DANE del municipio (identificador único) |
| cod_depto | cod_depto | Código del departamento |
| dpto | departamento | Nombre del departamento |
| nom_mpio | municipio | Nombre del municipio |

Además se guarda el JSON completo de cada registro en la columna json_original.

Como identificador se usa cod_mpio porque la API no trae un campo id y este código no se repite entre municipios.

## Requisitos

- Python 3.10 o superior
- SQL Server y SSMS
- Microsoft ODBC Driver 18 for SQL Server
- Navegador web

## Instalación

1. Crear y activar el entorno virtual:

```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instalar las dependencias:

```
pip install -r requirements.txt
```

3. En SSMS ejecutar el script `sql/crear_base_datos.sql`.

4. Revisar el archivo `.env` y ajustar DB_SERVER (por ejemplo `localhost\SQLEXPRESS`) y la autenticación. Si se usa usuario y contraseña de SQL Server, poner DB_TRUSTED=no y completar DB_USER y DB_PASSWORD.

## Ejecución

```
python app.py
```

Abrir http://127.0.0.1:5000 en el navegador y pulsar "Consultar API y guardar datos". Después se puede buscar por municipio o departamento.

## Estructura MVC

- Modelo: `models/datos_model.py`. Conexión a SQL Server, guardar registros y consultas SELECT.
- Vista: `templates/index.html` y `static/estilos.css`. Solo muestra los datos, no se conecta a la base de datos.
- Controlador: `app.py`. Rutas `/` y `/sincronizar`, recibe las peticiones y llama al cliente de API y al modelo.
- Cliente de API: `api/api_client.py`. Hace la petición HTTP a datos.gov.co.

## Evitar duplicados

La columna id_api tiene restricción UNIQUE y antes de insertar se verifica que el código no exista. Si se pulsa el botón de sincronizar varias veces no se duplican los municipios.
