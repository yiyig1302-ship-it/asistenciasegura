# app/__init__.py — Crea la aplicación y registra los 6 módulos (blueprints)
from flask import Flask, render_template, redirect, url_for, session, abort

from .config import Config
from . import db
from .comun.auth import ROLES

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Cada equipo registra aquí su blueprint (solo la maestra edita este archivo)
    from .modulos.login.routes import bp as login_bp  # E1
    from .modulos.rfid_api.routes import bp as rfid_api_bp  # E2
    from .modulos.rfid_panel.routes import bp as rfid_panel_bp  # E3
    from .modulos.alertas.routes import bp as alertas_bp  # E4
    from .modulos.reportes.routes import bp as reportes_bp  # E5
    from .modulos.usuarios.routes import bp as usuarios_bp  # E6

    app.register_blueprint(login_bp)
    app.register_blueprint(rfid_api_bp, url_prefix="/api")
    app.register_blueprint(rfid_panel_bp, url_prefix="/credenciales")
    app.register_blueprint(alertas_bp, url_prefix="/alertas")
    app.register_blueprint(reportes_bp, url_prefix="/reportes")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

    @app.route("/")
    def inicio():
        if "usuario_id" in session:
            return redirect(url_for("login.panel"))
        return redirect(url_for("login.entrar"))

    @app.route("/salud")
    def salud():
        """Comprueba que la app y la base de datos responden."""
        try:
            fila = db.consultar_uno("SELECT COUNT(*) AS total FROM alumno")
            return {"app": "ok", "bd": "ok", "alumnos": fila["total"]}
        except Exception as error:
            return {"app": "ok", "bd": "error", "detalle": str(error)}, 500

    # Atajo SOLO para desarrollo: entra con cualquier rol sin contraseña.
    # Así los equipos prueban sus pantallas aunque E1 no haya terminado el login.
    @app.route("/dev/entrar/<rol>")
    def dev_entrar(rol):
        if not app.config["MODO_DESARROLLO"]:
            abort(404)
        if rol not in ROLES:
            abort(400, f"Rol no válido. Usa uno de: {', '.join(ROLES)}")
        session.clear()
        session["usuario_id"] = 0
        session["rol"] = rol
        session["nombre"] = f"Prueba ({rol})"
        return redirect(url_for("login.panel"))

    @app.errorhandler(403)

    def prohibido(_error):
        return render_template("error.html", codigo=403,
                               mensaje="No tiene permiso para ver esta página."), 403

    @app.errorhandler(404)
    def no_encontrado(_error):
        return render_template("error.html", codigo=404,
                               mensaje="La página que busca no existe."), 404

    return app