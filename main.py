import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="📊 EDA Deportivo Interactivo", layout="wide")

st.title("🏆 Explorador de Datos Deportivos")
st.markdown("Interactúa con filtros, botones y gráficos para explorar datos deportivos ficticios.")

# ----------------------------
# Función para generar datos deportivos ficticios
# ----------------------------
def generar_datos(filas=500, seed=None):
    if seed:
        np.random.seed(seed)

    deportes = ["Fútbol", "Baloncesto", "Tenis", "Béisbol", "Ciclismo"]
    paises = ["España", "Brasil", "EE.UU.", "Argentina", "Francia", "Colombia"]

    data = pd.DataFrame({
        "Fecha": pd.date_range(start="2024-01-01", periods=filas, freq="D"),
        "Deporte": np.random.choice(deportes, size=filas),
        "País": np.random.choice(paises, size=filas),
        "Jugador": [f"Jugador_{i}" for i in range(1, filas + 1)],
        "Puntos": np.random.randint(0, 50, size=filas),
        "Asistencias": np.random.randint(0, 15, size=filas),
        "Rebotes": np.random.randint(0, 20, size=filas),
        "Faltas": np.random.randint(0, 10, size=filas),
        "Minutos Jugados": np.random.randint(10, 90, size=filas),
        "Partidos Jugados": np.random.randint(1, 30, size=filas)
    })

    return data

# ----------------------------
# Generación y control de datos
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = generar_datos()

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🔄 Regenerar datos"):
        st.session_state.data = generar_datos(seed=np.random.randint(0, 10000))

# ----------------------------
# Filtros interactivos
# ----------------------------
st.sidebar.header("🎯 Filtros")
deporte_sel = st.sidebar.multiselect(
    "Selecciona deporte(s):",
    options=st.session_state.data["Deporte"].unique(),
    default=st.session_state.data["Deporte"].unique()
)
pais_sel = st.sidebar.multiselect(
    "Selecciona país(es):",
    options=st.session_state.data["País"].unique(),
    default=st.session_state.data["País"].unique()
)
fecha_rango = st.sidebar.date_input(
    "Rango de fechas:",
    [st.session_state.data["Fecha"].min(), st.session_state.data["Fecha"].max()]
)

# Filtrado
data_filtrada = st.session_state.data[
    (st.session_state.data["Deporte"].isin(deporte_sel)) &
    (st.session_state.data["País"].isin(pais_sel)) &
    (st.session_state.data["Fecha"] >= pd.to_datetime(fecha_rango[0])) &
    (st.session_state.data["Fecha"] <= pd.to_datetime(fecha_rango[1]))
]

# ----------------------------
# Mostrar datos y estadísticas
# ----------------------------
if st.checkbox("📋 Mostrar tabla de datos"):
    st.dataframe(data_filtrada, use_container_width=True)

if st.checkbox("📈 Mostrar estadísticas descriptivas"):
    st.write(data_filtrada.describe())

# ----------------------------
# Visualizaciones
# ----------------------------
st.subheader("📊 Gráfico de Barras - Puntos promedio por deporte")
bar_data = data_filtrada.groupby("Deporte")["Puntos"].mean().reset_index()
fig_bar = px.bar(bar_data, x="Deporte", y="Puntos", color="Deporte",
                 title="Puntos promedio por deporte")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("📈 Gráfico de Líneas - Evolución de Puntos en el tiempo")
line_data = data_filtrada.groupby("Fecha")["Puntos"].mean().reset_index()
fig_line = px.line(line_data, x="Fecha", y="Puntos",
                   title="Evolución promedio de puntos en el tiempo",
                   markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# ----------------------------
# Mensaje final
# ----------------------------
st.markdown("---")
st.markdown("Hecho con ❤️ y 🏟️ usando [Streamlit](https://streamlit.io/)")
