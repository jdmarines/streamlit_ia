import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# Configuración de la página
# ----------------------------
st.set_page_config(page_title="EDA con Datos Aleatorios", layout="wide")

st.title("📊 Análisis Exploratorio de Datos (EDA) con Datos Aleatorios")
st.markdown("Este dashboard muestra un ejemplo simple de visualización con datos generados aleatoriamente.")

# ----------------------------
# Generar datos aleatorios
# ----------------------------
np.random.seed(42)  # Reproducibilidad
n_rows = st.slider("Número de filas", 10, 200, 50)

data = pd.DataFrame({
    "Categoría": np.random.choice(["A", "B", "C", "D"], size=n_rows),
    "Valor 1": np.random.randint(10, 100, size=n_rows),
    "Valor 2": np.random.randint(5, 50, size=n_rows),
    "Fecha": pd.date_range(start="2024-01-01", periods=n_rows, freq="D")
})

st.subheader("📋 Vista previa de los datos")
st.dataframe(data.head())

# ----------------------------
# Resumen estadístico
# ----------------------------
st.subheader("📈 Resumen estadístico")
st.write(data.describe())

# ----------------------------
# Gráfico de barras
# ----------------------------
st.subheader("📊 Gráfico de barras - Suma por categoría")
bar_data = data.groupby("Categoría")[["Valor 1", "Valor 2"]].sum().reset_index()
fig_bar = px.bar(bar_data, x="Categoría", y=["Valor 1", "Valor 2"],
                 barmode="group", title="Valores por Categoría")
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------
# Gráfico de líneas
# ----------------------------
st.subheader("📈 Gráfico de líneas - Evolución temporal de Valor 1")
line_data = data.sort_values("Fecha")
fig_line = px.line(line_data, x="Fecha", y="Valor 1",
                   title="Evolución de Valor 1 en el tiempo",
                   markers=True)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.markdown("Hecho con ❤️ usando [Streamlit](https://streamlit.io/)")
#Codigo de la serpiente
