# src/calculator.py
from datetime import timedelta
import math
from .utils import to_date, calcular_distribucion_mensual

def calcular_tabletas(frecuencia_horas, duracion_dias, dosis_toma, unidades_presentacion, fecha_orden, inicio_mismo_dia):
    """
    Calcula dosis totales, número de presentaciones y fechas de dispensación para tabletas.
    """
    # Validaciones básicas
    if frecuencia_horas <= 0:
        raise ValueError("frecuencia_horas debe ser > 0")
    if duracion_dias <= 0:
        raise ValueError("duracion_dias debe ser > 0")

    tomas_por_dia = 24 / frecuencia_horas
    total_tomas = tomas_por_dia * duracion_dias
    total_tabletas = total_tomas * dosis_toma
    presentaciones_necesarias = math.ceil(total_tabletas / unidades_presentacion)

    # Fecha inicio
    fecha_orden = to_date(fecha_orden)
    fecha_inicio = fecha_orden if inicio_mismo_dia else fecha_orden + timedelta(days=1)

    dias_mes_actual, dias_mes_siguiente, fecha_fin = calcular_distribucion_mensual(fecha_inicio, duracion_dias)

    tabletas_mes_actual = round(dosis_toma * tomas_por_dia * dias_mes_actual, 1)
    tabletas_mes_siguiente = round(total_tabletas - tabletas_mes_actual, 1)

    resultados = {
        "Total de tomas": round(total_tomas, 1),
        "Total de tabletas": round(total_tabletas, 1),
        "Presentaciones necesarias": presentaciones_necesarias,
        "Fecha de inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Fecha de finalización": fecha_fin.strftime("%Y-%m-%d"),
        "Días este mes": dias_mes_actual,
        "Días próximo mes": dias_mes_siguiente,
        "Tabletas este mes": tabletas_mes_actual,
        "Tabletas próximo mes": tabletas_mes_siguiente
    }
    return resultados

def calcular_ampollas(frecuencia_horas, duracion_dias, dosis_inyeccion, volumen_ampolla, fecha_orden, inicio_mismo_dia):
    """
    Calcula número de ampollas necesarias, volumen total e información mensual.
    (Versión sin consideraciones de esterilidad)
    """
    if frecuencia_horas <= 0:
        raise ValueError("frecuencia_horas debe ser > 0")
    if duracion_dias <= 0:
        raise ValueError("duracion_dias debe ser > 0")

    inyecciones_por_dia = 24 / frecuencia_horas
    total_inyecciones = inyecciones_por_dia * duracion_dias
    volumen_total = total_inyecciones * dosis_inyeccion
    ampollas_necesarias = math.ceil(volumen_total / volumen_ampolla)

    fecha_orden = to_date(fecha_orden)
    fecha_inicio = fecha_orden if inicio_mismo_dia else fecha_orden + timedelta(days=1)

    dias_mes_actual, dias_mes_siguiente, fecha_fin = calcular_distribucion_mensual(fecha_inicio, duracion_dias)

    inyecciones_mes_actual = round(inyecciones_por_dia * dias_mes_actual, 1)
    inyecciones_mes_siguiente = round(total_inyecciones - inyecciones_mes_actual, 1)

    volumen_mes_actual = round(inyecciones_mes_actual * dosis_inyeccion, 2)
    volumen_mes_siguiente = round(volumen_total - volumen_mes_actual, 2)

    ampollas_mes_actual = math.ceil(volumen_mes_actual / volumen_ampolla)
    ampollas_mes_siguiente = math.ceil(volumen_mes_siguiente / volumen_ampolla)

    resultados = {
        "Total de inyecciones": round(total_inyecciones, 1),
        "Volumen total (ml)": round(volumen_total, 2),
        "Ampollas necesarias": ampollas_necesarias,
        "Fecha de inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Fecha de finalización": fecha_fin.strftime("%Y-%m-%d"),
        "Días este mes": dias_mes_actual,
        "Días próximo mes": dias_mes_siguiente,
        "Ampollas este mes": ampollas_mes_actual,
        "Ampollas próximo mes": ampollas_mes_siguiente,
        "Volumen este mes (ml)": volumen_mes_actual,
        "Volumen próximo mes (ml)": volumen_mes_siguiente
    }
    return resultados
