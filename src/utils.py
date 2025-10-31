# src/utils.py
from datetime import datetime, timedelta, date

def to_date(obj):
    """
    Asegura que `obj` sea un date.
    Acepta datetime.date, datetime.datetime o strings (YYYY-MM-DD).
    """
    if isinstance(obj, date) and not isinstance(obj, datetime):
        return obj
    if isinstance(obj, datetime):
        return obj.date()
    if isinstance(obj, str):
        return datetime.strptime(obj, "%Y-%m-%d").date()
    raise ValueError("Fecha no reconocida. Use date, datetime o 'YYYY-MM-DD'")

def ultimo_dia_mes(fecha):
    """
    Devuelve el último día del mes de la fecha dada (tipo date).
    """
    fecha = to_date(fecha)
    if fecha.month < 12:
        primer_dia_sig = date(fecha.year, fecha.month + 1, 1)
        return primer_dia_sig - timedelta(days=1)
    else:
        return date(fecha.year, 12, 31)

def calcular_distribucion_mensual(fecha_inicio, duracion_dias):
    """
    Calcula los días del tratamiento que pertenecen al mes de inicio y al siguiente mes,
    y devuelve la fecha de fin.
    """
    fecha_inicio = to_date(fecha_inicio)
    fecha_fin = fecha_inicio + timedelta(days=duracion_dias - 1)
    fin_mes = ultimo_dia_mes(fecha_inicio)

    if fecha_fin <= fin_mes:
        dias_mes_actual = duracion_dias
        dias_mes_siguiente = 0
    else:
        dias_mes_actual = (fin_mes - fecha_inicio).days + 1
        dias_mes_siguiente = duracion_dias - dias_mes_actual

    return dias_mes_actual, dias_mes_siguiente, fecha_fin
