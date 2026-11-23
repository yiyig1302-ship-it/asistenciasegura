from functools import wraps

from flask import abort, flash, redirect, session, url_for

ROLES = ("Administrador", "Orientadora", "Alumno", "Padre de familia")

def login_requerido(vista):
    """La ruta solo se abre si hay una sesion inciada"""
    @wraps(vista)
    def envoltura(*arg, **kwargs):
        if "usuario_id" not in session:
            flash("Indice sesion para continuar.", "info")
            return redirect(url_for("login.entrar"))
        return vista(*arg, **kwargs)
    return envoltura

def rol_requerido(*roles_permitidos):
    """La ruta solo se abre si el rol de la sesión esta en la lista"""
    for rol in roles_permitidos:
        if rol not in ROLES:
            raise ValueError(f"Rol desconocido en @rol_requerido: {rol!r}")

    def decorador(vista):
        @wraps(vista)
        @login_requerido
        def envoltura(*arg, **kwargs):
            if session.get("rol") not in roles_permitidos:
                abort(403)
            return vista(*arg, **kwargs)
        return envoltura
    return decorador