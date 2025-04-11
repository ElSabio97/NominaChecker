import streamlit as st

# Sidebar para entradas del usuario
st.sidebar.header("Datos del Piloto")

# Selector de tipo de piloto
tipo_piloto = st.sidebar.selectbox(
    "Tipo de Piloto",
    options=["Primer Oficial", "Comandante"],
    help="Selecciona si eres Primer Oficial o Comandante"
)

# Título dinámico según el tipo de piloto
st.title(f"Calculadora de Nómina para {tipo_piloto}")

# Configuración según tipo de piloto (valores de 2025 del Anexo I)
if tipo_piloto == "Primer Oficial":
    niveles = ["Entrada", "1", "2", "3", "4", "5"]
    salarios_base_anual = {
        "Entrada": 15300,
        "1": 21700,
        "2": 25000,
        "3": 26250,
        "4": 27300,
        "5": 27982.50
    }
    prima_disponibilidad_anual = {
        "Entrada": 600,
        "1": 1200,
        "2": 1800,
        "3": 2400,
        "4": 3000,
        "5": 3300
    }
    prima_hora_vuelo = 25
    plus_nocturnidad_por_hora = 12.5
    imaginaria = 45
    compensacion_vacaciones = 95
    dieta_vuelo = 65
    dieta_pernocta = 95
    dieta_curso = 70
else:  # Comandante
    niveles = ["1", "2", "3", "4", "5", "6", "7"]
    salarios_base_anual = {
        "1": 35000,
        "2": 40000,
        "3": 45000,
        "4": 50000,
        "5": 52500,
        "6": 54600,
        "7": 55965
    }
    prima_responsabilidad_anual = {
        "1": 2000,
        "2": 2500,
        "3": 3500,
        "4": 4500,
        "5": 5500,
        "6": 6500,
        "7": 7500
    }
    prima_disponibilidad_anual = {
        "1": 6000,
        "2": 6600,
        "3": 7200,
        "4": 7800,
        "5": 8400,
        "6": 9000,
        "7": 9600
    }
    prima_hora_vuelo = 52
    plus_nocturnidad_por_hora = 26
    imaginaria = 45
    compensacion_vacaciones = 95
    dieta_vuelo = 65
    dieta_pernocta = 95
    dieta_curso = 70
    tri_tre = 600
    prima_lifus = 25

nivel_salarial = st.sidebar.selectbox(
    "Nivel Salarial",
    options=niveles,
    help="Selecciona tu nivel salarial"
)

dias_alta = st.sidebar.slider("Días de alta en el mes", 1, 31, 30, step=1)

# Entradas para conceptos variables
horas_vuelo = st.sidebar.number_input("Horas de vuelo totales", min_value=0.0, step=0.01, value=0.0)
horas_nocturnas = st.sidebar.number_input("Horas de vuelo nocturnas", min_value=0.0, step=0.01, value=0.0)
horas_sparring = st.sidebar.number_input("Horas de sparring", min_value=0.0, step=0.01, value=0.0)
dias_imaginaria = st.sidebar.number_input("Días de imaginaria", min_value=0, value=0)
dias_dieta_vuelo = st.sidebar.number_input("¿Cuántos días has volado?", min_value=0, value=0)
dias_pernocta = st.sidebar.number_input("Días de pernocta", min_value=0, value=0)
dias_curso = st.sidebar.number_input("Días de dieta curso", min_value=0, value=0)
dias_vacaciones = st.sidebar.number_input("Días de vacaciones", min_value=0, value=0)
extras_importe = st.sidebar.number_input("Extras", min_value=0.0, step=0.01, value=0.0, help="Introduce el importe de conceptos adicionales.")

# Conceptos exclusivos de Comandantes
if tipo_piloto == "Comandante":
    es_tri_tre = st.sidebar.checkbox("¿Eres TRI/TRE?", value=False)
    horas_lifus = st.sidebar.number_input("Horas de vuelo LIFUS", min_value=0.0, step=0.01, value=0.0)
else:
    es_tri_tre, horas_lifus = False, 0.0

# Cálculo de Devengos
salario_base_mensual_total = (salarios_base_anual[nivel_salarial] / 12) * (dias_alta / 30)
paga_extra_mensual = (salario_base_mensual_total / 7)
salario_base_mensual = salario_base_mensual_total - paga_extra_mensual

prima_disponibilidad_mensual = (prima_disponibilidad_anual[nivel_salarial] / 12) * (dias_alta / 30)
prima_responsabilidad_mensual = (prima_responsabilidad_anual[nivel_salarial] / 12) * (dias_alta / 30) if tipo_piloto == "Comandante" else 0

# Prima hora de vuelo y Plus de Nocturnidad
if horas_nocturnas > 0:
    if horas_nocturnas > 3:
        prima_hora_vuelo_total = horas_vuelo * prima_hora_vuelo
        plus_nocturnidad_total = horas_vuelo * plus_nocturnidad_por_hora
    else:
        horas_diurnas = horas_vuelo - horas_nocturnas
        prima_hora_vuelo_total = (horas_diurnas * prima_hora_vuelo) + (horas_nocturnas * prima_hora_vuelo)
        plus_nocturnidad_total = horas_nocturnas * plus_nocturnidad_por_hora
else:
    prima_hora_vuelo_total = horas_vuelo * prima_hora_vuelo
    plus_nocturnidad_total = 0.0

prima_sparring_total = horas_sparring * prima_hora_vuelo
imaginaria_total = dias_imaginaria * imaginaria
dieta_vuelo_total = dias_dieta_vuelo * dieta_vuelo
dieta_pernocta_total = dias_pernocta * dieta_pernocta
dieta_curso_total = dias_curso * dieta_curso
vacaciones_total = dias_vacaciones * compensacion_vacaciones
tri_tre_total = tri_tre if es_tri_tre else 0
prima_lifus_total = horas_lifus * prima_lifus if tipo_piloto == "Comandante" else 0

# Total Devengos (incluye Extras directamente)
total_devengos = (
    salario_base_mensual + paga_extra_mensual + prima_disponibilidad_mensual + prima_responsabilidad_mensual +
    prima_hora_vuelo_total + plus_nocturnidad_total + prima_sparring_total + imaginaria_total +
    dieta_vuelo_total + dieta_pernocta_total + dieta_curso_total + vacaciones_total +
    tri_tre_total + prima_lifus_total + extras_importe
)

# Mostrar resultados
st.header("Resumen de la Nómina")

# Orden específico: 1 Salario Base, 2 Prima Disponibilidad, 3 Imaginaria, 4 Plus Nocturnidad,
# 5 Prima Hora Vuelo, 6 Media Días de Vacaciones, 7 Dieta Vuelo, 8 Paga Extra
if salario_base_mensual > 0:
    st.write(f"**Salario Base:** {salario_base_mensual:.2f} €")
if prima_disponibilidad_mensual > 0:
    st.write(f"**Prima Disponibilidad:** {prima_disponibilidad_mensual:.2f} €")
if imaginaria_total > 0:
    st.write(f"**Imaginaria:** {imaginaria_total:.2f} €")
if plus_nocturnidad_total > 0:
    st.write(f"**Plus Nocturnidad:** {plus_nocturnidad_total:.2f} €")
if prima_hora_vuelo_total > 0:
    st.write(f"**Prima Hora Vuelo:** {prima_hora_vuelo_total:.2f} €")
if vacaciones_total > 0:
    st.write(f"**Compensación Vacaciones:** {vacaciones_total:.2f} €")
if dieta_vuelo_total > 0:
    st.write(f"**Dieta Vuelo:** {dieta_vuelo_total:.2f} €", help="Suma de dieta vuelo exenta y tributable")
if paga_extra_mensual > 0:
    st.write(f"**Paga Extra (prorrateada):** {paga_extra_mensual:.2f} €")

# Resto de devengos (sin orden específico)
if tipo_piloto == "Comandante" and prima_responsabilidad_mensual > 0:
    st.write(f"**Prima Responsabilidad:** {prima_responsabilidad_mensual:.2f} €")
if prima_sparring_total > 0:
    st.write(f"**Prima Horas Sparring:** {prima_sparring_total:.2f} €")
if dieta_pernocta_total > 0:
    st.write(f"**Dieta Pernocta:** {dieta_pernocta_total:.2f} €")
if dieta_curso_total > 0:
    st.write(f"**Dieta Curso:** {dieta_curso_total:.2f} €")
if tipo_piloto == "Comandante" and tri_tre_total > 0:
    st.write(f"**Plus TRI/TRE:** {tri_tre_total:.2f} €")
if tipo_piloto == "Comandante" and prima_lifus_total > 0:
    st.write(f"**Prima Horas LIFUS:** {prima_lifus_total:.2f} €")
if extras_importe > 0:
    st.write(f"**Extras:** {extras_importe:.2f} €")

st.subheader(f"**Total Devengos:** {total_devengos:.2f} €")
