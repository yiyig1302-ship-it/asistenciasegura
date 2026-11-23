# app/modulos/reportes/routes.py  —  Equipo E5: Reportes
# Este archivo es de E5. Solo E5 lo modifica.
from flask import Blueprint, render_template
 
from app.comun.auth import rol_requerido
 
bp = Blueprint("alertas", __name__,
               template_folder="templates", static_folder="static",
               static_url_path="/static/alertas")
 
 
@bp.route("/")
@rol_requerido("Administrador", "Orientadora")
def index():
    return render_template("alertas/index.html")