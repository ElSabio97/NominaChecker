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
    prima_hora_vuelo = 25  # €/h en 2025
    plus_nocturnidad_factor = 1.5  # Factor para horas nocturnas
    plus_nocturnidad_por_hora = 12.5  # 25 × 0.5 = 12,5 €/hora para copilotos
    imaginaria = 45  # €/día
    compensacion_vacaciones = 95  # €/día
    dieta_vuelo = 65  # €/día
    dieta_pernocta = 95  # €/día
    dieta_curso = 70  # €/día
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
    prima_hora_vuelo = 52  # €/h en 2025
    plus_nocturnidad_factor = 1.5  # Factor para horas nocturnas
    plus_nocturnidad_por_hora = 26  # 52 × 0.5 = 26 €/hora para comandantes
    imaginaria = 45  # €/día
    compensacion_vacaciones = 95  # €/día
    dieta_vuelo = 65  # €/día
    dieta_pernocta = 95  # €/día
    dieta_curso = 70  # €/día
    tri_tre = 600  # €/mes en 2025
    prima_lifus = 25  # €/h en 2025

nivel_salarial = st.sidebar.selectbox(
    "Nivel Salarial",
    options=niveles,
    help="Selecciona tu nivel salarial"
)

# Días de alta en el mes (fixed step to integer)
dias_alta = st.sidebar.slider("Días de alta en el mes", 1, 31, 30, step=1)

# Entradas para conceptos variables (step de 0.01 para horas)
horas_vuelo = st.sidebar.number_input("Horas de vuelo totales", min_value=0.0, step=0.01, value=0.0)
horas_nocturnas = st.sidebar.number_input("Horas de vuelo nocturnas", min_value=0.0, step=0.01, value=0.0)
horas_sparring = st.sidebar.number_input("Horas de sparring", min_value=0.0, step=0.01, value=0.0)
dias_imaginaria = st.sidebar.number_input("Días de imaginaria", min_value=0, value=0)
dias_dieta_vuelo = st.sidebar.number_input("Días de dieta vuelo", min_value=0, value=0)
dias_pernocta = st.sidebar.number_input("Días de pernocta", min_value=0, value=0)
dias_curso = st.sidebar.number_input("Días de dieta curso", min_value=0, value=0)
dias_vacaciones = st.sidebar.number_input("Días de vacaciones", min_value=0, value=0)

# Conceptos exclusivos de Comandantes
if tipo_piloto == "Comandante":
    es_tri_tre = st.sidebar.checkbox("¿Eres TRI/TRE?", value=False)
    horas_lifus = st.sidebar.number_input("Horas de vuelo LIFUS", min_value=0.0, step=0.01, value=0.0)
else:
    es_tri_tre, horas_lifus = False, 0.0

# Porcentaje de retención IRPF
irpf_porcentaje = st.sidebar.number_input("Retención IRPF (%)", min_value=0.0, step=0.01, value=0.0)

# Campo simplificado para "Extras"
st.sidebar.header("Conceptos Extras")
extras = st.sidebar.text_input(
    "Extras (ej. 'Media Días Vacaciones R: 80.00 € - Concepto no claro')",
    value="",
    help="Introduce conceptos adicionales con su importe y notas, si aplica."
)

# Cálculo de Devengos
salario_base_mensual = (salarios_base_anual[nivel_salarial] / 12) * (dias_alta / 30)
prima_disponibilidad_mensual = (prima_disponibilidad_anual[nivel_salarial] / 12) * (dias_alta / 30)
prima_responsabilidad_mensual = (prima_responsabilidad_anual[nivel_salarial] / 12) * (dias_alta / 30) if tipo_piloto == "Comandante" else 0

# Prima hora de vuelo y Plus de Nocturnidad
if horas_nocturnas > 0:
    if horas_nocturnas > 3:
        # Si las horas nocturnas superan 3 horas, todas las horas del servicio se factorizan por 1,5
        prima_hora_vuelo_total = horas_vuelo * prima_hora_vuelo  # Base
        plus_nocturnidad_total = horas_vuelo * plus_nocturnidad_por_hora  # Plus adicional
    else:
        # Solo las horas nocturnas se factorizan por 1,5
        horas_diurnas = horas_vuelo - horas_nocturnas
        prima_hora_vuelo_total = (horas_diurnas * prima_hora_vuelo) + (horas_nocturnas * prima_hora_vuelo)
        plus_nocturnidad_total = horas_nocturnas * plus_nocturnidad_por_hora
else:
    prima_hora_vuelo_total = horas_vuelo * prima_hora_vuelo
    plus_nocturnidad_total = 0.0

# Prima sparring (igual a prima hora de vuelo)
prima_sparring_total = horas_sparring * prima_hora_vuelo

imaginaria_total = dias_imaginaria * imaginaria
dieta_vuelo_total = dias_dieta_vuelo * dieta_vuelo
dieta_pernocta_total = dias_pernocta * dieta_pernocta
dieta_curso_total = dias_curso * dieta_curso
vacaciones_total = dias_vacaciones * compensacion_vacaciones
tri_tre_total = tri_tre if es_tri_tre else 0
prima_lifus_total = horas_lifus * prima_lifus if tipo_piloto == "Comandante" else 0

# Total Devengos (sin incluir Extras por ahora)
total_devengos = (
    salario_base_mensual + prima_disponibilidad_mensual + prima_responsabilidad_mensual +
    prima_hora_vuelo_total + plus_nocturnidad_total + prima_sparring_total + imaginaria_total +
    dieta_vuelo_total + dieta_pernocta_total + dieta_curso_total + vacaciones_total +
    tri_tre_total + prima_lifus_total
)

# Procesar el campo "Extras" para extraer el importe (si existe)
extras_importe = 0.0
if extras:
    try:
        # Buscar el importe en el texto (esperamos un formato como "Concepto: 80.00 € - Notas")
        partes = extras.split("€")
        importe_str = partes[0].split(":")[-1].strip()
        extras_importe = float(importe_str)
        total_devengos += extras_importe
    except (IndexError, ValueError):
        st.warning("Formato de 'Extras' incorrecto. Usa un formato como 'Concepto: 80.00 € - Notas'.")

# Deducciones (Seguridad Social en standby)
seguridad_social = 129.23  # Fijo por ahora
irpf = total_devengos * (irpf_porcentaje / 100)
total_deducciones = seguridad_social + irpf

# Importe Líquido
importe_liquido = total_devengos - total_deducciones

# Mostrar resultados
st.header("Resumen de la Nómina")
st.write(f"**Salario Base:** {salario_base_mensual:.2f} €")
st.write(f"**Prima Disponibilidad:** {prima_disponibilidad_mensual:.2f} €")
if tipo_piloto == "Comandante":
    st.write(f"**Prima Responsabilidad:** {prima_responsabilidad_mensual:.2f} €")
st.write(f"**Prima Hora Vuelo Total:** {prima_hora_vuelo_total:.2f} €")
if plus_nocturnidad_total > 0:
    st.write(f"**Plus Nocturnidad:** {plus_nocturnidad_total:.2f} €")
st.write(f"**Prima Horas Sparring:** {prima_sparring_total:.2f} €")
st.write(f"**Imaginaria:** {imaginaria_total:.2f} €")
st.write(f"**Dieta Vuelo:** {dieta_vuelo_total:.2f} €")
st.write(f"**Dieta Pernocta:** {dieta_pernocta_total:.2f} €")
st.write(f"**Dieta Curso:** {dieta_curso_total:.2f} €")
st.write(f"**Compensación Vacaciones:** {vacaciones_total:.2f} €")
if tipo_piloto == "Comandante":
    st.write(f"**Plus TRI/TRE:** {tri_tre_total:.2f} €")
    st.write(f"**Prima Horas LIFUS:** {prima_lifus_total:.2f} €")

# Mostrar concepto extra si existe
if extras:
    st.subheader("Conceptos Extras")
    st.write(f"**Extras:** {extras} ({extras_importe:.2f} €)")

st.subheader(f"**Total Devengos:** {total_devengos:.2f} €")

st.write("---")
st.write(f"**Seguridad Social:** -{seguridad_social:.2f} €")
st.write(f"**IRPF ({irpf_porcentaje}%):** -{irpf:.2f} €")
st.write(f"**Total Deducciones:** -{total_deducciones:.2f} €")

st.write("---")
st.subheader(f"**Importe Líquido:** {importe_liquido:.2f} €")

# Nota final
st.write("Nota: Los valores de Seguridad Social son fijos en esta versión. Ajusta según tus necesidades.")
