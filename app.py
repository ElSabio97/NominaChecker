import streamlit as st

# Configuración inicial
st.title("Calculadora de Dieta de Vuelo Tributable y Exenta")
st.sidebar.header("Datos del Piloto")

# Entradas del usuario
tipo_piloto = st.sidebar.selectbox("Tipo de Piloto", ["Primer Oficial", "Comandante"])
nivel_salarial = st.sidebar.selectbox("Nivel Salarial", ["Entrada", "1", "2", "3", "4", "5"] if tipo_piloto == "Primer Oficial" else ["1", "2", "3", "4", "5", "6", "7"])
horas_vuelo = st.sidebar.number_input("Horas de vuelo totales", min_value=0.0, step=0.01, value=49.05)
horas_nocturnas = st.sidebar.number_input("Horas de vuelo nocturnas", min_value=0.0, step=0.01, value=0.67)
dias_imaginaria = st.sidebar.number_input("Días de imaginaria", min_value=0, value=1)
dias_dieta_vuelo = st.sidebar.number_input("Días de dieta vuelo", min_value=0, value=10)
extras = st.sidebar.text_input("Extras (ej. 'Vacaciones: 80.00 €')", value="Vacaciones: 80.00 €")

# Constantes según tipo de piloto
if tipo_piloto == "Primer Oficial":
    dieta_vuelo = 65  # €/día
    prima_hora_vuelo = 25  # €/h
    plus_nocturnidad_por_hora = 12.5  # €/h
    imaginaria = 45  # €/día
else:
    dieta_vuelo = 65  # €/día
    prima_hora_vuelo = 52  # €/h
    plus_nocturnidad_por_hora = 26  # €/h
    imaginaria = 45  # €/día

# Límite exento para dieta de vuelo (ajustado según nómina real)
limite_exento_dieta = 41.85  # €/día, derivado de 418,48 / 10

# Cálculos
dieta_vuelo_total = dias_dieta_vuelo * dieta_vuelo
dieta_exenta = min(dieta_vuelo_total, dias_dieta_vuelo * limite_exento_dieta)
dieta_tributable = dieta_vuelo_total - dieta_exenta

prima_hora_vuelo_total = horas_vuelo * prima_hora_vuelo if horas_nocturnas <= 3 else horas_vuelo * prima_hora_vuelo * 1.5
plus_nocturnidad_total = horas_nocturnas * plus_nocturnidad_por_hora if horas_nocturnas <= 3 else horas_vuelo * plus_nocturnidad_por_hora
imaginaria_total = dias_imaginaria * imaginaria

# Procesar extras
extras_importe = 0.0
if extras:
    try:
        importe_str = extras.split(":")[1].split("€")[0].strip()
        extras_importe = float(importe_str)
    except:
        st.warning("Formato de 'Extras' incorrecto. Usa 'Concepto: 80.00 €'.")

# Mostrar resultados
st.header("Resumen")
st.write(f"**Prima Hora Vuelo:** {prima_hora_vuelo_total:.2f} €")
st.write(f"**Plus Nocturnidad:** {plus_nocturnidad_total:.2f} €")
st.write(f"**Imaginaria:** {imaginaria_total:.2f} €")
st.write(f"**Dieta Vuelo Total:** {dieta_vuelo_total:.2f} €")
st.write(f"**Dieta Vuelo Exenta:** {dieta_exenta:.2f} €")
st.write(f"**Dieta Vuelo Tributable:** {dieta_tributable:.2f} €")
if extras_importe > 0:
    st.write(f"**Extras:** {extras} ({extras_importe:.2f} €)")

st.write("Nota: El límite exento de dieta se ajusta a 41,85 €/día según nómina real.")
