# app/modulos/rfid_api/routes.py — Equipo E2: API que recibe las lecturas del ESP32
# Este archivo es de E2. Solo E2 lo modifica.
#
# CONTRATO DE LA API (no se cambia sin avisar a la maestra):
#   POST /api/lecturas
#   Encabezado:  X-Clave-Dispositivo: <CLAVE_DISPOSITIVO del .env>
#   Cuerpo JSON: {"uid": "A1B2C3D4", "carril": 2}
#   La HORA la pone el servidor, nunca el ESP32.
#
# Respuestas:
#   200 {"ok": true, "alumno": "Nombre Apellidos", "estatus": "Puntual"}
#   400 {"ok": false, "error": "Faltan datos: uid y carril"}
#   401 {"ok": false, "error": "Dispositivo no autorizado"}
#   404 {"ok": false, "error": "Credencial no registrada"}
from flask import Blueprint, current_app, jsonify, request

from app.comun.consultas import alumno_por_uid

bp = Blueprint("rfid_api", __name__)

@bp.route("/lecturas", methods=["POST"])
def recibir_lectura():
    if request.headers.get("X-Clave-Dispositivo") != current_app.config["CLAVE_DISPOSITIVO"]:
        return jsonify(ok=False, error="Dispositivo no autorizado"), 401

    datos = request.get_json(silent=True) or {}
    uid = str(datos.get("uid", "")).strip().upper()
    carril = datos.get("carril")
    if not uid or carril is None:
        return jsonify(ok=False, error="Faltan datos: uid y carril"), 400

    alumno = alumno_por_uid(uid)
    if alumno is None:
        return jsonify(ok=False, error="Credencial no registrada"), 404

    # TODO E2: calcular el estatus contra el horario y guardar en registro_asistencia.
    return jsonify(ok=True, alumno=f"{alumno['nombre']} {alumno['apellidos']}",
                   estatus="Puntual", nota="Semana 0: aún no se guarda nada")