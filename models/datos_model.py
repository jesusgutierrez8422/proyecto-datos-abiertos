import os
import json
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    servidor = os.getenv("DB_SERVER")
    base_datos = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    trusted = os.getenv("DB_TRUSTED", "yes").lower() == "yes"

    if trusted:
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        usuario = os.getenv("DB_USER")
        clave = os.getenv("DB_PASSWORD")
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            f"UID={usuario};PWD={clave};"
            "TrustServerCertificate=yes;"
        )

    return pyodbc.connect(cadena)


def guardar_registros(registros):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    insertados = 0

    try:
        for registro in registros:
            identificador = str(registro.get("cod_mpio") or "")
            if not identificador:
                continue

            cod_depto = registro.get("cod_depto") or registro.get("cod_dpto")

            cursor.execute(
                """
                IF NOT EXISTS (
                    SELECT 1 FROM RegistrosAPI WHERE id_api = ?
                )
                INSERT INTO RegistrosAPI
                (id_api, cod_depto, departamento, municipio, json_original)
                VALUES (?, ?, ?, ?, ?)
                """,
                identificador,
                identificador,
                cod_depto,
                registro.get("dpto"),
                registro.get("nom_mpio"),
                json.dumps(registro, ensure_ascii=False)
            )
            if cursor.rowcount > 0:
                insertados += 1

        conexion.commit()
        return insertados
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def consultar_registros(filtro=""):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        if filtro:
            cursor.execute(
                """
                SELECT TOP 100 id_api, cod_depto, departamento, municipio
                FROM RegistrosAPI
                WHERE municipio LIKE ?
                   OR departamento LIKE ?
                ORDER BY id DESC
                """,
                f"%{filtro}%",
                f"%{filtro}%"
            )
        else:
            cursor.execute(
                """
                SELECT TOP 100 id_api, cod_depto, departamento, municipio
                FROM RegistrosAPI
                ORDER BY id DESC
                """
            )

        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def obtener_resumen():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM RegistrosAPI")
        total = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT TOP 5 departamento, COUNT(*) AS cantidad
            FROM RegistrosAPI
            GROUP BY departamento
            ORDER BY cantidad DESC
            """
        )
        por_departamento = [
            {"departamento": fila[0], "cantidad": fila[1]}
            for fila in cursor.fetchall()
        ]

        return {"total": total, "por_departamento": por_departamento}
    finally:
        cursor.close()
        conexion.close()
