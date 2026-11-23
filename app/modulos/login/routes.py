# app/modulos/login/routes.py — Equipo E1: Inicio de sesión + paneles por rol
# Este archivo es de E1. Solo E1 lo modifica.
#
# CONTRATO: al iniciar sesión, E1 debe guardar
#   session["usuario_id"], session["rol"], session["nombre"]  (ver app/comun/auth.py)
from flask import Blueprint, flash, redirect, render_template, session, url_for

from app.comun.auth import login_requerido

bp = Blueprint("login", __name__,
    template_folder="templates", static_folder="static",
    static_url_path="/static/login")

@bp.route("/login", methods=["GET", "POST"])
def entrar():
    # TODO E1: validar correo y contraseña con check_password_hash, bloqueo por intentos, etc.
    return render_template("login/entrar.html")

@bp.route("/logout")
def salir():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("login.entrar"))

@bp.route("/panel")
@login_requerido
def panel():
    # TODO E1: mostrar un panel distinto según session["rol"]
    return render_template("login/panel.html")