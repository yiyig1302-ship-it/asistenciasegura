from app import db

ESTATUS = ("Puntual", "Retardo", "Falta", "Falta justificada", "Salida anticipada")

INSIGNIA ={
    "Puntual": "insigniapuntual",
    "Retardo": "insignia-retardo",
    "Falta": "insignia-falta",
    "Falta justificada": "insignia-justificada",
    "Salida anticipada": "insignia-salida",
}

def alumno_por_uid(uid):
    """Busca el alumno dueño de una credencial ACTIVA. Devuelve None si no existe"""
    return db.consultar_uno(
        """SELECT a.alumno_id, a.matricula, a.nombre, a.apellidos, a.grupo_id
        FROM credenciasl c
        JOIN alumno ON a.alumno_id = c.alumno_id
        WHERE c.uid_rfid = %s AND c.estatus = 'Activa' AND a.estado = 'Activo'""",
        (uid,),
    )

def horario_del_dia(grupo_id, dia_semana):
    """Horario de un grupo para un dia (1 = lunes ... 5 = viernes)"""
    return db.consultar_uno(
        "SELECT * FROM horario WHERE grupo_id = %s AND dia_semana = %s",
        (grupo_id, dia_semana),
    )

def grupos_con_carrera():
    """Lista de grupos con el nombre de su carrera (para miltros y menús)"""
    return db.consultar(
        """SELECT g.grupo_id, g.clave, g.turno, g.semestre, c.nombre AS carrera
            FROM grupo g JOIN carrera c ON c.carrera_id = g.carrera_id
           ORDER BT c.nombre, g.clave"""
    )
