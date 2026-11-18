from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.analysis_ep3 import apply_filters, compute_kpis, compute_market_insights, compute_quality_metrics, load_catalog

st.set_page_config(
    page_title="StreamView Analytics - EP3",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configuración de colores mejorada
COLORS_EP3 = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "info": "#17becf",
    "light": "#ecf0f1",
    "dark": "#2c3e50",
}

st.title("📊 StreamView Analytics - Entregable EP3")
st.caption("Dashboard optimizado con evaluación crítica, mejoras visuales y análisis profundos para decisiones estratégicas.")

@st.cache_data
def get_data():
    return load_catalog()

catalogo, peliculas, series = get_data()

for df in [catalogo, peliculas, series]:
    if "anio_estreno" in df.columns:
        df["anio_estreno"] = pd.to_numeric(df["anio_estreno"], errors="coerce")

st.sidebar.header("🎯 Filtros Globales")

op_tipo = sorted(catalogo["tipo"].dropna().unique().tolist())
sel_tipo = st.sidebar.multiselect("📺 Tipo de contenido", op_tipo, default=op_tipo, help="Selecciona películas y/o series")

min_year = int(np.nanmin(catalogo["anio_estreno"]))
max_year = int(np.nanmax(catalogo["anio_estreno"]))
sel_anio = st.sidebar.slider("📅 Rango año de estreno", min_year, max_year, (min_year, max_year), help="Filtra por período de lanzamiento")

op_pais = sorted(catalogo["pais_principal"].dropna().astype(str).unique().tolist())
op_genero = sorted(catalogo["genero_principal"].dropna().astype(str).unique().tolist())
op_idioma = sorted(catalogo["idioma"].dropna().astype(str).unique().tolist())

sel_pais = st.sidebar.multiselect("🌍 País principal", op_pais, default=[], help="Deja vacío para incluir todos")
sel_genero = st.sidebar.multiselect("🎬 Género principal", op_genero, default=[], help="Deja vacío para incluir todos")
sel_idioma = st.sidebar.multiselect("🗣️ Idioma", op_idioma, default=[], help="Deja vacío para incluir todos")

catalogo_f = apply_filters(catalogo, sel_tipo, sel_anio[0], sel_anio[1], sel_pais, sel_genero, sel_idioma)
peliculas_f = apply_filters(peliculas, sel_tipo, sel_anio[0], sel_anio[1], sel_pais, sel_genero, sel_idioma)
series_f = apply_filters(series, sel_tipo, sel_anio[0], sel_anio[1], sel_pais, sel_genero, sel_idioma)

if catalogo_f.empty:
    st.warning("⚠️ No hay datos para la combinación de filtros actual. Por favor, ajusta los criterios.")
    st.stop()

pagina = st.sidebar.radio(
    "🧭 Navegación",
    [
        "1) Vista Ejecutiva (KPIs)",
        "2) Análisis de Mercado",
        "3) Calidad de Contenido",
        "4) Rendimiento Financiero",
        "5) Segmentación y Catálogo",
        "6) Data Storytelling",
        "7) Evaluación Crítica EP3",
    ],
    help="Selecciona la sección que deseas explorar"
)

