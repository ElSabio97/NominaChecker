import streamlit as st

# Sidebar para entradas del usuario
st.sidebar.header("Datos del Piloto")

tipo_piloto = st.sidebar.selectbox(
    "Tipo de Piloto",
    options=["Primer Oficial", "Comandante"],
    help="Selecciona si eres Primer Oficial o Comandante"
)

st.title(f"Calculadora de Nómina para {tipo_piloto}")

if tipo_piloto == "Primer Oficial":
    niveles = ["Entrada", "1", "2", "3", "4", "5"]
    salarios_base_anual = {"Entrada": 15300, "1": 21700, "2": 25000, "3": 26250, "4": 27300, "5": 27982.50}
    prima_disponibilidad_anual = {"Entrada": 600, "1": 1200, "2": 1800, "3": 2400, "4": 3000, "5": 3300}
    prima_hora_vuelo = 25
    plus_nocturnidad_por_hora = 12.5
    imaginaria = 45
    dieta_vuelo = 65
else:  # Comandante
    niveles = ["1", "2", "3", "4", "5", "6", "7"]
    salarios_base_anual = {"1": 35000, "2": 40000, "3": 45000, "4": 50000, "5": 52500, "6": 54600, "7": 55965}
    prima_disponibilidad_anual = {"1": 6000, "2": 6600, "3": 7200, "4": 7800, "5": 8400, "6": 9000, "7": 9600}
    prima_hora_vuelo = 52
    plus_nocturnidad_por_hora = 26
    imaginaria = 45
    dieta_vuelo = 65

nivel_salarial = st.sidebar.selectbox("Nivel Salarial", options=niveles, help="Selecciona tu nivel salarial")
dias_alta = st.sidebar.slider("Días de alta en el mes", 1, 31, 30, step=1)
horas_vuelo = st.sidebar.number_input("Horas de vuelo totales", min_value=0.0, step=0.01, value=49.05)
horas_nocturnas = st.sidebar.number_input("Horas de vuelo nocturnas", min_value=0.0, step=0.01, value=0.67)
dias_imaginaria = st.sidebar.number_input("Días de imaginaria", min_value=0, value=1)
dias_dieta_vuelo = st.sidebar.number_input("Días de dieta vuelo", min_value=0, value=10)
extras = st.sidebar.text_input("Extras (ej. 'Media Días Vacaciones R: 80.00 €')", value="Media Días Vacaciones R: 80.00 €")

# Cálculo de Devengos
salario_base_mensual_total = (salarios_base_anual[nivel_salarial] / 12) * (dias_alta / 30)
paga_extra_mensual = salario_base_mensual_total / 7
salario_base_mensual = salario_base_mensual_total - paga_extra_mensual
prima_disponibilidad_mensual = (prima_disponibilidad_anual[nivel_salarial] / 12) * (dias_alta / 30)

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

imaginaria_total = dias_imaginaria * imaginaria
dieta_vuelo_total = dias_dieta_vuelo * dieta_vuelo

# Cálculo de dieta de vuelo exenta y tributable (según criterio de la empresa: 41.85 €/día exento)
dieta_exenta_por_dia = 41.85  # Deduced from company calculation
dieta_vuelo_exenta = dias_dieta_vuelo * dieta_exenta_por_dia
dieta_vuelo_tributable = dieta_vuelo_total - dieta_vuelo_exenta

# Procesar Extras
extras_importe = 0.0
if extras:
    try:
        partes = extras.split("€")
        importe_str = partes[0].split(":")[-1].strip()
        extras_importe = float(importe_str)
    except (IndexError, ValueError):
        st.warning("Formato de 'Extras' incorrecto. Usa 'Concepto: 80.00 € - Notas'.")

# Total Devengos
total_devengos = (
    salario_base_mensual + paga_extra_mensual + prima_disponibilidad_mensual +
    prima_hora_vuelo_total + plus_nocturnidad_total + imaginaria_total + dieta_vuelo_total + extras_importe
)

# Mostrar resultados
st.header("Resumen de la Nómina")
if salario_base_mensual > 0:
    st.write(f"**Salario Base:** {salario_base_mensual:.2f} €")
if paga_extra_mensual > 0:
    st.write(f"**Paga Extra (prorrateada):** {paga_extra_mensual:.2f} €")
if prima_disponibilidad_mensual > 0:
    st.write(f"**Prima Disponibilidad:** {prima_disponibilidad_mensual:.2f} €")
if prima_hora_vuelo_total > 0:
    st.write(f"**Prima Hora Vuelo:** {prima_hora_vuelo_total:.2f} €")
if plus_nocturnidad_total > 0:
    st.write(f"**Plus Nocturnidad:** {plus_nocturnidad_total:.2f} €")
if imaginaria_total > 0:
    st.write(f"**Imaginaria:** {imaginaria_total:.2f} €")
if dieta_vuelo_total > 0:
    st.write(f"**Dieta Vuelo Total:** {dieta_vuelo_total:.2f} €")
    st.write(f"**Dieta Vuelo Exenta:** {dieta_vuelo_exenta:.2f} €")
    st.write(f"**Dieta Vuelo Tributable:** {dieta_vuelo_tributable:.2f} €")
if extras_importe > 0:
    st.write(f"**Extras ({extras}):** {extras_importe:.2f} €")

st.subheader(f"**Total Devengos:** {total_devengos:.2f} €")
st.write("Nota: La dieta exenta se calcula con un límite de 41.85 €/día, según el criterio deducido de la empresa.")
