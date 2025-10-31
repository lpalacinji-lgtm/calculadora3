# app.py
import streamlit as st
from datetime import datetime
from src.calculator import calcular_tabletas, calcular_ampollas

# Cargar CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Calculadora de Medicamentos 💊",
    layout="wide",
    page_icon="💉"
)

st.title("💊 Calculadora de Dispensación Médica")
#st.caption("Sistema Profesional — Optimizado para Farmacias y Áreas Clínicas")

col_form, col_result = st.columns([1.1, 1])

with col_form:
    st.subheader("🧾 Datos del Medicamento")

    codigo = st.text_input("Código del medicamento:")
    nombre = st.text_input("Nombre del medicamento:")

    tipo = st.selectbox("Tipo:", ["Tableta 💊", "Ampolla 💉"])
    frecuencia = st.number_input("Frecuencia (horas):", min_value=1, max_value=24, value=8)
    duracion = st.number_input("Duración (días):", min_value=1, max_value=120, value=5)
    fecha_orden = st.date_input("Fecha de orden:", datetime.today())
    inicio_mismo_dia = st.checkbox("Inicia el mismo día", value=True)

    st.divider()

    if tipo == "Tableta 💊":
        dosis_toma = st.number_input("Dosis por toma (tabletas):", min_value=0.25, step=0.25, value=1.0)
        unidades_presentacion = st.number_input("Unidades por caja:", min_value=1, step=1, value=30)
        calcular = st.button("🧮 Calcular Tabletas", use_container_width=True)
    else:
        dosis_inyeccion = st.number_input("Dosis por inyección (ml):", min_value=0.1, step=0.1, value=1.0)
        volumen_ampolla = st.number_input("Volumen por ampolla (ml):", min_value=0.5, step=0.5, value=1.0)
        calcular = st.button("🧮 Calcular Ampollas", use_container_width=True)

with col_result:
    st.subheader("📊 Resultados")

    if tipo == "Tableta 💊" and 'calcular' in locals() and calcular:
        resultados = calcular_tabletas(frecuencia, duracion, dosis_toma, unidades_presentacion, fecha_orden, inicio_mismo_dia)
        st.success(f"**{codigo} — {nombre}**")
        st.info(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")
        colA, colB, colC = st.columns(3)
        colA.metric("Tomas", resultados["Total de tomas"])
        colB.metric("Tabletas", resultados["Total de tabletas"])
        colC.metric("Presentaciones", resultados["Presentaciones necesarias"])
        st.caption("📆 Distribución mensual:")
        st.info(f"**Este mes:** {resultados['Tabletas este mes']} tabletas")
        st.info(f"**Próximo mes:** {resultados['Tabletas próximo mes']} tabletas")

    elif tipo == "Ampolla 💉" and 'calcular' in locals() and calcular:
        resultados = calcular_ampollas(frecuencia, duracion, dosis_inyeccion, volumen_ampolla, fecha_orden, inicio_mismo_dia)
        st.success(f"**{codigo} — {nombre}**")
        st.info(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")
        colA, colB, colC = st.columns(3)
        colA.metric("Inyecciones", resultados["Total de inyecciones"])
        colB.metric("Volumen (ml)", resultados["Volumen total (ml)"])
        colC.metric("Ampollas", resultados["Ampollas necesarias"])
        st.caption("📆 Distribución mensual:")
        st.info(f"**Este mes:** {resultados['Ampollas este mes']} ampollas ({resultados['Volumen este mes (ml)']} ml)")
        st.info(f"**Próximo mes:** {resultados['Ampollas próximo mes']} ampollas ({resultados['Volumen próximo mes (ml)']} ml)")
