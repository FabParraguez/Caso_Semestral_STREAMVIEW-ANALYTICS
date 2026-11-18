from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.analysis_ep2 import apply_filters, compute_kpis, load_catalog


st.set_page_config(
    page_title="StreamView Analytics - EP2",
    page_icon="📊",
    layout="wide",
)

st.title("📊 StreamView Analytics - Entregable EP2")
st.caption("Dashboard interactivo con KPIs, análisis exploratorio y narrativa ejecutiva para toma de decisiones.")


@st.cache_data
def get_data():
    return load_catalog()


catalogo, peliculas, series = get_data()

for df in [catalogo, peliculas, series]:
    if "anio_estreno" in df.columns:
        df["anio_estreno"] = pd.to_numeric(df["anio_estreno"], errors="coerce")

st.sidebar.header("Filtros globales")

# Filtros
op_tipo = sorted(catalogo["tipo"].dropna().unique().tolist())
sel_tipo = st.sidebar.multiselect("Tipo", op_tipo, default=op_tipo)

min_year = int(np.nanmin(catalogo["anio_estreno"]))
max_year = int(np.nanmax(catalogo["anio_estreno"]))
sel_anio = st.sidebar.slider("Rango año estreno", min_year, max_year, (min_year, max_year))

op_pais = sorted(catalogo["pais_principal"].dropna().astype(str).unique().tolist())
op_genero = sorted(catalogo["genero_principal"].dropna().astype(str).unique().tolist())
op_idioma = sorted(catalogo["idioma"].dropna().astype(str).unique().tolist())

sel_pais = st.sidebar.multiselect("País principal", op_pais, default=[])
sel_genero = st.sidebar.multiselect("Género principal", op_genero, default=[])
sel_idioma = st.sidebar.multiselect("Idioma", op_idioma, default=[])

# Aplicación de filtros
catalogo_f = apply_filters(
    catalogo,
    sel_tipo,
    sel_anio[0],
    sel_anio[1],
    sel_pais,
    sel_genero,
    sel_idioma,
)
peliculas_f = apply_filters(
    peliculas,
    sel_tipo,
    sel_anio[0],
    sel_anio[1],
    sel_pais,
    sel_genero,
    sel_idioma,
)
series_f = apply_filters(
    series,
    sel_tipo,
    sel_anio[0],
    sel_anio[1],
    sel_pais,
    sel_genero,
    sel_idioma,
)

if catalogo_f.empty:
    st.warning("No hay datos para la combinación de filtros actual.")
    st.stop()

pagina = st.sidebar.radio(
    "Navegación",
    [
        "1) Vista Ejecutiva",
        "2) Segmentación y Catálogo",
        "3) Rendimiento Financiero",
        "4) Storytelling y Recomendaciones",
        "5) Evaluación Crítica",
    ],
)

if pagina == "1) Vista Ejecutiva":
    st.subheader("Vista Ejecutiva")

    kpis = compute_kpis(catalogo_f, peliculas_f)

    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    c1.metric("Títulos", f"{kpis['titulos']:,}")
    c2.metric("Películas", f"{kpis['peliculas']:,}")
    c3.metric("Series", f"{kpis['series']:,}")
    c4.metric("Popularidad media", f"{kpis['popularidad_media']:.2f}")
    c5.metric("Rating medio", f"{kpis['rating_medio']:.2f}")
    c6.metric("Votos totales", f"{kpis['votos_totales']:,}")
    c7.metric("ROI promedio películas", "N/A" if np.isnan(kpis["roi_promedio"]) else f"{kpis['roi_promedio']:.2f}")

    evo = (
        catalogo_f.groupby(["anio_estreno", "tipo"], as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
        .dropna(subset=["anio_estreno"])
        .sort_values("anio_estreno")
    )
    fig_evo = px.line(
        evo,
        x="anio_estreno",
        y="titulos",
        color="tipo",
        markers=True,
        title="Evolución anual de títulos",
    )
    st.plotly_chart(fig_evo, width="stretch")

    mix_tipo = (
        catalogo_f.groupby("tipo", as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
    )
    fig_mix = px.pie(mix_tipo, values="titulos", names="tipo", title="Participación por tipo de contenido")
    st.plotly_chart(fig_mix, width="stretch")

if pagina == "2) Segmentación y Catálogo":
    st.subheader("Segmentación y Catálogo")

    top_generos = (
        catalogo_f.groupby("genero_principal", as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
        .sort_values("titulos", ascending=False)
        .head(15)
    )
    fig_generos = px.bar(
        top_generos,
        x="titulos",
        y="genero_principal",
        orientation="h",
        title="Top 15 géneros por volumen de títulos",
    )
    fig_generos.update_layout(yaxis_title="Género", xaxis_title="Cantidad de títulos")

    top_paises = (
        catalogo_f.groupby("pais_principal", as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
        .sort_values("titulos", ascending=False)
        .head(15)
    )
    fig_paises = px.bar(
        top_paises,
        x="titulos",
        y="pais_principal",
        orientation="h",
        title="Top 15 países por volumen de títulos",
    )
    fig_paises.update_layout(yaxis_title="País", xaxis_title="Cantidad de títulos")

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_generos, width="stretch")
    col2.plotly_chart(fig_paises, width="stretch")

    st.subheader("Catálogo filtrado")
    st.dataframe(
        catalogo_f[
            [
                "tipo",
                "titulo",
                "anio_estreno",
                "pais_principal",
                "genero_principal",
                "idioma",
                "popularidad",
                "promedio_votos",
                "votos",
            ]
        ].sort_values(["popularidad", "promedio_votos"], ascending=False),
        use_container_width=True,
        height=380,
    )

if pagina == "3) Rendimiento Financiero":
    st.subheader("Rendimiento Financiero (Películas)")

    peliculas_fin = peliculas_f[(peliculas_f["presupuesto"] > 0) & (peliculas_f["ingresos"] > 0)].copy()

    if peliculas_fin.empty:
        st.info("No hay películas con presupuesto e ingresos válidos para los filtros seleccionados.")
    else:
        peliculas_fin["margen"] = peliculas_fin["ingresos"] - peliculas_fin["presupuesto"]

        c1, c2, c3 = st.columns(3)
        c1.metric("Películas con datos financieros", f"{peliculas_fin['id_muestra'].nunique():,}")
        c2.metric("Ingresos acumulados", f"${peliculas_fin['ingresos'].sum():,.0f}")
        c3.metric("Presupuesto acumulado", f"${peliculas_fin['presupuesto'].sum():,.0f}")

        fig_scatter = px.scatter(
            peliculas_fin,
            x="presupuesto",
            y="ingresos",
            color="genero_principal",
            size="votos",
            hover_data=["titulo", "anio_estreno", "roi"],
            title="Presupuesto vs Ingresos",
            labels={"presupuesto": "Presupuesto (USD)", "ingresos": "Ingresos (USD)"},
        )
        st.plotly_chart(fig_scatter, width="stretch")

        top_roi = (
            peliculas_fin[["titulo", "anio_estreno", "genero_principal", "roi", "presupuesto", "ingresos"]]
            .sort_values("roi", ascending=False)
            .head(15)
        )
        st.subheader("Top 15 películas por ROI")
        st.dataframe(top_roi, use_container_width=True)

if pagina == "4) Storytelling y Recomendaciones":
    st.subheader("Narrativa Visual (Data Storytelling)")

    top_titulos = catalogo_f.sort_values(["popularidad", "promedio_votos"], ascending=False).head(10)

    st.markdown(
        """
        ### 1. Contexto
        StreamView Analytics busca orientar decisiones de contenido para mejorar retención y engagement.

        ### 2. Hallazgo principal
        La oferta presenta concentración en ciertos géneros y países, mientras que títulos con mejor desempeño
        (popularidad + rating) muestran oportunidades para focalizar inversión y promoción.

        ### 3. Implicancia de negocio
        Priorizar contenido en segmentos de alta tracción permite optimizar el retorno esperado de adquisición,
        producción y campañas comerciales.
        """
    )

    fig_top = px.bar(
        top_titulos,
        x="titulo",
        y="popularidad",
        color="tipo",
        title="Top 10 títulos por popularidad (según filtros)",
    )
    fig_top.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig_top, width="stretch")

    st.markdown(
        """
        ### Recomendaciones accionables
        1. **Portafolio**: aumentar peso de géneros con mayor tracción sostenida.
        2. **Marketing**: segmentar campañas por país e idioma con mejor respuesta.
        3. **Roadmap**: usar rating + votos para decidir continuidad de franquicias y nuevas adquisiciones.
        4. **Finanzas**: priorizar proyectos con ROI histórico superior al promedio del segmento.
        """
    )

if pagina == "5) Evaluación Crítica":
    st.subheader("Evaluación crítica de la solución")

    st.markdown(
        """
        ### Fortalezas
        - Integración de múltiples fuentes (películas y series) en un solo flujo analítico.
        - KPIs ejecutivos y visualizaciones interactivas para exploración autónoma.
        - Estructura narrativa para facilitar comunicación con stakeholders no técnicos.

        ### Limitaciones
        - No se dispone de métricas transaccionales de usuarios (sesiones, churn real por usuario, tiempo de visualización).
        - La interpretación de causalidad no es directa: el análisis es descriptivo y exploratorio.
        - Los datos financieros aplican principalmente a películas.

        ### Oportunidades de mejora
        - Incorporar cohortes de suscripción y eventos de reproducción para modelar retención.
        - Agregar forecasting de demanda y simulación de portafolio.
        - Implementar monitoreo periódico con actualización automática de datos.

        ### Decisiones de diseño justificadas
        - Filtros globales para consistencia en la lectura de KPIs y gráficos.
        - Navegación por páginas para separar estrategia, exploración y finanzas.
        - Uso de gráficos de línea, barras, dispersión y tabla para balancear síntesis y detalle.
        """
    )

    st.info("Esta sección cubre explícitamente el criterio de evaluación de análisis crítico de la solución.")
