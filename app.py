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

# Configuración según tipo de piloto
if tipo_piloto == "Primer Oficial":
    niveles = ["E", "1", "2", "3", "4", "5"]
    salarios_base = {
        "E": 1092.857142857143,
        "1": 1550,
        "2": 1785.7142857142858,
        "3": 1875,
        "4": 1950,
        "5": 1998.75
    }
    plus_responsabilidad = 0  # No aplica para Primeros Oficiales en el ejemplo
    plus_disponibilidad = 0  # No aplica mensualmente en el ejemplo
else:  # Comandante
    niveles = ["E", "1", "2", "3", "4", "5", "6", "7"]
    salarios_base = {
        "E": 1785.71428571429,
        "1": 2500,
        "2": 2857.14285714286,
        "3": 3214.28571428571,
        "4": 3571.42857142857,
        "5": 3750,
        "6": 3900,
        "7": 3997.5
    }
    plus_responsabilidad = {
        "E": 0,
        "1": 166.666666666667,
        "2": 208.333333333333,
        "3": 291.666666666667,
        "4": 375,
        "5": 458.333333333333,
        "6": 541.666666666667,
        "7": 625
    }
    plus_disponibilidad = {
        "E": 0,
        "1": 500,
        "2": 550,
        "3": 600,
        "4": 650,
        "5": 700,
        "6": 750,
        "7": 800
    }

nivel_salarial = st.sidebar.selectbox(
    "Nivel Salarial",
    options=niveles,
    help="Selecciona tu nivel salarial"
)

# Días de alta en el mes
dias_alta = st.sidebar.slider("Días de alta en el mes", 1, 31, 30)

# Entradas para conceptos variables
horas_vuelo = st.sidebar.number_input("Horas de vuelo totales", min_value=0.0, step=0.5, value=0.0)
horas_nocturnas = st.sidebar.number_input("Horas de vuelo nocturnas", min_value=0.0, step=0.5, value=0.0)
dias_imaginaria = st.sidebar.number_input("Días de imaginaria", min_value=0, value=0)
situaciones_mayor_2 = st.sidebar.number_input("Situaciones > 2", min_value=0, value=0)
dias_dieta_vuelo = st.sidebar.number_input("Días de dieta vuelo", min_value=0, value=0)
dias_pernocta = st.sidebar.number_input("Días de pernocta", min_value=0, value=0)
dias_curso = st.sidebar.number_input("Días de dieta curso", min_value=0, value=0)
dias_vacaciones = st.sidebar.number_input("Días de vacaciones", min_value=0, value=0)

# Conceptos exclusivos de Comandantes
if tipo_piloto == "Comandante":
    es_tri_tre = st.sidebar.checkbox("¿Eres TRI/TRE?", value=False)
    horas_lifus = st.sidebar.number_input("Horas de vuelo LIFUS", min_value=0.0, step=0.5, value=0.0)
    dias_simulador = st.sidebar.number_input("Días de simulador", min_value=0, value=0)
else:
    es_tri_tre, horas_lifus, dias_simulador = False, 0, 0  # No aplica para Primeros Oficiales

# Porcentaje de retención IRPF
irpf_porcentaje = st.sidebar.slider("Retención IRPF (%)", 0.0, 30.0, 19.25)

# Cálculo de Devengos
salario_base_mensual = salarios_base[nivel_salarial] * (dias_alta / 30)
prima_disponibilidad = 250 if tipo_piloto == "Primer Oficial" else 0  # Solo para Primeros Oficiales
plus_resp_mensual = plus_responsabilidad[nivel_salarial] * (dias_alta / 30) if tipo_piloto == "Comandante" else 0
plus_disp_mensual = plus_disponibilidad[nivel_salarial] * (dias_alta / 30) if tipo_piloto == "Comandante" else 0
prima_hora_vuelo = horas_vuelo * (23 if tipo_piloto == "Primer Oficial" else 48)
plus_nocturnidad = horas_nocturnas * (11.5 if tipo_piloto == "Primer Oficial" else 24)
imaginaria = dias_imaginaria * 40
situaciones = situaciones_mayor_2 * (11.5 if tipo_piloto == "Primer Oficial" else 24)
vacaciones = dias_vacaciones * 90
dieta_vuelo = dias_dieta_vuelo * 60
dieta_pernocta = dias_pernocta * 90
dieta_curso = dias_curso * 65
tri_tre = 550 if es_tri_tre else 0
prima_lifus = horas_lifus * 20 if tipo_piloto == "Comandante" else 0
prima_simulador = dias_simulador * 350 if tipo_piloto == "Comandante" else 0

# Total Devengos
total_devengos = (
    salario_base_mensual + prima_disponibilidad + plus_resp_mensual + plus_disp_mensual +
    prima_hora_vuelo + plus_nocturnidad + imaginaria + situaciones + vacaciones +
    dieta_vuelo + dieta_pernocta + dieta_curso + tri_tre + prima_lifus + prima_simulador
)

# Deducciones
seguridad_social = 129.23  # Fijo en este ejemplo
irpf = total_devengos * (irpf_porcentaje / 100)
total_deducciones = seguridad_social + irpf

# Importe Líquido
importe_liquido = total_devengos - total_deducciones

# Mostrar resultados
st.header("Resumen de la Nómina")
st.write(f"**Salario Base:** {salario_base_mensual:.2f} €")
if tipo_piloto == "Comandante":
    st.write(f"**Plus Responsabilidad:** {plus_resp_mensual:.2f} €")
    st.write(f"**Plus Disponibilidad:** {plus_disp_mensual:.2f} €")
else:
    st.write(f"**Prima Disponibilidad:** {prima_disponibilidad:.2f} €")
st.write(f"**Prima Hora Vuelo:** {prima_hora_vuelo:.2f} €")
st.write(f"**Plus Nocturnidad:** {plus_nocturnidad:.2f} €")
st.write(f"**Imaginaria:** {imaginaria:.2f} €")
st.write(f"**Situaciones > 2:** {situaciones:.2f} €")
st.write(f"**Vacaciones:** {vacaciones:.2f} €")
st.write(f"**Dieta Vuelo:** {dieta_vuelo:.2f} €")
st.write(f"**Dieta Pernocta:** {dieta_pernocta:.2f} €")
st.write(f"**Dieta Curso:** {dieta_curso:.2f} €")
if tipo_piloto == "Comandante":
    st.write(f"**Plus TRI/TRE:** {tri_tre:.2f} €")
    st.write(f"**Prima Horas LIFUS:** {prima_lifus:.2f} €")
    st.write(f"**Prima Simulador:** {prima_simulador:.2f} €")
st.write(f"**Total Devengos:** {total_devengos:.2f} €")

st.write("---")
st.write(f"**Seguridad Social:** -{seguridad_social:.2f} €")
st.write(f"**IRPF ({irpf_porcentaje}%):** -{irpf:.2f} €")
st.write(f"**Total Deducciones:** -{total_deducciones:.2f} €")

st.write("---")
st.subheader(f"**Importe Líquido:** {importe_liquido:.2f} €")

# Nota final
st.write("Nota: Los valores de Seguridad Social son fijos en esta versión. Ajusta según tus necesidades.")