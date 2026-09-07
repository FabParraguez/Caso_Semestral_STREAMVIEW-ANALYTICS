from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="StreamView Analytics - Dashboard EP1",
    page_icon="📊",
    layout="wide",
)


BASE_DIR = Path(__file__).resolve().parents[2]


def resolve_data_dir() -> Path:
    """
    Busca la carpeta Dataset_Utilizado partiendo desde la ubicación del script
    y subiendo por sus directorios padres.
    """
    script_path = Path(__file__).resolve()
    for parent in script_path.parents:
        candidate = parent / "Dataset_Utilizado"
        if candidate.exists() and candidate.is_dir():
            return candidate

    raise FileNotFoundError(
        "No se encontró la carpeta 'Dataset_Utilizado' en los directorios padres del script. "
        "Verifica que exista dentro de 'Caso_Semestral_STREAMVIEW-ANALYTICS'."
    )


DATA_DIR = resolve_data_dir()


@st.cache_data
def load_data():
    peliculas = pd.read_csv(DATA_DIR / "peliculas_clean.csv")
    series = pd.read_csv(DATA_DIR / "series_clean.csv")
    peliculas_genero = pd.read_csv(DATA_DIR / "peliculas_por_genero.csv")
    series_genero = pd.read_csv(DATA_DIR / "series_por_genero.csv")

    peliculas_u = peliculas.drop_duplicates(subset=["id_muestra"]).copy()
    series_u = series.drop_duplicates(subset=["id_muestra"]).copy()

    peliculas_u["tipo"] = "Pelicula"
    series_u["tipo"] = "Serie"

    common_cols = [
        "id_muestra",
        "tipo",
        "titulo",
        "anio_estreno",
        "pais_principal",
        "genero_principal",
        "idioma",
        "popularidad",
        "votos",
        "promedio_votos",
    ]
    catalogo = pd.concat(
        [peliculas_u[common_cols], series_u[common_cols]],
        ignore_index=True,
    )

    for df in [catalogo, peliculas_u, series_u, peliculas, series]:
        if "anio_estreno" in df.columns:
            df["anio_estreno"] = pd.to_numeric(df["anio_estreno"], errors="coerce")

    return catalogo, peliculas_u, series_u, peliculas, series, peliculas_genero, series_genero


catalogo, peliculas_u, series_u, peliculas, series, peliculas_genero, series_genero = load_data()


st.title("📊 StreamView Analytics - Dashboard Interactivo EP1")
st.caption("KPIs, filtros y visualizaciones para apoyar decisiones de contenido, marketing y dirección.")


st.sidebar.header("Filtros globales")

tipos_disponibles = sorted(catalogo["tipo"].dropna().unique().tolist())
tipo_sel = st.sidebar.multiselect("Tipo", options=tipos_disponibles, default=tipos_disponibles)

min_year = int(np.nanmin(catalogo["anio_estreno"]))
max_year = int(np.nanmax(catalogo["anio_estreno"]))
anio_sel = st.sidebar.slider("Rango de año de estreno", min_value=min_year, max_value=max_year, value=(min_year, max_year))

paises = sorted(catalogo["pais_principal"].dropna().astype(str).unique().tolist())
generos = sorted(catalogo["genero_principal"].dropna().astype(str).unique().tolist())
idiomas = sorted(catalogo["idioma"].dropna().astype(str).unique().tolist())

pais_sel = st.sidebar.multiselect("País principal", options=paises, default=[])
genero_sel = st.sidebar.multiselect("Género principal", options=generos, default=[])
idioma_sel = st.sidebar.multiselect("Idioma", options=idiomas, default=[])


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out[out["tipo"].isin(tipo_sel)]
    out = out[(out["anio_estreno"] >= anio_sel[0]) & (out["anio_estreno"] <= anio_sel[1])]
    if pais_sel:
        out = out[out["pais_principal"].isin(pais_sel)]
    if genero_sel:
        out = out[out["genero_principal"].isin(genero_sel)]
    if idioma_sel:
        out = out[out["idioma"].isin(idioma_sel)]
    return out


catalogo_f = apply_filters(catalogo)
peliculas_u_f = apply_filters(peliculas_u)
series_u_f = apply_filters(series_u)


if catalogo_f.empty:
    st.warning("No hay datos para la combinación de filtros seleccionada.")
    st.stop()


pagina = st.sidebar.radio(
    "Navegación",
    [
        "Vista Ejecutiva",
        "Catálogo por Segmentos",
        "Engagement",
        "Finanzas (Películas)",
    ],
)


if pagina == "Vista Ejecutiva":
    st.subheader("Vista Ejecutiva")

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    kpi1.metric("Total títulos", f"{catalogo_f['id_muestra'].nunique():,}")
    kpi2.metric("Total películas", f"{peliculas_u_f['id_muestra'].nunique():,}")
    kpi3.metric("Total series", f"{series_u_f['id_muestra'].nunique():,}")
    kpi4.metric("Popularidad promedio", f"{catalogo_f['popularidad'].mean():.2f}")
    kpi5.metric("Promedio votos", f"{catalogo_f['promedio_votos'].mean():.2f}")
    kpi6.metric("Votos totales", f"{int(catalogo_f['votos'].sum()):,}")

    titulos_anio = (
        catalogo_f.groupby(["anio_estreno", "tipo"], as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
    )
    fig_line = px.line(
        titulos_anio,
        x="anio_estreno",
        y="titulos",
        color="tipo",
        markers=True,
        title="Evolución de títulos por año de estreno",
    )
    st.plotly_chart(fig_line, use_container_width=True)

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
        height=320,
    )


elif pagina == "Catálogo por Segmentos":
    st.subheader("Catálogo por Segmentos")

    genero_base = pd.concat([peliculas_genero.assign(tipo="Pelicula"), series_genero.assign(tipo="Serie")], ignore_index=True)
    genero_base["anio_estreno"] = pd.to_numeric(genero_base["anio_estreno"], errors="coerce")
    genero_base = genero_base[genero_base["tipo"].isin(tipo_sel)]
    genero_base = genero_base[(genero_base["anio_estreno"] >= anio_sel[0]) & (genero_base["anio_estreno"] <= anio_sel[1])]
    if pais_sel:
        genero_base = genero_base[genero_base["pais_principal"].isin(pais_sel)]
    if idioma_sel:
        genero_base = genero_base[genero_base["idioma"].isin(idioma_sel)]

    top_generos = (
        genero_base.groupby("generos", as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
        .sort_values("titulos", ascending=False)
        .head(10)
    )

    pais_base = pd.concat([peliculas.assign(tipo="Pelicula"), series.assign(tipo="Serie")], ignore_index=True)
    pais_base["anio_estreno"] = pd.to_numeric(pais_base["anio_estreno"], errors="coerce")
    pais_base = pais_base[pais_base["tipo"].isin(tipo_sel)]
    pais_base = pais_base[(pais_base["anio_estreno"] >= anio_sel[0]) & (pais_base["anio_estreno"] <= anio_sel[1])]
    if genero_sel:
        pais_base = pais_base[pais_base["genero_principal"].isin(genero_sel)]
    if idioma_sel:
        pais_base = pais_base[pais_base["idioma"].isin(idioma_sel)]
    if pais_sel:
        pais_base = pais_base[pais_base["pais_principal"].isin(pais_sel)]

    top_paises = (
        pais_base.groupby("pais", as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
        .sort_values("titulos", ascending=False)
        .head(10)
    )

    col1, col2 = st.columns(2)

    with col1:
        fig_g = px.bar(
            top_generos.sort_values("titulos", ascending=True),
            x="titulos",
            y="generos",
            orientation="h",
            title="Top 10 géneros por cantidad de títulos",
            color="titulos",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig_g, use_container_width=True)

    with col2:
        fig_p = px.bar(
            top_paises.sort_values("titulos", ascending=True),
            x="titulos",
            y="pais",
            orientation="h",
            title="Top 10 países por cantidad de títulos",
            color="titulos",
            color_continuous_scale="Teal",
        )
        st.plotly_chart(fig_p, use_container_width=True)


elif pagina == "Engagement":
    st.subheader("Engagement y percepción del catálogo")

    col1, col2 = st.columns(2)

    with col1:
        fig_pop_vote = px.scatter(
            catalogo_f,
            x="popularidad",
            y="promedio_votos",
            color="tipo",
            hover_data=["titulo", "pais_principal", "genero_principal", "anio_estreno"],
            title="Popularidad vs promedio de votos",
            opacity=0.65,
        )
        st.plotly_chart(fig_pop_vote, use_container_width=True)

    with col2:
        fig_pop_count = px.scatter(
            catalogo_f,
            x="popularidad",
            y="votos",
            color="tipo",
            hover_data=["titulo", "pais_principal", "genero_principal", "anio_estreno"],
            title="Popularidad vs cantidad de votos",
            opacity=0.65,
            log_y=True,
        )
        st.plotly_chart(fig_pop_count, use_container_width=True)


elif pagina == "Finanzas (Películas)":
    st.subheader("Finanzas — Solo películas")

    pel_fin = peliculas_u_f.copy()
    if "valido_para_financiero" in pel_fin.columns:
        pel_fin = pel_fin[pel_fin["valido_para_financiero"] == True]

    if pel_fin.empty:
        st.warning("No hay películas válidas para análisis financiero con los filtros seleccionados.")
        st.stop()

    roi_promedio = pel_fin["roi"].mean()
    ingreso_total = pel_fin["ingresos"].sum()
    presupuesto_total = pel_fin["presupuesto"].sum()

    k1, k2, k3 = st.columns(3)
    k1.metric("Películas financieras válidas", f"{pel_fin['id_muestra'].nunique():,}")
    k2.metric("ROI promedio", f"{roi_promedio:.2f}")
    k3.metric("Ingresos / Presupuesto", f"{ingreso_total / presupuesto_total:.2f}")

    c1, c2 = st.columns(2)

    with c1:
        fig_fin = px.scatter(
            pel_fin,
            x="presupuesto",
            y="ingresos",
            color="genero_principal",
            hover_data=["titulo", "anio_estreno", "pais_principal", "roi"],
            title="Presupuesto vs ingresos (películas válidas)",
            log_x=True,
            log_y=True,
            opacity=0.7,
        )
        st.plotly_chart(fig_fin, use_container_width=True)

    with c2:
        fig_roi = px.histogram(
            pel_fin,
            x="roi",
            nbins=40,
            title="Distribución de ROI",
            color_discrete_sequence=["#4C78A8"],
        )
        st.plotly_chart(fig_roi, use_container_width=True)
