# app/config.py Lee la configuración del archivo .env
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "solo-para-desarrollo")
    MODO_DESARROLLO =os.getenv("MODO_DESARROLLO", "0") == "1"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "asist_el")
    DB_SSL_CA = os.getenv("DB_SSL_CA", "")

    CLAVE_DISPOSITIVO = os.getenv("CLAVE_DISPOSITIVO","")