#app/db.py
import pymysql
import pymysql.cursors
from flask import current_app, g

def obtener_conexion():
    """Abre UNA conexión por petición y la reutiliza mientras dure la petición."""
    if "conexion" not in g:
        cfg = current_app.config
        opciones = dict(
            host=cfg["DB_HOST"],
            port=cfg["DB_PORT"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
            datebasde=cfg["DB_NAME"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor, #filas como diccionarios
            autocommit=False,
        )
        if cfg["DB_SSL_CA"]: #Aiven exige conexión cifrada
            opciones["ssl"] = {"ca": cfg["DB_SSL_CA"]}
        g.conexion = pymysql.connect(**opciones)
    return g.conexion


def cerrar_conexion(_error=None):
    conexion = g.pop("conexion", None)
    if conexion is not None:
        conexion.close()

def consultar(sql, parametros=None):
    """SELECT que devuelve una lista de filas"""
    with obtener_conexion().cursor() as cursor:
        cursor.execute(sql, parametros or ())
        return cursor.fetchone()

def consultar_uno(sql, parametros=None):
    """SELECT qyue devuelva una sola fila (o None)"""
    with obtener_conexion().cursor() as cursor:
        cursor.execute(sql, parametros or ())
        return cursor.fetchone()

def ejecutar(sql, parametros=None):
    """INSERT / UPDATE / DELETE. Devuelve el id generado (si lo hay)"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, parametros or ())
            nuevo_id = cursor.lastrowid
        conexion.commit()
        return nuevo_id
    except Exception:
        conexion.rollback()
        raise

def init_app(app):
    app.teardown_appcontext(cerrar_conexion)